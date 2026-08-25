---
tags:
  - kind/rule
  - topic/workflow
  - topic/security
---

> Up: [[README.md]]

# Commit Standard

> [!important]
> Every commit follows Conventional Commits, written in English, with each change explained as a list item.

## Core Requirement

Every commit follows the **Conventional Commits 1.0.0** specification, and explains each change as a list item in the commit body.

A commit message is read by you six months from now, with no memory of the change and no context beyond the diff. It is also read by release tooling, by a changelog generator, and by anyone tracing why a line of code exists. It is documentation, so it follows the same discipline as the rest of [[docs.rules.md]].

This applies to every commit, including a one-line fix and a configuration change.

## Language

All commit messages are written in **English**.

Where a project's own documentation is written in another language, per [[prd.rules.md]], the commit history is still English. History is consumed by tooling and by hosting platforms that expect it, and it sits directly next to code identifiers, which are already English per [[codes.rules.md]].

None of these is ever written in another language:

- The type
- The scope
- The description
- The body list
- The footers

Technical terms, library names, framework names, command names, file names, variable names, database field names, and route paths keep their original form.

Incorrect:

```text
feat(dashboard): tambah grafik baru

- Menambahkan grafik penjualan bulanan
```

Correct:

```text
feat(dashboard): add the monthly sales chart

- Add a monthly sales chart sourced from the reporting endpoint
```

## Structure

```text
<type>[optional scope]: <description>

<body as a list>

[optional footer(s)]
```

1. The type is required and lowercase.
2. The scope is optional, in parentheses immediately after the type.
3. A `!` immediately before the colon marks a breaking change.
4. A colon and a single space follow the type, the scope, or the `!`.
5. The description is required, on the first line.
6. Exactly one blank line separates the description from the body.
7. Exactly one blank line separates the body from the footers.

## Types

Use only these. The SemVer column is what a release tool reads.

| Type | Use for | SemVer impact |
| :- | :- | :- |
| `feat` | A new feature or capability | MINOR |
| `fix` | A bug fix | PATCH |
| `docs` | Documentation only | None |
| `style` | Formatting, whitespace, or lint, with no logic change | None |
| `refactor` | A change that neither fixes a bug nor adds a feature | None |
| `perf` | A performance improvement | PATCH |
| `test` | Adding or correcting tests | None |
| `build` | Build system, dependencies, packaging, environment file | None |
| `ci` | Pipeline and build-config changes | None |
| `chore` | Maintenance that fits nothing else | None |
| `revert` | Reverting a previous commit | Depends on what is reverted |
| `exp` | A machine-learning experiment: a run, a parameter sweep, a model change | None |

`exp` is the one addition to the standard set, because an ML project produces commits that are neither a feature nor a fix. Record what changed and what it scored.

Type rules:

- Do not invent a type. If none fits, use `chore` and explain the work in the body.
- Do not misspell a type. `feet` or `fixes` makes tooling skip the commit silently.
- A commit with a `BREAKING CHANGE` footer or a `!` marker is MAJOR regardless of its type.

## Scope

A scope is optional but recommended. Use it whenever the change is limited to an identifiable part of the codebase.

- Use a lowercase noun naming a section of the codebase, such as `auth`, `dashboard`, `api`, `upload`, `deploy`, `db`, `loader`, or `train`.
- Use a single scope. Do not list two.
- Keep the scope name consistent. Reuse the scope already used for that area.
- Omit the scope when the change is repository-wide, such as a dependency bump across the whole project.
- Never use a file path or a file name as a scope.

Correct:

```text
fix(auth): reject an expired refresh token
```

Incorrect, a path as a scope:

```text
fix(src/services/auth/token.py): reject an expired refresh token
```

Incorrect, two scopes:

```text
fix(auth,api): reject an expired refresh token
```

## Description

1. Imperative mood, as an instruction: "add", "fix", "remove", "update". Not "added" or "adds".
2. Start lowercase, unless the first word is a proper noun or an identifier that is normally capitalized.
3. No trailing period.
4. The whole first line is 72 characters or fewer.
5. State what the commit does, not what you did.
6. No issue number in the description. That is what a footer is for.

Correct:

```text
feat(loader): add a streaming reader for the parquet dataset
fix(train): stop the scaler fitting on the test split
exp(model): raise the embedding dim to 512, macro F1 0.81 from 0.78
```

Incorrect, past tense, capitalized, trailing period:

```text
feat(dashboard): Added new graphics.
```

Incorrect, over 72 characters and explaining in the subject:

```text
feat(dashboard): added new graphics for the dashboard page because the old ones were unreadable
```

## Body

The body is required. Every change in the commit gets its own list item.

1. A flat bullet list.
2. Use `-` as the marker. Never `*`, `+`, or a numbered list.
3. One item per change. A commit touching three concerns has at least three items.
4. Start each item with a capital letter and an imperative verb: "Add", "Fix", "Remove", "Replace", "Move", "Rename", "Update".
5. No trailing period on an item.
6. Explain the change and its purpose or effect in the same item, so a reader does not need the diff to understand it.
7. Wrap a long item at 100 characters, continuation indented two spaces.
8. No nested list. One level deep.
9. A single-change commit still uses a single-item list.
10. Never list a file name alone. Describe the change, and name the file only when it adds clarity.

