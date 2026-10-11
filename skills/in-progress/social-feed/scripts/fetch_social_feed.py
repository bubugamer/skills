#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shlex
import subprocess
import sys
import time
import uuid
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch structured items from X or Weibo feeds.")
    parser.add_argument(
        "source",
        choices=["x-home", "weibo-home", "weibo-profile"],
        help="Feed source to fetch.",
    )
    parser.add_argument("--limit", type=int, default=8, help="Maximum number of visible items to return.")
    parser.add_argument("--uid", help="Weibo uid for weibo-profile or expected uid for weibo-home verification.")
    parser.add_argument("--state-file", help="Explicit auth-state file path for X or logged-in Weibo.")
    parser.add_argument("--browser", default="chrome", help="Browser channel to use with playwright-cli.")
    parser.add_argument("--headed", action="store_true", help="Run the browser in headed mode.")
    return parser.parse_args()


def default_state_file(source: str) -> pathlib.Path | None:
    cwd = pathlib.Path.cwd()
    if source == "x-home":
        return cwd / ".playwright-cli" / "brief" / "x.auth-state.json"
    if source == "weibo-home":
        return cwd / ".playwright-cli" / "brief" / "weibo.auth-state.json"
    return None


def pwcli_path() -> pathlib.Path:
    code_home = pathlib.Path(os.environ.get("CODEX_HOME", pathlib.Path.home() / ".codex"))
    path = code_home / "skills" / "playwright" / "scripts" / "playwright_cli.sh"
    if not path.exists():
        raise FileNotFoundError(f"playwright wrapper not found: {path}")
    return path


