---
tags:
  - kind/pattern
  - layer/infra
  - topic/deploy
---

# Deploy steps come from the project's own runbook, in both shells

> [!warning]
> When someone asks how to deploy, do not answer from memory and do not answer from the canonical runbook. Both are placeholders where a command needs a value.

Open the runbook sitting in that project's own root and give the steps it actually carries, because **only that copy holds the real service name, region, image path, environment variables, secrets, and database instance** for the thing being deployed. The canonical file in this vault is the template those copies were made from.

**Give both shells every time, without asking which is in use.** Being asked to pick is a round trip the answer could have skipped, on a machine that uses both.

- Label the two blocks plainly and keep them adjacent so neither is missed.
- The cloud CLI's syntax is identical in both. Only variable assignment, interpolation, file writing, and command substitution differ, so most of a sequence is one block that runs unchanged in either.
- The runbook's shell-conventions section already carries the operation-by-operation table and the traps. Reuse it rather than re-deriving the differences.
- **Never hand over a block that writes a file with a plain redirect on PowerShell**, per [[powershell-redirection-corrupts-a-file-read-verbatim.pattern.md]].
- **Never interpolate around a colon in PowerShell.** It is a parse error, because the shell reads the prefix as a scoped variable. Compose the full reference once and reuse it.

Where a project's own runbook is written in a different language from this vault, read it for the values and the order. The section numbering is the same either way, which is the whole reason it is fixed.

**Where the project has no runbook of its own, that is the finding to report.** Do not substitute the canonical file and fill in guesses: the missing copy is a real gap.

**Why:** deploy commands carry real service names and real secret references, so a command assembled from memory or from a template's placeholders either fails on a name that does not exist or, worse, succeeds against the wrong service.

**Applies to:** any request to deploy, redeploy, roll back, run a migration job, or change configuration.

**Source:** an incident outside this repository. The canonical template is [[deploy.cloud.md]]; a project's copy is the one with values in it.

## Related

- [[deploy.cloud.md]]
- [[deploy.rules.md]]
- [[docs.rules.md]]
- [[powershell-redirection-corrupts-a-file-read-verbatim.pattern.md]]
- [[a-release-carrying-a-migration-is-built-off-the-release-branch-first.pattern.md]]
