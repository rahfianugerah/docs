> Up: [[README.md]]

# Pull Request Standard

## Core Requirement

A pull request is a written record of why a change happened. On a personal project it has no reviewer, which changes who it is for but not whether it is worth writing: **the reader is you, later, asking why the code looks like this.**

Titles and descriptions are written in **English**.

## When to Open One

Not every change needs a pull request. Use judgement, and default to the cheaper option.

| The change | Do this |
| :- | :- |
| A typo, a comment, a version bump | Commit straight to `main` |
| A small fix, one or two commits | Merge the branch directly, no PR |
| A feature, a refactor, a migration | Open a PR |
| An experiment worth remembering | Open a PR, even if you merge it yourself a minute later |
| Anything you might want to find again in a year | Open a PR |

The rule of thumb: **open a PR when the reasoning matters more than the diff.** A PR is searchable prose attached to a change, which is the one thing git history is bad at.

## Title

Same format as a commit description, per [[commit.rules.md]]:

```text
<type>[optional scope]: <description>
```

Imperative, lowercase start, no trailing period, 72 characters or fewer, type from the allowed list.

```text
feat(loader): add streaming reader for the parquet dataset
exp(model): sweep embedding dim from 128 to 512
```

## Description

Four sections, in this order. Omit Results on anything that is not an experiment; keep the other three.

```text
## Summary

<one or two sentences: what this does and why>

## Changes

- <one item per change, imperative, explaining the effect>

## Results

<experiments only: the metric, the baseline, the parameters, the seed>

## Test Plan

- [ ] <how you verified it, or why testing does not apply>
```

### Summary

One or two sentences. What changes and why. Not the sequence of things you tried.

### Changes

The same body rules as a commit: a flat `-` list, one item per change, imperative, no trailing period, explaining the effect rather than naming a file.

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

> [!tip]
> Open a PR when the reasoning matters more than the diff. A PR is searchable prose attached to a change, which is the one thing git history is bad at.

### Test Plan

How the change was verified. A checklist or a list.

When testing genuinely does not apply, say so directly rather than leaving it empty:

```text
## Test Plan

Documentation only, no runtime behavior to verify
```

## No Tool or AI Attribution

Never add a `Co-authored-by` naming an AI, a "generated with" line, a model name, a tool name, or a watermark, in a title, a description, or a comment.

## Formatting Restrictions

The same as [[commit.rules.md]]: no emoji, no em dash, no arrows, no smart quotes, no decorative dividers, no ALL CAPS except `BREAKING CHANGE`.

The `##` headings above are the required structure, not decoration.

## Security and Privacy

- No secret, token, password, or connection string in a title, description, or comment.
- No screenshot or log excerpt that exposes one.
- Reference a secret by its variable name only, per [[secret.rules.md]].

## Definition of Done

- Title in English, `<type>[scope]: <description>`, 72 or fewer, no trailing period.
- Summary, Changes, and Test Plan present.
- Changes is a flat `-` list where every item explains its effect.
- An experiment records the metric, the baseline, the parameters, and the seed.
- No AI or tool attribution, no secret, no prohibited formatting.
- One logical concern.

## Applies To

- [[commit.rules.md]]
- [[branch.rules.md]]
- [[docs.rules.md]]
- [[secret.rules.md]]
