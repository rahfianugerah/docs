---
tags:
  - kind/template
  - layer/backend
  - layer/docs
---

> Up: [[README.md]]

# API Template

> [!example]
> Every `[bracketed]` passage below is guidance to be replaced, not structure to be kept. Remove each one once the real content is in place, and keep the headings and their order exactly as they are.

Copy this into `API.md` for any project that exposes endpoints. **Endpoint documentation lives only here**, never in the project README, per [[docs.rules.md]].

Every shape below is fixed by [[api.rules.md]]. Where this template and that standard disagree, the standard wins and this template is corrected.

## Table of Contents

1. API Overview
2. Base Configuration
3. Authentication and Authorization
4. Request Standards
5. Response Standards
6. Endpoint Reference
7. Error Handling
8. Pagination, Filtering, and Sorting
9. Rate Limiting and Security
10. Testing and Versioning

## 1. API Overview

`[One paragraph: what this API serves, who calls it, and what it is for.]`

## 2. Base Configuration

| Item | Value |
| :- | :- |
| Base URL | `[https://api.example.com]` |
| Base path | `api/v1` |
| Protocol | HTTPS in production |
| Content type | `application/json` |
| Character encoding | UTF-8 |
| Versioning method | In the path, `api/v1` |

**Every route is `api/<version>/<route>`, and the health endpoint is the only route outside that prefix**, per [[api.rules.md]].

### General Request Flow

```text
Client > Auth Middleware > Router > Validation > Service > Response
```

## 3. Authentication and Authorization

### Authentication Method

`[Session cookie, bearer token, API key, or other]`

### Authentication Header

```http
Cookie: [cookie_name]=<token>
```

or, for machine-to-machine:

```http
X-API-Key: <key>
```

### Authentication Flow

```text
Credentials > Identity Provider > Session Cookie > Protected Resource
```

### Token Information

| Item | Value |
| :- | :- |
| Algorithm | `[RS256]` |
| Lifetime | `[15 minutes]` |
| Refresh | `[Rotated on every use, stored server-side as a hash]` |
| Claims | `[sub, iss, aud, exp, groups]` |

The rules behind those values are in [[auth.rules.md]].

### Authorization Model

`[Role-based, permission-based, or attribute-based]`

| Role | Permissions |
| :- | :- |
| `[Role]` | `[Permissions]` |

### Public and Protected Endpoints

| Endpoint | Access |
| :- | :- |
| `/health` | Public |
| `api/v1/auth/login` | Public |
| Everything else | Authenticated |

**Only the health and login routes may be public**, per [[security.rules.md]].

## 4. Request Standards

### Request Headers

| Header | Required | Description |
| :- | :- | :- |
| `Content-Type` | Yes, on a body | `application/json` |
| `[Header]` | `[Yes or No]` | `[Description]` |

### Path Parameters

| Parameter | Type | Required | Description |
| :- | :- | :- | :- |
| `[parameter]` | `[Type]` | `[Yes or No]` | `[Description]` |

### Query Parameters

| Parameter | Type | Required | Default | Description |
| :- | :- | :- | :- | :- |
| `[parameter]` | `[Type]` | `[Yes or No]` | `[Default]` | `[Description]` |

### Request Body Format

```json
{
  "field": "[value]"
}
```

### Data Types

| Type | Format |
| :- | :- |
| String | UTF-8 |
| Number | JSON number, not a quoted string |
| Boolean | `true` or `false`, never `"true"` |
| Date and time | ISO 8601 with an explicit offset |
| Identifier | `[UUID or integer]` |
| Money | `[Minor units as an integer, or a decimal string]` |

### Date and Time Format

```text
2026-07-09T14:30:00+07:00
```

**Always with an explicit offset.** A naive local time is correct until the first reader in another offset.

### Validation Rules

Validation happens at the boundary with a typed model that **rejects an unexpected field** rather than ignoring it, per [[security.rules.md]]. Every string is bounded and every number has a range.

A validation failure returns `422`, never a `200` with an error body.

### File Upload

| Item | Value |
| :- | :- |
| Method | `multipart/form-data` |
| Maximum size | `[10 MB]` |
| Allowed types | `[pdf, jpg, png, webp]` |
| Type detection | By content, never by extension or header |

Owned by [[media.rules.md]].

## 5. Response Standards

### Success Response

