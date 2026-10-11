#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict

from workspace_lib import (
    connect_db,
    ensure_workspace,
    extract_keywords,
    infer_form,
    infer_sensitivity,
    infer_source,
    init_db,
    now_iso,
    paths_for,
    read_text_excerpt,
    resolve_root,
    score_para_bucket,
    topic_label_from_keywords,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich files with tags, snippets, and PARA hints.")
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
        """
        SELECT rel_path, ext, mtime, is_junk, junk_reasons_json
        FROM files
        ORDER BY rel_path
        """
    ).fetchall()

    file_tags: list[dict] = []
    similarity_groups: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        rel_path = str(row["rel_path"])
        ext = str(row["ext"])
        excerpt, content_status = read_text_excerpt(root / rel_path, ext)
        keywords = extract_keywords(rel_path, excerpt)
        para_scores, dominant_bucket, confidence, reasons, flags = score_para_bucket(
            rel_path=rel_path,
            ext=ext,
            excerpt=excerpt,
            keywords=keywords,
            mtime=float(row["mtime"]),
            is_dir=False,
            is_junk=bool(row["is_junk"]),
        )
        tags = {
            "topic": [topic_label_from_keywords(rel_path, keywords)],
            "keywords": keywords[:8],
            "form": [infer_form(ext)],
            "source": [infer_source(rel_path)],
            "sensitivity": [infer_sensitivity(rel_path, excerpt)],
        }
        if row["is_junk"]:
            flags.extend(json.loads(row["junk_reasons_json"] or "[]"))
        similarity_key = f"{dominant_bucket}::{tags['topic'][0]}"
        similarity_groups[similarity_key].append(rel_path)

        conn.execute(
            """
            UPDATE files
            SET excerpt = ?, content_status = ?, keyword_text = ?, tags_json = ?, para_scores_json = ?,
                dominant_bucket = ?, classification_confidence = ?, reasons_json = ?, flags_json = ?, sensitivity = ?
            WHERE rel_path = ?
            """,
            (
                excerpt,
                content_status,
                " ".join(keywords),
                json.dumps(tags, ensure_ascii=False),
                json.dumps(para_scores, ensure_ascii=False),
                dominant_bucket,
                confidence,
                json.dumps(reasons, ensure_ascii=False),
                json.dumps(sorted(set(flags)), ensure_ascii=False),
                tags["sensitivity"][0],
                rel_path,
            ),
        )
        file_tags.append(
            {
                "rel_path": rel_path,
                "excerpt": excerpt,
                "content_status": content_status,
                "keywords": keywords,
                "tags": tags,
                "para_scores": para_scores,
                "dominant_bucket": dominant_bucket,
                "classification_confidence": confidence,
                "reasons": reasons,
                "flags": sorted(set(flags)),
            }
        )

    conn.commit()
    conn.close()

    grouped = [
        {"group_key": key, "count": len(paths_in_group), "paths": sorted(paths_in_group)}
        for key, paths_in_group in similarity_groups.items()
        if len(paths_in_group) > 1
    ]
    grouped.sort(key=lambda item: (-item["count"], item["group_key"]))
    summary = {
        "generated_at": now_iso(),
        "file_count": len(file_tags),
        "similarity_group_count": len(grouped),
        "low_confidence_files": sum(1 for row in file_tags if row["classification_confidence"] < 0.65),
    }

    write_json(paths.semantic_dir / "file_tags.json", file_tags)
    write_json(paths.semantic_dir / "similarity_groups.json", grouped)
    write_json(paths.semantic_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
