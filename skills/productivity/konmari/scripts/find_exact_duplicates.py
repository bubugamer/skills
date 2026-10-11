#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from workspace_lib import (
    connect_db,
    ensure_workspace,
    full_sha256,
    head_fingerprint,
    human_size,
    init_db,
    now_iso,
    paths_for,
    resolve_root,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find exact duplicate files.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    conn = connect_db(paths)
    init_db(conn)

    rows = conn.execute(
        "SELECT rel_path, size, head_hash, full_hash FROM files WHERE is_junk = 0 AND size > 0 ORDER BY size, rel_path"
    ).fetchall()

    by_size: dict[int, list[sqlite3.Row]] = defaultdict(list)  # type: ignore[name-defined]
    for row in rows:
        by_size[int(row["size"])].append(row)

    candidate_groups = [group for group in by_size.values() if len(group) > 1]
    conn.execute("UPDATE files SET exact_duplicate_group = NULL")

    exact_groups: list[dict] = []
    group_index = 1
    for candidates in candidate_groups:
        by_head: dict[str, list[dict]] = defaultdict(list)
        for row in candidates:
            rel_path = str(row["rel_path"])
            file_path = root / rel_path
            digest = row["head_hash"] or head_fingerprint(file_path)
            conn.execute("UPDATE files SET head_hash = ? WHERE rel_path = ?", (digest, rel_path))
            by_head[str(digest)].append({"rel_path": rel_path, "size": int(row["size"]), "full_hash": row["full_hash"]})

        for members in by_head.values():
            if len(members) < 2:
                continue
            by_full: dict[str, list[dict]] = defaultdict(list)
            for member in members:
                file_path = root / member["rel_path"]
                digest = member["full_hash"] or full_sha256(file_path)
                conn.execute("UPDATE files SET full_hash = ? WHERE rel_path = ?", (digest, member["rel_path"]))
                by_full[str(digest)].append(member)

            for digest, duplicates in by_full.items():
                if len(duplicates) < 2:
                    continue
                group_id = f"exact-{group_index:05d}"
                group_index += 1
                size_each = duplicates[0]["size"]
                reclaimable = size_each * (len(duplicates) - 1)
                sorted_paths = sorted(member["rel_path"] for member in duplicates)
                conn.executemany(
                    "UPDATE files SET exact_duplicate_group = ? WHERE rel_path = ?",
                    [(group_id, rel_path) for rel_path in sorted_paths],
                )
                exact_groups.append(
                    {
                        "group_id": group_id,
                        "sha256": digest,
                        "size_each": size_each,
                        "size_each_human": human_size(size_each),
                        "member_count": len(sorted_paths),
                        "reclaimable_bytes": reclaimable,
                        "reclaimable_human": human_size(reclaimable),
                        "paths": sorted_paths,
                    }
                )

    conn.commit()
    conn.close()

    exact_groups.sort(key=lambda item: (-item["reclaimable_bytes"], -item["member_count"], item["group_id"]))
    payload = {
        "generated_at": now_iso(),
        "group_count": len(exact_groups),
        "reclaimable_bytes": sum(item["reclaimable_bytes"] for item in exact_groups),
        "items": exact_groups,
    }
    write_json(paths.duplicates_dir / "exact_groups.json", payload)
    print(json.dumps({"generated_at": payload["generated_at"], "group_count": payload["group_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
