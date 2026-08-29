---
tags:
  - kind/component
  - layer/frontend
  - topic/data
---

> Up: [[README.md]] · [[uix.component.md]]

# Table Standard

> [!note]
> The wrapper, the header, the row, the cell, and the row actions. It does not own paging, which is [[pagination.component.md]].

## Core Requirement

A table is the shape data takes when the reader needs exact values rather than a shape. It owns the header, the row, the cell, the wrapper, and the empty state. It does **not** own how the reader moves between pages, which is [[pagination.component.md]], and it does not own the menus inside it, which is [[dropdown.component.md]].

Those three files describe one component in practice. **A table without a pager is a table that has silently decided how many rows exist.**

## Anatomy

A table is always three parts in this order, and the parts are never rearranged:

1. **The toolbar**, above the wrapper: the search field per [[search.component.md]], the filters, and the actions per [[button.component.md]].
2. **The wrapper**, `.tablewrap`, which owns the horizontal scroll and the radius.
3. **The pager**, below the wrapper and outside its scroll region, per [[pagination.component.md]].

The toolbar and the pager sit outside the scroll region on purpose. A wide table scrolls sideways, and a control that scrolls away with the columns is a control the reader has to hunt for.

## The Wrapper

```css
.tablewrap { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--r-sm); }
.tablewrap.scroll { max-height: min(58vh, 560px); overflow-y: auto; }
.tablewrap.scroll thead th { position: sticky; top: 0; z-index: 1; }
```

- **The wrapper is a leaf surface**, so it carries `--r-sm`, per the radius rule in [[uix.component.md]]. It only takes `--r` when it is itself a card wrapping other cards, which a table wrapper is not. Everything inside it, including a row action button, also carries `--r-sm`.
- **A table wider than its container scrolls**, following [[scrollbar.component.md]]. It never drops columns to fit, and it never shrinks the font until the columns fit.
- `.scroll` adds a vertical scroll with a sticky header, for a page whose table is the whole content. Use it sparingly: a table that needs an inner vertical scroll on top of paging is usually a page size problem, per [[pagination.component.md]].
- **Never nest a scroll region inside another scroll region.** A table inside a scrolling card traps the wheel and the reader cannot tell which surface is moving.

## Header

```css
thead th {
  text-align: left; font-size: 11.5px; font-weight: 600; color: var(--ink2);
  text-transform: uppercase; letter-spacing: .04em;
  padding: 11px 16px; background: var(--line2); border-bottom: 1px solid var(--line);
}
```

- **Header labels are Title Case in the source and uppercased by CSS**, per [[uix.component.md]]. Writing them uppercase in the markup breaks the screen reader reading and defeats a later change of mind.
- **The header names the column, not the query.** `Created Date` is a header; `created_at` is a field name.
- A sortable column carries a sort icon and toggles ascending, descending, and off. **The sort column and direction go in the URL**, per [[refresh.component.md]], so a sorted view survives a reload and can be shared.
- **The sort column is validated against an allowlist on the server**, per [[security.rules.md]]. A sort column taken from the request and interpolated into SQL is an injection.
- Never centre a header over a left-aligned column. The header aligns with its data: text left, numbers right.

## Rows and Cells

```css
tbody td { padding: 13px 16px; border-bottom: 1px solid var(--line2); font-size: 13.5px; vertical-align: middle; }
tbody tr.clk { cursor: pointer; }
tbody tr.clk:hover { background: var(--line2); }
tbody tr:last-child td { border-bottom: none; }
```

- **Separate rows with a hairline, never with a zebra stripe.** Striping adds a second visual system that carries no information and competes with the row highlight that does.
- The last row drops its border, so the wrapper's own edge is the last line the reader sees.
- A clickable row gets `.clk`, which supplies both the cursor and the hover. A row that navigates without one of those two is a hidden control.
- **A clickable row still needs a real link or button inside it** for keyboard and screen reader users. A click handler on a `tr` is unreachable without a mouse.
- **Money and counts use `tabular-nums` and align right**, per [[uix.component.md]]. Left-aligned numbers cannot be compared down a column, which is the only reason they are in a column.
- Dates use one format for the whole table, never two.

### Cell Content

- **A cell holds one value.** A cell holding `Name / ID / Role` is three columns that were merged to save width, and the reader now cannot sort or scan any of them.
- **Truncate long text visually, but keep the full value reachable** through a `title`, a tooltip, or the detail view. Text that is gone with no way to recover it is data loss dressed as layout.
- **A status is a badge, not a coloured cell background.** A painted cell reads as a warning about the row rather than a value in the column.
- Never put a raw identifier in a cell when a name exists. A UUID column is a column nobody reads.

## Actions in a Row

Row actions are the point where this file, [[button.component.md]], and [[dropdown.component.md]] meet.

