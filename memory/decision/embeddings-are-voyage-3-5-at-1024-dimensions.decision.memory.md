---
type: decision
created: 2026-08-10
updated: 2026-08-10
tags: [plugmybrain, embeddings]
status: current
---

# Embeddings are voyage-3.5 at 1024 dimensions

> [!important]
> 1024 is a ceiling, not a preference.

**Decision:** `EMBEDDING_MODEL=voyage/voyage-3.5` at `EMBEDDING_DIMENSIONS=1024`, with its own `EMBEDDING_API_KEY` separate from the chat key.

**Why:** 1024 is a ceiling, not a preference. **pgvector will not build an index on a `vector` column wider than 2000**, for HNSW or IVFFlat. It does not refuse loudly; it leaves every search doing a sequential scan. voyage-3.5 offers 2048, 1024, 512 and 256 via Matryoshka, so 1024 is the largest that stays indexable, and it is the model's own default.

**Rejected:** `text-embedding-3-large` at 3072, which is cognee's default and cannot be indexed at all. Also voyage-3.5 at 2048, for the same reason. Voyage ships no chat model, so the extraction model is a separate vendor and a separate key; a single-vendor setup was not available at this quality.

**Cost accepted:** two API keys to manage instead of one, and the embedding choice is locked to the corpus. Swapping the chat model is free; swapping the embedding model or its dimension means re-embedding everything. `config.py` refuses to start above 2000 rather than letting the mistake become a silent performance cliff.

**Source:** `plugmybrain/plugmybrain/config.py` for where the model and dimension are read, and `plugmybrain/.env.example` for the variables that set them.

## Related

- [[database.rules.md]]
- [[postgres-holds-the-graph-as-a-demo-feature.decision.memory.md]]
