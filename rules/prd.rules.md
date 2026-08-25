---
tags:
  - kind/rule
  - layer/docs
  - topic/workflow
---

> Up: [[README.md]]

# PRD Standard

> [!important]
> Every project starts from a PRD, written before the code. It states the problem and the non-goals, and never contains solution design.

## Core Requirement

**Every project has a `PRD.md`, and it is written before the code.** No feature is built without one, and no repository exists without one.

A PRD says what is being built, for whom, and why. It does not say how; that is the technical decision, and it belongs in the code, the API document, and the runbook.

The point is not process. It is that the most expensive mistake is not a bug, it is a feature nobody needed, built correctly, deployed properly, and used by no one. A PRD is the cheapest place to find that out, because it costs an hour rather than a sprint.

## Where It Lives

- One `PRD.md` in the repository root, beside the `README.md`.
- Written in the language its readers use, because its readers are whoever asked for the project. The eight sections and their order do not change with the language; only the headings are translated.
- Committed and versioned like any other document. It is not a chat message, not a spreadsheet, not a screenshot of a chat thread.
- A frontend and a backend that serve one app share the app's PRD. Put it in the backend repository and link to it from the frontend README, so the product intent is not split in half by a repository boundary, per [[repository.rules.md]].

## When It Is Written

| Situation | What is required |
| :- | :- |
| A new project | A full `PRD.md` before the first feature commit |
| A significant feature in an existing project | A new section in that project's `PRD.md`, before the branch is cut |
| A bug fix, a refactor, a dependency bump | Nothing. A PRD describes intent, and these change none |
| A change the owner asked for verbally | The PRD section first, then the code. The verbal ask is the input, not the record |

**The test for whether a change needs a PRD section:** would somebody, in six months, be able to tell from the code alone *why* this exists? If not, it needs a section. If yes, it does not.

## What It Contains

Eight sections, in this order. Every one is required, and the shortest useful answer is the right length.

```markdown
# PRD: [Project or Feature Name]

## Problem
[What happens today, who it hurts, and what it costs. Not "we need feature X".]

## Users
[Which team, which role, how many people. Name the ones who will use it every day.]

## What Is Built
[What a user will be able to do once this exists. Written as a capability, not as a screen.]

## What Is Not Built
[An explicit list of what is deliberately left out, and why.]

## Success Measure
[How we know this worked. A number or a behavior somebody can check, not "more efficient".]

## Constraints
[What cannot change: the data source, a business rule, compliance, a deadline.]

## Data
[What data is read and written, where it comes from, and whether any of it is personal.]

## Open Questions
[What is undecided, and who has to decide it.]
```

Header fields sit above the first section: the owner as a named person, the date, and a status of `Draft`, `Approved`, or `Done`.

## The Sections That Do the Work

Four of the eight carry almost all the value, and they are the four most often left thin.

**Problem, written as a problem and not as a solution.** "The team loses three days a month rebuilding a list of expiring contracts out of five spreadsheets" is a problem. "We need a contract dashboard" is a solution with the problem removed, and it forecloses every cheaper answer before anyone has looked.

**What Is Not Built is mandatory and is the most valuable section in the document.** It is where scope creep dies. An empty non-goals list means the scope was never bounded, and every conversation from then on can add to it without anyone noticing. Write down the obvious adjacent things and say no to them explicitly: no mobile app in this phase, no spreadsheet export, no approval workflow.

**Success Measure has to be checkable.** "Faster" is not a measure. "The monthly rollup finishes in one day instead of three" is. If nobody can say afterwards whether it worked, nobody will, and the next request for the same area starts from zero.

**Users names real people, not a role in the abstract.** A project for "management" is a project with no one to ask when a decision is needed. A project for "four people on one team, used daily by two of them" has a person to sit with.

## What It Must Not Contain

- **No solution design.** No schema, no endpoint list, no component tree, no library choice. Those live in the code, in `API.md`, and in the standards under [rules/](../rules/) and [component/](../component/). A PRD that specifies a table layout has stopped being a PRD and started being an argument about implementation.
- **No estimate presented as a commitment.** A date belongs in Constraints only when something external actually depends on it.
- **No real secret, credential, or configuration value**, per [[secret.rules.md]].
- **No personal data as an example.** Use an obviously fake placeholder identifier, never a real person's record, per [[security.rules.md]].
- **No feature with no named owner.** If nobody owns it, it is not ready to be built.

## Keeping It True

**A PRD is a living document, not a gate that swings once.** It is written before the code and updated whenever reality moves, in the same commit that moves it.

- When scope changes, the PRD changes first. A feature built beyond its PRD is a feature nobody agreed to.
- When something moves from What Is Built to What Is Not Built, say so and say why. That line is the record of a decision.
- When an open question is answered, move the answer into the section it belongs to and delete the question.
- When a feature ships, set its status to `Done`. A PRD full of `Draft` sections tells a reader nothing about what actually exists.
- A PRD that contradicts the running project is worse than no PRD, because it is believed. If they disagree, fix one of them in the same session.

## For an Agentic Session

An agentic coding tool reads the PRD before it writes code, and this is where it matters most: a model given a task with no PRD will infer the intent, build something coherent, and be confidently wrong about why.

- Read `PRD.md` before starting a feature. If the repository has none, say so and offer to draft one rather than inferring the intent from the code.
- Where the ask exceeds the PRD, name the gap before building. The PRD section comes first.
- A PRD drafted by an agent is a draft. It is not approved until the named owner says so, and `Draft` stays in the status field until then.
- A durable decision from a PRD conversation, especially a rejected approach, belongs in the memory too, per [[agent.rules.md]].

## Definition of Done

- The repository has a `PRD.md` in its root, in the readers' language, with a named owner and a status.
- All eight sections are present, and What Is Not Built is not empty.
- Problem describes a problem rather than a solution.
- Success Measure is something a person can actually check afterwards.
- No schema, endpoint list, or library choice appears anywhere in it.
- No secret, no real configuration value, and no real personal data appears anywhere in it.
- The PRD matches what the project actually does today, or the difference is recorded.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This PRD policy
4. [[docs.rules.md]]
5. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[docs.rules.md]]
- [[repository.rules.md]]
- [[pr.rules.md]]
- [[agent.rules.md]]
- [[security.rules.md]]
- [[secret.rules.md]]
