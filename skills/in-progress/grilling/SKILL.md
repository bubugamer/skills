---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Present concise questions with clearly stated options and a recommendation. Keep independent questions in small rounds that the user can answer comfortably.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a question needs a fact from the environment, inspect it with the available tools yourself. Delegate only when the current user or applicable instructions authorize delegation. An unresolved factual dependency delays only the decisions that depend on it; other independent decisions can be addressed now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. For consequential unresolved decisions, wait for the answer before dependent work. Existing authorization remains valid; do not request the same permission again. End with settled decisions, open dependencies and observable completion criteria.

## Codex collection adaptation

This is a manually selected trial. Current user instructions, workspace rules and tool permissions take precedence. Use the language of the conversation. Tool names and agent invocation mechanisms are resolved from the current environment, not invented from another host. Perform authorized work without repeating settled approval questions.