```json
{
  "id": "abc123",
  "result": "value"
}
```

**The resource is the body.** Do not wrap a success in an envelope that repeats the HTTP status.

### List Response

```json
{
  "items": [],
  "total": 0,
  "limit": 20,
  "offset": 0
}
```

### Error Response

One shape for every error, so a caller writes one handler:

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order does not exist",
    "detail": null
  }
}
```

- `code` is a stable string a machine can rely on. **It must not change once published.**
- `message` is for a human reader, in the project's UI language.
- `detail` carries optional structured context, or `null`.

### Standard Status Codes

| Status | Name | Usage |
| :- | :- | :- |
| `200` | OK | Successful request |
| `201` | Created | Resource created |
| `204` | No Content | Success with no body |
| `400` | Bad Request | Malformed request |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Authenticated but not permitted |
| `404` | Not Found | Resource does not exist, or the caller may not see it |
| `409` | Conflict | Resource or state conflict |
| `422` | Unprocessable Entity | Validation failure |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unexpected server error |

Include only the codes the implementation actually returns.

> [!warning]
> **Never return `200` with a body saying the call failed.** The status must reflect the real outcome, or every client has to parse the body to find out whether the call worked.

**`404` is returned both for a record that does not exist and for one the caller may not see**, so the API does not confirm that a record exists, per [[security.rules.md]].

### Null and Empty Values

Describe how the API represents a missing value, an empty array, an empty object, an optional field, and a deleted resource. Pick one convention and hold it.

### Sensitive Data

A response never carries a password, a password hash, an access or refresh token, a private key, an internal stack trace, a database credential, secret configuration, or an internal identifier that leaks structure.

## 6. Endpoint Reference

Group endpoints by resource. One row per endpoint in the index, and a full section only where the behaviour is not obvious from the row.

| Method | Path | Purpose | Auth |
| :- | :- | :- | :- |
| `GET` | `/health` | Liveness check | No |
| `POST` | `api/v1/[resource]` | `[What it creates]` | Yes |
| `GET` | `api/v1/[resource]/{id}` | `[What it returns]` | Yes |

### `[Resource Name]`

#### `[METHOD] api/v1/[path]`

`[One sentence: what it does.]`

| Item | Value |
| :- | :- |
| Authentication | `[Required or Not required]` |
| Required role | `[Role or Not applicable]` |
| Idempotent | `[Yes or No]` |

Path parameters:

| Parameter | Type | Required | Description |
| :- | :- | :- | :- |
| `[parameter]` | `[Type]` | `[Yes or No]` | `[Description]` |

Query parameters:

| Parameter | Type | Required | Default | Description |
| :- | :- | :- | :- | :- |
| `[parameter]` | `[Type]` | `[Yes or No]` | `[Default]` | `[Description]` |

Request body:

```json
{
  "field": "[value]"
}
```

| Field | Type | Required | Validation | Description |
| :- | :- | :- | :- | :- |
| `field` | string | Yes | `[Length, range, allowed values]` | `[Description]` |

Example request:

```bash
curl -X [METHOD] "[BASE_URL]/api/v1/[path]" \
  -H "Content-Type: application/json" \
  -d '{ "field": "[value]" }'
```

Success response, `[200]`:

```json
{
  "id": "abc123",
  "result": "value"
}
```

| Field | Type | Description |
| :- | :- | :- |
| `id` | string | `[Description]` |

Error responses:

| Status | Code | When |
| :- | :- | :- |
| `422` | `[VALIDATION_FAILED]` | `[When]` |
| `404` | `[NOT_FOUND]` | `[When]` |

Notes:

`[Anything a caller will hit that the tables do not say.]`

## 7. Error Handling

### Error Categories

| Category | Status | Description |
| :- | :- | :- |
| Validation | `422` | Invalid input or a business rule failure |
| Authentication | `401` | Missing or invalid authentication |
| Authorization | `403` | Insufficient permission |
| Not found | `404` | Resource does not exist, or is not visible to this caller |
| Conflict | `409` | Data or state conflict |
| Rate limit | `429` | Too many requests |
| Internal | `500` | Unexpected failure |

### Error Code Convention

`[RESOURCE]_[CONDITION]`, in screaming snake case, stable once published.

```text
ORDER_NOT_FOUND
INVALID_CREDENTIALS
RATE_LIMIT_EXCEEDED
```

### Validation Error Example

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The request could not be processed",
    "detail": [
      { "field": "email", "reason": "not a valid address" }
    ]
  }
}
```

