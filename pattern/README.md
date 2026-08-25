---
tags:
  - kind/pattern
  - topic/workflow
---

> Up: [[README.md]]

# Patterns

> [!info]
> A lesson that cost something to learn, written so the next project does not pay for it again. A pattern is not a memory note: it carries no claim about any repository in this vault.

## What a Pattern Is

A pattern records **a failure and its mechanism**, generalized away from the system it happened in. It is here because the mechanism repeats and the symptom points somewhere else.

The difference from [[memory/README.md]] matters and is not a technicality:

| | A memory note | A pattern |
| :- | :- | :- |
| Claims | Something is true of a named file, project, or environment | A mechanism repeats wherever the conditions hold |
| `Source` | A real path from this workspace root | The incident it came from, which is outside this repository |
| Goes stale | When the file it names changes | When the technology it describes changes |
| Written by | The session that learned it | A session that generalized someone's incident |

**A memory note requires a `Source` path that resolves from the workspace root**, per [[memory.rules.md]]. A lesson learned in a system this vault does not contain cannot honour that, and inventing a path would be a fabricated provenance. So it lives here instead, and says plainly where it came from.

## Shape

The same shape as a memory note, with `kind/pattern` in the frontmatter and one difference in the labels:

```markdown
---
tags:
  - kind/pattern
  - topic/[concern]
---

# One line stating the mechanism

> [!danger]
> The line a reader must not miss.

The statement, in one or two sentences.

The detail underneath it.

**Why:** why the symptom points at the wrong thing.

**Applies to:** the conditions under which this repeats.

**Source:** the incident, named honestly as being outside this repository.

## Related
```

- **One pattern holds one mechanism.** Two mechanisms is two files.
- **The title states the mechanism, not the topic.** "A host-only cookie never reaches a second host" beats "Cookie notes".
- At most one callout, per [[callout.rules.md]].
- One paragraph is one line, per [[docs.rules.md]].

## Related

- [[memory/README.md]]
- [[memory.rules.md]]
- [[docs.rules.md]]
- [[callout.rules.md]]
