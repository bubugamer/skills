# Organization Profiles

Keep workspace-specific choices in `_catalog/metadata/profile.json`. The skill instructions define PARA meaning; the profile defines local names and exclusions.

## Default PARA Buckets

- `Projects`
  - Short-lived efforts with a specific outcome or deliverable.
- `Areas`
  - Long-lived responsibilities that need ongoing maintenance.
  - Classify by ongoing obligation and stewardship, not by whether the material was self-authored or externally received.
- `Resources`
  - Reference materials, manuals, ebooks, tutorials, research, and reusable assets.
  - User-authored notes, templates, and summaries can belong here when they are kept mainly for lookup or reuse rather than active maintenance.
- `Archives`
  - Historical backups, completed work, exports, recovered material, and low-activity content.
- `ToDelete`
  - Quarantine target for items the user wants out of the active workspace without physically deleting them.

## Reserved Support Paths

- `Resources/Unsorted`
  - Fallback bucket for low-confidence items.
- `Resources/Unsorted/Conflicts`
  - Fallback bucket for target-path collisions or ambiguous rewrites.
- `Archives/Snapshots`
  - Preferred subtree for backups, exports, recovery folders, and other snapshot-like material.

## Customization Points

Store custom settings in `_catalog/metadata/profile.json`.

### `organization_mode`

- `para`
- `custom`

### `bucket_names`

Map logical buckets to actual directory names.

Example:

```json
{
  "projects": "Projects",
  "areas": "Areas",
  "resources": "Resources",
  "archives": "Archives",
  "to_delete": "ToDelete",
  "unsorted": "Resources/Unsorted",
  "conflicts": "Resources/Unsorted/Conflicts",
  "snapshots": "Archives/Snapshots"
}
```

### `ignore_dirs`

Use this to add workspace-specific directories that should never be treated as user content.

### `ignore_patterns`

Use glob-style path patterns for extra exclusions when needed.

## Guidance

- Prefer keeping the logical PARA bucket names stable even if the directory names change.
- Do not encode one user's private numbering or category taxonomy as the global default.
- Keep `ToDelete`, `Unsorted`, `Conflicts`, and `Snapshots` available even when bucket names are customized.

## Existing containers and numbering

On first initialization, a uniquely named Projects, Areas, Resources, or Archives folder is reused. Matching ignores case and a numeric prefix followed by a separator; a prefix by itself conveys no PARA meaning. Ambiguous matches remain for user review. Changing an existing profile is an explicit workspace decision, not an automatic migration.

For other languages or personal names, set `bucket_names` explicitly. For example, Projects can map to `Work/Current` and Resources to `Library`. Primary buckets must be distinct, non-overlapping relative paths within the root. Absolute paths, parent traversal, and internal `_catalog` paths are rejected. Missing support paths derive from the configured Resources and Archives locations. Review older explicit support paths when changing those locations.

Existing mapped containers and their contents remain in place in generated plans. Content that suggests another bucket is review evidence, not permission to relocate it. Intentional reclassification uses a separately reviewed plan edit.