Correct:

```text
feat(dashboard): add the reporting charts

- Add a monthly revenue line chart so the numbers can be compared without exporting data
- Add a headcount bar chart to replace the manual spreadsheet report
- Add a shared chart color palette so every chart on the page uses the same series colors
```

Correct, a single change with a wrapped item:

```text
fix(api): return 422 for an invalid page parameter

- Validate the page query parameter before the query runs, so an invalid value returns 422
  instead of a 500
```

Incorrect, no body:

```text
fix(api): return 422 for an invalid page parameter
```

Incorrect, a paragraph instead of a list:

```text
fix(api): return 422 for an invalid page parameter

The page parameter was not validated, so an invalid value reached the query layer
and produced a 500. It is now validated first.
```

Incorrect, file names with no explanation:

```text
refactor(auth): clean up the auth service

- token.py
- session.py
```

For an `exp` commit, name the metric and the baseline. A commit that says "improve model" and nothing else is a commit that has to be rerun to be understood.

## Footers

Optional, after exactly one blank line following the body.

- A word token, then `: ` or ` #`, then the value.
- Use `-` in place of a space inside a token, such as `Reviewed-by`. `BREAKING CHANGE` is the only token allowed to contain a space.
- One footer per line.

| Token | Use for | Example |
| :- | :- | :- |
| `BREAKING CHANGE` | What breaks and what to do instead | `BREAKING CHANGE: the auth header is now required` |
| `Refs` | An issue, a ticket, or a commit SHA | `Refs: #123` |
| `Closes` | An issue this closes | `Closes: #123` |
| `Reviewed-by` | The reviewer | `Reviewed-by: A Person` |
| `Co-authored-by` | An additional human author | `Co-authored-by: A Person <person@example.com>` |

Do not use a footer that is not on this table.

## No Tool or AI Attribution

A commit records what changed in the codebase, not which tool was used to write it. You are accountable for the change either way.

Never add:

- A `Co-authored-by` footer naming an AI assistant, a model, or a bot
- A "generated with", "created with", or "written with" footer or line of any kind
- A tool name, an assistant name, a model name, or a product link used as attribution
- A tool signature or watermark anywhere in the message

`Co-authored-by` is reserved for a human who worked on the change.

Incorrect:

```text
docs(rules): add the commit standard

- Add commit.rules.md as the commit standard for every project

Co-Authored-By: An AI Assistant <noreply@example.com>
```

Incorrect:

```text
docs(rules): add the commit standard

- Add commit.rules.md as the commit standard for every project

Generated with an AI coding tool
```

Correct:

```text
docs(rules): add the commit standard

- Add commit.rules.md as the commit standard for every project
```

## Breaking Changes

A breaking change is any change that forces a consumer to change something: a removed endpoint, a renamed response field, a newly required environment variable, a changed database contract.

1. Mark it with a `!` before the colon, with a `BREAKING CHANGE` footer, or with both.
2. Write `BREAKING CHANGE` in uppercase. `BREAKING-CHANGE` is an accepted synonym.
3. With only the `!` marker, the description must describe the break itself.
4. With the footer, state what breaks and what a consumer must do instead.
5. The body list is still required.

Correct, marker and footer:

```text
feat(api)!: require an Authorization header on every report endpoint

- Add header validation to every report endpoint, so an unauthenticated request is rejected
- Remove the anonymous read path the internal dashboard used

BREAKING CHANGE: every report endpoint now requires an Authorization header. A client without
a token receives a 401.
```

Correct, marker only:

```text
build!: drop support for Node 18

- Raise the minimum Node version to 20, so the build can use the current runtime features
```

## One Concern Per Commit

- A change that fits two types is two commits. Do not pick one and hide the rest in the body.
- Do not mix a refactor with a fix, or a formatting pass with a feature.
- A change across many files serving one concern is still one commit.
- Use a branch for a large change, per [[branch.rules.md]].

## Revert Commits

Use the `revert` type and reference the reverted SHA in a footer.

```text
revert: remove the monthly revenue chart from the dashboard

- Revert the monthly revenue chart, because the reporting endpoint returns incorrect totals

Refs: 676104e
```

## Formatting Restrictions

Every formatting restriction in [[docs.rules.md]] applies to a commit message in full.

Do not use, anywhere in a message:

- An emoji, including a Gitmoji prefix
- An em dash, a left arrow, or a right arrow; use `-`, `<`, and `>`
- Smart quotation marks
- A decorative Unicode symbol
- A divider, border, or banner built from a repeated character
- Markdown headings, bold, italics, or a code fence
- Extra blank lines used only for visual separation
- A trailing period on the description or on a list item
- ALL CAPS, except the `BREAKING CHANGE` token

Incorrect, an em dash and an arrow:

```text
feat(dashboard): add the reporting charts

- Add a revenue chart [em dash] sourced from the reporting endpoint
- Data flow: API [right arrow] chart component
```

Correct:

