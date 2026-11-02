# Upstream runtime

The personal entry loads the full upstream Codex rendering. It does not replace gstack's engineering review with a shorter checklist. The selected rendering includes the architecture, code quality, test and performance sections, scope challenge, evidence rules, and review outputs.

## Installation binding

The default private binding is `~/.codex/skill-runtimes/plan-eng-review.json`. It contains three absolute paths on the user's machine:

```json
{
  "runtime_root": "<absolute path to the pinned gstack checkout>",
  "state_root": "<absolute path to separate mutable gstack state>",
  "bun_path": "<absolute path to the pinned Bun executable>"
}
```

Keep this binding, mutable state, generated host files, and binaries outside the public collection. Existing gstack installations and global Bun remain independently managed. A missing binding is an incomplete runtime installation, not permission to install the entire gstack skill set.

The approved revision, Bun version, required files, and generated document fingerprints are in [runtime-spec.json](runtime-spec.json). Use the system skill-installer to retrieve the selected upstream package at that revision for comparison. A full pinned upstream checkout supplies its shared scripts and libraries, including their licenses. Run its own generator, without registering its whole collection:

```text
<pinned-bun> --no-env-file --config=/dev/null run scripts/gen-skill-docs.ts \
  --host codex --out-dir codex-render --install-root <absolute-runtime-root>
```

Run from the pinned checkout. Retain the upstream model-neutral `gpt` rendering profile. The selected entry is under `codex-render/.agents/skills/gstack-plan-eng-review/`; keep its `sections/preamble.md` beside it. Other generated entries are runtime data, outside every skill discovery root. Register only the approved personal entry with this collection's installer.

Check the binding with `python3 scripts/runtime.py check`. It verifies the revision, document fingerprints, required helper files, and exact Bun version. It does not execute a plan, start an agent, or contact an outside model.

## Shell environment

Each upstream shell block runs through the launcher's `shell` command. Pass the block through standard input using the current host's execution tool. Keep the target repository as the working directory. The launcher sets runtime and state paths and prepends the private Bun directory for this child process; it leaves the user's shell profile and Codex settings unchanged.

The installation uses separate local state with telemetry off, update checks and automatic upgrades off, outside-model reviews disabled, automatic skill suggestions off, and cross-project learning off. These are installation defaults, not a record of user consent to any external action. The wrapper omits framework onboarding rather than pretending those questions were answered. Change these settings only for a later explicit request.

Git, Python 3, Bash, and the pinned Bun are required. Current host web tools can provide source research. A missing optional browser or outside reviewer must be reported as unavailable; it does not justify installing or invoking other skills.

## Verification limits

Passing the runtime check establishes that the selected documents and basic tools are available. Scenario definitions and helper checks do not prove that a real plan review is correct. A review still needs a plan, its target repository/revision, and evidence from that repository. Upstream labels its Codex host experimental.
