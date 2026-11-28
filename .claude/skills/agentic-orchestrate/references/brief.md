# The Brief

Every agent receives one JSON object and nothing else. Apart from its own agent file, the brief is its whole context, so write it as if for a stranger: someone who has never seen the conversation can do the task from it.

## Format

```json
{"task": "login-otp/T-01", "goal": "Reject an expired OTP", "acceptance": ["FR-AUTH-03"], "paths_allowed": ["app/auth/"], "paths_forbidden": ["app/billing/"], "verify": "pytest test/auth -q", "reports": []}
```

| Key | Holds | Rule |
| :- | :- | :- |
| `task` | `<request-slug>/<task-id>` | The slug names every report of the run; the ID matches the plan. A fix keeps the task's ID |
| `goal` | One sentence: the outcome | An outcome, not steps. "Reject an expired OTP", not "edit otp.py" |
| `acceptance` | Requirement codes, or short statements | Each can be checked true or false. Codes from `docs/SRS.md` where the project has one |
| `paths_allowed` | The paths the agent may change | As narrow as the task allows. For a reviewer, the changed and new files: the scope it reads, never edits |
| `paths_forbidden` | The paths it must not touch | Name a sibling's paths whenever parallel agents work near each other |
| `verify` | The command that proves the result | Runnable as written. For a reviewer, the `git diff` command first, then the test command |
| `reports` | Paths of earlier reports the agent needs | Paths only, never their text. Always empty for a reviewer |

## By Role

- **Intake** (`system-analyst`, `research-agent`, `planner`): `goal` is the request restated in English. `acceptance` says what the output must contain, such as "every requirement numbered and checkable". `paths_allowed` is `docs/`.
- **Build** (`backend-engineer`, `frontend-engineer`, `devops-engineer`, `test-designer`, `statechart-modeler`): one task per brief. `test-designer` works from the acceptance criteria, never from the builder's code or report, so it can run beside the builder.
- **Verify** (`verifier`, `slop-reviewer`, `security-reviewer`): the same brief for all three. `task` names the wave, such as `login-otp/W-1`, `acceptance` is copied from the build briefs, `verify` starts with `git diff <base-commit>`, and `reports` is empty. Nothing the author wrote about the change goes in.
- **Fix**: the builder's own brief with the same `task`, the goal "Fix the items listed in the report, and nothing else", and the failing report's path in `reports`.
- **Close** (`chore-agent`): the goal names the documents to sync, such as the Done log in `docs/PLAN.md`, and `paths_allowed` lists only those documents.

## Before Launching

- The brief is one valid JSON object, with the seven keys and no others. For an agent with no `run` tool, such as `system-analyst`, `planner`, or `architect`, the brief adds an eighth key, `report`: the path to write its report to, because that agent cannot take the timestamp from the clock itself.
- No path appears in the `paths_allowed` of two briefs launched in parallel.
- No secret, token, or real environment value appears anywhere in it.
- A reviewer's brief holds the requirements and the diff command, and nothing else.

## Worked Example

The owner asks: "OTP login should reject codes older than five minutes." The project is `shop-backend`, the slug is `login-otp`, and the base commit is `3f2a1c0`. The SRS already holds the requirement, so it is a feature inside the existing boundaries with no intake: build, verify, fix, close.

**Build.** The orchestrator launches both tasks in one message, since neither depends on the other:

```json
{"task": "login-otp/T-01", "goal": "Reject an OTP older than five minutes at login", "acceptance": ["FR-AUTH-03", "FR-AUTH-04"], "paths_allowed": ["app/auth/otp.py"], "paths_forbidden": ["test/", "app/billing/"], "verify": "pytest test/auth -q", "reports": []}
```

```json
{"task": "login-otp/T-02", "goal": "Write the tests that prove FR-AUTH-03 and FR-AUTH-04", "acceptance": ["FR-AUTH-03", "FR-AUTH-04"], "paths_allowed": ["test/auth/test_otp_expiry.py"], "paths_forbidden": ["app/"], "verify": "pytest test/auth/test_otp_expiry.py -q", "reports": []}
```

Both return `Done`. The orchestrator reads only the JSON:

```json
{"status": "Done", "report": "~/agentic/report/shop-backend/report-backend-engineer-to-verifier-login-otp-20261128-08_40_11.md", "summary": "expiry check added to verify_otp", "next": "verifier"}
```

**Verify.** One brief, sent to the three reviewers in one message:

```json
{"task": "login-otp/W-1", "goal": "Verify the change meets every acceptance criterion", "acceptance": ["FR-AUTH-03", "FR-AUTH-04"], "paths_allowed": ["app/auth/otp.py", "test/auth/test_otp_expiry.py"], "paths_forbidden": [], "verify": "git diff 3f2a1c0; pytest test/auth -q", "reports": []}
```

The `verifier` and the `security-reviewer` return `Pass`. The `slop-reviewer` returns:

```json
{"status": "Fail", "report": "~/agentic/report/shop-backend/report-slop-reviewer-to-backend-engineer-login-otp-20261128-09_02_44.md", "summary": "comment restates the code at app/auth/otp.py:42", "next": "backend-engineer"}
```

**Fix, round 1.** The status is `Fail`, so the path goes forward; the orchestrator does not need to open the report to route it:

```json
{"task": "login-otp/T-01", "goal": "Fix the items listed in the report, and nothing else", "acceptance": ["FR-AUTH-03", "FR-AUTH-04"], "paths_allowed": ["app/auth/otp.py"], "paths_forbidden": ["test/", "app/billing/"], "verify": "pytest test/auth -q", "reports": ["~/agentic/report/shop-backend/report-slop-reviewer-to-backend-engineer-login-otp-20261128-09_02_44.md"]}
```

The builder returns `Done`, and only the `slop-reviewer` runs again, with the verify brief on the new diff. It passes.

**Close.** `chore-agent` adds T-01 and T-02 to the Done log in `docs/PLAN.md`. The orchestrator makes three local commits, one per task and one for the documents, records the usage, and tells the owner the push is waiting for them.
