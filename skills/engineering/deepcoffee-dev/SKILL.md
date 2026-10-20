---
name: deepcoffee-dev
description: Operate the DeepCoffee development and knowledge workflow, including direct-main or PR delivery, deployment, routine maintenance, test-account resets, and reviewing or adding knowledge articles. Use when the user selects deepcoffee-dev for these DeepCoffee tasks. Its accumulated operating rules live in this skill; resolve local scripts and runtime settings from the current context.
---

# DeepCoffee Development

Keep the operating rules learned through DeepCoffee work in this skill and its references. Use the current user request, applicable project instructions, and actual tool permissions when applying them. Preserve existing user choices and authorization; ask only for decisions that are still missing.

## Resolve the operation

Confirm the selected DeepCoffee workspace and requested outcome. Read [runtime.md](references/runtime.md) when an operation needs a script, backend environment, or deployment binding. Read [operating-rules.md](references/operating-rules.md) for the shared maintenance, verification, and versioning policy.

Before an actual DeepCoffee operation, run the shared maintenance check once. Follow the user's existing routine-maintenance authorization for pending work; current request restrictions still apply. A maintenance-check failure does not block the requested operation. Reading or editing this skill is not a DeepCoffee operation.

## Choose the matching workflow

Read only the references needed for the task:

| Intent | Reference |
| --- | --- |
| Choose direct-main versus PR delivery, or ship a change | [delivery.md](references/delivery.md) |
| Deploy frontend or backend changes and hand off acceptance | [deployment.md](references/deployment.md) |
| Check or apply routine maintenance, or reset a test account | [maintenance.md](references/maintenance.md) |
| Review knowledge materials or rewrite an article into the knowledge base | [knowledge.md](references/knowledge.md) |

Use the requested workflow within its confirmed scope. Keep its rules here as they evolve; local paths, credentials, service targets, and environment values remain in the user's runtime configuration.

## Verify and report

Run the checks relevant to the change and the project's CI. Distinguish submitted code, passed checks, triggered deployment, and user-confirmed online acceptance. Follow the established division of verification: online status and production rendering are checked by the user.

Report the actual completed actions, relevant file or commit references, failures, and the pages or flows the user should accept. For maintenance, report the actual counts and failed items. For knowledge work, list the user-facing pages, model notes, source-display mode, and checks performed. Reply in the conversation's language.
