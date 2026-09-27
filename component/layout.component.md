---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Layout Standard

> [!important]
> An internal console fills the full width beside the navigation. There is no centered column with a maximum width. A width limit belongs to prose and to overlays, never to the page.

## Core Requirement

**An internal console is a workspace, and its content area fills whatever width the navigation leaves.**

People compare rows, scan a timeline across months, and keep a board of several columns in view. A centered column wastes the sides of a wide monitor while forcing those same tables and timelines to scroll sideways, so it costs the most exactly where the work is densest.

This extends [[uix.component.md]] and takes every spacing value from the scale defined there. A public or marketing page is a different surface and may centre its content, per the navigation rule in that file.

## The Page Shell

The shell has two parts and no third: the navigation rail, owned by [[sidebar.component.md]], and the content area beside it.

```css
.app { display: grid; grid-template-columns: 236px 1fr; min-height: 100vh; }
.main { display: flex; flex-direction: column; min-width: 0; }
.content { padding: 22px 24px 60px; width: 100%; min-width: 0; }

@media (max-width: 900px) {
  .app { grid-template-columns: 1fr; }
  .content { padding: 16px 14px 48px; }
}
```

- **`.content` never carries `max-width` or `margin-inline: auto`.** Its width is whatever the rail leaves.
- **`min-width: 0` on both `.main` and `.content` is required.** Without it a wide table or timeline stretches the grid track instead of scrolling inside its own wrapper, and the whole page scrolls sideways. This is the single most common layout bug in a sidebar shell, and it is invisible until the first wide table lands.
- **The padding is the only gutter.** A page component never adds its own horizontal padding on top of it, because two gutters stacked read as a misaligned page.
- The `.app` grid and the 900px breakpoint are the same values [[sidebar.component.md]] declares. They are one shell, so the two files must never carry different numbers.
- Below the breakpoint the rail becomes a drawer, per [[sidebar.component.md]], and the content takes the full screen width.

## What Fills the Width

Every page is made of full-width blocks stacked vertically, each separated by the same gap from [[uix.component.md]].

- **The page heading** spans the width: the title and description on the left, the page's filters and actions on the right, per [[header.page.component.md]].
- **Stat tiles** use the four-column grid from [[uix.component.md]]. At full width they stay four columns; they do not grow into five or six.
- **Cards, tables, and charts** span the full width unless two of them are meant to be read side by side, in which case they share a two-column grid.
- **A grid of repeated cards** adds columns as the width grows, with `auto-fill` or a responsive column count, instead of stretching a fixed three columns across a wide screen.
- **A timeline or a board** stretches its columns to fill the available width, and scrolls sideways only once its columns reach their minimum readable size. Measure the wrapper and widen each column to fit rather than fixing a column width.
- **A long list inside a card** pages with the shared pager, per [[pagination.component.md]] and [[table.component.md]], and scrolls inside its own card where the page size makes it tall.

## What May Carry a Width Limit

A width limit belongs to reading and to overlays, never to the page.

| Element | Limit | Why |
| :- | :- | :- |
| A paragraph of prose, such as a page description | About `68ch` | A line longer than that is hard to follow back to the start of the next one |
| An empty state message | About `340px` | It is a sentence in the middle of empty space, not a layout |
| A modal or a sheet | Its own `max-width` | It floats above the page and is centred on purpose, per [[uix.component.md]] |
| The login card | Its own cap, centred | Owned by [[login.component.md]]; it is not a console page |
| A field holding a short value | Its natural width | A code or a date input stretched across a wide screen reads as a text area |

## Do and Do Not

| Do | Do not |
| :- | :- |
| Let the content fill the width beside the rail | Give the content a `max-width` and centre it |
| Put `min-width: 0` on every grid child holding wide content | Let a wide table push the whole page into a horizontal scroll |
| Grow a card grid by adding columns on a wide screen | Stretch three fixed columns across a 2560px monitor |
| Stretch timeline and board columns to fill the width | Leave a short timeline as a narrow strip beside empty space |
| Limit the width of a prose paragraph | Limit the width of the page to keep prose short |
| Keep one gutter, from the content padding | Add horizontal padding inside a page component on top of it |
| Keep the shell values identical to the sidebar standard | Carry a second grid definition or a second breakpoint |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens, the spacing scale, the grids, and the single breakpoint | Every value this file names but does not define, and the overlay rules |
| [[sidebar.component.md]] | The navigation rail | The `.app` grid this file shares with it, and the drawer below the breakpoint |
| [[header.page.component.md]] | The header bar and the page heading | Where a page title, a page action, and a page filter belong |
| [[table.component.md]] | The table itself | Why a wide table scrolls inside its wrapper rather than widening the page |
| [[pagination.component.md]] | Paging | Why a long list pages instead of growing the page |
| [[login.component.md]] | The sign-in screen | The one centred, width-capped card in the project |

## Deviations

A public or marketing page is not a console and may centre its content, per [[uix.component.md]]. Any other intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. [[sidebar.component.md]], for anything the rail and the shell share
6. This layout standard
7. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements.

## Related

- [[uix.component.md]]
- [[sidebar.component.md]]
- [[header.page.component.md]]
- [[table.component.md]]
- [[pagination.component.md]]
- [[dashboard.component.md]]
- [[login.component.md]]
