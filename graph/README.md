> Up: [[README.md]]

# Graph

![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Graphify](https://img.shields.io/badge/Graphify-Structural-B45309)
![Cognee](https://img.shields.io/badge/Cognee-Semantic-0F766E)

The machine-generated half of the memory. Everything below this file is rebuilt from a
command and is not part of the memory itself.

## Nothing Here Is Hand-Edited

This is the one folder in the vault that a tool writes into. Editing a file here is
wasted work: the next rebuild overwrites it, and git does not track it, so there is
nothing to recover.

**The memory is [[memory/README.md]] and [[docs.rules.md]] and the rest of this vault.**
Those files are human-authored, committed, and are what feeds the index. This folder is
the output. Delete it entirely and one command puts it back.

| Folder | Written by | Holds |
| :- | :- | :- |
| `code/` | `pmb map <path>` | `GRAPH_REPORT.md` per project: the hubs, the surprising connections, the questions worth asking |
| `kg/` | `pmb export --project <name>` | The Cognee knowledge graph as `[[wikilink]]` notes, so the vault graph view renders it |
| `kg/` | `pmb visualize --project <name>` | `graph.html`: the same graph as one self-contained file, for when you just want to look |

Both are gitignored. The full Graphify output, including `graph.json` and the interactive
`graph.html`, lives in the `plugmybrain` repository under `graph/`, not in the vault.

## Why the Split

An agent that greps a repository to work out how it is wired pays for that in tokens
every session. `graph.json` is that answer, extracted once by tree-sitter with no model
involved, and read instead of the tree.

The rule that keeps this honest: **a rebuild must never modify a human-authored file.**
The folders are separate on disk, the generated ones are gitignored, and `git status`
after a rebuild is the test.

## Rebuilding

```bash
conda activate env
pmb map C:\path\to\any-project
```

## Related

- [[memory/README.md]]
- [[memory.rules.md]]
- [[docs.rules.md]]
