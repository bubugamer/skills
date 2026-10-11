# PARA Rebuild

Treat PARA rebuild as a staged workflow that uses most of the skill's other capabilities.

PARA is a second-layer action model, not a license to ignore an already meaningful workspace taxonomy.

## Execution Order

1. Initialize `_catalog`.
2. Scan the workspace.
3. Build inventory and statistics.
4. Detect whether the workspace already has a meaningful top-level taxonomy.
5. Detect duplicate names, exact duplicates, junk candidates, and residual candidates.
6. Enrich semantics with filenames, readable content, metadata, and optional OCR or vision.
7. Decide reorganization granularity.
8. Classify units into `Projects`, `Areas`, `Resources`, or `Archives`.
9. Generate target paths and fallback routes.
10. Validate the plan.
11. Execute only after user confirmation.

## Existing Taxonomy First

Before moving anything, ask whether the current workspace already has a stable structure.

- If the workspace uses coded top-level categories such as `01-*`, `02-*`, `03-*`, `09-*`, `10-*`, treat that as a meaningful taxonomy.
- If root-level note files such as `编码说明*.txt` exist, treat them as evidence that the current structure is intentional.
- If a top-level directory is already a coherent archive, library, topic area, or cleanup pool, preserve it as a directory unit before considering deeper splits.
- `_catalog` remains internal and is never part of this reasoning.

## Granularity Logic

Do not flatten everything to file level by default.

- Move a directory as a single unit when:
  - its topic is cohesive,
  - its dominant PARA bucket is clear,
  - its internal structure has value worth preserving.
- Split to child directories when:
  - the parent mixes several stable groups,
  - the children themselves look coherent.
- Split to files only when:
  - the parent and its children are still mixed,
  - keeping the container would preserve disorder.

Preserve containers more aggressively when:

- the directory is a coded top-level category in an already organized workspace,
- the directory is obviously an archive, backup, restore, duplicate-photo, or cleanup container,
- the directory is mostly media with generic camera-style filenames and the collection context is more meaningful than any individual filename.

## Non-Overlapping Unit Rule

The final execution units must not overlap.

- If `A` moves as a directory unit, do not also move `A/B` or `A/file.txt`.
- If `A` splits into children, drop `A` from the final unit list and keep only the chosen child directories or files.

This prevents path invalidation, double moves, and execution-order bugs.

## Confidence Model

Track two confidence values:

- `classification_confidence`
  - How stable the PARA bucket choice is.
- `granularity_confidence`
  - How stable the move-as-dir vs split decision is.

Set final `confidence` to:

```text
min(classification_confidence, granularity_confidence)
```

Route low-confidence units into `Resources/Unsorted`.

Confidence is intentionally conservative when:

- the current workspace already appears well organized,
- the path has archive context that conflicts with project-like keywords,
- the item name is generic media such as `IMG_5705` and the collection context matters more than the filename,
- the top two PARA buckets remain too close after applying path, content, and structure signals.

## PARA Classification Heuristics

The classifier should prefer action semantics over raw keywords.

- Distinguish `Areas` from `Resources` by responsibility, not by origin.
- Do not treat "external input" as automatically `Resources`.
- Do not treat "user-created output" as automatically `Areas`.
- `Projects` requires active-project signals.
  Examples: current work context, planning artifacts, deliverable flow, code plus docs, or clearly active implementation material.
- `Projects` should be suppressed by strong archive, report, research, manual, ebook, invoice, or media signals.
- `Archives` should dominate when a path already lives inside archival containers such as backup, snapshot, restore, export, or explicit archive folders.
- `Resources` should dominate for manuals, ebooks, tutorials, reports, reference material, and curated content libraries.
- `Areas` should dominate for stable long-term responsibility domains such as family, health, finance, or ongoing topic workspaces.

## Areas Versus Resources

Use these rules when the top candidates are `Areas` and `Resources`.

- `Areas` means the user has an ongoing responsibility to maintain, review, update, or manage the domain.
- `Resources` means the user keeps the material because it is useful to consult, learn from, or reuse later.
- The key question is not "where did this come from?" but "what kind of relationship does the user have to it now?"
- If ignoring the item would weaken an active responsibility, stewardship duty, or recurring life/work operation, bias toward `Areas`.
- If the item mainly exists as a reference library, knowledge source, inspiration pool, or reusable artifact, bias toward `Resources`.

Examples that should bias toward `Areas`:

- health records, insurance documents, school notices, tax files, household finance records, and other materials tied to a continuing duty,
- operating documents for ongoing family, admin, career, or business responsibilities.

Examples that should bias toward `Resources`:

- books, manuals, research reports, tutorials, reference notes, templates, reading notes, summaries, and reusable guides,
- user-authored content whose main value is future lookup rather than active maintenance.

Example consequences:

- An archived work requirement document should stay archive-biased even if its filename contains words such as `需求` or `方案`.
- Stock research reports should bias toward `Resources` or `Areas`, not `Projects`.
- A large photo pool should remain a collection unless the user explicitly asks for aggressive regrouping.

## Conflict Handling

If a target path already exists or two plan items want the same target path:

- do not overwrite,
- do not guess,
- reroute the item to `Resources/Unsorted/Conflicts`.

## Duplicate Handling

- Mark duplicate status in metadata.
- Let duplicate signals influence classification and review.
- Do not auto-delete duplicates during PARA rebuild.
- Allow duplicates to move or aggregate with the rest of the plan.
