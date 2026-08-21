---
type: session
created: 2026-08-11
updated: 2026-08-11
tags: [plugmybrain, ingest]
status: current
---

# Ingestion must run in the container, not on Windows

> [!note]
> `pmb sync` on Windows hung after init with no log activity and no rows written.

Cognee spawns subprocess database workers and talks to them over sockets, which is also what produced the earlier ConnectionRefusedError. The same code runs clean inside the Linux container.

Worse, the killed Windows runs wrote host paths into Postgres: cognee stored `raw_data_location` as `C:\...\.data_storage`, so a later container run died with `FileNotFoundError: /C:/Users/...`. The database had to be wiped, not repaired.

**Fix:** always ingest with `docker compose run --rm cognee-ingest`. **Lesson:** mixing hosts for one dataset poisons it. The path a document was ingested from is stored, so whichever machine ingests must be the machine that can still read those paths.

**Source:** `plugmybrain/plugmybrain/ingest.py` for the ingest path, and `plugmybrain/compose.yaml` for the container it has to run in.

## Related

- [[plugmybrain-runs-on-a-flat-cost-vm.decision.memory.md]]
- [[postgres-holds-the-graph-as-a-demo-feature.decision.memory.md]]
