---
name: llm-wiki
description: "Maintain and evolve a personal knowledge wiki built on Markdown files. Use this skill when the user wants to compile research notes into structured wiki pages, update existing knowledge pages with new findings, cross-link related concepts, check wiki health (orphan pages, broken links, outdated conclusions), rebuild the wiki index, ask questions that should be answered from their accumulated knowledge base, or test their understanding via exam-style questioning. Also trigger when the user mentions '帮我沉淀', '更新主题页', '知识库健康检查', '帮我把这几篇串起来', '我之前研究过这个吗', '考考我', 'exam', '帮我复习', or anything about maintaining, growing, querying, or self-testing against a long-lived knowledge base — even if they don't say 'wiki' explicitly."
---

# LLM Wiki

A knowledge maintenance skill. It takes notes and research that have already been captured (typically by read or manually) and compiles them into a structured, interlinked, continuously maintained wiki.

Think of it as the "knowledge editor" in a newsroom: read is the reporter who gathers material, and this skill is the editor who turns raw notes into a coherent, navigable, up-to-date knowledge base.

## When to Use

- User wants to compile scattered notes into a structured wiki page
- User wants to update an existing wiki page with new findings
- User wants to cross-link related knowledge pages
- User wants to check wiki health: orphan pages, broken links, outdated conclusions, missing sources
- User wants to query their knowledge base ("what do I know about X")
- User wants to rebuild or review the wiki index
- User wants to start or access the local wiki site ("启动本地wiki", "打开wiki", "本地部署wiki")

## When NOT to Use

- User is asking "is this worth reading?" or wants content intake → use read
- User wants to rebuild the workspace around PARA → use para
- User wants reminders or follow-up on pending tasks or ideas → use remind; full priority planning is outside its scope.

## Operating Zone

The wiki lives inside the user's knowledge base. The wiki root (where all `.md` pages live) is:

```
<knowledge-root>/02-Areas/_wiki/docs/
```

This directory is also the MkDocs `docs_dir` for the static site (GitHub Pages). Any page created or modified here will be included in the next deployment.

The wiki index is:

```
<knowledge-root>/02-Areas/_wiki/docs/index.md
```

The activity log is:

```
<knowledge-root>/02-Areas/_wiki/docs/log.md
```

The MkDocs nav structure is defined in:

```
<knowledge-root>/02-Areas/_wiki/mkdocs.yml
```

When adding or renaming pages, update both `docs/index.md` and the `nav:` section in `mkdocs.yml`.

Source notes live in `03-Resources/articles/共读笔记/`. The wiki reads them but never modifies them.

## Core Principles

These six rules govern every action. When uncertain, fall back to them.

1. **Orient before acting.** Read the index and scan relevant existing pages before doing anything. Never create or modify a page without knowing what's already there.

2. **Find existing before creating new.** Search for pages that already cover the topic. Update, extend, or link to them first. Only create a new page when no existing page is a reasonable home.

3. **Preserve evidence before synthesizing.** Source notes in `03-Resources` are never modified. Wiki pages reference them. When synthesizing conclusions, always note where they came from.

4. **Expose conflicts, don't rush to resolve.** When new information contradicts existing content, keep both versions and mark the section `<!-- status: 待核验 -->`. Do not silently overwrite one with the other. The user decides which version wins.

5. **Human readability first.** Every page starts with a one-sentence summary. Every section should be understandable on its own. Prefer clear prose over dense cross-references.

6. **Maintain the middle layer.** The index and cross-links are the wiki's backbone. Keep them accurate. Don't introduce databases, search engines, or heavy tooling until the simple layer breaks down.

## Four Actions

### 1. Ingest — Compile notes into wiki pages

**When:** User says "帮我沉淀", "把这个整理进知识库", "update the wiki page on X", or there are stable conclusions ready to be compiled.

**Steps:**

1. Read `docs/index.md` to orient.
2. Identify which wiki page(s) this content belongs to. Search by topic keywords across existing pages.
3. If a matching page exists:
   - Read the existing page fully.
   - Add new content as a new section, or extend an existing section.
   - If new content conflicts with existing content, preserve both and add a `<!-- status: 待核验 -->` marker.
   - Update the page's `last_updated` date.
   - Add cross-links to related pages if connections are clear and useful.
4. If no matching page exists:
   - Choose the appropriate page template from `references/page-templates.md`.
   - Create the page with proper frontmatter and structure.
   - Add it to `docs/index.md` and `mkdocs.yml` nav.
   - Add cross-links to related pages.
