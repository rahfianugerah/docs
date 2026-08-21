> Up: [[README.md]]

# Secret and Configuration Standard

> [!warning]
> API keys, signing keys, and `.pem` files live in a secret manager. A frontend bundle holds no secrets at all, because everything in it is public.

## Core Requirement

Every value a project needs at runtime is either a **secret** or **configuration**. This policy decides which, and where each one lives.

Nothing real is ever hardcoded, committed, or baked into an image.

> [!danger]
> A secret that was committed, pasted, or shown on a screen share is compromised. Rotating it takes minutes; finding out later does not.

[[env.rules.md]] owns how these files are read. This one owns what goes in them.

## The Test

**Is the value a key?**

If holding it lets someone authenticate as you, sign what you would sign, decrypt what you can decrypt, or spend your money, it is a **secret**. If it only says where to connect or how to behave, it is **configuration**.

Classify by what possession allows, not by how sensitive the value feels.

| Kind | Examples | Where it lives |
| :- | :- | :- |
| **Secret** | API key, access token, private key, signing secret, password, service account JSON | A secret store, or a gitignored `.env` for local work |
| **Configuration** | Host, port, database name, model name, data path, batch size, log level, feature flag | `.env`, a config file, or a command-line argument |

## Secrets

These are always secrets, with no exception:

- An API key or token for a third party: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `HF_TOKEN`, a Kaggle key, a weights-and-biases key.
- A private key or certificate file: `.pem`, `.key`, `.p12`, `.pfx`.
- A cloud service account JSON key.
- A JWT or session signing secret. Forging it forges sessions, so it is key material even though it is not called a key.
- A standalone password, including a database or SMTP password.
- A webhook signing secret.

Rules:

1. **One secret per value.** Never bundle several into one blob; they then rotate as one thing.
2. **Never in source code.** Not in a constant, not in a notebook cell, not in a docstring, not in a comment, not in a test fixture.
3. **Never in a committed file**, in any format. See [[commit.rules.md]].
4. **Never printed.** Not to a terminal, a log, a notebook output, a traceback, an issue, or a chat message.
5. **Rotate on any doubt.** A secret that was committed, pasted, or shown on a screen share is compromised. Rotating is minutes; finding out later is not.
6. **One secret per project and per environment.** A single key shared across five projects cannot be revoked without breaking four of them.

### Where a Secret Actually Lives

In order of preference:

1. **A secret manager**, where the project has one available: cloud Secret Manager, 1Password, `pass`, the OS keychain. Best for anything shared between machines or that outlives a project.
2. **A gitignored `.env`**, for local development. Fine for a personal project on one machine, and the default here.
3. **An environment variable set by the shell or the platform**, for CI and deployment. Never committed to the workflow file; use the platform's own secret store.

Never a fourth option. Not a config file "outside the repo but next to it", not a note, not a chat message to yourself.

## Configuration

Everything that is not key material. It goes in `.env`, a config file, or a CLI argument, and it may be committed when it holds no real value.

- A host, a port, a database name, a URL.
- A data directory, an output directory, a checkpoint path.
- A model name, a batch size, a learning rate, a seed.
- A log level, a timeout, a feature flag.

Rules:

1. Read configuration once into a typed settings object, per [[codes.rules.md]].
2. Fail fast when a required value is missing or still holds its placeholder.
3. List every name in `.env.example` with a placeholder, per [[env.rules.md]].
4. **Do not promote configuration into a secret store because it looks sensitive.** A data path in a keychain costs a retrieval procedure and buys nothing.

### Where a Value Is Both

A database URL is configuration, but a password inside it is key material.

Preferred order:

1. **No password at all**, where the database supports another method.
2. **Split the value**: host, port, and name in `.env`, the password from the secret store, assembled in the settings object.
3. **The whole string in `.env`**, gitignored. Acceptable on a personal project; know that it is the one place a credential sits in a plain file.

## Machine Learning Specifics

- **A dataset can be a secret.** Data under an NDA, scraped data, or anything with personal information is not committed and not uploaded to a public model hub.
- **A model can leak its training data.** Do not publish weights trained on private data without knowing what memorization risk that carries.
- **A notebook output is a publication.** A printed key, a sample row of personal data, or a connection string in an output cell ships with the file. Clear outputs before committing.
- **A `wandb` or `mlflow` run carries whatever you log.** Never log a raw config that contains a key.
- **A public Hugging Face or Colab notebook is public.** Nothing real goes in one, ever.

## Naming

- `SCREAMING_SNAKE_CASE` for every environment variable.
- Name the value, not its tier: `OPENAI_API_KEY`, not `SECRET_1`.
- Keep the same name across projects for the same concept, so `DATABASE_URL` always means the same thing.
- Never encode the environment into the name. The same name carries a different value per environment.

## Definition of Done

- No key, token, private key file, or password appears in source, a notebook, or a committed file.
- Every secret is in a secret store or a gitignored `.env`.
- `.env.example` lists every variable name with a placeholder and no real value.
- The project fails to start when a required value is missing.
- No secret is printed, logged, or written into a notebook output.
- Any secret that was ever exposed has been rotated.

## Applies To

- [[env.rules.md]]
- [[security.rules.md]]
- [[commit.rules.md]]
- [[codes.rules.md]]
