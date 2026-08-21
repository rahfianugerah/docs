> Up: [[README.md]]

# Branch Standard

> [!important]
> Three branches only. Work happens in `dev`, and promotion runs `dev` > `staging` > `main` through a pull request every time.

## Core Requirement

**A project uses one of two shapes, and it says which one in its README.**

| Shape | Permanent branches | For |
| :- | :- | :- |
| **Trunk** | `main` | A project with no deployment, or one deployed straight from `main` |
| **Promotion** | `dev`, `staging`, `main` | A project with a real deployment that needs a soak period |

Trunk is the default. A staging branch exists to coordinate a deployment window; with no deployment it is ceremony that drifts out of sync.

**A project that deploys uses promotion.** Once something real runs from a branch, a change needs somewhere to be wrong before it is wrong in production.

## The Branches

| Branch | Lives | Rule |
| :- | :- | :- |
| `main` | Forever | What is deployed. Always in a working state. Never force pushed |
| `staging` | Forever, on a promotion project | What is being verified before release. Never force pushed |
| `dev` | Forever, on a promotion project | Where work lands first. Never force pushed |
| `<type>/<description>` | Days, not weeks | Branch off `dev`, or off `main` on a trunk project, merge back, delete |

## Promotion

A change moves in one direction only: **`dev` to `staging` to `main`**, through a pull request at every stage, per [[pr.rules.md]].

- **Never commit straight to `staging` or `main`.** A commit that skips a stage skips the verification that stage exists for.
- **Never merge backwards.** A fix made on `main` is cherry-picked back to `dev` and `staging` in the same session, or the branches diverge and the next promotion carries a revert nobody intended.
- A hotfix branches from `main`, merges to `main`, and is carried back immediately. It is the one path that starts anywhere but `dev`.
- Protect all three against force push and deletion.
- Promote small and often. A promotion that has been waiting a month is not a release, it is a migration.

Rules:

1. **`main` always works.** Someone cloning it can install the environment and run the thing. A commit that leaves `main` broken gets fixed or reverted immediately.
2. **Branch for anything that will take more than one commit**, or anything you might abandon. On a trunk project a one-line typo fix goes straight on `main`; on a promotion project it goes to `dev` like everything else.
3. **Merge back within a few days.** A branch alive for three weeks is a merge conflict growing in the dark.
4. **Delete the branch after merging.** `git branch -d` locally and on the remote. The commits are in `main`; the branch name adds nothing.
5. **Never force push a permanent branch.** Force pushing a side branch nobody else has is fine.

> [!warning]
> A branch alive for three weeks is a merge conflict growing in the dark. Merge back within a few days, or the branch becomes the work.

## Naming

`<type>/<description>`, where the type is one from the Allowed Types table in [[commit.rules.md]].

1. Write it in **English**.
2. Lowercase kebab-case after the slash.
3. Name the thing being changed, not yourself and not a ticket number.
4. Keep it short enough to type without looking.

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
```

## Merging

- **Merge commit for anything with more than one commit**, so the branch's history stays readable and the merge point is visible.
- **Squash a messy branch** whose intermediate commits are noise: "wip", "fix typo", "actually fix it". Squash into one commit whose message follows [[commit.rules.md]].
- **Rebase your branch onto `main`** before merging when `main` has moved, so the history stays linear and readable.
- Never rebase a branch after pushing it somewhere another clone has pulled it.

## Experiment Branches

Machine learning produces branches that are questions, not features. Treat them as questions.

- An `exp/` branch is allowed to be abandoned. That is its purpose; most experiments fail and that is information.
- **Record the outcome before deleting an abandoned branch.** The finding lives in [[memory/README.md]] or the project's own notes, not in a branch name nobody will read again. A deleted branch whose result was never written down means the same experiment gets run again next year.
- A successful experiment merges to `main` like any other branch.

## Remote

- One remote, `origin`. Push `main` and any branch you want backed up off your machine.
- Push work in progress rather than losing a laptop with three days on it. A pushed branch is a backup, not a publication.
- Delete a remote branch when its local branch goes.

## Definition of Done

- `main` installs and runs, and the README says which branch shape the project uses.
- On a promotion project, every change reached `main` through `dev` and `staging`, and no permanent branch was force pushed.
- The branch is named `<type>/<description>` in English.
- The branch is merged and deleted, locally and on the remote.
- An abandoned experiment has its finding written down somewhere durable.
- `main` was never force pushed.

## Applies To

- [[commit.rules.md]]
- [[pr.rules.md]]
- [[codes.rules.md]]
