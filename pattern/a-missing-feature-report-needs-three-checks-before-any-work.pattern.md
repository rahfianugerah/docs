---
tags:
  - kind/pattern
  - topic/workflow
---

# A missing-feature report needs three checks before any work

> [!warning]
> Two of five reported defects in one testing round turned out to be features that already existed. Neither absence was visible in the code, which is why reading the code alone would not have caught either one.

- **"There is no settings screen for this."** The screen was complete and passing its tests, but its file was still untracked, so it was never in any built image. `git status` answered this; a code search would have confirmed the feature existed and explained nothing.
- **"There is nowhere to update this status."** The button had been live for days and renders only for the record's owner. The tester held an administrative account and saw an empty screen with nothing explaining the absence.

**An untracked file and an owner-scoped element both present to a tester as "the feature does not exist"**, and neither shows up as missing when you read the source. Taking either report at its word would have meant rebuilding something that already worked.

Three checks, before any work is planned:

1. **Is the file tracked, and did it actually reach the deployed image?**
2. **Which role did the reporter hold**, against the visibility condition on the element?
3. **Is the cause the report names the one the code actually takes?**

**Why:** a bug report names a symptom, and the reporter's model of the cause is a guess made from outside the system. Treating that guess as the finding is how work gets done twice.

**Applies to:** any acceptance-testing round or bug report where the claim is that something is missing rather than wrong.

**Source:** an incident outside this repository. The finding was that the features existed and the report had not found them, which no single file records.

## Related

- [[pr.rules.md]]
- [[repository.rules.md]]
- [[seed-data-cannot-answer-what-production-holds.pattern.md]]
