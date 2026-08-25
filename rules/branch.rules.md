---
tags:
  - kind/rule
  - topic/workflow
---

> Up: [[README.md]]

# Branch Standard

> [!important]
> A project picks one of two shapes and says which in its README. Trunk is the default; a project that deploys uses promotion, and then a change moves `dev` > `staging` > `main` through a pull request every time.

## Core Requirement

**A project uses one of two shapes, and it says which one in its README.**

| Shape | Permanent branches | For |
| :- | :- | :- |
| **Trunk** | `main` | A project with no deployment, or one deployed straight from `main` |
| **Promotion** | `dev`, `staging`, `main` | A project with a real deployment that needs a soak period |

Trunk is the default. A staging branch exists to coordinate a deployment window; with no deployment it is ceremony that drifts out of sync.

**A project that deploys uses promotion.** Once something real runs from a branch, a change needs somewhere to be wrong before it is wrong in production.

This standard governs where code lives and how it moves. [[pr.rules.md]] governs what a pull request looks like, and [[commit.rules.md]] governs what a commit message looks like. A promotion follows all three.

## The Branches

| Branch | Lives | Accepts a merge from | Rule |
| :- | :- | :- | :- |
| `main` | Forever | `staging`, or a working branch on a trunk project | What is deployed. Always in a working state |
| `staging` | Forever, on a promotion project | `dev` only | What is being verified before release |
| `dev` | Forever, on a promotion project | A working branch, merged locally | Where work lands first. The default branch |
| `<type>/<description>` | Days, not weeks | Nothing | Branch off `dev`, or off `main` on a trunk project, merge back, delete |

Rules:

1. **`main` always works.** Someone cloning it can install the environment and run the thing. A commit that leaves `main` broken gets fixed or reverted immediately.
2. On a promotion project, all three permanent branches exist from the first push, and `dev` is the default branch on the remote, so a fresh clone lands where work happens and a pull request opened without a base does not default to production.
3. None of the permanent branches is ever deleted, renamed, or force pushed. Force pushing a side branch nobody else has is fine.
4. Nothing but the permanent branches and a `legacy` archive lives on the remote long-term. A working branch pushed for backup is deleted once merged.

### Creating a Missing Branch

A promotion project that has only `main`, or `main` and one of the other two, is not following this standard. The missing branch is always created; it is never treated as optional, and it is never worked around by using the branch above it instead.

1. Create the missing branch before writing any code, not after the change is ready. A change written before the branches exist has nowhere correct to land.
2. Create each branch from the one above it in the promotion path, so all three start identical: `staging` from `main`, then `dev` from `staging`.
3. Never substitute a branch that does exist. A project without `dev` does not get its work committed to `staging` or `main` in the meantime.

```text
git checkout main
git pull
git checkout -b staging
git push -u origin staging
git checkout -b dev
git push -u origin dev
```

Then finish the setup on the remote, because the branches alone do not enforce anything: set `dev` as the default branch and apply the settings in "Branch Protection" below. The project only follows this standard once both are done.

### The legacy Branch

Some repositories carry a branch named `legacy`. It holds the original code as it was before the project was brought onto these standards, or the combined state of a repository that has since been split. Either way it is a historical record, and it is the one permitted exception to the branch list above.

Leave it alone.

1. Never commit to it, never merge it in either direction, and never branch new work off it. It is outside the promotion path entirely.
2. Never delete, rename, or force push it. Its value is that it still shows exactly what was there before.
3. Never open a pull request from it or into it.
4. Reading it is always fine. Check it out to look, run `git log` or `git show` against it, compare a file against it. This restricts writing, not reading. When something in it is still needed, copy that into a working branch off `dev` so the code enters through the normal path.
5. Do not create a `legacy` branch where none exists, with one exception: a combined repository being split, where `legacy` is created once from `main` to freeze the pre-split state before the move, per [[repository.rules.md]].
6. Protect it against a force push and a deletion like the others. An archive that can be overwritten is not an archive.

## Promotion

A change moves in one direction only:

```text
local work > dev > staging > main
```

1. Every change is written on `dev`, or on a working branch merged into `dev`.
2. `dev` is promoted to `staging` by a pull request whose head is `dev` and whose base is `staging`.
3. `staging` is promoted to `main` by a pull request whose head is `staging` and whose base is `main`.
4. A pull request into `main` from anything other than `staging` is closed, not merged. The same applies to `staging` from anything other than `dev`.
5. **Never push directly to `staging` or `main`**, and never merge into them locally and push the result. The pull request is the only way in, and a commit that skips a stage skips the verification that stage exists for.
6. Promote small and often. A promotion that has been waiting a month is not a release, it is a migration.

