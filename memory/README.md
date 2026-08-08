> Up: [[README.md]]

# Memory

![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Graphiti](https://img.shields.io/badge/Graphiti-Temporal-1E293B)
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
| **Semantic** | Cognee | A knowledge graph and vector index built from the markdown | Yes |
| **Temporal** | Graphiti | Episodes with valid-time: what was true, and when | Yes |

**The markdown is the only durable store.** Cognee and Graphiti are indexes over it. Delete either one and rebuild it from the files; delete the files and the memory is gone.

That inversion is the whole design. It means:

- Any model can read the memory with nothing but file access.
- Switching from one embedding model, graph database, or framework to another costs a reindex, not a migration.
- The memory is diffable, reviewable, and versioned, because it is text in git.
- A human can read and correct it in Obsidian without touching a database.

Obsidian is the write and read surface for a human. Cognee answers "what do I know about X". Graphiti answers "what did I know about X in March, and what changed".

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

**2. Cognee.** Point it at the folder and let it build.

```python
import cognee, asyncio

async def index():
    await cognee.add("memory/")          # ingest the markdown
    await cognee.cognify()               # build graph + embeddings
    return await cognee.search("what did I decide about the data loader")

asyncio.run(index())
```

**3. Graphiti.** Feed each session note as an episode, so the graph carries time.

```python
from graphiti_core import Graphiti

graphiti = Graphiti(uri, user, password)
await graphiti.add_episode(
    name="2026-02-11-scaler-leak",
    episode_body=note_text,
    source_description="memory/session",
    reference_time=note_created_at,      # valid-time, not ingest-time
)
```

Reindex both after a batch of writes, not after every note. They are derived; they can lag.

**4. Any model.** Give it [[memory.rules.md]] and file access. That is the whole integration.

## Rules

The protocol for writing and recalling is [[memory.rules.md]]. Read it before writing a note.

## Related

- [[memory.rules.md]]
- [[note.template.md]]
- [[docs.rules.md]]
- [[secret.rules.md]]
