---
name: agentic-test-matrix
description: Picks the kinds of test a change needs from a four-stage taxonomy (pre-production, deploy, release, post-release), and returns a short table of each kind, why this change needs it, and where it lives in this stack (pytest on PostgreSQL, Playwright, ruff, ESLint, locust, Cloud Run). Use when planning the tests for a task, before a verifier or test designer writes them, or when a change feels under-tested or over-tested. Stays lean: the fewest kinds that cover the risk, never the whole list.
---

# Test Matrix

Every kind of test costs time to write and time on every run. Pick the fewest kinds that cover what this change can break, and say why each one earns its place.

## Steps

1. **Read the change.**

   ```bash
   git diff --stat --merge-base main
   git diff --merge-base main
   ```

   Or the paths and the plan the brief names, when nothing is written yet.

2. **Say what changed.** One change can be several of these:

   | What changed | It looks like |
   | :- | :- |
   | Pure logic | A function with no I/O: a calculation, a parser, a validator, a mapper |
   | An API contract | A route, a request or response schema, a status code, the error shape |
   | A query | SQL, an ORM query, an index, an Alembic migration |
   | A UI flow | A page, a form, a step a user takes |
   | A hot path | Code that runs per request at volume, per row, or per frame |
   | A deploy setting | An environment variable name, a Cloud Run flag, the Dockerfile, a build step |

   Note two more: whether it fixes a bug, and whether it touches auth, a secret, or personal data.

3. **Take the default picks for each, then cut.**

   | What changed | Pick | Add only when |
   | :- | :- | :- |
   | Pure logic | unit | property-based when the inputs are wide: parsing, money, dates. Mutation when the logic is critical and the tests look complete |
   | An API contract | functional, contract | integration when the route touches PostgreSQL |
   | A query | integration | benchmark when the table is large or the query sits on a hot path. A migration also upgrades and downgrades on a fresh database |
   | A UI flow | UI | acceptance when the owner signs the flow off; usability when the flow is new to users |
   | A hot path | benchmark | load before release when many users hit it at once; profiling after release when the benchmark cannot explain a number |
   | A deploy setting | config, smoke | canarying when a bad value takes the service down for everyone |
   | A bug fix | regression | |
   | Auth, a secret, personal data | threat modelling | penetration before release |

   - Drop a kind whose risk another picked kind already covers: a UI test through a form covers the component that only renders it.
   - Add a kind only for a risk you can name in one sentence. For an unusual risk, look it up in `references/taxonomy.md`, which has one line per kind across all four stages.
   - Lint, type checks, and static analysis (`ruff check`, `npx eslint`, `npx tsc --noEmit`) run on every change. Never list them as a pick.

4. **Place each pick in this stack.**

   | Kind | Where it lives |
   | :- | :- |
   | unit, functional, regression (backend) | pytest in `test/<area>/test_<module>.py`; `test/` mirrors `app/`; a route through `httpx.AsyncClient` |
   | unit (frontend) | Vitest, only for a parser, a formatter, or a calculation |
   | integration | pytest against a real PostgreSQL from `testcontainers`, never SQLite or a mock |
   | property-based | Hypothesis in pytest; fast-check in Vitest |
   | contract | `app.openapi()` compared with the committed schema, and the frontend client type-checked against it |
   | UI, acceptance | Playwright in `test/e2e/<flow>.spec.ts`, found by `data-testid`, run in the light and the dark theme |
   | benchmark | `EXPLAIN (ANALYZE, BUFFERS)` on the query, or a timed test, with the number compared to its budget |
   | load | locust in `test/load/locustfile.py`, against staging |
   | config, smoke | `gcloud run deploy --no-traffic --tag canary`, then the health route and one read route on the tag URL |
   | canarying | `gcloud run services update-traffic <service> --to-tags canary=10`, error rate and p95 compared with the current revision |
   | performance (frontend) | Lighthouse on the staging URL against the page budgets |

   A new test dependency, such as Hypothesis or fast-check, is the owner's call. Say so in the table rather than adding it.

5. **Return the table**, usually two to four rows, then one line for any kind someone might expect and you left out.

## Output

Change: `POST /api/v1/orders` accepts a discount code, with a new column `orders.discount_code` and its Alembic migration.

| Kind | Why this change needs it | Where it lives |
| :- | :- | :- |
| functional | The route must reject an expired code with 422 and the error shape | `test/orders/test_router.py` |
| contract | The response gains `discount_code`, and the frontend client must still type-check | `app.openapi()` snapshot, `npx tsc --noEmit` |
| integration | The code is looked up and stored in PostgreSQL, and the migration must apply and roll back | `test/orders/test_repository.py` on `testcontainers` |
| unit | Discount arithmetic rounds per line, not per order | `test/orders/test_pricing.py` |

Left out: UI, because no screen changes in this task; load, because the route is not on a hot path; property-based, because one rounding rule is covered by four cases.
