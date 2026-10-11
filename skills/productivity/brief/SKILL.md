---
name: brief
description: Build a concise brief from user-provided information sources. Use when the user wants Codex to scan named sources, feeds, newsletters, sites, accounts, or links for topics they care about, pull out what matters, and produce a digest with links for deeper reading instead of full long-form analysis or note-taking. Also use for requests like “帮我盯这几个来源”, “给我一份简报”, “抓一下今天值得看的”, “按这个主题扫一遍信息源”, “看看 X 首页有什么值得读”, “扫一下微博关注流”, or “先帮我筛一下哪些值得点开”.
---

# Brief

`brief` is an intake and briefing layer.

Use it to scan user-specified sources, filter for relevance, and return a compact brief with links for deeper reading.

It does not replace deep reading, long-form summarization, or action planning.

## Boundaries

- Use `brief` when the user wants a quick scan across multiple sources, a short digest, a ranked list of what matters, or a briefing for a theme, project, or watchlist.
- Use `social-feed` before `brief` when the source is a feed-like social timeline such as `x.com/home`, logged-in `m.weibo.cn`, or `m.weibo.cn/u/<uid>`.
- Use `dongnaojin-yeye` when the user wants to deeply read one item, decide whether a single item is worth reading now, translate it, trace its source, or save stable reading notes into the knowledge base.
- Use `tang-monk` when the output should become a decision, exploration item, backlog item, weekly focus, or today's one core push.
- Use `konmari` when the problem is where files or notes should live, how to clean up a workspace, or how to reorganize folders.

If the user wants a real briefing first and deep reading later, use `brief` first and hand off selected items afterward.

## What Counts As Input

Accept inputs such as:

- a list of URLs
- a list of authors, accounts, newsletters, or sites
- a topic plus a small source list
- a watchlist with inclusion and exclusion hints
- a request to check “today”, “this week”, or “recent” items from user-provided sources

If the user has not provided any source list, ask for one or state clearly that the brief cannot be grounded yet.

## Working Rules

1. Start from the user's provided sources.
2. Prefer primary or direct sources over reposts and commentary when both are available.
3. Do a first-pass filter before spending time on detailed reading.
4. Keep the brief short enough that the user can scan it quickly.
5. Preserve jump-off links so the user can go deeper without asking for the whole pipeline again.
6. If a source is unreadable, say so directly rather than pretending the content was reviewed.

## Source Handling

- For ordinary readable pages, read the content directly.
- For feed-like social sources such as X home feed, Weibo home timeline, or a public Weibo profile, call `social-feed` first.
- For single X posts, WeChat pages, login-heavy article pages, JavaScript-heavy pages, or pages that only expose a shell, call `site-unlocker` first.
- Do not use `site-unlocker` as the default first step for `x.com/home` or `m.weibo.cn` timelines when `social-feed` is the better fit.
- If `site-unlocker` does not retrieve readable content, do not fabricate a summary from the shell page.
- If `social-feed` reports missing or expired auth state for X or logged-in Weibo, say so directly instead of pretending the feed was scanned.
- If the user supplied a second-hand summary and the original source is available, prefer the original source.
- If multiple sources say the same thing, keep the best source link and collapse duplicates in the brief.

## Relevance Filter

When choosing what to include, prioritize:

- direct relevance to the user's stated interests
- novelty relative to the other items in the same batch
- information density
- first-hand reporting, original data, or concrete examples
- likely follow-through value if the user clicks through

Downgrade items that are:

- repetitive takes on the same story
- vague commentary without specifics
- low-signal reposts
- clickbait headlines with thin content

## Output Style

The brief should feel like a sharp front page, not a wall of notes.

- Lead with the handful of items worth attention.
- Keep each item compact.
- Include why it matters.
- Include a direct link for deeper reading.
- Make it obvious what to read now and what to park.
- Filter weak items quietly by default instead of listing a separate "可忽略" section, unless the user explicitly asks to see what was filtered out.

Read [references/brief-format.md](references/brief-format.md) before finalizing the response.

## Default Workflow

1. Confirm the source set and the topic or interest filter.
2. Gather candidate items from those sources.
3. If the source set includes X home feed or Weibo timelines, extract those items through `social-feed` first.
4. If the source set includes single-page special links, unlock those pages through `site-unlocker` first.
5. Remove duplicates and thin commentary.
6. Read enough to judge relevance and signal.
7. Produce the brief in the standard format.
8. If the user wants to go deeper on one item, hand that item to `dongnaojin-yeye`.
9. If the brief suggests concrete work, hand that outcome to `TangMonk`.

## Do Not Do

- Do not turn the brief into a long research report by default.
- Do not silently save notes into the knowledge base unless the user explicitly asks for that next step.
- Do not invent source details when a page could not be read.
- Do not confuse “interesting” with “actionable”; `brief` surfaces signals, it does not manage commitments.
- Do not broaden beyond the user's provided source universe unless the user explicitly asks for extra discovery.
- Do not treat a public Weibo profile as if it were a fresh “today” source when the visible posts are old.
- Do not keep ads from X or obvious promotional cards from timelines unless the user explicitly wants ad monitoring.

## Report Structure

Use this structure by default:

### 结论

One short paragraph saying what is worth attention in this batch.

### 本期值得点开

- Item title
  Why it matters in one or two sentences.
  Link: direct source URL

### 可先放入稍后阅读

- Item title
  Why it is secondary.
  Link: direct source URL

### 下一步

Choose only what fits:

- 深入读其中一条
- 继续扩大来源
- 下次继续跟踪同一批来源
- 暂不处理

## Example Triggers

**Example 1:**
Input: “帮我盯这几个 AI 研究博客，给我一份今天值得点开的简报，别铺太开。”
Output: A short relevance-ranked brief with direct links.

**Example 2:**
Input: “把我这几个新闻源里和自动化、agent、开发工具有关的内容筛一下，告诉我哪些值得我点进去看。”
Output: A themed digest with read-now vs park-later triage.

**Example 3:**
Input: “先扫这一批来源，做个 front page，我只想知道今天别错过什么。”
Output: A compact front-page style brief, not a full research memo.
