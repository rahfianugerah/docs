> Up: [[README.md]]

# API Template

Copy the block below into `API.md` for any project that exposes endpoints. One row per endpoint, and a section only for those whose behaviour is not obvious from the row.

Rules for filling it in are in [[docs.rules.md]].

```markdown
# [Project Name] API

![FastAPI](https://img.shields.io/badge/FastAPI-[Version]-009688?logo=fastapi&logoColor=white)
![Version](https://img.shields.io/badge/API-v1-6E7681)

Base URL: `[http://localhost:8000]`

All endpoints accept and return `application/json`.

## Authentication

[How a caller authenticates, and what happens without it. If there is none, say so and say why that is acceptable.]

```http
Authorization: Bearer <token>
```

## Endpoints

| Method | Path | Purpose | Auth |
| :- | :- | :- | :- |
| `GET` | `/health` | Liveness check | No |
| `POST` | `/v1/[resource]` | [What it creates] | Yes |
| `GET` | `/v1/[resource]/{id}` | [What it returns] | Yes |

## POST /v1/[resource]

[One sentence: what it does.]

Request:

```json
{
  "field": "value"
}
```

| Field | Type | Required | Notes |
| :- | :- | :- | :- |
| `field` | string | Yes | [Constraint: length, range, allowed values] |

Response `200`:

```json
{
  "id": "abc123",
  "result": "value"
}
```

## Errors

One shape for every error, so a caller writes one handler.

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "field must be between 1 and 100 characters"
  }
}
```

| Status | Code | Means |
| :- | :- | :- |
| `400` | `INVALID_INPUT` | The request failed validation |
| `401` | `UNAUTHORIZED` | Missing or invalid credentials |
| `404` | `NOT_FOUND` | No such resource |
| `429` | `RATE_LIMITED` | Too many requests |
| `500` | `INTERNAL_ERROR` | Something broke; the detail is in the server log, not in the response |

A `500` never returns a stack trace or an internal detail to the caller, per [[security.rules.md]].

## Rate Limits

[Requests per window, and what the caller sees when they exceed it. If there is none, say so.]

## Notes

[Anything a caller will hit that the tables do not say: pagination, idempotency, long-running requests, model inference latency.]
```

## Related

- [[docs.rules.md]]
- [[project.template.md]]
- [[security.rules.md]]
