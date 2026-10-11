#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from workspace_lib import ensure_workspace, paths_for, read_json, resolve_root

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSET_DIR = SKILL_DIR / "assets" / "review-desk"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the lightweight review desk.")
    parser.add_argument("--root", default=".", help="Workspace root directory")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8765, help="Bind port")
    return parser.parse_args()


def build_overview(paths) -> dict:
    manifest = read_json(paths.manifest_path, {})
    review = read_json(paths.review_dir / "summary.json", {})
    plan = read_json(paths.plans_dir / "para_plan.json", {})
    return {"manifest": manifest, "review": review, "plan": plan.get("summary", {})}


def handler_factory(paths):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ASSET_DIR), **kwargs)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/api/overview":
                payload = json.dumps(build_overview(paths), ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return
            super().do_GET()

    return Handler


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    paths = paths_for(root)
    ensure_workspace(paths)
    server = ThreadingHTTPServer((args.host, args.port), handler_factory(paths))
    print(json.dumps({"ok": True, "url": f"http://{args.host}:{args.port}"}, ensure_ascii=False))
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