5. Update `docs/index.md` and `mkdocs.yml` nav if any pages were added, renamed, or re-categorized.
6. Append one entry to `docs/log.md` recording what was done (see Activity Log section below).

**Web 调研补充：**

当本地调研材料可能过时或不够完整时，可使用 Web Search 补充验证。流程：

1. 先基于本地材料起草页面内容。
2. 对关键事实（版本号、功能变更、定价等易过时信息）做 Web Search 交叉验证。
3. 新信息使用证据标注体系（见下文）标注来源。
4. 如果 Web 调研发现本地材料有误，保留两个版本并标记 `<!-- status: 待核验 -->`。
5. **重要：启动多 Agent 并行调研前，必须先向用户确认调研方向和范围**。

**Restraint rules:**
- Don't automatically ingest every note. Only compile when the user asks, or when lint reveals unintegrated stable conclusions.
- Don't batch-update many pages without showing the user the scope first.
- Source notes in `03-Resources/articles/共读笔记/` are read-only — reference them, don't copy their full content into wiki pages.
- Evidence strength matters more than recency. "Newer" does not automatically mean "better." Primary sources (original papers, official docs, firsthand data) outweigh secondary summaries.

### 2. Query — Answer from the knowledge base

**When:** User asks a question their wiki might already answer, or says "what do I know about X", "我之前研究过这个吗".

**Steps:**

1. Read `docs/index.md` and `mkdocs.yml` nav to find relevant pages.
2. Read the relevant page(s).
3. Synthesize an answer from the wiki content, citing which page(s) it draws from.
4. If the wiki doesn't cover the topic well enough, say so clearly. Don't fill gaps with outside knowledge without flagging that it's not from the wiki.
5. If answering reveals that a page is outdated or incomplete, note that as a suggestion — but don't automatically fix it.
6. If the query led to wiki page updates, append one entry to `docs/log.md`. Pure queries with no wiki changes are not logged.

#### 对谈式 Query（Query + Discuss + Ingest）

更常见的使用模式是用户基于 wiki 内容发起讨论，通过多轮对话澄清认知后将结论回写 wiki。流程：

1. 用户指向一个 wiki 页面或其中的某个观点提问。
2. 基于 wiki 内容回答，区分"wiki 已有内容"和"wiki 之外的补充"。
3. 讨论过程中如果需要验证事实，使用 Web Search 并明确标注来源。
4. 讨论收束后，将澄清后的结论回写到对应 wiki 页面：
   - 如果是修正，更新原文并保持证据标注。
   - 如果是补充，新增段落或小节。
   - 如果结论改变了页面结构（如合并/拆分章节），先说明改动范围再执行。
5. 回写后更新 `last_updated` 日期。
6. 在 `docs/log.md` 记录一条 `query` 类型日志（因为产生了 wiki 变更）。

**关键原则**：讨论中涉及的推断和验证过程要在回写时体现——不是直接把结论写进去，而是保留证据标注（确认来源 / 推断），让读者知道结论的可信度。

### 3. Exam — 基于 wiki 的自测问答

**When:** User says "考考我", "exam", "帮我复习", or wants to verify their understanding of wiki content.

**两种启动方式：**

- **指定页面**："考考我 GCA-Runtime-Execution"——围绕该页面出题。
- **不指定页面**："考考我 GCA 相关的"——从该主题下多个页面综合出题。

**出题流程：**

1. 读取目标页面（或按主题范围读取多个页面）。
2. 从页面内容中提炼问题，按以下类型混合出题：
   - **概念题**：某个术语/机制的含义（如"Silent Disconnect 是什么？什么条件下触发？"）
   - **区分题**：容易混淆的概念对比（如"Error Event 和 Failure Output 分支的区别是什么？"）
   - **场景题**：给出一个场景，问怎么设计/会发生什么（如"Data Action 调用超时了，Flow 会怎么走？"）
   - **盲区题**：页面中标注为"推断"或"待核验"的内容，以及页面没有覆盖但逻辑上应该知道的（如"如果 Error Event Handler 自身也报错了呢？"）
3. 一次列出 5-8 个问题，标注每个问题对应的页面和章节。
4. **不主动给出答案**——等用户决定怎么互动。

**互动走向：**

用户可能有三种反应，对应不同走向：

