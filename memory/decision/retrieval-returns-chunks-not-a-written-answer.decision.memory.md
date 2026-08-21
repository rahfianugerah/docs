---
type: decision
created: 2026-08-10
updated: 2026-08-10
tags: [plugmybrain, retrieval]
status: current
---

# Retrieval returns chunks and sources, not a written answer

> [!important]
> The caller is already a model.

**Decision:** `pmb search` defaults to `SearchType.CHUNKS` with `only_context=True`, which returns retrieved passages and the files they came from. `GRAPH_COMPLETION` is behind an explicit `--mode graph`.

**Why:** the caller is already a model. Paying a second model to write prose about passages that an agent was going to read anyway doubles the latency and the bill for nothing, on the one path that runs on every question.

**Rejected:** `GRAPH_COMPLETION` as the default, which is cognee's own default. It reads better to a human and is the right choice for the HTTP API if a person ever uses it, which is why it stayed as a flag rather than being removed.

**Cost accepted:** cognee has no single mode returning chunks **and** graph context without a completion step, so the graph's connective value is only reachable through the paid path. If the question set shows retrieval missing multi-hop answers, the fix is a second query, and that is not built until the evaluation asks for it.

**Source:** `plugmybrain/plugmybrain/retrieve.py`, where the search type and `only_context` are set.

## Related

- [[embeddings-are-voyage-3-5-at-1024-dimensions.decision.memory.md]]
- [[memory.rules.md]]
