---
tags:
  - kind/rule
  - layer/docs
---

> Up: [[README.md]]

# Callout Standard

## Core Requirement

A callout is a blockquote whose first line names a type, so a reader scanning a page sees the shape of a passage before reading it. Every rules document, component standard, template, and memory note in this vault uses the types below, and no other.

```markdown
> [!warning]
> Deleting the frontmatter stops the note from being parsed.
```

The type is what does the work. It tells the reader whether a passage is a fact to absorb, a trap to avoid, or an example to copy, and it does so before the first word is read. That signal is also what the graph view draws on, so a vault whose notes carry types reads as a structured body of knowledge rather than a wall of undifferentiated prose.

> [!warning]
> A callout is Obsidian syntax. Outside Obsidian it renders as a plain blockquote whose first line reads `[!warning]`, and its text is digested into the memory index exactly as written. Use it where the emphasis earns that cost, and nowhere else.

## The Types

Use the first name in each row. The aliases exist in Obsidian and render identically, but one name per meaning keeps the vault searchable.

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

## Where a Callout Belongs

A callout earns its place when a passage is a different kind of thing from the prose around it. Reach for one when the text is a hard prohibition, a trap that has already cost someone time, a worked example, or a result the reader should verify.

Write it as a normal paragraph when it is simply the next thing to say. A page where most paragraphs are boxed has taught the reader nothing about which passage matters, because the boxes no longer distinguish anything, and the reader who skims past a decorative one will skim past the one that would have saved them.

A useful check: if removing the box would lose nothing but the color, the passage was ordinary prose all along.

## Where a Callout Is Required

These are the cases where the emphasis is not optional, because the cost of missing the line is real.

- **`danger` on anything destructive or irreversible.** A command that deletes data, a step that leaks a credential, an action that cannot be undone.
- **`warning` on the trap in a rule.** Where a document explains the way people actually get this wrong, that sentence is a callout. Every rules document has at least one.
- **`info` on a scope limit.** Where a rule applies only to one platform, one shell, or one environment, say so in a callout rather than in a parenthesis somebody skims past.
- **`example` on a worked demonstration** that follows a rule, where the example is not already a fenced code block. A code block is its own emphasis and needs no wrapper.

## Where a Callout Is Forbidden

> [!danger]
> Never put a secret, a credential, a token, or a real configuration value inside a callout. A callout draws the eye, which is the opposite of what those need, and [[secret.rules.md]] forbids them anywhere in the vault regardless.

- **Never in the frontmatter or above the breadcrumb.** The frontmatter is first and the breadcrumb is second, per [[docs.rules.md]], and a callout above either breaks the fixed placement every document shares.
- **Never as a section divider.** The heading already divides. A callout used for rhythm is decoration.
- **Never nested.** A callout inside a callout does not render reliably and means the point has two parts, which is two callouts or one paragraph.
- **Never around a fenced code block.** Both render, but the inner block reads as noise and the reader loses which level they are on. A worked example belongs in prose beside the callout, not inside it.
- **Never more than three in one document.** A page of callouts has no emphasis left; the reader stops seeing them, which is exactly what happens to a document where everything is bold. This file is the one exception, because a document defining the types has to show them.
- **Never in a memory note body beyond one.** A note holds one thing, per [[memory.rules.md]], so at most one line in it can be the thing that must not be missed.

## Per Document Type

### Rules

Every rules document opens with one `[!info]` or `[!important]` callout stating in a sentence what the rule governs, so a reader landing from the index knows within a line whether this is the file they want.

Inside the document, a prohibition that carries real cost is a `[!danger]` or a `[!warning]`, not a bolded sentence. A prohibition that reads as ordinary prose gets skipped, and the reader finds out it was serious only after breaking it.

### Components

A component standard names its reference implementation in a `[!note]` near the top, because the source is what gets copied and the standard's text is only the description of it.

A deviation from the design system, where a project deliberately does something the standard does not, is a `[!warning]`. It is not an error, but a reader must not copy it by accident.

### Memory

Every memory note carries a callout matching what the note records, placed directly under the title so the type is visible in the graph view and in a hover preview.

| Note type | Callout |
| :- | :- |
| `fact` | `[!info]` |
| `decision` | `[!important]` |
| `session` | `[!note]` |
| `reference` | `[!quote]` |

