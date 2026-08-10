> Up: [[README.md]]

# Memory

![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Graphify](https://img.shields.io/badge/Graphify-Structural-B45309)
![Cognee](https://img.shields.io/badge/Cognee-Semantic-0F766E)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)

A shared, portable memory for every AI model that works on these projects. One store, many readers.

## The Idea

An assistant with no memory relearns the same context every session, and asks the same question it asked last week. An assistant whose memory lives inside one vendor's product is a memory you lose when you switch models.

So the memory is **plain markdown in a git repository**. Every model reads it. No model owns it.

## Architecture

Three layers, one substrate:

| Layer | Tool | Holds | Rebuildable |
| :- | :- | :- | :- |
| **Substrate** | Obsidian vault, markdown files | Everything. The source of truth | **No.** This is the memory |
| **Structural** | Graphify | An AST map of a codebase: classes, functions, imports, call graph | Yes |
| **Semantic** | Cognee | A knowledge graph and vector index built from the markdown | Yes |

**The markdown is the only durable store.** Graphify and Cognee are indexes over it. Delete either one and rebuild it from the files; delete the files and the memory is gone.

That inversion is the whole design. It means:

- Any model can read the memory with nothing but file access.
- Switching from one embedding model, graph database, or framework to another costs a reindex, not a migration.
- The memory is diffable, reviewable, and versioned, because it is text in git.
- A human can read and correct it in Obsidian without touching a database.

Obsidian is the write and read surface for a human. Cognee answers "what do I know about X". Graphify answers "where in the code is X", without a model reading a single file.

Nothing here answers "what did I know in March". Git history does, and a `session/` note records what happened. A temporal layer was considered and dropped rather than left as an unbuilt claim.

## Layout

```text
memory/
  README.md            this file
  memory.rules.md      the write and recall protocol
  note.template.md     the shape of every note
  fact/                durable facts: who, what, preferences, constraints
  decision/            why something was chosen, and what was rejected
  session/             episodic log: what happened, when
  reference/           pointers to external things
```

Four note types, and no fifth without a reason. A type that holds three notes after six months should have been a tag.

| Type | Answers | Example |
| :- | :- | :- |
| `fact` | What is true | The conda env for project X is `xyz`; the user prefers Ruff over Black |
| `decision` | Why it is this way | Chose Polars over pandas for the loader, because the file is 40GB |
| `session` | What happened | 2026-02-11, debugged the scaler leak, found it in `preprocess.py` |
| `reference` | Where to look | The dataset licence page, the paper the architecture came from |

## Plugging It In

**1. Obsidian.** Open `docs/` as a vault. The memory is a folder inside it, so the rules and the memory share one graph and can link to each other.

**2. Cognee.** `plugmybrain` wraps the ingest, so this is one command.

```bash
pmb sync                                        # ingest rules/ and memory/ into the graph
pmb search "what did I decide about the loader" --project curated
```

**3. Graphify.** Point it at a repository to get the code map. No model is involved and no
file leaves the machine.

```bash
pmb map C:\path\to\any-project
```

Reindex both after a batch of writes, not after every note. They are derived; they can lag.

**4. Any model.** Give it [[memory.rules.md]] and file access. That is the whole integration.

## Rules

The protocol for writing and recalling is [[memory.rules.md]]. Read it before writing a note.

## Related

- [[memory.rules.md]]
- [[note.template.md]]
- [[graph/README.md]]
- [[docs.rules.md]]
- [[secret.rules.md]]
