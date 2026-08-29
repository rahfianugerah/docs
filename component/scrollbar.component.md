---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Scrollbar Standard

> [!note]
> The one shared scrollbar: a pill thumb, no arrows, following the component it scrolls.

## Core Requirement

**A region that scrolls must show that it scrolls.**

This is the rule everything else here serves, and it is the one most often broken. A hidden scrollbar on a region with more content below it produces a page where the remaining content simply does not exist as far as the user is concerned.

This extends [[uix.component.md]] and uses its tokens.

## A Scrollbar Is an Affordance, Not Decoration

Hiding a scrollbar is styling that removes information. The scrollbar answers two questions nothing else on the screen answers: is there more, and how much more.

- **Never set `scrollbar-width: none` or hide the WebKit scrollbar** on a region a user scrolls.
- Never rely on a fade or a shadow alone to imply more content. It says something is below; it does not say how much, and it disappears on the platforms that need it most.
- A custom scrollbar is allowed. An absent one is not.

## The Shared Scrollbar

One scrollbar style for the whole product, defined once beside the token set and applied wherever a region scrolls.

Two properties matter and are non-negotiable: **the thumb is a full pill**, and **there are no arrow buttons**.

```css
/* The shared scrollbar. Applied to every scrollable region. */
.scroll, .tablewrap, .sheet, .content, .selectpop {
  scrollbar-width: thin;                          /* Firefox: thin, and never arrows */
  scrollbar-color: var(--ink3) transparent;       /* thumb, track */
}

.scroll::-webkit-scrollbar,
.tablewrap::-webkit-scrollbar,
.sheet::-webkit-scrollbar,
.content::-webkit-scrollbar,
.selectpop::-webkit-scrollbar { width: 10px; height: 10px; }

.scroll::-webkit-scrollbar-track,
.tablewrap::-webkit-scrollbar-track { background: transparent; }

.scroll::-webkit-scrollbar-thumb,
.tablewrap::-webkit-scrollbar-thumb {
  background: var(--ink3);
  border-radius: 999px;                           /* full pill, both ends */
  border: 2px solid var(--surface);               /* inset, so the pill never touches the edge */
  background-clip: padding-box;
}

.scroll::-webkit-scrollbar-thumb:hover,
.tablewrap::-webkit-scrollbar-thumb:hover { background: var(--ink2); }

/* No arrows at either end, on any scrollbar. */
::-webkit-scrollbar-button { display: none; width: 0; height: 0; }
::-webkit-scrollbar-corner { background: transparent; }
```

Rules:

- **The thumb radius is `999px`, the full pill** from the shape scale in [[uix.component.md]]. Not `--r`, not `--r-sm`. A rectangular or slightly rounded thumb is not this component.
- **`::-webkit-scrollbar-button` is `display: none`**, so there is no arrow at the start and none at the end. Firefox with `scrollbar-width: thin` draws none either, so the two engines match.
- **The track is transparent.** It takes the color of whatever the component's own background is, which is what makes the scrollbar follow the layout rather than sit on top of it. Never a contrasting stripe.
- **The `2px` border with `background-clip: padding-box` insets the thumb** inside the 10px channel, leaving a visible 6px pill with breathing room on both sides. Without it the pill touches the container edge and stops reading as a pill.
- **The thumb rests at `--ink3` and darkens to `--ink2` on hover.** It is visible at rest, because a scrollbar that appears only on hover is not an affordance.
- Keep the thumb wide enough to grab with a mouse. A two-pixel hairline is a decorative line, not a control.
- **Style both engines together.** Styling only the WebKit pseudo-elements leaves Firefox on its platform default, which is the widest visual divergence between two browsers in the whole app.
- **Never animate the thumb's size or position.** The browser owns that.

## The Scrollbar Belongs to the Component

**The region that scrolls owns its scrollbar**, and the page does not scroll on its behalf.

- Put the overflow on the element whose content overflows, not on an ancestor.
- A modal body scrolls inside the modal. The page behind it does not scroll at the same time.
- **Lock the background when a modal or drawer is open**, and restore the scroll position when it closes, per [[refresh.component.md]].
- Never nest two vertical scroll regions. The user cannot tell which one their wheel will move, and neither can the browser.

