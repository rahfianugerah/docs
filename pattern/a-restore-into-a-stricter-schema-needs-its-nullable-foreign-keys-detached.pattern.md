---
tags:
  - kind/pattern
  - layer/database
  - topic/data
---

# A restore into a stricter schema needs its nullable foreign keys detached

> [!danger]
> The failure names one row while the cause is a schema-wide difference in how strictly each side was defined, so it reads like bad data and invites cleaning the wrong database.

Restoring a dump into a schema built by a different tool fails on the first table carrying a stale reference, with a foreign key constraint violation.

**The value is not corrupt data.** The source schema either left the constraint off or created it as not-validated, so rows that point at nothing were always allowed to exist there. The new schema declares the constraint properly and refuses them.

Two reflexes are both wrong here:

- **Cleaning the source is not available** when it is still serving production and the access is read-only.
- **Disabling triggers during the dump is not available either** on a managed database. The flag emits a statement that needs superuser, which a managed instance grants to nobody, and the restore stops with a permission error naming a system trigger.

What works is to **detach only the foreign keys whose column is nullable**, load the dump, null the orphaned values, then re-add the constraints. A table owner may drop and add its own constraints, so no elevated rights are involved.

**Keep every non-nullable foreign key enforced throughout.** An orphan there means the source really is broken, and that has to stop the migration rather than be patched silently.

**Why:** the error points at a row, so the instinct is to fix data. The difference is in the schema definitions, and it is invisible from either side alone.

**Applies to:** any restore into a schema whose constraints are stricter than the source's, which is every migration away from a tool that treats constraints as optional.

**Source:** an incident outside this repository. The mechanism is confirmed by comparing the two schemas' constraint definitions rather than the rows.

## Related

- [[database.rules.md]]
- [[a-pooler-host-changes-the-port-and-the-username.pattern.md]]
- [[a-read-only-migration-still-blocks-ddl-while-it-runs.pattern.md]]