- **One or two actions:** inline `.btn.sm` buttons. Two is the ceiling for inline actions; a third makes the column wider than the data beside it.
- **Three or more:** one `.iconbtn` with a vertical-dots glyph opening a menu, per [[dropdown.component.md]]. The menu carries the same labels the inline buttons would have carried.
- The action column is the last column, right-aligned, with a header that is empty or reads `Actions`.
- **A destructive row action is never the first item in the menu** and never sits directly beside a navigating action, per [[button.component.md]]. The row is small and the pointer travel between them is a few pixels.
- **A destructive row action always confirms, and the confirmation names the specific record**, because a modal reading "Delete this item?" is a modal the reader cannot verify.

> [!danger]
> Never let a row action fire from the row click itself. A row that navigates on click and deletes on a nested button will eventually delete when the user meant to open, because the nested button did not stop propagation.

## Data Source and Paging

The rows come from one paginated endpoint, and this standard does not restate the contract. It is owned by [[pagination.component.md]] and fixed by [[api.rules.md]].

What matters here is the seam:

- **The table renders exactly the items it was given.** It does not slice, filter, or sort them a second time on the client, because the pager below it is describing the server's numbers and the two would then disagree.
- A filter from the toolbar changes the total, so it changes the page count in the same render. A page number beyond the new count falls back to the last valid page rather than rendering empty rows.
- **Sorting is a server round trip**, not a client re-order of the current page. Sorting one page of 20 out of 300 rows sorts the wrong set and looks correct.

> [!warning]
> A table that pages on the client over a set it already fetched is the failure this seam exists to prevent. It shows a page count derived from what was fetched rather than from what exists, so the reader believes they have seen everything at exactly the moment they have not.

## Empty, Loading, and Error

- **Empty** renders the shared empty state from [[uix.component.md]], inside the wrapper, with the header still visible so the reader can see what the table would have held. The pager is hidden, not rendered reading "Page 0 of 0".
- **Loading** renders a skeleton, never a spinner over the table, per [[skeleton.component.md]]. The shape of a table is known before its data arrives, which is exactly the case a skeleton exists for.
- **Error** keeps the current rows and the controls in place and shows the error beside them. A table that empties itself on a network error is indistinguishable from a table with no data.

The three are mutually exclusive. Guard each on the others so an error is never drawn under a skeleton.

## No Collapsing

The guardrails in [[analytics.rules.md]] apply to a table in the forms a table can break them, and [[pagination.component.md]] states them in full. In short:

- **Every column the table defines renders on first paint.** Nothing starts hidden.
- **Every row in the filtered set is reachable by paging.** The table never trims its own result.
- A wide table scrolls rather than dropping columns.
- A computed total belongs in a footer that is labelled as computed, never as an invented row in the body.

## Accessibility

- **Use a real `<table>`** with `<thead>`, `<tbody>`, `<th>`, and `<td>`. A grid of `div` elements is not a table to a screen reader, whatever it looks like.
- Give every `<th>` a `scope`, `col` for a column header and `row` for a row header.
- Give the table a caption or an `aria-label` naming what it holds.
- A sortable header carries `aria-sort` reflecting the current state, so the sort is announced rather than only drawn.
- Every interactive element in a row is reachable by keyboard in the order it appears.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Put the toolbar above and the pager below, both outside the scroll region | Let either scroll away with the columns |
| Scroll a wide table | Drop columns to make it fit |
| Separate rows with a hairline | Add zebra striping |
| Render two inline actions, then a menu | Line up four buttons in the action column |
| Sort on the server | Re-order the current page on the client |
| Show a skeleton while loading | Cover the table with a spinner |
| Keep rows on screen when a request fails | Empty the table on an error |
| Name the record in a delete confirmation | Ask "delete this item?" |
| Give `<th>` a `scope` and the table a name | Build the table from `div` elements |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[pagination.component.md]] | How the reader moves between pages, and the data contract behind the rows | The seam this file describes from the rendering side |
| [[dropdown.component.md]] | The row action menu and the filter selects in the toolbar | What a third row action becomes |
| [[button.component.md]] | Every button in the toolbar and the action column | The small variant, and why a destructive action sits apart |
| [[skeleton.component.md]] | The loading state a table uses instead of a spinner | Why the header renders real and the rows do not |
| [[search.component.md]] | The search field above the table and the query underneath it | Why sorting and filtering happen in the database |
| [[scrollbar.component.md]] | The scrollbar a wide table uses rather than cropping | Why the horizontal bar is always visible |
| [[uix.component.md]] | The tokens, the radius scale, and the empty state | Any value this file names but does not define |
| [[refresh.component.md]] | The URL state | What makes a sorted, filtered page shareable |
| [[security.rules.md]] | Injection and object authorization | Why a sort column from a request goes through an allowlist |

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This table standard
6. Existing project conventions

## Related

- [[pagination.component.md]]
- [[dropdown.component.md]]
- [[button.component.md]]
- [[skeleton.component.md]]
- [[search.component.md]]
- [[scrollbar.component.md]]
- [[uix.component.md]]
- [[refresh.component.md]]
- [[analytics.rules.md]]
- [[api.rules.md]]
