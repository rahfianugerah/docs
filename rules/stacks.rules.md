---
tags:
  - kind/rule
  - topic/workflow
---

> Up: [[README.md]]

# Tech Stack Standard

> [!important]
> The approved stack for every layer, the pinning rules, and the choices prohibited without a written decision.

## Core Requirement

When scaffolding, building, or modifying a project, follow the stack defined here.

One stack across every project is what makes a second project cheap. A stack chosen per project means every setup is a first setup, every bug is a new bug, and nothing learned on one carries to the next.

> [!warning]
> **Where this text and a real manifest disagree, the manifest is correct and this file gets updated to match it.** A standard describing what was true a year ago is worse than none, because it is believed.

## Backend

- **Language:** Python 3.13, per [[codes.rules.md]]. Declare `requires-python = ">=3.13"` in the manifest and build on `python:3.13-slim`.
- **Framework:** FastAPI with Pydantic v2. Keep the auto-generated OpenAPI enabled and functional, and closed or authenticated in production per [[security.rules.md]].
- **Settings:** `pydantic-settings`. Configuration is read once into a typed settings object, never with a bare `os.getenv` scattered through the code, per [[env.rules.md]].
- **Server:** `uvicorn[standard]`, at least one worker, behind a static web server or proxy. Do not hold request state in memory; an instance can disappear between two requests.
- **Database driver:** `psycopg[binary]` v3. A project running async SQLAlchemy uses `asyncpg` on the app path and keeps `psycopg` for the migration path, because the migration tool runs sync.
- **Auth:** `PyJWT[crypto]` for RS256 verification and `passlib[argon2]` for any local hash. Never hand-roll token signing or a password hash, per [[security.rules.md]] and [[auth.rules.md]].
- **Uploads:** `python-multipart` for request parsing and an object-store client for storage, per [[media.rules.md]].
- **Scheduled work:** APScheduler in-process, or a scheduled container job. Do not build an event bus at this stage.
- **Dev tooling**, kept in `pyproject.toml` under `[project.optional-dependencies]` and out of the runtime image: `ruff`, `mypy`, `pytest`, `pytest-asyncio`, `pytest-cov`, and `testcontainers[postgresql]` for integration tests against a real database.

## Frontend

- **Scaffold:** `npm create vite@latest`, then React, then TypeScript with the React Compiler, then ESLint.
- **Runtime:** React 19 with `react-dom` 19. Do not start a new project on Create React App or a legacy bundler setup.
- **Build:** Vite, built on `node:20-alpine`, served from `nginx:1.27-alpine` as a static bundle. The frontend ships as files; do not introduce server-side rendering or a Node runtime in production without a documented exception.
- **Routing:** `react-router-dom` v7.
- **Language:** TypeScript. A JavaScript project is a legacy state to converge, not a second option for something new.
- **Icons: Tabler only**, per [[uix.component.md]]. The Tabler webfont is the reference; `@tabler/icons-react` is acceptable where tree shaking is needed. Never a second icon set in the same project, and never an emoji as an icon.
- **Fonts: Inter, and only Inter**, per [[uix.component.md]]. One family carries display, headings, body, UI, and numerals, with a system sans-serif fallback stack behind it.
- **Styling:** the token contract in [[uix.component.md]] is the source of truth. It is a hand-written token and semantic class layer (`:root`, `.btn`, `.field`, `.selectbox`, `.datepop`). Tailwind is available through `@tailwindcss/vite` and may be used for one-off layout, but it never replaces a semantic class the component standards define, and a component is never rebuilt out of utility classes.
- **Data fetching:** `@tanstack/react-query` v5 with `axios`. A project starts here rather than writing its own fetch and cache layer.
- **State:** React context and hooks. Introduce a state management library only when complexity genuinely requires it. Do not over-engineer.
- **Charts:** Chart.js, per [[dashboard.component.md]] and [[analytics.rules.md]].
- **Testing:** `@playwright/test` for end-to-end flows.
- **UI language:** the language the project's users speak, per [[prd.rules.md]]. Technical terms may stay in their original language.

