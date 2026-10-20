# Save confirmed design decisions

Find the project's existing design documents and any page-specific rules. Use their actual paths and hierarchy; do not assume that every project stores rules in the same flat folder. Show references relative to the document that will contain them and check they resolve.

Prepare the proposed content from confirmed decisions, not raw search output. Compare it with existing rules. Retain user edits and meaningful project choices. Distinguish global conventions from page-specific exceptions.

The helper previews a new document or shows a diff against the exact selected target:

```bash
python3 scripts/save_rules.py --input proposed.md --target <selected-file>
```

When creating a new file within the authorized scope:

```bash
python3 scripts/save_rules.py --input proposed.md --target <selected-file> --apply
```

The helper creates a missing file exclusively. If the target already exists, it displays the difference and refuses to replace it, preserving its bytes. To update an existing file, use the diff to prepare a focused merge with normal file-editing tools, within the user's existing authorization. Preserve unrelated rules and review the final difference. Do not treat a refusal as a reason to bypass the intended preservation.

Keep runtime settings and personal filesystem locations out of public source. Return the actual saved file and describe which decisions changed. Creating documentation does not imply that a page has been implemented or visually checked.
