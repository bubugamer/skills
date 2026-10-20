# Results and review

Keep evaluation artifacts in a user-selected workspace, separate from the skill source and existing installations.

## Task records

Write a JSON object with `kind: "task-comparison"` and a `runs` array. Each run has:

- `case_id`, `variant`, and `run_id`: strings identifying comparable trials.
- `status`: `ok`, `error`, or `timeout`.
- `prompt` and `output`: the actual task and output text, when available.
- `expectations`: for a successful execution, a nonempty array with `text`, Boolean `passed`, and `evidence` explaining the judgment.
- Optional `seconds` and `tokens`: actual measurements; omit if unavailable.
- `error`: the actual failure detail for an unsuccessful execution.

```json
{"kind":"task-comparison","runs":[{"case_id":"one","variant":"candidate","run_id":"1","status":"ok","prompt":"The actual task","output":"The actual result","expectations":[{"text":"Required result","passed":true,"evidence":"Observable evidence"}]}]}
```

Summarize with explicit comparison labels:

```bash
python3 scripts/task_results.py --results results.json --candidate candidate --baseline baseline
python3 scripts/review_report.py --results results.json --candidate candidate --baseline baseline --output <new-review-file>
```

The summarizer rejects duplicate run identities, missing judgments, and invented numeric defaults. Execution failures are excluded from quality averages but retained as errors. Deltas use only matching successful pairs with the same criteria, with missing pairs reported. They are not evidence that the skill always improves results.

The review page includes source outputs, judgment evidence, and incomplete executions. Its feedback controls produce a JSON preview for explicit saving; they do not transmit data or modify source files.

## Trigger records

The trigger helper produces `kind: "trigger-probe"`, the cases and per-run status, and summary counts for completed, incomplete, passed, failed, and execution errors. A missing live output is not a negative trigger result. Use:

```bash
python3 scripts/review_report.py --results trigger-results.json --output <new-review-file>
```

Review generation and summary commands make no model calls. They do not package or install skills. The former `skill-creator` packaging tool and embedded `yt-dlp-download.skill` are not included in this skill; repository publishing continues through the collection's normal checks and explicit release list.
