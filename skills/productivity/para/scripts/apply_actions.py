#!/usr/bin/env python3
"""Validate the complete plan, then execute within one workspace and record recovery steps."""
from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from pathlib import Path

from workspace_lib import ensure_workspace, now_iso, paths_for, read_json, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute a confirmed, validated PARA plan.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument("--plan-type", default="para", choices=["para", "move", "quarantine", "package"])
    parser.add_argument("--plan-file", help="Optional explicit plan file path")
    parser.add_argument("--confirm", action="store_true", help="Required flag for execution")
    return parser.parse_args()


def default_plan_path(paths, plan_type: str) -> Path:
    return paths.plans_dir / f"{plan_type}_plan.json"


def overlaps(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def content_path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute() or any(
        part in {"", ".", ".."} for part in value.split("/")
    ):
        raise ValueError(f"Expected a relative content path: {value!r}")
    if value.split("/")[0] == "_catalog":
        raise ValueError("_catalog is internal state, not an execution source or target")
    path = root / value
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"Path leaves the selected workspace: {value!r}")
    if any(part.is_symlink() for part in [path, *path.parents] if part != root and part.is_relative_to(root)):
        raise ValueError(f"Symbolic links require separate review: {value!r}")
    if any(parent.exists() and not parent.is_dir() for parent in path.parents if parent.is_relative_to(root)):
        raise ValueError(f"Parent is not a directory: {value!r}")
    return path


def validate_plan(root: Path, plan: object, plan_type: str) -> list[dict]:
    if not isinstance(plan, dict) or not isinstance(plan.get("items"), list):
        raise ValueError("Plan must contain an items array")
    catalog = root / "_catalog"
    if catalog.is_symlink() or (catalog.exists() and any(p.is_symlink() for p in catalog.rglob("*"))):
        raise ValueError("Internal _catalog state must not contain symbolic links")
    sources: list[Path] = []
    targets: list[Path] = []
    items = plan["items"]
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each plan item must be an object")
        source = content_path(root, item.get("source_path"))
        if not source.exists():
            raise ValueError(f"Missing source: {item['source_path']}")
        if not source.is_file() and not source.is_dir():
            raise ValueError(f"Unsupported source type: {item['source_path']}")
        if source.is_dir() and any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError(f"Source contains symbolic links: {item['source_path']}")
        if plan_type == "package":
            sources.append(source)
            targets.append(content_path(root, item.get("archive_path")))
            if item.get("move_original_to_quarantine"):
                targets.append(content_path(root, item.get("quarantine_path")))
        else:
            action = item.get("action", "move")
            if action not in {"move", "quarantine", "keep"}:
                raise ValueError(f"Unsupported action: {action!r}")
            target = content_path(root, item.get("target_rel_path"))
            if action == "keep" and source != target:
                raise ValueError("A keep item must retain its source path")
            if source != target:
                sources.append(source)
                targets.append(target)
    for i, source in enumerate(sources):
        if any(overlaps(source, other) for other in sources[i + 1:]):
            raise ValueError("Plan contains overlapping source paths")
    for i, target in enumerate(targets):
        if target.exists() or target.is_symlink():
            raise ValueError(f"Target already exists; nothing was changed: {target.relative_to(root)}")
        if any(overlaps(target, other) for other in targets[i + 1:]):
            raise ValueError("Plan contains overlapping target paths")
        if any(overlaps(target, source) for source in sources):
            raise ValueError("A target overlaps a source path")
    return items


def record_progress(backup_dir: Path, plan_type: str, operations: list[dict], rollback: list[dict],
                    status: str, error: str | None = None) -> None:
    write_json(backup_dir / "execution_report.json", {
        "generated_at": now_iso(), "plan_type": plan_type, "status": status,
        "operation_count": len(operations), "operations": operations, "error": error,
    })
    write_json(backup_dir / "rollback_plan.json", {
        "generated_at": now_iso(), "plan_type": "move", "item_count": len(rollback),
        "items": list(reversed(rollback)),
        "note": "Moves can be reversed with apply_actions --plan-type move. Created ZIPs are retained; inspect them separately.",
    })
    write_json(backup_dir / "path_map_final.json", operations)


