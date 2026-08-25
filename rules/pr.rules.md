---
tags:
  - kind/rule
  - topic/workflow
---

> Up: [[README.md]]

# Pull Request Standard

> [!important]
> A pull request carries a Summary, a Changes list, and a Test Plan. Merging into `staging` or `main` requires explicit permission, every time.

## Core Requirement

A pull request is a written record of why a change happened. On a personal project it has no reviewer, which changes who it is for but not whether it is worth writing: **the reader is you, later, asking why the code looks like this.**

It sits directly next to the commit history it merges, so it follows the same discipline as [[commit.rules.md]]. This applies to every pull request, including a one-line fix and a configuration change.

## AI Authorization to Open and Merge

> [!danger] This is the most important rule in this standard
> An AI assistant may open a pull request, and may merge one into `staging` or into `main`, only when the user has explicitly told it to, for that specific action, in that specific instance. If the user says it may, it may. If the user says it may not, it may not. There is no third case.

### The Default Is No

- Silence is not permission. Having write access is not permission. Being mid-task is not permission.
- Finishing the work is not permission to ship it. An AI that has just written and committed a change has no standing to open a pull request for it, and no standing to merge one.
- Permission is **per action and per instance**. Authorization to merge this pull request is not authorization to merge the next one, and permission given yesterday does not carry into today.
- Permission to **open** a pull request is not permission to **merge** it. They are two separate acts and each needs its own instruction.
- Permission to promote `dev` into `staging` is **not** permission to promote `staging` into `main`. The second releases to production and always requires its own explicit authorization, per [[branch.rules.md]].
- An instruction that could plausibly mean something else is not permission. Ask, and do nothing until the answer arrives.

### When the User Says No

Stop. Do not open the pull request, do not merge, and do not do a smaller version of the thing that was refused.

- Do not open the pull request anyway "so it is ready to merge".
- Do not merge into `staging` when `main` was refused.
- Do not ask again in the same turn, and do not reframe the request hoping for a different answer.
- Report what was left undone, and leave the work where the user can act on it themselves.

### The User's Yes Is the Human Approval

[[branch.rules.md]] requires an approving review from a human before any promotion is merged, and states that an AI never approves a promotion. This rule does not weaken that one.

The user's explicit instruction **is** that human approval. The AI carries the decision out; it never supplies the decision. The accountable party is the person who said yes, which is exactly why the instruction has to be explicit rather than assumed.

It follows that an AI must never:

- Approve a pull request through a review, including one it did not open.
- Use an administrator override, a force merge, or any path that bypasses branch protection.
- Merge a pull request whose required approval is missing, on the grounds that it was told to merge.
- Mark a Test Plan item as verified when it did not actually run that step. Reporting an unrun check as passed is a fabrication, and it is worse here than anywhere else because the Test Plan is what the approval is given against.

### When Something Blocks the Merge

Permission to merge is permission to merge cleanly. If a conflict appears, CI fails, a required check is missing, or branch protection rejects the merge, **stop and report it**. Do not work around it, do not retry with a different method, and do not disable the check. The permission covered the merge, not the removal of whatever prevented it.

### Attribution Is Unchanged

An AI that opens or merges a pull request still records no attribution of any kind, per "No Tool or AI Attribution" below. The pull request belongs to the person accountable for the change. The AI may act on an instruction, and it never signs the work.

## When to Open One

Not every change needs a pull request. Use judgement, and default to the cheaper option.

| The change | Do this |
| :- | :- |
| A typo, a comment, a version bump | Commit straight to the default branch |
| A small fix, one or two commits | Merge the branch directly, no PR |
| A feature, a refactor, a migration | Open a PR |
| An experiment worth remembering | Open a PR, even if you merge it yourself a minute later |
| Anything you might want to find again in a year | Open a PR |
| A promotion on a promotion-shape project | Always a PR, per [[branch.rules.md]] |

> [!tip]
> Open a PR when the reasoning matters more than the diff. A PR is searchable prose attached to a change, which is the one thing git history is bad at.

## Relationship to the Commit Standard

This standard reuses the type list, the scope rules, and the terminology already defined in [[commit.rules.md]]. It does not define a second set of types or a second set of scopes.

A pull request that would need a type not on that table, or more than one scope, covers more than one concern and must be split, the same as a commit would.

## Language

