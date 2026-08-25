---
tags:
  - kind/template
  - layer/backend
  - layer/docs
---

> Up: [[README.md]]

# Backend README Template

> [!example]
> Every `[bracketed]` passage below is guidance to be replaced, not structure to be kept. Remove each one once the real content is in place, and keep the headings and their order exactly as they are.

Copy everything from the `# Title` line down into the backend repository's `README.md`.

```markdown
# [Project Name]

![Python](https://img.shields.io/badge/Python-VERSION-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-VERSION-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-VERSION-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-VERSION-D71F00?logo=sqlalchemy&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Managed-4285F4?logo=googlecloud&logoColor=white)
![Testing](https://img.shields.io/badge/Testing-VALUE-COLOR)
![Cache](https://img.shields.io/badge/Cache-VALUE-COLOR)
![Status](https://img.shields.io/badge/Status-VALUE-COLOR)
![License](https://img.shields.io/badge/License-VALUE-COLOR)
```

Follow [[badge.rules.md]] for the row. Remove a badge only when the project genuinely has no equivalent value to report; never invent one.

## Table of Contents

1. Project Overview
2. Technology Stack
3. System Architecture
4. Project Structure
5. Configuration
6. Database
7. Authentication and Security
8. Business Logic and Integrations
9. Testing and Error Handling
10. Development and Deployment

## 1. Project Overview

`[One paragraph: what this backend is, what problem it solves, and its main purpose.]`

**Do not include endpoint details.** API documentation lives in `API.md`, per [[api.template.md]] and [[docs.rules.md]].

## 2. Technology Stack

| Category | Technology | Version |
| :- | :- | :- |
| Runtime | `[Runtime]` | `[Version]` |
| Framework | `[Framework]` | `[Version]` |
| Language | `[Language]` | `[Version]` |
| Database | `[Database]` | `[Version]` |
| ORM or driver | `[ORM, query builder, or driver]` | `[Version]` |
| Cache | `[Technology or status]` | `[Version]` |
| Queue | `[Technology or status]` | `[Version]` |
| Testing | `[Testing tool]` | `[Version]` |
| Deployment | `[Platform]` | `[Version or Not applicable]` |

Use this status when a technology is not used:

```html
<code style="color: red">Not Used</code>
```

## 3. System Architecture

### Architecture Type

`[Monolith, modular monolith, microservices, serverless, or other]`

### Architecture Description

`[How the backend is organized]`

### Main Components

| Component | Responsibility |
| :- | :- |
| `[Component]` | `[Responsibility]` |

### Application Flow

```text
Request > Middleware > Router > Service > Repository > Database
```

### Processing Model

`[Synchronous, asynchronous, event-driven, scheduled, or mixed]`

## 4. Project Structure

```text
[The relevant directory structure]
```

### Directory Explanation

| Directory | Purpose |
| :- | :- |
| `[Path]` | `[Purpose]` |

Include only the directories needed to understand the system. **Do not include generated, dependency, cache, or build output directories** unless one genuinely requires explanation.

## 5. Configuration

### Configuration Files

| File | Purpose |
| :- | :- |
| `.env.example` | Environment variable reference |
| `[File]` | `[Purpose]` |

### Environment Variables

| Variable | Required | Description | Example |
| :- | :- | :- | :- |
| `[VARIABLE_NAME]` | `[Yes or No]` | `[Description]` | `[Placeholder]` |

**`.env.example` is the only environment variable reference.** Do not read, inspect, print, or use a value from a real environment file, per [[env.rules.md]].

Never include a real credential, API key, password, token, private key, or production connection string.

### Environments

| Environment | Purpose |
| :- | :- |
| Development | Local development |
| Test | Automated testing |
| Staging | Pre-production verification |
| Production | Live |

## 6. Database

### Overview

`[What the database holds and what it is for]`

### Information

| Item | Value |
| :- | :- |
| Engine | `[Engine]` |
| Version | `[Version]` |
| Access method | `[ORM, driver, or query builder]` |
| Migration tool | `[Tool]` |

### Main Tables

| Table | Purpose |
| :- | :- |
| `[Name]` | `[Purpose]` |

### Main Entity Details

#### `[Entity Name]`

| Field | Type | Required | Description |
| :- | :- | :- | :- |
| `[field_name]` | `[Type]` | `[Yes or No]` | `[Description]` |

Primary key: `[field]`

| Source | Relationship | Target |
| :- | :- | :- |
| `[Entity]` | `[One-to-one, one-to-many, many-to-many]` | `[Entity]` |

| Index or constraint | Fields | Purpose |
| :- | :- | :- |
| `[Name]` | `[Fields]` | `[Purpose]` |

Repeat only for important entities.

### Migration and Seeding

```bash
[Migration command]
```

