---
name: writing-master
description: Write, continue, review, proofread, condense, or analyze prose using reusable named writing-style profiles. Use when the user invokes writing-master, names a style such as "bbs" or "research-analysis", asks for a natural Chinese forum post, wants notes turned into an article, asks to match their established voice, provides an article for language or style review, wants a deep-research or analytical article with direct evidence-backed conclusions, asks to simplify a verbose analysis, or wants a new writing style added to this skill.
---

# Writing Master

Use named style profiles to produce prose that matches the user's intended voice instead of default assistant prose.

## Workflow

1. Determine whether the user wants discussion, an outline, a new draft, a continuation, review of an existing text, style analysis, or a new style profile.
2. Select the requested style profile and read it completely before writing:
   - `bbs` → `references/bbs.md`
   - `research-analysis` → `references/research-analysis.md`
3. Preserve the user's actual opinions, experiences, examples, uncertainty, and degree of conviction. Do not manufacture personal history or stronger claims.
4. Match the requested output stage:
   - For discussion, exchange views without prematurely drafting the article.
   - For an outline, keep it skeletal rather than turning it into finished prose.
   - For a draft, return usable copy instead of explaining the writing process.
   - For a supplied article or original text, review it without directly modifying it.
5. Check basic language correctness regardless of the selected style.
6. Apply the selected profile and then perform its self-check.
7. Keep the response compact unless the user explicitly wants alternatives or commentary.

## Style Routing

- Use `bbs` for Chinese forum posts, personal experience posts, project retrospectives written for peers, or requests for a conversational and approachable forum voice.
- Use `research-analysis` for deep-research reports, company or investment analysis, evidence-based comparisons, product or policy analysis, and requests to make an analytical article shorter, more decisive, or less defensive.
- Do not infer `bbs` merely because the text is in Chinese. Use it when the venue, genre, or requested voice matches.
- If the user explicitly names another profile, look for `references/<profile>.md`. If it does not exist, say so and offer to create it.

## Editing Boundaries

- Treat the user's draft as the source of truth for both substance and voice.
- Keep technical terms when they are natural to the audience. Explain only what the intended readers are unlikely to know.
- Do not turn prose into headings, taxonomies, numbered arguments, or a tutorial unless the user asks for that structure.
- Do not add citations, research, examples, conclusions, or calls to action unless requested or needed to support a newly introduced factual claim.

## Universal Language Check

Apply this check to every writing style:

- Check grammar, typos, missing or duplicated characters, punctuation, word choice, collocations, and incorrect idiom or set-phrase usage.
- Distinguish genuine errors from deliberate colloquial wording, rhythm, repetition, punctuation, dialect, or stylistic fragments.
- Produce clean language in newly drafted text without flattening the selected voice.
- Do not silently preserve an error merely because the requested style is informal.

## Supplied Article Boundary

When the user provides an attached article, pasted article, or other original text for review:

- Do not edit the source file.
- Do not return a fully revised version that silently incorporates changes.
- Report correction points and suggestions in the conversation only.
- For each necessary correction, quote or locate the original wording, identify the problem, and give a suggested replacement.
- Separate objective language errors from optional style suggestions when both are present.
- Keep the list focused; do not use proofreading as a reason to rewrite the author's voice.
- A new article may be drafted separately from notes or an outline when explicitly requested, but it must not be presented as a direct modification of the supplied original.
- If the user explicitly asks to revise or replace a named local file, treat that as direct authorization to edit it while preserving facts, sources, and the user's substantive position.

## Adding a Writing Style

When the user asks to implement another writing style:

1. Create `references/<style-name>.md`.
2. Define its purpose, voice, typical flow, sentence and paragraph habits, preferred moves, anti-patterns, editing rules, and self-check.
3. Include a few short phrasing patterns only when the user has supplied representative writing.
4. Add one routing bullet to this file.
5. Keep shared rules here and style-specific rules in the reference file.
6. Validate the skill after substantial changes.
