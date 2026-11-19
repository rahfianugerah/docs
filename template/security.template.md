---
tags:
  - kind/template
  - layer/docs
---

> Up: [[README.md]]

# Security Policy Template

> [!example]
> Copy the block below into `SECURITY.md` at the repository root. Replace every `[bracketed]` passage, and keep the private reporting channel: a vulnerability reported in public is a vulnerability handed to everyone before it is fixed.

Every repository carries this file, per [[repository.rules.md]]. It follows the formatting rules in [[docs.rules.md]] but not the README shape: no badge row and no table of contents. The controls the project actually implements are [[security.rules.md]]; this file only tells an outsider how to report a flaw.

## Workflow

```mermaid
flowchart TD
  F["A vulnerability is found"] --> P{"Where is it reported?"}
  P -->|A public issue or pull request| X["Wrong channel: the flaw is public before any fix"]
  P -->|The private channel| A["Acknowledged within 3 business days"]
  A --> S["Assessed with a severity within 7 days"]
  S --> FX["Fixed by severity"]
  FX --> D["Disclosed after the fix, credited on request"]
```

## The Block

````markdown
# Security Policy

## Supported Versions

| Version | Security fixes |
| :- | :- |
| [Latest release, or `main`] | <code style="color: green">Supported</code> |
| [Older releases] | <code style="color: red">Not Supported</code> |

## Reporting a Vulnerability

**Never report a vulnerability in a public issue, a pull request, or a discussion.** Report it privately through [GitHub private vulnerability reporting on this repository, or [security contact email]], with:

- What the vulnerability is, and where it is.
- The steps to reproduce it.
- The version or commit it affects.
- The impact you expect.

Do not access, change, or delete data that is not yours while testing, and stop as soon as you have shown the issue.

## What Happens Next

| Step | Within |
| :- | :- |
| Acknowledgement of your report | 3 business days |
| An assessment, with a severity | 7 days |
| A fix or a mitigation for a critical or high finding | 30 days |
| A fix for a medium or low finding | The next release |

You are kept informed at every step, and credited in the release notes if you wish.

## Disclosure

Details are published only after a fix is released, or after 90 days, whichever comes first, on a date agreed with you.

## Out of Scope

- A finding that needs physical access to a device, or a device already compromised.
- Social engineering of anyone involved in the project.
- Denial of service by volume.
- A scanner's output with no demonstrated impact.
````

## Related

- [[repository.rules.md]]
- [[security.rules.md]]
- [[docs.rules.md]]
