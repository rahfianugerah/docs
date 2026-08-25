---
tags:
  - kind/pattern
  - topic/workflow
---

# Derive a repository name from the remote, not from the folder

> [!danger]
> One folder name differing from its remote by a single letter makes a bulk operation succeed twenty times and fail once. That single failure is the dangerous shape.

A loop over a workspace that builds the remote name from the directory name prints twenty successes and one "could not resolve to a repository", which is easy to read past in a long run and **leaves exactly one repository behind without the run looking failed.**

Derive the name from the remote instead:

```bash
r=$(git -C "$d" remote get-url origin | sed "s|.*/||;s|\.git$||")
```

The mismatch is a typo in the local clone rather than on the remote, so it is fixable by renaming the folder. It often is not renamed, because several tools hold the path and a rename is a separate change from whatever work happens to be running. **That is precisely why the loop must not depend on the name being right.**

The general form: **never derive an identifier from a human-typed path when the authoritative value is available from the system that owns it.** A folder name is a convenience; the remote is the fact.

**Why:** a bulk pull request run over fourteen repositories failed on exactly this one, and the error arrived in the middle of thirteen successful lines.

**Applies to:** any script or loop that maps a workspace folder to a remote repository, and any automation whose per-item failure is one line in a long output.

**Source:** an incident outside this repository. Confirm the general case by comparing every folder name in a workspace with its own remote URL.

## Related

- [[repository.rules.md]]
- [[branch.rules.md]]
- [[deploy-steps-come-from-the-project-own-runbook-in-both-shells.pattern.md]]
