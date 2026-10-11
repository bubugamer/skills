#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from workspace_lib import connect_db, ensure_workspace, human_size, init_db, now_iso, paths_for, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build directory and extension statistics.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    conn = connect_db(paths)
    init_db(conn)

    dir_rows = conn.execute(
        """
        SELECT rel_path, depth, direct_dir_count, direct_file_count, total_file_count, total_size
        FROM dirs
        ORDER BY total_size DESC, rel_path ASC
        """
    ).fetchall()
    ext_rows = conn.execute(
        """
        SELECT ext, COUNT(*) AS file_count, SUM(size) AS total_size
        FROM files
        GROUP BY ext
        ORDER BY file_count DESC, ext ASC
        """
    ).fetchall()
    summary = conn.execute(
        """
        SELECT
            COUNT(*) AS total_files,
            SUM(size) AS total_size,
            SUM(is_junk) AS junk_files
        FROM files
        """
    ).fetchone()
    conn.close()

    directory_stats = [
        {
            "rel_path": row["rel_path"] or ".",
            "depth": row["depth"],
            "direct_dir_count": row["direct_dir_count"],
            "direct_file_count": row["direct_file_count"],
            "total_file_count": row["total_file_count"],
            "total_size": row["total_size"],
            "total_size_human": human_size(int(row["total_size"] or 0)),
        }
        for row in dir_rows
    ]
    extension_stats = [
        {
            "ext": row["ext"],
            "file_count": row["file_count"],
            "total_size": row["total_size"] or 0,
            "total_size_human": human_size(int(row["total_size"] or 0)),
        }
        for row in ext_rows
    ]
    summary_payload = {
        "generated_at": now_iso(),
        "root": str(root),
        "total_dirs": len(directory_stats),
        "total_files": int(summary["total_files"] or 0),
        "total_size": int(summary["total_size"] or 0),
        "total_size_human": human_size(int(summary["total_size"] or 0)),
        "junk_files": int(summary["junk_files"] or 0),
        "extension_count": len(extension_stats),
    }

    write_json(paths.stats_dir / "directories.json", directory_stats)
    write_json(paths.stats_dir / "extensions.json", extension_stats)
    write_json(paths.stats_dir / "summary.json", summary_payload)

    print(json.dumps(summary_payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
