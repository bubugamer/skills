---
name: social-feed
description: Extract recent items from X home feed, Weibo home timeline, or a public Weibo profile using saved local browser state when needed. Use when the user wants Codex to scan `x.com/home`, `m.weibo.cn` logged-in feed, or a public Weibo profile URL and return structured items with timestamps and jump links for downstream use, especially when a brief or watchlist depends on these feeds. Also use for requests like “抓一下 X 首页”, “看看微博关注流”, “扫一下这个微博 uid”, “把社交时间线内容结构化”, or when `brief` needs X/微博 feed items rather than a single post/article body.
---

# Social Feed

`social-feed` is a feed extraction layer for timeline-style social sources.

Use it to:

- read the logged-in X home feed
- read the logged-in Weibo home timeline
- read a public Weibo profile by uid
- turn visible timeline cards into structured items with timestamps and jump links

It is not a summarizer and it is not a note-taking skill.

## Boundaries

- Use `social-feed` when the user wants recent items from `x.com/home`, `m.weibo.cn` home, or a public Weibo profile page.
- Use `brief` after `social-feed` when the user wants ranking, triage, and a compact digest.
- Use `site-unlocker` for a single X post, Weibo status page, article page, paywalled page, or other one-off page where the goal is readable body extraction rather than timeline scanning.
- Use `dongnaojin-yeye` after a specific item has been selected and needs deeper reading, translation, or saving.

## What This Skill Returns

Return structured items, not prose by default.

Each item should include, when available:

- source
- author or account label
- timestamp
- short text snippet
- status URL or direct jump-off URL
- flags such as `is_ad`, `is_video`, or `is_unreadable`

## Default State Files

When running inside a workspace, prefer these default local state files if they exist:

- X home feed: `<workspace>/.playwright-cli/brief/x.auth-state.json`
- Weibo home timeline: `<workspace>/.playwright-cli/brief/weibo.auth-state.json`

If the needed state file does not exist or is expired, do not guess. Follow the auth setup flow in [references/auth-setup.md](references/auth-setup.md).

## Default Workflow

1. Identify which source the user wants:
   - `x-home`
   - `weibo-home`
   - `weibo-profile`
2. Use `scripts/fetch_social_feed.py` to fetch structured items.
3. For X and logged-in Weibo, load the saved state file first.
4. Verify the session is really authenticated before trusting the feed:
   - X: URL is `https://x.com/home`, title is not the login page, and visible `article` elements exist.
   - Weibo home: `api/config` reports `login: true` and the home page shows the `关注` tab.
5. Extract a small batch of recent visible items.
6. Mark ads, empty cards, and unusable cards instead of pretending they are meaningful feed items.
7. If the user asked for a brief, hand the extracted items to `brief`. If the user only asked for structured feed content, return the structured items directly.

## Commands

Use the bundled script instead of rewriting Playwright commands in the transcript:

```bash
python <skill-dir>/scripts/fetch_social_feed.py x-home --limit 8
python <skill-dir>/scripts/fetch_social_feed.py weibo-home --limit 8 --uid <weibo-uid>
python <skill-dir>/scripts/fetch_social_feed.py weibo-profile --uid <weibo-uid> --limit 8
```

If the workspace uses a non-default state-file location, pass it explicitly:

```bash
python <skill-dir>/scripts/fetch_social_feed.py x-home --state-file /abs/path/to/x.auth-state.json
```

## Output Rules

- Keep the extraction output factual and compact.
- Preserve direct jump links whenever available.
- Do not silently drop authentication problems; say the state file is missing or expired.
- Do not fabricate timestamps or links.
- Do not summarize the feed into a brief inside this skill unless the user explicitly asked for that and no separate `brief` handoff is needed.

## Source-Specific Notes

### X Home Feed

- Prefer the logged-in `For You` feed at `https://x.com/home`.
- Mark promoted posts as ads and deprioritize them.
- Preserve the status URL for each useful item.

### Weibo Home Timeline

- Prefer the logged-in home page at `https://m.weibo.cn/`.
- Confirm it is the real logged-in homepage by checking both `api/config` and the visible `关注` tab.
- Preserve `https://m.weibo.cn/status/<id>` links when the card exposes them.

### Public Weibo Profile

- Read `https://m.weibo.cn/u/<uid>`.
- Treat cards with “仅自己可见” or similar platform visibility notices as unavailable.
- Do not force profile items into a “today” brief when the profile has no recent public posts.

## Do Not Do

- Do not ask the user to paste passwords into chat.
- Do not claim a feed is authenticated if only the public homepage is visible.
- Do not confuse a public Weibo profile with the logged-in Weibo home timeline.
- Do not keep retyping raw Playwright extraction snippets when the bundled script already covers the workflow.

## Report Structure

When returning the feed extraction itself, use this shape:

### Source

One short line naming the source and whether authentication succeeded.

### Items

- Short item label
  Timestamp, why it is usable or not, and the direct jump link if present.

### Notes

- Missing state file
- Expired auth
- Ads filtered
- Public-profile recency caveat

## References

- [references/auth-setup.md](references/auth-setup.md): how to create and verify reusable X / Weibo state files


## Locating bundled scripts

Resolve `<skill-dir>` to the absolute folder containing this SKILL.md before running a command. Paths beginning `scripts/` are relative to that folder, not to the user workspace. Keep the user workspace as the working directory when a script uses `--root .`.
