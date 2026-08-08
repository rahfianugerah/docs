> Up: [[README.md]]

# Branch Standard

## Core Requirement

**`main` is the only permanent branch.** It always works. Everything else is a short-lived branch that merges into it and is deleted.

This is trunk-based development, and it is the right shape for a personal project. A staging branch and a release train exist to coordinate a team and a deployment window; with one developer they are ceremony that slows you down and drifts out of sync.

If a project later grows a real deployment that needs a soak period, add the branch then. Not before.

## The Branches

| Branch | Lives | Rule |
| :- | :- | :- |
| `main` | Forever | Always in a working state. Never force pushed |
| `<type>/<description>` | Days, not weeks | Branch off `main`, merge back, delete |

Rules:

1. **`main` always works.** Someone cloning it can install the environment and run the thing. A commit that leaves `main` broken gets fixed or reverted immediately.
2. **Branch for anything that will take more than one commit**, or anything you might abandon. A one-line typo fix goes straight on `main`; there is nobody to coordinate with.
3. **Merge back within a few days.** A branch alive for three weeks is a merge conflict growing in the dark.
4. **Delete the branch after merging.** `git branch -d` locally and on the remote. The commits are in `main`; the branch name adds nothing.
5. **Never force push `main`.** Force pushing a side branch nobody else has is fine.

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

- `main` installs and runs.
- The branch is named `<type>/<description>` in English.
- The branch is merged and deleted, locally and on the remote.
- An abandoned experiment has its finding written down somewhere durable.
- `main` was never force pushed.

## Applies To

- [[commit.rules.md]]
- [[pr.rules.md]]
- [[codes.rules.md]]
