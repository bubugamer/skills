# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation in Codex

Both choices keep `name` and `description` in SKILL.md. The description remains the concise pointer to the skill's purpose; invocation policy belongs in `agents/openai.yaml`.

- A **model-invoked** skill allows automatic selection as well as explicit user invocation. Set `policy.allow_implicit_invocation: true`, or retain the default when no policy is present. Write a description that states the useful trigger branches.
- A **user-invoked** skill is chosen explicitly by the user. Keep the required description, and set `policy.allow_implicit_invocation: false`. The user can select it with `$skill-name`; a router can recommend that choice without running it.

Preserve an existing skill's invocation policy unless the user asks to change it. Put shared reference behind a normal file pointer when several skills need the same material; a reference file does not require a separate skill entry.

These are this collection's Codex mappings. Upstream `disable-model-invocation` is represented by the policy file rather than copied into SKILL.md. Naming, discovery and invocation conventions follow the current Codex environment; an upstream explanation does not grant extra tool or execution authority.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human has one skill to remember instead of many. In this collection, the router recommends a suitable entry and how to invoke it; recommending does not install or run the target skill.
