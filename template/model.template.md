---
tags:
  - kind/template
  - layer/docs
  - topic/data
---

> Up: [[README.md]]

# Model Card Template

> [!example]
> Every `[bracketed]` passage below is guidance to be replaced, not structure to be kept. Remove each one once the real content is in place, and keep the section order.

Copy the block below into `MODEL.md` for any project that trains a model. **The block carries no frontmatter and no `---`**, per the project document shape in [[docs.rules.md]].

**Every section exists because leaving it out has cost somebody a rerun.** Intended Use and Failure Modes are the two that make this a model card rather than a changelog, and they are the two that get left thin.

````markdown
# [Model Name]

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-[Version]-EE4C2C?logo=pytorch&logoColor=white)
![Task](https://img.shields.io/badge/Task-[Classification]-6E7681)
![Status](https://img.shields.io/badge/Status-[Experimental]-D29922)

[One or two sentences: what the model predicts, from what input, for what purpose, with **the
claim that matters in bold**.]

[Then one sentence on why it exists: what it replaced, or what was impossible without it.]

## Table of Contents

1. [Intended Use](#intended-use)
2. [Data](#data)
3. [Preprocessing](#preprocessing)
4. [Training](#training)
5. [Results](#results)
6. [Failure Modes](#failure-modes)
7. [Reproducing](#reproducing)
8. [Artifacts](#artifacts)
9. [Known Limitations](#known-limitations)

## Intended Use

**Use for:** [The task it was built and evaluated for.]

**Do not use for:** [Where it will silently be wrong. Be specific; this is the point of the
card. A model is quietly wrong rather than broken, so this section is the only thing standing
between the model and a decision it should not have informed.]

## Data

| Field | Value |
| :- | :- |
| Source | [Where it came from] |
| Version | [Dataset version or snapshot date] |
| Size | [Rows, after cleaning] |
| Split | [Train, validation, test, and how it was split] |
| Split seed | [Number] |

[How the data was collected and what biases that introduces. A model trained on one region,
one period, or one demographic says so here, in bold, because it is a limit on every number
below.]

## Preprocessing

[Every transform, in order. **Note which ones are fitted on train only**, because that is where
leakage enters and it does not show up in the metrics.]

1. [Step]
2. [Step]

## Training

| Field | Value |
| :- | :- |
| Architecture | [Model and size] |
| Parameters | [Learning rate, batch size, epochs, optimizer] |
| Random seed | [Number] |
| Hardware | [GPU or CPU] |
| Runtime | [Duration] |
| Commit | [Git SHA that produced this model] |

## Results

| Metric | This model | Baseline | Notes |
| :- | :- | :- | :- |
| [Macro F1] | [0.81] | [0.78] | [What the baseline is] |

[Evaluated on the held-out test set, once.] **If a number was produced by tuning against the
test set, say so; it is not a test result.**

## Failure Modes

[What it gets wrong, and on which inputs. Found by looking at the errors, not by guessing.
Each item is the failure in bold, then how often, then what it looks like from outside.]

- **[The class or input where it fails.]** [How often, and what the wrong output looks like.]
- **[The distribution shift it does not survive.]** [What changes, and what happens then.]

## Reproducing

```bash
conda activate [env-name]
python -m [package].train --config configs/[name].yaml --seed [seed]
```

[Anything the command does not capture: a data download, a preprocessing run, an environment
detail. **If the run cannot be reproduced from this section alone, it is not reproducible**,
and saying which part is missing is more useful than implying it is complete.]

## Artifacts

| Artifact | Location | Notes |
| :- | :- | :- |
| Weights | [Path or registry] | Gitignored. [How to regenerate] |
| Config | `configs/[name].yaml` | Committed |
| Metrics | [Run URL or file] | [Committed or not] |

## Known Limitations

[The ceiling of each part, beyond the failure modes above: what the card itself does not cover,
what has not been measured, and what would change the numbers.]

- **[The limit.]** [Why it is that way, and what it costs.]
````

## Related

- [[docs.rules.md]]
- [[project.template.md]]
- [[api.template.md]]
- [[codes.rules.md]]
- [[ai.rules.md]]
- [[ml.rules.md]]
- [[dl.rules.md]]
