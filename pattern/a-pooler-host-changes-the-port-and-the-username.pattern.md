---
tags:
  - kind/pattern
  - layer/database
  - topic/data
---

# A pooler host changes the port and the username, and neither failure says so

> [!danger]
> A managed database's direct host may publish an AAAA record and no A record. A machine without global IPv6 then fails before it opens a socket, with a name-resolution error that reads like a mistyped hostname.

Confirm it by resolving the host: an AAAA row and no A row is the whole story. Use the pooler host instead, which resolves to IPv4. **Two details change with it, and both are silent failures on their own:**

- **The port must be the session-mode port**, not the transaction-mode one. Transaction mode hands the connection between transactions, so a dump loses its session partway and the result is inconsistent.
- **The username gains the project reference as a suffix.** The pooler reads that suffix to pick the project, and without it the connection is established and then refused at authentication with nothing naming the cause.

Any connection-string parameter copied from the provider's console may belong to a different client library entirely. A driver that does not recognize it rejects the whole string as an unknown parameter.

**Why:** three separate failures all present as either a name-resolution error or a bare authentication refusal, and none of them mentions the address family, the pooler, or the missing suffix.

**Applies to:** any migration or one-off dump against a managed database reached through a pooler.

**Source:** an incident outside this repository. Confirm the address-family half by resolving the direct host and finding no A record.

## Related

- [[database.rules.md]]
- [[a-restore-into-a-stricter-schema-needs-its-nullable-foreign-keys-detached.pattern.md]]
