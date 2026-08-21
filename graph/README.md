> Up: [[README.md]]

# Graph

![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Graphify](https://img.shields.io/badge/Graphify-Structural-B45309)
![Cognee](https://img.shields.io/badge/Cognee-Semantic-0F766E)

> [!warning]
> Everything below this file is machine-generated and rebuilt from a command. Editing it by hand is lost on the next rebuild, so write to the notes in `memory/` instead.

The machine-generated half of the memory. Everything below this file is rebuilt from a
command and is not part of the memory itself.

## Nothing Here Is Hand-Edited

This is the one folder in the vault that a tool writes into. Editing a file here is
wasted work: the next rebuild overwrites it, and git does not track it, so there is
nothing to recover.

**The memory is [[memory/README.md]] and [[docs.rules.md]] and the rest of this vault.**
Those files are human-authored, committed, and are what feeds the index. This folder is
the output. Delete it entirely and one command puts it back.

**Every brain on this machine generates into here**, one folder per brain, not into the project
it came from. A digested folder is only ever read; eighteen service repositories do not each
need a `graph/` nobody asked for, and the point of a vault is that it is one place you open and
see everything in.

| Folder | Holds |
| :- | :- |
| `code/<brain>/` | `GRAPH_REPORT.md`: the hubs, the surprising connections, the questions worth asking |
| `kg/<brain>/` | The Cognee knowledge graph as `[[wikilink]]` notes, so the vault graph view renders it |

Both are written by `pmb digest`, deleted by `pmb reset`, and gitignored. This README is none of
those and survives a reset. Graphify's raw `graph.json` stays in the `plugmybrain` repository,
because nobody reads json in Obsidian.

## Keeping Something You Find Here

A note here is disposable, so editing it is wasted work. When one turns out to be worth
keeping, move it into [[memory/README.md]] yourself, give it the frontmatter from
[[note.template.md]], and fill in the `**Why:**` line. From then on it is human-authored:
committed, yours to edit, and it survives every `pmb reset`.

The blank `**Why:**` line is the whole point. A kept note with no reason written down is a
machine's guess with a date on it.

## Why the Split

An agent that greps a repository to work out how it is wired pays for that in tokens
every session. `graph.json` is that answer, extracted once by tree-sitter with no model
involved, and read instead of the tree.

The rule that keeps this honest: **a rebuild must never modify a human-authored file.**
The folders are separate on disk, the generated ones are gitignored, and `git status`
after a rebuild is the test.

## Rebuilding

One command, run from this vault. It rebuilds both folders from the markdown above them.

```bash
pmb digest
```

## Related

- [[memory/README.md]]
- [[memory.rules.md]]
- [[docs.rules.md]]
