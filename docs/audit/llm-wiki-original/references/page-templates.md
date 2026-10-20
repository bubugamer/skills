# Page Templates

Wiki pages use different templates depending on their purpose. Choose the closest match. All templates share the same frontmatter structure — only the body sections differ.

## Choosing a Template

- Is it one concept, technology, or idea? → **Concept Page** (#1)
- Is it "X vs Y" or "which approach for Z"? → **Comparison Page** (#2)
- Is it "we decided to do X because Y"? → **Decision Record** (#3)
- Is it a broad area with its own content + sub-links? → **Content Topic Page** (#4)
- Is it a pure navigation hub (only links)? → **Topic Overview** (#5)
- Is it a term glossary with cross-references? → **Glossary Page** (#6)
- None of the above? → Start with Concept Page and adapt.

## 1. Concept Page

For explaining a single concept, technology, framework, or idea.

```markdown
---
title: <concept name>
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: 草稿
tags: []
sources: []
---

> One-sentence definition or summary.

## What It Is

Core definition in plain language.

## How It Works

Mechanism, process, or structure.

## Key Properties

Bullet points of the most important characteristics.

## Common Misconceptions

Things people get wrong about this concept (optional — only include if there are genuine, widespread misunderstandings).

## Related Pages

- [[page]] — relationship
```

## 2. Comparison Page

For comparing two or more alternatives — tools, approaches, frameworks, strategies.

```markdown
---
title: <A> vs <B>
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: 草稿
tags: []
sources: []
---

> One-sentence summary of when to use which.

## Context

Why this comparison matters — what decision or trade-off prompted it.

## Comparison

| Dimension | A | B |
|---|---|---|
| ... | ... | ... |

## When to Use A

## When to Use B

## Open Questions

Dimensions where the answer isn't clear yet.

## Related Pages

- [[page]] — relationship
```

## 3. Decision Record

For documenting a specific decision and its reasoning. Useful when the user wants to remember why they chose one approach over another.

```markdown
---
title: Decision — <short description>
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: 草稿
tags: []
sources: []
---

> One-sentence summary of the decision.

## Context

What prompted this decision — the problem, constraint, or opportunity.

## Options Considered

### Option A

- Pros:
- Cons:

### Option B

- Pros:
- Cons:

## Decision

What was chosen and why.

## Consequences

What changed as a result — both intended and discovered.

## Related Pages

- [[page]] — relationship
```

## 4. Content Topic Page

For a topic area that has substantive content of its own (not just links). Uses standard frontmatter.

```markdown
---
title: <topic name>
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: 草稿
tags: []
sources: []
---

> One-sentence summary of the topic scope.

## Overview

Brief introduction — what this topic covers and why it matters to the user.

## Key Concepts

- [[concept-1]] — one-line description
- [[concept-2]] — one-line description

## Current Understanding

Summary of what the user knows so far about this topic.

## Open Questions

What remains unclear or unresolved.

## Related Pages

- [[page]] — relationship
```

Note: If a topic page is purely a navigation hub (only links, no substantive content), use the **Topic Overview** template (#5) instead.

## 5. Topic Overview (Navigation Hub)

For a broad topic area that links to multiple sub-pages. Acts as a navigational hub, not a content page.

```markdown
---
title: "<topic name>"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
type: topic
---

# Topic Name

> One-sentence scope description.

---

- [Sub-page Title](Sub-page.md) — one-line summary
- [Sub-page Title](Sub-page.md) — one-line summary
```

Notes:
- Uses `type: topic` instead of `status`/`tags`/`sources` — these pages don't contain verifiable claims.
- No `## Related Pages` section — the page itself is a link hub.
- Keep each entry to one line: link + dash + summary.

## 6. Glossary Page

For term definitions with cross-references to detail pages.

```markdown
---
title: <domain> — 术语表
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: 草稿
tags: [domain-tag]
sources: []
---

> 术语快速解释与跳转索引，按功能域分组。

## Category A

| 术语 | 解释 | 详情 |
|------|------|------|
| **Term** | One-sentence definition | [[Detail-Page#section]] |

## Related Pages

- [[page]] — relationship
```

Notes:
- Group terms by functional domain, not alphabetically.
- Each term links to the detail page section where it's explained in depth.
- Only include terms that benefit from a quick-reference definition — don't list every noun.

## Adaptation Notes

- These templates are starting points, not straitjackets. Add or remove sections as the content demands.
- The one non-negotiable elements are: frontmatter with all required fields, the opening `>` summary line, and a `## Related Pages` section at the end.
- Keep section names as short noun phrases. Avoid negative or procedural headings like "What Not to Do" or "Steps Taken".
