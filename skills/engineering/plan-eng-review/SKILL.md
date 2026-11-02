---
name: plan-eng-review
description: Review an engineering plan against the existing codebase before implementation. Check architecture, affected callers, scope, tests, failure paths, and performance using gstack's plan-eng-review workflow.
---

# Engineering Plan Review

Use gstack's pinned Codex rendering for the review. The upstream workflow and its shared tools live in an external runtime; this entry connects them to the personal collection.

## Load the upstream workflow

Resolve this folder from the loaded SKILL.md. Run `python3 scripts/runtime.py check` from this folder, or use the absolute script path while keeping the target repository as the working directory. Read the returned `entrypoint` and `preamble` in full, in chunks when needed. They retain the upstream English review procedure, including the code-grounded scope challenge and four engineering review sections.

If the runtime check fails, read [runtime.md](references/runtime.md), report the exact missing dependency, and repair it only within the current installation authorization.

## Use it in the current task

Apply the upstream review to the user-selected plan, repository, and revision. Trace proposed changes against existing implementations, interfaces, callers, and tests. Keep evidence of current behavior distinct from assumptions about future code. Include the affected scope and omitted dependencies in the report.

Run upstream shell blocks through `python3 scripts/runtime.py shell`, passing the original block on standard input and keeping the target repository as the working directory. The launcher supplies the pinned Bun runtime and isolated gstack state for every new shell. Relative upstream document links resolve from the returned upstream entrypoint directory. Read-only helper commands and existing bounded checks provide installation or code evidence; a review does not itself authorize implementing its findings.

Current user instructions, project rules, host tools, and existing authorizations govern execution. Use available host question and web tools in place of unavailable upstream tool names. Extra agents and outside-model reviews require existing authorization; record unavailable or unauthorized coverage accurately. Follow the current task's decision and approval rules rather than adding repeated upstream approval gates for already authorized work.

This installation selects one review entry. Framework onboarding, telemetry enrollment, self-upgrades, automatic skill chaining, and cross-project learning are outside this entry's task. Use the configured local state; additional skills remain separately selectable and require their own admission.

Finish with the review's evidence, affected scope, open decisions, and conclusion. Distinguish installed tools and defined scenarios from a completed review of a real plan.

Reply in Chinese.