| 用户反应 | 走向 |
|---------|------|
| **不回答，只看题** | 用户自行对照 wiki 反思，无需进一步操作 |
| **回答了某些问题** | 对照 wiki 内容判断回答是否准确，指出遗漏或偏差，引用页面原文 |
| **答不出来或发现 wiki 也没写清楚** | 这暴露了 wiki 的盲区——建议补充内容（转为对谈式 Query 或 Ingest） |

**出题原则：**
- 问题应该能用 wiki 内容回答（不是超纲题），但可以包含需要综合多个章节才能回答的问题。
- 盲区题可以超出 wiki 范围，目的是暴露 wiki 的不完整。标注为"[超出 wiki]"让用户知道。
- 不要出纯记忆题（"Action 上限是多少？"），优先出理解和应用题。
- 如果用户回答暴露了 wiki 表述不清的地方，主动建议改进页面措辞。

### 4. Lint — Check wiki health

**When:** User says "检查一下知识库", "wiki health check", "有没有过期的", or as periodic maintenance.

**Steps:**

1. Run the lint checks defined in `references/lint-rules.md`. If `scripts/lint_wiki.py` exists, use it for mechanical checks first.
2. Report findings grouped by severity:
   - **Broken**: broken links, missing pages referenced by index
   - **Stale**: pages with `<!-- status: 待核验 -->` markers, pages not updated in >6 months
   - **Orphan**: pages not linked from index or any other page
   - **Incomplete**: pages missing sources for key claims, pages still in 草稿 status for >30 days
3. Suggest specific fixes but don't auto-apply. Let the user decide what to address.
4. After fixes are applied, append one entry to `docs/log.md` recording what was checked and what was fixed.

## Page Structure

Every wiki page follows this structure:

```markdown
---
title: Page Title
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: 草稿 | 已看过 | 已确认
tags: [tag1, tag2]
sources:
  - 03-Resources/articles/共读笔记/YYYY-MM-DD-topic.md
visibility: public | private
---

> One-sentence summary of what this page covers.

## Content sections...

## Related Pages

- [[Related Page 1]] — how it relates
- [[Related Page 2]] — how it relates
```

Different page types use different body templates. Read `references/page-templates.md` for the full set: concept pages, comparison pages, decision records, topic overviews, and glossary pages.

### Topic Overview 页的 frontmatter 差异

Topic Overview 页（如 `AI-总览与框架.md`、`CCaaS-平台与架构.md`）是导航枢纽，不是知识内容页。它们的 frontmatter 使用 `type: topic` 替代 `status`，且不需要 `tags` 和 `sources` 字段：

### Visibility 字段

每个页面都有 `visibility` 字段，控制发布时是否包含在公开站点中：

- **`public`**：包含在公开构建中（默认值，新建页面默认为 public）
- **`private`**：仅本地可见，公开构建时自动排除

创建新页面时必须包含此字段。用户可以随时将页面从 public 改为 private 或反向操作。

```markdown
---
title: "主题名"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
type: topic
---
```

Topic 页也不需要 `## Related Pages` 尾部——它们本身就是链接页。

### Page Status

- **草稿**: New page, content is preliminary. May have gaps or unverified claims.
- **已看过**: User has read the page and found it roughly correct.
- **已确认**: User has verified the content. Strongest confidence level.

Status only moves forward when the user explicitly confirms. The skill never auto-promotes status.

## 证据标注体系

对于涉及外部产品/技术的 wiki 页面，每个事实性断言应标注证据来源。使用以下三级标注，以粗体内联方式标注在断言之后：

| 标注 | 含义 | 示例 |
|------|------|------|
| **确认来源：官方文档** | 来自产品官方文档（help pages、developer docs）的明确描述 | `（**确认来源：官方文档**）` |
| **确认来源：社区论坛/博客** | 来自官方论坛、开发者博客、知名技术社区的信息 | `（**确认来源：社区论坛**）` |
| **推断** | 基于已有信息和领域常识的合理推断，未被官方明确证实 | `（**推断**）` |

规则：
- 纯知识概念页（如 AI 术语解释）不需要逐条标注，通常在 frontmatter 的 `sources` 字段列出来源即可。
- 产品/平台文档类页面（如 GCA 系列）应逐条标注，因为这类信息易过时且需要可追溯性。
- 页面底部可加标注说明段落，解释三级标注的含义。
- 标注为"推断"的内容经用户确认或找到官方来源后，应升级标注。

