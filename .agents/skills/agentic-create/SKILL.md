---
name: agentic-create
description: Adds a new agent to the roster - validates the name, refuses a role an existing agent already covers, picks the tier, writes .agents/agents/<agent-name>.md from the template, and syncs it into every tool. Use when the owner types /agentic-create <agent-name> [definition], or asks for a new agent.
---

# Create an Agent

Usage: `/agentic-create <agent-name> [definition]`. Run every command from `~/agentic`.

## Steps

1. **Check the name.**

   ```bash
   python scripts/harness/sync_agents.py --can-create <agent-name>
   ```

   A non-zero exit means the name is invalid or taken. Stop, print the script's message, and say which of the two it is. Never pick another name on the owner's behalf.

2. **Read the roster.**

   ```bash
   python scripts/harness/sync_agents.py --roster
   ```

   Compare the new role with every line. A role overlaps when an existing agent already does the same job on the same input, or when the new job is part of an existing one. On an overlap, refuse: name the existing agent, propose extending `.agents/agents/<existing-agent>.md` instead, and stop until the owner chooses.

3. **Complete the definition.** Where it is missing or vague, ask at most three short questions, in one message:
   - What is its one job, and what event launches it?
   - Which tier: deep, build, or fast? Or should I pick one?
   - Which tools does it need: read, search, edit, run, web?

   Then repeat the overlap check of step 2 with the answers.

4. **Pick the tier**, unless the owner named one:

   | Tier | For |
   | :- | :- |
   | `deep` | Research, analysis, architecture, planning, orchestration, independent verification, security, and improving the harness |
   | `build` | Writing code and tests |
   | `fast` | Mechanical work: formatting, lint fixes, renames, regenerating files, syncing documents |

   Take the cheapest tier that does the job well. A hard decision inside a `build` or `fast` job goes to `advisor`; it is no reason to move the agent to `deep`.

5. **Pick the tools**: the smallest set from `read`, `search`, `edit`, `run`, and `web`. Never `delegate`, which only the orchestrator holds. A reviewer or a verifier gets no `edit`.

6. **Write the agent.** Copy `assets/agent.template.md` to `.agents/agents/<agent-name>.md`, and replace every line in angle brackets.
   - Four frontmatter keys and no others: `name`, the same as the file name; `description`, one line that names the trigger; `tier`; and `tools`.
   - The six headings, in the template's order. Delete `## Ask the advisor when` for a `deep` agent, which does not escalate.
   - At most 120 lines. No model name, no date, and no counter: a stable body keeps the prompt cache working.
   - Self-contained: it names the rule files it follows by file name, and carries the lines it cannot work without.
   - Every run ends with a report and one closing JSON object: `status`, `report`, `summary`, `next`.

7. **Sync and check.**

   ```bash
   python scripts/harness/sync_agents.py
   python scripts/harness/sync_agents.py --check
   ```

   On a failed check, fix `.agents/agents/<agent-name>.md` only, and run both again. Never edit a generated file under `.claude/` or `.codex/`, or the generated roster.

8. **List it in the handbook.** Add the name to its tier's row of the Routing table in `AGENTS.md`, so the handbook and the roster agree.

## Output

```text
Created .agents/agents/api-docs-writer.md
Tier: fast    Tools: read, search, edit
Roster: api-docs-writer - writes API.md from the route table after an endpoint changes
Check: passed
```

On a refusal, the output is the reason and the next step instead:

```text
Not created: test-writer overlaps test-designer, which already writes the tests from the acceptance criteria.
Proposal: extend .agents/agents/test-designer.md with the new duty.
```
