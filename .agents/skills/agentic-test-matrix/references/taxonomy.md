# Test Taxonomy

Every kind of test, grouped by the stage where it runs. One line each: what it catches, then where it lives in this stack. `/agentic-test-matrix` picks from here only when its default table does not cover the risk.

## Pre-production

Run before the code is deployed anywhere.

- **unit**: one function's logic in isolation. pytest in `test/<area>/`; Vitest for a frontend parser, formatter, or calculation.
- **functional**: one feature's behaviour through its public entry, such as a route. pytest calling the app through `httpx.AsyncClient`.
- **component**: one UI component's behaviour in isolation. A component that only renders is covered by its Playwright flow; Vitest only when it holds logic.
- **fuzz**: crashes and unhandled errors on malformed input. Schemathesis against `/openapi.json`, or Hypothesis feeding a parser.
- **property-based**: a rule that must hold for every generated input, such as "parse then print returns the input". Hypothesis in pytest; fast-check in Vitest.
- **formal verification**: every ordering in a model, or every input of a function, checked by a tool. TLA+ and TLC, Lean, or CrossHair, set up by `/agentic-create-formal-verification-skill`.
- **static analysis**: bug patterns found without running the code. `ruff check`, `npx tsc --noEmit`, and Bandit or Semgrep for security.
- **mutation**: tests that pass whatever the code does. mutmut for Python, StrykerJS for TypeScript, run on one module, never the whole repository.
- **coverage**: lines no test runs. `pytest --cov=app`, read as a list of gaps, never chased as a target.
- **benchmark**: a time or memory number against its budget. `EXPLAIN (ANALYZE, BUFFERS)` for a query, or a timed test, with the number recorded.
- **contract**: a producer and a consumer that disagree about an interface. `app.openapi()` compared with the committed schema, and the frontend client type-checked against it.
- **lint**: style and suspicious constructs. `ruff check`, `ruff format --check`, `npx eslint`, on every change.
- **acceptance**: each acceptance criterion from the requirements, as a named test. pytest or Playwright, one test per criterion ID, signed off by the owner.
- **regression**: a fixed bug coming back. A test that reproduces it, named after the behaviour, written before the fix.
- **smoke**: a build that does not start or serve at all. The health route and one read route, run first after every deploy.
- **usability**: a flow people cannot finish or understand. The owner or a user walks it on a phone; findings go in the report.
- **UI**: a user flow breaking end to end in the browser. Playwright in `test/e2e/`, by `data-testid`, in the light and the dark theme.
- **penetration**: what an attacker can actually do. An attacker's pass on staging with the security reviewer, never production without the owner's approval.
- **threat modelling**: abuse nobody designed against. Assets, entry points, and abuse cases listed with the security reviewer before the build.
- **performance**: a page or route outside its budget. Lighthouse on staging for the frontend; route latency against the backend budget.

## Deploy

Run while a new version goes out, before users depend on it.

- **integration**: parts that work alone and fail together, such as a query against the real schema. pytest on a `testcontainers` PostgreSQL before deploy, then the service against its staging database.
- **tap compare**: a new version that answers differently from the old one. The same requests sent to both Cloud Run revisions through their tag URLs, and the responses diffed.
- **load**: failure under many users at once. locust in `test/load/locustfile.py` against staging.
- **shadowing**: a new version failing on real traffic. Real requests mirrored to it and its answers thrown away; needs a proxy, so rarely worth it at this scale.
- **config**: a service that breaks with its deployed settings. `gcloud run deploy --no-traffic --tag canary`, then requests to the tag URL.
- **soak**: leaks that show only after hours. locust at normal load for hours, watching memory and the database connection pool.

## Release

Run while users start to reach the new version.

- **canarying**: a bad release reaching everyone. `gcloud run services update-traffic <service> --to-tags canary=10`, then the canary compared with the current revision.
- **monitoring**: the canary doing worse than the current revision. Error rate and p95 latency per revision in Cloud Monitoring.
- **traffic shaping**: a rollout too fast to stop. Traffic moved in steps, such as 10, 50, then 100 percent, and rolled back with `--to-revisions <previous>=100`.
- **feature flagging**: a feature that must be switched off without a deploy. A flag read at runtime, removed once the rollout is done.
- **exception tracking**: new errors in production. Uncaught exceptions grouped with their traces by Cloud Error Reporting from the Cloud Run logs.

## Post-release

Run against the live system, for as long as it runs.

- **teeing**: behaviour on real requests, replayed offline. Production requests copied to a test system and replayed there.
- **profiling**: where the time and memory actually go. py-spy against a running process; the browser's performance panel for the frontend.
- **logs and events**: what happened on one request. Structured JSON logs in Cloud Logging, queried by request ID.
- **chaos**: a failure the system does not survive. An instance killed, the database connection dropped, or a dependency slowed, on staging first.
- **monitoring**: a live system degrading. Dashboards and alerts on errors, latency, traffic, and saturation, each alert with an owner.
- **A/B**: which of two variants serves users better. Traffic split between them, judged on one metric chosen before the test starts.
- **tracing**: where a slow request spends its time across services. OpenTelemetry spans from the frontend through the API to the database, in Cloud Trace.
- **dynamic exploration**: behaviour nobody specified. A person or an agent explores the live app without a script.
- **real user monitoring**: speed as real users get it. Web Vitals (LCP, INP, CLS) sent from real browsers to an endpoint.
- **auditing**: who did what, and whether anyone checks. The audit trail of sensitive actions, read on a schedule.
- **on-call experience**: an alert that wakes someone and does not help. Each alert says what broke and links its runbook; tested by paging yourself.
