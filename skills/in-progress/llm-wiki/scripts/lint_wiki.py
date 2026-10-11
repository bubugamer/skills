#!/usr/bin/env python3
"""Lint the wiki for health issues: broken links, orphan pages, stale content, etc."""

import argparse
import json
import re
from pathlib import Path
from datetime import date, timedelta


def extract_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from a markdown file."""
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, content

    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value:
                fm[key] = value
    return fm, content[match.end() :]


def find_wiki_links(content: str) -> list[str]:
    """Find all [[...]] wiki links in content (strips #section anchors)."""
    raw = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)
    return [link.split("#")[0] for link in raw]


def find_markdown_links(content: str) -> list[str]:
    """Find all [text](file.md) markdown links in content (strips #section anchors)."""
    raw = re.findall(r"\[(?:[^\]]*)\]\(([^)]+)\)", content)
    # Only keep relative .md links, strip anchors and query strings
    result = []
    for link in raw:
        if link.startswith("http") or link.startswith("#"):
            continue
        link = link.split("#")[0].split("?")[0]
        if link:
            result.append(link)
    return result


def get_wiki_pages(root: Path) -> list[Path]:
    """Get all wiki pages (excluding index and hidden files)."""
    pages = []
    for f in sorted(root.rglob("*.md")):
        if f.name.startswith("_") or f.name.startswith("."):
            continue
        rel = f.relative_to(root)
        if any(part.startswith("_") for part in rel.parts):
            continue
        pages.append(f)
    return pages


def resolve_link(root: Path, link: str, all_pages: list[Path]) -> bool:
    """Try to resolve a wiki link to an existing file."""
    link = link.strip()

    # Direct path match
    if (root / link).exists():
        return True
    # With .md extension
    if (root / f"{link}.md").exists():
        return True
    # Stem match (filename without extension)
    link_stem = Path(link).stem
    for page in all_pages:
        if page.stem == link_stem:
            return True
    return False


# --- Check functions ---


def check_broken_links(root: Path, pages: list[Path]) -> list[dict]:
    """Check for broken internal links."""
    issues = []
    for page in pages:
        content = page.read_text(encoding="utf-8")
        links = find_wiki_links(content)
        for link in links:
            if not resolve_link(root, link, pages):
                issues.append(
                    {
                        "source": str(page.relative_to(root)),
                        "link": link,
                    }
                )
    return issues


def check_index_sync(root: Path, pages: list[Path]) -> list[dict]:
    """Check that index and pages are in sync."""
    index_path = root / "index.md"
    issues = []

    if not index_path.exists():
        return [{"type": "missing_index", "detail": "index.md does not exist"}]

    index_content = index_path.read_text(encoding="utf-8")
    # Collect both [[wiki]] and [text](file.md) style links
    wiki_links = set(find_wiki_links(index_content))
    md_links = set(find_markdown_links(index_content))
    all_index_links = wiki_links | md_links
    indexed_stems = {Path(link).stem for link in all_index_links}

    # Also check mkdocs.yml nav for indexed pages
    mkdocs_path = root.parent / "mkdocs.yml" if (root.parent / "mkdocs.yml").exists() else None
    if mkdocs_path:
        mkdocs_content = mkdocs_path.read_text(encoding="utf-8")
        nav_files = re.findall(r":\s+(\S+\.md)\s*$", mkdocs_content, re.MULTILINE)
        for nf in nav_files:
            indexed_stems.add(Path(nf).stem)

    # Pages not in index or nav
    for page in pages:
        if page.stem not in indexed_stems:
            issues.append(
                {
                    "type": "not_in_index",
                    "page": str(page.relative_to(root)),
                }
            )

    # Index entries pointing to missing files
    for link in all_index_links:
        if not resolve_link(root, link, pages):
            issues.append(
                {
                    "type": "dangling_index_entry",
                    "link": link,
                }
            )

    return issues


