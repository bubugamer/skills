# PARA workflow

Resolve `<skill-dir>` to the folder containing SKILL.md and `<workspace>` to the selected root. Generated state goes into `<workspace>/_catalog`. Inspection changes internal state only.

## Inspect and plan

Run the following in order. Stop after inventory/statistics for an inspection request; stop before execution for a plan request.

```bash
python3 <skill-dir>/scripts/init_workspace.py --root <workspace>
python3 <skill-dir>/scripts/scan_inventory.py --root <workspace>
python3 <skill-dir>/scripts/build_stats.py --root <workspace>
python3 <skill-dir>/scripts/find_name_duplicates.py --root <workspace>
python3 <skill-dir>/scripts/find_exact_duplicates.py --root <workspace>
python3 <skill-dir>/scripts/enrich_semantics.py --root <workspace>
python3 <skill-dir>/scripts/build_review.py --root <workspace>
python3 <skill-dir>/scripts/plan_actions.py --root <workspace> --mode para
```

Set workspace-specific mappings in `_catalog/metadata/profile.json` before enrichment. Review `_catalog/metadata/plans/para_plan.json`: source and destination, folder/file granularity, confidence, and keep decisions. Scores use filenames, readable snippets, and metadata; they cannot establish the user's current commitments. Existing mapped containers are retained, with conflicting content hints flagged for review. Intentional reclassification within them requires an explicitly reviewed plan edit.

Optional navigation: `build_workspace_index.py` and `build_workspace_tree.py` create compact indexes. `serve_review_desk.py` opens a local review interface only on request. Read each script's `--help` for its options. These tools support the PARA rebuild.

## Execute the approved plan

```bash
python3 <skill-dir>/scripts/apply_actions.py --root <workspace> --plan-type para --confirm
```

An explicit reviewed JSON file can be passed with `--plan-file`. Items use `source_path`, `target_rel_path`, and `action` (`move`, `quarantine`, or `keep`). All paths are relative to the root. A keep item's source and destination are identical.

Execution checks every item before moving anything. It rejects missing sources, existing targets, source/target overlap, absolute or parent traversal paths, internal state, and symbolic links (including links within a moved folder). It rechecks paths while executing. Run with exclusive access to the workspace; this is not a concurrency-safe transaction or a cross-filesystem copy tool.

A later runtime failure stops the run. Already completed operations remain recorded rather than being silently undone. Inspect the failure report and reverse plan before recovery.

## Records and recovery

Each run has a separate `_catalog/backups/<run>/` folder containing:

- `input_plan.json`: the executed plan.
- `execution_report.json`: status, completed operations, and runtime errors.
- `path_map_final.json`: completed moves, keeps, and packages.
- `rollback_plan.json`: reverse moves in recovery order.

The folder stores recovery records, not duplicate copies of all user files. Reverse a reviewed move plan with:

```bash
python3 <skill-dir>/scripts/apply_actions.py --root <workspace> --plan-type move --plan-file <rollback-plan> --confirm
```

Recovery also rejects occupied paths. Empty destination folders remain. Package rollback restores a quarantined original but retains the new ZIP for separate review; it does not remove archives.

## Optional quarantine and packaging

These actions need their own scope and approval. Quarantine moves material to the configured ToDelete folder. Physical deletion is outside the bundled executor.

A package item specifies `source_path` and `archive_path`, optionally `move_original_to_quarantine: true` and `quarantine_path`. ZIP creation uses an exclusive new file and refuses any existing archive. Packaging leaves the source in place unless quarantine is explicitly requested. A directory ZIP includes empty folders. Review archive contents before treating packaging as a verified backup.

```bash
python3 <skill-dir>/scripts/apply_actions.py --root <workspace> --plan-type package --plan-file <package-plan> --confirm
```
