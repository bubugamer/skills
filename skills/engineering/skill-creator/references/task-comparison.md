# Real task comparisons

Choose concrete tasks representing the skill's intended use, edge cases, and likely confusion with neighboring abilities. Derive success criteria from the user outcome, not from whether an output repeats the skill's wording.

Define a candidate and a baseline. A revised skill can use its previous version; a new skill can use an otherwise equivalent run without that skill. Keep inputs, allowed tools, environment, and evaluation criteria comparable. Store each run in a separate workspace, retaining its exact skill version and outputs.

Perform independent runs only when available and authorized. If only a sequential self-check is possible, label it accordingly and avoid presenting its outcome as a controlled benchmark. Define an execution limit and stopping condition proportionate to the actual work; do not run a fixed large matrix for every small edit.

Judge observable requirements with the output or execution evidence that establishes them. Use code checks for deterministic properties and human review for subjective quality. Report malformed outputs, failures, and timeouts separately. Do not assign invented zero cost or an automatic failure grade to missing measurements.

Use the task record format in [result-records.md](result-records.md). The summarizer reports valid samples and failed executions, and compares only matching successful case/run pairs with equivalent criteria. Unmatched or invalid pairs remain visible. A small sample or subjective grading cannot establish a universal improvement.

Generate the local review page when it helps the user compare real outputs. The page escapes output text and uses no remote assets; feedback stays on the page until the user chooses how to save it. Incorporate concrete feedback into the next focused revision.