def check_conflicts(root: Path, pages: list[Path]) -> list[dict]:
    """Find pages with unresolved conflict markers."""
    issues = []
    for page in pages:
        content = page.read_text(encoding="utf-8")
        markers = re.findall(r"<!--\s*status:\s*待核验\s*-->", content)
        if markers:
            issues.append(
                {
                    "page": str(page.relative_to(root)),
                    "count": len(markers),
                }
            )
    return issues


def check_stale_pages(root: Path, pages: list[Path], days: int = 180) -> list[dict]:
    """Find pages not updated in a long time."""
    issues = []
    cutoff = date.today() - timedelta(days=days)

    for page in pages:
        fm, _ = extract_frontmatter(page)
        last_updated = fm.get("last_updated", "")
        if last_updated:
            try:
                updated_date = date.fromisoformat(last_updated)
                if updated_date < cutoff:
                    age = (date.today() - updated_date).days
                    issues.append(
                        {
                            "page": str(page.relative_to(root)),
                            "last_updated": last_updated,
                            "age_days": age,
                        }
                    )
            except ValueError:
                pass
    return issues


def check_orphans(root: Path, pages: list[Path]) -> list[dict]:
    """Find pages not linked from any other page."""
    linked_from: dict[str, set[str]] = {p.stem: set() for p in pages}

    # Check cross-links between pages (both wiki and markdown link styles)
    for page in pages:
        content = page.read_text(encoding="utf-8")
        for link in find_wiki_links(content):
            stem = Path(link).stem
            if stem in linked_from:
                linked_from[stem].add(page.stem)
        for link in find_markdown_links(content):
            stem = Path(link).stem
            if stem in linked_from:
                linked_from[stem].add(page.stem)

    # Check index links
    index_path = root / "index.md"
    if index_path.exists():
        index_content = index_path.read_text(encoding="utf-8")
        for link in find_wiki_links(index_content) + find_markdown_links(index_content):
            stem = Path(link).stem
            if stem in linked_from:
                linked_from[stem].add("index")

    # Check mkdocs.yml nav
    mkdocs_path = root.parent / "mkdocs.yml" if (root.parent / "mkdocs.yml").exists() else None
    if mkdocs_path:
        mkdocs_content = mkdocs_path.read_text(encoding="utf-8")
        nav_files = re.findall(r":\s+(\S+\.md)\s*$", mkdocs_content, re.MULTILINE)
        for nf in nav_files:
            stem = Path(nf).stem
            if stem in linked_from:
                linked_from[stem].add("mkdocs_nav")

    # Orphans: only in nav/index or not linked at all
    issues = []
    for page in pages:
        sources = linked_from.get(page.stem, set())
        non_nav = sources - {"index", "mkdocs_nav"}
        if not non_nav:
            issues.append(
                {
                    "page": str(page.relative_to(root)),
                    "in_index": "index" in sources,
                }
            )
    return issues


def check_missing_sources(root: Path, pages: list[Path]) -> list[dict]:
    """Find pages with empty or missing sources frontmatter (skips topic pages)."""
    issues = []
    for page in pages:
        fm, _ = extract_frontmatter(page)
        # Skip topic overview pages — they don't need sources
        if fm.get("type") == "topic":
            continue
        sources = fm.get("sources", "")
        if not sources or sources in ("[]", ""):
            issues.append({"page": str(page.relative_to(root))})
    return issues


def check_old_drafts(root: Path, pages: list[Path], days: int = 30) -> list[dict]:
    """Find draft pages older than threshold."""
    issues = []
    cutoff = date.today() - timedelta(days=days)

    for page in pages:
        fm, _ = extract_frontmatter(page)
        if fm.get("status") == "草稿":
            created = fm.get("created", "")
            if created:
                try:
                    created_date = date.fromisoformat(created)
                    if created_date < cutoff:
                        age = (date.today() - created_date).days
                        issues.append(
                            {
                                "page": str(page.relative_to(root)),
                                "created": created,
                                "age_days": age,
                            }
                        )
                except ValueError:
                    pass
    return issues


