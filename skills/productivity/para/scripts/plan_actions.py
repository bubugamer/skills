#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from workspace_lib import (
    DISPLAY_TO_LOGICAL,
    bucket_dir,
    clamp,
    connect_db,
    ensure_workspace,
    existing_paths_outside_catalog,
    existing_para_bucket,
    first_component,
    flattened_source_fragment,
    infer_form,
    init_db,
    load_profile,
    looks_like_coded_category,
    looks_like_generic_media_name,
    now_iso,
    paths_for,
    read_json,
    resolve_root,
    safe_path_component,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PARA, move, quarantine, and package plans.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument(
        "--mode",
        default="para",
        choices=["para", "quarantine", "package", "all"],
        help="Plan mode to generate",
    )
    return parser.parse_args()


def load_file_records(conn) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT rel_path, dir_rel_path, name, ext, size, dominant_bucket, classification_confidence,
               tags_json, flags_json, sensitivity, is_junk, exact_duplicate_group
        FROM files
        ORDER BY rel_path
        """
    ).fetchall()
    output = []
    for row in rows:
        tags = json.loads(row["tags_json"] or "{}")
        output.append(
            {
                "rel_path": row["rel_path"],
                "dir_rel_path": row["dir_rel_path"],
                "name": row["name"],
                "ext": row["ext"],
                "size": int(row["size"] or 0),
                "dominant_bucket": row["dominant_bucket"] or "Resources",
                "classification_confidence": float(row["classification_confidence"] or 0.0),
                "topic": (tags.get("topic") or ["Unsorted"])[0],
                "flags": json.loads(row["flags_json"] or "[]"),
                "sensitivity": row["sensitivity"] or "low",
                "is_junk": bool(row["is_junk"]),
                "exact_duplicate_group": row["exact_duplicate_group"],
            }
        )
    return output


def detect_workspace_structure(root: Path, dir_rows: list[Any]) -> dict[str, Any]:
    top_dirs = [str(row["rel_path"]) for row in dir_rows if int(row["depth"] or 0) == 1]
    coded_top_dirs = [rel_path for rel_path in top_dirs if looks_like_coded_category(Path(rel_path).name)]
    root_note_files = [item.name for item in root.iterdir() if item.is_file() and item.name.startswith("编码说明")]
    coded_taxonomy_detected = bool(root_note_files) or (
        len(coded_top_dirs) >= 3 and len(coded_top_dirs) >= max(1, round(len(top_dirs) * 0.4))
    )
    return {
        "coded_taxonomy_detected": coded_taxonomy_detected,
        "coded_top_level_dirs": sorted(coded_top_dirs),
        "root_note_files": sorted(root_note_files),
    }


def compute_directory_metrics(
    conn, file_records: list[dict[str, Any]], structure_profile: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    dir_rows = conn.execute(
        """
        SELECT rel_path, parent_rel_path, name, depth, direct_dir_count, direct_file_count, total_file_count, total_size
        FROM dirs
        ORDER BY depth DESC, rel_path ASC
        """
    ).fetchall()
    children_dirs: dict[str, list[str]] = defaultdict(list)
    direct_files: dict[str, list[dict[str, Any]]] = defaultdict(list)
    descendant_files: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for record in file_records:
        direct_files[record["dir_rel_path"]].append(record)
        ancestors = [""]
        if record["dir_rel_path"]:
            parts = record["dir_rel_path"].split("/")
            ancestors.extend("/".join(parts[:index]) for index in range(1, len(parts) + 1))
        for ancestor in ancestors:
            descendant_files[ancestor].append(record)

    for row in dir_rows:
        parent = row["parent_rel_path"]
        if parent is not None:
            children_dirs[parent].append(row["rel_path"])

    metrics: dict[str, dict[str, Any]] = {}
    for row in dir_rows:
        rel_path = str(row["rel_path"])
        records = descendant_files.get(rel_path, [])
        non_junk_records = [record for record in records if not record["is_junk"]]
        total = len(records)
        bucket_counts = Counter(record["dominant_bucket"] for record in non_junk_records)
        topic_counts = Counter(record["topic"] for record in non_junk_records)
        ext_counts = Counter(record["ext"] for record in non_junk_records)
        form_counts = Counter(infer_form(record["ext"]) for record in non_junk_records)
        low_conf_count = sum(1 for record in records if record["classification_confidence"] < 0.65)
        junk_count = sum(1 for record in records if record["is_junk"])

        dominant_bucket, dominant_bucket_count = ("Resources", 0)
        if bucket_counts:
            dominant_bucket, dominant_bucket_count = bucket_counts.most_common(1)[0]
        dominant_topic = "Unsorted"
        dominant_topic_count = 0
        if topic_counts:
            dominant_topic, dominant_topic_count = topic_counts.most_common(1)[0]
        dominant_ext_count = ext_counts.most_common(1)[0][1] if ext_counts else 0

        share_bucket = dominant_bucket_count / total if total else 0.0
        share_topic = dominant_topic_count / total if total else 0.0
        share_ext = dominant_ext_count / total if total else 0.0
        low_conf_share = low_conf_count / total if total else 0.0
        junk_share = junk_count / total if total else 0.0
        multi_bucket = sum(1 for _, count in bucket_counts.items() if total and count / total >= 0.2)
        media_count = form_counts["image"] + form_counts["video"] + form_counts["audio"]
        media_share = media_count / len(non_junk_records) if non_junk_records else 0.0
        generic_media_count = sum(
            1
            for record in non_junk_records
            if infer_form(record["ext"]) in {"image", "video"} and looks_like_generic_media_name(Path(record["name"]).stem)
        )
        generic_media_share = generic_media_count / media_count if media_count else 0.0
        cohesion = clamp(0.45 * share_bucket + 0.35 * share_topic + 0.20 * share_ext)
        split_need = clamp(
            (1.0 - share_bucket) * 0.6
            + (1.0 - share_topic) * 0.2
            + low_conf_share * 0.15
            + junk_share * 0.05
            + (0.15 if multi_bucket >= 2 else 0.0)
        )

        lowered = rel_path.lower()
        structure_value = 0.25
        if int(row["direct_dir_count"] or 0) > 0:
            structure_value += 0.25
        if any(keyword in lowered for keyword in ("backup", "archive", "snapshot", "restore", "project")) or any(
            keyword in rel_path for keyword in ("备份", "归档", "恢复", "项目")
        ):
            structure_value += 0.25
        if total <= 8:
            structure_value += 0.15
        if share_bucket >= 0.7:
            structure_value += 0.10
        structure_value = clamp(structure_value)

        is_top_level = bool(rel_path) and "/" not in rel_path
        preserve_top_level_taxonomy = (
            structure_profile.get("coded_taxonomy_detected", False)
            and is_top_level
            and looks_like_coded_category(Path(rel_path).name)
        )
        archive_container_like = bool(rel_path) and (
            any(keyword in lowered for keyword in ("backup", "archive", "snapshot", "restore", "wechat files", "tencent files"))
            or any(keyword in rel_path for keyword in ("备份", "归档", "恢复", "待删除", "重复照片"))
        )
        media_collection_like = total >= 20 and media_share >= 0.75 and generic_media_share >= 0.55
        flags: list[str] = []

        if rel_path == "":
            decision = "children"
        elif preserve_top_level_taxonomy:
            decision = "dir"
            structure_value = max(structure_value, 0.95)
            flags.append("preserve_top_level_taxonomy")
        elif archive_container_like and total > 0:
            decision = "dir"
            structure_value = max(structure_value, 0.92)
            flags.append("archive_container_like")
        elif media_collection_like:
            decision = "dir"
            structure_value = max(structure_value, 0.90)
            flags.append("preserve_media_collection")
        elif total == 0:
            decision = "dir"
        elif cohesion >= 0.78 and split_need <= 0.35:
            decision = "dir"
        elif int(row["direct_dir_count"] or 0) > 0 and split_need >= 0.55:
            decision = "children"
        elif int(row["direct_dir_count"] or 0) == 0 and split_need >= 0.55:
            decision = "files"
        elif total <= 8 and cohesion >= 0.55:
            decision = "dir"
        elif int(row["direct_dir_count"] or 0) > 0:
            decision = "children"
        else:
            decision = "files"

        if preserve_top_level_taxonomy:
            granularity_confidence = 0.98
        elif archive_container_like:
            granularity_confidence = clamp(0.70 + 0.20 * structure_value + 0.10 * cohesion)
        elif media_collection_like:
            granularity_confidence = clamp(0.68 + 0.18 * structure_value + 0.14 * cohesion)
        elif decision == "dir":
            granularity_confidence = clamp(0.48 + 0.38 * cohesion + 0.14 * structure_value - 0.18 * split_need)
        elif decision == "children":
            granularity_confidence = clamp(0.45 + 0.35 * split_need + 0.15 * structure_value - 0.10 * low_conf_share)
        else:
            granularity_confidence = clamp(0.42 + 0.45 * split_need - 0.20 * cohesion)

        if granularity_confidence < 0.65:
            flags.append("low_confidence")

        metrics[rel_path] = {
            "rel_path": rel_path,
            "name": row["name"],
            "parent_rel_path": row["parent_rel_path"],
            "depth": int(row["depth"] or 0),
            "direct_dir_count": int(row["direct_dir_count"] or 0),
            "direct_file_count": int(row["direct_file_count"] or 0),
            "total_file_count": int(row["total_file_count"] or 0),
            "total_size": int(row["total_size"] or 0),
            "dominant_bucket": dominant_bucket,
            "dominant_topic": dominant_topic,
            "bucket_distribution": dict(bucket_counts),
            "cohesion_score": cohesion,
            "split_need_score": split_need,
            "structure_value_score": structure_value,
            "granularity_decision": decision,
            "granularity_confidence": granularity_confidence,
            "child_dirs": sorted(children_dirs.get(rel_path, [])),
            "direct_files": direct_files.get(rel_path, []),
            "descendant_files": records,
            "flags": flags,
        }
    return metrics


def build_units(metrics: dict[str, dict[str, Any]], root_files: list[dict[str, Any]], profile: dict[str, Any]) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []

    def add_file_unit(record: dict[str, Any], origin: str) -> None:
        if record["is_junk"]:
            return
        units.append(
            {
                "source_path": record["rel_path"],
                "unit_type": "file",
                "source_scope": origin,
                "dominant_bucket": record["dominant_bucket"],
                "topic": record["topic"],
                "classification_confidence": record["classification_confidence"],
                "granularity_confidence": 0.90,
                "confidence": record["classification_confidence"],
                "flags": list(record["flags"]),
                "duplicate_status": "exact_duplicate" if record["exact_duplicate_group"] else "unique",
                "sensitivity": record["sensitivity"],
            }
        )

    def visit(rel_path: str) -> None:
        metric = metrics[rel_path]
        decision = metric["granularity_decision"]
        mapped_paths = [Path(bucket_dir(profile, key)) for key in ("projects", "areas", "resources", "archives")]
        if rel_path and any(Path(rel_path) in path.parents for path in mapped_paths):
            decision = "children"
        elif rel_path and existing_para_bucket(rel_path, profile):
            decision = "dir"
        if rel_path != "" and decision == "dir":
            confidence = min(
                clamp(0.40 + 0.60 * (metric["bucket_distribution"].get(metric["dominant_bucket"], 0) / max(metric["total_file_count"], 1))),
                metric["granularity_confidence"],
            )
            units.append(
                {
                    "source_path": rel_path,
                    "unit_type": "dir",
                    "source_scope": "directory_unit",
                    "dominant_bucket": metric["dominant_bucket"],
                    "topic": metric["dominant_topic"],
                    "classification_confidence": confidence,
                    "granularity_confidence": metric["granularity_confidence"],
                    "confidence": min(confidence, metric["granularity_confidence"]),
                    "flags": list(metric["flags"]),
                    "duplicate_status": "has_duplicates"
                    if any(record["exact_duplicate_group"] for record in metric["descendant_files"])
                    else "unique",
                    "sensitivity": "high"
                    if any(record["sensitivity"] == "high" for record in metric["descendant_files"])
                    else "medium"
                    if any(record["sensitivity"] == "medium" for record in metric["descendant_files"])
                    else "low",
                }
            )
            return

        if decision == "children":
            for child in metric["child_dirs"]:
                visit(child)
            for record in metric["direct_files"]:
                add_file_unit(record, "direct_file_from_child_split")
            return

        if decision == "files":
            for record in metric["descendant_files"]:
                add_file_unit(record, "descendant_file_split")
            return

        for child in metric["child_dirs"]:
            visit(child)
        for record in metric["direct_files"]:
            add_file_unit(record, "fallback_file")

    for record in root_files:
        add_file_unit(record, "root_file")
    for child in metrics[""]["child_dirs"]:
        visit(child)

    deduped: dict[str, dict[str, Any]] = {}
    for unit in units:
        deduped[unit["source_path"]] = unit
    return sorted(deduped.values(), key=lambda item: (item["unit_type"] != "dir", item["source_path"]))


def build_target_path(unit: dict[str, Any], profile: dict[str, Any]) -> tuple[str, str, list[str]]:
    flags = list(unit["flags"])
    bucket = str(unit["dominant_bucket"] or "Resources")
    source_path = str(unit["source_path"])
    base_name = Path(source_path).name
    topic = safe_path_component(str(unit["topic"] or "Unsorted"))
    confidence = float(unit["confidence"] or 0.0)
    lowered_source = source_path.lower()

    mapped_bucket = existing_para_bucket(source_path, profile)
    if mapped_bucket:
        return mapped_bucket, source_path, flags + ["existing_para_location", "keep_in_place"]

    if "/" not in source_path and base_name.startswith("编码说明"):
        return "Keep", source_path, flags + ["workspace_taxonomy_note", "keep_in_place"]

    if "待删除" in source_path or "to delete" in lowered_source or "todelete" in lowered_source:
        return "ToDelete", f"{bucket_dir(profile, 'to_delete')}/{base_name}", flags + ["quarantine_container"]

    if confidence < 0.65:
        return "Resources", f"{bucket_dir(profile, 'unsorted')}/{flattened_source_fragment(source_path)}", flags + ["unsorted_target"]

    logical = DISPLAY_TO_LOGICAL.get(bucket, "resources")
    root_dir = bucket_dir(profile, logical)
    if logical == "archives" and ("snapshot_like" in flags or "chat_export" in flags):
        root_dir = bucket_dir(profile, "snapshots")
    if unit["unit_type"] == "dir":
        if any(flag in flags for flag in ("preserve_top_level_taxonomy", "archive_container_like", "preserve_media_collection")):
            target = f"{root_dir}/{base_name}"
        elif topic != safe_path_component(base_name):
            target = f"{root_dir}/{topic}/{base_name}"
        else:
            target = f"{root_dir}/{base_name}"
    else:
        target = f"{root_dir}/{topic}/{base_name}"
    return bucket, target, flags


def resolve_target_conflicts(items: list[dict[str, Any]], profile: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    occupied = existing_paths_outside_catalog(root)
    target_map: Counter[str] = Counter()
    for item in items:
        target_map[item["target_rel_path"]] += 1

    resolved: list[dict[str, Any]] = []
    reserved = set(occupied) | set(target_map)
    for item in items:
        target = item["target_rel_path"]
        if target == item["source_path"]:
            item["action"] = "keep"
        if target_map[target] > 1 or (target in occupied and target != item["source_path"]):
            item["flags"] = sorted(set(item["flags"] + ["target_conflict"]))
            item["target_bucket"] = "Resources"
            fallback = f"{bucket_dir(profile, 'conflicts')}/{flattened_source_fragment(item['source_path'])}"
            candidate = fallback
            suffix = 2
            while candidate in reserved:
                candidate = f"{fallback}__{suffix}"
                suffix += 1
            reserved.add(candidate)
            item["target_rel_path"] = candidate
            item["confidence"] = min(float(item["confidence"]), 0.64)
        resolved.append(item)
    return resolved


def write_dir_metrics(conn, metrics: dict[str, dict[str, Any]]) -> None:
    for metric in metrics.values():
        conn.execute(
            """
            UPDATE dirs
            SET dominant_bucket = ?, dominant_topic = ?, bucket_distribution_json = ?, cohesion_score = ?,
                split_need_score = ?, structure_value_score = ?, granularity_decision = ?,
                granularity_confidence = ?, summary = ?, flags_json = ?
            WHERE rel_path = ?
            """,
            (
                metric["dominant_bucket"],
                metric["dominant_topic"],
                json.dumps(metric["bucket_distribution"], ensure_ascii=False),
                metric["cohesion_score"],
                metric["split_need_score"],
                metric["structure_value_score"],
                metric["granularity_decision"],
                metric["granularity_confidence"],
                f"{metric['dominant_topic']} -> {metric['dominant_bucket']} ({metric['granularity_decision']})",
                json.dumps(metric["flags"], ensure_ascii=False),
                metric["rel_path"],
            ),
        )
    conn.commit()


def build_quarantine_plan(file_records: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    items = []
    for record in file_records:
        if not record["is_junk"]:
            continue
        items.append(
            {
                "source_path": record["rel_path"],
                "action": "quarantine",
                "target_bucket": "ToDelete",
                "target_rel_path": f"{bucket_dir(profile, 'to_delete')}/{record['rel_path']}",
                "reasons": ["matched junk rule"],
            }
        )
    return {"generated_at": now_iso(), "item_count": len(items), "items": items}


def build_package_plan() -> dict[str, Any]:
    return {
        "generated_at": now_iso(),
        "item_count": 0,
        "items": [],
        "note": "Populate this plan from an explicit user request that identifies sources and archive targets.",
    }


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    profile = load_profile(paths)
    conn = connect_db(paths)
    init_db(conn)

    file_records = load_file_records(conn)
    dir_rows = conn.execute(
        """
        SELECT rel_path, depth
        FROM dirs
        ORDER BY depth ASC, rel_path ASC
        """
    ).fetchall()
    structure_profile = detect_workspace_structure(root, dir_rows)
    metrics = compute_directory_metrics(conn, file_records, structure_profile)
    write_dir_metrics(conn, metrics)

    para_plan: dict[str, Any] = {"generated_at": now_iso(), "item_count": 0, "items": [], "summary": {}}
    if args.mode in {"para", "all"}:
        root_files = [record for record in file_records if record["dir_rel_path"] == ""]
        units = build_units(metrics, root_files, profile)
        planned_items = []
        for unit in units:
            target_bucket, target_rel_path, flags = build_target_path(unit, profile)
            planned_items.append(
                {
                    "source_path": unit["source_path"],
                    "unit_type": unit["unit_type"],
                    "source_scope": unit["source_scope"],
                    "action": "move",
                    "target_bucket": target_bucket,
                    "target_rel_path": target_rel_path,
                    "classification_confidence": round(float(unit["classification_confidence"]), 4),
                    "granularity_confidence": round(float(unit["granularity_confidence"]), 4),
                    "confidence": round(float(unit["confidence"]), 4),
                    "reasons": [
                        f"dominant bucket -> {unit['dominant_bucket']}",
                        f"topic -> {unit['topic']}",
                        f"source scope -> {unit['source_scope']}",
                    ],
                    "flags": flags,
                    "duplicate_status": unit["duplicate_status"],
                    "sensitivity": unit["sensitivity"],
                }
            )
        planned_items = resolve_target_conflicts(planned_items, profile, root)
        summary = {
            "generated_at": now_iso(),
            "item_count": len(planned_items),
            "by_bucket": Counter(item["target_bucket"] for item in planned_items),
            "by_unit_type": Counter(item["unit_type"] for item in planned_items),
            "low_confidence_items": sum(1 for item in planned_items if item["confidence"] < 0.65),
            "keep_items": sum(1 for item in planned_items if item["action"] == "keep"),
            "structure_profile": structure_profile,
        }
        para_plan = {
            "generated_at": now_iso(),
            "item_count": len(planned_items),
            "summary": summary,
            "items": planned_items,
        }
        write_json(paths.plans_dir / "para_plan.json", para_plan)
        write_json(
            paths.plans_dir / "move_plan.json",
            {
                "generated_at": now_iso(),
                "item_count": len([item for item in planned_items if item["action"] == "move"]),
                "items": [item for item in planned_items if item["action"] == "move"],
            },
        )

    quarantine_plan = build_quarantine_plan(file_records, profile)
    write_json(paths.plans_dir / "quarantine_plan.json", quarantine_plan)
    package_plan = build_package_plan()
    write_json(paths.plans_dir / "package_plan.json", package_plan)
    conn.close()

    payload = {
        "generated_at": now_iso(),
        "mode": args.mode,
        "para_items": para_plan.get("item_count", 0),
        "quarantine_items": quarantine_plan["item_count"],
        "package_items": package_plan["item_count"],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
