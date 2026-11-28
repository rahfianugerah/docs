---
name: agentic-verify
description: Verifies the current diff independently - launches the verifier, the slop-reviewer, and the security-reviewer together, each given only the requirements and the git diff, and reports Pass only when all three pass. Use after a build and before a commit, when the owner types /agentic-verify, or from /agentic-orchestrate at its verify step. The session that wrote the code never grades it.
---

# Verify

Three agents judge the change, each from the requirements and the diff alone. This session gathers those two inputs, launches the agents, and relays their verdicts. It adds no opinion of its own, above all when it wrote the code: the author never grades the work.

## Steps

1. **Find the diff.** The base is `HEAD` for uncommitted work. For committed work it is the commit before the work started: the one the orchestrator recorded, or `git merge-base HEAD main` on a feature branch.

   ```bash
   git diff --stat <base>
   git diff --name-only <base>
   git ls-files --others --exclude-standard
   ```

   A new file that is not yet tracked is missing from `git diff`, so the third command lists those. An empty diff with no new file stops here: report "nothing to verify".

2. **Collect the requirements**, from the first source that has them:
   - the `acceptance` list of the brief the change was built from
   - the requirement codes in `docs/SRS.md` that the change claims, by its task or its request
   - the owner, asked in one line

   Never write requirements from the diff: criteria read off the code pass whatever the code does.

3. **Write one brief**, the JSON object each of the three agents receives:

   ```json
   {"task": "login-otp/T-01", "goal": "Verify the change meets every acceptance criterion", "acceptance": ["FR-AUTH-03", "FR-AUTH-04"], "paths_allowed": ["app/auth/otp.py", "test/auth/test_otp_expiry.py"], "paths_forbidden": [], "verify": "git diff 3f2a1c0; pytest test/auth -q", "reports": []}
   ```

   - `task` is `<request-slug>/<task-id>`, so the reports land under the run's slug.
   - `paths_allowed` lists the changed and new files: the scope each agent reads. None of them edits it.
   - `verify` starts with the `git diff` command, then the project's test command where it has one.
   - `reports` stays empty. Leave out the author's report, summary, commit message, and reasoning, and this conversation.

4. **Launch the three together**, in one message, each with the same brief: `verifier`, `slop-reviewer`, and `security-reviewer`.

5. **Gather the three closing JSON objects**, each with `status`, `report`, `summary`, and `next`. Where one is missing or malformed, relaunch that agent once with the same brief; a second miss counts as `Blocked`.

6. **Decide the verdict**, from the three statuses alone:

   | The three statuses | Verdict |
   | :- | :- |
   | All `Pass` | Pass |
   | Any `Fail` | Fail |
   | No `Fail`, any `Blocked` | Blocked |
   | No `Fail` or `Blocked`, any `Needs Decision` | Needs Decision |

   - Never turn a `Fail` into a Pass: not by rerunning the tests, by arguing with the finding, or by relaunching until an agent passes. A finding that looks wrong goes to the owner, with its report path.
   - A critical security finding goes to the owner at once.

## Output

```text
Verify login-otp/T-01: Fail
verifier           Pass  12 checks ran, 0 failed
slop-reviewer      Fail  comment restates the code at app/auth/otp.py:42
security-reviewer  Pass  no finding
Reports: ~/agentic/report/shop-backend/report-slop-reviewer-to-backend-engineer-login-otp-20261128-09_02_44.md
Next: the agent that built T-01 fixes the slop-reviewer's items
```

List the report path of every agent that did not pass. Inside `/agentic-orchestrate`, the verdict and the three report paths go back to the orchestrator, which routes a fix to the agent that built the task.

## Never

- Grade the change yourself, or add a finding no agent reported.
- Give an agent anything but the requirements and the diff.
- Launch the three one after another when they can start together.