Titles and descriptions are written in **English**, the same exception [[commit.rules.md]] makes for commit messages and for the same reason: a pull request is consumed by hosting platforms and release tooling that expect it, and it sits next to a history already written in English.

Technical terms, library names, framework names, command names, file names, variable names, database field names, and route paths keep their original form.

## Title

Same structure as a commit description:

```text
<type>[optional scope]: <description>
```

1. The type is required, lowercase, and from the Types table in [[commit.rules.md]].
2. The scope is optional and follows the Scope rules there: a single lowercase noun, no file path, reused from what the project already uses for that area.
3. A `!` immediately before the colon marks a breaking change.
4. The description is imperative, starts lowercase unless the first word is a proper noun, has no trailing period, and stays at 72 characters or fewer.
5. No issue number in the title. Use the Related Issues section.
6. When a pull request carries several commits, the title describes its overall concern. Do not concatenate two types or two scopes into one title.

Correct:

```text
feat(loader): add a streaming reader for the parquet dataset
exp(model): sweep the embedding dim from 128 to 512
fix(auth): reject an expired refresh token
```

Incorrect, past tense, capitalized, trailing period:

```text
fix(auth): Fixed a bug with tokens.
```

Incorrect, more than one concern:

```text
feat(dashboard)+fix(api): add graphics and fix pagination
```

## Description Structure

Four sections, in this order. Omit Results on anything that is not an experiment, and omit Related Issues when there is nothing to reference. Never omit Summary, Changes, or Test Plan.

```text
## Summary

<one or two sentences: what this does and why>

## Changes

- <one item per change, imperative, explaining the effect>

## Results

<experiments only: the metric, the baseline, the parameters, the seed>

## Test Plan

- [ ] <how you verified it, or why testing does not apply>

## Related Issues

[optional]
```

### Summary

One or two sentences stating what the pull request does and why, the same distinction [[commit.rules.md]] draws for a commit description: state what changes, not the sequence of things that were tried.

### Changes

The Changes section follows the same Body rules [[commit.rules.md]] sets for a commit message:

1. A flat bullet list, using `-`. Never `*`, `+`, or a numbered list.
2. One item per change. Three concerns means at least three items.
3. Start each item with a capital letter and an imperative verb.
4. No trailing period.
5. Explain the change and its purpose or effect in the same item, so a reviewer does not need to open the diff.
6. No nested list.
7. Never list a file name alone. Describe the change, and name the file only when it adds clarity.

When a pull request is a single commit, the Changes list may mirror that commit's body. When it bundles several, the list summarizes the combined effect; it is not a copy of every commit message in sequence.

Correct:

```text
## Changes

- Add a monthly revenue line chart so the numbers can be compared without exporting data
- Add a headcount bar chart to replace the manual spreadsheet report
- Add a shared chart color palette so every chart on the page uses the same series colors
```

Incorrect, file names with no explanation:

```text
## Changes

- Dashboard.tsx
- charts/RevenueChart.tsx
```

### Results

Experiments only, and this is the section that makes a PR worth opening on an ML project.

State the metric, the baseline it beat or failed to beat, the parameters that changed, the seed, and the data version. A result without those cannot be reproduced and is not a result.

```text
## Results

- Macro F1 0.81, baseline 0.78, same 5-fold split, seed 42
- Changed: embedding dim 256 > 512, everything else held
- Data: dataset v3, 12,400 rows
- Cost: training time 4m > 11m, which is the trade being accepted
```

**Record a negative result too.** An experiment that failed is worth a merged-or-closed PR saying so, because the alternative is running it again next year having forgotten.

### Test Plan

A Test Plan is required on every pull request. State how the change can be verified, as a bullet list or a task list:

```text
## Test Plan

- [ ] Run the existing test suite and confirm it passes
- [ ] Log in and confirm the revenue chart renders with real data
```

When testing genuinely does not apply, state that directly instead of leaving the section empty:

```text
## Test Plan

Documentation only, no runtime behavior to verify
```

### Related Issues

Use only the footer tokens permitted by [[commit.rules.md]], one per line.

| Token | Use for | Example |
| :- | :- | :- |
| `Refs` | An issue, a ticket, or a commit SHA | `Refs: #123` |
| `Closes` | An issue this closes | `Closes: #123` |
| `Reviewed-by` | The reviewer | `Reviewed-by: A Person` |
| `Co-authored-by` | An additional human author | `Co-authored-by: A Person <person@example.com>` |