A fact recording something that went wrong, such as a build that fails on first run or a connection that cannot be reached, uses `[!danger]` instead of `[!info]`. The note is a warning to a future reader, and typing it as neutral information hides exactly the thing that makes it worth keeping.

### Templates

A template marks its placeholder guidance with `[!example]`, so whoever fills it in can see at a glance which passages are instructions to be removed and which are structure to be kept.

## Writing a Callout

Keep it to one idea, in one to three sentences. A callout is a signal, and a long one stops being scannable, which was the only reason to use a box instead of a paragraph.

State the thing itself, not the fact that it is important. `[!warning]` already says it is important, so a first line reading "Important: be careful here" spends the reader's attention repeating what the type declared.

Weak, because the type already carries the emphasis and the text adds none of the specifics:

```markdown
> [!warning]
> Be very careful with this setting.
```

Strong, because it names what breaks and what it costs:

```markdown
> [!warning]
> Raising the concurrency setting does not add capacity. One instance holds a fixed CPU share, so the extra requests only queue, and the delay surfaces as a timeout rather than as a clear signal.
```

## Shape

```markdown
> [!warning]
> One line saying what goes wrong, and what to do instead.
```

- **The type is lowercase**, in square brackets with a leading `!`, on its own line.
- **One blank line before and after** the callout, per the block spacing in [[docs.rules.md]].
- **Every line of the callout is prefixed with `>`**, including a blank line inside it. A bare blank line ends the callout there, and the remainder renders as ordinary prose.
- **The body is one or two sentences.** A callout that runs to a paragraph is a section, and it gets a heading instead.
- The body follows every writing rule in [[docs.rules.md]]: one paragraph per line, no em dash, no emoji.

A multi-paragraph callout keeps its marker on the blank line:

```markdown
> [!info]
> First paragraph of the callout.
>
> Second paragraph, still inside it.
```

A title after the type replaces the default heading:

```markdown
> [!warning] The cookie is host-only
> A session cookie set on the API host never reaches a frontend served from another host.
```

Add a title when the default word is too generic to be useful. Leave it off when the type alone is clear, since a title repeating the type wastes the line.

Foldable callouts, written `> [!note]-` or `> [!note]+`, are not used. They hide content behind an interaction that does not exist outside Obsidian, so the passage renders expanded there and collapsed in the vault, and the two readings disagree.

## Rendering Outside Obsidian

GitHub renders five types: `note`, `tip`, `important`, `warning`, and `caution`. Every other type falls back to a plain blockquote there, keeping its text and losing its color.

This is a real constraint for a vault whose files are read on GitHub as often as in Obsidian. Prefer a GitHub-supported type when one fits the meaning, and reach for `danger`, `example`, `question`, `success`, or `todo` when the meaning genuinely needs them. The fallback degrades cleanly, so a passage never becomes unreadable, but it does become unmarked.

> [!warning]
> Never put meaning in the color alone. A passage reading "the red box above" breaks for every reader on GitHub, and for every colorblind reader everywhere. Write it so the words carry the meaning and the type only reinforces it.

## In a Memory Note

A note may carry **at most one** callout, and only for the line that changes what the reader does.

- Prefer the fixed `**Why:**` and `**Applies to:**` labels from [[memory.rules.md]]. They already carry the reasoning, and a callout does not replace them.
- Use `danger` where the note records something that destroyed data or leaked a value, so the next reader sees it before the detail.
- Use `warning` where the note records a symptom that misled, since that is the part a future session will otherwise repeat.
- Never wrap the whole note in a callout.

## Definition of Done

- Every type used is from the table, written in lowercase with a leading `!`.
- Every rules document opens with one `info` or `important` callout naming what it governs.
- Every destructive or irreversible instruction carries a `danger` callout.
- Every rules document carries at least one `warning` on its most common failure.
- No document carries more than three callouts, and no note more than one.
- No callout is nested, folded, wrapped around a code block, or used as a divider.
- No callout holds a secret or a real configuration value.
- No passage refers to a callout by its color.
- A blank line sits on both sides of every callout, and every line inside one carries its `>`.

## Applies To

- [[docs.rules.md]]
- [[memory.rules.md]]
- [[memory/codes.rules.md]]
- [[note.template.md]]
- [[secret.rules.md]]
- [[uix.component.md]]