def move_without_overwrite(source: Path, target: Path) -> None:
    # Execution assumes exclusive access to the workspace; recheck before each operation.
    if target.exists() or target.is_symlink():
        raise ValueError(f"Target appeared after validation: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    # rename fails rather than leaving partially copied files across filesystem boundaries.
    source.rename(target)


def execute(root: Path, items: list[dict], plan_type: str, backup_dir: Path,
            operations: list[dict], rollback: list[dict]) -> None:
    for item in items:
        source = content_path(root, item["source_path"])
        if plan_type == "package":
            archive = content_path(root, item["archive_path"])
            archive.parent.mkdir(parents=True, exist_ok=True)
            created = False
            try:
                with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as handle:
                    created = True
                    if source.is_dir():
                        handle.write(source, source.name)
                        for nested in sorted(source.rglob("*")):
                            if nested.is_symlink():
                                raise ValueError("Source changed to contain a symbolic link")
                            handle.write(nested, nested.relative_to(source.parent))
                    else:
                        handle.write(source, source.name)
            except Exception:
                if created:
                    archive.unlink()
                raise
            operations.append({"source_path": item["source_path"], "archive_path": item["archive_path"], "status": "packaged"})
            record_progress(backup_dir, plan_type, operations, rollback, "running")
            if item.get("move_original_to_quarantine"):
                quarantine = content_path(root, item["quarantine_path"])
                move_without_overwrite(source, quarantine)
                operations.append({"source_path": item["source_path"], "target_rel_path": item["quarantine_path"], "status": "moved"})
                rollback.append({"source_path": item["quarantine_path"], "target_rel_path": item["source_path"], "action": "move"})
        else:
            target = content_path(root, item["target_rel_path"])
            if source == target:
                operations.append({"source_path": item["source_path"], "target_rel_path": item["target_rel_path"], "status": "kept"})
            else:
                move_without_overwrite(source, target)
                operations.append({"source_path": item["source_path"], "target_rel_path": item["target_rel_path"], "status": "moved"})
                rollback.append({"source_path": item["target_rel_path"], "target_rel_path": item["source_path"], "action": "move"})
        record_progress(backup_dir, plan_type, operations, rollback, "running")


def main() -> int:
    args = parse_args()
    if not args.confirm:
        raise SystemExit("Refusing to execute without --confirm")
    root = resolve_root(args.root)
    paths = paths_for(root)
    plan_path = Path(args.plan_file).expanduser().resolve() if args.plan_file else default_plan_path(paths, args.plan_type)
    if not plan_path.is_file():
        raise SystemExit(f"Plan file not found: {plan_path}")
    try:
        plan = read_json(plan_path)
        items = validate_plan(root, plan, args.plan_type)
    except (ValueError, OSError) as exc:
        raise SystemExit(f"Plan rejected before execution: {exc}") from exc

    ensure_workspace(paths)
    backup_dir = Path(tempfile.mkdtemp(prefix=f"{args.plan_type}_", dir=paths.backups_dir))
    write_json(backup_dir / "input_plan.json", plan)
    operations: list[dict] = []
    rollback: list[dict] = []
    record_progress(backup_dir, args.plan_type, operations, rollback, "running")
    try:
        execute(root, items, args.plan_type, backup_dir, operations, rollback)
    except Exception as exc:
        record_progress(backup_dir, args.plan_type, operations, rollback, "failed", str(exc))
        print(json.dumps({"status": "failed", "error": str(exc), "backup_dir": str(backup_dir)}, ensure_ascii=False))
        return 1
    record_progress(backup_dir, args.plan_type, operations, rollback, "complete")
    print(json.dumps({"status": "complete", "plan_type": args.plan_type,
                      "operation_count": len(operations), "backup_dir": str(backup_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
