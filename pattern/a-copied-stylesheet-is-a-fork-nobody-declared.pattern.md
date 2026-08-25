---
tags:
  - kind/pattern
  - layer/frontend
  - topic/ux
---

# A copied stylesheet is a fork nobody declared

> [!warning]
> A design system adopted by copying a stylesheet line for line is correct on the day of the copy and diverging from the next commit onward, silently, because nothing compares the two files again.

Copying is the right way to adopt a design system: [[uix.component.md]] says a project adopts a standard by copying the reference implementation, not by re-deriving it from prose. **The failure is not the copy. It is that the copy is never declared, so nobody knows a second version exists.**

Two states follow from a verbatim copy, and only one of them is stable:

- **Never edited in place.** The copy stays identical, a new shared value added upstream is copied down, and the two files remain one thing in two places. This works, and it needs the copy to be recorded somewhere a person will read.
- **Edited locally, once.** From that moment the file is a fork. The upstream fix does not arrive, the local fix does not travel back, and both sides believe they share a design system.

The recovery is not to re-copy over the local edits. **Read what diverged, decide per difference whether it belongs upstream or is a genuine project-specific deviation, push the first kind up and record the second kind** in that project's README, per the deviations rule every component standard carries.

A project that abandons the shared system entirely is a third state, and it is fine as long as it is written down. What is not fine is a project that looks like it follows the system because its class names still match.

**Why:** class names surviving a rewrite is the trap. A reader greps for a shared class, finds it, and concludes the project is on the design system, when the file behind it shares nothing but the names.

**Applies to:** any project that adopted a design system, a configuration, or a pipeline by copying a file rather than depending on one.

**Source:** an incident outside this repository, where an app's stylesheet was a verbatim copy until the day it was replaced wholesale and nothing recorded either fact.

## Related

- [[uix.component.md]]
- [[docs.rules.md]]
- [[repository.rules.md]]
- [[a-ui-rule-reasoned-about-one-component-breaks-where-a-page-stacks-two.pattern.md]]