Because every change enters at `dev` and moves one way, the three branches never diverge and a back merge is never needed. If they do diverge, that is evidence the path was bypassed, and it is fixed by finding what was pushed out of order rather than by merging backward.

**The hotfix is the one path that starts anywhere but `dev`.** It branches from `main`, merges to `main`, and is carried back to `dev` and `staging` in the same session. Carried back later means never, and the next promotion then arrives with a revert nobody intended.

There is no other emergency exception. An urgent fix takes the same path; it moves faster, it does not skip a stage. A fix too urgent to verify on `staging` is a fix that reaches production unverified.

## Working Branches

A working branch is optional, local, temporary, and short lived. Use one for anything that will take more than one commit, anything you might abandon, or whenever more than one change is in progress at once. It is where a change is written, not where the app is run and not where work is stored between sessions.

On a trunk project a one-line typo fix goes straight on `main`. On a promotion project it goes to `dev` like everything else.

### Naming

`<type>/<description>`, where the type is one from the Types table in [[commit.rules.md]].

1. Write it in **English**, the same exception [[commit.rules.md]] makes for a commit message.
2. Lowercase kebab-case after the slash.
3. Name the thing being changed, not yourself and not a ticket number.
4. Keep it short enough to type without looking, and leave out an issue number, a date, and a personal name.

```text
feat/streaming-dataloader
fix/scaler-leak
exp/embedding-dim-sweep
refactor/split-training-loop
```

```text
fix/perbaikan-model      not English
feature/dataloader       wrong type prefix
fix/123                  says nothing
rahfi-branch             named after a person
new-stuff                says nothing
FeatDataLoader           wrong case, no slash
```

### Lifecycle

- Branch off `dev`, or off `main` on a trunk project. Never off `staging`.
- **Merge back as soon as its work runs**, not only when the whole feature is finished. Work that runs at the end of a day is merged that day.
- Delete it once merged, locally and on the remote. The commits are in the permanent branch; the name adds nothing.
- Rebase or squash it however you like. It has never been shared, so its history is yours to tidy. Never rebase it after another clone has pulled it.

> [!warning]
> A branch alive for three weeks is a merge conflict growing in the dark. Merge back within a few days, or the branch becomes the work.

## Local Development Happens on the Default Branch

`dev` on a promotion project, `main` on a trunk one, is the branch the repository sits on. Local development, the local server, and every manual check run from there, never from a working branch.

This keeps local setup simple. There is one branch to check out, one server to start, and one copy of the app that always holds everything written so far.

1. Merge a working branch in as soon as its work runs.
2. Merge before running the local server, before starting another change, and before ending a session.
3. Start the local server only from the default branch, so what is running is what that branch actually contains.
4. Return to it at the end of every session. Never leave a repository checked out on a working branch.
5. Delete a working branch as soon as it is merged, so every name still listed by `git branch` is genuinely unfinished work.

### Check Before Running

> [!warning]
> The failure this prevents is silent. A feature is written on a working branch, the branch is never merged, and the app is later run from `dev`, where that feature does not exist. Nothing errors, because `dev` is still a valid and slightly older copy. The time goes into re-checking the code, the environment, and the database before anyone thinks to check the branch list.

Before starting the local server, confirm the default branch already holds every working branch:

```text
git branch --no-merged dev
```

Every branch listed has work the default branch does not have. Merge it or delete it before running the app. An empty list means the default branch is the complete picture, which is the state a repository should sit in at all times.

When the app is missing something that was definitely written, run that command before debugging anything else. An unmerged local branch is a more likely cause than a bug.

## Merging

- **Merge commit for anything with more than one commit**, so the branch's history stays readable and the merge point is visible.
- **Squash a messy branch** whose intermediate commits are noise: "wip", "fix typo", "actually fix it". Squash into one commit whose message follows [[commit.rules.md]].
- **Rebase onto the base branch** before merging when it has moved, so the history stays linear.
- **Never squash or rebase a promotion.** Either one rewrites the commits and makes the branch diverge from the branch it was promoted from, which breaks the next promotion. A promotion always merges with a merge commit.

## Pull Requests and Approval

On a promotion project there are only two kinds of pull request: `dev` into `staging`, and `staging` into `main`. Both follow [[pr.rules.md]] in full, including the title format and the required Summary, Changes, and Test Plan sections.

