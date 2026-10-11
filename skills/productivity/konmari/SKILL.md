---
name: konmari
description: Reorganize the current directory or a user-selected workspace with a careful, review-first approach. Use when the user wants to inspect structure, summarize a workspace, find duplicates, prepare a cleanup review, or plan and execute a confirmed PARA rebuild. Preserve meaningful existing taxonomies when possible, and treat `_catalog` as internal skill state rather than user content.
---

# Konmari

## Overview

Treat the current directory as the user's workspace and build an internal `_catalog` workspace beside it.

Use this skill when the user wants to inspect structure, collect metadata, detect duplicates, prepare a review desk, or reorganize the workspace with a confirmed PARA rebuild.

When a workspace already has a meaningful directory taxonomy, understand that taxonomy first. Do not treat PARA as a reason to blindly flatten or relabel an already curated structure.

## Boundaries

This skill is about workspace structure, not content judgment or action management.

- Use `konmari` when the problem is where things live, whether folders are coherent, which files are duplicates, or how to prepare a safe reorganization plan.
- Use `tang-monk` when the problem is what the user should do next, what belongs in `Today`, `Weekly`, `Backlog`, or `Exploration`, or whether something should become real work.
- Use `dongnaojin-yeye` when the problem is whether a document is worth reading, how to summarize it, how to trace its source, or where to store reading and research notes.

If the user mostly needs understanding, curation, or task choice, do not reach for this skill just because files are involved.

## Internal Workspace Model

- Treat the current directory as the user workspace.
- Treat `_catalog` as an internal workspace owned by this skill.
- Do not treat `_catalog` as part of the user's content.
- Do not scan, classify, count, or reorganize `_catalog` as if it were user data.
- Store all generated metadata, plans, logs, review data, and helper state inside `_catalog`.

## Quick Start

Choose the smallest flow that matches the request.

- If the user only wants a quick understanding of the workspace, stop after inventory and stats.
- If the user wants cleanup guidance, add duplicate detection and review output.
- If the user wants a reorganization, generate a plan first and do not execute it without explicit confirmation.
- Do not jump to a PARA rebuild when the user only asked for a summary.

### Inspect or summarize a workspace

```bash
python3 scripts/init_workspace.py --root .
python3 scripts/scan_inventory.py --root .
python3 scripts/build_stats.py --root .
```

### Find duplicates or prepare a cleanup review

```bash
python3 scripts/init_workspace.py --root .
python3 scripts/scan_inventory.py --root .
python3 scripts/build_stats.py --root .
python3 scripts/find_name_duplicates.py --root .
python3 scripts/find_exact_duplicates.py --root .
python3 scripts/build_review.py --root .
```

### Build a PARA plan

```bash
python3 scripts/init_workspace.py --root .
python3 scripts/scan_inventory.py --root .
python3 scripts/build_stats.py --root .
python3 scripts/find_name_duplicates.py --root .
python3 scripts/find_exact_duplicates.py --root .
python3 scripts/enrich_semantics.py --root .
python3 scripts/build_review.py --root .
python3 scripts/plan_actions.py --root . --mode para
```

### Execute a confirmed PARA plan

```bash
python3 scripts/apply_actions.py --root . --plan-type para --confirm
```

## Core Commands

Use these scripts as the main building blocks.

- `scripts/init_workspace.py`
  - Create `_catalog`, initialize `profile.json`, and prepare the metadata layout.
- `scripts/scan_inventory.py`
  - Walk the workspace, build the SQLite index, and write `manifest.json` and `tree.json`.
- `scripts/build_stats.py`
  - Produce directory, extension, and workspace-level statistics.
- `scripts/find_name_duplicates.py`
  - Find duplicate names with or without extensions.
- `scripts/find_exact_duplicates.py`
  - Find exact duplicates by candidate reduction and full hashing.
- `scripts/enrich_semantics.py`
  - Extract readable snippets, keywords, tags, PARA scores, and similarity hints.
- `scripts/build_review.py`
  - Produce review queues, hotspots, and duplicate summaries.
- `scripts/build_workspace_index.py`
  - Produce a compact workspace index in both JSON and Markdown for review and navigation.
