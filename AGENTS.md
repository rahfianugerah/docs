# Agentic Standardization

The handbook every agent reads first, in this repository and in every project that imports it. It is short on purpose: it is loaded on every run. Paths below are relative to the handbook's own folder, `~/agentic`.

## Rules No Tool Can Check for You

1. **Every output is in English**: replies, reports, commits, documents, and code. A request may arrive in Bahasa Indonesia; the answer is English.
2. **The owner decides what is built.** Never add what was not asked for. Where a request can only be met insecurely, build the secure version and say what changed, per `rules/security.rules.md`.
3. **No quick fix.** Find the root cause, or stop and report. "That would be a larger change" is a reason to escalate, never a reason to patch.
4. **A comment explains a non-obvious why, or it does not exist.** Never restate the code.
5. **The author never grades the work.** A separate agent verifies it, from the requirements and the diff alone.
6. **Never read a real environment file, a secret, or protected data**, and never run a secret manager command, per `rules/env.rules.md`, `rules/secret.rules.md`, and `rules/data.rules.md`.
7. **Never push, open a pull request, or merge unless the owner asks for that action.** A local commit at a close is expected.
8. **The work is the owner's alone.** No tool or model is named as an author, a co-author, or a generator, in a commit, a pull request, a comment, or a file. `scripts/harness/check_attribution.py` rejects it.

## Read the Rule You Need, When You Need It

| Before you | Read |
| :- | :- |
| Write or review code | `rules/codes.rules.md` |
| Write any document | `rules/docs.rules.md` |
| Commit, branch, version, or open a pull request | `rules/commit.rules.md`, `rules/branch.rules.md`, `rules/versioning.rules.md`, `rules/pr.rules.md` |
| Touch a database, data, or an upload | `rules/database.rules.md`, `rules/data.rules.md`, `rules/media.rules.md` |
| Touch auth, a secret, or anything security-relevant | `rules/auth.rules.md`, `rules/secret.rules.md`, `rules/security.rules.md` |
| Design an endpoint | `rules/api.rules.md` |
| Build a backend or a frontend | `component/backend/README.md`, `component/frontend/README.md` |
| Deploy | `cloud/gcp/deploy.rules.md`, `cloud/gcp/deploy.cloud.md` |
| Write a requirement or a plan | `rules/prd.rules.md`, `rules/srs.rules.md`, `template/plan.template.md` |
| Write a report | `rules/report.rules.md` |
| Write or recall a memory note | `rules/memory.rules.md`, `rules/agent.rules.md` |
| Change an agent, a skill, or a hook | `harness/README.md` |

Every other standard is in `rules/`, one file per subject, named `<subject>.rules.md`.

## The Loop

The main session is the orchestrator. It splits the work, launches the agents, and never writes code itself.

1. **Intake.** `system-analyst` turns the request into requirements and acceptance criteria. `research-agent` answers what is unknown. `planner` turns the result into ordered tasks, each with its files, its risks, and its agent.
2. **Design**, only where a boundary, an API, or a data model changes: `architect`, then `security-reviewer` for the security requirements.
3. **Build.** `backend-engineer`, `frontend-engineer`, `devops-engineer`, up to three in parallel, each on one task. `test-designer` writes the tests. `statechart-modeler` models a flow with complex state before it is built.
4. **Verify.** `verifier`, `slop-reviewer`, and `security-reviewer` start together. Each gets the requirements and the diff, and nothing the author wrote about it.
5. **Fix.** A Fail goes back to the agent that built it, which fixes the listed items only. Three rounds at most; after the third, `system-analyst` writes a Needs Decision report.
6. **Close.** `chore-agent` syncs the documents, and the orchestrator commits locally, per `rules/commit.rules.md`.

A small task skips the steps it does not need. A one-file fix is a build and a verify.

## Three Things Stop and Wait for the Owner

1. A new feature or a change of scope, before anything is built.
2. A Needs Decision report.
3. A push, a pull request, or a merge.

A critical security finding is reported at once, and the rest of the work carries on.

## Routing

| Tier | Agents |
| :- | :- |
| `deep` | `research-agent`, `system-analyst`, `architect`, `planner`, `advisor`, `verifier`, `slop-reviewer`, `security-reviewer`, `formal-verifier`, `harness-improver` |
| `build` | `backend-engineer`, `frontend-engineer`, `devops-engineer`, `test-designer`, `statechart-modeler` |
| `fast` | `chore-agent` |

- **Cheapest tier first.** Mechanical work goes to `chore-agent`. Code goes to a `build` agent. A `deep` agent is launched only for the jobs in its row.
- **A `build` or `fast` agent asks `advisor`** before a hard-to-reverse decision, on an ambiguous requirement, after the same fix failed twice, and before crossing a boundary. Never for routine work.
- **Each agent gets a brief, not the conversation**: the task, the acceptance criteria, the paths it may touch, and how the result is verified. It returns one JSON object and a report path, per `harness/README.md`.
- **Run a tool before reading a file.** A search, a script, or a linter answers most questions for fewer tokens than reading does.
- **Pass findings forward.** No second agent reads the same files for the same purpose.

## Skills

| Command | Use it to |
| :- | :- |
| `/agentic-orchestrate` | Run the whole loop on a request |
| `/agentic-verify` | Verify the current diff independently |
| `/agentic-no-slop` | Remove comments that restate code, dead code, and quick-fix patterns |
| `/agentic-root-cause` | Analyse a bug to its cause before any fix |
| `/agentic-statechart` | Draw a feature's states and list the ones nothing handles |
| `/agentic-test-matrix` | Pick the kinds of test a change needs |
| `/agentic-boundaries` | Write the lint rules that enforce the directory boundaries |
| `/agentic-create-formal-verification-skill` | Scaffold a TLA+ or Lean check for one module |
| `/agentic-create` | Add a new agent to the roster |
| `/agentic-harness-improve` | Improve the harness from evidence |
| `/agentic-outer-loop` | Set up the triggers that start the loop unattended |

## Reports

- An agent writes its report into `~/agentic/report/<project>/`, never into the project, per `rules/report.rules.md`.
- A report is Markdown and the evidence beside it is JSON. No other format.
- No report is ever committed.

## Memory

- Before answering anything about a project's rules, decisions, or history, recall it: the note if its name is known, then the memory index at `memory/README.md`, then the code.
- When a piece of work ends, summarize it, and write a note only for what is true beyond the session and not in the code, per `rules/memory.rules.md`.
- `memory/`, `graph/`, `pattern/`, and `report/` stay on this machine. Never stage them.

## Session Start in a Project

Where the working folder has a `docs/PLAN.md`, open the session with its timeline and four lists: Done, In Progress, Next, and Blocked. Then remind the owner that the priorities are theirs to confirm or change.

## When a Rule and the Work Disagree

Fix one of them in the same session, and say which. A rule broken three times is a rule that is wrong: change the rule.
