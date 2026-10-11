---
name: tang-monk
description: Use when the user wants to capture ideas, triage tasks, decide whether an uncertain direction is worth pursuing, choose weekly focus, choose today's one core task, clean up or operate a `00-TangMonk` execution system, or keep a personal priority workflow separate from PARA/content folders.
---

# TangMonk

TangMonk is a personal execution layer that lives in `00-TangMonk`.

Use it to manage **action state and decisions**. Do not use it to classify content. PARA answers "what is this material?" TangMonk answers "what is happening with it now?"

## Folder Model

Create or maintain this structure beside the user's content roots:

```text
00-TangMonk/
  README.md
  Inbox/
    README.md
    Inbox.md
  Exploration/
    README.md
    Exploration.md
  Backlog/
    README.md
    Backlog.md
  Weekly/
    README.md
    Weekly.md
  Today/
    README.md
    Today.md
  _Legacy/
```

Rules live in this `SKILL.md`.
Keep workspace `README.md` files short and local.
Do not hide TangMonk inside `Projects`, `Areas`, or `Resources`.

## Core Principles

- One `Today ONE` at a time.
- New ideas do not interrupt the current path by default.
- Tasks must be executable and verifiable.
- Distinguish storage from action. A document can stay in PARA while its action state lives in TangMonk.
- Prefer explicit choice over silent accumulation.
- The model can advise and remind, but it must not pretend to make the user's life decisions for them.

## How To Work

When helping the user:

1. Decide whether the item is:
   - raw idea,
   - decision to be made,
   - executable task,
   - weekly responsibility,
   - today's single push,
   - or just reference material.
2. Update the TangMonk state files.
3. Keep content in its normal home unless the user explicitly wants to move it.
4. If a local README and this skill disagree, follow this skill and shorten the local README later.

## Inbox

`Inbox` is for raw ideas that have not been judged yet.

Rules:

- One line per idea.
- Record the intake date.
- Do not add progress, status, score, or decomposition here.
- Remove the line once it has been routed elsewhere.

Use `Inbox` for:

- interruptions,
- future possibilities,
- undeveloped ideas,
- things that are too vague to execute.

Do not use `Inbox` as a progress tracker or a storage folder.

## Routing From Inbox

### Inbox -> Exploration

Route to `Exploration` when all are true:

- the user has not decided whether to commit,
- the cost is non-trivial,
- the payoff is uncertain,
- starting too early could absorb long-term attention,
- a timeboxed decision can be made quickly.

Typical cases:

- "Should I invest in this direction?"
- "Is this worth learning now?"
- "Should this become a real project?"
- "Should I adopt this tool, system, or workflow?"

### Inbox -> Backlog

Route to `Backlog` when all are true:

- the user has already decided to do it,
- the output is clear,
- done can be judged,
- it is not just open-ended learning or vague research,
- the scope is bounded enough to execute.

Default heuristics:

- target `<= 14 days`,
- target `<= 3` meaningful execution steps,
- if it breaks those defaults, split it or send it through `Exploration` first.

### Inbox -> Weekly or Today

Do not route `Inbox` directly to `Weekly` or `Today`.

- `Weekly` must come from `Backlog` or a deliberately named `Exploration`.
- `Today` must come from `Weekly`.

### Inbox -> Reference Material

If something is only useful for lookup, keep it in the user's content system, not in TangMonk.

TangMonk tracks what the user is deciding or doing, not what they are storing.

## Exploration

`Exploration` is not execution. It is a timeboxed decision process.

Defaults:

- one decision question per exploration item,
- one clear timebox, usually `<= 2 hours`,
- one output: `Continue`, `Pause`, or `Abandon`.

Allow:

- quick research,
- quick comparison,
- quick synthesis.

Do not allow:

- deep implementation,
- full environment setup,
- open-ended learning,
- "just doing a little bit" of the real project.

Every exploration must end with:

- `Continue`: close the exploration and create an executable `Backlog` item.
- `Pause`: close the exploration and return the idea to `Inbox` or keep only the useful reference material.
- `Abandon`: close the exploration and treat the path as rejected unless something materially changes.

Keep concurrent explorations low. Default max is `1` active exploration unless the user explicitly wants more.

## Backlog

`Backlog` is a candidate pool for real work, not a parking lot.

Each item should say:

- title,
- output,
- done rule.

Reject or rewrite items that are really:

- vague intentions,
- passive learning,
- pure collection,
- hidden exploration.

If a backlog item expands beyond a reasonable bound, split it or send it back through `Exploration`.

## Weekly

`Weekly` is a responsibility declaration for the current week.

Rules:

- maximum `3` items,
- no day-by-day scheduling here,
- every item should matter if missed,
- every item should be concrete enough to advance this week.

`Weekly` can contain:

- executable `Backlog` items,
- a named `Exploration` that must conclude this week,
- a multi-day push with a clear weekly result.

At each weekly reset:

1. close or clear the previous week,
2. choose up to `3` items,
3. ignore the rest for that week.

## Today

`Today` contains exactly one `Today ONE`.

`Today ONE` means:

- the highest-cost-to-miss push for the day,
- not the only thing the user can do,
- the one thing that carries completion responsibility.

Prefer this structure:

```md
## Today ONE · YYYY-MM-DD
- [ ] Title
  - Scope:
  - Goal:
  - Constraints:
  - Timebox:
```

Defaults:

- choose it from `Weekly`,
- use a clear timebox, often `60-240 minutes`,
- close it the same day as done, moved, or canceled.

After it is finished:

- do not silently create a second `Today ONE`,
- let the rest of the day be secondary work, admin, or rest.

## Interruption Rule

A new idea may bypass the normal queue only when all of these are true:

- it has repeated enough to be obviously costly to ignore,
- a useful MVP fits in a short timebox,
- it does not require major learning or research,
- it does not break the current `Today ONE`.

Otherwise capture it in `Inbox`.

## Relationship To PARA

- PARA answers "what is this material?"
- TangMonk answers "what is the current execution state?"
- Keep those dimensions separate.
- Do not store TangMonk state inside `Projects`, `Areas`, `Resources`, or `Archives`.
- Prefer links, references, or content paths over moving files just to match task state.

Finished or abandoned work should leave TangMonk and follow the user's normal archive rules.

## Local Workspace Rules

When operating a TangMonk workspace:

- keep the active state in `Inbox.md`, `Exploration.md`, `Backlog.md`, `Weekly.md`, and `Today.md`,
- keep local `README.md` files short: one sentence of purpose plus a pointer back to this skill,
- avoid duplicating the full rule set in workspace files,
- treat `_Legacy` as historical material, not as the active rule source.

## Communication Style

TangMonk can be firm and a little nagging, but it should still be clear.

- Separate observations from decisions.
- Call out ambiguity, queue bloat, fake tasks, and hidden exploration.
- Prefer a small next action over motivational language.
