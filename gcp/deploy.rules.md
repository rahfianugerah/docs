> Up: [[README.md]]

# Deploy Standard

![Cloud Run](https://img.shields.io/badge/Cloud_Run-Serverless-4285F4?logo=googlecloud&logoColor=white)
![Cloud Build](https://img.shields.io/badge/Cloud_Build-CI-4285F4?logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)

## Core Requirement

Every deployed project ships as a container image to **Cloud Run**, built by **Cloud Build**, stored in **Artifact Registry**.

The runbook with the actual commands is [[deploy.cloud.md]]. This file decides the rules; that one is copy and paste.

## What Runs Where

Cloud Run is not the answer to everything, and picking wrong is expensive.

| Workload | Where | Why |
| :- | :- | :- |
| An API serving a model | **Cloud Run service** | Scales to zero, pays per request |
| A batch job, a nightly scan, an ETL | **Cloud Run job** | Runs to completion and exits, no request needed |
| A migration | **Cloud Run job** | Never from the container `CMD`, see below |
| **Training a model** | **Not Cloud Run.** Vertex AI custom job, or a VM | A Cloud Run task caps at 24 hours, has no persistent disk, and its GPU support is for inference |
| A notebook | **Not deployed at all** | Run it locally, or in Vertex AI Workbench |

**Never run migrations from the container `CMD`.** With more than one instance, a cold-start burst runs them concurrently and they contend for the version table; a failure crash-loops the service instead of failing one visible job.

## Cost

A personal project has no finance team absorbing a mistake. This section is the one that matters.

- **`--min-instances 0`, always.** Scale to zero is the entire reason to use Cloud Run for a side project. A single always-warm instance is roughly the cost of a small VM running all month, for nothing.
- **Cap `--max-instances`.** The default is high. A loop, a scraper, or a public endpoint someone finds will scale until it hits the ceiling, and the bill follows. Set 2 to 4 unless there is a reason.
- **Set a budget alert before the first deploy**, not after the first surprise. It costs nothing and it is the only thing that tells you.
- **Delete what is not in use.** An idle Cloud Run service is free; an idle Cloud SQL instance, a static IP, a load balancer, and a persistent disk are not. Cloud SQL is the usual culprit on a dormant project.
- **Artifact Registry charges for storage.** Old image tags accumulate. Set a cleanup policy keeping the last handful.
- Accept the cold start. A few seconds on the first request after idle is the trade for paying nothing while idle.

## Container Rules

- One `Dockerfile` at the repository root, building one image.
- Pin the base image: `python:3.13-slim`, never `python:latest`.
- Multi-stage build. Dependencies install in a build stage; the runtime stage carries the app and the installed packages, not the compiler.
- Run as a non-root user.
- **Listen on the `PORT` environment variable Cloud Run injects.** Not a hardcoded 8080. This is the most common reason a container "fails to start and listen on the port".
- A `.dockerignore` excluding `.venv`, `.git`, `data/`, `*.ipynb`, `__pycache__`, and model weights. Without it the build context includes the dataset, and the build is slow before it is broken.
- Never `ENV` a secret or a configuration value into the image, per [[secret.rules.md]].

```dockerfile
FROM python:3.13-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim
RUN useradd -m app
COPY --from=build /install /usr/local
COPY --chown=app:app . /app
WORKDIR /app
USER app
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
```

A conda project builds from a `micromamba` base or exports `environment.yml` to a `requirements.txt` for the image. Conda in a container is heavy; use it where native dependencies genuinely require it, and pip otherwise.

## Model Weights Do Not Go in the Image

An image carrying a 2GB checkpoint is slow to build, slow to cold start, and rebuilt in full every time the code changes.

- Store weights in **Cloud Storage**, and download them at startup into `/tmp`.
- Or mount a Cloud Storage bucket as a volume, where the runtime supports it.
- Pin the weights by version or checksum, so a redeploy cannot silently pick up different weights.
- A small model, under about 100MB, is fine in the image. Measure before assuming.

## Configuration and Secrets

Follows [[secret.rules.md]]. The GCP mechanics:

| Kind | Delivered by |
| :- | :- |
| Configuration | `--set-env-vars`, or `--env-vars-file` when a value contains a comma |
| Secret | `--set-secrets`, backed by Secret Manager |

- Never in the `Dockerfile`, never in a committed `.env`, never baked into the image.
- The runtime service account needs `roles/secretmanager.secretAccessor` on each secret it reads. Without it the revision fails to start with a permission error naming the secret.
- A secret whose `--set-secrets` key contains a `/` mounts as a file at that path rather than an environment variable.
- **Cloud Build substitutions are visible in the build log and the trigger config.** A secret never travels as a substitution.

## Build Rules

- Build through the repository's own `cloudbuild.yaml`, never `gcloud builds submit --tag`. Only the config path runs the deploy step and exercises the file a trigger will later use.
- Pass the image tag explicitly as a `_TAG` substitution. Cloud Build's `$SHORT_SHA` is populated only for trigger-started builds; relying on it in a manual build produces an image reference ending in a bare colon.
- **Declare `options: logging: CLOUD_LOGGING_ONLY`** when the build runs under an explicit service account, or the build fails before any step with a message about the logs bucket.
- Never deploy `:latest`. A tag that moves cannot be rolled back to.
- The build account needs `artifactregistry.writer`, `run.admin`, `iam.serviceAccountUser` on the runtime account, and `logging.logWriter`.

## Region

Pick one region and keep everything in it: the service, the registry, the bucket, the database. Cross-region traffic costs money and adds latency for no benefit.

- `asia-southeast1` (Singapore) is the default here: closest to Indonesia with full Cloud Run support including custom domain mapping.
- `asia-southeast2` (Jakarta) is closer but **does not support Cloud Run domain mapping**. Use it only for a service that will never need a custom domain.
- Move to a US or EU region only for something that region has and yours does not, usually GPU availability or a specific Vertex AI feature.

## GPU Inference

Cloud Run supports GPUs in a limited set of regions, for **inference**, not training.

- `--gpu 1 --gpu-type nvidia-l4`, and `--no-cpu-throttling` so the instance keeps its CPU between requests.
- `--min-instances 0` still applies, and the cold start is much longer while the model loads. Measure it before promising a latency number.
- A GPU instance is expensive per hour. Cap `--max-instances` low, and set the budget alert.
- If the workload is a batch of predictions rather than live requests, a Cloud Run job or Vertex AI batch prediction is cheaper than a warm GPU service.

## Definition of Done

- The image builds from a pinned base, runs as non-root, and listens on `PORT`.
- `.dockerignore` excludes data, weights, notebooks, and `.venv`.
- No secret or configuration value is baked into the image.
- `--min-instances 0` and a capped `--max-instances`.
- A budget alert exists on the project.
- The service, registry, bucket, and database are in one region.
- Migrations run as a job, never from `CMD`.
- Model weights load from storage, not from the image, unless they are small.

## Applies To

- [[deploy.cloud.md]]
- [[secret.rules.md]]
- [[env.rules.md]]
- [[codes.rules.md]]
