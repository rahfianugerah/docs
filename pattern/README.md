---
tags:
  - kind/pattern
  - topic/workflow
---

> Up: [[README.md]]

# Patterns

> [!info]
> A lesson that cost something to learn, written so the next project does not pay for it again. A pattern is not a memory note: it carries no claim about any repository in this vault.

## What a Pattern Is

A pattern records **a failure and its mechanism**, generalized away from the system it happened in. It is here because the mechanism repeats and the symptom points somewhere else.

The difference from [[memory/README.md]] matters and is not a technicality:

| | A memory note | A pattern |
| :- | :- | :- |
| Claims | Something is true of a named file, project, or environment | A mechanism repeats wherever the conditions hold |
| `Source` | A real path from this workspace root | The incident it came from, which is outside this repository |
| Goes stale | When the file it names changes | When the technology it describes changes |
| Written by | The session that learned it | A session that generalized someone's incident |

**A memory note requires a `Source` path that resolves from the workspace root**, per [[memory.rules.md]]. A lesson learned in a system this vault does not contain cannot honour that, and inventing a path would be a fabricated provenance. So it lives here instead, and says plainly where it came from.

## Shape

The same shape as a memory note, with `kind/pattern` in the frontmatter and one difference in the labels:

```markdown
---
tags:
  - kind/pattern
  - topic/[concern]
---

# One line stating the mechanism

> [!danger]
> The line a reader must not miss.

The statement, in one or two sentences.

The detail underneath it.

**Why:** why the symptom points at the wrong thing.

**Applies to:** the conditions under which this repeats.

**Source:** the incident, named honestly as being outside this repository.

## Related
```

- **One pattern holds one mechanism.** Two mechanisms is two files.
- **The title states the mechanism, not the topic.** "A host-only cookie never reaches a second host" beats "Cookie notes".
- At most one callout, per [[callout.rules.md]].
- One paragraph is one line, per [[docs.rules.md]].

## Index

All sixteen. **A pattern that is not listed here is unreachable**, so it is added on the same commit that writes it.

### Deploys That Fail in the Wrong Place

- [[a-static-bundle-built-without-its-api-origin-calls-itself.pattern.md]] - the value is baked at build time, so redeploying cannot fix it
- [[the-first-build-on-a-new-service-fails-at-the-deploy-step.pattern.md]] - there is no configuration to preserve yet, and that is by design
- [[a-release-carrying-a-migration-is-built-off-the-release-branch-first.pattern.md]] - the job needs an image the release has not built yet
- [[deploy-steps-come-from-the-project-own-runbook-in-both-shells.pattern.md]] - the canonical runbook holds placeholders, never values
- [[powershell-redirection-corrupts-a-file-read-verbatim.pattern.md]] - a byte order mark fails far from the shell that wrote it

### Databases That Isolate or Restore Less Than They Appear To

- [[revoke-connect-alone-does-not-isolate-two-databases-on-one-instance.pattern.md]] - an inherited superuser role outranks the revoke, silently
- [[a-restore-into-a-stricter-schema-needs-its-nullable-foreign-keys-detached.pattern.md]] - the error names a row while the cause is the schema
- [[a-read-only-migration-still-blocks-ddl-while-it-runs.pattern.md]] - no writes is not the same as no impact
- [[a-pooler-host-changes-the-port-and-the-username.pattern.md]] - three failures, none of which mentions the pooler

### Identity and the Browser

- [[a-host-only-cookie-never-reaches-a-second-host.pattern.md]] - the 401 reads like a permissions bug and is not
- [[an-identity-provider-publishes-its-integration-values-at-a-discovery-endpoint.pattern.md]] - the values are self-serve, so asking for them is a round trip nobody needs

### Interfaces Reasoned About in Isolation

- [[a-ui-rule-reasoned-about-one-component-breaks-where-a-page-stacks-two.pattern.md]] - draw the page that renders two of them before adding the rule
- [[a-copied-stylesheet-is-a-fork-nobody-declared.pattern.md]] - correct on the day of the copy, diverging from the next commit

### Reports and Runs That Name the Wrong Cause

- [[seed-data-cannot-answer-what-production-holds.pattern.md]] - a successful query feels like evidence and is not
- [[a-missing-feature-report-needs-three-checks-before-any-work.pattern.md]] - an untracked file and a scoped element both read as absent
- [[derive-a-repository-name-from-the-remote-not-the-folder.pattern.md]] - twenty successes and one failure is the dangerous shape

## Related

- [[memory/README.md]]
- [[memory.rules.md]]
- [[docs.rules.md]]
- [[callout.rules.md]]
