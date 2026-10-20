# Optional evidence records

Use persistent records when the user has requested a research bundle or agreed to preserve a long investigation. Resolve the location from that scope; ordinary conversational research does not create a record directory by default.

A useful record links a source to an exact excerpt and its location. Keep source facts separate from your interpretation. Store only relevant excerpts within applicable quotation limits, rather than copying whole articles.

## Recording helper

The optional Python 3 helper records JSON objects in a selected JSONL file. Resolve its path relative to the skill folder:

```bash
python3 scripts/records.py add --ledger research/evidence.jsonl --record source.json
python3 scripts/records.py add --ledger research/evidence.jsonl --record excerpt.json
python3 scripts/records.py check --ledger research/evidence.jsonl
```

The two input JSON files contain these fields:

```json
{"kind":"source","title":"Original specification","location":"https://example.org/specification","retrieved_at":"2026-10-20"}
```

```json
{"kind":"evidence","source_id":"ID returned when adding the source","quote":"An exact, limited passage from the source.","locator":"Section 3, paragraph 2","note":"What needs to be checked before using this passage."}
```

A source location can instead identify a local material file. Give each excerpt a stable location, such as a page, section, table, or timestamp. The optional note is an interpretation or review reminder, not an evidence quote.

The helper assigns stable IDs, preserves existing entries, avoids recording the same identity twice, and checks required fields and source links. A repeated source location retains its first metadata; use a distinct version location for changed source material. Use one writer at a time. It performs no fetching, semantic verification, scoring, or claim approval. Passing `check` means only that the records have a valid structure and links.

## Claims and continuation

For a substantial investigation, keep a short review note beside the records with:

- the research question, scope, and material assumptions;
- each key claim, its source or excerpt IDs, and whether it is a fact, inference, or recommendation;
- supporting and contrary passages, interpretation limits, and checks still needed;
- findings already delivered and the next useful investigation step.

These can be ordinary Markdown notes; a separate claim database is unnecessary unless the task benefits from it. On resuming, read the question, evidence, open issues, and completed work before continuing. Creating records does not authorize additional agents or continued work beyond the user's scope.
