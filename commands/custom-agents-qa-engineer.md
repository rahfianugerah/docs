---
description: Run only the qa-engineer agent - writes and runs every test, and approves or rejects
argument-hint: "<task>"
---
Launch the `qa-engineer` subagent with the Agent tool, and only that agent. Its skill is `~/docs/agents/qa-engineer/SKILL.md`.

The task may be written in Bahasa Indonesia or in English. Take it as written, make the request slug English, and have everything written into the project in English, the language of every personal project, per `~/docs/rules/docs.rules.md`.

Pass it, from $ARGUMENTS and the project:

- the request, as written
- a request slug: kebab-case, 2 to 6 words, taken from the request
- the feature IDs and the files it owns, where the request or `docs/PLAN.md` names them
- the paths of related reports in `report/`

When it returns, read its report and tell me in Bahasa Indonesia: the status, the findings, and the Next Action it named. **Do not launch that next agent**: this command runs one agent only. Do not test or re-check its work yourself.

If $ARGUMENTS is empty, ask me what the qa-engineer should work on.
