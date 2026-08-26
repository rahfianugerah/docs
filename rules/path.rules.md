---
tags:
  - kind/rule
  - topic/workflow
---

> Up: [[README.md]]

# Path Standard

> [!important]
> Every path is relative to a declared anchor. An absolute path in source is a path that works on exactly one machine, and a path that mixes two namespaces is a path that works on none.

## Core Requirement

**A path is written relative to an anchor, and the anchor is named.**

An absolute path hardcodes a machine into the code: a drive letter, a home directory, a username, a mount point that exists on the laptop it was written on and nowhere else. It runs for one person, and for the next reader it fails with an error that names a missing file rather than a wrong assumption.

**A relative path is not a style preference. It is what makes the same source run on a laptop, in a container, in CI, and on a server.** Those four have four different filesystem layouts and nothing else in common.

This standard owns the **shape** of a path. Three neighbours own the rest and are not repeated here:

| Standard | Owns |
| :- | :- |
| [[docs.rules.md]] | The absolute path to an *executable* in a command, and why writing one hides a broken `PATH` |
| [[security.rules.md]] | A path built from user input: traversal, null bytes, and resolving inside the intended directory |
| [[env.rules.md]] | Where a configured path comes from, and why a real environment file is never read |

## The Three Namespaces

**A project carries three kinds of path, and they never mix.** Each has its own anchor, its own separator, and its own way of being joined. Mixing them is the single most common path bug, and it is invisible until runtime because both halves are strings.

| Namespace | Anchor | Separator | Joined with |
| :- | :- | :- | :- |
| **Filesystem** | The repository root, the package root, or a configured data directory | The platform's, handled by the path library | A path library, never string concatenation |
| **URL** | The origin, which comes from configuration | Always `/`, on every platform | The HTTP client's base, appended once |
| **Import** | The package root | The language's own, `.` or `/` | The module system |

> [!danger]
> **Never build a filesystem path out of a URL path, or a URL out of a filesystem path.** A route segment is not a directory name, a URL is always `/` while a filesystem path is not, and a leading `/` means "the domain root" in one namespace and "the disk root" in the other. Code that treats them as interchangeable serves a file from outside the intended directory, which is the traversal [[security.rules.md]] forbids.

The failure has a recognizable shape on Windows, where the two separators differ: a URL built from a filesystem join comes out as `https://example.com\api\v1\users` and the request fails with a message about the host, not about the path.

## Filesystem Paths

**Anchor to the file or the package, never to the current working directory.**