1. Title the pull request for the concern of the promotion as a whole. Its single concern is the promotion itself, so the Changes list summarizes the combined effect rather than repeating every commit message in sequence.
2. **A promotion is merged only after a human has approved it**, recorded as a review on the pull request itself. An approval given verbally or in chat does not count, because it does not stay with the change.
3. **An AI assistant, a bot, or an automation never approves a promotion.** An AI may carry out the merge, but only on an explicit, per-instance instruction, and a merge into `main` is authorized separately from one into `staging`. The instruction is the human approval; the AI executes the decision and never supplies it.
4. On a solo project the approval is still recorded explicitly, as a deliberate act of confirming the Test Plan was run.
5. A new commit pushed to the head branch after an approval invalidates that approval. Approve again before merging.
6. Never close a promotion by pushing the merge yourself. The pull request is the record that the stage happened.

## Branch Protection

Configure the repository so the rules above cannot be bypassed by accident. A rule that lives only in this document is a rule someone will skip at two in the morning.

- Block a force push and block deletion on every permanent branch, and on `legacy` where it exists.
- Require a pull request before a merge into `main`, and into `staging` on a promotion project.
- Require at least one approving review on those pull requests.
- Dismiss a stale approval automatically when a new commit is pushed to the head branch.
- Restrict the base and head pairs so `main` accepts only `staging` and `staging` accepts only `dev`.
- Set `dev` as the default branch on a promotion project.
- Do not allow a merge to bypass protection, including for an administrator.

## Experiment Branches

Machine learning produces branches that are questions, not features. Treat them as questions.

- An `exp/` branch is allowed to be abandoned. That is its purpose; most experiments fail and that is information.
- **Record the outcome before deleting an abandoned branch.** The finding lives in [[memory/README.md]] or the project's own notes, not in a branch name nobody will read again. A deleted branch whose result was never written down means the same experiment gets run again next year.
- A successful experiment merges like any other branch.

## Remote

- One remote, `origin`.
- Push work in progress rather than losing a laptop with three days on it. A pushed branch is a backup, not a publication.
- Delete a remote branch when its local branch goes.

## Definition of Done

- The README says which branch shape the project uses, and `main` installs and runs.
- On a promotion project, the three branches exist, `dev` is the default, and any that were missing were created from the branch above them before the work started.
- `legacy`, where present, was not committed to, merged, renamed, deleted, or branched off.
- Every permanent branch is protected against a force push and a deletion.
- The change was written on the default branch or on a working branch merged into it.
- Any working branch is named `<type>/<description>` in English, and was deleted after merging.
- `git branch --no-merged dev` returns nothing, so the default branch holds every change written locally.
- The repository is left checked out on the default branch, and the local server was last run from it.
- On a promotion project, the change reached `main` through `dev` and `staging`, with a pull request and a human approval at each stage, and no stage skipped.
- Every promotion was merged with a merge commit, not a squash or a rebase.
- A hotfix taken straight to `main` was carried back to `dev` and `staging` in the same session.
- An abandoned experiment has its finding written down somewhere durable.

## Do and Do Not

| Do | Do not |
| :- | :- |
| State the branch shape in the README | Leave a reader to infer it from the branch list |
| Create a missing `staging` or `dev` from the branch above it, before writing code | Work on the branch above it while the missing one does not exist |
| Write every change on the default branch first | Commit directly to `staging` or `main` |
| Promote one stage at a time through a pull request | Skip `staging` because a change is small, urgent, or already tested locally |
| Merge a promotion with a merge commit | Squash or rebase a promotion |
| Record the approval on the pull request | Count an approval given in chat |
| Let a human approve and an AI execute | Let a bot or an assistant stand in for the approver |
| Name a branch `<type>/<description>` in English | Name it after a person, an issue number, or in another language |
| Merge a working branch in as soon as its work runs | Keep it unmerged across sessions, or use it to store work |
| Run the local server from the default branch | Run it from a working branch, or leave the repository checked out on one |
| Leave a `legacy` branch exactly as it is, and protect it | Commit to it, merge it, rename it, or branch new work off it |
| Force push a private side branch | Force push any permanent branch, or delete one to start it over |

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This branch standard
4. [[pr.rules.md]]
5. [[commit.rules.md]]
6. [[repository.rules.md]]
7. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Applies To

- [[commit.rules.md]]
- [[pr.rules.md]]
- [[repository.rules.md]]
- [[codes.rules.md]]
