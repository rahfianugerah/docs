> Up: [[README.md]] · [[ai/README.md]]

# AI Project Standard

> [!important]
> Every AI project gets its own conda environment, and the environment file is what defines it.

## Core Requirement

Every AI project follows this file, plus the one for its kind: [[ml.rules.md]] for classical machine learning, [[dl.rules.md]] for deep learning.

An AI project fails differently from ordinary software. Ordinary code is broken or working; a model is **quietly wrong**. It returns a number, the number looks plausible, and nothing raises an error. Every rule here exists to make silence impossible.

The general code standard in [[codes.rules.md]] still applies: YAGNI, KISS, DRY, English, Python 3.13, Ruff, pytest. This file adds what is specific to AI and does not repeat what is not.

## Environment: One Per Project, Always Conda

**Every ML, DL, or AI project gets its own conda environment. No exceptions, no sharing, no reuse.**

This is not tidiness. AI dependency trees are the most fragile in Python: NumPy, SciPy, PyTorch, CUDA, cuDNN, BLAS, and a dozen compiled libraries all pin each other, and installing one package can silently downgrade another and change your results. An environment shared between two projects will break one of them, usually the one you are not looking at.

### Rules

1. **One environment per project**, named after the project. `iris-classifier`, not `ml`, not `work`, not `test`.
2. **Never install into `base`.** A broken `base` breaks conda itself, and recovering it means reinstalling Miniconda.
3. **conda-forge is the channel.** Not `defaults`, not `pytorch`, not a mix.
4. **Set strict channel priority**, once per machine. Without it conda mixes packages built against different ABIs and produces an environment that imports but segfaults.
5. **`environment.yml` is committed and is the source of truth.** An environment nobody can recreate is a result nobody can reproduce.
6. **pip only for what conda-forge does not carry**, and always inside the `pip:` block of the same `environment.yml`. A package installed with a bare `pip install` and never recorded is the most common reason an environment cannot be rebuilt.
7. **Pin the Python version** in the file. Do not let a rebuild silently land on a different interpreter.

### Setup

Once per machine:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Per project:

```bash
conda env create -f environment.yml
conda activate my-project
```

```yaml
# environment.yml
name: my-project
channels:
  - conda-forge
  - nodefaults          # refuse to silently fall back to the defaults channel
dependencies:
  - python=3.13
  - numpy
  - pandas
  - scikit-learn
  - jupyterlab
  - pip
  - pip:
      - some-package-conda-forge-lacks
```

`nodefaults` matters. Without it a package missing from conda-forge is pulled from `defaults` instead, and the mixed-ABI environment that produces is the hardest kind of broken to diagnose: it installs cleanly and fails at import or, worse, at runtime.

### Use Mamba

`conda` solves environments slowly enough that people start skipping the environment file. Use the same commands with a faster solver:

```bash
conda install -n base -c conda-forge conda-libmamba-solver
conda config --set solver libmamba
```

Or use `mamba` or `micromamba` directly. Same channels, same file, same rules.

### Exporting

```bash
conda env export --from-history > environment.yml
```

**`--from-history` is not optional.** A plain export writes every transitive dependency with an exact build string, which is unreadable, enormous, and will not solve on another operating system. `--from-history` writes only what you actually asked for.

Read the exported file before committing it. It sometimes drops the `pip:` block, and it always drops packages installed with bare pip.

## Reproducibility

**A result you cannot reproduce is an anecdote.** These are the five things that make a run repeatable, and every one of them is a thing people skip.

### 1. Seed Everything, and Record the Seed

```python
import random, numpy as np

def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    # frameworks add their own; see ml.rules.md and dl.rules.md
```

The seed goes in the config and in the run record, not in a variable somebody edited once. A run with an unrecorded seed cannot be repeated even by the person who ran it.

### 2. Version the Data

Code without data is not reproducible. Record, for every run:

- Where the data came from and when it was pulled
- A version, a snapshot date, or a content hash
- The row count after cleaning

A hash of the file is enough for a small dataset, and it is the only thing that catches a file being silently replaced.

