#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import defaultdict

from workspace_lib import connect_db, ensure_workspace, human_size, init_db, now_iso, paths_for, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a tree-shaped workspace index.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument("--focus-path", default="", help="Optional relative directory to render as the root of the tree")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum depth to expand from the focus root")
    parser.add_argument("--max-children", type=int, default=40, help="Maximum child directories to show per directory")
    parser.add_argument("--include-files", action="store_true", help="Include direct file nodes when practical")
    parser.add_argument("--file-limit", type=int, default=20, help="Maximum direct files to show per directory")
    return parser.parse_args()


def load_dirs(conn: sqlite3.Connection) -> tuple[dict[str, dict], dict[str, list[str]]]:
    rows = conn.execute(
        """
        SELECT rel_path, parent_rel_path, name, depth, direct_dir_count, direct_file_count, total_file_count,
               total_size, dominant_bucket, dominant_topic, granularity_decision, granularity_confidence, flags_json
        FROM dirs
        ORDER BY rel_path ASC
        """
    ).fetchall()
    by_path: dict[str, dict] = {}
    children: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        rel_path = str(row["rel_path"])
        by_path[rel_path] = {
            "rel_path": rel_path,
            "parent_rel_path": row["parent_rel_path"],
            "name": row["name"],
            "depth": int(row["depth"] or 0),
            "direct_dir_count": int(row["direct_dir_count"] or 0),
            "direct_file_count": int(row["direct_file_count"] or 0),
            "total_file_count": int(row["total_file_count"] or 0),
            "total_size": int(row["total_size"] or 0),
            "total_size_human": human_size(int(row["total_size"] or 0)),
            "dominant_bucket": row["dominant_bucket"],
            "dominant_topic": row["dominant_topic"],
            "granularity_decision": row["granularity_decision"],
            "granularity_confidence": float(row["granularity_confidence"] or 0.0),
            "flags": json.loads(row["flags_json"] or "[]"),
        }
        parent = row["parent_rel_path"]
        if parent is not None:
            children[str(parent)].append(rel_path)
    for parent, child_list in children.items():
        child_list.sort()
    return by_path, children