def run_cmd(args: list[str], check: bool = True) -> str:
    proc = subprocess.run(args, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    if check and proc.returncode != 0:
        quoted = " ".join(shlex.quote(part) for part in args)
        raise RuntimeError(f"command failed ({proc.returncode}): {quoted}\n{output.strip()}")
    return output.strip()


def pw(session: str, *parts: str, raw: bool = False, check: bool = True) -> str:
    args = [str(pwcli_path())]
    if raw:
        args.append("--raw")
    args.append(f"-s={session}")
    args.extend(parts)
    return run_cmd(args, check=check)


def parse_raw_value(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(value, str):
        inner = value.strip()
        if inner and inner[0] in "[{":
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                return value
    return value


def wait_for(session: str, expression: str, timeout_s: int = 15, step_s: float = 1.0) -> Any:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        last = parse_raw_value(pw(session, "eval", expression, raw=True))
        if last:
            return last
        time.sleep(step_s)
    return last


def x_items_js(limit: int) -> str:
    return (
        "JSON.stringify("
        "Array.from(document.querySelectorAll('article')).slice(0,"
        f"{limit}"
        ").map((a,i)=>{"
        "const text=(a.innerText||'').replace(/\\s+/g,' ').trim();"
        "const links=Array.from(a.querySelectorAll('a[href]')).map(x=>x.href);"
        "const status=links.find(h=>/\\/status\\//.test(h))||null;"
        "const external=links.find(h=>!h.includes('x.com')&&!h.includes('twitter.com'))||null;"
        "const time=a.querySelector('time')?.getAttribute('datetime')||null;"
        "const isAd=text.includes('广告')||text.includes('Promoted')||text.includes('Order now');"
        "return {index:i+1,time,status_url:status,external_url:external,is_ad:isAd,text:text.slice(0,360)};"
        "})"
        ")"
    )


def weibo_items_js(limit: int) -> str:
    return (
        "JSON.stringify("
        "Array.from(document.querySelectorAll('article')).slice(0,"
        f"{limit}"
        ").map((article,i)=>{"
        "const root=article.parentElement?.parentElement || article.parentElement || article;"
        "const text=(article.innerText||'').replace(/\\s+/g,' ').trim();"
        "const links=Array.from(root.querySelectorAll('a[href]')).map(a=>a.getAttribute('href')).filter(Boolean);"
        "const full=links.find(h=>/\\/status\\//.test(h)) || null;"
        "const headers=Array.from(root.querySelectorAll('h3,h4')).map(el=>el.innerText.trim()).filter(Boolean);"
        "const unreadable=text.includes('仅自己可见') || text.includes('不可见') || text.includes('无法查看');"
        "const isVideo=text.includes('微博视频') || text.includes('次播放');"
        "return {index:i+1,headers,status_url:full ? ('https://m.weibo.cn' + full) : null,is_unreadable:unreadable,is_video:isVideo,text:text.slice(0,320)};"
        "})"
        ")"
    )


def fetch_x_home(args: argparse.Namespace, session: str) -> dict[str, Any]:
    state_file = pathlib.Path(args.state_file) if args.state_file else default_state_file("x-home")
    if not state_file or not state_file.exists():
        raise FileNotFoundError(f"missing X auth-state file: {state_file}")
    pw(session, "open", "about:blank", "--browser", args.browser, *("--headed",) if args.headed else ())
    pw(session, "state-load", str(state_file))
    pw(session, "goto", "https://x.com/home")
    article_count = wait_for(session, "document.querySelectorAll('article').length")
    url = parse_raw_value(pw(session, "eval", "location.href", raw=True))
    title = parse_raw_value(pw(session, "eval", "document.title", raw=True))
    items = parse_raw_value(pw(session, "eval", x_items_js(args.limit), raw=True)) or []
    if not article_count:
        article_count = len(items)
    authenticated = (
        isinstance(url, str)
        and url.startswith("https://x.com/home")
        and "Log in to X" not in str(title)
        and bool(items)
    )
    return {
        "source": "x-home",
        "authenticated": authenticated,
        "state_file": str(state_file),
        "url": url,
        "title": title,
        "article_count": article_count or 0,
        "items": items,
    }


def fetch_weibo_home(args: argparse.Namespace, session: str) -> dict[str, Any]:
    state_file = pathlib.Path(args.state_file) if args.state_file else default_state_file("weibo-home")
    if not state_file or not state_file.exists():
        raise FileNotFoundError(f"missing Weibo auth-state file: {state_file}")
    pw(session, "open", "about:blank", "--browser", args.browser, *("--headed",) if args.headed else ())
    pw(session, "state-load", str(state_file))
    pw(session, "goto", "https://m.weibo.cn/")
    config = parse_raw_value(
        pw(
            session,
            "eval",
            'fetch("https://m.weibo.cn/api/config").then(r=>r.json()).then(x=>JSON.stringify(x))',
            raw=True,
        )
    )
    has_follow_tab = wait_for(
        session,
        'Array.from(document.querySelectorAll("*")).some(el => (el.textContent || "").trim() === "关注")',
    )
    items = parse_raw_value(pw(session, "eval", weibo_items_js(args.limit), raw=True)) or []
    config_data = config.get("data", {}) if isinstance(config, dict) else {}
    uid = str(config_data.get("uid")) if config_data.get("uid") is not None else None
    expected_uid = str(args.uid) if args.uid else None
    authenticated = bool(config_data.get("login")) and bool(has_follow_tab) and (expected_uid is None or uid == expected_uid)
    return {
        "source": "weibo-home",
        "authenticated": authenticated,
        "state_file": str(state_file),
        "url": parse_raw_value(pw(session, "eval", "location.href", raw=True)),
        "title": parse_raw_value(pw(session, "eval", "document.title", raw=True)),
        "config": config,
        "items": items,
    }


def fetch_weibo_profile(args: argparse.Namespace, session: str) -> dict[str, Any]:
    if not args.uid:
        raise ValueError("--uid is required for weibo-profile")
    url = f"https://m.weibo.cn/u/{args.uid}"
    pw(session, "open", url, "--browser", args.browser, *("--headed",) if args.headed else ())
    items = parse_raw_value(pw(session, "eval", weibo_items_js(args.limit), raw=True)) or []
    headers = parse_raw_value(
        pw(session, "eval", 'JSON.stringify(Array.from(document.querySelectorAll("h3,h4")).slice(0,10).map(x=>x.innerText.trim()))', raw=True)
    )
    return {
        "source": "weibo-profile",
        "uid": str(args.uid),
        "authenticated": False,
        "url": parse_raw_value(pw(session, "eval", "location.href", raw=True)),
        "title": parse_raw_value(pw(session, "eval", "document.title", raw=True)),
        "header_sample": headers or [],
        "items": items,
    }


def main() -> int:
    args = parse_args()
    aliases = {
        "x-home": "xh",
        "weibo-home": "wh",
        "weibo-profile": "wp",
    }
    session = f"sf-{aliases[args.source]}-{uuid.uuid4().hex[:6]}"
    fetchers = {
        "x-home": fetch_x_home,
        "weibo-home": fetch_weibo_home,
        "weibo-profile": fetch_weibo_profile,
    }
    try:
        result = fetchers[args.source](args, session)
    finally:
        try:
            pw(session, "close", check=False)
        except Exception:
            pass
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
