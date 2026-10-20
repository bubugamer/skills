# Metadata Schema

All generated state lives under `_catalog`.

## Top-Level Layout

```text
_catalog/
  metadata/
    manifest.json
    profile.json
    tree.json
    stats/
    duplicates/
    semantic/
    review/
    plans/
    _work/catalog.sqlite3
  tools/
  app/
  backups/
```

## Key Files

### `manifest.json`

Workspace-level summary:

- `generated_at`
- `root`
- `catalog_dir`
- `total_dirs`
- `total_files`
- `junk_files`
- `largest_dirs`

### `profile.json`

Workspace policy:

- `version`
- `organization_mode`
- `bucket_names`
- `ignore_dirs`
- `ignore_patterns`
- `junk_rules`
- `tag_rules`
- `ocr_mode`
- `safety_policy`

### `tree.json`

Flat tree representation:

- `format`
- `root`
- `generated_at`
- `nodes`

Each node includes:

- `id`
- `parent_id`
- `rel_path`
- `name`
- `node_type`
- `ext`
- `size`

### `stats/summary.json`

Workspace summary with:

- directory count
- file count
- size totals
- extension totals
- junk totals

### `duplicates/name_groups_*.json`

Duplicate-name groups with:

- `group_key`
- `match_mode`
- `count`
- `paths`

### `duplicates/exact_groups.json`

Exact duplicate groups with:

- `group_id`
- `size_each`
- `member_count`
- `reclaimable_bytes`
- `paths`

### `semantic/file_tags.json`

Per-file semantic output with:

- `rel_path`
- `excerpt`
- `keywords`
- `tags`
- `para_scores`
- `dominant_bucket`
- `classification_confidence`

### `semantic/similarity_groups.json`

Loose clustering output for similar files.

### `review/summary.json`

Review overview with:

- low-confidence counts
- duplicate counts
- hotspot directories
- pending plan counts

### `workspace_index.json`

Compact workspace index with:

- root summary
- root directories
- root files
- top-level bucket children
- review signals
- largest directories

### `workspace_index.md`

Human-readable workspace index for fast review.

### `workspace_tree.json`

Tree-shaped workspace index with:

- selected focus root
- depth and child limits
- nested directory nodes
- optional file nodes
- truncation markers

### `workspace_tree.md`

Human-readable tree rendering for the current workspace or a focused subtree.

### `plans/para_plan.json`

PARA execution plan. Each item includes:

- `source_path`
- `unit_type`
- `action`
- `target_bucket`
- `target_rel_path`
- `confidence`
- `classification_confidence`
- `granularity_confidence`
- `reasons`
- `flags`
- `duplicate_status`
- `sensitivity`

## Execution records

Each `_catalog/backups/<run>/` stores the input plan, execution report, completed path map, and reverse move plan. The report has `status` (`running`, `complete`, or `failed`), `operations`, `operation_count`, and an optional `error`. A failed run lists completed operations. Reverse moves appear in recovery order, with `plan_type: move`; newly created archives remain for separate review.

`para_scores` are raw content hints. `dominant_bucket` can instead preserve an existing mapped PARA location; `content_differs_from_existing_bucket` flags a differing content suggestion for review.