- `scripts/build_workspace_tree.py`
  - Produce a tree-shaped workspace index in both JSON and Markdown, with configurable depth and optional file nodes.
- `scripts/plan_actions.py`
  - Generate PARA, quarantine, move, and package plans.
- `scripts/apply_actions.py`
  - Execute a confirmed plan and write logs, mappings, and rollback data.
- `scripts/serve_review_desk.py`
  - Start the lightweight review desk only when the user explicitly asks for it.

## PARA Rebuild Workflow

Treat `PARA rebuild` as a full workflow, not as a single blind move operation.

1. Initialize `_catalog`.
2. Scan the workspace.
3. Build statistics and summaries.
4. Detect whether the current workspace already has a meaningful top-level taxonomy.
5. Detect name duplicates, exact duplicates, junk candidates, and residual candidates.
6. Enrich files with readable snippets, metadata-derived hints, and tags.
7. Compute directory cohesion, split need, structure value, and container-preservation signals.
8. Decide the reorganization granularity.
9. Score each directory or file unit against `Projects`, `Areas`, `Resources`, and `Archives`.
10. Generate target paths and a PARA plan.
11. Validate that source paths do not overlap and that conflicts route into `Resources/Unsorted/Conflicts`.
12. Show the user the plan summary.
13. Execute only after explicit confirmation.

When scoring `Areas` versus `Resources`, prefer responsibility over source:

- Bias toward `Areas` when the user has an ongoing duty to maintain the domain.
- Bias toward `Resources` when the material is mainly kept for reference, learning, or reuse.
- Do not use "user-created" versus "externally received" as the primary rule.
- Read [references/para-rebuild.md](references/para-rebuild.md) for the full `Areas` versus `Resources` guidance and examples.

When deciding granularity, use these rules:

- Move a directory as one unit when it is cohesive.
- Split to child directories when the parent mixes multiple stable groups.
- Split to files only when child directories are still mixed.
- Keep the final set of execution units non-overlapping.
- Preserve coded top-level categories, archive containers, backup trees, duplicate-media pools, and other meaningful collections unless the user explicitly asks for aggressive deeper splitting.

When deciding confidence, use these rules:

- Track `classification_confidence` for the PARA bucket choice.
- Track `granularity_confidence` for the move-as-dir vs split decision.
- Set final `confidence` to the smaller of the two values.
- Route low-confidence units into `Resources/Unsorted`.
- Treat `Projects` as a high bar: project-like keywords alone are not enough when archive, research, report, manual, or media context is stronger.

Read [references/para-rebuild.md](references/para-rebuild.md) before modifying the PARA logic.

## Safety Rules

- Never delete files or directories without explicit user approval.
- Treat user requests to "delete" as quarantine requests unless the user clearly asks for physical deletion.
- Default quarantine targets to `ToDelete`.
- Always generate a plan before any move, quarantine, package, or rebuild action.
- Never execute a plan until the user explicitly confirms it.
- Write execution logs, path mappings, and rollback information after every confirmed run.
- Keep `_catalog` internal and transparent to the user.

## Communication

When reporting back to the user:

- Explain what was inspected, what was planned, and what was actually changed in plain language.
- Make the current safety state explicit: whether this was only analysis, a proposed plan, or a confirmed execution.
- Call out preserved structures on purpose when the workspace already had a meaningful taxonomy.
- If confidence is low, say so directly and route the uncertain material into review or `Resources/Unsorted` rather than pretending the classification is settled.

## Resources

- Read [references/organization-profiles.md](references/organization-profiles.md) when the user wants custom bucket mappings or wants to override default PARA names.
- Read [references/junk-rules.md](references/junk-rules.md) when deciding what should be marked as junk or residual.
- Read [references/para-rebuild.md](references/para-rebuild.md) for the core rebuild algorithm, granularity logic, and confidence model.
- Read [references/metadata-schema.md](references/metadata-schema.md) before adding new metadata outputs or changing JSON payloads.

## Locating bundled scripts

Resolve `<skill-dir>` to the absolute folder containing this SKILL.md before running a command. Paths beginning `scripts/` are relative to that folder, not to the user workspace. Keep the user workspace as the working directory when a script uses `--root .`.