The working directory is whatever the process happened to be started from. A script that works when run from the repository root breaks when run from anywhere else, and the failure is a missing file rather than a wrong assumption.

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]     # anchor, declared once
DATA = ROOT / "data"                           # relative from it
CONFIG = ROOT / "config" / "settings.toml"
```

```python
DATA = Path("C:/Users/name/project/data")      # one machine
DATA = Path("./data")                          # depends on the working directory
DATA = Path(ROOT + "/data")                    # string concatenation
```

Rules:

1. **Declare the anchor once, in one module**, and import it. An anchor computed in four files is four things that drift when the layout changes.
2. **Never a home directory, a drive letter, or a username** anywhere in source, a config file, a test, a notebook, or a document. `C:\Users\...` and `/home/...` and `/Users/...` are all the same defect.
3. **Never build a path by concatenating strings.** Use the path library, which handles the separator, the redundant separator, and the platform. `Path(a) / b` in Python; the equivalent join in any other language.
4. **Write `/` in a literal even on Windows.** The path library normalizes it. A backslash literal is an escape character in most languages and a syntax hazard for no benefit.
5. **Resolve before use, and confirm the result is still inside the anchor.** That check is what turns a relative path into a safe one, per [[security.rules.md]].
6. **No trailing separator.** `data` not `data/`. The join adds it, and a trailing one produces a doubled separator that some tools accept and others do not.
7. **A path that leaves the repository is configuration**, per the section below. It is never a literal in source.

### Where an Absolute Path Is Unavoidable

Three cases, and only three. In each one the absolute path is a *value*, supplied from outside, never written in source:

- **A mount point inside a container.** `/data`, `/app`. It is absolute because the container's filesystem is the contract, and it is declared in the container definition rather than in code.
- **A variable that names an interpreter or a key file**, such as an interpreter path or a credential file flag. Those take paths because that is what they are for. Write a placeholder in the example file, never a real one.
- **A path the operating system defines**, such as a system certificate store.

Everything else is relative. **An absolute path in source is a defect even when it happens to work**, because it works by coincidence of layout.

## URL Paths

**The origin comes from configuration, and the path is appended by the client.** The two are joined in exactly one place, in code, under review.

```text
API_BASE_URL = https://api.example.com          origin only
```

```text
API_BASE_URL = https://api.example.com/api      carries a path
API_BASE_URL = https://api.example.com/api/v1   carries a route
API_BASE_URL = https://api.example.com/         trailing slash
```

- **Set the client's base once, at construction.** Never concatenate a base into a call site; that is how one call gets the prefix twice and another gets it never.
- **A trailing slash matters.** An origin ending in `/` joined to a path beginning with `/` yields a doubled separator in most clients.
- **Every route is appended relative to the base**, which is `api/<version>/<route>` per [[api.rules.md]].
- **A redirect target is a same-origin relative path**, validated against an allowlist before use, per [[refresh.component.md]] and [[security.rules.md]].
- A static frontend bakes this at build time, so **changing it means rebuilding, not redeploying**, per [[deploy.rules.md]].

## Import Paths

**Pick one convention per project and hold it.** The mixture is what makes a file impossible to move.

- **Absolute from the package root** is the default: it survives a file being moved, and it reads the same from every depth.
- **A relative import is acceptable within one package**, for a sibling module, where the two files genuinely move together.
- **Never a deep relative chain.** More than one `..` means the module is in the wrong place, and the chain breaks the moment either end moves.
- **Never add the project root to the module search path at runtime** to make an import work. That is a layout problem being papered over, and it works in one entry point and fails in every other.

## In Documentation and a Memory Note

- **A path in a document is relative from the workspace root**, and it is a real path that exists today.
- **A path inside the repository stays relative**, per [[docs.rules.md]]. `./scripts/migrate.py`, not the absolute form of the same file.
- **The `Source` line of a memory note names a real path from the workspace root**, per [[memory.rules.md]]. `plugmybrain/src/pmb/ingest.py`, never a bare `src/pmb/ingest.py` on that line and never an absolute one.
- **A wikilink is not a path.** It resolves by filename across the vault, so it carries no directory, per [[docs.rules.md]].
- **An example path in a template or a runbook is a placeholder in the same shape as the real thing.** `C:\path\to\python.exe` says what goes there without leaking whose machine it came from.

## Configuration

A path that varies per environment is configuration, per [[secret.rules.md]], and it follows the same rules as any other configured value:

- The name is in `.env.example` with a placeholder, never a real value, per [[env.rules.md]].
- It is read once into a typed settings object, never with a bare lookup scattered through the code.
- **The application fails fast when it is missing or still holds its placeholder**, rather than falling back to a default that silently writes somewhere else.
- A default is acceptable only where it is relative to the anchor: `DATA_DIR` defaulting to `ROOT / "data"` is fine, defaulting to `/var/data` is not.

## Definition of Done

- No absolute path appears in source, a test, a notebook, a config file, or a document, outside the three cases named above.
- No home directory, drive letter, or username appears anywhere in the repository.
- The anchor is declared once and imported, and nothing resolves against the current working directory.
- Every filesystem path is joined with the path library, and every literal uses `/`.
- Every path derived from input is resolved and confirmed to be inside its anchor.
- The API base is an origin with no path and no trailing slash, and it is joined to a route in exactly one place.
- Import style is one convention, with no relative chain deeper than one level.
- Every configured path is in `.env.example` with a placeholder, and the app fails fast without it.
- No filesystem path is used to build a URL, and no URL path is used to build a filesystem path.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Anchor to the file or the package | Anchor to the current working directory |
| Declare the anchor once and import it | Recompute it in four modules |
| Join with the path library | Concatenate strings, or hardcode a separator |
| Write `/` in a literal | Write a backslash and escape it |
| Keep the API base an origin | Bake a route into the base |
| Append the route through the client's base | Concatenate a base at the call site |
| Put a varying path in configuration | Put a machine's path in source |
| Use a placeholder in an example | Paste the real path from your machine |
| Resolve and check the result stays inside the anchor | Trust that a relative path stayed relative |
| Keep the three namespaces apart | Build a URL out of a filesystem join |

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements, including the traversal rules in [[security.rules.md]]
2. Direct user instructions
3. This path standard
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Applies To

- [[codes.rules.md]]
- [[docs.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]
- [[api.rules.md]]
- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[media.rules.md]]
- [[memory.rules.md]]
- [[repository.rules.md]]
- [[refresh.component.md]]
