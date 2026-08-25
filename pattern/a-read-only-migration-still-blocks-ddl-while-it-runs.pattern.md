---
tags:
  - kind/pattern
  - layer/database
  - topic/data
---

# A read-only migration still blocks DDL while it runs

> [!warning]
> "No writes" is not the same as "no impact". A dump that cannot write to the source can still stop a schema change on it.

A migration script that opens every source connection as read-only is safe to run against a production database people are actively using. The refusal then comes from the database rather than from the script's discipline, which is what makes it verifiable: attempt every write statement through each connection pattern the script uses and confirm all of them are rejected.

**Four effects are real, and none of them change data:**

- The snapshot transaction stays open for the whole dump, so vacuum cannot reclaim rows that died after it started. The bloat clears on the next vacuum.
- **The dump holds a shared lock on every table.** This does not block reads or ordinary writes, so users notice nothing. It **does** block `ALTER TABLE`, `DROP`, `TRUNCATE`, and a non-concurrent index build.
- Every table is read sequentially: disk and network load on the source host. Compression happens inside the dump process, which means on the operator's machine, not on the server.
- One connection is consumed from the instance's budget.

Separately, **the snapshot freezes the source at the instant it opens**, so anything written during the dump does not travel. That is a completeness problem, not a safety one: fine for a rehearsal, which is why a real cutover stops the old application first.

**Why:** the question "is it safe to point this at live production?" gets asked again before every cutover, and answering it properly means auditing every source connection site, sweeping the subprocess calls, and proving the read-only enforcement rather than trusting it.

**Applies to:** any rehearsal or cutover run of a migration script against a live source.

**Source:** an incident outside this repository. Confirm the enforcement by attempting each write statement through every connection the script opens.

## Related

- [[database.rules.md]]
- [[a-restore-into-a-stricter-schema-needs-its-nullable-foreign-keys-detached.pattern.md]]
- [[seed-data-cannot-answer-what-production-holds.pattern.md]]
