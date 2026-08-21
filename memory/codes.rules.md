> Up: [[README.md]] · [[memory/README.md]]

# Reference Code Standard

> [!note]
> How a code-level note is filed under `memory/codes/`, separate from the four durable note types.

## Core Requirement

`memory/codes/` holds a working piece of code worth reading again, and every file in it is paired with a markdown note of the same name.

**The note is the memory. The code file is the attachment.** `pmb digest` reads markdown only, so the note is what gets chunked, embedded, and found by `recall`; the code file is never sent anywhere. An agent reads the short note, learns what the code does and why it was kept, and opens the file only when it actually needs the body. That is the whole point: one small note in context instead of two hundred lines of source.

This is a deliberate departure from [[memory.rules.md]], which allows only the four type folders and forbids a per-project subfolder. The reason is written in Why This Breaks the Four-Folder Rule below, so it is a decision rather than an oversight.

## Layout

```text
memory/codes/<project-name>/<yyyy-mm-dd>-<what-it-does>.py
memory/codes/<project-name>/<yyyy-mm-dd>-<what-it-does>.md
```

- `<project-name>` is the repository's own name, lowercase kebab-case, exactly as the folder is named on disk.
- The date is the day the code was generated or last proven to work, written absolutely as `yyyy-mm-dd`, so the folder sorts chronologically without a numbering scheme anybody has to maintain.
- The rest of the name is kebab-case and says what the code does, so `2026-08-18-test-user-login.py` reads as a sentence and `test1.py` does not.
- The pair shares one stem. The note for `2026-08-18-test-user-login.py` is `2026-08-18-test-user-login.md` beside it, and nothing else.
- Any language is allowed. The extension is the language's own, and the paired note is always `.md`.

## The Code File Carries a Header

The first thing in the file is a comment block, in that language's comment syntax, holding four lines and nothing else.

```python
# Project: [APP]-backend
# Date: 2026-08-18
# Why kept: the only login path that exercises the allowlist and the local row together
# Note: 2026-08-18-test-user-login.md
```

A snippet without provenance is a file nobody dares delete and nobody dares trust. Six months later the header is the only thing that says which project it came from and why it survived.

## The Note Carries the Memory

The note follows [[memory.rules.md]] in full: frontmatter, absolute dates, one paragraph per line, a `## Related` list, no `##` heading inside the body.

```markdown
---
type: reference
created: 2026-08-18
updated: 2026-08-18
tags: [app-backend, auth, code]
status: current
---

# Logging in as the system account needs both the allowlist and a local row

`codes/[app]-backend/2026-08-18-test-user-login.py` is the smallest script that reproduces the two-step check, and it is kept because the failure looks like a wrong password and is not.

- It asserts the allowlist entry first, then the local row, so a failure names which half is missing.
- It runs against a local instance only, and reads every value from the environment.

**Why:** the same investigation was repeated twice because the symptom pointed at credentials rather than at authorization.
**Applies to:** any app resolving authorization outside its identity provider.

## Related

- [[memory/codes.rules.md]]
```

Rules for the note:

1. **`type: reference`**, because it points at something rather than asserting a durable fact on its own. A finding the code merely illustrates is a `fact` note in `fact/`, linking here.
2. **Name the code file in the first line of the body**, as a path relative to `memory/`, so a reader who found the note by search knows immediately what to open.
3. **Tag `code`**, plus the project and the topic. The tag is how a project is filtered, which is what `memory.rules.md` means by a project being a tag rather than a directory.
4. **The note explains, the code demonstrates.** Never paste the whole file into the note. If the note repeats the code, the pair has become one thing written twice, and the next edit will change only one of them.

## Never Store Here

Everything [[memory.rules.md]] forbids applies unchanged, and code makes two of them easy to break by accident.

- **No secret, key, token, password, or connection string**, per [[secret.rules.md]]. A script that needs one reads it from the environment, and the note names the variable rather than the value.
- **No real value from any configuration file**, per [[env.rules.md]]. A hardcoded host or bucket name is a real value.
- No dataset, no fixture holding personal data, no captured production payload.
- No file large enough that nobody will read it. A reference longer than a screen or two is a repository, not a memory.

## Keeping It True

- **Code here is not maintained by anything.** Nothing imports it and no test runs it, so it rots silently while the project moves. Verify before trusting it, exactly as [[memory.rules.md]] says of any recalled note.
- When it stops working, either fix it and move `updated`, or set `status: superseded` on the note and say what replaced it.
- Delete the pair together. A note pointing at a file that is gone is worse than neither, and an orphan file with no note is unfindable.

## Why This Breaks the Four-Folder Rule

[[memory.rules.md]] allows only `fact/`, `decision/`, `session/`, and `reference/`, and forbids a per-project subfolder under any of them. That rule exists because a note filed under `fact/<project>/` is invisible to anyone who does not already know the project exists, and because the same fact about two projects then gets written twice.

Neither failure applies to a file on disk. A code file is not a claim that can be true of two projects at once; it came from exactly one repository, on exactly one day, and it is opened by path rather than found by browsing. The project subfolder is what makes it possible to delete a project's references in one action when that project is retired.

The searchable half still obeys the rule, because the note is what `recall` sees, and it is filed by tag rather than by folder.

## Definition of Done

- The file sits in `memory/codes/<project-name>/` and its name is `<yyyy-mm-dd>-<what-it-does>` in kebab-case.
- A markdown note of the same stem sits beside it.
- The code file opens with the four-line header naming the project, the date, why it was kept, and its note.
- The note follows [[memory.rules.md]], names the code file in its first body line, and carries the `code` tag with the project.
- Neither file holds a secret, a credential, or a real configuration value.
- Nothing in the note repeats the body of the code.

## Related

- [[memory.rules.md]]
- [[note.template.md]]
- [[codes.rules.md]]
- [[secret.rules.md]]
- [[env.rules.md]]
