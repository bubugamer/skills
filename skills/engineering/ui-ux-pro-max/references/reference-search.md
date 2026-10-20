# External references and search

The upstream reference data and search engine remain maintained by [NextLevelBuilder](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill). This skill does not bundle that library or claim to be its upstream distribution.

## Runtime selection

Use a trusted, already available upstream runtime containing `scripts/core.py` and `data/`. Pass its location explicitly with `--runtime`, or use the user's `UI_UX_PRO_MAX_RUNTIME` setting. A full upstream checkout can use its `src/ui-ux-pro-max` directory. Keep that runtime separate from this adapter when consolidating installations; this adapter's own folder is not the external data library.

Do not automatically install or upgrade an external package to answer a design question. If it is unavailable, explain the missing reference search and continue with the project and known design requirements where useful.

Resolve the following helper path from this SKILL.md folder. It calls the external core search functions against a temporary, validated table, without modifying the source runtime:

```bash
python3 scripts/search_references.py --runtime <selected-runtime> --list
python3 scripts/search_references.py "keyboard focus error feedback" --domain ux --runtime <selected-runtime>
python3 scripts/search_references.py "table selection state" --stack react --runtime <selected-runtime>
```

Search by the actual need: style, color, typography, chart, product, landing, icons, UX, or the selected platform. `--list` reports what the selected runtime actually provides. Stack files are discovered from its data directory, so an existing React or Vue table is not hidden merely because an old CLI hardcodes React Native.

English queries generally match the English library better. Translate the design intent into suitable search terms, then explain the result in Chinese.

## Data quality and interpretation

The adapter rejects invalid headers and skips records with mismatched fields, null bytes, or embedded CSV rows. It reports skipped records and the remaining coverage. Excluding a malformed record does not reconstruct entries that were swallowed into it. If a needed table has no usable data or incompatible fields, report the limit and choose another actual source rather than inventing guidance.

Search ranking is a way to find references, not a quality score for the proposed interface. A successful search does not validate a website, accessibility compliance, or user experience. Review suggestions against the page's task and constraints.

Use existing project rules before generating new ones. Do not call the old tool's `--persist` path: the reviewed version overwrites existing files and uses inconsistent navigation paths. Save confirmed decisions using [design-records.md](design-records.md).
