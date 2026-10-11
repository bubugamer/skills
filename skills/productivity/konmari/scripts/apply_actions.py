#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path

from workspace_lib import ensure_workspace, now_iso, paths_for, read_json, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute a confirmed plan.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument(
        "--plan-type",
        default="para",
        choices=["para", "move", "quarantine", "package"],
        help="Plan type to execute",
    )
    parser.add_argument("--plan-file", help="Optional explicit plan file path")
    parser.add_argument("--confirm", action="store_true", help="Required flag for execution")
    return parser.parse_args()


def default_plan_path(paths, plan_type: str) -> Path:
    mapping = {
        "para": paths.plans_dir / "para_plan.json",
        "move": paths.plans_dir / "move_plan.json",
        "quarantine": paths.plans_dir / "quarantine_plan.json",
        "package": paths.plans_dir / "package_plan.json",
    }
    return mapping[plan_type]


def execute_move_like(root: Path, items: list[dict], backup_dir: Path) -> tuple[list[dict], list[dict]]:
    operations: list[dict] = []
    rollback: list[dict] = []
    ordered = sorted(items, key=lambda item: item["source_path"].count("/"), reverse=True)
    for item in ordered:
        source_path = root / item["source_path"]
        target_path = root / item["target_rel_path"]
        if item.get("action") == "keep":
            operations.append({"source_path": item["source_path"], "target_rel_path": item["target_rel_path"], "status": "kept"})
            continue
        if not source_path.exists():
            operations.append({"source_path": item["source_path"], "target_rel_path": item["target_rel_path"], "status": "missing"})
            continue
        if target_path.exists() and source_path.resolve() != target_path.resolve():
            operations.append({"source_path": item["source_path"], "target_rel_path": item["target_rel_path"], "status": "target_exists"})
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(target_path))
        operations.append({"source_path": item["source_path"], "target_rel_path": item["target_rel_path"], "status": "moved"})
        rollback.append({"source_path": item["target_rel_path"], "target_rel_path": item["source_path"], "action": "move"})
    return operations, rollback


def execute_package(root: Path, items: list[dict], backup_dir: Path) -> tuple[list[dict], list[dict]]:
    operations: list[dict] = []
    rollback: list[dict] = []
    for item in items:
        source_path = root / item["source_path"]
        archive_path = root / item["archive_path"]
        if not source_path.exists():
            operations.append({"source_path": item["source_path"], "archive_path": item["archive_path"], "status": "missing"})
            continue
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as handle:
            if source_path.is_dir():
                for nested in source_path.rglob("*"):
                    if nested.is_file():
                        handle.write(nested, nested.relative_to(source_path.parent))
            else:
                handle.write(source_path, source_path.name)
        operations.append({"source_path": item["source_path"], "archive_path": item["archive_path"], "status": "packaged"})
        if item.get("move_original_to_quarantine"):
            quarantine_path = root / item["quarantine_path"]
            quarantine_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(quarantine_path))
            rollback.append({"source_path": item["quarantine_path"], "target_rel_path": item["source_path"], "action": "move"})
    return operations, rollback


def main() -> int:
    args = parse_args()
    if not args.confirm:
        raise SystemExit("Refusing to execute without --confirm")

    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    plan_path = Path(args.plan_file).expanduser().resolve() if args.plan_file else default_plan_path(paths, args.plan_type)
    if not plan_path.exists():
        raise SystemExit(f"Plan file not found: {plan_path}")

    plan = read_json(plan_path, {})
    items = plan.get("items") or []
    timestamp = now_iso().replace(":", "").replace("+", "_")
    backup_dir = paths.backups_dir / f"{args.plan_type}_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    write_json(backup_dir / "input_plan.json", plan)

    if args.plan_type == "package":
        operations, rollback = execute_package(root, items, backup_dir)
    else:
        operations, rollback = execute_move_like(root, items, backup_dir)

    execution_report = {
        "generated_at": now_iso(),
        "plan_type": args.plan_type,
        "plan_path": str(plan_path),
        "operation_count": len(operations),
        "operations": operations,
    }
    rollback_plan = {
        "generated_at": now_iso(),
        "plan_type": args.plan_type,
        "item_count": len(rollback),
        "items": rollback,
    }
    path_map = [
        {"source_path": op.get("source_path"), "target_rel_path": op.get("target_rel_path"), "status": op["status"]}
        for op in operations
        if op["status"] in {"moved", "kept"}
    ]

    write_json(backup_dir / "execution_report.json", execution_report)
    write_json(backup_dir / "rollback_plan.json", rollback_plan)
    write_json(backup_dir / "path_map_final.json", path_map)

    print(
        json.dumps(
            {
                "generated_at": now_iso(),
                "plan_type": args.plan_type,
                "operation_count": len(operations),
                "backup_dir": str(backup_dir),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