# --- Output ---


def print_report(
    pages: list[Path],
    broken_links: list,
    index_sync: list,
    conflicts: list,
    stale: list,
    orphans: list,
    missing_sources: list,
    old_drafts: list,
):
    """Print a human-readable lint report."""
    broken_count = len(broken_links) + len(index_sync)
    stale_count = len(conflicts) + len(stale)
    orphan_count = len(orphans)
    incomplete_count = len(missing_sources) + len(old_drafts)
    total = broken_count + stale_count + orphan_count + incomplete_count

    print(f"Wiki Lint Report ({len(pages)} pages scanned)")
    print("=" * 44)
    print(f"  Broken:     {broken_count}")
    print(f"  Stale:      {stale_count}")
    print(f"  Orphan:     {orphan_count}")
    print(f"  Incomplete: {incomplete_count}")
    print(f"  Total:      {total}")
    print()

    if broken_links:
        print("## Broken Links")
        for issue in broken_links:
            print(f"  {issue['source']} → [[{issue['link']}]] (not found)")
        print()

    if index_sync:
        print("## Index Sync Issues")
        for issue in index_sync:
            if issue.get("type") == "missing_index":
                print(f"  {issue['detail']}")
            elif issue.get("type") == "not_in_index":
                print(f"  Not in index: {issue['page']}")
            elif issue.get("type") == "dangling_index_entry":
                print(f"  Dangling index entry: [[{issue['link']}]]")
        print()

    if conflicts:
        print("## Unresolved Conflicts")
        for issue in conflicts:
            print(f"  {issue['page']} ({issue['count']} 待核验 marker(s))")
        print()

    if stale:
        print("## Stale Pages (>6 months)")
        for issue in stale:
            print(
                f"  {issue['page']} (last updated: {issue['last_updated']}, {issue['age_days']}d ago)"
            )
        print()

    if orphans:
        print("## Orphan Pages")
        for issue in orphans:
            idx = "(in index)" if issue["in_index"] else "(NOT in index)"
            print(f"  {issue['page']} {idx}")
        print()

    if missing_sources:
        print("## Missing Sources")
        for issue in missing_sources:
            print(f"  {issue['page']}")
        print()

    if old_drafts:
        print("## Old Drafts (>30 days)")
        for issue in old_drafts:
            print(
                f"  {issue['page']} (created: {issue['created']}, {issue['age_days']}d ago)"
            )
        print()

    if total == 0:
        print("All clear! No issues found.")


def main():
    parser = argparse.ArgumentParser(description="Lint wiki for health issues")
    parser.add_argument("--root", required=True, help="Wiki root directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        return 1

    pages = get_wiki_pages(root)
    if not pages:
        print("No wiki pages found.")
        return 0

    # Run all checks
    broken_links = check_broken_links(root, pages)
    index_sync = check_index_sync(root, pages)
    conflicts = check_conflicts(root, pages)
    stale = check_stale_pages(root, pages)
    orphans = check_orphans(root, pages)
    missing_sources = check_missing_sources(root, pages)
    old_drafts = check_old_drafts(root, pages)

    if args.json:
        result = {
            "summary": {
                "pages_scanned": len(pages),
                "broken": len(broken_links) + len(index_sync),
                "stale": len(conflicts) + len(stale),
                "orphan": len(orphans),
                "incomplete": len(missing_sources) + len(old_drafts),
            },
            "broken_links": broken_links,
            "index_sync": index_sync,
            "conflicts": conflicts,
            "stale": stale,
            "orphans": orphans,
            "missing_sources": missing_sources,
            "old_drafts": old_drafts,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_report(
            pages,
            broken_links,
            index_sync,
            conflicts,
            stale,
            orphans,
            missing_sources,
            old_drafts,
        )

    return 0


if __name__ == "__main__":
    exit(main())
