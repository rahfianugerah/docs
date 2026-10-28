---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Button Standard

> [!note]
> Every button is a HeroUI `Button`, in one of HeroUI's seven variants, with an icon before the label and exactly one primary action per view.

## Core Requirement

**Every button is a HeroUI `Button`**, in one of the seven variants below, carries an icon where the action has a shape, and sits on the 8px radius.

HeroUI owns the markup, the press handling, the focus ring, and the pending state. This standard owns the decisions HeroUI leaves to the project: which variant an action earns, how many primary actions a view may have, where the icon goes, and how a row of buttons is ordered. Exact props come from the HeroUI MCP server, per [[stacks.rules.md]].

This extends [[uix.component.md]]. A button never gets its own color, padding, or radius; it changes only through HeroUI's theme variables.

## The Seven Variants

The variant carries the weight of the action, and weight is what tells a reader which button on a row is the one they came for. Two buttons of equal weight side by side is the most common way a screen stops having a primary action.

| `variant` | Use for | Weight |
| :- | :- | :- |
| `primary` | The one main action of the view | Highest |
| `outline` | A companion action that still reads as important | Second |
| `secondary` | A neutral action, and the trigger of a menu | Default |
| `tertiary` | A quieter neutral action beside a secondary one | Low |
| `ghost` | An action inside an already crowded row, and every icon-only button | Lowest |
| `danger-soft` | A destructive action on a page | Signals harm |
| `danger` | The confirm button inside a destructive dialog, and nowhere else | Signals harm, final |

> [!warning]
> Exactly one `primary` button per view. A second one does not make the screen twice as actionable; it removes the meaning of the first, and the reader then has to read every label to find the action instead of seeing it.

**A destructive action on a page is `danger-soft`, never solid `danger`.** Solid red is reserved for the last step, inside the dialog that asks "are you sure", so the heaviest red on screen is always the one that actually destroys something.

## Icons

A button carries an icon when the action has a recognizable shape, and the icon sits **before** the label.

```tsx
import { Button } from "@heroui/react";
import { IconCirclePlus, IconDownload, IconTrash } from "@tabler/icons-react";

<Button variant="primary"><IconCirclePlus size={16} /> Add Document</Button>
<Button variant="danger-soft"><IconTrash size={16} /> Delete</Button>
<Button variant="secondary"><IconDownload size={16} /> Download</Button>
```

Rules:

- The icon set is the project's one set, per [[uix.component.md]]. Never mix in a second set, an emoji, or an inline SVG of your own.
- The icon is `16px` on every button, a step below the `18px` body icon so it reads as part of the label rather than as a second element.
- HeroUI sets the gap between icon and label. **Do not add a margin to the icon.**
- The icon reinforces the label; it never replaces it. A button whose only content is an icon is an icon button and follows the rule below.
- Use the icon that names the action, not the object: a trash glyph for delete, a plus for add, a download arrow for download, a pencil for edit.
- **The same action wears the same icon everywhere.** Delete is one glyph on every screen, or the icon has stopped carrying meaning.

> [!danger]
> Never put a destructive icon on a non-destructive button. A trash glyph on a `primary` button reads as "delete" at a glance and as "save" on reading, and the glance is what a user acts on.

### Icon-Only Buttons

A button with no label is a HeroUI `Button` with `isIconOnly`, usually `variant="ghost"`. It is a square control for a toolbar or a table row, and it always carries an accessible name:

```tsx
<Button isIconOnly variant="ghost" aria-label="Reload"><IconRefresh size={16} /></Button>
```

An icon alone is unreadable to a screen reader and ambiguous to everyone else, so `aria-label` is required rather than encouraged, and the label says the action in the same words the visible buttons use.

## Shape and Size

- **The radius is HeroUI's `--radius`, `0.5rem`**, the one radius in the project, per [[uix.component.md]]. Never a radius on a button of its own, and never above 8px.
- **`size="md"` is the default.** `size="sm"` is for a button inside a dense row, such as a table row action or a pager, per [[pagination.component.md]]. A small button changes its height and padding only, never its radius.
- **Buttons in one row share one `size`**, so they share one height.
- On a touch screen every button clears the 44px minimum height from [[uix.component.md]].

## States

- **Hover, press, and focus are HeroUI's.** Never override them with a size change or a thicker border, which shifts every element beside the button.
- **A disabled button uses `isDisabled`**, so it is skipped by the keyboard and announced as disabled, not merely dimmed. A button that looks disabled but still fires is worse than one that does not look disabled at all.
- **HeroUI's focus ring stays**, per [[uix.component.md]]. Keyboard users navigate by it.
- **A button that submits uses `isPending`**, per [[loading.component.md]]. It shows the wait on itself, refuses a second press, and **keeps its width**.

## Buttons in a Row

- **Order by weight, lowest first, with the primary action last on the right.** That places the main action closest to where a reader ends a scan and closest to where the thumb sits on a phone.
- **A destructive action never sits directly beside the primary action.** Put a neutral button, a gap, or a separator between them, because the two are one mis-click apart and the mistake is not undoable.
- **Three buttons is the practical limit for one row.** Past that, the row is a menu, and the extra actions belong in a dropdown per [[dropdown.component.md]].
- A button that opens a menu is a `secondary` button with a trailing chevron, and that chevron rotates on open, per [[dropdown.component.md]]. It is the one case where an icon sits after the label rather than before it, because the chevron describes the button's state rather than its action.

## Labels

Labels follow the Title Case rule in [[uix.component.md]] and are written in the project's UI language.

- **Name the action, not the mechanism:** `Save Changes`, not `Submit Form`.
- **Use a verb.** A button labelled `Documents` tells a reader nothing about what pressing it does.
- **Keep a destructive label explicit.** `Delete Document` is correct; `Delete` alone in a modal that could be deleting one of two things is not.
- Never label a button with only an icon name or a symbol.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Use one `primary` button per view | Put two primary buttons on one screen |
| Use `danger-soft` on a page and `danger` only to confirm | Put a solid red button on a page |
| Put the icon before the label | Add an icon after the label, except the dropdown chevron |
| Use HeroUI's `Button` and its variants | Hand-build a button, or restyle one per page |
| Give an icon-only button an `aria-label` | Ship a bare icon button and rely on the tooltip |
| Separate a destructive action from the primary one | Seat `Delete` next to `Save` |
| Move the fourth action into a dropdown | Line up five buttons in a row |
| Keep the button width while it loads | Let it shrink to fit the loading label |
| Use `isDisabled` and `isPending` | Style a button to look disabled while it still fires |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens, the one 8px radius, the icon set, and the Title Case rule | Any value this file names but does not define, and what carries containment now that the curve does not |
| [[dropdown.component.md]] | The button that opens a menu, and the chevron on it | The one case where an icon sits after the label |
| [[loading.component.md]] | The button that is submitting | What replaces the label, and why the width must not change |
| [[table.component.md]] | The toolbar and the action column | Where two inline buttons become a menu |
| [[pagination.component.md]] | The pager | The small variant, and why it keeps the same radius |
| [[login.component.md]] | The sign-in screen | The one full-width primary button in the system |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This button standard
6. Existing project conventions

## Related

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[loading.component.md]]
- [[table.component.md]]
- [[pagination.component.md]]
- [[login.component.md]]
- [[docs.rules.md]]