```bash
[Seed command]
```

### Backup and Recovery

| Item | Description |
| :- | :- |
| Backup method | `[Method]` |
| Frequency | `[Frequency]` |
| Retention | `[Period]` |
| Recovery process | `[Process]` |

**An untested restore procedure is a hypothesis**, per [[database.rules.md]]. Say when it was last verified.

## 7. Authentication and Security

### Authentication Method

`[Session, token, API key, external provider, or other]`

### Authentication Flow

```text
Credentials > Identity Provider > Session or Token > Protected Resource
```

### Authorization Model

`[Role-based, permission-based, attribute-based, or other]`

### Roles

| Role | Permission Summary |
| :- | :- |
| `[Role]` | `[Permissions]` |

### Security Controls

| Control | Implementation |
| :- | :- |
| Input validation | `[Implementation]` |
| Password protection | `[Implementation]` |
| Rate limiting | `[Implementation]` |
| Data encryption | `[Implementation]` |
| Secret management | `[Implementation]` |
| Audit logging | `[Implementation]` |

Use these statuses where appropriate:

```html
<code style="color: green">Active</code>
<code style="color: yellow">Needs Confirmation</code>
<code style="color: red">Not Used</code>
```

## 8. Business Logic and Integrations

### Main Modules

| Module | Responsibility |
| :- | :- |
| `[Module]` | `[Responsibility]` |

### Main Business Rules

| Rule | Description |
| :- | :- |
| `[Rule]` | `[Description]` |

### Background Processes

| Process | Type | Schedule or trigger | Purpose |
| :- | :- | :- | :- |
| `[Process]` | `[Job, queue, worker, event]` | `[Schedule]` | `[Purpose]` |

Every job here is listed in the project's `deploy.cloud.md` section 1 table too, per [[deploy.cloud.md]]. **A job missing from that table is a job nobody moves forward on release.**

### External Services

| Service | Purpose | Integration method |
| :- | :- | :- |
| `[Service]` | `[Purpose]` | `[SDK, HTTP, webhook]` |

### Failure Handling

`[Timeout, retry, fallback, and failure handling]`

**An external validation fails closed**, per [[repository.rules.md]]. Do not include a secret key or a detailed endpoint specification here.

## 9. Testing and Error Handling

### Testing Strategy

| Test type | Purpose | Tool |
| :- | :- | :- |
| Unit | `[Purpose]` | `[Tool]` |
| Integration | `[Purpose]` | `[Tool]` |
| Database | `[Purpose]` | `[Tool]` |
| End-to-end | `[Purpose]` | `[Tool]` |

Include only the test types the project uses.

### Running Tests

```bash
[Test command]
```

### Error Categories

| Category | Description |
| :- | :- |
| Validation | Invalid input or business rule failure |
| Authentication | Missing or invalid authentication |
| Authorization | Insufficient permission |
| Not found | Resource does not exist |
| Conflict | Data or state conflict |
| Internal | Unexpected backend failure |

### Error Flow

```text
Application Error > Error Handler > Log Entry > Standard Response
```

The response shape is fixed by [[api.rules.md]]. **Endpoint-specific errors are documented in `API.md`, not here.**

### Logging and Monitoring

| Area | Tool or method |
| :- | :- |
| Application logs | `[Tool]` |
| Error tracking | `[Tool]` |
| Performance monitoring | `[Tool]` |
| Database monitoring | `[Tool]` |

## 10. Development and Deployment

### Requirements

- `[Runtime]`
- `[Package manager]`
- `[Database]`
- `[Other]`

### Installation

```bash
[Installation command]
```

### Environment Setup

1. Copy `.env.example` to the local environment file.
2. Add the required values by hand.
3. Do not commit the local environment file.

```bash
[Setup command]
```

### Database Setup

```bash
[Database setup command]
```

### Start the Application

```bash
[Development command]
```

### Build

```bash
[Build command]
```

### Deployment

| Item | Description |
| :- | :- |
| Platform | `[Platform]` |
| Trigger | `[Branch, tag, or manual]` |
| Migration process | `[Process]` |
| Health check | `[Method]` |
| Rollback process | `[Process]` |

The full procedure is the project's own `deploy.cloud.md`, copied from [[deploy.cloud.md]].

### Known Limitations

| Limitation | Impact | Planned resolution |
| :- | :- | :- |
| `[Limitation]` | `[Impact]` | `[Resolution or Not planned]` |

Use this status when there are none:

```html
<code style="color: green">No Known Limitations</code>
```

## Related

- [[docs.rules.md]]
- [[badge.rules.md]]
- [[frontend.template.md]]
- [[api.template.md]]
- [[project.template.md]]
- [[env.rules.md]]
- [[deploy.cloud.md]]
