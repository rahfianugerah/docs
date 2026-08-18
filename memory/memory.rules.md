> Up: [[README.md]] · [[memory/README.md]]

# Memory Protocol

## Core Requirement

This is the protocol every model follows when reading or writing the memory in [[memory/README.md]].

**One note holds one thing.** A note that holds three facts cannot be corrected, superseded, or linked to precisely, and it will rot as one unit.

## What to Write

Write a note when something is **true beyond this session** and **not recoverable from the code**.

| Write it | Do not write it |
| :- | :- |
| A preference the user stated | Anything the code already says |
| A constraint that shaped a decision | What a function does |
| Why an approach was rejected | A restatement of git history |
| An experiment's finding, including a failure | A running summary of the conversation |
| A fact about the environment or the data | Something that will be false next week |
| A pointer to an external resource | A secret, a key, or a credential |

The test: **would the next session waste time without this?** If not, do not write it. A memory full of noise is a memory nobody reads.

## Note Shape

Every note uses the frontmatter in [[note.template.md]]:

```markdown
---
type: fact | decision | session | reference
created: 2026-02-11
updated: 2026-02-11
tags: [project-x, data]
status: current | superseded
---

# One-line title that states the thing

The fact, the decision, or the event. Short.

**Why:** the reason it is true or was chosen.
**Applies to:** where this is relevant.

Related: [[other-note.md]]
```

Rules:

1. **The title states the thing**, not the topic. "Loader uses Polars, not pandas" beats "Data loading notes".
2. **The filename is a kebab-case slug of the title**, so a wikilink reads as a sentence.
3. **`created` and `updated` are real dates**, written absolutely. Never "last week"; a relative date in a durable note is meaningless the moment it is read.
4. **Frontmatter is required.** Cognee reads it, and Obsidian shows it as properties.
5. **Link liberally.** A wikilink whose target does not exist yet is fine; it marks a note worth writing.
6. **Keep it short.** If a note runs past a screen, it holds more than one thing.
7. **At most one callout**, per [[callout.rules.md]], and only for the line that changes what the reader does. A note holds one thing, so only one line in it can be the thing that must not be missed.

## Recall Order

Before answering from general knowledge, check the memory in this order. Stop at the first layer that answers.

1. **The note itself**, if you know its name. Cheapest, exact.
2. **Cognee semantic search**, for "what do I know about X". Handles the case where you do not know the note's name.
3. **Graphify's `graph.json`**, for "where is X handled". Never grep the tree for this; the map is already extracted and costs no tokens to read.
4. **The code**, for anything about how something works today. The code is always more current than a note about the code.

Layer 4 outranks layers 1 to 3 on anything the code can answer. A note describing an implementation is a note that will be wrong eventually.

No layer answers "what was true in March". Git history does.

## Trust and Staleness

**A recalled note is what was true when it was written, not what is true now.**

- Verify anything a note claims about a file, a function, a path, or a flag before acting on it. Files move.
- A note that turns out to be wrong is corrected or marked `status: superseded`, not left alone. A wrong memory is worse than no memory, because it is trusted.
- When a note is superseded, link the new note from the old one, and set `status: superseded`. Do not delete it; the fact that something changed is itself worth knowing, and a reader who finds the old note needs the pointer to the new one.
- Delete a note only when it was never true.

## Never Store

> [!danger]
> A note carrying a secret is a secret published to a git repository and to every model that reads the memory. Rotate anything that reaches one, per [[secret.rules.md]].

- **A secret, a key, a token, a password, or a connection string.** The memory is a git repository and it is read by every model. See [[secret.rules.md]].
- Personal data about a third party.
- A real value from any environment or configuration file, per [[env.rules.md]].
- A large paste: a full file, a full dataset sample, a full traceback. Write the finding and link the source.
- Anything that is a to-do. A memory is what is known, not what is planned; a plan belongs in an issue.

## Writing from an Agent

- Write the note as a file in this folder, then run `pmb digest`. Do not write to Cognee directly; it is an index and a direct write is lost on the next rebuild.
- A note the graph proposed is not a memory until a human keeps it. It lands in `graph/kg/`, which `pmb reset` deletes and `pmb digest` overwrites. To keep one, move it here yourself and write the `**Why:**` line: a kept note with no reason written down is a machine's guess with a date on it.
- Digest after a batch of writes, not after each one.
- One note per commit is unnecessary; a session's notes commit together, per [[commit.rules.md]].
- Never rewrite a note you did not write without saying so in `updated`.

## Definition of Done

- The note holds one thing, and its title states that thing.
- Frontmatter is present, with absolute dates and a real type.
- The reason is written down, not just the conclusion.
- It links to at least one related note where one exists.
- It contains no secret, no personal data, and no real configuration value.
- It says something the code and git history do not already say.

## Related

- [[memory/README.md]]
- [[note.template.md]]
- [[secret.rules.md]]
- [[env.rules.md]]
- [[docs.rules.md]]
- [[callout.rules.md]]