## Tables

A wide table is the most common horizontal scroll in a product, and the most commonly broken.

- **The table scrolls inside its own container**, with the overflow on that container. The page body never scrolls horizontally.
- Keep the header row visible while the body scrolls vertically.
- Where the first column identifies the row, pin it while the rest scrolls horizontally, or the numbers stop meaning anything.
- Give the container a maximum height only when the surrounding layout genuinely needs one. A table free to grow inside a scrolling page is easier to read than one squeezed into a small window.
- **The horizontal scrollbar under a wide table is always visible.** Never hide it. It is the only cue that more columns exist.
- The scrollbar sits directly below the last row, inside the table's bordered container, so it reads as belonging to the table.
- **Reserve the space** rather than letting the layout jump when the scrollbar appears: `scrollbar-gutter: stable` on the wrapper.
- On a touch screen the platform draws the scrollbar as an overlay that fades when idle. That is correct and is not to be worked around; the touch gesture is its own affordance.

## Where It Applies

Anywhere content can exceed its box: a sidebar nav, a modal body, a table container, a long select list, a code block, a chart container, a card list with a fixed height.

### The Two Exceptions

- **A carousel or a snap track** that moves by control rather than by dragging a bar may hide its scrollbar, provided the controls are visible and the position is shown some other way, such as dots.
- **A single-line horizontally scrolling strip of chips**, where the content is obviously cut and the gesture is the only interaction, may hide it. Fade the trailing edge so the cut is visible.

- **A narrow floating panel** where a scrollbar would take a meaningful share of the width and the content visibly continues past the fold, such as a year grid inside a date panel.
- **A fixed narrow rail** whose content only occasionally overflows, such as a sidebar nav, where a scrollbar would sit permanently beside the navigation.

Everything else shows its scrollbar. These are documented exceptions, not a pattern. If a new case seems to need hiding, that is usually a sign the region is too small, and the fix is the layout rather than the scrollbar.

## Accessibility

- **Never remove a scrollbar from a region that has no other affordance.** A horizontal table scroll with a hidden scrollbar is unusable with a mouse.
- A scrollable region is reachable and operable by keyboard. Give a scrollable container that holds no focusable child a `tabindex="0"` so arrow keys, Page Up, and Page Down work in it.
- **The thumb at `--ink3` clears 3:1 against a white surface**, so it is visible to a low-vision user. Do not lighten it to `--line`, which does not.
- Never rely on a fade or an appear-on-hover scrollbar as the only indication that content continues.
- Respect the platform on touch: do not force a persistent scrollbar over content on a small screen.
- Give a scrollable region an accessible name where it is a distinct region, so a screen reader user knows what they are scrolling.
- **Never trap the wheel** or override the platform's scrolling behaviour.
- Respect `prefers-reduced-motion` on any programmatic scroll: jump rather than smooth-scroll.


## Do and Do Not

Do:

- Show a scrollbar on every region that scrolls.
- Put the overflow on the element that actually overflows.
- Scroll a wide table inside its own container.
- Keep a table header visible while the body scrolls.
- Make a scroll region keyboard reachable.

Do not:

- Hide a scrollbar for looks.
- Nest two vertical scroll regions.
- Let the page body scroll horizontally.
- Use a fade alone to signal more content.
- Style the thumb so thin it cannot be grabbed.


## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens and the shape scale | Why the thumb is a full pill and not a token radius |
| [[table.component.md]] | The wide table | The case this component exists for |
| [[pagination.component.md]] | Paging rather than scrolling | Why a long list pages and a wide one scrolls |
| [[dropdown.component.md]] | The panel that scrolls when the list is long | One of the regions this style applies to |
| [[calendar.component.md]] | The year grid | One of the two documented exceptions that hides its scrollbar |
| [[sidebar.component.md]] | The rail | The other documented exception |
| [[dashboard.component.md]] | The chart region | Why a chart scrolls rather than cropping |

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This standard
6. Existing project conventions
## Related

- [[uix.component.md]]
- [[refresh.component.md]]
- [[dashboard.component.md]]
- [[sidebar.component.md]]
