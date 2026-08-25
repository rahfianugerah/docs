---
tags:
  - kind/component
  - layer/frontend
  - topic/state
---

> Up: [[README.md]] · [[uix.component.md]]

# Skeleton Standard

> [!note]
> A grey block shaped like the content about to replace it. The loading state for a component whose layout is already known.

## Core Requirement

A skeleton is the loading state for **a component whose layout is already known**: a table, a list, a card grid, a stat row, a chart panel.

**A component that is loading shows a skeleton in its own place. It never hands the wait up to the page.** The route gate in [[loading.component.md]] holds the entire viewport and exists for exactly one thing, checking the session before the first paint. Using it for a table that is fetching blanks a page the reader could have been reading.

This standard extends [[uix.component.md]] and does not redefine a token.

## When a Skeleton, and When Not

| The wait | Use | Why |
| :- | :- | :- |
| A table, list, card grid, or chart whose layout is known | Skeleton | The final shape is predictable, so the page does not jump when the data lands |
| A section whose result could be one row or forty | Inline loader, per [[loading.component.md]] | A skeleton would promise a layout the app then breaks |
| The session is being checked on first paint | Route gate | Nothing can be drawn yet, and the wrong screen must not flash |
| A form the user just submitted | Button loading | The wait belongs to the control the user pressed |

The test is whether the shape is genuinely known before the data arrives. A table with fixed columns and a known page size passes it. A search result that might return nothing does not.

> [!warning]
> A skeleton that does not match what arrives is worse than a spinner. It states a layout as fact, the reader starts reading the page around it, and then the page reflows underneath them. A spinner promises nothing and is honest when the shape is unknown.

## The Class

```css
.skel {
  background: linear-gradient(90deg,
    var(--line2) 25%, var(--surface) 50%, var(--line2) 75%);
  background-size: 200% 100%;
  animation: sh 1.3s infinite;
  border-radius: var(--r-sm);
}
@keyframes sh { 0% { background-position: 200% 0 } 100% { background-position: -200% 0 } }
```

- `.skel` carries the shimmer and the radius. **The size comes from where it is used**, never from the class. One class, many shapes.
- The radius is `--r-sm`, because a skeleton always stands inside a surface, so it takes the leaf value the same as a button or an input, per [[uix.component.md]].
- **Do not add a second grey, a second radius, or a second animation to `.skel`.** Every skeleton in a project shimmers at one speed, or two loading regions on one screen look like two different states.

## Per Component

### Table

A table skeleton renders the **real header** and skeleton rows beneath it. The header is already known, so drawing it as grey blocks throws away information the reader could have used.

```html
<div class="tablewrap">
  <table>
    <thead><tr><th>Name</th><th>Team</th><th>Status</th></tr></thead>
    <tbody>
      <!-- repeated once per row the page size will produce -->
      <tr>
        <td><div class="skel" style="height:14px;width:60%"></div></td>
        <td><div class="skel" style="height:14px;width:40%"></div></td>
        <td><div class="skel" style="height:14px;width:72px"></div></td>
      </tr>
    </tbody>
  </table>
</div>
```

- **Render the number of rows the page size will actually produce**, capped at what the viewport shows. Ten skeleton rows for a page of twenty is fine; forty is animating content nobody can see.
- **Keep the real column widths.** A skeleton table whose columns shift when the data lands has caused the reflow it existed to prevent.
- **Vary the bar widths per column** so the block reads as text, not as a barcode. A name is longer than a status.
- The pager below is hidden or disabled while the skeleton shows, per [[pagination.component.md]]. A pager reading "Page 1 of 0" beside a skeleton is a contradiction the reader has to resolve.
- See [[table.component.md]] for how this state interacts with the empty and error states.

### List and Card Grid

- **One skeleton per card, at the real card size, in the real grid.** A single wide block where a grid will appear is not a skeleton, it is a grey rectangle.
- Render the number of cards one screen holds, not the number the request will return.

### Stat Row and Chart

- **A stat tile skeleton is two bars:** a short one for the label and a taller one for the value. Do not skeleton the whole tile as one block; the tile has internal structure and the reader already knows it.
- **A chart panel skeletons its plot area only.** The title and the axis labels are known before the data, so they render as real text.

## Paging and Refetching

When a table changes page, the previous rows stay in place and the loading state is drawn over the table body rather than replacing it, per [[pagination.component.md]].

> [!danger]
> Never swap a rendered table back to a full skeleton on a page change. The rows disappear, the layout height changes, and the pager moves under a pointer that was already travelling toward the next-page button. That is the same failure endless scroll has, arriving through the loading state instead.

**A skeleton is for the first load of a component.** A refetch of something already on screen keeps what is on screen.

## Accessibility

- Wrap the skeleton region in `role="status"` with `aria-live="polite"`, and give it visible or screen-reader text naming what is loading, such as "Loading the employee list". A grey block announces nothing on its own.
- Mark the skeleton blocks themselves `aria-hidden="true"`, so the wait is announced once rather than as a run of empty elements.
- **Honour reduced motion by removing the shimmer, not the block.** The block is the information; the animation is decoration:

```css
@media (prefers-reduced-motion: reduce) { .skel { animation: none; } }
```

- Never move focus onto a skeleton, and never trap the keyboard behind one.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Show a skeleton inside the component that is loading | Hold the whole page for one section |
| Render the real table header above skeleton rows | Skeleton the header too |
| Size each block where it is used | Add sizes to `.skel` |
| Render what one screen shows | Animate forty rows below the fold |
| Keep rows in place on a page change | Swap back to a full skeleton on every fetch |
| Use a spinner when the shape is unknown | Promise a layout the data will not match |
| Give the region `role="status"` and a name | Ship silent grey blocks |
| Drop the shimmer under reduced motion | Drop the block and leave nothing |

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This skeleton standard
6. Existing project conventions

## Related

- [[loading.component.md]]
- [[table.component.md]]
- [[pagination.component.md]]
- [[dashboard.component.md]]
- [[uix.component.md]]
