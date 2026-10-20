#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from workspace_lib import connect_db, ensure_workspace, init_db, now_iso, paths_for, read_json, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build review queues and hotspot summaries.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    conn = connect_db(paths)
    init_db(conn)

    low_conf_rows = conn.execute(
        """
        SELECT rel_path, dominant_bucket, classification_confidence, tags_json, flags_json
        FROM files
        WHERE COALESCE(classification_confidence, 0) < 0.65
        ORDER BY classification_confidence ASC, rel_path ASC
        LIMIT 200
        """
    ).fetchall()
    low_conf_count = conn.execute(
        "SELECT COUNT(*) AS count FROM files WHERE COALESCE(classification_confidence, 0) < 0.65"
    ).fetchone()
    hotspot_rows = conn.execute(
        """
        SELECT rel_path, total_file_count, total_size
        FROM dirs
        WHERE rel_path != ''
        ORDER BY total_size DESC, total_file_count DESC, rel_path ASC
        LIMIT 50
        """
    ).fetchall()
    junk_candidates = conn.execute("SELECT COUNT(*) AS count FROM files WHERE is_junk = 1").fetchone()
    exact_groups = read_json(paths.duplicates_dir / "exact_groups.json", {"items": []}) or {"items": []}
    para_plan = read_json(paths.plans_dir / "para_plan.json", {})
    conn.close()

    queue = [
        {
            "rel_path": row["rel_path"],
            "dominant_bucket": row["dominant_bucket"],
            "classification_confidence": row["classification_confidence"] or 0.0,
            "tags": json.loads(row["tags_json"] or "{}"),
            "flags": json.loads(row["flags_json"] or "[]"),
        }
        for row in low_conf_rows
    ]
    hotspots = [
        {
            "rel_path": row["rel_path"],
            "total_file_count": row["total_file_count"],
            "total_size": row["total_size"],
        }
        for row in hotspot_rows
    ]
    summary = {
        "generated_at": now_iso(),
        "root": str(root),
        "low_confidence_files": int(low_conf_count["count"] or 0),
        "junk_candidates": int(junk_candidates["count"] or 0),
        "exact_duplicate_groups": len(exact_groups.get("items", [])),
        "hotspot_count": len(hotspots),
        "pending_para_plan_items": len((para_plan or {}).get("items", [])),
    }

    write_json(paths.review_dir / "summary.json", summary)
    write_json(paths.review_dir / "queue.json", queue)
    write_json(paths.review_dir / "hotspots.json", hotspots)
    write_json(paths.review_dir / "duplicate_groups.json", exact_groups.get("items", []))
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
