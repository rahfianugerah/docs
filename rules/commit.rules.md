> Up: [[README.md]]

# Commit Standard

## Core Requirement

Every commit follows **Conventional Commits 1.0.0** and explains each change as a list item.

A commit message is read by you six months from now, with no memory of the change and no context beyond the diff. Write it for that reader.

All commit messages are written in **English**, including the type, the scope, the description, and the body.

## Structure

```text
<type>[optional scope]: <description>

<body as a list>

[optional footer]
```

1. The type is required and lowercase.
2. The scope is optional, in parentheses, a single lowercase noun.
3. A `!` before the colon marks a breaking change.
4. The description is required, on the first line.
5. One blank line between the description and the body.

## Types

| Type | Use for |
| :- | :- |
| `feat` | A new feature or capability |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `style` | Formatting or lint, no logic change |
| `refactor` | Neither fixes a bug nor adds a feature |
| `perf` | A performance improvement |
| `test` | Adding or correcting tests |
| `build` | Dependencies, packaging, environment file |
| `ci` | Pipeline changes |
| `chore` | Maintenance that fits nothing else |
| `revert` | Reverting a previous commit |
| `exp` | A machine-learning experiment: a run, a parameter sweep, a model change |

`exp` is the one addition to the standard set, because an ML project produces commits that are neither a feature nor a fix. Record what changed and what it scored.

## Description

1. Imperative mood: "add", "fix", "remove", not "added" or "adds".
2. Start lowercase, unless the first word is a proper noun.
3. No trailing period.
4. Keep the whole first line at 72 characters or fewer.
5. State what the commit does, not what you did.

```text
feat(loader): add streaming reader for the parquet dataset
fix(train): stop the scaler fitting on the test split
exp(model): raise embedding dim to 512, macro F1 0.81 from 0.78
```

## Body

The body is required. Every change in the commit gets its own list item.

1. A flat bullet list, using `-`.
2. One item per change. Three concerns means at least three items.
3. Start each item with a capital letter and an imperative verb.
4. No trailing period.
5. Explain the change and its effect together, so the diff is not needed to understand it.
6. Wrap at 100 characters, continuation indented two spaces.
7. No nested list.

```text
fix(train): stop the scaler fitting on the test split

- Move the train and test split above the scaler fit, so the test distribution no longer leaks
  into training
- Record the split seed in the run config, so the same split can be reproduced
```

For an `exp` commit, name the metric and the baseline. A commit that says "improve model" and nothing else is a commit that has to be rerun to be understood.

## Footers

Optional, after one blank line.

| Token | Use for |
| :- | :- |
| `BREAKING CHANGE` | What breaks and what to do instead |
| `Refs` | An issue or a commit SHA |
| `Closes` | An issue this closes |

## No Tool or AI Attribution

A commit records what changed, not what wrote it. You are accountable for the change either way.

Never add a `Co-authored-by` naming an AI, a "generated with" line, a model name, a tool name, or any watermark.

## What Never Goes in a Commit

Beyond the message, the commit itself:

- No secret, key, token, password, or connection string. See [[secret.rules.md]].
- No `.env` or any real configuration file, in any format. See [[env.rules.md]].
- No dataset, model weight, checkpoint, or `.ipynb_checkpoints/`.
- No notebook output. Clear outputs before committing, or the diff is unreadable and the repository grows without limit.

> [!danger]
> Read `git status` before staging. `git add -A` is how an untracked key or a 2GB checkpoint gets committed, and a pushed secret is leaked whatever a later commit removes.

Once pushed, treat a committed secret as leaked and rotate it. Deleting it in a later commit does not remove it from history.

## Formatting Restrictions

Do not use, anywhere in a commit message:

- An emoji, including a Gitmoji prefix
- An em dash, a left arrow, or a right arrow; use `-`, `<`, and `>`
- Smart quotation marks
- A divider built from repeated characters
- Markdown headings, bold, italics, or a code fence
- ALL CAPS, except the `BREAKING CHANGE` token

## One Concern Per Commit

- A change that fits two types is two commits.
- Do not mix a refactor with a fix, or a formatting pass with a feature.
- A change across many files serving one concern is still one commit.

## Definition of Done

- Written in English, type on the allowed list and lowercase.
- Description imperative, no trailing period, first line at 72 or fewer.
- Body present, a flat `-` list, every change explained.
- No secret, data file, or notebook output in the commit.
- No AI or tool attribution.
- One logical concern.

## Applies To

- [[branch.rules.md]]
- [[pr.rules.md]]
- [[docs.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
