> Up: [[README.md]]

# Callout Standard

## Core Requirement

A callout marks the one thing on a page a reader must not miss. Every rules document, component document, and memory note uses the types below, and no other.

> [!warning]
> A callout is Obsidian syntax. Outside Obsidian it renders as a plain blockquote whose first line reads `[!warning]`, and its text is digested into the memory index exactly as written. Use it where the emphasis earns that cost, and nowhere else.

## The Types

Use the first name in each row. The aliases exist in Obsidian and are recognised, but one name per meaning keeps the vault searchable.

| Type | Color | Use for | Aliases |
| :- | :- | :- | :- |
| `note` | Blue | Standard information worth setting apart | |
| `info` | Blue | An informational notice about context or scope | |
| `todo` | Blue | A task item inside a runbook | |
| `tip` | Cyan | Advice that saves the reader time | `hint`, `important` |
| `success` | Green | A completed state or a positive result | `check`, `done` |
| `question` | Yellow | An open inquiry, or a decision not yet made | `help` |
| `warning` | Orange | A cautionary alert: this is where people go wrong | `caution`, `attention` |
| `danger` | Red | A critical issue: data loss, a leaked secret, a broken deploy | `failure`, `fail`, `missing`, `error`, `bug` |
| `example` | Purple | A demonstration of the rule just stated | |
| `quote` | Gray | A quotation from another document or a source | |

## Where a Callout Is Required

These are the cases where the emphasis is not optional, because the cost of missing the line is real.

- **`danger` on anything destructive or irreversible.** A command that deletes data, a step that leaks a credential, an action that cannot be undone.
- **`warning` on the trap in a rule.** Where a document explains the way people actually get this wrong, that sentence is a callout. Every rules document has at least one.
- **`info` on a scope limit.** Where a rule applies only to one platform, one shell, or one environment, say so in a callout rather than in a parenthesis somebody skims past.
- **`example` on a worked demonstration** that follows a rule, where the example is not already a fenced code block. A code block is its own emphasis and needs no wrapper.

## Where a Callout Is Forbidden

> [!danger]
> Never put a secret, a credential, a token, or a real configuration value inside a callout. A callout draws the eye, which is the opposite of what those need, and [[secret.rules.md]] forbids them anywhere in the vault regardless.

- **Never in the frontmatter or above the breadcrumb.** The first line of a document is `> Up:`, per [[docs.rules.md]], and a callout above it breaks the fixed placement every document shares.
- **Never as a section divider.** The heading already divides. A callout used for rhythm is decoration.
- **Never nested.** A callout inside a callout does not render reliably and means the point has two parts, which is two callouts or one paragraph.
- **Never more than three in one document.** A page of callouts has no emphasis left; the reader stops seeing them, which is exactly what happens to a document where everything is bold. This file is the one exception, because a document defining the types has to show them.
- **Never in a memory note body beyond one.** A note holds one thing, per [[memory.rules.md]], so at most one line in it can be the thing that must not be missed.

## Shape

```markdown
> [!warning]
> One line saying what goes wrong, and what to do instead.
```

- **The type is lowercase**, in square brackets with a leading `!`, on its own line.
- **One blank line before and after** the callout, per the block spacing in [[docs.rules.md]].
- **The body is one or two sentences.** A callout that runs to a paragraph is a section, and it gets a heading instead.
- A title is optional and goes on the type line, as `> [!warning] The title`. Use one only when the type alone does not say what the callout is about.
- Do not use the foldable forms `+` and `-`. Content worth a callout is worth showing, and a folded callout is invisible outside Obsidian.
- The body follows every writing rule in [[docs.rules.md]]: one paragraph per line, no em dash, no emoji.

> [!example]
> A rule stating the trap, with the callout carrying the consequence.
>
> ```markdown
> Digest in the container, never on the host.
>
> > [!danger]
> > A killed host run writes host paths into the database that no later run can resolve, and recovering costs a full volume wipe.
> ```

## In a Memory Note

A note may carry **at most one** callout, and only for the line that changes what the reader does.

- Prefer the fixed `**Why:**` and `**Applies to:**` labels from [[memory.rules.md]]. They already carry the reasoning, and a callout does not replace them.
- Use `danger` where the note records something that destroyed data or leaked a value, so the next reader sees it before the detail.
- Use `warning` where the note records a symptom that misled, since that is the part a future session will otherwise repeat.
- Never wrap the whole note in a callout.

## Definition of Done

- Every type used is from the table, written in lowercase with a leading `!`.
- Every destructive or irreversible instruction carries a `danger` callout.
- Every rules document carries at least one `warning` on its most common failure.
- No document carries more than three callouts, and no note more than one.
- No callout is nested, folded, or used as a divider.
- No callout holds a secret or a real configuration value.
- A blank line sits on both sides of every callout.

## Applies To

- [[docs.rules.md]]
- [[memory.rules.md]]
- [[memory/codes.rules.md]]
- [[secret.rules.md]]
- [[uix.component.md]]
