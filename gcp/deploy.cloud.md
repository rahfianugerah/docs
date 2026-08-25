---
tags:
  - kind/runbook
  - layer/infra
  - topic/deploy
---

> Up: [[README.md]]

# Cloud Run Deploy Runbook

> [!important]
> This file is the canonical runbook. Every project copies it into its own repository root as `deploy.cloud.md` and keeps the section numbering identical, so any two repositories stay comparable line for line.

![Region](https://img.shields.io/badge/Region-asia--southeast1-4285F4?logo=googlecloud&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Cloud_Run-4285F4?logo=googlecloud&logoColor=white)
![Registry](https://img.shields.io/badge/Registry-Artifact_Registry-4285F4?logo=googlecloud&logoColor=white)
![Production](https://img.shields.io/badge/Production-Main-2EA043?logo=github&logoColor=white)

A project copy replaces the generic placeholders with its real service name, variables, and secrets. **Never commit a filled-in copy that contains a real secret value.**

Implements [[deploy.rules.md]]. Region is always `asia-southeast1`.

## 1. Service Summary

Every project copy opens with this table, filled in.

| Field | Value |
| :- | :- |
| Repository | `[REPO]` |
| Cloud Run service | `[SERVICE]` |
| Image | `asia-southeast1-docker.pkg.dev/[PROJECT_ID]/[REPOSITORY]/[SERVICE]` |
| Region | `asia-southeast1` |
| Allocation | `[1 vCPU, 1Gi, max-instances 4, concurrency 30]` |
| Trigger | `[SERVICE]-main`, branch `main` |
| Substitutions sent by the trigger | `_TAG` for a backend, `_TAG` and `_API_BASE_URL` for a frontend |
| Domain | `[HOST]` |
| Health check | `[URL]/health` |
| Cloud Run Jobs | `[SERVICE]-migrate`, plus one row per purpose-built job with its schedule, or `None` |
| Related files | `cloudbuild.yaml`, `Dockerfile`, `env-vars.example.yaml` |

**List every job the repository owns in that row.** A job is created by hand and updated by hand, so a job missing from this table is a job nobody moves forward on release.

### Resource Allocation

| Service | CPU | Memory | max-instances | concurrency |
| :- | :- | :- | :- | :- |
| Frontend, a static bundle | 1 | 512Mi | 2 | 80 to 100 |
| Backend | 1 | 1Gi | 4 to 5 | 25 to 30 |

A static frontend only serves pre-built files, so one instance absorbs a lot of traffic and the ceiling exists to cap cost, not to carry load. A backend does real work per request, so each instance takes fewer of them at a time and the ceiling is higher.

> [!warning]
> Raising `--concurrency` does not add capacity. One instance holds a fixed CPU share no matter how many requests it carries, so the extra ones only queue, and the delay surfaces as a timeout rather than as a clear signal.

A backend that talks to a database has a second ceiling that is easy to miss:

```text
max-instances x (pool size + max overflow) = total database connections
```

That total is shared with every other service on the same database instance. **Check the instance's `max_connections` before raising `--max-instances`**, not after the connection errors start.

### The Three Phases

| Phase | When | Who runs it |
| :- | :- | :- |
| 1. Bootstrap | Once, for a new service | A person, by hand, from a terminal |
| 2. Trigger | Once, right after bootstrap | A person, by hand, one command |
| 3. Ongoing | Every release after that | `git push` |

**Phase 1 is mandatory and cannot be replaced by the trigger.** A trigger only swaps the container image. It does not create the service, does not set environment variables, and does not touch secrets. Those must exist first. Any value that can only be known after a service has a public URL, such as a token issuer or a CORS origin, can likewise only be filled in once Phase 1 has run.

**After Phase 2 the division is fixed: the trigger owns the image, the terminal owns the config.** Do not use both paths for the same change. They deploy to the same service, so whichever finishes last wins and the running version stops matching expectations.

### Two Patterns Every Project Keeps

1. **Pass the image tag explicitly through a `_TAG` substitution.** Cloud Build's own `$SHORT_SHA` is populated only for builds started from a connected trigger, not for a manual `gcloud builds submit`. Relying on it in a manual build produces an image reference ending in a bare colon, which Cloud Build rejects with `could not parse reference`. In the trigger, put `_TAG=$SHORT_SHA` in single quotes so the shell does not expand it to an empty string first.

2. **After a successful manual build, record the pushed tag in a local `.last-tag` file**, and on any later config-only redeploy read the tag back from it rather than recomputing from git HEAD. HEAD moves the moment you commit again or open a new shell, and a recomputed tag can point at an image that was never pushed (`Image ... not found`). Git-ignore `.last-tag`; it is a local pointer.

## 2. Prerequisites

Run once per machine.

```bash
gcloud auth login
gcloud config set project [PROJECT_ID]
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

Add these only if the project uses them:

- `secretmanager.googleapis.com` if any value is a secret
- `sqladmin.googleapis.com` if the project connects to Cloud SQL
- `cloudscheduler.googleapis.com` if any work runs on a schedule

## 3. Shell Conventions

Commands here work in both bash and PowerShell. `gcloud` syntax is identical in both. Only variable assignment, interpolation, file writing, and command substitution differ, and those are confined to section 5 and to the table below.

| Operation | bash | PowerShell |
| :- | :- | :- |
| Write `.last-tag` | `echo $TAG > .last-tag` | `Set-Content -NoNewline -Encoding ascii .last-tag $TAG` |
| Read `.last-tag` | `export TAG=$(cat .last-tag)` | `$TAG = Get-Content .last-tag` |
| Call an HTTP endpoint | `curl https://...` | `curl.exe https://...` |
| Conditional chain | `command_a && command_b` | `command_a; if ($?) { command_b }` |

> [!danger]
> **PowerShell `>` writes a byte order mark, and on Windows PowerShell 5.1 often writes UTF-16LE.** Any file whose bytes are read literally is then wrong, and each case fails far from its cause: a secret written with `>` aborts the revision before the container runs with `contains non-UTF8 data` and no application log at all, and a `.last-tag` gains an invisible leading character that surfaces much later as `Image ... not found`. Use `Set-Content -Encoding ascii`, or write with .NET and check the byte count before uploading.

Two more PowerShell traps, because each surfaces far away from its cause:

- **`openssl` is not on PowerShell's `PATH` by default** even though Git for Windows ships it. Add that toolchain's `bin` to `PATH` once rather than writing the full path into a command, per [[docs.rules.md]].
- **`"$IMAGE:$TAG"` is a parse error**, because PowerShell reads `$IMAGE:` as a scoped variable. This runbook avoids it by composing `IMAGE_TAG` once in section 5 and never interpolating around a colon again.
- Any argument containing a comma must be quoted. Writing the quoted form everywhere is correct in both shells.

The same class of problem hits git on Windows: with `core.autocrlf=true` and no `.gitattributes`, a checkout rewrites a shell script to CRLF, the shebang gains a carriage return, and the container reports `no such file or directory` for a script that is plainly present. **Pin `*.sh`, `Dockerfile`, `nginx.conf`, and `.dockerignore` to `eol=lf` in `.gitattributes`.** Only a manual `gcloud builds submit` is affected, because it uploads the working tree, while a trigger clones LF from the remote.

## 4. Configuration Model

Fill in the variant that applies. The other stays in place, marked unused.

### Backend, Config at Runtime

Every environment variable and secret is supplied on the `gcloud run deploy` command through `--set-env-vars`, `--env-vars-file`, or `--set-secrets`. **Never declare one with `ENV` in the `Dockerfile`, never load it from a committed `.env`, and never bake it into the image**, per [[secret.rules.md]].

Use `--env-vars-file` when any value contains a comma, for example a CORS origin list. A comma-separated `--set-env-vars` string splits that value into the wrong variables.

A secret goes through Secret Manager and `--set-secrets`. **A secret whose key contains a `/` is mounted as a file at that path**, not as an environment variable.

**The `cloudbuild.yaml` deploy step deliberately carries none of these flags.** `gcloud run deploy` preserves whatever the service already has, and that is what makes "the trigger owns the image" safe.

### Frontend, Config at Build Time

A static bundle has no server-side process to read environment variables at runtime. The container only serves pre-built files, and the browser runs the already-built JavaScript. **Any API base URL or similar config must be baked in at build time through a `--build-arg`.**

Supplying such a value with `--set-env-vars` does nothing. It reaches the container but nothing reads it, and the JavaScript already shipped to the browser still holds the old baked value. **Changing it means rebuilding, not redeploying.**

Because a build-arg is required, and a plain `gcloud builds submit --tag` cannot pass one, a static frontend always builds through `cloudbuild.yaml`. **Deploy the backend first** so its URL is known.

Declare one `--build-arg` per `ARG` the repository's own `Dockerfile` declares. Do not add a build-arg no code reads: an unknown build-arg is ignored silently, so the value would simply never reach the bundle.

### `_API_BASE_URL` Is an Origin, Never a Path

**`_API_BASE_URL` carries the scheme and the host and nothing else, on every frontend, in every project.**

```text
_API_BASE_URL=https://example.com
```

Never a path, never a route, never a trailing slash:

```text
_API_BASE_URL=https://example.com/api            wrong
_API_BASE_URL=https://example.com/api/v1         wrong
_API_BASE_URL=https://example.com/               wrong
```

The HTTP client holds the origin and appends `api/v1/...` itself, which is the route shape [[api.rules.md]] fixes. The two halves are then joined in exactly one place, in code, under review.

This used to be a judgement call: check what the client expects, then include the suffix or leave it out. That produced a doubled `api/v1/api/v1/...` in one direction and a 404 in the other, both invisible until runtime and both baked into a bundle that only a rebuild can fix. **The rule removes the judgement:** the substitution is always an origin, and the client always appends.

- **A trailing slash matters.** `https://example.com/` joined to `/api/v1` yields `//api/v1` in most clients.
- Set the client's base once, at construction, and never concatenate a base into a call site.
- **The guard step in `cloudbuild.yaml` fails the build on an empty `_API_BASE_URL`.** Extend it to fail on a value containing a path, since a wrong path is as broken as an empty value and takes longer to find.

## 5. Session Variables

Run this block again in every new terminal window. Pick the one matching your shell. Every command after this section is the same in both.

```bash
export PROJECT_ID=[PROJECT_ID]
export REGION=asia-southeast1
export REPOSITORY=[REPOSITORY]
export SERVICE=[SERVICE]
export TAG=$(git rev-parse --short HEAD)
export IMAGE=$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE
export IMAGE_TAG=$IMAGE:$TAG
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export SA=${PROJECT_NUMBER}-compute@developer.gserviceaccount.com
export CLOUDSQL_INSTANCE=[PROJECT_ID]:asia-southeast1:[INSTANCE]
export BUCKET=[BUCKET]
echo "TAG=[$TAG]"
echo "IMAGE_TAG=[$IMAGE_TAG]"
```

```powershell
$PROJECT_ID        = "[PROJECT_ID]"
$REGION            = "asia-southeast1"
$REPOSITORY        = "[REPOSITORY]"
$SERVICE           = "[SERVICE]"
$TAG               = git rev-parse --short HEAD
$IMAGE             = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE"
$IMAGE_TAG         = "${IMAGE}:${TAG}"
$PROJECT_NUMBER    = gcloud projects describe $PROJECT_ID --format="value(projectNumber)"
$SA                = "$PROJECT_NUMBER-compute@developer.gserviceaccount.com"
$CLOUDSQL_INSTANCE = "[PROJECT_ID]:asia-southeast1:[INSTANCE]"
$BUCKET            = "[BUCKET]"
Write-Output "TAG=[$TAG]"
Write-Output "IMAGE_TAG=[$IMAGE_TAG]"
```

**Read both output lines before continuing.** An empty `TAG` means you are not inside the git repository, and the image reference ends in a bare colon, which Cloud Build rejects with `could not parse reference`.

`SA` defaults to the compute service account; 6.4 overrides it when the service gets a dedicated one. Drop `CLOUDSQL_INSTANCE` if the project has no database, and `BUCKET` if it stores no files.

## 6. Phase 1, Bootstrap

Run once, by hand, for a new service.

### 6.1 Set the Project and Region

```bash
gcloud config set project [PROJECT_ID]
gcloud config set run/region asia-southeast1
```

### 6.2 Enable APIs

See section 2. Skip if already done for this project.

### 6.3 Artifact Registry

Once per project, not per service. Skip if the repository already exists.

```bash
gcloud artifacts repositories create [REPOSITORY] --repository-format=docker --location=asia-southeast1
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

The repository also carries a cleanup policy, per [[deploy.rules.md]]. **Without one nothing is ever deleted**, and every build adds a version for as long as the project is worked on.

```bash
gcloud artifacts repositories set-cleanup-policies [REPOSITORY] \
  --location=asia-southeast1 --policy=cleanup-policy.json --dry-run
```

> [!warning]
> Keep `--dry-run` on the first application, read what it reports, and only re-apply without the flag once the list holds nothing a rollback still needs. A deleted image does not come back, and rebuilding from the same commit does not reproduce it, because base images and dependencies move underneath.

Confirm what is in force before trusting it, since a policy that failed to apply leaves no error behind on the repository:

```bash
gcloud artifacts repositories describe [REPOSITORY] --location=asia-southeast1 \
  --format="value(cleanupPolicies,cleanupPolicyDryRun)"
```

`cleanupPolicyDryRun` reading `True` means the policy is listed but deleting nothing.

### 6.4 Dedicated Runtime Service Account

Optional. Only when the service needs permissions the default compute service account should not carry project-wide, for example write access to a single bucket.

```bash
gcloud iam service-accounts create [SERVICE] --display-name="[SERVICE] runtime"
```

The resulting member is `[SERVICE]@[PROJECT_ID].iam.gserviceaccount.com`. Update `SA` in section 5 to this value, and pass `$SA` with `--service-account` on the deploy command. If this section is unused, `SA` keeps its section 5 default and every binding below targets that instead.

### 6.5 Cloud SQL

Only for a project with a database. Create it with **no public IP**, and grant the runtime account `cloudsql.client`.

```bash
gcloud services enable sqladmin.googleapis.com

gcloud sql instances create [INSTANCE] \
  --database-version=POSTGRES_18 \
  --tier=db-f1-micro \
  --region=asia-southeast1 \
  --no-assign-ip \
  --storage-auto-increase

gcloud sql databases create [DB] --instance=[INSTANCE]
gcloud sql users create [USER] --instance=[INSTANCE] --password=[PASSWORD]
```

Put that password straight into Secret Manager in 6.7 and do not keep it anywhere else.

> [!danger]
> **Cloud SQL does not scale to zero.** It is the largest cost on an idle project, and it bills whether anything is using it or not. Stop it when the project goes quiet.

```bash
gcloud sql instances patch [INSTANCE] --activation-policy=NEVER    # stop
gcloud sql instances patch [INSTANCE] --activation-policy=ALWAYS   # start
```

### 6.6 Budget Alert and Cloud Storage

**Set the budget now, not later.** It is the only thing that tells you a mistake is running.

```bash
gcloud billing budgets create \
  --billing-account=[BILLING_ACCOUNT_ID] \
  --display-name="[PROJECT_ID] budget" \
  --budget-amount=[AMOUNT]USD \
  --threshold-rule=percent=0.5 --threshold-rule=percent=0.9
```

A bucket is optional, and only when the project stores uploaded files. Cloud Run instances are stateless and ephemeral, so nothing may be written to local disk.

```bash
gcloud storage buckets create gs://$BUCKET --location=asia-southeast1 --uniform-bucket-level-access
gcloud storage buckets add-iam-policy-binding gs://$BUCKET \
  --member="serviceAccount:$SA" --role="roles/storage.objectUser"
```

**Grant `objectUser` on the bucket, not `storage.admin` on the project.** The scope of the grant is the point.

### 6.7 Secret Manager

Optional. One entry per secret. **Create the secret before deploying**; a revision referencing a missing secret fails to start.

```bash
echo -n "[VALUE]" | gcloud secrets create [SECRET_NAME] --data-file=- --replication-policy=automatic
```

**`echo -n` matters.** Without it the secret carries a trailing newline, and the failure appears far away as an authentication rejection nobody can explain. On PowerShell see the byte order mark warning in section 3.

Rotate by adding a version, then redeploying with the same image:

```bash
echo -n "[NEW_VALUE]" | gcloud secrets versions add [SECRET_NAME] --data-file=-
```

Delete any local value file afterwards. Never commit one, and never print a secret back out, per [[env.rules.md]].

### 6.8 Runtime IAM Bindings

Skip any binding the project does not need. The member is the Cloud Run revision service account, either the dedicated one from 6.4 or the default compute one.

```bash
gcloud secrets add-iam-policy-binding [SECRET_NAME] \
  --member="serviceAccount:$SA" --role="roles/secretmanager.secretAccessor"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA" --role="roles/cloudsql.client"
```

**Without `secretAccessor`, the revision fails to start** with a permission error naming the secret. **Without `cloudsql.client`, the Auth Proxy sidecar cannot authenticate**, the app blocks trying to reach the database, and the container never listens on `PORT`. Cloud Run reports that as a plain startup timeout with no permission error, which is easy to mistake for a port misconfiguration.

IAM changes take a minute or two to propagate.

### 6.9 The env-vars.yaml File

Backend only. Copy the committed example, fill in the real values, and **delete it after deploying**.

```bash
cp env-vars.example.yaml env-vars.yaml
```

The example file is committed and holds placeholders only. The filled copy is git-ignored, holds real values including database passwords, and exists only for the length of a deploy, per [[env.rules.md]].

### 6.10 Build, Push, and Deploy

**Always build through the repository's own `cloudbuild.yaml`, never `gcloud builds submit --tag`.** Both produce an image from the same `Dockerfile`, but only the `cloudbuild.yaml` path runs the deploy step and exercises the exact file the trigger will later use. A broken pipeline file found here is a one-command fix; found after Phase 2, it is a failed production release.

Backend:

```bash
gcloud builds submit --config cloudbuild.yaml --substitutions=_TAG=$TAG
```

Frontend:

```bash
gcloud builds submit --config cloudbuild.yaml "--substitutions=_TAG=$TAG,_API_BASE_URL=$API_BASE_URL"
```

Every other value is already a default inside `cloudbuild.yaml`, so nothing else is passed.

Record the pushed tag. See the shell table in section 3:

```bash
echo $TAG > .last-tag
```

`cloudbuild.yaml` builds, pushes, and deploys, so there is no separate deploy step. Its deploy step carries the allocation from section 1, and deliberately carries no `--env-vars-file` and no `--set-secrets`.

**The first deploy of a backend is the exception:** the service does not exist yet, so environment variables and secrets have to be attached by hand once, from the terminal.

```bash
gcloud run deploy [SERVICE] --image "$IMAGE_TAG" --platform managed --region asia-southeast1 \
  --cpu 1 --memory 1Gi --min-instances 0 --max-instances 4 --concurrency 30 \
  --port 8080 --timeout 60 --add-cloudsql-instances $CLOUDSQL_INSTANCE \
  --env-vars-file env-vars.yaml --set-secrets "[ENV_OR_PATH]=[SECRET_NAME]:latest" \
  --allow-unauthenticated
```

Every later config change repeats this command with the tag read back from `.last-tag`. Every later code change is just a push.

> [!warning]
> **The first Cloud Build on a new service always fails at the deploy step**, because the image does not exist until the build that is currently failing has pushed it. The build itself succeeded. Re-run it, or deploy by hand once as above, and the second attempt goes green.

### 6.11 Values Only Known After the First Deploy

```bash
gcloud run services describe [SERVICE] --region asia-southeast1 --format="value(status.url)"
```

Fill in any setting that needed this service's own public URL, or another service's, such as a token issuer or a CORS origin. Then run the deploy command in 6.10 again with the tag from `.last-tag`.

**For a frontend the equivalent is not a redeploy but a rebuild**, because the value is baked into the bundle.

### 6.12 Cloud Run Jobs

Backend only. A Cloud Run Job runs the app's image to completion and exits, instead of serving requests. Migrations use one, and so does any other piece of work that runs on its own rather than in response to a user.

**Work never runs from the container `CMD` and never from a scheduler thread inside the app.** Running a migration at container start looks convenient and works at one instance. At four instances with `--min-instances=0`, a cold-start burst starts several containers at once and they contend for the migration version table, and a failed migration crash-loops the service instead of failing one visible job. A thread inside the app has the mirror problem: with more than one instance every run happens more than once, and with `--min-instances=0` a scaled-to-zero service never runs it at all.

#### Endpoint or Job

Both patterns are standard. Pick by how the work behaves, not by which is quicker to write.

| The work | Use |
| :- | :- |
| Finishes in a few seconds | An endpoint called by a scheduler, see 6.12.4 |
| Runs longer than the service request timeout | A job |
| Needs more CPU or memory than the service is sized for | A job |
| Would compete with user traffic for an instance | A job |
| Needs retries, or a run split across parallel tasks | A job |
| Must be runnable by hand on demand, such as a migration or a backfill | A job |

A notification scan that reads a few hundred rows is an endpoint. A nightly sweep that walks every open record is a job.

#### The Rules Every Job Follows

1. **One image.** A job runs the same image as its service, with a different entrypoint through `--command` and `--args`. Never build a second image for a job; two images from one repository drift, and the release then has to remember both.
2. **The entrypoint is a module in the app**, run as `python -m app.jobs.[JOB]`. It is code, reviewed and tested like the rest, not a shell one-liner pasted into a flag.
3. **Named `[SERVICE]-[JOB]`**, using the full service name and no abbreviation. Every backend in the project shares one `gcloud run jobs list`, so a shortened name no longer says which service it belongs to, and the name in the runbook stops matching what a release has to execute. That gap stays silent until someone runs the command and is told the job does not exist.
4. **Idempotent, always.** A job retries on failure and a person can run it twice. Doing the same work twice must be impossible. **Guard on the state of the record**, never on the assumption that the job runs once.
5. **Bounded.** A job that scans "everything" grows until it hits its timeout. Give it a date window, a batch size, or both, and make the window a parameter rather than a constant.
6. **Honest exit codes.** Exit `0` only on success. A caught exception that still exits `0` makes a failing job look healthy forever, and nothing raises an alert.
7. **A one-line summary at the end**, naming how many records were considered and how many changed. It is what turns a log into an answer when someone asks whether last night's run worked.
8. **Same config as the service.** Environment variables through `--env-vars-file`, secrets through `--set-secrets`. A job that reads its own config from somewhere else will disagree with the service eventually.
9. **Nothing on local disk.** A job instance is as ephemeral as a service instance.
10. **Run once by hand and read the log** before it is considered done. A job that exists is not a job that works.

Note that `--add-cloudsql-instances` is the flag for `gcloud run deploy`. **On `gcloud run jobs create` the same setting is `--set-cloudsql-instances`**, and passing the deploy spelling is rejected as an unrecognized argument.

#### 6.12.1 The Migration Job

Always named `[SERVICE]-migrate`.

```bash
gcloud run jobs create [SERVICE]-migrate --image "$IMAGE_TAG" --region asia-southeast1 \
  --set-cloudsql-instances $CLOUDSQL_INSTANCE --env-vars-file env-vars.yaml \
  --command alembic --args "upgrade,head"
gcloud run jobs execute [SERVICE]-migrate --region asia-southeast1 --wait
```

Before the first `upgrade,head` on a database that already carries data, read where it actually is:

```bash
gcloud run jobs update [SERVICE]-migrate --region asia-southeast1 --args "current"
gcloud run jobs execute [SERVICE]-migrate --region asia-southeast1 --wait
```

`alembic current` writes nothing. **Run it whenever the applied revision is not known with certainty**, because `upgrade head` on a database further behind than assumed replays every revision in between, and one of those may drop a column. Switch the args back once the answer is in.

#### 6.12.2 A Purpose-Built Job

```bash
gcloud run jobs create [SERVICE]-[JOB] --image "$IMAGE_TAG" --region asia-southeast1 \
  --service-account $SA --set-cloudsql-instances $CLOUDSQL_INSTANCE \
  --env-vars-file env-vars.yaml --set-secrets "[ENV_OR_PATH]=[SECRET_NAME]:latest" \
  --command python --args "-m,app.jobs.[JOB]" \
  --cpu 1 --memory 1Gi --task-timeout 900s --max-retries 3 --tasks 1 --parallelism 1
gcloud run jobs execute [SERVICE]-[JOB] --region asia-southeast1 --wait
```

On the flags that matter:

- **`--task-timeout` must exceed the realistic worst case, not the average.** A job killed at the timeout has already done half its work, and rule 4 is what makes the retry safe.
- **`--max-retries` defaults to 3. Keep it and make the job idempotent**, rather than setting it to 0 to avoid thinking about repeats.
- **`--tasks` and `--parallelism` stay at 1** unless the work genuinely splits into independent shards. A job that writes to one table is not one of those.
- `--service-account` is the same runtime account as the service, so the job reaches the same secrets and the same database with the same permissions.

Read the log of that first run before scheduling it:

```bash
gcloud run jobs executions list --job [SERVICE]-[JOB] --region asia-southeast1 --limit 3
gcloud logging read 'resource.type="cloud_run_job" AND resource.labels.job_name="[SERVICE]-[JOB]"' \
  --limit 50 --freshness 1h
```

#### 6.12.3 Scheduling a Job

Cloud Scheduler calls the Cloud Run Admin API to start a job. It is a different call from hitting an endpoint: the target is the API, and it authenticates with OAuth as a service account rather than with a shared token.

```bash
gcloud services enable cloudscheduler.googleapis.com
gcloud run jobs add-iam-policy-binding [SERVICE]-[JOB] --region asia-southeast1 \
  --member="serviceAccount:$SA" --role="roles/run.invoker"
gcloud scheduler jobs create http [SERVICE]-[JOB]-sched --location asia-southeast1 \
  --schedule "0 22 * * *" --time-zone "Asia/Jakarta" \
  --uri "https://run.googleapis.com/v2/projects/$PROJECT_ID/locations/asia-southeast1/jobs/[SERVICE]-[JOB]:run" \
  --http-method POST --oauth-service-account-email $SA
```

- **Always set the time zone.** A cron expression with no time zone runs in UTC, which puts a "10pm" job at 5am local.
- Without `roles/run.invoker` on the job, the scheduler reports a `PERMISSION_DENIED` that names the API rather than the missing binding.
- The scheduler entry is named `[SERVICE]-[JOB]-sched`, so one listing says which service and which job each entry drives.

**Run it once by hand and confirm the job actually executed**, not just that the scheduler returned success:

```bash
gcloud scheduler jobs run [SERVICE]-[JOB]-sched --location asia-southeast1
gcloud run jobs executions list --job [SERVICE]-[JOB] --region asia-southeast1 --limit 1
```

#### 6.12.4 Recurring Work as an Endpoint

For work that finishes in seconds, expose it as an endpoint and let the scheduler call it.

```bash
gcloud scheduler jobs create http [SERVICE]-[JOB] --location asia-southeast1 \
  --schedule "0 22 * * *" --time-zone "Asia/Jakarta" \
  --uri "https://[HOST]/api/v1/jobs/[JOB]" --http-method POST \
  --headers "X-Job-Token=$JOB_TOKEN" --attempt-deadline 300s
```

**The endpoint is authenticated, never public.** [[security.rules.md]] allows only the health and login routes to be open, and a job endpoint anyone can POST to is a way to trigger work from outside.

Always run it once by hand and read the answer:

```bash
gcloud scheduler jobs run [SERVICE]-[JOB] --location asia-southeast1
gcloud logging read 'resource.type="cloud_scheduler_job"' --limit=5 --freshness=10m
```

**Read the status the app returned, not just the one the scheduler reports.** A 401 means the token never matched. A 400 is often the job's own guard refusing to run at the wrong hour, which is the job working, not failing.

#### Updating a Job on Release

**A job pins the image it was created with**, so a release that changes job code has to move the job forward too. That does not happen through the trigger.

```bash
gcloud run jobs update [SERVICE]-[JOB] --image "$IMAGE_TAG" --region asia-southeast1
```

**Update every job the repository owns, not only the migration one.** A job left on an old image keeps running last month's code against this month's schema, and nothing reports it. List them and check:

```bash
gcloud run jobs list --region asia-southeast1 \
  --format="table(name,template.template.containers[0].image)"
```

### 6.13 Domain Mapping

Cloud Run supports custom domain mapping in `asia-southeast1`. **This is the reason the region is Singapore and not Jakarta**, where mapping is unavailable.

```bash
gcloud beta run domain-mappings create --service [SERVICE] --domain [HOST] --region asia-southeast1
```

Add the DNS records the command prints, then wait for the certificate to be issued. A frontend is `[app].example.com`; a backend is `[app]-api.example.com`.

**Cross-service single sign-on depends on this.** The session cookie is scoped to the shared domain, so it will never reach a bare platform host. Do not enable single sign-on on either side until both are on the domain, per [[auth.rules.md]].

### 6.14 Verify

```bash
gcloud run services describe [SERVICE] --region asia-southeast1
curl https://[HOST]/health
```

Check that CPU, memory, max-instances, and concurrency match section 1, and that the database is still attached.

**For a frontend, open the service URL in a private window and check in the browser network tab that API requests go to the backend host, not to the frontend's own origin.** A request answered with `index.html` means the bundle was built with an empty or relative base URL.

### 6.15 Clean Up Local Files

```bash
rm env-vars.yaml
```

It holds real values once filled in. Delete it rather than letting it sit on disk. Delete any local key or credential file generated in 6.7 as well.

## 7. Phase 2, Connect the Trigger

Run once per service.

### 7.1 Do Not Use the Console Continuous Deployment Button

The "Set up Continuous Deployment" button in the Cloud Run console generates an inline build config stored inside the trigger, which:

- ignores the repository's `cloudbuild.yaml` entirely
- pushes to a separate `cloud-run-source-deploy` repository
- passes none of the substitutions the project declares
- for a static frontend, runs a plain `docker build` with no `--build-arg`, silently producing a broken bundle on every push
- sets `substitutionOption: ALLOW_LOOSE`, so nothing fails loudly

### 7.2 Check What Already Exists

**A trigger's own region is independent of the deploy region.** `cloudbuild.yaml` sets the deploy region, so a trigger in `global` still deploys to Singapore. Console-created triggers live in `global`, so a regional listing looks empty even when triggers exist.

```bash
gcloud builds triggers list --region=global --format="table(name,filename,substitutions)"
```

**An empty `filename` column means an inline trigger** that must be converted.

### 7.3 Create the Trigger

Trigger names follow `[REPO_NAME]-[BRANCH]`. A service has exactly one trigger per deployed environment: `[REPO_NAME]-main` for production, and `[REPO_NAME]-staging` where a staging environment exists, per [[branch.rules.md]]. No other branch pattern is permitted.

**A trigger must name the service account that runs its builds.** The legacy build account is no longer provisioned in a new project, so a trigger created without `--service-account` is rejected with `INVALID_ARGUMENT: Request contains an invalid argument` and nothing in the message says which argument.

Backend:

```bash
gcloud builds triggers create github --name=[REPO_NAME]-main --region=global \
  --repo-owner=[OWNER] --repo-name=[REPO_NAME] --branch-pattern='^main$' \
  --build-config=cloudbuild.yaml \
  --service-account=projects/[PROJECT_ID]/serviceAccounts/$SA \
  --substitutions='_TAG=$SHORT_SHA'
```

Frontend:

```bash
gcloud builds triggers create github --name=[REPO_NAME]-main --region=global \
  --repo-owner=[OWNER] --repo-name=[REPO_NAME] --branch-pattern='^main$' \
  --build-config=cloudbuild.yaml \
  --service-account=projects/[PROJECT_ID]/serviceAccounts/$SA \
  --substitutions='_TAG=$SHORT_SHA,_API_BASE_URL=[BACKEND_BASE_URL]'
```

The build account needs `roles/artifactregistry.writer` to push the image, `roles/run.admin` to deploy the revision, `roles/iam.serviceAccountUser` on the runtime account to deploy as it, and `roles/logging.logWriter` to write build logs. The default compute account already carries all four in most projects; confirm before assuming it.

**The single quotes around `--substitutions` and `--branch-pattern` are required.** With double quotes the shell expands `$SHORT_SHA` to an empty string before Cloud Build sees it, and the image reference ends in a bare colon.

Every substitution the trigger passes must be declared in `cloudbuild.yaml`. Every substitution that is not passed must have a real default there. **Keeping the passed set this small is deliberate:** a value that lives in both the trigger and the repository can disagree, and the trigger is not under version control.

### 7.4 Convert an Existing Inline Trigger

```bash
gcloud builds triggers update github [EXISTING_TRIGGER_NAME] --region=global \
  --build-config=cloudbuild.yaml --substitutions='_TAG=$SHORT_SHA'
```

Remove the leftover console substitutions: `_AR_HOSTNAME`, `_AR_PROJECT_ID`, `_AR_REPOSITORY`, `_DEPLOY_REGION`, `_PLATFORM`, `_SERVICE_NAME`. The repository's `cloudbuild.yaml` does not declare them, and an undeclared substitution fails the build once `ALLOW_LOOSE` no longer applies.

### 7.5 Verify the Trigger

**Verifying that the build turned green is not enough.**

```bash
git commit --allow-empty -m "chore: test the deploy trigger"
git push origin main
gcloud builds list --region=global --limit=3
gcloud run services describe [SERVICE] --region asia-southeast1 \
  --format="value(spec.template.spec.containers[0].image)"
```

The image must come from the project's own Artifact Registry repository, not from `cloud-run-source-deploy`. Then confirm the config survived the automated deploy: call the health endpoint, and exercise one feature that depends on an environment variable or a secret.

## 8. Phase 3, Ongoing Releases

### 8.1 Code Change

```bash
git push origin main
```

That is the whole procedure, with one exception. **If the release carries a new migration revision, run the migration job from 6.12 first, then push.** Migrating after the push leaves the new code running against the old schema.

### 8.2 Config-Only Change

Backend only. Editing environment variables, rotating a secret, or changing CPU or memory never requires a rebuild, because the trigger does not touch config. Reuse the image already deployed.

```bash
export TAG=$(cat .last-tag)
```

Then apply the change and re-run the deploy command from 6.10. If `.last-tag` is stale or missing, read the tag from what is actually running:

```bash
gcloud run services describe [SERVICE] --region asia-southeast1 \
  --format="value(spec.template.spec.containers[0].image)"
```

### 8.3 Build-Time Config Change

Frontend only. **Changing the baked API base URL, the product name, or a build-time flag is not a config change and cannot be fixed by redeploying.**

If the value is a `cloudbuild.yaml` default, edit it, commit, and push. If it is `_API_BASE_URL`, update the trigger substitution and push a commit to force a rebuild:

```bash
gcloud builds triggers update github [REPO_NAME]-main --region=global \
  --substitutions='_TAG=$SHORT_SHA,_API_BASE_URL=[NEW_URL]'
```

## 9. Troubleshooting

**The trigger goes green but the deployed service behaves like an older or broken build.** The trigger is probably inline rather than pointing at `cloudbuild.yaml`. Run `gcloud builds triggers describe [NAME] --region=global`. An inline trigger shows a `build:` block and no `filename:`. Convert it, see 7.4.

**`if 'build.service_account' is specified, the build must use either CLOUD_LOGGING_ONLY / NONE logging options`.** This fails before any step runs, right after converting an inline trigger. A trigger runs the build under an explicit service account, and Cloud Build then refuses the legacy default logs bucket. `cloudbuild.yaml` must declare a logging mode:

```yaml
options:
  logging: CLOUD_LOGGING_ONLY
```

The console's inline config had this; a hand-written `cloudbuild.yaml` often does not.

**A static frontend calls its own origin, and the browser reports a failed fetch.** The bundle was built without a usable API base URL, so the HTTP client has an empty base and hits the frontend's own origin, where the single-page fallback answers with `index.html`. Either the trigger is inline, so no build-arg was passed, or the build ran with the URL substitution empty. **Rebuild with the correct value; redeploying cannot fix a value already baked into the bundle.** The guard step in `cloudbuild.yaml` exists to stop this at build time.

**`Image '...:XXXXXXX' not found`.** `TAG` was recomputed from git HEAD after it moved past the commit that was actually built, or `.last-tag` was written with a byte order mark. List what is really in Artifact Registry and deploy from that:

```bash
gcloud artifacts docker images list $IMAGE --include-tags --limit=5
```

**`could not parse reference: ...service:`** with a trailing colon and empty tag. The build ran without a tag because it relied on `$SHORT_SHA` in a manual submit, or because `--substitutions` used double quotes and the shell consumed it. Pass `_TAG` explicitly, in single quotes for a trigger.

**`The user-provided container failed to start and listen on the port ... within the allocated timeout`.** Cloud Run reports only the symptom. Read the real cause first:

```bash
gcloud run services logs read [SERVICE] --region asia-southeast1 --limit=100
```

Common causes: a missing `cloudsql.client` binding, so the app blocks on a database it cannot reach; a bad connection string; or the app not reading the `PORT` variable Cloud Run injects.

**`Setting IAM policy failed, try gcloud beta run services add-iam-policy-binding`.** `--allow-unauthenticated` deployed the revision but could not also grant public invoke access, usually because an organization policy blocks `allUsers`. Retry the exact command gcloud printed. **If a service is meant to be public, do not make it authenticated as a workaround.** Ask whoever manages the organization for an exception on this project.

**A cookie set by the API host never reaches the frontend.** A session cookie is host-only unless a domain is set, and a domain cookie only crosses hosts that share it. Until both halves are domain-mapped, the API host needs its own login path, per [[auth.rules.md]].

## 10. Rules and Deviations

- **Region is always `asia-southeast1`.** Never deploy elsewhere.
- Backend is `--cpu 1 --memory 1Gi --max-instances 4-5 --concurrency 25-30`. Frontend is `--cpu 1 --memory 512Mi --max-instances 2 --concurrency 80-100`. Do not change any of those four values without a documented reason in the project README.
- For a backend on a managed database, `max-instances x (pool size + max overflow)` is the connection budget, shared with every other service on that instance.
- **Bootstrap by hand once, then let the trigger own every subsequent release.** Do not run both paths for the same change.
- **The trigger must point at the repository's `cloudbuild.yaml`.** An inline trigger generated by the console is not acceptable: it bypasses version control and drops every substitution.
- One trigger per service per deployed environment, named `[REPO_NAME]-[BRANCH]`, watching `^main$` or `^staging$`.
- **A `cloudbuild.yaml` serving two environments carries a guard step** that whitelists the legal substitution combinations by name and fails the build on anything else. Without it a trigger that loses its substitutions deploys the staging branch to the production service, and the build goes green.
- **A non-production environment uses its own database, bucket, queue, signing keys, and runtime service account.** Sharing any of them makes the lower environment a path into the higher one.
- `--max-instances` is a substitution wherever two environments differ. `cloudbuild.yaml` sets it on every deploy, so a limit that is not a substitution is silently restored on the next push, and the connection budget goes with it.
- `_API_BASE_URL` is an origin and nothing else. Never a path, never a route, never a trailing slash.
- **The image must live in Artifact Registry, tagged with an explicit tag** passed as a substitution. Record it in `.last-tag`. Never rely on `$SHORT_SHA` for manual builds. **Never deploy `:latest` to production.**
- All environment variables and secrets go through the deploy command only. **Never in the `Dockerfile`, in a compose file, or in a committed `.env`.**
- A secret goes through Secret Manager, and the runtime account must hold `roles/secretmanager.secretAccessor`. A database app also needs `roles/cloudsql.client`.
- **Static frontend config is baked at build time.** Changing it means rebuilding, not redeploying.
- **Migrations run as a Cloud Run Job, never from the container `CMD`**, named `[SERVICE]-migrate` with the full service name.
- Any other work that runs on its own is either a job or an endpoint called by a scheduler, chosen by the table in 6.12. **It is never a scheduler thread inside the app.**
- A job runs the same image as its service with a different entrypoint, is named `[SERVICE]-[JOB]`, and its entrypoint is a reviewed module rather than a shell line in a flag.
- **Every job is idempotent and bounded**, exits non-zero on failure, and logs a one-line summary of how many records it considered and changed.
- A scheduled job is driven through the Cloud Run Admin API with an OAuth service account holding `roles/run.invoker` on that job, and its entry is named `[SERVICE]-[JOB]-sched` with an explicit time zone.
- **Every job and scheduler entry is run once by hand and its log read** before it is considered done.
- **Every job is listed in the section 1 table**, and every job is moved to the new image on a release that changes its code. The trigger does not update a job.
- **A budget alert exists before the first deploy.**
- **Never save or commit a filled-in copy of this runbook**, or the `env-vars.yaml` it creates, containing a real value.

Each project copy ends this section with its own documented deviations from the rules above, and the reason for each.

## Related

- [[deploy.rules.md]]
- [[docs.rules.md]]
- [[secret.rules.md]]
- [[env.rules.md]]
- [[security.rules.md]]
- [[api.rules.md]]
- [[auth.rules.md]]
- [[branch.rules.md]]
- [[database.rules.md]]
