---
type: decision
created: 2026-08-10
updated: 2026-08-10
tags: [plugmybrain, database]
status: current
---

# Postgres holds the knowledge graph, and that is a cognee demo feature

**Decision:** `GRAPH_DATABASE_PROVIDER=postgres`, so one PostgreSQL 18 container holds the
relational store, the pgvector index and the knowledge graph at once.

**Why:** one container is the entire local setup and one `pg_dump` is the entire backup. On a
2 GiB VM, a second database process is memory that is not available.

**Rejected:** embedded Kuzu, which is cognee's production-shaped default. It is a file, so the
one-shot ingest container would build the graph into its own ephemeral filesystem and lose it
on exit, and the MCP server could never read it. Neo4j was rejected as a second always-on
service on a box chosen for having only one.

**Cost accepted:** **cognee releases Postgres-as-graph as a demo feature; the production
version is licensed.** If it proves unstable the fallback is one environment variable,
`GRAPH_DATABASE_PROVIDER=kuzu`, which now works because the volume is persistent. The README
flags it as demo-only so nobody discovers this from a failure.

Related: [[plugmybrain-runs-on-a-flat-cost-vm.md]] · [[database.rules.md]]
