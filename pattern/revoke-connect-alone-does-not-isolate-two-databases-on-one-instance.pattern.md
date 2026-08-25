---
tags:
  - kind/pattern
  - layer/database
  - topic/security
---

# REVOKE CONNECT alone does not isolate two databases on one instance

> [!danger]
> Two databases with a user each, cross-revoked, still let either user reach the other, because the managed platform makes every user it creates a member of a shared superuser role. Every symptom of the missing wall is silence.

A user created through the platform's own command comes back as a member of that role, confirmed by querying the role membership table. A database created the same way is owned by that same role. **While both remain true, each application user inherits owner rights on both databases and the revoke changes nothing it can observe.**

Three steps make the wall real, and all three are needed:

- `ALTER DATABASE <db> OWNER TO <user>`, so the database is owned by the application user rather than by the role both users belong to.
- `REVOKE ALL ON DATABASE <db> FROM PUBLIC` and from the sibling environment's user.
- `REVOKE <shared_superuser_role> FROM <user>`, which is the step that actually removes the inherited path.

Two things get in the way of running them:

- **The ownership change fails on PostgreSQL 16 and later** with `must be able to SET ROLE`, because that release split role membership into separate inherit, set, and admin rights. Run `GRANT <user> TO CURRENT_USER WITH SET TRUE` first.
- **A null ACL is not proof of a successful revoke.** Null means the default ACL, and the default for a database grants connect and temporary to public. A revoke that worked materialises the ACL, so the passing shape is an explicit grant to one user and nothing else.

**The only check that settles it is connecting as one environment's user to the other environment's database and being refused.** Reading the ACL narrows the possibilities; it does not close them.

**Why:** the isolation is the entire basis for putting a lower and a production database on one shared instance. Nothing errors, nothing logs, and the wall is assumed to exist until something writes across it.

**Applies to:** any two environments sharing one managed database instance, per [[database.rules.md]].

**Source:** an incident outside this repository. This lives in database role membership, not in any file. Confirm it by querying the role membership table on the instance.

## Related

- [[database.rules.md]]
- [[secret.rules.md]]
- [[deploy.rules.md]]
