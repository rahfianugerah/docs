> Up: [[README.md]]

# Cloud Run Runbook

![Cloud Run](https://img.shields.io/badge/Cloud_Run-Serverless-4285F4?logo=googlecloud&logoColor=white)
![Region](https://img.shields.io/badge/Region-asia--southeast1-4285F4?logo=googlecloud&logoColor=white)

> [!important]
> The Cloud Run runbook itself, copied into each repository and kept comparable line for line.

Copy and paste, top to bottom. Implements [[deploy.rules.md]]; when the two disagree, that file is the rule and this one is the mistake.

Replace every `[BRACKET]` before running anything.

## 1. Session Variables

Run this again in every new terminal.

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
export CLOUDSQL_INSTANCE=$PROJECT_ID:$REGION:[INSTANCE]
echo "IMAGE_TAG=[$IMAGE_TAG]"
```

Read that last line. An empty `TAG` means you are not inside the git repository, and the image reference ends in a bare colon, which Cloud Build rejects with `could not parse reference`.

PowerShell differs only in assignment. Note `"${IMAGE}:${TAG}"` with braces: `"$IMAGE:$TAG"` is a parse error, because PowerShell reads `$IMAGE:` as a scoped variable.

```powershell
$PROJECT_ID = "[PROJECT_ID]"
$REGION     = "asia-southeast1"
$REPOSITORY = "[REPOSITORY]"
$SERVICE    = "[SERVICE]"
$TAG        = git rev-parse --short HEAD
$IMAGE      = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE"
$IMAGE_TAG  = "${IMAGE}:${TAG}"
```

## 2. One-Time Project Setup

```bash
gcloud auth login
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com    # if the project uses secrets

gcloud artifacts repositories create $REPOSITORY --repository-format=docker --location=$REGION
```

### Cloud SQL

Only for a project with a database. Create it with **no public IP**, and grant the runtime account `cloudsql.client`.

```bash
gcloud services enable sqladmin.googleapis.com

gcloud sql instances create [INSTANCE] \
  --database-version=POSTGRES_17 \
  --tier=db-f1-micro \
  --region=$REGION \
  --no-assign-ip \
  --storage-auto-increase

gcloud sql databases create [DB] --instance=[INSTANCE]
gcloud sql users create [USER] --instance=[INSTANCE] --password=[PASSWORD]

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA" --role="roles/cloudsql.client"
```

Put that password straight into Secret Manager in section 3 and do not keep it anywhere else.

**Cloud SQL does not scale to zero.** It is the largest cost on an idle project. Stop it when the project goes quiet:

```bash
gcloud sql instances patch [INSTANCE] --activation-policy=NEVER    # stop
gcloud sql instances patch [INSTANCE] --activation-policy=ALWAYS   # start
```

### Budget Alert

Do this now, not later. It is the only thing that tells you a mistake is running.

```bash
gcloud billing budgets create \
  --billing-account=[BILLING_ACCOUNT_ID] \
  --display-name="$PROJECT_ID budget" \
  --budget-amount=[AMOUNT]USD \
  --threshold-rule=percent=0.5 --threshold-rule=percent=0.9
```

### Image Cleanup Policy

Artifact Registry charges for storage and old tags accumulate forever.

```bash
gcloud artifacts repositories set-cleanup-policies $REPOSITORY --location=$REGION \
  --policy=<(echo '[{"name":"keep-recent","action":{"type":"Keep"},"mostRecentVersions":{"keepCount":5}}]')
```

## 3. Secrets

One secret per value. Create it before deploying; a revision referencing a missing secret fails to start.

```bash
echo -n "[VALUE]" | gcloud secrets create [SECRET_NAME] --data-file=- --replication-policy=automatic
gcloud secrets add-iam-policy-binding [SECRET_NAME] \
  --member="serviceAccount:$SA" --role="roles/secretmanager.secretAccessor"
```

`echo -n` matters. Without it the secret carries a trailing newline, and the failure appears far away as an authentication rejection nobody can explain.

Rotate by adding a version, then redeploying with the same image:

```bash
echo -n "[NEW_VALUE]" | gcloud secrets versions add [SECRET_NAME] --data-file=-
```

Never print a secret back out. See [[env.rules.md]].

## 4. Build and Deploy

Always through `cloudbuild.yaml`, never `gcloud builds submit --tag`.

```bash
gcloud builds submit --config cloudbuild.yaml --substitutions=_TAG=$TAG
echo $TAG > .last-tag
```

`.last-tag` is gitignored, and it is what a later config-only deploy reads. Recomputing the tag from git HEAD after committing again points at an image that was never built.

The first deploy attaches the configuration, because `cloudbuild.yaml` deliberately carries none.

**Backend**, 1 vCPU and 1Gi, concurrency 30, with Cloud SQL attached:

```bash
gcloud run deploy $SERVICE \
  --image "$IMAGE_TAG" \
  --region $REGION \
  --platform managed \
  --cpu 1 --memory 1Gi \
  --min-instances 0 --max-instances 5 \
  --concurrency 30 \
  --port 8080 \
  --timeout 60 \
  --add-cloudsql-instances $CLOUDSQL_INSTANCE \
  --set-env-vars "LOG_LEVEL=INFO,DB_NAME=[DB],DB_USER=[USER],CLOUDSQL_INSTANCE=$CLOUDSQL_INSTANCE" \
  --set-secrets "DB_PASSWORD=[SECRET_NAME]:latest" \
  --allow-unauthenticated
```

**Frontend**, 512Mi, concurrency 80, no database:

```bash
gcloud run deploy $SERVICE-frontend \
  --image "$IMAGE-frontend:$TAG" \
  --region $REGION \
  --platform managed \
  --cpu 1 --memory 512Mi \
  --min-instances 0 --max-instances 5 \
  --concurrency 80 \
  --port 8080 \
  --timeout 60 \
  --allow-unauthenticated
```

`--port 8080` is the Cloud Run default and is stated here so it is visible rather than assumed. The container still has to read the injected `PORT` variable; the flag tells Cloud Run which port to send traffic to, it does not tell the app which port to open.

Drop `--allow-unauthenticated` for anything that is not meant to be public. A public endpoint on a personal project is a public endpoint on your bill.

A static frontend bakes its configuration in at build time through a `--build-arg`, so `--set-env-vars` on a frontend does nothing. Changing the API URL means rebuilding, not redeploying.

## 5. Verify

```bash
curl $(gcloud run services describe $SERVICE --region $REGION --format="value(status.url)")/health
gcloud run services describe $SERVICE --region $REGION \
  --format="value(spec.template.spec.containers[0].image)"
```

Confirm the image is the tag you just built, and that `/health` answers.

## 6. Jobs

For a migration, a batch scan, or any work that runs to completion and exits. A job runs the **same image** with a different entrypoint; never build a second image.

```bash
gcloud run jobs create $SERVICE-[JOB] \
  --image "$IMAGE_TAG" \
  --region $REGION \
  --service-account $SA \
  --set-cloudsql-instances $CLOUDSQL_INSTANCE \
  --set-env-vars "LOG_LEVEL=INFO,DB_NAME=[DB],DB_USER=[USER],CLOUDSQL_INSTANCE=$CLOUDSQL_INSTANCE" \
  --set-secrets "DB_PASSWORD=[SECRET_NAME]:latest" \
  --command python --args "-m,app.jobs.[JOB]" \
  --cpu 1 --memory 1Gi \
  --task-timeout 900s --max-retries 3 --tasks 1 --parallelism 1

gcloud run jobs execute $SERVICE-[JOB] --region $REGION --wait
```

- `--set-cloudsql-instances` is the flag on a job; `--add-cloudsql-instances` is the deploy flag and is rejected here.
- **Make the job idempotent.** It retries up to `--max-retries` and you can run it twice by hand.
- A job pins its image. A release that changes job code updates the job too:

```bash
gcloud run jobs update $SERVICE-[JOB] --image "$IMAGE_TAG" --region $REGION
```

Schedule one through Cloud Scheduler against the Admin API, not an HTTP endpoint:

```bash
gcloud services enable cloudscheduler.googleapis.com
gcloud run jobs add-iam-policy-binding $SERVICE-[JOB] --region $REGION \
  --member="serviceAccount:$SA" --role="roles/run.invoker"
gcloud scheduler jobs create http $SERVICE-[JOB]-sched \
  --location $REGION \
  --schedule "0 22 * * *" --time-zone "Asia/Jakarta" \
  --uri "https://run.googleapis.com/v2/projects/$PROJECT_ID/locations/$REGION/jobs/$SERVICE-[JOB]:run" \
  --http-method POST --oauth-service-account-email $SA
```

`--time-zone` is not optional. Without it the schedule runs in UTC, putting a 10pm job at 5am local.

## 7. Ongoing

**Code change:** rebuild and redeploy.

```bash
gcloud builds submit --config cloudbuild.yaml --substitutions=_TAG=$TAG && echo $TAG > .last-tag
```

**Config or secret change:** no rebuild. Reuse the deployed image.

```bash
export TAG=$(cat .last-tag)
# then re-run the gcloud run deploy command from section 4
```

**Rollback:** deploy an older tag.

```bash
gcloud artifacts docker images list $IMAGE --include-tags --limit=10
gcloud run deploy $SERVICE --image "$IMAGE:[OLDER_TAG]" --region $REGION
```

## 8. Troubleshooting

**`The user-provided container failed to start and listen on the port`.** Almost always the app hardcoding a port instead of reading `PORT`. Read the real cause:

```bash
gcloud run services logs read $SERVICE --region $REGION --limit=100
```

Other causes: a missing `secretAccessor` binding, or the app blocking on something unreachable at startup.

**`could not parse reference: ...service:`** with a trailing colon. The build ran with an empty `_TAG`. Pass it explicitly.

**`Image '...:XXXXXXX' not found`.** `TAG` was recomputed after HEAD moved past what was built. List what actually exists:

```bash
gcloud artifacts docker images list $IMAGE --include-tags --limit=5
```

**Build fails immediately with a message about the logs bucket.** The build runs under an explicit service account and needs a logging mode in `cloudbuild.yaml`:

```yaml
options:
  logging: CLOUD_LOGGING_ONLY
```

**`Permission denied on secret`.** The runtime service account lacks `secretAccessor` on that secret. Grant it and redeploy; IAM takes a minute to propagate.

**The bill is higher than expected.** Check for a service without `--min-instances 0`, a Cloud SQL instance left running, or a `--max-instances` that let a loop scale.

```bash
gcloud run services list --format="table(name,region,spec.template.metadata.annotations)"
```

## Related

- [[deploy.rules.md]]
- [[cloudbuild.service.template.yaml]]
- [[cloudbuild.job.template.yaml]]
- [[secret.rules.md]]
- [[env.rules.md]]
