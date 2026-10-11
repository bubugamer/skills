#!/usr/bin/env python3
"""Rebuild index.md by scanning all wiki pages in the wiki root."""

import argparse
import re
from pathlib import Path
from datetime import date


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


def extract_summary(body: str) -> str:
    """Extract the one-line summary (first blockquote line after frontmatter)."""
    for line in body.split("\n"):
        stripped = line.strip()
        if stripped.startswith(">"):
            return stripped.lstrip(">").strip()
    return ""


def get_wiki_pages(root: Path) -> list[Path]:
    """Get all wiki pages, excluding index/hidden/internal files."""
    pages = []
    for f in sorted(root.rglob("*.md")):
        if f.name.startswith("_") or f.name.startswith("."):
            continue
        # Skip files in _archive or other internal directories
        rel = f.relative_to(root)
        if any(part.startswith("_") for part in rel.parts):
            continue
        pages.append(f)
    return pages


def scan_pages(root: Path) -> list[dict]:
    """Scan all wiki pages and extract metadata."""
    pages = get_wiki_pages(root)
    results = []

    for f in pages:
        fm, body = extract_frontmatter(f)
        summary = extract_summary(body)
        rel = f.relative_to(root)

        results.append(
            {
                "path": rel,
                "title": fm.get("title", f.stem),
                "status": fm.get("status", "未知"),
                "last_updated": fm.get("last_updated", ""),
                "summary": summary,
            }
        )

    return results


def group_by_category(pages: list[dict]) -> dict[str, list[dict]]:
    """Group pages by their top-level parent directory."""
    groups: dict[str, list[dict]] = {}
    for page in pages:
        parts = page["path"].parts
        category = parts[0] if len(parts) > 1 else "未分类"
        groups.setdefault(category, []).append(page)
    return groups


def build_index(pages: list[dict]) -> str:
    """Build the index markdown content."""
    lines = [
        "# Wiki Index",
        "",
        f"Last rebuilt: {date.today().isoformat()}",
        "",
    ]

    groups = group_by_category(pages)

    for category in sorted(groups.keys()):
        lines.append(f"## {category}")
        lines.append("")
        for page in sorted(groups[category], key=lambda p: p["title"]):
            summary_part = f" — {page['summary']}" if page["summary"] else ""
            # Use Obsidian-style wiki links
            lines.append(f"- [[{page['path']}|{page['title']}]]{summary_part}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rebuild wiki index")
    parser.add_argument("--root", required=True, help="Wiki root directory")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print index without writing"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        return 1

    pages = scan_pages(root)
    index_content = build_index(pages)

    if args.dry_run:
        print(index_content)
        print(f"\n--- {len(pages)} pages found ---")
    else:
        index_path = root / "index.md"
        index_path.write_text(index_content, encoding="utf-8")
        print(f"Rebuilt index at {index_path} ({len(pages)} pages)")

    return 0


if __name__ == "__main__":
    exit(main())