```text
feat(dashboard): add the reporting charts

- Add a revenue chart sourced from the reporting endpoint
- Route the data flow as API > chart component
```

## Security and Privacy in the Message

- Never put a credential, a token, a password, a connection string, or a real environment value in a commit message.
- Never put personal data, such as a national identity number, a phone number, or a user's email address, in a message. A `Co-authored-by` footer for a collaborator is permitted.
- Reference a secret by its variable name only, such as `DATABASE_URL`, per [[env.rules.md]].
- A message cannot be rewritten safely after it is pushed and shared, so treat every message as permanent.

## Never Commit a Key or a Credential

The rules above govern the message. These govern what the commit contains. A secret in a message and a secret in a file are the same leak, and the file is the more common one.

Never commit any of the following:

| Kind | Examples |
| :- | :- |
| A private key or certificate | `.pem`, `.key`, `.p12`, `.pfx`, `.jks`, `.keystore`, `.asc`, `.gpg`, `id_rsa`, `id_ed25519`, and any file containing a `BEGIN PRIVATE KEY` block |
| A credential in JSON | A cloud service account key, an admin key, `client_secret*.json`, `application_default_credentials.json`, a stored OAuth token |
| A key directory | `keys/`, `key/`, `secrets/`, `certs/`, `credentials/`, `.ssh/` |
| An environment file | `.env` and every variant listed in [[env.rules.md]]. `.env.example`, holding placeholders only, is the one file that is committed |
| A tool or cloud config carrying a token | `kubeconfig`, `.aws/credentials`, `.npmrc`, `.pypirc`, `.docker/config.json`, or a CI config with an inline token |
| Real data | A database file, a dump, a session store, or an export containing personal data, per [[repository.rules.md]] |
| Machine learning output | A dataset, a model weight, a checkpoint, `.ipynb_checkpoints/`, or a notebook with its outputs still in it |

Rules:

1. Add these patterns to `.gitignore` before the first commit, not after the file appears. [[repository.rules.md]] sets the minimum list; these extend it.
2. Ignore a `keys/` or `key/` directory as a whole, never file by file. A per-file rule misses the next file someone drops into it.
3. Never run `git add -f` on a path `.gitignore` already covers. The ignore rule was the control; forcing past it removes the control.
4. A credential the app needs at runtime comes from an environment variable or a secret manager, per [[env.rules.md]] and [[secret.rules.md]]. It never ships inside the repository.
5. A private repository is not a safe place for a key. Its access list is wider than it looks, its history is permanent, and it can be made public with one click.
6. Keep local key material outside the working tree, or inside an ignored directory that is never staged.
7. A key that is genuinely public may be committed. The public half of a signing key set is published at its discovery endpoint instead, per [[auth.rules.md]]. The private half is never committed under any circumstance.
8. Clear notebook outputs before committing, or the diff is unreadable and the repository grows without limit.

> [!warning]
> Read `git status` before staging. `git add -A`, `git add .`, and `git commit -a` are how an untracked key or a two-gigabyte checkpoint reaches a commit, so never run one without looking at what it is about to include.

## A Committed Key Is a Leaked Key

> [!danger]
> A committed credential is compromised the moment it lands, and rewriting history does not undo it. Rotate the key instead of deleting the commit.

- Once a commit containing a key is pushed, treat that key as compromised and rotate it, per [[security.rules.md]].
- Deleting the file in a later commit does not remove it. It stays in the history and can be read by anyone who can read the repository.
- Rewriting history does not guarantee removal either. A fork, an existing clone, a CI log, a cached build, and the hosting platform's own unreferenced objects can all still hold the file.
- Rotate first, then clean the history, then record what happened. Cleaning without rotating leaves a valid key in circulation and only hides it.
- Caught before pushing, reset or amend the commit rather than adding a second one that deletes the file, and still rotate if the key ever left the machine it was generated on.

## Definition of Done

- The message is written in English.
- The type is on the allowed list and is lowercase.
- The scope, when present, is a single lowercase noun matching the scope already used for that area.
- The description is imperative, has no trailing period, and the first line is 72 characters or fewer.
- The body is present and is a flat `-` list.
- Every change in the commit has its own item, and each item explains the purpose or the effect.
- A breaking change is marked with `!`, a `BREAKING CHANGE` footer, or both.
- Every footer uses a permitted token and sits after a single blank line.
- No tool, AI, model, or bot attribution appears anywhere in the message.
- The commit covers one logical concern.
- No emoji, prohibited character, Markdown formatting, or decorative divider is present.
- No secret, credential, or personal data is present in the message.
- No private key, credential file, environment file, key directory, dataset, checkpoint, or notebook output is included in the commit.
- `git status` was reviewed before staging, and nothing was force-added past `.gitignore`.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This commit standard
4. Conventional Commits 1.0.0
5. Existing project conventions

A direct user instruction must not override security or privacy requirements. The English requirement here overrides a project's own documentation language for commit messages only. Every other document follows [[docs.rules.md]] and [[prd.rules.md]].

## Applies To

- [[branch.rules.md]]
- [[pr.rules.md]]
- [[docs.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]
- [[repository.rules.md]]
- [[auth.rules.md]]
