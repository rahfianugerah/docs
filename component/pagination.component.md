> Up: [[README.md]]

# Pagination Standard Policy

> [!important]
> Every table in every project pages. Infinite scroll and virtualized endless scroll are prohibited, and no row is ever hidden from the reader. The data behind these tables is the same data the charts read, per [[dashboard.component.md#Data Tables]].

> [!note]
> This standard has no reference implementation yet. The first project to build it becomes the source every later one copies from.

## Core Requirement

A table shows a bounded number of rows at a time, and the reader moves between those bounds by an explicit control that names where they are. This is not a performance technique that happens to be visible; it is the interaction model, and it is chosen over scrolling on purpose.

## Pagination, Never Scroll

Infinite scroll, endless scroll, and load-on-scroll virtualization are prohibited for tabular data. Four properties are lost the moment a table scrolls instead of paging, and each of them is something a user of an internal business app relies on:

- **Addressability.** Page 4 is a place. A scroll position is not: it cannot be linked, bookmarked, or described to a colleague, and it does not survive a reload. [[refresh.component.md]] requires that a view be reconstructible from its URL, and a scroll offset is not a view.
- **Boundedness.** A page has a known size, so the reader knows what they have seen. A scrolling list has no end the reader can perceive, and there is no moment at which they know they have looked at everything.
- **Exportability.** A report exports page 1 to page N, per [[dashboard.component.md#Reporting]]. There is no equivalent sentence for a scroll position, and an export from a scrolling list ends up meaning whatever the user happened to have loaded.
- **Predictability.** Rows stay where they were put. In an endless list, rows shift under the pointer as new ones load, and a click meant for one row lands on another. That failure is worst on exactly the actions that matter, such as approve and delete.

> [!failure]
> The performance argument for virtualization does not apply here. A page of 20 to 100 rows is small; nothing needs virtualizing. Virtualization only becomes necessary once the decision to render thousands of rows at once has already been made, and this policy does not make that decision.

## Adaptive Page Size

Page size follows the size of the result set, so a small table is not split into pointless pages and a large one is not delivered in fragments.

| Result set | Rows per page | Reason |
| :- | -: | :- |
| Up to 200 rows | 20 | Matches the API default, and a set this size is only a few pages deep |
| 201 to 2000 rows | 50 | Halves the page count without making one page unreadable |
| More than 2000 rows | 100 | The API ceiling; past this the answer is a filter, not a bigger page |

These sizes align with the contract in [[api.rules.md#Pagination, Filtering, and Sorting]]: `limit` defaults to 20 and is capped at 100. The ceiling is the API's, not a preference, and a page size above 100 is not available to ask for.

> [!warning]
> `total` is not known until the first response returns, so the first request of a table always uses 20. The adaptive size applies from the second request onward, once `total` has been read from the envelope. An implementation that tries to pick the size before it knows the total is guessing, and the guess is wrong on exactly the large tables the rule exists for.

The user may override the size from a control offering 20, 50, and 100. A user choice outranks the adaptive default and persists in the URL, so it survives a refresh like any other view state.

Past 2000 rows, more paging is not the answer. A reader who needs a specific row reaches it through search and filters, per [[search.component.md]], not by walking 40 pages.

## Controls

Every paginated table carries the full control set. A partial set is what forces a reader to count pages in their head.

| Control | Behaviour |
| :- | :- |
| First and last | Jump to page 1 or page N. Disabled, not hidden, when already there |
| Previous and next | Step one page. Disabled, not hidden, at the ends |
| Page number | The current page, and direct entry or selection of another |
| Range indicator | `Menampilkan 21-40 dari 137` |
| Total pages | `Halaman 2 dari 7` |

- Disable a control at a boundary rather than removing it. A control that disappears makes the row of controls change width and move the others under the pointer.
- The range indicator is not optional. It is the only element that tells a reader both where they are and how much there is, and it is what makes a page count meaningful rather than abstract.
- Write both indicators in the app's own language, and format the numbers with the same separators the rest of the app uses.
- The current page lives in the URL, per [[refresh.component.md]]. A reload returns to the same page, and the link can be sent to someone else.
- Controls sit below the table, outside the scroll region, so they stay reachable while a wide table scrolls horizontally. The scroll region itself follows [[scrollbar.component.md]]. Where they sit when the region is taller than a screen is fixed by "Where the Controls Sit" below.
- On a touch screen every control clears the 44px minimum from [[uix.component.md]].
- **The controls are one shared component, used by every paged region in the app**, tables and facet grids alike. A page that pages two kinds of thing with two different control sets has taught its reader two idioms for one action.

## Where the Controls Sit

The control set has **one home and only one**: directly below the paged content, outside its scroll region, full width, with the range indicator on the left and the navigation on the right. There is no second position and no second copy, whatever the height of the page.

> [!warning]
> An earlier version of this policy repeated the controls **above** content taller than one screen, so a reader who scanned and gave up at the top would not have to scroll back down. That rule is withdrawn. It reasoned about one list in isolation, and these pages do not hold one list: a dashboard stacks a facet grid, then a table, then another table. The upper pager of one list lands immediately beneath the lower pager of the list before it, and two pager rows in a row read as a rendering fault, not as a convenience. The problem it solved is real but smaller than the problem it caused.

Rules:

- **One set, below, always.** Do not add a second copy above, beside, or floating.
- **Size the page so it fits instead.** A page the reader has to scroll through is a page size problem, not a placement problem. A facet grid is sized to fit one screen exactly, per [[dashboard.component.md#Paged Small Multiples]], and a table adapts its size from the result, per "Adaptive Page Size" above.
- The controls sit outside the scroll region, so a wide table scrolling horizontally does not carry them off the screen.
- The controls keep their position while a page loads. A set that unmounts during the request moves the content under a pointer that was already travelling toward it, which is the same failure endless scroll has.
- Do not pin the controls to the viewport. A floating bar covers content on short screens and adds a layer that has to be dismissed on touch.
- The pager is one row on desktop. Below the mobile breakpoint it wraps to two, range above and navigation below, both still full width and both still clearing the 44px minimum from [[uix.component.md]].
- Give the pager an `aria-label` naming what it pages, such as `Paginasi daftar project`. A page carries more than one pager as soon as a dashboard carries more than one list, and `Halaman 2 dari 7` alone does not say which one it belongs to.

## The Control Set Is Never Trimmed

Every control in the set renders in every state. At a boundary a control is **disabled**, and when there is only one page the navigation is disabled too. Nothing is removed, and this holds even when a removed control would have been unusable anyway.

The page size control is the case that proves the rule, because removing it is the version that looks most reasonable:

> A table of 22 rows is set to 100 per page. There is now one page, so the pager has nothing to navigate. Trimming the row drops the buttons and the page size control together. But the single page is the **result of choosing 100**, and the control just removed is the only way to choose anything else. The reader is left on a setting they cannot undo.

Rules:

- **A control never removes the way to undo the state it produced.** This is the general form, and it is worth checking against any control that hides itself based on its own effect.
- Disable at a boundary; never remove. A control that disappears changes the width of the row and moves its neighbours under a pointer already travelling toward them.
- The range indicator renders even at one page. `Menampilkan 1-22 dari 22` is a fact the reader wants; `Halaman 1 dari 1` beside it is the price, and it is a smaller cost than a dead end.
- Applies to the facet grid as well as the table, per [[dashboard.component.md#Paged Small Multiples]].

## Table Data Source

A table receives its rows from one paginated endpoint, through the app's single API layer, and it holds no second copy of the data.

The response envelope is fixed by [[api.rules.md]] and is the same in every app:

```json
{ "items": [], "total": 0, "limit": 20, "offset": 0 }
```

- Paging is done by the **server**, with `limit` and `offset`. The client does not fetch a large set and slice it locally: that is a page size the server never agreed to, it breaks the moment the set exceeds what was fetched, and it means `total` describes something different from what is on screen.
- `total` is the count of the **filtered** set, not the table. A filter that changes the result changes the page count in the same render, and a page number beyond the new count falls back to the last valid page rather than rendering empty.
- Every list endpoint is paginated, per [[api.rules.md]]. There is no unbounded list endpoint to bind to, so a table that appears to need one is reading the wrong endpoint.

### Staying Consistent With the Charts

A dashboard table and the chart above it describe the same data, and they have to agree at every moment a user looks at them.

- Both read from **one query result**, per [[dashboard.component.md#Data Tables]]. Two independent queries drift as soon as a filter reaches one before the other.
- The chart shows the whole filtered set; the table pages through that same set. Turning to page 3 does not change the chart, because the chart was never showing page 1.
- A filter applies to both in the same render. A table showing filtered rows beside a chart showing unfiltered ones is the single most misleading state a dashboard can reach, because both look correct in isolation.
- The table is also the accessible reading of its chart, per [[analytics.rules.md#Color and Legibility]], so it carries every series the chart draws.

## No Collapsing

The guardrails in [[analytics.rules.md#Guardrails]] apply to tables in the forms a table can break them.

- **No hidden columns on load.** Every column the table defines renders on first paint. A user may hide one afterwards; nothing starts hidden. A column hidden by default is a decision made for the reader that the reader cannot see was made.
- **No silently dropped rows.** Every row in the filtered set is reachable by paging. A table never trims its own result, never caps at a round number, and never quietly excludes rows the renderer found awkward.
- **No truncated cell content without a way to read it.** A cell may clip its text visually, but the full value stays reachable through a title attribute, a tooltip, or a detail view. Text that is gone with no way to recover it is data loss dressed as layout.
- **No aggregated placeholder rows.** A table does not invent a Lainnya, Other, or Total row that is not in the data. A genuine total belongs in a footer that is labeled as computed.
- **No horizontal cropping.** A table wider than its container scrolls, per [[scrollbar.component.md]]. Columns are not dropped to make it fit.

> [!warning]
> Every one of these is invisible when it goes wrong. A reader cannot tell the difference between a table that has 137 rows and a table that has 137 rows of which it is showing 120, so the reader trusts the wrong number and has no reason to doubt it. That is why the rule is no dropping at all rather than dropping carefully.

## Empty, Loading, and Error

- An empty result renders the shared empty state from [[uix.component.md]] with the controls hidden, not a table of zero rows with a pager reading `Halaman 0 dari 0`.
- A page change shows the loading state from [[loading.component.md]] over the table body while the previous rows stay in place, so the layout does not jump and the controls do not move under the pointer.
- A failed request keeps the current page and its controls, and shows the error beside them. A table that empties itself on a network error looks exactly like a table with no data.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Page every table | Load more rows as the user scrolls |
| Ask the server for `limit` and `offset` | Fetch a large set and slice it on the client |
| Start at 20 and adapt once `total` is known | Guess a page size before the total exists |
| Disable a control at a boundary | Remove it and let the row reflow |
| Show `Menampilkan 21-40 dari 137` | Show a page number alone |
| Keep the page in the URL | Keep it only in component state |
| Repeat the controls above a region taller than a screen | Make the reader scroll a full page to reach the next one |
| Hide the controls when there is only one page | Render a row of disabled arrows |
| Render every column on load | Hide a column by default |
| Scroll a wide table | Drop columns to make it fit |

## Related

- [[analytics.rules.md]] owns the guardrails this policy applies to tabular data
- [[analytics.rules.md#Guardrails]] is where the no-collapsing rules are defined in full
- [[dashboard.component.md]] renders the charts these tables sit beside
- [[dashboard.component.md#Data Tables]] is the binding that keeps a chart and its table on one query result
- [[dashboard.component.md#Reporting]] is why every page of a table must be exportable, not only the visible one
- [[dashboard.component.md#Paged Small Multiples]] is the other paged region this control set drives
- [[api.rules.md#Pagination, Filtering, and Sorting]] fixes the `limit`, `offset`, and `total` contract
- [[search.component.md]] owns the filters that change `total` and therefore the page count
- [[refresh.component.md]] owns the URL state that makes a page addressable
- [[scrollbar.component.md]] owns the scroll region a wide table uses rather than cropping
- [[uix.component.md]] owns the control sizing and the empty state
