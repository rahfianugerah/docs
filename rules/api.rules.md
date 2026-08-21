> Up: [[README.md]]

# API Standard

> [!important]
> Every route is `api/<version>/<route>`. This policy owns that shape, the shared error format, and pagination.

## Core Requirement

When designing, building, or modifying a REST API, follow the rules in this policy.

One consistent style makes integration between services predictable and makes every endpoint safe to expose as a tool to an agent. This standard covers REST. An event bus is a later phase and is not part of it.

## Base Shape

- Prefix every endpoint with `/api/v1`. Put the version in the path. A breaking change ships as `/api/v2`; never change the behavior of `v1` silently.
- Use JSON for every request and response body, with `Content-Type: application/json`.
- Name a resource as a plural noun in kebab-case, for example `/api/v1/purchase-orders`.
- Use HTTP methods for their intended purpose: `GET` to read, `POST` to create, `PUT` or `PATCH` to update, `DELETE` to remove. Never perform a write or a destructive action through `GET`.
- Reference a person by the one stable identifier the system already uses, and use the same field name in every service. Two services calling it `user_id` and `employee_no` is how a join silently produces nothing.
- Format every timestamp as ISO 8601 with an explicit offset, for example `2026-07-09T14:30:00+07:00`. Never a naive local time.
- Keep OpenAPI generation enabled at all times. In production, `/docs` and `/openapi.json` are disabled or authenticated, per [[security.rules.md]].

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

- Every endpoint sits under `/api/v1` and OpenAPI generation is valid.
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
