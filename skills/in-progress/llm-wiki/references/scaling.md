# Scaling the Wiki

Read this when `_wiki-index.md` exceeds ~80 entries. Until then, a single flat index works fine — don't pre-optimize.

## Medium Scale (80–200 pages)

### Split the Index

Replace the single `_wiki-index.md` with a two-level structure:

- `_wiki-index.md` — top-level hub: lists topic categories with links to sub-indexes
- `_index-<category>.md` — one per major category, listing pages in that category with summaries

Example top-level:

```markdown
# Wiki Index

Last rebuilt: 2026-04-13

## Categories

- [[_index-编程]] — Programming languages, frameworks, and tools (23 pages)
- [[_index-产品]] — Product thinking, design, and user research (15 pages)
- [[_index-AI]] — Machine learning, LLMs, and AI applications (31 pages)
```

### Maintain Page Summaries

Ensure every page's opening `> summary` line is current. Sub-indexes can echo these summaries so you can navigate without opening every page.

### Review Category Boundaries

- Categories with >30 pages may need splitting.
- Categories with <3 pages may need merging into a parent or neighbor.
- Let categories emerge from content — don't force a taxonomy.

## Large Scale (200+ pages)

At this scale, consider these additional measures. Apply them one at a time, only when you actually hit the pain point.

### Topic Maps

Create overview pages that show how major topics relate — not just flat lists, but relationship diagrams or structured narratives. These serve as "you are here" guides for navigating dense knowledge areas.

### Lightweight Search

If scanning indexes becomes too slow or imprecise, consider adding a lightweight search layer. But exhaust simpler options first:

1. Better page titles and summaries
2. More cross-links between related pages
3. Better category structure
4. A "recent changes" log that tracks the last N updates

Only after these prove insufficient should you consider external search tooling.

### Archival

Some pages will become irrelevant over time. Move them to a `_archive/` subdirectory rather than deleting:

- Remove from the active index
- Keep discoverable via archive index
- Preserve for historical reference

### Change Log

At this scale, a `_changelog.md` that records significant wiki edits (page created, major update, conflict resolved) becomes valuable for understanding what changed and when.

## General Principles

- Don't pre-optimize. Only apply scaling measures when you actually hit the pain point.
- Each scaling step should be reversible.
- The wiki must remain fully functional as plain Markdown files. No external tool should be required to read or navigate it.
- If a scaling measure makes the wiki harder for a human to use, it's not worth it.
