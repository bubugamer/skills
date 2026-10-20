# Creating and maintaining a skill

Start from an observed task or repeated workflow. Use the conversation, existing outputs, and user feedback to identify what the user wants, what input starts the work, and what a completed result looks like. Ask only for missing information that materially changes the design; continue independent work with the available context.

Inspect existing skills before adding an entry. Improve an existing skill when the purpose is already covered. Preserve the user's chosen boundary and name; a helper script or an evaluation step does not need its own skill. When creation and evaluation serve the same workflow, they can share an entry and use separate references.

## Write the entry and supporting resources

Use a short, stable name and a description that states the purpose and recognizable usage situations. Include realistic near misses when they clarify a confusing boundary, rather than accumulating keywords. Preserve existing manual or automatic invocation settings unless changing them is part of the request.

Keep SKILL.md focused on decisions and the core procedure. Put detailed methods in linked references, repeatable deterministic work in scripts, and reusable output structures in templates when needed. Every supporting resource should have a clear route from the entry or another linked reference. Avoid copying general knowledge or inventing a folder for every possible future need.

Keep source lineage, personal workspace settings, and runtime artifacts separate. A public skill can contain reusable personal preferences, but environment paths, credentials, login state, and live results belong in the user's configuration or selected workspace. Attribute adapted methods and respect upstream terms. Follow the target repository's catalog, provenance, documentation, and publication rules rather than introducing a parallel packaging process.

## Verify the requested change

Choose representative success cases, edge cases, and plausible tasks that should use a neighboring capability. Define expectations in terms of the user's outcome. Scenario definitions describe intended behavior; they are not evidence that a model has already performed it.

Run available structural checks and relevant script tests. If actual task behavior or trigger selection needs evaluation, use the corresponding reference from SKILL.md. Use a previous version as a baseline when helpful. A small wording change does not automatically require a large model benchmark, and a file check cannot establish better model performance.

Inspect the result, fix problems, and repeat affected checks. Explain what changed, what ran, what happened, and any material limits. Preserve user edits and unrelated content. Install or publish only within the current request and existing authorization; writing a skill does not itself authorize replacing an installation or launching additional agents.
