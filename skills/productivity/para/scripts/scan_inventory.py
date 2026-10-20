#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from workspace_lib import (
    connect_db,
    detect_junk,
    ensure_workspace,
    first_component,
    init_db,
    join_rel,
    load_profile,
    now_iso,
    normalize_ext,
    parent_rel,
    paths_for,
    rel_from_path,
    reset_inventory,
    resolve_root,
    should_skip_dir,
    should_skip_file,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan the workspace and build the inventory index.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    profile = load_profile(paths)
    conn = connect_db(paths)
    init_db(conn)
    reset_inventory(conn)

    dir_nodes: dict[str, dict] = {
        "": {
            "rel_path": "",
            "parent_rel_path": None,
            "name": root.name,
            "depth": 0,
            "top_dir": "[root]",
            "direct_dir_count": 0,
            "direct_file_count": 0,
            "total_file_count": 0,
            "total_size": 0,
        }
    }
    file_rows: list[dict] = []

    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        rel_dir = "" if current_path == root else rel_from_path(current_path, root)
        if rel_dir and should_skip_dir(rel_dir, current_path.name, profile):
            dirnames[:] = []
            continue

        filtered_dirnames: list[str] = []
        for dirname in sorted(dirnames):
            child_rel = join_rel(rel_dir, dirname)
            if should_skip_dir(child_rel, dirname, profile):
                continue
            filtered_dirnames.append(dirname)
            dir_nodes.setdefault(
                child_rel,
                {
                    "rel_path": child_rel,
                    "parent_rel_path": rel_dir if rel_dir != "" else "",
                    "name": dirname,
                    "depth": child_rel.count("/") + 1,
                    "top_dir": first_component(child_rel),
                    "direct_dir_count": 0,
                    "direct_file_count": 0,
                    "total_file_count": 0,
                    "total_size": 0,
                },
            )
        dirnames[:] = filtered_dirnames

        current_node = dir_nodes.setdefault(
            rel_dir,
            {
                "rel_path": rel_dir,
                "parent_rel_path": parent_rel(rel_dir),
                "name": root.name if rel_dir == "" else Path(rel_dir).name,
                "depth": 0 if rel_dir == "" else rel_dir.count("/") + 1,
                "top_dir": "[root]" if rel_dir == "" else first_component(rel_dir),
                "direct_dir_count": 0,
                "direct_file_count": 0,
                "total_file_count": 0,
                "total_size": 0,
            },
        )
        current_node["direct_dir_count"] = len(filtered_dirnames)

        direct_file_count = 0
        for filename in sorted(filenames):
            rel_file = join_rel(rel_dir, filename) if rel_dir else filename
            if should_skip_file(rel_file, filename, profile):
                continue
            file_path = current_path / filename
            try:
                stat = file_path.stat()
            except FileNotFoundError:
                continue
            ext = normalize_ext(filename)
            junk_reasons = detect_junk(rel_file, filename, ext, is_dir=False)
            file_rows.append(
                {
                    "rel_path": rel_file,
                    "dir_rel_path": rel_dir,
                    "name": filename,
                    "stem": Path(filename).stem,
                    "ext": ext,
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "depth": rel_file.count("/") + 1,
                    "top_dir": first_component(rel_file),
                    "is_junk": 1 if junk_reasons else 0,
                    "junk_reasons_json": json.dumps(junk_reasons, ensure_ascii=False),
                }
            )
            direct_file_count += 1
        current_node["direct_file_count"] = direct_file_count

    total_files = len(file_rows)
    junk_files = 0
    file_counts = Counter()
    size_counts = Counter()
    for row in file_rows:
        if row["is_junk"]:
            junk_files += 1
        for ancestor in ([""] + [p for p in row["dir_rel_path"].split("/") if False]):
            pass
        current = row["dir_rel_path"]
        ancestors = [""]
        if current:
            parts = current.split("/")
            ancestors.extend("/".join(parts[:index]) for index in range(1, len(parts) + 1))
        for ancestor in ancestors:
            file_counts[ancestor] += 1
            size_counts[ancestor] += row["size"]

    for rel_dir, node in dir_nodes.items():
        node["total_file_count"] = int(file_counts.get(rel_dir, 0))
        node["total_size"] = int(size_counts.get(rel_dir, 0))

    conn.executemany(
        """
        INSERT INTO dirs(
            rel_path, parent_rel_path, name, depth, top_dir, direct_dir_count,
            direct_file_count, total_file_count, total_size
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                node["rel_path"],
                node["parent_rel_path"],
                node["name"],
                node["depth"],
                node["top_dir"],
                node["direct_dir_count"],
                node["direct_file_count"],
                node["total_file_count"],
                node["total_size"],
            )
            for node in dir_nodes.values()
        ],
    )
    conn.executemany(
        """
        INSERT INTO files(
            rel_path, dir_rel_path, name, stem, ext, size, mtime, depth, top_dir,
            is_junk, junk_reasons_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                row["rel_path"],
                row["dir_rel_path"],
                row["name"],
                row["stem"],
                row["ext"],
                row["size"],
                row["mtime"],
                row["depth"],
                row["top_dir"],
                row["is_junk"],
                row["junk_reasons_json"],
            )
            for row in file_rows
        ],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
        [
            ("generated_at", now_iso()),
            ("root", str(root)),
            ("catalog_dir", str(paths.catalog_dir)),
        ],
    )
    conn.commit()
    conn.close()

    id_map: dict[str, int] = {}
    nodes: list[dict] = []
    next_id = 1
    for rel_dir, node in sorted(dir_nodes.items(), key=lambda item: (item[1]["depth"], item[0])):
        id_map[rel_dir] = next_id
        nodes.append(
            {
                "id": next_id,
                "parent_id": None if rel_dir == "" else id_map.get(parent_rel(rel_dir) or "", 1),
                "rel_path": rel_dir,
                "name": node["name"],
                "node_type": "dir",
                "ext": None,
                "size": node["total_size"],
                "total_file_count": node["total_file_count"],
            }
        )
        next_id += 1
    for row in file_rows:
        nodes.append(
            {
                "id": next_id,
                "parent_id": id_map.get(row["dir_rel_path"], id_map[""]),
                "rel_path": row["rel_path"],
                "name": row["name"],
                "node_type": "file",
                "ext": row["ext"],
                "size": row["size"],
            }
        )
        next_id += 1

    largest_dirs = sorted(
        (
            {
                "rel_path": rel_dir or ".",
                "total_file_count": node["total_file_count"],
                "total_size": node["total_size"],
            }
            for rel_dir, node in dir_nodes.items()
            if rel_dir
        ),
        key=lambda item: (-item["total_size"], item["rel_path"]),
    )[:10]

    write_json(
        paths.manifest_path,
        {
            "generated_at": now_iso(),
            "root": str(root),
            "catalog_dir": str(paths.catalog_dir),
            "total_dirs": len(dir_nodes),
            "total_files": total_files,
            "junk_files": junk_files,
            "largest_dirs": largest_dirs,
        },
    )
    write_json(
        paths.tree_path,
        {
            "generated_at": now_iso(),
            "root": str(root),
            "format": "flat_nodes_v1",
            "nodes": nodes,
        },
    )

    print(
        json.dumps(
            {
                "ok": True,
                "generated_at": now_iso(),
                "root": str(root),
                "total_dirs": len(dir_nodes),
                "total_files": total_files,
                "junk_files": junk_files,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
