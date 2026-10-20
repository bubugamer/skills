#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict

from workspace_lib import connect_db, ensure_workspace, init_db, now_iso, paths_for, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find duplicate names with or without extensions.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def build_groups(rows, key_name: str) -> list[dict]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        groups[str(row[key_name]).lower()].append(str(row["rel_path"]))
    payload = []
    for key, paths in groups.items():
        if len(paths) < 2:
            continue
        payload.append(
            {
                "group_key": key,
                "match_mode": "ignore_extension" if key_name == "stem" else "with_extension",
                "count": len(paths),
                "paths": sorted(paths),
            }
        )
    payload.sort(key=lambda item: (-item["count"], item["group_key"]))
    return payload


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    conn = connect_db(paths)
    init_db(conn)

    rows = conn.execute(
        "SELECT rel_path, name, stem FROM files WHERE is_junk = 0 ORDER BY rel_path"
    ).fetchall()
    with_ext = build_groups(rows, "name")
    ignore_ext = build_groups(rows, "stem")

    conn.execute("UPDATE files SET duplicate_name_with_ext_group = NULL, duplicate_name_ignore_ext_group = NULL")
    for index, group in enumerate(with_ext, start=1):
        group_id = f"with-ext-{index:05d}"
        conn.executemany(
            "UPDATE files SET duplicate_name_with_ext_group = ? WHERE rel_path = ?",
            [(group_id, rel_path) for rel_path in group["paths"]],
        )
        group["group_id"] = group_id
    for index, group in enumerate(ignore_ext, start=1):
        group_id = f"ignore-ext-{index:05d}"
        conn.executemany(
            "UPDATE files SET duplicate_name_ignore_ext_group = ? WHERE rel_path = ?",
            [(group_id, rel_path) for rel_path in group["paths"]],
        )
        group["group_id"] = group_id
    conn.commit()
    conn.close()

    write_json(paths.duplicates_dir / "name_groups_with_ext.json", with_ext)
    write_json(paths.duplicates_dir / "name_groups_ignore_ext.json", ignore_ext)
    summary = {
        "generated_at": now_iso(),
        "with_extension_group_count": len(with_ext),
        "ignore_extension_group_count": len(ignore_ext),
    }
    write_json(paths.duplicates_dir / "name_groups_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