## Activity Log

`docs/log.md` is an append-only activity log that lives alongside the index:

```
<knowledge-root>/02-Areas/_wiki/docs/log.md
```

### Entry format

```markdown
## [YYYY-MM-DD] <action> | <topic short name>

- 新建/更新/删除：affected pages
- 来源：what triggered this action
```

### Action types

| Type | What to log |
|---|---|
| `ingest` | Which pages were created or updated, and what the source material was |
| `query` | Only when the query led to wiki page updates; pure Q&A with no changes is not logged |
| `exam` | Only when exam 暴露了 wiki 盲区并导致页面补充；纯出题无变更不记录 |
| `lint` | What was checked, what problems were found, what was fixed |

### What NOT to log

- Pure queries that didn't change any wiki page
- Mid-conversation discussion, back-and-forth, corrections
- read's reading queue operations
- Each affected file individually — one entry per ingest/lint operation, listing all affected pages together

### Granularity

One entry per operation, not one entry per file. If a single ingest creates 4 pages and updates the index, that's one log entry listing all of them.

## 导航体系

Wiki 有两层导航，各有分工：

### mkdocs.yml nav（主导航）

`mkdocs.yml` 的 `nav:` 是权威的、完整的页面树。**每个 wiki 页面必须出现在 nav 中**。nav 支持多级嵌套，定义了站点的完整结构。

新增或重命名页面时，必须同步更新 nav。

### docs/index.md（精简入口）

`docs/index.md` 是首页，只展示一级/二级主题分类和 topic 页链接，不列出每个子页面。它是读者进入 wiki 的入口，不是完整索引。

```markdown
## 主题分类名

- [Topic 页标题](Topic-页.md) — 一句话概述
```

Rules:
- index.md 只需列出 topic overview 页，不需要列出 topic 下的每个子页面。
- 当新增一个主题分类时，同步更新 index.md。
- 子页面的导航由 mkdocs.yml nav 和 topic 页负责，不在 index.md 中重复。

## Handoff with Other Skills

| From | To | Trigger |
|---|---|---|
| read | llm-wiki | Stable conclusions in 02-Areas need compiling or linking |
| llm-wiki | read | Wiki page references source material that needs deeper reading |
| llm-wiki | para | Wiki workspace needs PARA organization |
| para | llm-wiki | After PARA rebuild, wiki index may need updating |

## 5. Serve — 启动本地 Wiki

**When:** User says "启动本地wiki", "打开wiki", "本地部署wiki", or similar.

**Steps:**

1. Run the serve script:
   ```bash
   bash <knowledge-root>/02-Areas/_wiki/serve.sh
   ```
2. Wait ~3 seconds for the server to start, then open the browser:
   ```bash
   open http://127.0.0.1:8732
   ```
3. Tell the user the wiki is live at **http://127.0.0.1:8732**

**Notes:**
- Port **8732** is intentionally uncommon — safe to keep running as a background service
- All pages (including `visibility: private`) are served locally — no filtering
- The venv is at `_wiki/.venv/`; the script activates it automatically
- To stop: kill the background process (`停止本次操作启动的进程，按记录的 PID 操作`)

## Scripts

Mechanical tasks use scripts in `scripts/`:

- `scripts/rebuild_index.py --root <path>` — Scan all wiki pages and regenerate导航结构
- `scripts/lint_wiki.py --root <path>` — Check for broken links, orphan pages, missing sources, stale pages

Both scripts support `--dry-run` to preview without writing. `lint_wiki.py` also supports `--json` for machine-readable output.

**注意**：脚本的 `--root` 参数应传入 `_wiki/docs/` 目录。脚本可能需要更新以适配当前的双导航体系（mkdocs.yml nav + index.md）。运行前先用 `--dry-run` 确认行为是否符合预期。

## References

- `references/page-templates.md` — Templates for different page types (concept, comparison, decision record, topic overview)
- `references/lint-rules.md` — Detailed lint check rules and severity levels
- `references/scaling.md` — What to do when the wiki outgrows a single index (read when needed)

## Collection status

This skill is manually selected. Use read-only inspection by default. The index rebuilder is not approved for the current two-layer navigation; do not execute its writing mode until the migration in the audit is complete. Resolve `<knowledge-root>` from the user or workspace profile; never treat the placeholder as a literal path. The lint script has no `--dry-run` flag: it is already read-only.
