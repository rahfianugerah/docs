> Up: [[README.md]]

# AI Projects

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Conda Forge](https://img.shields.io/badge/conda--forge-Channel-00A99D?logo=condaforge&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-conda--forge-EE4C2C?logo=pytorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/Scikit--learn-Tabular-F7931E?logo=scikitlearn&logoColor=white)

Standards for machine learning and deep learning projects, separated from the general project rules because AI projects fail differently.

## Why This Is Separate

Ordinary software is broken or working. **A model is quietly wrong**: it returns a plausible number, nothing raises, and the mistake surfaces weeks later in a decision somebody made. The rules in this folder exist to make that silence impossible.

The second difference is the environment. An AI dependency tree, with NumPy, BLAS, CUDA, and a dozen compiled libraries pinning each other, is the most fragile in Python. Installing one package can silently downgrade another and change your results without an error anywhere.

That is why every AI project gets **its own conda environment, from conda-forge, every time**.

## Read in This Order

| Document | Covers |
| :- | :- |
| [[ai.rules.md]] | Everything common: the environment, reproducibility, data, experiments, evaluation, serving |
| [[ml.rules.md]] | Classical and tabular: scikit-learn, gradient boosting, pipelines, splitting, imbalance |
| [[dl.rules.md]] | Deep learning: PyTorch from conda-forge, determinism, the training loop, checkpoints |

Start with [[ai.rules.md]], always. Then read the one for the kind of project you are building.

**Which one?** If the data is a table, read [[ml.rules.md]] and start with gradient boosting. If the data is images, audio, or long text, read [[dl.rules.md]]. A neural network on tabular data is usually the wrong first answer, and [[ml.rules.md]] says why.

## The Environment Rule

The one rule that matters more than the rest, stated here so it cannot be missed:

```bash
# Once per machine
conda config --add channels conda-forge
conda config --set channel_priority strict

# Once per project, never shared, never `base`
conda env create -f environment.yml
conda activate my-project
```

- **One environment per project.** Never shared, never reused, never `base`.
- **conda-forge only.** Not `defaults`, not the `pytorch` channel, not a mix. Mixing channels produces an environment that installs cleanly and fails at runtime.
- **`nodefaults` in the channel list**, so a missing package fails loudly rather than being pulled from another channel.
- **PyTorch comes from conda-forge**: `pytorch` for CPU, `pytorch-gpu` for CUDA. Never `pip install torch`.
- **`environment.yml` is committed** and is the source of truth. An environment nobody can recreate is a result nobody can reproduce.

## What These Rules Assume

| Layer | Choice |
| :- | :- |
| Language | Python 3.13 |
| Environment | Miniconda, conda-forge, strict channel priority, one env per project |
| Tabular | scikit-learn, LightGBM or XGBoost |
| Deep learning | PyTorch from conda-forge |
| Tracking | MLflow or Weights and Biases |
| Serving | CPU only, per [[deploy.rules.md]]. There is no GPU budget |

## Related

- [[ai.rules.md]]
- [[ml.rules.md]]
- [[dl.rules.md]]
- [[codes.rules.md]]
- [[model.template.md]]
- [[deploy.rules.md]]
