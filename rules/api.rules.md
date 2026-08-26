---
tags:
  - kind/rule
  - layer/backend
  - topic/data
---

> Up: [[README.md]]

# API Standard

> [!important]
> Every route is `api/<version>/<route>`. This policy owns that shape, the shared error format, and pagination.

## Core Requirement

When designing, building, or modifying a REST API, follow the rules in this policy.

One consistent style makes integration between services predictable and makes every endpoint safe to expose as a tool to an agent. This standard covers REST. An event bus is a later phase and is not part of it.

## Route Shape

**Every route is `api/<version>/<route>`. There is no exception, and nothing sits outside it.**

```text
api/v1/docs
api/v1/users
api/v1/users/{id}
api/v1/orders/{id}/documents
```

The three parts are fixed:

- **`api`** is the literal first segment on every route the backend serves. A backend serves nothing else.
- **`<version>`** is `v` followed by an integer: `v1`, `v2`. Never a decimal, never a date, never a name.
- **`<route>`** is the resource and whatever follows it, a plural noun in kebab-case: `purchase-orders`, `users`, `orders/{id}/documents`.

Rules:

- **Every route carries the prefix, including the ones that feel like infrastructure.** `api/v1/docs`, `api/v1/openapi.json`, and `api/v1/auth/login` all sit inside it. A framework that mounts `/docs` at the root by default is configured to move it, not left alone.
- **`/health` is the one route outside the prefix**, at the root. Every uptime probe expects it there, it must answer before the app knows its own version, and it is the only route [[security.rules.md]] allows to be public. Nothing else joins it.
- **Never a version anywhere but the path.** Not a header, not a query parameter, not a subdomain. A version in a header is invisible in a log, in a browser address bar, and in a bug report.
- A breaking change ships as `api/v2`, mounted alongside `v1`. Never change the behavior of `v1` silently.

This is what lets one proxy rule, one CORS origin, and one auth dependency cover the whole surface. It is also why a frontend is built with an origin and no path, per [[deploy.rules.md]]: the client holds the origin, every call appends `api/v1/...` itself, and the two halves are joined in exactly one place.

## Base Shape

- The route shape above applies to every endpoint. Everything below is what sits inside it.
- Use JSON for every request and response body, with `Content-Type: application/json`.
- Name a resource as a plural noun in kebab-case, for example `/api/v1/purchase-orders`.
- Use HTTP methods for their intended purpose: `GET` to read, `POST` to create, `PUT` or `PATCH` to update, `DELETE` to remove. Never perform a write or a destructive action through `GET`.
- Reference a person by the one stable identifier the system already uses, and use the same field name in every service. Two services calling it `user_id` and `employee_no` is how a join silently produces nothing.
- Format every timestamp as ISO 8601 with an explicit offset, for example `2026-07-09T14:30:00+07:00`. Never a naive local time.
- Keep OpenAPI generation enabled at all times, mounted at `api/v1/docs` and `api/v1/openapi.json`. In production both are disabled or authenticated, per [[security.rules.md]].

## Error Format

Return every error in the same shape across every service:

```json
{ "error": { "code": "ORDER_NOT_FOUND", "message": "Order does not exist", "detail": null } }
```

- `code` is a stable string a machine can rely on. It must not change once published.
- `message` is for a human reader, in the project's chosen UI language.
- `detail` carries optional structured context, or `null` when there is none.
- Use the HTTP status that matches the failure: `400` malformed, `401` missing authentication, `403` authenticated but not authorized, `404` missing, `409` conflict, `422` validation failure, `500` server error.

> [!warning]
> **Never return HTTP `200` with a body such as `{"success": false}`.** The status must reflect the real outcome, or every client has to parse the body to find out whether the call worked.

## Pagination, Filtering, and Sorting

- Paginate every endpoint that returns a list. Use `?limit=` with a default of 20 and a maximum of 100, and `?offset=` for the starting position. Include the `total` count in the response.
- Filter through one query parameter per column, for example `?status=approved&from=2026-07-01`.
- Sort through `?sort=`, where a `-` prefix means descending, for example `?sort=-created_at`.
- Never return an unbounded result set, per [[database.rules.md]]. An endpoint with no limit works until the table grows.

## Idempotency and Write Safety

- Support an idempotency key, or deduplicate by a content hash, for any write a client may retry: a webhook, a data ingest, a transfer. A retried payment that charges twice is the failure this prevents.
- Require an explicit confirmation step on the client for a destructive action, and record it in the audit trail with the acting identity and a timestamp, per [[security.rules.md]].

## Machine-to-Machine Access and Tool Endpoints

- Authenticate machine-to-machine calls with an `X-API-Key` header, scoped as `resource:action`. Never accept an unscoped or superadmin key.
- An endpoint exposed as a tool to an agent follows every rule here and also carries a clear `summary` and `description` in its OpenAPI definition, because those fields are what the tool definition is built from.
- Keep a tool endpoint's response friendly to a model: concise, with meaningful field names, and without a large blob in the default response. Offer a `?fields=` parameter when a caller needs to narrow it.
- **Treat every model-generated value as untrusted input.** It is derived from something a user typed, so it is never rendered as HTML and never executed, per [[security.rules.md]].

## Definition of Done

- Every route is `api/<version>/<route>`, including `api/v1/docs`, and `/health` is the only route outside the prefix.
- No version appears in a header, a query parameter, or a subdomain.
- OpenAPI generation is enabled and valid.
- Every error follows the standard error format, and every HTTP status reflects the real outcome.
- Every list endpoint is paginated.
- Every machine-to-machine call authenticates through a scoped API key.
- Every reference to a person uses the one agreed identifier.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This API policy
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[database.rules.md]]
- [[security.rules.md]]
- [[repository.rules.md]]
- [[stacks.rules.md]]
- [[path.rules.md]]
