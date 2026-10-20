---
name: para
description: Rebuild a user-selected workspace around PARA—Projects, Areas, Resources, and Archives. Use when the user asks to organize or migrate folders into PARA, review a PARA structure, or prepare and execute a PARA rebuild plan. Inventory, duplicate checks, classification, and recovery records support this workflow.
---

# PARA

Organize files according to their current purpose:

- **Projects:** active efforts with a defined outcome and an end point.
- **Areas:** ongoing responsibilities that require maintenance.
- **Resources:** material kept for reference, learning, or reuse.
- **Archives:** completed or inactive work and historical material.

## Understand the workspace

Confirm the selected root and the requested stage: inspection, planning, or execution. Establish active projects and ongoing responsibilities from the user's context. Ask about decisions that change classification; treat automated content scores as suggestions.

Read [organization-profiles.md](references/organization-profiles.md). Keep folder names, mappings, exclusions, and other workspace choices in `_catalog/metadata/profile.json`. Existing PARA containers retain their names and contents by default. Numbering alone carries no classification meaning.

## Build a reviewable plan

Follow [workflow.md](references/workflow.md) to inventory files, check duplicates, enrich content hints, and generate the plan. Generated records live in `_catalog`, which is excluded from user content.

Classify by the user's relationship to the material. A continuing duty belongs in Areas; a reusable reference belongs in Resources, regardless of authorship. Use current goals and deadlines to distinguish Projects from Archives.

Move cohesive folders as units. Split mixed folders into coherent children, then individual files when needed. Preserve useful collections and keep execution sources non-overlapping. Read [para-rebuild.md](references/para-rebuild.md) for classification and granularity details.

Show proposed moves, preserved folders, uncertain classifications, duplicates, and conflicts. Put unresolved material into review or the configured Unsorted location. Duplicate findings are review evidence; removal requires a separate user decision.

## Execute and verify

Execute the concrete plan within its authorized scope. If execution approval is still missing, obtain it after presenting the plan; existing approval remains valid for that scope.

The executor checks the whole plan before changing content. It accepts relative paths inside the selected root, excludes `_catalog`, and rejects symlinks, overlapping paths, missing sources, and occupied targets. ZIP creation also preserves existing files. Keep the workspace free of concurrent changes during execution; moves across filesystem boundaries require separate handling.

After execution, inspect the report, compare file counts and content hashes, and check the resulting locations. Report completed and failed operations clearly. Move recovery uses the recorded reverse plan; newly created ZIPs and empty destination folders remain for separate review.

## Supporting resources

- [workflow.md](references/workflow.md): commands, execution records, and recovery.
- [organization-profiles.md](references/organization-profiles.md): workspace mappings and exclusions.
- [para-rebuild.md](references/para-rebuild.md): classification, granularity, and conflicts.
- [junk-rules.md](references/junk-rules.md): junk and residual review candidates.
- [metadata-schema.md](references/metadata-schema.md): generated data formats.

Resolve script paths from the folder containing this SKILL.md. Pass the selected workspace explicitly with `--root`.
