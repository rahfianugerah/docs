---
tags:
  - kind/pattern
  - layer/database
  - topic/data
---

# Seed data cannot answer what production holds

> [!danger]
> A row read from the local database describes the local database and nothing else. Reporting it as what production contains is wrong roughly as often as it is right, and it reads as authoritative because the query genuinely succeeded.

The standing rule is to query the local database and never the production one. **That rule is about safety, not about accuracy**, and the two are easy to conflate: the only source available is also the only source that sounds like an answer.

Seeded rows drift from production in ways that look like real findings. A local fixture may carry a fully populated record where production deliberately keeps every one of those fields empty, and may hold an extra administrative account that no production instance has.

**The tell is in the data itself:**

- An email address on a local-only domain.
- A name as generic as "Super Admin".
- A creation timestamp matching the day the seed ran rather than the day the person joined.
- A row that contradicts a decision already recorded.

**What can be said about production without touching its database:** whatever the deployed configuration says, read from the platform's own service description, and whatever the code does with it. That combination answers most real questions correctly while a database reading is misleading.

**Why:** two consecutive reports were drawn from seeded local rows and both were wrong, and the correction came from the owner rather than from any check. A successful query feels like evidence.

**Applies to:** any claim about what production data contains, especially about accounts, roles, and permissions.

**Source:** an incident outside this repository. Confirm the shape of the drift by comparing a seed migration against the deployed configuration.

## Related

- [[database.rules.md]]
- [[a-read-only-migration-still-blocks-ddl-while-it-runs.pattern.md]]
- [[a-missing-feature-report-needs-three-checks-before-any-work.pattern.md]]
