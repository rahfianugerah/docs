---
tags:
  - kind/pattern
  - layer/infra
  - topic/deploy
---

# A release carrying a migration is built off the release branch first

> [!warning]
> The migration job has to finish before the new code serves traffic, or every request fails against a table that does not exist yet.

The obvious order cannot be run. The job needs an image containing the new revision, and no such image exists until a build has produced one, while a push to the release branch builds and deploys in the same pipeline.

**Build from the development branch instead.** The trigger only watches the release branch, so it does not fire:

```bash
git checkout dev
gcloud builds submit --config cloudbuild.yaml --substitutions=_TAG=$(git rev-parse --short HEAD)
gcloud run jobs update  <service>-migrate --image "$IMAGE_TAG" --region <region>
gcloud run jobs execute <service>-migrate --region <region> --wait
```

Only then promote. The trigger rebuilds the same commit onto a schema that is already migrated.

Two things about this sequence are easy to get wrong:

- **The database flag is spelled differently on each command, and the error names neither.** The deploy command takes `--add-cloudsql-instances`, while the jobs command accepts only `--set-cloudsql-instances`.
- **A release that also adds a secret needs one manual deploy after the promotion.** A push never installs a new secret, because the trigger never touches configuration.

**Why:** a runbook that says "run the migration job before pushing" is impossible as written, and nothing records that the job's image does not exist yet at that point. The failure surfaces as every authenticated request breaking after a green build.

**Applies to:** any release that adds a schema revision, on any platform where one pipeline both builds and deploys.

**Source:** an incident outside this repository. The ordering constraint is visible in any pipeline that builds and deploys in a single trigger.

## Related

- [[deploy.cloud.md]]
- [[database.rules.md]]
- [[branch.rules.md]]
- [[the-first-build-on-a-new-service-fails-at-the-deploy-step.pattern.md]]
