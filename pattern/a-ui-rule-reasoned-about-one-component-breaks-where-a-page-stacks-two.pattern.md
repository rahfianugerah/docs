---
tags:
  - kind/pattern
  - layer/frontend
  - topic/ux
---

# A UI rule reasoned about one component breaks where a page stacks two

> [!warning]
> Before adding a rule to a component standard, draw the page that renders **two** of that component, one under the other. Every rule withdrawn so far survived the single-instance drawing and failed the stacked one.

Two rules were added to a pagination standard and withdrawn the same day, both after reaching production, and both caught by the owner rather than by review.

| Rule | Reasoning that justified it | What the stacked page did |
| :- | :- | :- |
| Repeat the pager **above** content taller than one screen | A reader who scans and gives up is at the top, so make them not scroll back down | A dashboard stacks a facet grid, a table, then another table. The upper pager of one list landed directly beneath the lower pager of the list before it, and two pager rows in a row read as a rendering fault |
| Drop the controls when there is only one page | "Page 1 of 1" is a control that can do nothing | Choosing 100 rows on a 22-row table **produces** that single page, so the trim removed the page size control that was the only way back to 20 |

The second is the sharper form and generalizes past pagination: **a control must never remove the way to undo the state it produced.** Check it against any control that hides itself based on its own effect.

**Why:** a component standard is written per component, so the mental model while writing is one component alone on a page. Real apps never render one; a dashboard carries three paged lists, several charts, and a toolbar of the same select. **The interaction between two instances is where the rule is actually tested, and it is invisible from inside the component's own file.**

**Applies to:** every new rule added to any file in [component/](../component/), and every rule that says a part appears, repeats, or disappears conditionally.

**Source:** an incident outside this repository. The withdrawals are recorded in that project's pagination standard; the cause they share is not.

## Related

- [[pagination.component.md]]
- [[dashboard.component.md]]
- [[uix.component.md]]
- [[a-copied-stylesheet-is-a-fork-nobody-declared.pattern.md]]
