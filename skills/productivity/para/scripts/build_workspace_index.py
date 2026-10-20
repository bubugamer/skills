#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from workspace_lib import connect_db, ensure_workspace, human_size, init_db, now_iso, paths_for, read_json, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a human-readable and machine-readable workspace index.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def load_dir_index(conn: sqlite3.Connection, rel_path: str) -> dict[str, object] | None:
    row = conn.execute(
        """
        SELECT rel_path, name, depth, direct_dir_count, direct_file_count, total_file_count, total_size,
               dominant_bucket, dominant_topic, cohesion_score, split_need_score, granularity_decision,
               granularity_confidence, flags_json
        FROM dirs
        WHERE rel_path = ?
        """,
        (rel_path,),
    ).fetchone()
    if row is None:
        return None
    return {
        "rel_path": row["rel_path"],
        "name": row["name"],
        "depth": int(row["depth"] or 0),
        "direct_dir_count": int(row["direct_dir_count"] or 0),
        "direct_file_count": int(row["direct_file_count"] or 0),
        "total_file_count": int(row["total_file_count"] or 0),
        "total_size": int(row["total_size"] or 0),
        "total_size_human": human_size(int(row["total_size"] or 0)),
        "dominant_bucket": row["dominant_bucket"],
        "dominant_topic": row["dominant_topic"],
        "cohesion_score": float(row["cohesion_score"] or 0.0),
        "split_need_score": float(row["split_need_score"] or 0.0),
        "granularity_decision": row["granularity_decision"],
        "granularity_confidence": float(row["granularity_confidence"] or 0.0),
        "flags": json.loads(row["flags_json"] or "[]"),
    }


def load_root_dirs(conn: sqlite3.Connection) -> list[dict[str, object]]:
    rows = conn.execute(
        """
        SELECT rel_path
        FROM dirs
        WHERE depth = 1
        ORDER BY rel_path ASC
        """
    ).fetchall()
    return [load_dir_index(conn, str(row["rel_path"])) for row in rows if load_dir_index(conn, str(row["rel_path"])) is not None]


def load_root_files(conn: sqlite3.Connection) -> list[dict[str, object]]:
    rows = conn.execute(
        """
        SELECT rel_path, name, ext, size, dominant_bucket, classification_confidence, flags_json, is_junk
        FROM files
        WHERE dir_rel_path = ''
        ORDER BY rel_path ASC
        """
    ).fetchall()
    output = []
    for row in rows:
        if bool(row["is_junk"]):
            continue
        output.append(
            {
                "rel_path": row["rel_path"],
                "name": row["name"],
                "ext": row["ext"],
                "size": int(row["size"] or 0),
                "size_human": human_size(int(row["size"] or 0)),
                "dominant_bucket": row["dominant_bucket"],
                "classification_confidence": float(row["classification_confidence"] or 0.0),
                "flags": json.loads(row["flags_json"] or "[]"),
            }
        )
    return output


def load_children(conn: sqlite3.Connection, parent_rel_path: str, limit: int = 30) -> list[dict[str, object]]:
    rows = conn.execute(
        """
        SELECT rel_path, name, total_file_count, total_size, dominant_bucket, dominant_topic,
               granularity_decision, granularity_confidence, flags_json
        FROM dirs
        WHERE parent_rel_path = ?
        ORDER BY total_size DESC, total_file_count DESC, rel_path ASC
        LIMIT ?
        """,
        (parent_rel_path, limit),
    ).fetchall()
    return [
        {
            "rel_path": row["rel_path"],
            "name": row["name"],
            "total_file_count": int(row["total_file_count"] or 0),
            "total_size": int(row["total_size"] or 0),
            "total_size_human": human_size(int(row["total_size"] or 0)),
            "dominant_bucket": row["dominant_bucket"],
            "dominant_topic": row["dominant_topic"],
            "granularity_decision": row["granularity_decision"],
            "granularity_confidence": float(row["granularity_confidence"] or 0.0),
            "flags": json.loads(row["flags_json"] or "[]"),
        }
        for row in rows
    ]


