> Up: [[README.md]]

# Deploy Standard

![Cloud Run](https://img.shields.io/badge/Cloud_Run-Serverless-4285F4?logo=googlecloud&logoColor=white)
![Cloud Build](https://img.shields.io/badge/Cloud_Build-CI-4285F4?logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)

> [!important]
> How an app is containerized and what its deployment must satisfy before it is considered shipped.

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
| **Training a model** | **Not Cloud Run.** Vertex AI custom job, or a VM | A Cloud Run task caps at 24 hours and has no persistent disk |
| A notebook | **Not deployed at all** | Run it locally, or in Vertex AI Workbench |

**Never run migrations from the container `CMD`.** With more than one instance, a cold-start burst runs them concurrently and they contend for the version table; a failure crash-loops the service instead of failing one visible job.

## The PlugMyBrain Exception

**One project does not ship to Cloud Run: `plugmybrain`.** It runs as a single `docker compose` stack on one always-on `e2-small` Compute Engine VM, with its own Postgres in a container.

The reason is the Cost section below, not an argument against it. The memory has no idle state to scale into: the database must always be up, so the managed shape pays the Cloud SQL monthly floor **and** needs a service in front of it. One small VM covers both for one fixed line. The rejected alternatives and the cost accepted are in [[plugmybrain-runs-on-a-flat-cost-vm.decision.memory.md]].

**This does not generalise.** The exception is for a stateful, always-on, single-user service whose managed equivalent costs more than the machine. A project that scales to zero has no claim on it. If a second project ever qualifies, that is when this becomes a rule rather than an exception, per [[README.md]] on a rule broken three times.

What still applies to it unchanged: a pinned base image, a non-root container, no secret in the image, one region, a budget alert, and migrations as a job rather than from `CMD`.

## Resource Allocation

Fixed for every project. Do not change a value without writing down why in the project README.

| Service | CPU | Memory | min | max | Concurrency | Port |
| :- | :- | :- | :- | :- | :- | :- |
| Backend (API) | 1 | 1Gi | 0 | 5 | 30 | 8080 |
| Frontend (static) | 1 | 512Mi | 0 | 5 | 80 | 8080 |

- **Port 8080 is the Cloud Run default**, and the container must read it from the injected `PORT` variable rather than hardcoding it. This is the most common cause of "the container failed to start and listen on the port".
- A backend does real work per request, so each instance takes fewer at a time. A static frontend only serves pre-built files, so one instance absorbs many.
- **Do not raise concurrency to save instances.** An instance gets a fixed CPU share regardless of how many requests it holds, so a higher number adds no capacity; it only makes every request wait longer, and the slowdown surfaces as timeouts rather than as a clear signal.
- `--max-instances 5` is a cost ceiling, not a capacity target. It is what stops a loop or a scraper from scaling until the bill notices.

### The Second Ceiling

A backend on Cloud SQL has a limit that is easy to miss:

```text
max-instances x (pool size + max overflow) = total database connections
```

At 5 instances with a pool of 5 and an overflow of 5, that is 50 connections against a `db-f1-micro` whose default `max_connections` is around 25. The app then fails on connection exhaustion under load, which looks like a database problem and is a configuration problem.

Check the instance's `max_connections` before raising either number, and keep the pool small: a pool of 2 with an overflow of 3 is plenty at this scale.

## Cost

A personal project has no finance team absorbing a mistake. This section is the one that matters.

- **`--min-instances 0`, always.** Scale to zero is the entire reason to use Cloud Run for a side project. A single always-warm instance is roughly the cost of a small VM running all month, for nothing.
- **Cap `--max-instances` at 5.** The default is high. A loop, a scraper, or a public endpoint someone finds will scale until it hits the ceiling, and the bill follows.
- **Set a budget alert before the first deploy**, not after the first surprise. It costs nothing and it is the only thing that tells you.
- **Delete what is not in use.** An idle Cloud Run service is free; an idle Cloud SQL instance, a static IP, and a load balancer are not. Cloud SQL is the usual culprit on a dormant project, because it bills whether or not anything connects to it.
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

## Cloud SQL

PostgreSQL runs on Cloud SQL, attached through the Cloud SQL Auth Proxy rather than over a public IP.

- Attach with `--add-cloudsql-instances $CLOUDSQL_INSTANCE` on a service, and `--set-cloudsql-instances` on a job. The two flags are spelled differently and the wrong one is rejected as an unrecognized argument.
- The connection name is `PROJECT_ID:REGION:INSTANCE`, and its region must match the service's region.
- The runtime service account needs **`roles/cloudsql.client`**. Without it the proxy cannot authenticate, the app blocks on a database it cannot reach, and the container never listens on `PORT`. Cloud Run reports that as a plain startup timeout with no permission error, which is why it is usually mistaken for a port problem.
- Connect over the unix socket the proxy mounts at `/cloudsql/<connection-name>`, not over an IP.
- **Give the instance no public IP.** A public Cloud SQL instance with a weak password is found by scanners within hours.
- The database password is a secret, per [[secret.rules.md]]. Keep the host, port, and database name in environment variables and the password in Secret Manager, or use IAM database authentication and have no password at all.
- Cloud SQL **does not scale to zero**. It bills while it exists, which makes it the single largest cost on an idle project. Stop the instance when a project goes dormant, and delete it when the project is done.

```bash
DATABASE_URL=postgresql+psycopg://[USER]:[PASSWORD]@/[DB]?host=/cloudsql/[CONNECTION_NAME]
```

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
- Move to a US or EU region only for something that region has and yours does not, such as a specific Vertex AI feature.

## No GPU

**Cloud Run GPU is not used on these projects.** There is no budget for it.

A GPU instance bills by the hour it is alive, and a cold start that loads a model onto a GPU is long enough that the temptation is to set `--min-instances 1`, which is exactly the thing that turns a side project into a monthly bill.

Run inference on CPU. If a model is too slow on CPU:

1. Make the model smaller: quantize it, distill it, or use a smaller checkpoint.
2. Move the work off the request path into a Cloud Run job, where slow is acceptable.
3. Batch the predictions instead of serving them one at a time.

Only if all three fail does a GPU become the question, and then it is a budget decision made deliberately, not a flag added to a deploy command.

## Definition of Done

- The image builds from a pinned base, runs as non-root, and listens on `PORT`.
- `.dockerignore` excludes data, weights, notebooks, and `.venv`.
- No secret or configuration value is baked into the image.
- `--min-instances 0` and `--max-instances 5`, with the CPU, memory, and concurrency from the allocation table.
- No GPU flag anywhere.
- Cloud SQL is attached through the proxy, the runtime account holds `roles/cloudsql.client`, and the instance has no public IP.
- A budget alert exists on the project.
- The service, registry, bucket, and Cloud SQL instance are in one region.
- `max-instances x pool size` fits inside the database `max_connections`.
- Migrations run as a job, never from `CMD`.
- Model weights load from storage, not from the image, unless they are small.

## Applies To

- [[deploy.cloud.md]]
- [[secret.rules.md]]
- [[env.rules.md]]
- [[codes.rules.md]]
- [[plugmybrain-runs-on-a-flat-cost-vm.decision.memory.md]]
