> Up: [[README.md]]

# Tech Stack Standard

## Core Requirement

When scaffolding, building, or modifying a project, follow the stack defined here.

One stack across every project is what makes a second project cheap. A stack chosen per project means every setup is a first setup, every bug is a new bug, and nothing learned on one carries to the next.

> [!warning]
> **Where this text and a real manifest disagree, the manifest is correct and this file gets updated to match it.** A standard describing what was true a year ago is worse than none, because it is believed.

## Backend

- **Language:** Python 3.13, per [[codes.rules.md]]. Declare it in the manifest and build on a pinned slim image.
- **Framework:** FastAPI with Pydantic v2. Keep OpenAPI generation enabled, and closed or authenticated in production per [[security.rules.md]].
- **Settings:** `pydantic-settings`. Configuration is read once into a typed settings object, never with a bare `os.getenv` scattered through the code, per [[env.rules.md]].
- **Server:** `uvicorn[standard]`. Do not hold request state in memory; an instance can disappear between two requests.
- **Database driver:** `psycopg[binary]` v3. A project running async SQLAlchemy uses `asyncpg` on the app path and keeps a sync driver for the migration path.
- **Auth:** a maintained library for token verification and password hashing. Never hand-roll token signing or a password hash, per [[security.rules.md]].
- **Dev tooling**, kept out of the runtime image: `ruff`, `mypy`, `pytest`, and a container-based fixture for integration tests against a real database.

## Frontend

- **Scaffold:** Vite, with React and TypeScript.
- **Runtime:** current React. Do not start a new project on Create React App or a legacy bundler setup.
- **Build:** a static bundle, built in a Node stage and served by a static web server. The frontend ships as files; do not introduce server-side rendering without a documented exception.
- **Routing:** one router library, chosen once and used everywhere.
- **Language:** TypeScript. A JavaScript project is a legacy state to converge, not a second option.
- **Styling:** the token contract in [[uix.component.md]] is the source of truth. A utility framework may be used for one-off layout, but it never replaces a semantic class the component standards define, and a component is never rebuilt out of utility classes.
- **Icons:** one icon set for the whole project. Never mix two sets, and never an emoji as an icon.
- **Data fetching:** one query and cache library with one HTTP client. A project does not write its own fetch and cache layer.
- **State:** context and hooks. Introduce a state library only when complexity genuinely requires it.

## Database

- **Engine:** PostgreSQL, one instance, one database per project, per [[database.rules.md]].
- **ORM:** SQLAlchemy 2.x, with raw SQL for the cases [[database.rules.md]] names.
- **Migrations:** mandatory. Never apply a manual schema change directly to a database.
- **Extensions** are enabled through a migration, never by hand on a live database.

### Prohibited Without a Written Decision

- **SQLite in production.** It locks the whole database on write and does not survive multiple instances. It is fine for a local, single-user tool.
- **Any additional engine** as a primary store. Each one is another thing to back up, patch, and learn. A memory or search layer that runs on top of PostgreSQL does not replace it.

## AI and Model Usage

- **Call the model from the backend only.** An API key never reaches the browser.
- **Redact personal data before it reaches the model**, per [[security.rules.md]]. Extract text from a document first, redact the extracted text, then send it. Raw bytes cannot be redacted.
- Pin the SDK major version like any other dependency, and treat a model identifier as configuration rather than a literal spread through the code.
- Any write action performed by a model requires a confirmation flow and an audit trail.
- **Treat every model response as untrusted input.** It is generated from data a person typed, so it is never rendered as HTML and never executed.

## Versioning and Dependencies

- Pin the major version in the manifest. Do not float on `latest`.
- Use a bounded range rather than an exact pin for a library that patches often, so a security patch arrives without a manual bump but a major cannot land unreviewed.
- Commit a single lockfile.
- **When a pin exists to work around a specific bug, write the reason next to it.** An unexplained pin is removed by the next person who reads it, and the bug comes back.
- Keep runtime and development dependencies separate, so the production image does not carry the test and lint toolchain.
- Apply security updates on a cadence, not only when something breaks.

## Documented Exceptions

A project may use a different runtime only when a specific library requires it. Any exception must be recorded in that project's README with the reason, and must still comply with every other rule here.

## Definition of Done

- The manifest pins a major version for every direct dependency, and a lockfile is committed.
- Configuration is read once into a typed settings object, and no secret is in source.
- Migrations run from an empty database.
- No model is called from the browser, and no personal data reaches one unredacted.
- Any deviation from this stack is written in the project README with its reason.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This tech stack policy
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy and is not a documented exception, tell the user which standard is affected before proceeding.

## Applies To

- [[api.rules.md]]
- [[codes.rules.md]]
- [[database.rules.md]]
- [[deploy.rules.md]]
- [[env.rules.md]]
- [[repository.rules.md]]
- [[security.rules.md]]
- [[uix.component.md]]
