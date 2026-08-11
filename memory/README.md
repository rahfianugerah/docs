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

**1. Obsidian.** Open `docs/` as a vault. The memory is a folder inside it, and so is `graph/`, where every brain on this machine writes what it generated. So the rules, the memory, and the graph a model built all share one view and can link to each other.

**2. Cognee and Graphify.** `plugmybrain` runs both from one command, so this whole folder becomes a memory in a single step. Point it at any folder of markdown; the folder's own name is the memory it lands in.

```bash
pmb init brain .                                # once: scaffold this folder and wire the agents
pmb digest                                      # this folder: markdown to memory, plus the code map
pmb list                                        # what the memory holds, and what it was built from
pmb reset                                       # throw the index away; every markdown file survives
```

`init brain` is what marks this folder as the rules and memory rather than an ordinary project. In a parent folder holding many projects, `pmb init root .` marks that instead, and one digest walks every child with the brain going first. Whatever is digested, the generated notes land here in `graph/`, never in the project.

Digest after a batch of writes, not after every note. The index is derived; it can lag.

**3. Any coding agent.** Claude Code, Codex, opencode, anything speaking MCP. The memory is connected as a server with two read-only tools, `recall` and `brains`, so a question needs no command at all: ask, and the agent reads. `/pmb-map <brain>` switches which memory the session reads from when the work moves elsewhere.

## Rules

The protocol for writing and recalling is [[memory.rules.md]]. Read it before writing a note.

## Related

- [[memory.rules.md]]
- [[note.template.md]]
- [[graph/README.md]]
- [[docs.rules.md]]
- [[secret.rules.md]]