## Database

- **Engine:** PostgreSQL 18, one instance, one database per project, per [[database.rules.md]].
- **ORM:** SQLAlchemy 2.x, with raw SQL for the cases [[database.rules.md]] names.
- **Migrations:** Alembic is mandatory. Never apply a manual schema change directly to a database.
- **Extensions:** `pg_trgm` and `unaccent`, enabled through a migration, wherever text search is implemented, per [[search.component.md]]. Never enabled by hand on a live database.

### Prohibited Without a Written Decision

- **SQLite in production.** It locks the whole database on write and does not survive multiple instances. It is fine for a local, single-user tool.
- **Any additional engine as a primary store**, such as MongoDB, Neo4j, or Redis. Each one is another thing to back up, patch, and learn. A memory or search layer that runs on top of PostgreSQL does not replace it.

## AI and Model Usage

- **Provider:** Claude, through the official `anthropic` Python SDK. Do not add a second provider or a local model without a written decision.
- **Call the model from the backend only.** An API key never reaches the browser.
- **Redact personal data before it reaches the model**, per [[security.rules.md]]. This is why a document is not sent as raw bytes: extract the text first with `pypdf` or `python-docx`, redact the extracted text, then send it. Raw PDF bytes cannot be redacted.
- Pin the SDK major version like any other dependency, and treat a model identifier as configuration rather than a literal spread through the code.
- Any write action performed by a model requires a confirmation flow and an audit trail.
- **Treat every model response as untrusted input.** It is generated from data a person typed, so it is never rendered as HTML and never executed.
- The memory layer runs on PostgreSQL, per [[memory/README.md]]. It is an index over markdown, not a replacement for the database.

## Runtime and Deployment

- Backend image: `python:3.13-slim`. Frontend: a `node:20-alpine` build stage producing a static bundle served by `nginx:1.27-alpine`.
- Target: Cloud Run, following [[deploy.rules.md]] and the runbook in [[deploy.cloud.md]].
- Machine learning work runs in a conda environment rather than a container image, per [[ai.rules.md]]. That is the one place this stack splits.

## Versioning and Dependencies

- Pin the major version in the manifest (`requirements.txt`, `pyproject.toml`, `package.json`). Do not float on `latest`.
- Use a bounded range rather than an exact pin for a library that patches often, such as `fastapi>=0.115,<1.0`, so a security patch arrives without a manual bump but a major cannot land unreviewed.
- Commit a single lockfile (`package-lock.json`, a pip freeze output, or `uv.lock`).
- **When a pin exists to work around a specific bug, write the reason next to it.** `bcrypt>=4.0,<4.1` is the ecosystem-wide example: passlib 1.7.4 reads `bcrypt.__about__.__version__`, which bcrypt 4.1 removed, so an unpinned install prints a false traceback at every start. An unexplained pin is removed by the next person who reads it, and the bug comes back.
- Keep runtime and development dependencies separate, so the production image does not carry the test and lint toolchain.
- Apply security updates on a cadence, not only when something breaks, and run the audit in CI, per [[security.rules.md]].

## Documented Exceptions

A project may use a different runtime only when a specific library requires it. Any exception must:

1. Be recorded in that project's README with the reason.
2. Still comply with every other rule here, including the database, versioning, and model rules.

## Definition of Done

- The manifest pins a major version for every direct dependency, and a lockfile is committed.
- Configuration is read once into a typed settings object, and no secret is in source.
- Migrations run from an empty database.
- No model is called from the browser, and no personal data reaches one unredacted.
- The frontend carries one icon set and one font family.
- Any deviation from this stack is written in the project README with its reason.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This tech stack standard
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this standard and is not a documented exception, tell the user which standard is affected before proceeding.

## Applies To

- [[api.rules.md]]
- [[auth.rules.md]]
- [[codes.rules.md]]
- [[database.rules.md]]
- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[env.rules.md]]
- [[media.rules.md]]
- [[repository.rules.md]]
- [[security.rules.md]]
- [[uix.component.md]]
