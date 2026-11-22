---
description: Run only the system-analyst agent - problem analysis and solution design
argument-hint: "<the task, feature IDs, or a report path>"
---
Launch the `system-analyst` subagent with the Agent tool, and only that agent. Its skill is `~/docs/agents/system-analyst/SKILL.md`.

Pass it, from $ARGUMENTS and the project:

- the request, as written
- a request slug: kebab-case, 2 to 6 words, taken from the request
- the feature IDs and the files it owns, where the request or `docs/PLAN.md` names them
- the paths of related reports in `report/`

When it returns, read its report and tell me in Bahasa Indonesia: the status, the findings, and the Next Action it named. **Do not launch that next agent**: this command runs one agent only. Do not test or re-check its work yourself.

If $ARGUMENTS is empty, ask me what the system-analyst should work on.
