# Lint Rules

Health checks for the wiki. Grouped by severity — address Broken issues first, then Stale, then Orphan, then Incomplete.

## Broken (must fix)

These issues mean something is actively wrong.

### Broken Internal Links

- Scan all `[[...]]` links in wiki pages.
- Check that each target file exists (try stem match, relative path, and `.md` extension).
- Report: source page, broken link text, expected path.

### Index Desync

- Every `.md` file in the wiki root (excluding files starting with `_`) should appear in `_wiki-index.md`.
- Every entry in the index should point to an existing file.
- Report: files missing from index, index entries pointing to missing files.

## Stale (should review)

These issues mean content might be outdated but isn't necessarily wrong.

### Unresolved Conflicts

- Find pages containing `<!-- status: 待核验 -->` markers.
- Report: page, section containing the marker, how long it has been marked.
- These represent explicit "two versions coexist" situations that need the user's judgment.

### Old Pages

- Find pages where `last_updated` is more than 6 months ago.
- Report: page, last_updated date, age in days.
- Important: old does not mean wrong. This is a review prompt — the user decides whether the content still holds. Don't auto-flag these as errors.

## Orphan (should link)

These issues mean the wiki's navigability could be improved.

### Unlinked Pages

- Find pages that are not linked from any other page (only appearing in the index, or not even there).
- Report: page, whether it appears in the index.
- Orphan pages aren't broken — they're just harder to discover. Adding cross-links from related pages improves the wiki's network.

## Incomplete (nice to fix)

These issues are about quality and completeness, not correctness.

### Missing Sources

- Find pages where `sources` frontmatter is empty or `[]`.
- Find sections that make specific factual claims but have no inline source reference.
- Report: page, section.
- This matters because unsourced claims are harder to verify later. But don't be overly pedantic — common knowledge and the user's own synthesis don't need citations.

### Old Drafts

- Find pages with `status: 草稿` that were created more than 30 days ago.
- Report: page, created date, age in days.
- These pages may need attention (promote to 已看过 after review) or may have been abandoned.

## Running Lint

### Mechanical checks (use scripts)

If `scripts/lint_wiki.py` exists, run it first for all checks that can be done programmatically:
- Broken links
- Index desync
- Missing frontmatter fields
- Orphan pages
- Old pages by date

### Semantic checks (use judgment)

After the script, do a quick scan for things scripts can't catch:
- Whether "old" pages are actually outdated vs. still accurate
- Whether claims really need sources or are reasonable synthesis
- Whether orphan pages should be linked from specific related pages

## Report Format

```
## Wiki Health Report

Scanned: N pages
Date: YYYY-MM-DD

### Summary

- Broken: N
- Stale: N
- Orphan: N
- Incomplete: N

### Broken
(details)

### Stale
(details)

### Orphan
(details)

### Incomplete
(details)

### Suggested Actions
(prioritized list of what to fix, with the user deciding scope)
```
