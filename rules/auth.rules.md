---
tags:
  - kind/rule
  - layer/backend
  - topic/security
---

> Up: [[README.md]]

# Auth and Identity Standard

> [!important]
> One identity source, one identity key, one swappable abstraction. The browser holds an `HttpOnly` cookie and nothing else, and every route but health and login requires auth.

## Core Requirement

When building, modifying, or reviewing authentication, follow the controls here.

This standard makes a project ready to join a shared identity provider before one exists, which is the only time that decision is cheap. Retrofitting single sign-on onto an app that grew its own user table is most of a rewrite.

Where a reference implementation exists, follow it. Where it does not decide a matter, follow the rules below.

## Mandatory Principles

1. **One identity key.** Pick one stable identifier and carry it in the token as the subject claim. Do not use a username or an email address as the primary identity key: both change, and a person who changes theirs becomes a different person to every system that keyed on it.
2. **No bespoke account system.** Do not create a new user or password table per project. Credentials are owned by the identity source. The only local secret allowed is a stopgap hash in the environment file.
3. **Auth behind one swappable abstraction.** Every project reads identity from a single point that fills a request-scoped `auth = { subject, groups }`, plus a `require_role(...)` dependency. Changing the identity source must not require rewriting route code.
4. **Backend-for-frontend.** The browser holds only an `HttpOnly` cookie. **Never store a token in `localStorage` or `sessionStorage`**, because that exposes it to any XSS bug on the page.
5. **No open data routes.** Only the health endpoint and the login page or login endpoint may be public. Every other route requires auth, per [[api.rules.md]] and [[security.rules.md]].

## Identity Provider

- The identity provider verifies the credential against the identity source directly, read-only.
- **The provider reads the credential source through a least-privilege database user** that can `SELECT` only the login columns. It never reads personal data columns and never writes to the identity source. This follows [[database.rules.md]] and [[security.rules.md]].
- **The identity source must block an inactive account.** Someone who has left must lose access, enforced with an active condition checked on every login and every refresh, not only at first sign-in.
- Do not build a second identity source per project. Reuse one provider so identity stays consistent across every service.

## Auth Modes

Configure the mode through one environment variable. Every mode fills the same `auth = { subject, groups }`, so route code does not change between them.

| Mode | Identity source | When to use |
| :- | :- | :- |
| `local` | The identity source's user table, with this backend acting as the identity provider | Standard mode, including production |
| `dev` | A default local admin identity | Local development only. Never allowed on a server |
| `stopgap` | A password hash stored in the environment file | A thin in-app login used before a shared identity provider is ready |
| `proxy` | Headers from an authenticating proxy | Behind an external proxy that has already authenticated the user |

> [!danger]
> Production must not run the `dev` mode. The backend fails fast and refuses to start if it is set, because a dev-mode identity in production is an unauthenticated admin on every route.

## Password and Credential Handling

- Accept only strong hashes: **Argon2id** as the primary choice, bcrypt as acceptable, both through a maintained library.
- **Prohibited:** MD5, plain SHA1 or SHA256, a plaintext password, and any plaintext initial password stored in a database.
- Verify only against an allowlist of accepted hash schemes. A hash outside the allowlist is rejected, never guessed as plaintext.
- Store a stopgap password only as a hash in the environment file, never in a database and never in the repository, per [[secret.rules.md]].
- A password reset flow never sends a password through chat or plaintext email.

## Tokens

- **Sign access tokens with RS256** and publish the public key at `/.well-known/jwks.json`. Other services validate tokens offline against that key set.
- **Do not share a symmetric secret across services.** A shared HS256 secret makes every service a place the signing secret can leak from, and any one of them can then mint tokens for all of them.
- Other services must not call the identity provider on every request. They fetch and cache the key set, then validate locally, so the provider is not a single point of failure on their request path.
- **Every token has an `exp`.** Never issue one without an expiry.
- Keep the access token short-lived, about 15 minutes.
- Validate the `iss` and `aud` claims. The `iss` value must match exactly on the issuing side and the validating side. It is an identity string, not necessarily a publicly reachable URL.
- **The signing private key is persistent and secret.** If it is lost or rotated, every session dies at once. Store it outside the repository per [[secret.rules.md]], and back it up separately.

## Sessions and Cookies

- Deliver the access token in a cookie that is `HttpOnly`, `Secure` in production, and `SameSite=Lax`.
- **Store refresh state server-side.** Keep only a hash of the refresh token, never the token itself.
- **Rotate the refresh token on every use.** Detect reuse of an old refresh token and revoke every session for that subject when reuse is detected, because reuse means the token was copied.
- On logout, delete the cookie, revoke the refresh session, and, for an external provider, end the upstream session.

## Cross-Service Single Sign-On

- Cross-service sign-on works through a domain-scoped cookie, for example a cookie set for `.example.com`. Once a user logs in, every subdomain recognizes them without a redirect flow.
- Every participating service must sit under the shared cookie domain and be served over HTTPS in production, or the cookie will not be sent.
- **Set the cookie domain only in production.** Leave it empty on `localhost`, which has no subdomains, or the cookie is silently dropped and local login appears to succeed and then fail.

## Integration Guide: Connecting a Service

This is how a new or existing service joins. It does not call the identity provider on every request; it validates the cookie locally using the published key set.

### Step 1: Get the Required Values from the Provider Owner