def render_markdown(index_payload: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append("# Workspace Index")
    lines.append("")
    lines.append(f"- Generated at: `{index_payload['generated_at']}`")
    lines.append(f"- Root: `{index_payload['root']}`")
    summary = index_payload["summary"]
    lines.append(f"- Total dirs: `{summary['total_dirs']}`")
    lines.append(f"- Total files: `{summary['total_files']}`")
    lines.append(f"- Total size: `{summary['total_size_human']}`")
    lines.append(f"- Junk candidates: `{summary['junk_files']}`")
    lines.append(f"- Low-confidence files: `{summary['low_confidence_files']}`")
    lines.append("")

    lines.append("## Root View")
    lines.append("")
    for item in index_payload["root_directories"]:
        line = (
            f"- `{item['rel_path']}`: {item['total_file_count']} files, {item['total_size_human']}, "
            f"{item['direct_dir_count']} child dirs"
        )
        if item["dominant_bucket"]:
            line += f", dominant `{item['dominant_bucket']}`"
        lines.append(line)
    for item in index_payload["root_files"]:
        line = f"- root file `{item['rel_path']}`: {item['size_human']}"
        if item["dominant_bucket"]:
            line += f", bucket hint `{item['dominant_bucket']}`"
        lines.append(line)
    lines.append("")

    lines.append("## Bucket Children")
    lines.append("")
    for bucket in index_payload["bucket_children"]:
        lines.append(f"### `{bucket['bucket']}`")
        if not bucket["children"]:
            lines.append("")
            lines.append("- no child directories")
            lines.append("")
            continue
        lines.append("")
        for child in bucket["children"]:
            line = f"- `{child['name']}`: {child['total_file_count']} files, {child['total_size_human']}"
            if child["dominant_topic"]:
                line += f", topic `{child['dominant_topic']}`"
            lines.append(line)
        lines.append("")

    lines.append("## Review Signals")
    lines.append("")
    review = index_payload["review"]
    lines.append(f"- Pending PARA plan items: `{review['pending_para_plan_items']}`")
    lines.append(f"- Junk candidates: `{review['junk_candidates']}`")
    lines.append(f"- Exact duplicate groups: `{review['exact_duplicate_groups']}`")
    lines.append(f"- Hotspot count: `{review['hotspot_count']}`")
    lines.append("")

    lines.append("## Largest Directories")
    lines.append("")
    for item in index_payload["largest_dirs"]:
        lines.append(
            f"- `{item['rel_path']}`: {item['total_file_count']} files, {human_size(int(item['total_size']))}"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    conn = connect_db(paths)
    init_db(conn)

    manifest = read_json(paths.manifest_path, {}) or {}
    stats_summary = read_json(paths.stats_dir / "summary.json", {}) or {}
    review_summary = read_json(paths.review_dir / "summary.json", {}) or {}
    para_plan = read_json(paths.plans_dir / "para_plan.json", {}) or {}

    root_directories = load_root_dirs(conn)
    root_files = load_root_files(conn)
    bucket_children = []
    for item in root_directories:
        bucket_children.append(
            {
                "bucket": item["rel_path"],
                "children": load_children(conn, str(item["rel_path"])),
            }
        )
    conn.close()

    summary = {
        "total_dirs": int(stats_summary.get("total_dirs") or manifest.get("total_dirs") or 0),
        "total_files": int(stats_summary.get("total_files") or manifest.get("total_files") or 0),
        "total_size": int(stats_summary.get("total_size") or 0),
        "total_size_human": stats_summary.get("total_size_human") or human_size(int(stats_summary.get("total_size") or 0)),
        "junk_files": int(stats_summary.get("junk_files") or manifest.get("junk_files") or 0),
        "low_confidence_files": int(review_summary.get("low_confidence_files") or 0),
    }

    index_payload = {
        "generated_at": now_iso(),
        "root": str(root),
        "summary": summary,
        "root_directories": root_directories,
        "root_files": root_files,
        "bucket_children": bucket_children,
        "review": {
            "pending_para_plan_items": int(review_summary.get("pending_para_plan_items") or len(para_plan.get("items") or [])),
            "junk_candidates": int(review_summary.get("junk_candidates") or 0),
            "exact_duplicate_groups": int(review_summary.get("exact_duplicate_groups") or 0),
            "hotspot_count": int(review_summary.get("hotspot_count") or 0),
        },
        "largest_dirs": manifest.get("largest_dirs") or [],
    }

    write_json(paths.metadata_dir / "workspace_index.json", index_payload)
    (paths.metadata_dir / "workspace_index.md").write_text(render_markdown(index_payload), encoding="utf-8")

    print(
        json.dumps(
            {
                "generated_at": index_payload["generated_at"],
                "root": index_payload["root"],
                "root_dir_count": len(root_directories),
                "root_file_count": len(root_files),
                "output_json": str(paths.metadata_dir / "workspace_index.json"),
                "output_md": str(paths.metadata_dir / "workspace_index.md"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
