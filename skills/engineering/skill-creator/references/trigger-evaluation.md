# Description probes and revision

A trigger probe tests whether the skill description leads to reading a temporary marker skill. It does not execute the real skill body and cannot measure task quality.

Use realistic positive cases and plausible near misses. Preserve the user's task distribution instead of filling a fixed quota. Give each query one expected trigger decision; duplicate query texts are rejected to prevent conflicting or merged results.

The optional helper requires Python 3, PyYAML, and a working Codex CLI only for live probes. It stages a temporary project skill in `.agents/skills`, invokes the CLI with read-only access, and uses the user's configured model unless an explicit model is supplied. Existing user configuration and global skills may still influence selection; do not describe this as complete environment isolation.

Resolve script paths from this skill folder. Preview the planned number of calls first:

```bash
python3 scripts/trigger_eval.py --skill-path <selected-skill> --cases cases.json --runs 2
```

Only when live probes are in the authorized scope:

```bash
python3 scripts/trigger_eval.py --skill-path <selected-skill> --cases cases.json --runs 2 --execute --output <new-results-file>
```

The cases file is an array of objects containing `query` and a Boolean `should_trigger`. Each run records a valid triggered/not-triggered response, an execution error, or a timeout. Rates use valid responses only; any failed repetition makes that case incomplete with `pass: null`. An empty final response is an execution error, not a valid non-trigger.

To revise a description, inspect failures from a development set and generalize the intent boundary. Avoid adding every failed phrase as a keyword. Compare the candidate and previous description on the same cases and budget. Reserve a separate final set when useful; do not repeatedly select wording against that final set and call it unseen evidence.

Suggest the revised description with its rationale, probe coverage, and errors. Apply it only within the user's requested scope. Recheck real task behavior when the revised boundary affects which tasks will load the skill.

Official context: [Codex skills](https://developers.openai.com/codex/skills/). Discovery conventions can change; a completed file/CLI check is not a measured live trigger rate.