def load_files(conn: sqlite3.Connection) -> dict[str, list[dict]]:
    rows = conn.execute(
        """
        SELECT rel_path, dir_rel_path, name, ext, size, dominant_bucket, classification_confidence, flags_json, is_junk
        FROM files
        ORDER BY dir_rel_path ASC, rel_path ASC
        """
    ).fetchall()
    files_by_dir: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if bool(row["is_junk"]):
            continue
        files_by_dir[str(row["dir_rel_path"])].append(
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
    return files_by_dir


def sort_child_dirs(child_paths: list[str], dir_map: dict[str, dict]) -> list[str]:
    return sorted(
        child_paths,
        key=lambda rel_path: (-dir_map[rel_path]["total_size"], rel_path.lower()),
    )


def make_dir_label(node: dict, focus_path: str) -> str:
    if node["rel_path"] == focus_path:
        name = node["name"] if focus_path else "."
    else:
        name = node["name"]
    line = f"{name}/ [{node['total_file_count']} files, {node['total_size_human']}]"
    if node.get("dominant_topic"):
        line += f" <{node['dominant_topic']}>"
    return line


def make_file_label(node: dict) -> str:
    line = f"{node['name']} [{node['size_human']}]"
    if node.get("dominant_bucket"):
        line += f" <{node['dominant_bucket']}>"
    return line


def build_tree_node(
    rel_path: str,
    dir_map: dict[str, dict],
    child_dirs: dict[str, list[str]],
    files_by_dir: dict[str, list[dict]],
    focus_path: str,
    current_depth: int,
    max_depth: int,
    max_children: int,
    include_files: bool,
    file_limit: int,
) -> dict:
    node = dict(dir_map[rel_path])
    node["node_type"] = "dir"
    node["children"] = []
    node["truncated"] = {"dirs_hidden": 0, "files_hidden": 0}

    raw_child_dirs = sort_child_dirs(child_dirs.get(rel_path, []), dir_map)
    shown_child_dirs = raw_child_dirs[:max_children]
    node["truncated"]["dirs_hidden"] = max(0, len(raw_child_dirs) - len(shown_child_dirs))

    if current_depth < max_depth:
        for child_rel in shown_child_dirs:
            node["children"].append(
                build_tree_node(
                    child_rel,
                    dir_map,
                    child_dirs,
                    files_by_dir,
                    focus_path,
                    current_depth + 1,
                    max_depth,
                    max_children,
                    include_files,
                    file_limit,
                )
            )

    if include_files:
        direct_files = files_by_dir.get(rel_path, [])
        show_files = False
        if current_depth >= max_depth:
            show_files = True
        elif node["direct_dir_count"] == 0:
            show_files = True
        elif node["direct_file_count"] <= file_limit:
            show_files = True
        if show_files:
            shown_files = direct_files[:file_limit]
            node["children"].extend(
                {
                    "node_type": "file",
                    **item,
                }
                for item in shown_files
            )
            node["truncated"]["files_hidden"] = max(0, len(direct_files) - len(shown_files))

    return node


def render_tree_lines(node: dict, prefix: str = "", is_last: bool = True, focus_path: str = "") -> list[str]:
    lines: list[str] = []
    connector = "└── " if is_last else "├── "
    if node["node_type"] == "dir":
        label = make_dir_label(node, focus_path)
    else:
        label = make_file_label(node)

    if prefix == "":
        lines.append(label)
    else:
        lines.append(f"{prefix}{connector}{label}")

    next_prefix = prefix + ("    " if is_last else "│   ")
    children = node.get("children", [])
    for index, child in enumerate(children):
        child_is_last = index == len(children) - 1 and not any(node["truncated"].values())
        lines.extend(render_tree_lines(child, next_prefix, child_is_last, focus_path))

    if node["node_type"] == "dir":
        hidden_dirs = int(node["truncated"].get("dirs_hidden") or 0)
        hidden_files = int(node["truncated"].get("files_hidden") or 0)
        hidden_parts = []
        if hidden_dirs:
            hidden_parts.append(f"{hidden_dirs} dirs hidden")
        if hidden_files:
            hidden_parts.append(f"{hidden_files} files hidden")
        if hidden_parts:
            lines.append(f"{next_prefix}└── … [{', '.join(hidden_parts)}]")
    return lines


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    conn = connect_db(paths)
    init_db(conn)
    dir_map, child_dirs = load_dirs(conn)
    files_by_dir = load_files(conn)
    conn.close()

    focus_path = args.focus_path.strip().strip("/")
    if focus_path not in dir_map:
        raise SystemExit(f"Focus path not found in index: {focus_path or '.'}")

    tree_root = build_tree_node(
        rel_path=focus_path,
        dir_map=dir_map,
        child_dirs=child_dirs,
        files_by_dir=files_by_dir,
        focus_path=focus_path,
        current_depth=0,
        max_depth=max(args.max_depth, 0),
        max_children=max(args.max_children, 1),
        include_files=args.include_files,
        file_limit=max(args.file_limit, 1),
    )

    tree_payload = {
        "generated_at": now_iso(),
        "root": str(root),
        "focus_path": focus_path,
        "max_depth": args.max_depth,
        "max_children": args.max_children,
        "include_files": args.include_files,
        "file_limit": args.file_limit,
        "tree": tree_root,
    }

    suffix = "workspace_tree" if not focus_path else f"workspace_tree__{focus_path.replace('/', '__')}"
    json_path = paths.metadata_dir / f"{suffix}.json"
    md_path = paths.metadata_dir / f"{suffix}.md"
    write_json(json_path, tree_payload)
    md_path.write_text("\n".join(render_tree_lines(tree_root, focus_path=focus_path)) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "generated_at": tree_payload["generated_at"],
                "focus_path": focus_path,
                "output_json": str(json_path),
                "output_md": str(md_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
