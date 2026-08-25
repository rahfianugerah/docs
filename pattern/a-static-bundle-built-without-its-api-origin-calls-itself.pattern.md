---
tags:
  - kind/pattern
  - layer/frontend
  - topic/deploy
---

# A static bundle built without its API origin calls itself

> [!danger]
> The value is baked at build time, so redeploying cannot fix it. Only a rebuild can.

A build path that omits the build argument produces a bundle whose HTTP client has an empty base, so every request goes to the frontend's own origin. The static fallback answers with `index.html`, and the browser surfaces a network error rather than an HTTP status.

Two signs identify it without guessing:

- The deployed image comes from the platform's generic source-deploy repository rather than the project's own registry.
- A request to the app's own origin at an API path returns an HTML body with a status that is not the backend's, and grepping the served bundle for the API host finds nothing.

The console's own "set up continuous deployment" button is the usual cause: it generates an inline build config that runs a bare image build with no build arguments and ignores the repository's pipeline file entirely. The fix is a trigger that points at that pipeline and passes the origin, then a rebuild.

While there, check the tag substitution. A typo in the short-SHA variable leaves the tag empty and the build rejects the image reference with `could not parse reference`.

**Why:** the failure appears in the browser as a CORS or connectivity problem, so the investigation goes to CORS headers and the backend, both of which turn out to be correct.

**Applies to:** any static frontend whose configuration is baked at build time, and any service whose trigger was created from a cloud console rather than by hand.

**Source:** an incident outside this repository. The mechanism is confirmed by reading any frontend pipeline file for the build-argument pairs the console path omits.

## Related

- [[deploy.cloud.md]]
- [[deploy.rules.md]]
- [[secret.rules.md]]
- [[the-first-build-on-a-new-service-fails-at-the-deploy-step.pattern.md]]
