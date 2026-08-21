---
type: decision
created: 2026-08-10
updated: 2026-08-10
tags: [plugmybrain, deploy]
status: current
---

# PlugMyBrain runs on a flat-cost VM, not Cloud Run

> [!important]
> The memory has no idle state.

**Decision:** one `docker compose` stack on a single always-on `e2-small` Compute Engine VM, holding Postgres, the Cognee MCP server and the one-shot ingest container. No Cloud Run, no Cloud SQL, no Secret Manager. [[deploy.rules.md]] carries the named exception.

**Why:** the memory has no idle state. Cloud Run scales to zero, but the database behind it cannot, so the managed shape pays a monthly floor for Cloud SQL and still needs a second service in front of it. One small VM covers both for one fixed line. [[deploy.rules.md]] already says Cloud SQL *"bills whether or not anything connects to it"* and is *"the single largest cost on an idle project"*; this is that reasoning applied to a database that must never sleep.

**Rejected:** Cloud SQL `db-f1-micro` plus Cloud Run, which is the cheapest managed shape and was the original plan. Its 0.6 GiB cannot run pgvector ingestion. The managed setup that would actually have worked is `db-g1-small` plus Cloud Run, which costs more than the VM and adds Cloud Build, Artifact Registry and Secret Manager to maintain.

**Cost accepted:** one machine is one point of failure, and patching, backups and disk are now mine. The mitigation is a nightly `pg_dump` plus the fact that the markdown vault is the real durable store: the whole database is rebuildable by re-running `pmb sync`. The exception does not generalise, and every other project still ships to Cloud Run.

**Source:** `plugmybrain/compose.yaml` and `plugmybrain/compose.override.yaml`, which are the whole stack the VM runs.

## Related

- [[deploy.rules.md]]
- [[database.rules.md]]
- [[postgres-holds-the-graph-as-a-demo-feature.decision.memory.md]]