| Value | Purpose |
| :- | :- |
| JWKS URL | Where to fetch the RS256 public key set. Expose it on the internal network only, never on a public port |
| Issuer (`iss`) | The exact string the provider stamps into every token. Must match on validation |
| Audience (`aud`) | The value the provider issues tokens for |
| Cookie name and domain | The access token cookie name and the shared cookie domain |

Do not guess these values or copy them from an unrelated environment. Confirm them against the provider.

### Step 2: Validate the Token on the Backend

Fetch and cache the key set, then verify every incoming request against it. Do not fetch the key set on every request; cache it and only refetch when a `kid` is unknown.

```python
import jwt
from jwt import PyJWKClient

jwks = PyJWKClient(SSO_JWKS_URL, cache_keys=True)

def current_user(request):
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        return None
    try:
        key = jwks.get_signing_key_from_jwt(token).key
        claims = jwt.decode(
            token, key, algorithms=["RS256"],
            audience=SSO_AUDIENCE,
            issuer=SSO_ISSUER,
        )
    except jwt.PyJWTError:
        return None
    return {"subject": claims["sub"], "groups": claims.get("groups", [])}
```

Wrap this in the project's single auth abstraction, per Mandatory Principle 3, so the result fills `auth = { subject, groups }` the same way every other mode does. Build `require_role(...)` on top of `auth.groups`, not on a new role table.

### Step 3: Handle the Unauthenticated Case

- If the cookie is missing or the token fails validation, **do not render a local login form**. Redirect the browser to the shared login page, and return the user to the original page after login.
- Return a `401` for an API call made without a valid cookie. Let the frontend handle the redirect, not the backend.
- Validate the return-to target against an allowlist before redirecting to it, per [[security.rules.md]].

### Step 4: Meet the Network and Cookie Requirements

- The service must be served over HTTPS in production and must sit under the shared cookie domain, or the cookie will never arrive.
- The service's backend must be able to reach the JWKS URL. Confirm that path for the actual topology before deploying.
- **Do not open the provider's port to the public internet to satisfy this.** Reachability is solved on the internal network, not by exposing the port.

### Step 5: Verify the Integration

- Log in through the shared login page, then confirm the service's own identity endpoint returns the expected subject and groups.
- Confirm an expired or tampered token is rejected.
- Confirm a request with no cookie is redirected to login, not treated as an anonymous data route.
- Confirm the service still starts and denies access cleanly if the provider is briefly unreachable during a key rotation, since a cached key set should keep already-fetched keys valid until the next fetch.

## Authorization

- **Roles and groups come from the identity source.** A service only checks membership through `require_role(...)`. Do not create a bespoke role table per service.
- The token carries only identity and group membership. Fine-grained authorization, meaning which specific records a user may see, stays in the service and is enforced in the query, per [[security.rules.md]].
- Gate a sensitive action, such as a configuration change, a device pairing, or a bulk delete, to an admin group.
- One role in the identity source maps to exactly one role in the service. A job title that maps to two application roles is a mapping nobody can reason about, and the second one is always the one that gets forgotten.

## A Non-Human Account

A system account, a service account, or an integration identity is not a person, and giving it a real role in the identity source to grant it access is the wrong move: it then appears in every report, every headcount, and every role-based screen as if it were a person.

Recognize it instead at the service's single authorization chokepoint, by its identifier, through one setting per service.

- The account holds no role in the identity source.
- Each service names the chokepoint it uses, so the exception exists in exactly one place per service.
- **The exception must be re-added to every new service**, which is the cost of this approach and the reason it is written down.
- The account is still audited like any other identity, per [[security.rules.md]].

## Legacy Projects With an Existing User Table

- Add an identity column and a `user_identities` table mapping the local user to the external identity: provider, subject, and the identity key.
- Run the legacy login and the shared login side by side during the transition. Disable the legacy login only after the shared one is stable.
- Never migrate password hashes into the shared provider. The provider owns credentials; the legacy table is being retired, not copied.

## Configuration and Fail-Fast

- Read every auth setting from the environment following [[env.rules.md]]. Never hardcode a secret. Never read a real environment file.
- **The backend fails fast and refuses to start** when a required secret is empty, still set to its placeholder, or inconsistent with the selected mode.
- In production, enforce that the dev mode is rejected, that the cookie is marked secure, and that the public API docs are disabled or authenticated.
- Rate-limit the login endpoint and store the lockout state in a shared store, not in the memory of a single worker, per [[security.rules.md]].
- Record an audit trail for login, failed login, and logout, with the acting identity and a timestamp.

## Definition of Done

- Identity is one stable key, carried as the subject claim. No service uses a username or an email address as the identity key.
- The auth mode switch works for at least `local`, `dev`, and `stopgap`, and switching modes does not change route code.
- Every data route reads `auth = { subject, groups }` and uses `require_role`. Only health and login are public.
- No token is stored in `localStorage` or `sessionStorage`. The browser holds only an `HttpOnly` cookie.
- Access tokens are RS256, validated offline through a cached key set, and every token has an `exp`.
- Refresh tokens rotate, are stored server-side as a hash, and are revoked on logout and on reuse detection.
- Passwords exist only as an Argon2id or bcrypt hash. No plaintext password exists in any database or in the repository.
- Production rejects the dev mode, the cookie is secure, public docs are closed, login is rate-limited, and the signing key is persistent and backed up separately.
- A non-human account is recognized by its identifier at a named chokepoint, not by a role in the identity source.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This auth standard
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Applies To

- [[api.rules.md]]
- [[database.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]
- [[stacks.rules.md]]
- [[login.component.md]]
- [[refresh.component.md]]