### 3. Pin the Environment

`environment.yml` is committed and matches what you ran. If you installed something mid-session, update the file before recording the result.

### 4. Record the Commit

The git SHA of the code that produced the result, alongside the result. A metric with no commit is a metric nobody can trace back to the code that made it.

### 5. Make the Split Deterministic

The train/validation/test split is derived from a recorded seed, or written to disk and committed. A split that is re-randomised on every run makes every comparison meaningless, because two runs saw different data.

## Data

- **Data never enters git.** Not raw, not processed, not a "small sample". A repository with a dataset in it is a repository nobody can clone quickly and a history nobody can rewrite.
- Data lives in `data/`, which is gitignored, with a documented way to obtain it.
- **`data/raw/` is read-only.** Never modify a raw file in place. Every transform writes to `data/processed/`, so the pipeline can be rerun from the original.
- **Split before you look.** Every decision made while looking at the test set leaks into the model, including decisions about preprocessing and feature selection.
- **Fit on train only.** A scaler, an encoder, an imputer, or a vocabulary fitted on the full dataset has seen the test distribution. This is the most common leak, and it shows up as a validation score that is much better than the test score.
- Know where the data came from. Licence, consent, and personal data are constraints on what you may publish, per [[secret.rules.md]].

## Experiments

- **A notebook explores. A module keeps.** Anything that runs twice moves out of the notebook into a function a module exposes, and the notebook imports it.
- Track runs with a tool, not a spreadsheet: MLflow or Weights and Biases. Log the parameters, the metrics, the seed, the data version, and the commit.
- **Record failures.** An experiment that did not work is information, and the alternative is running it again next year having forgotten. Write the finding into [[memory/README.md]].
- One variable at a time. Two changes and an improved metric tell you nothing about which one caused it.
- Never tune against the test set. Tune on validation; touch test once, at the end, and report that number.

## Evaluation

- **A baseline first.** Predict the majority class, or the mean. A model that cannot beat that has not learned anything, and you cannot know that without the number.
- Choose the metric before training, from the problem. Accuracy on an imbalanced dataset is a way of not measuring anything.
- Report a range, not a point. A single number from one split is noise; use cross-validation or several seeds.
- **Look at the errors.** The confusion matrix and a sample of wrong predictions say more about what to do next than any aggregate metric.
- Write down what the model is bad at, in `MODEL.md`, per [[model.template.md]]. It is the section everyone skips and the only one that stops the model being misused.

## Serving

- The **exact preprocessing used at training** runs at inference. Reimplementing it separately is where training and serving skew comes from; share the code path.
- Version the model artifact, and record which artifact answered which request.
- Validate the input at the boundary. A model given an out-of-range feature returns a confident wrong answer rather than an error.
- **Never load a pickle you did not create.** `pickle.load` executes arbitrary code, which makes a downloaded `.pkl` a remote code execution vector. Prefer `safetensors`, ONNX, or a plain format. See [[security.rules.md]].
- Deploy per [[deploy.rules.md]]: CPU inference on Cloud Run, no GPU, weights loaded from storage rather than baked into the image.

## Do and Do Not

Do:

- Create a fresh conda environment per project, from conda-forge, with strict priority.
- Commit `environment.yml` and keep it current.
- Seed everything and record the seed with the result.
- Split before preprocessing, and fit only on train.
- Establish a baseline before claiming a model works.
- Move anything that runs twice out of the notebook.
- Record failed experiments.

Do not:

- Install into `base`, or share an environment between projects.
- Mix conda-forge with `defaults` or another channel.
- Install with bare pip and not record it.
- Commit data, weights, or checkpoints.
- Fit a transform on the full dataset.
- Tune against the test set.
- Report a metric without a baseline, a seed, and a data version.
- Load an untrusted pickle.

## Related

- [[ai/README.md]]
- [[ml.rules.md]]
- [[dl.rules.md]]
- [[codes.rules.md]]
- [[database.rules.md]]
- [[model.template.md]]
