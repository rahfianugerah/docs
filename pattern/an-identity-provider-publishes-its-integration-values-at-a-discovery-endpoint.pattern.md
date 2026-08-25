---
tags:
  - kind/pattern
  - layer/backend
  - topic/security
---

# An identity provider publishes its integration values at a discovery endpoint

> [!info]
> The issuer, the key set URI, the signing algorithm, and the claim names are all self-serve. Nothing has to be asked for and nothing has to be guessed.

A standards-compliant provider serves a discovery document that carries every value an integrating service needs. Read the issuer and the key set URL straight from it, and confirm the claim names against the supported-claims list in the same response.

**Check the body, not the status code.** The provider's frontend and its API are usually different hosts, and a single-page frontend answers *any* path with its own HTML and a 200. Probing the frontend host for the key set therefore looks like it succeeded while returning a document, which makes the wrong host easy to write into a configuration and hard to notice.

**Why:** a runbook that says these values must be requested from the provider's owner and never guessed has the right instinct and the wrong conclusion. The values are self-serve, so the request is a round trip nobody needs, and someone who takes the instruction literally is blocked waiting on a reply.

**Applies to:** any service configuring a key set URL, an issuer, or claim names against a provider that serves a discovery document.

**Source:** an incident outside this repository. Confirm by fetching the discovery path on the provider's API host.

## Related

- [[auth.rules.md]]
- [[env.rules.md]]
- [[deploy.cloud.md]]
