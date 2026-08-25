---
tags:
  - kind/pattern
  - layer/backend
  - topic/security
---

# A host-only cookie never reaches a second host

> [!warning]
> A session cookie issued without an explicit domain is host-only and travels only to the exact host that set it. The symptom is a 401 that reads like a permissions bug.

While a frontend sits on a platform-assigned host and the API sits on a custom domain, they are different hosts. A login on the frontend never reaches the API host, and a request to the API carries no cookie at all.

The 401 misleads because everything it might implicate is correct:

- The API's own documentation endpoint returns 401 rather than 404, so it is mounted and the roles are right.
- The request simply has no cookie, because the one issued on the other host never travels here.

**To reach the API host directly in the meantime, log in against that host first**, from the same browser tab, then use it. Note the route prefix while doing so; guessing the login path is a second failure on top of the first.

**The permanent fix is to map both halves onto one shared domain**, then set the cookie domain and switch to a shared-domain cookie.

> Do not set the cookie domain while either half is still on a platform-assigned host. Setting it requires the host to sit under that domain, so it would break the login that currently works.

This is also exactly what cross-service single sign-on needs, per [[auth.rules.md]].

**Why:** a host-only cookie plus a not-yet-mapped host produces a 401 that reads like a documentation, role, or configuration bug, and sends debugging down the wrong path entirely.

**Applies to:** any two services on different hosts sharing a session, and any domain cutover.

**Source:** an incident outside this repository. The mechanism is visible wherever the code decides whether a cookie carries a domain.

## Related

- [[auth.rules.md]]
- [[login.component.md]]
- [[deploy.cloud.md]]
- [[security.rules.md]]
