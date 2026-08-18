> Up: [[README.md]]

# Documentation Standard

## Core Requirement

Documentation is written for the person who arrives with no context, which is usually you in six months.

Everything is written in **English**: every document, every heading, every comment, every commit, every identifier.

Every document starts from a template in `template/` and keeps the template's section order, so any two projects are comparable. They are [[project.template.md]], [[api.template.md]] and [[model.template.md]].

## What Every Project Documents

Four files, and no more unless something genuinely needs one.

| File | Holds |
| :- | :- |
| `README.md` | What it is, how to run it, what it needs. The only file most readers open |
| `API.md` | The endpoints, if the project has any |
| `MODEL.md` | The model card, if the project trains one |
| `.env.example` | Every variable name with a placeholder, per [[env.rules.md]] |

A project that needs a fifth document usually needs a shorter README instead.

## The README Is the Contract

A reader must be able to go from a clone to a running project using only the README. If they cannot, the README is incomplete regardless of how much it contains.

Required, in this order:

1. Title, then the badge row per [[badge.rules.md]].
2. One paragraph: what this is and what it is for.
3. Setup: the exact commands, copy and paste, including the environment activation.
4. Usage: the smallest example that does something real.
5. Configuration: the variable names, never a real value.
6. Project structure, if the layout is not obvious.

Write the setup commands as a block that can be pasted whole. Do not describe the steps in prose and leave the reader to assemble them.

## Writing

- **Short sentences.** One idea per sentence.
- **Active voice.** "The loader reads the file", not "the file is read by the loader".
- **Say what it does, then why.** The why is the part nobody can reconstruct.
- **No filler.** Delete "basically", "simply", "just", "in order to", "it should be noted that". "Simply" is a lie whenever the thing is not simple.
- **Concrete over abstract.** Name the file, the function, the value.
- **Write the failure.** The command that fails and what the error looks like is worth more than three paragraphs of happy path.
- **If the explanation is longer than the code, delete the explanation** and make the code clearer instead.

## Formatting

- ATX headings (`#`), sentence-case or title-case consistently within a file.
- Fenced code blocks with a language tag.
- Tables for anything with two or more parallel attributes.
- A bullet list for items, a numbered list only for genuine ordered steps.
- One blank line between blocks. No trailing whitespace.
- A path, a filename, a variable, a command, and a value all wear backticks.

Do not use:

- Emoji
- An em dash, a left arrow, or a right arrow; use `-`, `<`, and `>`
- Smart quotation marks
- A horizontal rule (`---`) as a section divider; the heading already divides
- ALL CAPS for emphasis
- A wall of bold text; if everything is bold, nothing is

## Obsidian

This documentation set is an Obsidian vault, and so is the memory brain in [[memory/README.md]]. Two conventions keep the graph usable.

**Wikilinks with the extension:** `[[commit.rules.md]]`, not the bare `commit` form without the extension. The extension form survives being read outside Obsidian, where a bare link means nothing.

**Callouts** mark the one thing on a page a reader must not miss, and every type comes from [[callout.rules.md]]. A destructive instruction carries a `danger` callout, and every rules document carries at least one `warning` on the way people actually get it wrong.

> [!warning]
> A callout is Obsidian syntax, so it renders as a plain blockquote everywhere else and is digested into the memory index verbatim. Three per document is the ceiling, because a page of callouts has no emphasis left.

**Fixed placement, so re-runs are deterministic:**

| Block | Where | Contains |
| :- | :- | :- |
| Breadcrumb | The very first line | `> Up: [[README.md]]` |
| `## Index` | `README.md` only | Every document, grouped |
| `## Applies To` | A rules document, at the end | What it governs |
| `## Related` | Any other document, at the end | Lateral links |

Update a block in place. Never append a second one.

## Keeping It True

**A stale document is worse than no document**, because it is believed.

- Update the document in the same commit that makes it wrong. A README fixed "later" is a README that stays wrong.
- Delete a section describing something that no longer exists.
- A code example in a document is code: if it stops working, it is a bug.
- When the document and the code disagree, the code is right and the document gets fixed. Never the reverse.

## Machine Learning Documents

An ML project has one documentation failure the rest do not: a result nobody can reproduce.

A `MODEL.md` records, at minimum:

- What the model does, and what it must not be used for.
- The data: source, version, size, and how it was split.
- The training setup: parameters, seed, hardware, runtime.
- The metrics, with the baseline they are compared against.
- The known failure modes, and what the model is bad at.

The last one is the one everybody skips and the only one that prevents the model being misused.

An experiment's result belongs in the pull request that carried it, per [[pr.rules.md]], and its durable finding belongs in [[memory/README.md]]. A number in a notebook cell is not a record.

## Definition of Done

- Written in English, from the right template, with the template's section order.
- The README takes a reader from clone to running with no other source.
- The badge row follows [[badge.rules.md]] and every version is current.
- No real value from any environment or configuration file appears anywhere.
- No emoji, no prohibited character, no decorative divider.
- Every wikilink resolves.
- Nothing in the document contradicts the code.

## Applies To

- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]
- [[badge.rules.md]]
- [[codes.rules.md]]
- [[env.rules.md]]
