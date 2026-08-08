> Up: [[README.md]]

# Model Card Template

Copy the block below into `MODEL.md` for any project that trains a model. Every section exists because leaving it out has cost somebody a rerun.

Rules for filling it in are in [[docs.rules.md]].

```markdown
# [Model Name]

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-[Version]-EE4C2C?logo=pytorch&logoColor=white)
![Task](https://img.shields.io/badge/Task-[Classification]-6E7681)
![Status](https://img.shields.io/badge/Status-[Experimental]-D29922)

[One paragraph: what the model predicts, from what input, for what purpose.]

## Intended Use

**Use for:** [The task it was built and evaluated for.]

**Do not use for:** [Where it will silently be wrong. Be specific; this section is the point of the card.]

## Data

| Field | Value |
| :- | :- |
| Source | [Where it came from] |
| Version | [Dataset version or snapshot date] |
| Size | [Rows, after cleaning] |
| Split | [Train / validation / test, and how it was split] |
| Split seed | [Number] |

[How the data was collected and what biases that introduces. A model trained on one region, one period, or one demographic says so here.]

## Preprocessing

[Every transform, in order. Note which ones are fitted on train only.]

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

[Evaluated on the held-out test set, once. If a number was produced by tuning against the test set, say so; it is not a test result.]

## Failure Modes

[What it gets wrong, and on which inputs. Found by looking at the errors, not by guessing.]

- [Class or input where it fails, and how often]
- [Distribution shift it does not survive]

## Reproducing

```bash
conda activate [env-name]
python -m [package].train --config configs/[name].yaml --seed [seed]
```

[Anything the command does not capture: a data download, a preprocessing run, an environment detail.]

## Artifacts

| Artifact | Location | Notes |
| :- | :- | :- |
| Weights | [Path or registry] | Not committed |
| Config | `configs/[name].yaml` | Committed |
| Metrics | [Run URL or file] | |
```

## Related

- [[docs.rules.md]]
- [[project.template.md]]
- [[codes.rules.md]]
