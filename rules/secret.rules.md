---
tags:
  - kind/rule
  - layer/infra
  - topic/security
---

> Up: [[README.md]]

# Secret and Configuration Standard

> [!warning]
> API keys, signing keys, and `.pem` files live in a secret manager. A frontend bundle holds no secrets at all, because everything in it is public.

## Core Requirement

Every value a project needs at runtime is either a **secret** or **configuration**. This standard decides which one a value is, and where each kind lives.

Nothing real is ever hardcoded, committed, or baked into an image. A backend receives every value at deploy time. A frontend receives no secrets at all.

> [!danger]
> A secret that was committed, pasted, or shown on a screen share is compromised. Rotating it takes minutes; finding out later does not.

This standard owns the classification. The surrounding standards own the rest, and this file does not repeat them:

| Standard | Owns |
| :- | :- |
| [[env.rules.md]] | Why a real environment file is never read, and what `.env.example` may contain |
| [[security.rules.md]] | That a secret never appears in source, a compose file, or a UI, and that a leaked one is rotated |
| [[commit.rules.md]] | That a key file or an environment file is never committed |
| [[deploy.rules.md]], [[deploy.cloud.md]] | The deploy mechanics: setting environment variables, mounting secrets, and the IAM bindings |
| [[stacks.rules.md]] | That configuration is read once into a typed settings object |

## The Test

**Is the value a key?**

If holding it lets someone authenticate as you, sign what you would sign, decrypt what you can decrypt, or spend your money, it is a **secret**. If it only says where to connect or how to behave, it is **configuration**.

Classify by what possession allows, not by how sensitive the value feels.

## The Two Tiers

| Tier | Holds | Stored in | Delivered by |
| :- | :- | :- | :- |
| Secret | Key material | A secret manager | A secret mount on the deploy command |
| Configuration | Everything else | The deploy command | An environment variable or an env-vars file |

An environment variable on a managed runtime is readable by anyone who can describe the service. That is acceptable for configuration, and it is exactly why key material does not go there.

## Secrets

These always go through a secret manager, never a plain environment variable:

- An API key or token for a third party: a model provider key, a payment gateway key, a webhook signing secret, a dataset host token, an experiment tracker key.
- An API key this service issues to another service, per the machine-to-machine rules in [[security.rules.md]].
- A token signing key. For RS256 this is the private half; the public half is published at the discovery endpoint per [[auth.rules.md]] and is not a secret.
- Any private key or certificate file: `.pem`, `.key`, `.p12`, `.pfx`, `.jks`.
- A cloud service account JSON key, where one is genuinely unavoidable. Prefer workload identity and no key at all.
- A session or cookie signing secret. Forging it forges sessions, so it is key material even though it is not called a key.
- A standalone password, including an SMTP password and a database password. See "Where a Value Is Both" below.
- A password hash pepper.

Rules:

1. **One secret per value.** Never bundle several into one JSON blob, because they then rotate and audit as one thing.
2. **Create the secret before the deploy.** A revision that references a missing secret fails to start.
3. **Grant the runtime identity read access on the secret**, and nothing wider. Without it the revision fails with a permission error that names the secret rather than the binding, per [[deploy.cloud.md]].
4. **Reference the latest version by default.** Pin an explicit version when a rollback has to be deterministic.
5. **A key the app needs as a file is mounted as a file.** Point the app's configuration at that path rather than reading the value into a variable and writing it out again.
6. **Rotate by adding a new version and redeploying.** That is a config-only change, so it reuses the deployed image and never needs a rebuild.
7. **Never print a secret value** into a terminal, a log, a notebook output, a traceback, a pull request, an issue, or a chat message, including through the secret manager's own read command.
8. **Never in source code.** Not in a constant, not in a notebook cell, not in a docstring, not in a comment, not in a test fixture.
9. **One secret per project and per environment.** A single key shared across five projects cannot be revoked without breaking four of them.

### Where a Secret Actually Lives

In order of preference:

1. **A secret manager**, where the project has one available: a cloud secret manager, 1Password, `pass`, the OS keychain. Best for anything shared between machines or that outlives a project.
2. **A gitignored `.env`**, for local development. Fine for a personal project on one machine, and the default for local work.
3. **An environment variable set by the platform**, for CI and deployment. Never committed to the workflow file; use the platform's own secret store.

Never a fourth option. Not a config file "outside the repo but next to it", not a note, not a chat message to yourself.

## Configuration

Everything that is not key material. It is supplied directly on the deploy command and does not need a secret manager.

- A database connection string and its parameters: host, port, database name, user.
- A service URL or hostname, such as an identity provider base URL or a key set URL.
- A CORS origin list.
- A token issuer and audience string. These are identity strings, not credentials, per [[auth.rules.md]].
- A bucket name, a region, a project identifier.
- A data directory, an output directory, a checkpoint path.
- A model name, a batch size, a learning rate, a seed.
- A feature flag, a timeout, a page size, a log level.
- A session cookie name or lifetime. The cookie's **signing secret** is a secret; its name and lifetime are not.

Rules:

1. Supply configuration on the deploy command. Use an env-vars file when any value contains a comma, because a comma inside a flat variable list splits the value into the wrong variables.
2. **Never declare one with `ENV` in the `Dockerfile`**, never load a committed `.env`, and never bake one into the image.
3. Read every variable once into a typed settings object, per [[stacks.rules.md]] and [[codes.rules.md]]. Do not scatter `os.getenv` through the code.
4. Fail fast at startup when a required variable is missing or still holds its default, per [[security.rules.md]].
5. List every variable name in `.env.example` with a placeholder value, per [[env.rules.md]].
6. **Do not promote a configuration value into a secret manager because it looks sensitive.** A URL in a secret manager costs a rotation procedure and an access binding and buys nothing.

## Where a Value Is Both

A database connection string is configuration, but a password embedded in it is key material. The two halves of that sentence pull in different directions, so decide it deliberately rather than by habit.

Order of preference:

1. **No password at all.** Where the database supports identity-based authentication, use it. That removes the password from the connection string entirely, which is the only option that makes the question go away.
2. **Split the value.** Keep host, port, database name, and user as configuration, put the password alone in the secret manager, and assemble the URL in the settings object.
3. **The whole string as one environment variable.** Simplest, and the default this standard allows for a database connection. Accept that the password is then visible to anyone who can read the service configuration.

Choose the first where the database supports it. Where the third is used, record that choice in the project README, because it is the one place this standard knowingly leaves a credential in an environment variable.

The same reasoning applies to any other connection string that embeds a password, such as an SMTP URL.

## A Frontend Holds No Secrets

A static single-page app has no server-side process. Every build-time variable is baked into the bundle through a build argument and ends up inside the JavaScript the browser downloads. **It is public the moment it ships.**

- A frontend never receives a secret of any kind: no API key, no service account, no signing key, no database credential. Not as a build argument, not as a runtime variable, not in a committed config file.
- Anything the browser needs that requires a key is done by the backend. The backend holds the key and exposes an endpoint; the browser calls the endpoint.
- The values a frontend legitimately carries are public by nature: the API base URL, the app name, a feature flag, a login URL.
- A build system passes these as substitutions, and a substitution is visible in the build log and in the trigger configuration. That is a second reason a secret never travels this way.
- **Changing one of these means rebuilding, not redeploying.** Supplying it as a runtime variable does nothing: it reaches the container, but the JavaScript already in the browser still holds the value baked at build time.
- A server-rendered frontend does read runtime variables and follows the backend rules instead.

## Local Development

- Local values live in a gitignored `.env`, never in source, per [[commit.rules.md]].
- `.env.example` lists every variable name with an obvious placeholder and no real value, per [[env.rules.md]].
- **Never copy a production secret into a local `.env`.** Issue a separate development key, so a laptop never holds a production credential.
- A local key file lives outside the working tree, or inside an ignored directory that is never staged.
- Running the project locally does not require access to the production secret manager. Local development uses development values.

## Machine Learning Specifics

- **A dataset can be a secret.** Data under an agreement, scraped data, or anything holding personal information is not committed and not uploaded to a public model hub.
- **A model can leak its training data.** Do not publish weights trained on private data without knowing what memorization risk that carries.
- **A notebook output is a publication.** A printed key, a sample row of personal data, or a connection string in an output cell ships with the file. Clear outputs before committing.
- **An experiment tracker carries whatever you log.** Never log a raw config that contains a key.
- **A public hosted notebook is public.** Nothing real goes in one, ever.

## Naming

- Use `SCREAMING_SNAKE_CASE` for every environment variable.
- **Name the value, not its tier.** `ANTHROPIC_API_KEY`, not `SECRET_1` or `KEY_A`.
- Keep the same name across every project for the same concept, so `DATABASE_URL` means the same thing everywhere.
- Name a secret manager resource for the project and the value, such as `myapp-anthropic-api-key`. A secret named `key` or `prod-secret` is unmaintainable once a project holds twenty of them.
- **Never encode an environment into the variable name.** The same name carries a different value per deployment; that is what the deployment is for.
- That rule governs the variable, not the secret resource. Two environments in one project need two secret resources, so those carry an environment suffix, such as `myapp-anthropic-api-key-staging`. The variable each is mounted as does not change, and that is the point: the deploy command decides which secret fills `ANTHROPIC_API_KEY`, and the application never learns which environment it is running in.
- **A non-production environment never mounts a production secret.** A signing key in particular: sharing one means a token minted in the lower environment is accepted by the higher one, and any credential copied down with a database clone becomes usable against production.

## Definition of Done

- Every key, token, private key file, and signing secret is in a secret manager and reaches the app as a mounted secret.
- Every other value is configuration supplied on the deploy command.
- The runtime identity holds read access on every secret it reads, and nothing wider.
- No secret and no environment variable is declared in the `Dockerfile`, committed in a `.env`, or baked into the image.
- The frontend carries no secret of any kind, and every build-time value it does carry is public by nature.
- `.env.example` lists every variable name with a placeholder, and no real value.
- The project fails to start when a required value is missing or still at its default.
- Where a database password sits in an environment variable, the README records that choice.
- No secret is printed, logged, or written into a notebook output.
- Any secret that was ever exposed has been rotated.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements, including [[security.rules.md]] and [[env.rules.md]]
2. Direct user instructions
3. This secret and configuration standard
4. [[deploy.rules.md]] and [[deploy.cloud.md]]
5. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Applies To

- [[env.rules.md]]
- [[security.rules.md]]
- [[commit.rules.md]]
- [[codes.rules.md]]
- [[auth.rules.md]]
- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[stacks.rules.md]]
