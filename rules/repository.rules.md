---
tags:
  - kind/rule
  - topic/workflow
---

> Up: [[README.md]]

# Repository Quality and Operations Standard

> [!note]
> Repository hygiene: git history, `.gitignore`, logging, error handling, and testing.

## Core Requirement

When creating, modifying, or reviewing a repository, follow the rules in this policy.

These are the baseline hygiene practices that let a project be maintained by someone other than its original author. Each one exists because its absence has actually cost something: a repository with no git history, a database file committed into the tree, a secret hardcoded in a compose file.

## One Deployable, One Repository

**There is no monorepo.** A backend and a frontend are two separate repositories, even when they are two halves of one product and are worked on by the same person on the same day.

The naming is fixed: `[APP]-backend` and `[APP]-frontend`.

This is not a preference about layout. Everything downstream assumes it:

- A repository gets one build config at its root, one image, one service, and one trigger on the release branch. A combined repository has two of each and no correct place to put either.
- With one trigger on a combined repository, **every frontend commit rebuilds and redeploys the backend**, and every backend commit rebuilds the frontend. A typo fixed in a label restarts the API.
- The two halves have different runtimes, different dependency manifests, different audits, different `.gitignore` needs, and different reasons to release.
- Branch promotion moves one repository as a unit. A combined repository forces both halves to ship together even when only one changed.

A repository that is not a deployable, such as this documentation vault or a shared schema repository, is a single repository for its own content. That is not a monorepo; it has one purpose and ships no service.

### Splitting a Combined Repository

An existing repository holding both halves is migrated, not left alone. The order matters, because the record of what was there has to be frozen before anything moves.

1. **Freeze the combined state as `legacy`.** Create a `legacy` branch from the current release branch, push it, and protect it against a force push and a deletion. From that moment it is a read-only record of the project before the split, and nothing is ever committed to it again.
2. **Create the two new repositories**, `[APP]-backend` and `[APP]-frontend`, each with the branches and protection settings [[branch.rules.md]] requires.
3. **Move the code with its history** where practical, using `git subtree split` or `git filter-repo`, so `git blame` still answers questions afterwards. Where that is not practical, make a single initial commit whose message names the source repository and the commit it came from, so the trail is not lost entirely.
4. **Give each new repository its own supporting files**: `.gitignore`, `.env.example`, a README from [[project.template.md]], the build config, and its own deployment runbook. Do not copy the combined compose file into either one.
5. **Bootstrap each service** through the deployment runbook, then connect its own trigger. Deploy the backend first, because the frontend usually bakes the backend URL in at build time.
6. **Retire the old repository** once both are live and verified: archive it, and never delete it. It carries the `legacy` branch, which is the only remaining record of the combined history.

Point every reference, in documentation and in a runbook, at the new repositories in the same change. A link left pointing at the retired repository sends the next person to code that is no longer built.

> [!danger]
> A retired repository is archived, never deleted. It carries the `legacy` branch, which is the only remaining record of the combined history, and deleting it destroys the only copy.

## Version Control

- Use git from the first commit. A project without git history is not acceptable.
- Maintain a `.gitignore` excluding at minimum `.env`, database files (`*.db`, `*.sqlite*`), `uploads/`, `sessions/`, `node_modules/`, `__pycache__/`, and build artifacts.
- Never commit a database file or user data.
- Write meaningful commit messages, per [[commit.rules.md]]. Use a branch for a large change, per [[branch.rules.md]].
- Keep the permanent branches the project's shape declares, and promote a change through a pull request at every stage, per [[branch.rules.md]]. Nothing else lives on the remote long-term.

## Configuration and Documentation

- Maintain a `.env.example` listing every variable the project uses, with a placeholder value such as `__fill__` and an explanatory comment, per [[env.rules.md]].
- Maintain a README covering what the project does, how to run it in development, how to run it in a container, the environment variables, the ports, the volumes, and a checklist against these standards.
- Record an important architectural decision briefly, in the README or in the memory, so the reasoning stays traceable.

## Database

- Change the schema only through a migration, committed to the repository and replayable from an empty database, per [[database.rules.md]].
- Seed data through a script, not an untracked manual insert. Never hardcode a seed user or a seed password.
- Use a timezone-aware timestamp type for every time column, never a naive one. A naive timestamp is correct until the first reader in another offset.
- Use one column name for a person reference across the whole project, chosen once. Two names for the same identity is two joins nobody can see are the same.

## Logging and Error Handling

- Log in a structured format to stdout. Default to `INFO`; use `DEBUG` only in development.
- **Never log personal data**, such as a password, a national identifier, or a phone number. Redact it where the entry needs the surrounding context, per [[security.rules.md]].
- Do not swallow an error silently. Fail fast on a configuration problem at startup. Log a `500` with its stack trace on the server, while the client still receives the standard error format from [[api.rules.md]] without a stack trace.
- **Make an external validation fail closed.** A call to a model or a third-party API that fails open silently is a check that is not a check.

## Testing

- Maintain at minimum a smoke test that starts the project, checks its health endpoint, and exercises one critical flow per core feature, runnable locally.
- Cover important logic with a unit test: a money calculation, a redaction, a routing decision.
- Documented manual testing may supplement a smoke test. It does not replace one.

## Language and Naming

- Write code identifiers in English, and keep comments consistent within a file, per [[codes.rules.md]].
- The UI language is the project's choice, stated once in its README rather than decided per screen.
- Keep the repository and project name consistent with the naming already used across the ecosystem it belongs to.

## Definition of Done

- The repository holds one deployable, named `[APP]-backend` or `[APP]-frontend`, and no repository holds both halves.
- Where a combined repository was split, the pre-split state is frozen on a protected `legacy` branch, the old repository is archived rather than deleted, and every reference points at the new repositories.
- Git is initialized with a correct `.gitignore`, and no secret or database file is committed.
- `.env.example` and the README are complete.
- Migrations run cleanly from an empty database.
- Logs go to stdout without personal data, configuration failures fail fast, and no validation fails open silently.
- The smoke test passes.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This repository policy
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[api.rules.md]]
- [[branch.rules.md]]
- [[commit.rules.md]]
- [[database.rules.md]]
- [[env.rules.md]]
- [[security.rules.md]]
- [[stacks.rules.md]]
- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[codes.rules.md]]
- [[path.rules.md]]
