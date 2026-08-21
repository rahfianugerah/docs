> Up: [[README.md]] · [[ai/README.md]]

# Deep Learning Standard

> [!note]
> Deep learning: the environment, the CUDA build, the checkpoint, and the run that has to be reproducible.

## Core Requirement

For neural networks: PyTorch, on unstructured data such as images, audio, or text.

Read [[ai.rules.md]] first. It owns the environment, reproducibility, data, and experiment rules for every AI project. Read [[ml.rules.md]] before starting a tabular project, because **on tabular data gradient boosting usually wins** and a neural network is the wrong first answer.

## Environment: PyTorch From conda-forge

Per [[ai.rules.md]], a fresh environment per project, conda-forge only, strict priority. PyTorch is where that matters most: it is the package that most often drags in a mismatched NumPy, BLAS, or CUDA runtime and produces an environment that imports and then fails at the first tensor operation.

**CPU:**

```yaml
name: my-dl-project
channels:
  - conda-forge
  - nodefaults
dependencies:
  - python=3.13
  - pytorch                 # CPU build
  - torchvision
  - numpy
  - pillow
  - tensorboard
  - jupyterlab
  - pytest
  - ruff
```

**GPU (NVIDIA):**

```yaml
dependencies:
  - python=3.13
  - pytorch-gpu             # conda-forge's CUDA-enabled build
  - torchvision
  - cuda-version=12.4       # pin, so a solve cannot move you to another CUDA
```

Rules:

1. **Install PyTorch from conda-forge, not pip**, and not from the `pytorch` channel. Mixing channels is the single most common way a working environment breaks; conda-forge builds everything against one consistent ABI.
2. **`pytorch-gpu` is the package name** for a CUDA build on conda-forge. Plain `pytorch` gives you CPU, silently, and the first sign is `torch.cuda.is_available()` returning `False`.
3. **Pin `cuda-version`.** Without it a later solve can move CUDA and leave the driver behind.
4. **Verify immediately after creating the environment**, before writing any code:

```python
import torch
print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))
```

An environment that reports `False` here will train, slowly, on CPU, and you will not notice until a run that should take ten minutes takes six hours.

5. Never `pip install torch` into a conda environment that already has it. You now have two, and which one imports depends on path order.

## Determinism

Neural networks have more sources of randomness than classical models, and the GPU adds its own.

```python
import random, numpy as np, torch

def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

# Full determinism, at a cost in speed:
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.benchmark = False
```

- `cudnn.benchmark = True` picks the fastest kernel per input shape and is **not** deterministic. It is a real speedup on fixed input sizes; keep it off while you are comparing runs, and turn it on once results are settled.
- **A `DataLoader` with `num_workers > 0` needs its own seeding**, through `worker_init_fn` and a seeded `generator`, or each worker draws a different augmentation stream on every run.
- Full determinism costs throughput. Accept it while establishing a result; document if you turn it off.
- Even seeded, results differ across GPU models and library versions. Record the hardware, per [[model.template.md]].

## The Training Loop

Write it once, plainly, and keep it readable. A loop nobody can follow is a loop nobody can debug at 2am.

```python
for epoch in range(epochs):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad(set_to_none=True)
        loss = criterion(model(batch.x), batch.y)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        # validation
        ...
```

The mistakes that cost the most time, in order of how often they happen:

1. **Forgetting `model.eval()`.** Dropout and batch norm stay in training mode, and validation numbers are wrong in a way that looks like a real result.
2. **Forgetting `torch.no_grad()` in validation.** Memory grows until it runs out, usually several epochs in.
3. **Forgetting `optimizer.zero_grad()`.** Gradients accumulate across batches. The loss goes strange rather than erroring.
4. **Calling `.item()` or `.cpu()` inside the loop.** Each one forces a synchronisation and can dominate the runtime.
5. **Keeping the loss tensor for logging.** It holds the whole graph; accumulate `loss.item()` instead.
6. **Shuffling the validation loader.** Harmless until you compare per-sample outputs across runs.

Use a framework such as PyTorch Lightning when the loop grows past readability, but only then. A hand-written loop for a simple project is clearer than a framework's abstractions, per [[codes.rules.md]].

