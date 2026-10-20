#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from workspace_lib import ensure_workspace, load_profile, now_iso, paths_for, resolve_root, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize the internal _catalog workspace.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    profile = load_profile(paths)

    write_json(
        paths.manifest_path,
        {
            "generated_at": now_iso(),
            "root": str(root),
            "catalog_dir": str(paths.catalog_dir),
            "status": "initialized",
        },
    )

    payload = {
        "ok": True,
        "generated_at": now_iso(),
        "root": str(root),
        "catalog_dir": str(paths.catalog_dir),
        "profile_path": str(paths.profile_path),
        "organization_mode": profile["organization_mode"],
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