### Internal Error Example

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Something went wrong. Try again shortly",
    "detail": null
  }
}
```

**A `500` never returns a stack trace or an internal detail to the caller.** It is logged in full on the server, per [[repository.rules.md]].

### Retry Guidance

| Status | Retry |
| :- | :- |
| `429` | Yes, after the window the headers name |
| `500`, `502`, `503`, `504` | Yes, with backoff |
| `4xx` other than `429` | No; the request is wrong and will stay wrong |

**Any write a client may retry supports an idempotency key**, or deduplicates by a content hash, per [[api.rules.md]].

## 8. Pagination, Filtering, and Sorting

### Pagination

Every endpoint that returns a list is paginated. **There is no unbounded result set.**

| Parameter | Default | Maximum |
| :- | :- | :- |
| `limit` | 20 | 100 |
| `offset` | 0 | none |

The response carries `total`, so a client can compute the page count without a second call.

### Filtering

One query parameter per column, combined with `AND`.

```text
?status=approved&from=2026-07-01
```

A multi-select within one filter is a repeated parameter or a comma list, matched with `IN`.

### Sorting

```text
?sort=-created_at
```

A `-` prefix means descending. **The sort column is matched against an allowlist on the server**, per [[security.rules.md]]; an unknown column returns `422` rather than being interpolated into SQL.

### Search

Free-text search follows the ladder in [[search.component.md]]. **An identifier, a number, a date, and an enum are matched exactly, never fuzzily.**

## 9. Rate Limiting and Security

### Rate Limit

| Endpoint group | Limit | Window |
| :- | :- | :- |
| Login | `[5]` | `[per minute]` |
| Search | `[30]` | `[per minute]` |
| Everything else | `[120]` | `[per minute]` |

**Lockout state lives in a shared store**, never in the memory of a single worker.

### Rate Limit Headers

```http
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 118
X-RateLimit-Reset: 1767225600
```

### Security Controls

| Control | Implementation |
| :- | :- |
| Transport | HTTPS only, with HSTS |
| Input validation | Typed model at the boundary, unexpected fields rejected |
| Object authorization | Scoped in the query, not checked after the fetch |
| Injection | Parameterized queries only; identifiers via allowlist |
| Secrets | Never in a response, a log, or an error |
| Audit | Login, failed login, logout, and every destructive action |

Owned by [[security.rules.md]].

### CORS

| Item | Value |
| :- | :- |
| Allowed origins | `[An explicit list, never *]` |
| Allowed methods | `[GET, POST, PUT, PATCH, DELETE]` |
| Credentials | `[true or false]` |

**A reflected origin with credentials enabled is equivalent to no origin check at all.**

### Request Size Limits

| Item | Limit |
| :- | :- |
| JSON body | `[1 MB]` |
| Upload | `[10 MB]` |

## 10. Testing and Versioning

### Testing

| Item | Value |
| :- | :- |
| Tools | `[Tool]` |
| Automated tests | `[Where they live]` |
| Test environment | `[URL or Not applicable]` |

```bash
[Test command]
```

**Never point a test suite at production**, and never use a real credential in a fixture.

### Version History

| Version | Released | Notes |
| :- | :- | :- |
| `v1` | `[Date]` | `[Initial]` |

### Deprecation Policy

`[How long a deprecated endpoint is kept, and how a caller is told.]`

| Endpoint | Deprecated | Removal | Replacement |
| :- | :- | :- | :- |
| `[Path]` | `[Date]` | `[Date]` | `[Path]` |

### Breaking Changes

**A breaking change ships as a new version mounted alongside the old one.** The behaviour of a published version never changes silently, per [[api.rules.md]].

### Documentation Validation

Before treating this document as complete:

- Every documented endpoint exists, and every existing endpoint is documented.
- Every example request runs as written.
- No real credential, token, or personal record appears anywhere.
- Every error code listed is one the implementation actually returns.
- The pagination, error, and date formats match [[api.rules.md]].

## Related

- [[api.rules.md]]
- [[docs.rules.md]]
- [[backend.template.md]]
- [[project.template.md]]
- [[security.rules.md]]
- [[auth.rules.md]]
- [[search.component.md]]
- [[media.rules.md]]
