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
> Six variants, an icon before the label, and the control radius. There is no seventh variant and no per-page button style.

## Core Requirement

Every button is one of the six variants below, carries an icon where the action has a shape, and sits on the `--r-sm` radius.

This standard extends [[uix.component.md]]. It does not redefine a token: every color, size, and radius here is already declared in that file's `:root` block. A button that introduces its own hex value, its own padding, or its own radius is not following this standard.

## The Six Variants

The variant carries the weight of the action, and weight is what tells a reader which button on a row is the one they came for. Two buttons of equal weight side by side is the most common way a screen stops having a primary action.

| Class | Look | Use for | Weight |
| :- | :- | :- | :- |
| `.btn.pri` | Filled accent, white label | The one main action of the view | Highest |
| `.btn.out` | Surface, accent border, accent label | A companion action that still reads as primary | Second |
| `.btn` | Surface, hairline border, ink label | A neutral action, and the trigger of a dropdown | Default |
| `.btn.bad` | Surface, red border, red label | A destructive action | Signals harm |
| `.btn.dark` | Filled ink, white label | A heavy neutral action that is neither primary nor destructive | High, neutral |
| `.btn.ghost` | No background, no border, accent label | A tertiary action inside an already crowded row | Lowest |

> [!warning]
> Exactly one `.btn.pri` per view. A second one does not make the screen twice as actionable; it removes the meaning of the first, and the reader then has to read every label to find the action instead of seeing it.

`.btn.dark` exists precisely so a heavy action does not have to borrow one of the other two meanings. Reaching for `.btn.pri` makes it look like the page's main action, and reaching for `.btn.bad` makes it look destructive. Both are lies about what the button does.

`.btn.ghost` gains an `--accent-soft` background on hover. Without it the click target is invisible until the pointer is already on the text.

## Icons

A button carries an icon when the action has a recognizable shape, and the icon sits **before** the label.

```html
<button class="btn pri"><i class="ti ti-circle-plus"></i> Add Document</button>
<button class="btn bad"><i class="ti ti-trash"></i> Delete</button>
<button class="btn"><i class="ti ti-download"></i> Download</button>
```

Rules:

- The icon set is the project's one set, per [[uix.component.md]]. Never mix in a second set, an emoji, or an inline SVG of your own.
- The icon is `16px`, set once by `.btn i`, and never sized per button. It is deliberately a step below the `18px` body icon so it reads as part of the label rather than as a second element.
- The gap between icon and label is `7px`, set once by `.btn`. **Do not add a margin to the icon.**
- The icon reinforces the label; it never replaces it. A button whose only content is an icon is an icon button and follows the rule below.
- Use the icon that names the action, not the object: a trash glyph for delete, a plus for add, a download arrow for download, a pencil for edit.
- **The same action wears the same icon everywhere.** Delete is one glyph on every screen, or the icon has stopped carrying meaning.

> [!danger]
> Never put a destructive icon on a non-destructive button. A trash glyph on a `.btn.pri` reads as "delete" at a glance and as "save" on reading, and the glance is what a user acts on.

### Icon-Only Buttons

A button with no label is `.iconbtn`, not `.btn`. It is a square control for a toolbar or a table row, and it always carries an accessible name.

```html
<button class="iconbtn" aria-label="Reload"><i class="ti ti-refresh"></i></button>
```

An icon alone is unreadable to a screen reader and ambiguous to everyone else, so `aria-label` is required rather than encouraged, and the label says the action in the same words the visible buttons use.

## Shape and Size

| Property | Value | Where it is set |
| :- | :- | :- |
| Border radius | `var(--r-sm)`, 8px | `.btn` |
| Padding | `9px 14px` | `.btn` |
| Font size | `13px` | `.btn` |
| Font weight | `600` | `.btn` |
| Icon size | `16px` | `.btn i` |
| Gap | `7px` | `.btn` |
| Small variant | `6px 11px`, `12.5px` | `.btn.sm` |

The radius is `--r-sm` because a button is always nested inside something: a card, a toolbar, a table wrapper.

**Never give a button `--r` or a hardcoded `16px`.** A button at the same radius as the card it sits in makes the two read as siblings at the same level, and the card stops looking like a container. The difference between the two values is what says which box holds which, per [[uix.component.md]].

`.btn.sm` is for a button inside a dense row, such as a table row action or a pager, per [[pagination.component.md]]. It changes padding and font size only. **It never changes the radius**, so a small button and a full button on the same screen still read as the same control.

On a touch screen every button clears the 44px minimum height from [[uix.component.md]]. Where `9px 14px` padding does not reach it, the minimum is set on the button rather than the padding being inflated, so the button does not grow on the desktop layout too.

## States

- **`:hover` changes the background only**, never the size or the border width. A border that thickens on hover shifts every element beside it.
- **`:disabled` is `opacity: .55` with `cursor: default`, and the `disabled` attribute is always present** rather than the button only looking disabled. A button that looks disabled but still fires is worse than one that does not look disabled at all.
- A focus ring is required and comes from [[uix.component.md]]. Never remove the outline without replacing it; keyboard users navigate by it.
- A button that submits shows its wait on itself, per [[loading.component.md]]. The label is replaced, the button is disabled, and **the width does not change**.

## Buttons in a Row

- **Order by weight, lowest first, with the primary action last on the right.** That places the main action closest to where a reader ends a scan and closest to where the thumb sits on a phone.
- **A destructive action never sits directly beside the primary action.** Put a neutral button, a gap, or a separator between them, because the two are one mis-click apart and the mistake is not undoable.
- **Three buttons is the practical limit for one row.** Past that, the row is a menu, and the extra actions belong in a dropdown per [[dropdown.component.md]].
- A button that opens a menu is a default `.btn` with a trailing chevron, and that chevron rotates on open, per [[dropdown.component.md]]. It is the one case where an icon sits after the label rather than before it, because the chevron describes the button's state rather than its action.

## Labels

Labels follow the Title Case rule in [[uix.component.md]] and are written in the project's UI language.

- **Name the action, not the mechanism:** `Save Changes`, not `Submit Form`.
- **Use a verb.** A button labelled `Documents` tells a reader nothing about what pressing it does.
- **Keep a destructive label explicit.** `Delete Document` is correct; `Delete` alone in a modal that could be deleting one of two things is not.
- Never label a button with only an icon name or a symbol.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Use one `.btn.pri` per view | Put two filled accent buttons on one screen |
| Put the icon before the label | Add an icon after the label, except the dropdown chevron |
| Set the radius from `--r-sm` | Hardcode a radius, or borrow `--r` from the card |
| Give an icon-only button an `aria-label` | Ship a bare icon button and rely on the tooltip |
| Separate a destructive action from the primary one | Seat `Delete` next to `Save` |
| Move the fourth action into a dropdown | Line up five buttons in a row |
| Keep the button width while it loads | Let it shrink to fit the loading label |
| Set the `disabled` attribute | Style a button to look disabled while it still fires |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens, the radius scale, the icon set, and the Title Case rule | Any value this file names but does not define, and why a button takes the leaf radius |
| [[dropdown.component.md]] | The button that opens a menu, and the chevron on it | The one case where an icon sits after the label |
| [[loading.component.md]] | The button that is submitting | What replaces the label, and why the width must not change |
| [[table.component.md]] | The toolbar and the action column | Where two inline buttons become a menu |
| [[pagination.component.md]] | The pager | The small variant, and why it keeps the same radius |
| [[login.component.md]] | The sign-in screen | The one full-width primary button in the system |

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard, the same requirement [[uix.component.md]] sets for the rest of the system.

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
