> Up: [[README.md]] · [[ai/README.md]]

# Classical Machine Learning Standard

> [!note]
> Classical machine learning: the split, the baseline, the metric, and the leak that makes a score look good.

## Core Requirement

For tabular and classical machine learning: scikit-learn, gradient boosting, and anything that is not a neural network.

Read [[ai.rules.md]] first. It owns the environment, reproducibility, data handling, and experiment tracking rules that apply to every AI project. This file adds what is specific to classical ML.

## Start Here, Not With Deep Learning

**On tabular data, gradient boosting beats a neural network almost every time**, trains in seconds instead of hours, needs no GPU, and explains itself. Reach for deep learning when the data is genuinely unstructured: images, audio, long text.

The order to try things:

1. A baseline: majority class, or the mean.
2. Logistic or linear regression. Fast, and it tells you whether the features carry signal at all.
3. Gradient boosting: LightGBM, XGBoost, or CatBoost.
4. Anything else, only once you know why the above is not enough.

Most of the gain in a tabular project comes from the data, not the model. Fixing labels, adding a feature, or removing a leak moves the metric more than swapping algorithms.

## Environment

Per [[ai.rules.md]], with the packages this kind of project needs:

```yaml
name: my-ml-project
channels:
  - conda-forge
  - nodefaults
dependencies:
  - python=3.13
  - numpy
  - pandas
  - scikit-learn
  - lightgbm            # conda-forge carries it with working OpenMP
  - matplotlib
  - jupyterlab
  - pytest
  - ruff
```

Install LightGBM and XGBoost from conda-forge rather than pip. The conda-forge builds bring their own OpenMP runtime; the pip wheels on macOS need one installed separately and fail at import without it.

## Use a Pipeline, Always

**Every preprocessing step lives inside a scikit-learn `Pipeline`.** This is not a style preference; it is what makes leakage structurally impossible.

A scaler fitted outside a pipeline, before the split, has seen the test set. Inside a pipeline with cross-validation, it is refitted on each training fold automatically, and the leak cannot happen.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
])

model = Pipeline([("prep", preprocess), ("clf", LGBMClassifier(random_state=42))])
model.fit(X_train, y_train)
```

Rules:

- **The pipeline is the model.** Save and load the whole pipeline, never the estimator alone, or inference silently skips the preprocessing.
- `handle_unknown="ignore"` on any encoder. A category seen only at inference otherwise raises, and it will happen in production.
- **Never call `fit` or `fit_transform` on test data.** Only `transform`. If you find yourself wanting to, the step belongs in the pipeline.
- Impute inside the pipeline, so the fill value comes from the training fold.

## Splitting and Validation

The split is the part that decides whether your number means anything.

| Data | Split |
| :- | :- |
| Independent rows | `train_test_split`, stratified on the target |
| Imbalanced classes | Stratified, always |
| **Time series** | **Chronological.** Never shuffle |
| Grouped rows (patients, users, sessions) | `GroupKFold`, so a group is never split across train and test |

- **Stratify on the target** for classification. Without it a rare class can land entirely in one side of the split.
- **Never shuffle time series.** A random split lets the model see the future to predict the past, which produces an excellent score and a useless model. Use `TimeSeriesSplit`.
- **Group leakage is invisible and common.** Ten rows from the same user split across train and test means the model memorises the user rather than learning the task. Split by group.
- Use cross-validation for the reported number, not a single split. One split is one sample of a noisy estimate.
- Keep a **held-out test set touched once**, at the end. Everything else happens on validation.

## Features

- **A feature computed from the target is a leak.** So is a feature computed after the event you are predicting. Ask, for every feature: would this value have been available at prediction time?
- Target encoding leaks unless it is fitted inside the cross-validation fold. Use a library that does it correctly, or use one-hot.
- **Do not scale tree models.** Gradient boosting and random forests are invariant to monotonic transforms; scaling adds a step that can only go wrong.
- Do scale linear models, SVMs, and anything distance-based. They are dominated by whichever feature has the largest range otherwise.
- Prefer fewer, better features. A feature that does not move the metric is a feature that will break silently later.
- Compute features once, in shared code, so training and inference use the same definition.

## Class Imbalance

Handle it deliberately, and know that the first two options change what the model outputs.

| Approach | Effect |
| :- | :- |
| `class_weight="balanced"` | Reweights the loss. First thing to try |
| Resampling (SMOTE, undersampling) | Changes the training distribution. **Apply inside the CV fold only** |
| Threshold tuning | Leaves the model alone and moves the decision point. Often the right answer |
| Nothing, and use the right metric | Sometimes correct. The imbalance may be real and informative |

- Never resample the test set. It must reflect reality.
- Accuracy is the wrong metric under imbalance. Use precision, recall, F1, or average precision, chosen from what the errors cost.
- The default `0.5` threshold is not sacred. Pick the threshold from the precision-recall curve and the cost of each error type, and record which threshold you chose.

## Persisting a Model

- Save the whole pipeline with `joblib`, alongside the metadata that makes it reproducible: the training date, the data version, the library versions, the metrics, the commit.
- **A pickled model is a Python object with a version dependency.** It may fail to load under a different scikit-learn version. Record the version that wrote it, and validate the load in the same environment before deploying.
- **Never load a model file you did not produce.** Unpickling executes code, per [[security.rules.md]].
- For anything long-lived or cross-language, prefer ONNX over a pickle.

## Explaining a Model

- Report feature importance for any model presented to a person. Permutation importance is honest; the impurity-based importance built into tree models is biased toward high-cardinality features.
- Use SHAP for individual predictions when a decision affects someone and must be explained.
- **A feature at the top of the importance list that should not matter is a leak**, not a discovery. It is the fastest leak detector there is.

## Testing

- Test the pipeline end to end on a small fixture: it fits, it predicts, and the output has the expected shape and range.
- Test that a feature function returns what it should for a known input, especially anything with date arithmetic or a groupby.
- **Assert there is no leak**: a test that fails if the training columns include the target, or if a fitted transform is called on the test set.
- Test that the saved model loads and predicts identically to the one in memory.

## Do and Do Not

Do:

- Establish a baseline, then a linear model, then gradient boosting.
- Put every preprocessing step inside a `Pipeline`.
- Stratify a classification split, and split time series chronologically.
- Split by group when rows are grouped.
- Save the whole pipeline with its metadata.
- Check the importance list for a feature that should not be there.

Do not:

- Reach for a neural network on tabular data before trying boosting.
- Fit any transform outside the pipeline or on test data.
- Shuffle a time series split.
- Scale features for a tree model.
- Resample the test set.
- Report accuracy on an imbalanced problem.
- Load a pickle from an untrusted source.

## Related

- [[ai.rules.md]]
- [[dl.rules.md]]
- [[ai/README.md]]
- [[model.template.md]]