## Data Loading

- `num_workers` above 0, tuned by measurement. The default of 0 loads on the main process and starves the GPU.
- `pin_memory=True` with a GPU.
- **Augment on train only.** A validation set with random augmentation gives a different number every epoch.
- **Normalise with the training set's statistics**, not each batch's own.
- If GPU utilisation sits low, the bottleneck is the data pipeline, not the model. Profile before optimising the model.

## Checkpoints

- Save `state_dict`, never the whole model object. Pickling a model ties the file to your exact class definition and module layout.
- Save the optimizer and scheduler state too, or a resumed run restarts the learning rate schedule from the beginning.
- Record the epoch, the metric, the seed, and the commit alongside the file.
- **Keep the best and the last, not every epoch.** Checkpoints fill a disk faster than anything else in the project.
- **Checkpoints never enter git.** Per [[ai.rules.md]], they live in storage with a documented path.

```python
torch.save({
    "epoch": epoch,
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "metric": best_metric,
    "seed": seed,
}, path)
```

**Load with `weights_only=True`.** A checkpoint is a pickle, and `torch.load` on an untrusted file executes arbitrary code, per [[security.rules.md]]. `safetensors` avoids the problem entirely for weights.

## Training Practice

- **Overfit a single batch first.** If the model cannot drive the loss to near zero on ten samples, it will never learn the dataset, and you have found a bug rather than a hyperparameter.
- Start from a pretrained model wherever one exists. Training from scratch is rarely the right first move.
- Log the training and validation loss together, every epoch. The gap between them is the diagnosis: both high is underfitting, train low and validation high is overfitting.
- Use early stopping on a validation metric, not on a fixed epoch count.
- Use mixed precision (`torch.amp`) on a GPU. It is roughly free speed and memory.
- Increase the batch size before increasing the learning rate. Learning rate is the hyperparameter most likely to make training diverge.
- **Watch for a loss that becomes NaN.** It is almost always a learning rate that is too high, a division by zero, or an unclipped gradient. Add `torch.nn.utils.clip_grad_norm_` before assuming the model is wrong.

## No GPU in Deployment

Per [[deploy.rules.md]], deployment is CPU-only on Cloud Run and there is no budget for a GPU.

That is a constraint on what you build, not just on how you ship it:

- **Export for CPU inference.** Quantize, or distil to a smaller model, and measure the latency on CPU before promising anything.
- `torch.compile` or ONNX Runtime gives a real CPU speedup with no accuracy change.
- Batch predictions in a job rather than serving them one at a time, where the use case allows.
- If a model is only viable on a GPU, that is a design decision that needs a budget, made before training rather than after.

Training happens locally, on a rented machine, or in Colab. Serving happens on CPU.

## Testing

- Test that a forward pass returns the expected shape for a known input.
- Test that one training step reduces the loss on a fixed batch.
- Test that a checkpoint saves and loads to identical outputs.
- Test the data pipeline: a batch has the right shape, the right dtype, and no NaN.

These four are fast, they run on CPU, and they catch the majority of silent breakage.

## Do and Do Not

Do:

- Install PyTorch from conda-forge, using `pytorch-gpu` for CUDA, with `cuda-version` pinned.
- Verify `torch.cuda.is_available()` before writing code.
- Seed Python, NumPy, torch, and the DataLoader workers.
- Overfit one batch before training on the dataset.
- Save `state_dict` with the optimizer state and the metadata.
- Load checkpoints with `weights_only=True`.
- Design for CPU inference from the start.

Do not:

- `pip install torch` into a conda environment.
- Mix conda-forge with the `pytorch` channel.
- Forget `model.eval()` or `torch.no_grad()` in validation.
- Call `.item()` inside the inner loop, or keep loss tensors for logging.
- Augment or shuffle the validation set.
- Save the whole model object, or commit a checkpoint.
- Assume a GPU will be available in production.

## Related

- [[ai.rules.md]]
- [[ml.rules.md]]
- [[ai/README.md]]
- [[deploy.rules.md]]
- [[model.template.md]]