Do not use a token that is not on this table.

## No Tool or AI Attribution

A pull request records what changed and why, not which tool was used to write it, the same principle [[commit.rules.md]] states for a commit.

Never add, in a title, a description, or a comment:

- A `Co-authored-by` line naming an AI assistant, a model, or a bot
- A "generated with", "created with", or "written with" line of any kind
- A tool name, an assistant name, a model name, or a product link used as attribution
- A tool signature or watermark anywhere in the pull request

`Co-authored-by` is reserved for a human who worked on the change.

## Breaking Changes

Same definition [[commit.rules.md]] uses: any change that forces a consumer to change something.

1. Mark the title with a `!` before the colon.
2. Add a `BREAKING CHANGE` line to the Changes section, in uppercase, stating what breaks and what a consumer must do instead.
3. `BREAKING-CHANGE` is an accepted synonym.

```text
## Changes

- Add header validation to every report endpoint, so an unauthenticated request is rejected
- Remove the anonymous read path the internal dashboard used

BREAKING CHANGE: every report endpoint now requires an Authorization header. A client without
a token receives a 401.
```

## One Concern Per Pull Request

- A change that fits two types is two pull requests. Do not pick one and hide the rest in the description.
- Do not mix a refactor with a fix, or a formatting pass with a feature.
- A change across many files serving one concern is still one pull request.
- Use a branch per [[branch.rules.md]] for the underlying work.
- A pull request carrying a feature names the PRD section it implements, per [[prd.rules.md]]. A feature with no PRD section is a feature nobody agreed to.
- A promotion satisfies this rule: its one concern is the promotion itself, and its Changes list summarizes the combined effect.

## Formatting Restrictions

Every restriction in [[docs.rules.md]] and [[commit.rules.md]] applies in full: no emoji, no em dash, no arrows, no smart quotes, no decorative divider, no extra blank lines for spacing, no trailing period on the title or a list item, and no ALL CAPS except the `BREAKING CHANGE` token.

The `##` headings that lay out Summary, Changes, Results, Test Plan, and Related Issues are this standard's required structure and are not a prohibited decoration.

## Security and Privacy

- Never put a credential, a token, a password, a connection string, or a real environment value in a title, description, or comment.
- Never put personal data, such as a national identity number, a phone number, or a user's email address, in a pull request. A `Co-authored-by` footer for a collaborator is permitted.
- Reference a secret by its variable name only, such as `DATABASE_URL`, per [[env.rules.md]] and [[secret.rules.md]].
- Never attach a screenshot or a log excerpt that exposes a secret, a token, or personal data.

## Definition of Done

- The title is in English, follows `<type>[scope]: <description>`, is 72 characters or fewer, and has no trailing period.
- The type is on the allowed list in [[commit.rules.md]] and is lowercase.
- The scope, when present, is a single lowercase noun matching the scope already used for that area.
- Summary, Changes, and Test Plan are all present.
- Changes is a flat `-` list where every item explains its purpose or effect.
- The Test Plan states how the change was or can be verified, or states why testing does not apply.
- An experiment records the metric, the baseline, the parameters, the seed, and the data version.
- A breaking change is marked with `!` and a `BREAKING CHANGE` line.
- Related Issues, when present, uses only a permitted token.
- No tool, AI, model, or bot attribution appears anywhere.
- The pull request covers one logical concern.
- A promotion carries an approving review from a human before it is merged, per [[branch.rules.md]].
- No emoji, prohibited character, or decorative divider is present.
- No secret, credential, or personal data is present.
- When an AI opened or merged it, the user explicitly authorized that specific action, and authorization for a merge into `main` was given separately from any authorization for `staging`.
- No Test Plan item is marked verified unless that step was actually run.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. The AI authorization rule above. An AI opens or merges a pull request only on an explicit, per-instance instruction, and never approves one
3. Direct user instructions
4. This pull request standard
5. [[commit.rules.md]]
6. Existing project conventions

A direct user instruction must not override security or privacy requirements.

The AI authorization rule sits above direct user instructions in one direction only: a user can always withhold or refuse permission, and no instruction grants an AI standing to approve its own promotion or to bypass branch protection. A user granting permission for a specific merge is the rule working as intended, not an override of it.

## Applies To

- [[branch.rules.md]]
- [[commit.rules.md]]
- [[docs.rules.md]]
- [[prd.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
