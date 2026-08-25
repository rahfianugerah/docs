---
tags:
  - kind/component
  - layer/frontend
  - topic/data
---

> Up: [[README.md]] · [[uix.component.md]]

# Dashboard and Reporting Standard

> [!important]
> This standard owns rendering: the library, the palette, axes, layout, the report, and PDF export. It does not decide which chart a dataset earns. That reasoning lives in [[analytics.rules.md]], and this file may not sanction a chart type that document does not.

## Core Requirement

A dashboard renders what [[analytics.rules.md]] sanctions, and renders it without losing anything on the way to the screen. The guardrails in that document are not advice to keep in mind here; they are configuration this file has to set explicitly, because several of them are things a charting library will otherwise do by default.

## The Library

**Chart.js, one library, wrapped once.**

- Use Chart.js for every chart. Do not add Plotly, Recharts, ApexCharts, ECharts, D3, or a hand-rolled SVG chart alongside it, and **never two chart libraries in one project**.
- **Register only the controllers the project draws.** Importing the auto bundle pulls in every chart type the library has, including the ones this standard does not sanction, and bundle size is the reason the library was chosen.
- Pin the major version like any other dependency, per [[stacks.rules.md]].
- **Wrap it in one shared chart component** rather than calling it directly from a page. The wrapper applies the option defaults, the palette, the number format, the guardrail configuration, and the empty state once, so twenty charts cannot drift into twenty configurations.
- Set `responsive: true` with `maintainAspectRatio: false`, and let the container decide the height. Never give a chart a fixed pixel width.
- **Set `devicePixelRatio: 2` on every chart.** The canvas is what the PDF export reads, and a canvas rendered at CSS scale is soft the moment the document is zoomed or printed.
- **Load the library on use, not on first paint.** A dynamic `import()` inside the wrapper puts it in its own chunk, so a page that draws no chart pays nothing for it.
- **Format every number through one shared formatter**, in axis ticks and tooltips alike, so separators match the rest of the UI. Chart.js ships no locale option; the formatting is the project's to supply, in one place.
- Write the tooltip callbacks rather than accepting the defaults, so a tooltip reads `Completed: 1,240 cards` and not `undefined: 1240`.
- A chart is loading, empty, or in error like any other section: use the states in [[loading.component.md]] and [[skeleton.component.md]] and the shared empty state in [[uix.component.md]]. **Never render empty axes as though they were data.**

> [!warning]
> **A tick callback must branch on the scale type.** A category scale hands the callback the tick's **index**, not its label, so a plain number formatter silently rewrites a whole axis of names as `0`, `1`, `2`. Return the label for the value on a category scale and format only on a linear one. The failure surfaces on horizontal bars, the one form that puts names on the axis a value formatter is usually attached to.

### Why This Library

Chart.js is chosen for weight. It draws every form this standard sanctions, and it is roughly a fifth the size of the nearest full-featured alternative for the same set of charts. Lazy loading a heavier library moves that cost rather than removing it.

What is given up is real and worth naming: built-in zoom, pan, and box select are not in Chart.js, and neither is a locale. A dashboard that genuinely needs to zoom into a dense series is the one case to raise rather than to work around, and the locale is supplied by the project in one place.

The choice also decides the export path below. **A Chart.js chart is a canvas**, so an export asks the canvas for its own image directly, at the density it was rendered at, rather than screenshotting the browser.

### Rendering a Canvas, Not an SVG

Two consequences follow, both handled in the wrapper rather than per chart:

- **Text drawn into the canvas is not text.** It cannot be selected, searched, or read by a screen reader, and it does not scale with the user's font size. Anything a reader might need to read as text, such as the total in a donut's hole, is HTML positioned over the canvas instead. That also removes the coordinate arithmetic: HTML centres itself.
- **The canvas has no DOM to inspect.** The table view required below is therefore not optional; it is the only accessible reading of the chart.

## Chart Rendering

Each guardrail from [[analytics.rules.md]] becomes a specific setting here. The library's defaults violate two of the six, so leaving them alone is not neutral.

| Guardrail | What the wrapper sets | What happens without it |
| :- | :- | :- |
| No axis truncation | `beginAtZero: true` on the value axis of every bar chart | The library fits the axis to the data and invents a baseline, exaggerating small differences |
| No hidden series on load | Never set `hidden: true` on a dataset | A series ships invisible and the reader has no way to know it exists |
| No collapsed legends | Legend display on, never behind a control | The identity of the series is one click away and most readers never click |
| No clipping | Container sizes to the data; the chart region scrolls per [[scrollbar.component.md]] | The figure crops silently and looks complete |
| No downsampling | No decimation plugin, and no bucketing that drops points | The spikes and gaps that were the finding are the first thing thinned |
| No silent aggregation | No renderer-side bucketing into an "Other" slice | A category appears that never existed in the data |

> [!danger]
> Never draw a chart in three dimensions. Chart.js ships no 3D type, which removes the temptation rather than the rule: do not reach for a plugin or a second library to add one. If a requirement seems to call for it, stop and ask the owner first, per the gate in [[analytics.rules.md]].

### The Donut

Register the doughnut controller and the arc element. **There is no pie**, because [[analytics.rules.md]] does not allow one.

- **Print the total in the centre.** An empty centre gives up the angle cue and buys nothing back, which is the one way to get the worst of both forms.
- **Put that centre text in HTML over the canvas, not drawn into it.** A centre plugin has to measure the arc and compute a coordinate, and it gets that coordinate wrong the moment the canvas resizes; an absolutely positioned element with `display: grid; place-items: center` is always centred, stays selectable, and is read by a screen reader. Set `pointer-events: none` on it so the tooltip underneath still works.
- **Position that overlay from the arc's own centre, not from the canvas box.** The two are the same only while the chart has no legend. A legend takes the bottom edge of the canvas, the chart is drawn higher to make room, and an overlay stretched across the canvas box stays centred on the box and lands below the hole. The library knows where the arc is: read the first arc's `x` and `y` from an `afterDraw` plugin and place the element at that point. Doing it on `afterDraw` rather than once at creation keeps it right through every resize.
- **The tooltip is HTML too, and it is the reason the rule cannot be applied by halves.** The library draws its own tooltip *into* the canvas, and that produces two failures at once against HTML text sitting above the same canvas. The text wins the paint order and shows through the tooltip box at every position; and the tooltip cannot be drawn past the edge of its own canvas, so on a small multiple around 118px wide it is cut off mid-sentence. Neither is reachable from CSS and neither is fixed by moving the tooltip.

  Disable the built-in tooltip and supply an external one, rendering a single shared element on `document.body` with `position: fixed`. Being outside the canvas it cannot be clipped by it, cannot be clipped by a scrolling ancestor, and sits above the centre text rather than beneath it. **Clamp its position into the viewport**, or the facet in the last column reproduces the clipping one level further out. **Build it from DOM nodes and `textContent`, never `innerHTML`**: the content carries names that people typed, per [[security.rules.md]].
- Keep the cutout at roughly `55%` to `60%` on a full-size donut. Smaller and the total has no room; larger and the arcs get thin enough that the small slices stop being readable. A small multiple may go to `68%`, because it carries two slices and a short percentage rather than a legend.
- **Label every slice with its name and its value**, on the arc or in the legend beside it. With more than two slices the legend alone is a matching exercise, which is the reading this form is already weak at.
- **Order slices by size, largest first, clockwise from twelve o'clock.** An arbitrary order makes rank something the reader has to work out instead of see. The library draws datasets in the order given and never reorders them, so order the data before it reaches the chart.
- **A donut whose values are all zero draws nothing**, and an empty cell reads as a chart that failed to load. Substitute a single full slice in the neutral rest colour, so an empty subject still renders as an empty ring.

### Paged Small Multiples

Faceting is the remedy [[analytics.rules.md]] already prescribes past six series. Past roughly a dozen facets the facet grid has the same problem the series count had: everything is on screen and none of it is readable.

- **Page the facet grid.** Size the page so one page fits one screen without scrolling; eight facets in a four-by-two grid is the worked value. A reader who has to scroll to see the page they are on gets no benefit from the paging.
- Use the same pager as the tables, per [[pagination.component.md]], with the same range indicator and the same disabled-at-the-ends behaviour. A second pagination idiom on one page is one too many.
- **Keep the facet page in the URL**, per [[refresh.component.md]], so a reload returns to it.
- **Each facet is its own canvas in a CSS grid**, with its label as an HTML `figcaption` beneath it. Drawing the whole grid into one canvas means computing a domain and a label coordinate per cell, and those coordinates are what drift out of alignment between one cell and the next.
- Paging the facets does not break the rule that a chart shows the whole filtered set, **because the paired table beneath carries every facet.** That pairing is required: a paged facet grid without its table is dropping data.
- In the report, a paged facet grid contributes the page that is on screen, composited from the individual canvases, and the full set travels in the table. This is the one place a chart in the export is not the whole set, and it is allowed only because the table beside it is.

## Is It Even a Chart

Before reaching for a chart type at all, check that the answer is a chart:

| The data is | Use | Not |
| :- | :- | :- |
| A single current value, with or without a trend | A stat tile: value, delta, optional sparkline | A one-bar bar chart |
| A handful of headline numbers | A row of stat tiles | A grouped bar chart |
| The one number the dashboard leads with | A hero figure | A gauge |
| A single ratio against a limit | A meter on one hue | A donut with two slices |
| More than about seven classes that all matter | A table, or a table beside a chart | More colors |

A KPI does not become more informative by being drawn as a chart. Keep the stat tile and the hero figure as shared classes in the stylesheet, alongside the rest of the component set.

## The Categorical Palette

Assign these in **fixed order**, starting at slot 1, never cycled and never reordered per chart. **Color follows the entity, not its rank**, so a filter that removes a series must not repaint the ones that remain.

| Slot | Hex | Hue |
| :- | :- | :- |
| 1 | `#1273AE` | Blue |
| 2 | `#A50000` | Dark red |
| 3 | `#16915a` | Green |
| 4 | `#5D5DED` | Indigo |
| 5 | `#b9791a` | Amber |
| 6 | `#0891b2` | Cyan |

Measured on a white surface, this order passes every check: lightness band, chroma floor, contrast, and colorblind separation. The worst adjacent pair is green against dark red at **ΔE 12.4** under deuteranopia, well above the 8 target, and **23.2** for normal vision.

**The order is the safety mechanism, not a preference.** Red sits at slot 2 and green at slot 3 because the dark red separates from green by lightness; putting a mid red next to green collapses them to ΔE 5.3 under deuteranopia, which is the single most common way a chart becomes unreadable.

A project that brings its own brand replaces these hexes and revalidates in the same order. Swapping a hex without rerunning the checks is how a palette that looks brighter becomes one two readers in a hundred cannot use.

Rules:

- **Six is the ceiling.** A seventh series means small multiples on a shared scale, or a table, per [[analytics.rules.md]].
- **Scatter, bubble, map, and small multiples cap at three series**, slots 1 to 3. In those forms any two marks can end up side by side, and slot 4 collides with slot 1 at ΔE 13.2 for normal vision. Facet instead of seating a fourth.
- **Never generate a seventh hue.** A generated hue is indistinguishable from an existing one under colorblindness and breaks every check at once.
- **Never fold the remainder into an "Other" bucket.** That is exactly the silent aggregation [[analytics.rules.md]] prohibits. Faceting and tables keep every category reachable; a bucket invented by the renderer does not.

## Sequential and Diverging

**Sequential**, for magnitude. One hue, light to dark, validated as monotone with visible steps and a light end that clears the surface:

```text
#6bb5e2 > #2f92cb > #1273AE > #0e5883
```

- **Do not extend it with a lighter step.** A background tint reaches only about 1.1:1 against white, so a cell painted with it looks empty.
- **Never use a rainbow ramp.** It invents order where the data has none and is unreadable under colorblindness.

**Diverging**, for polarity around a baseline: one arm, a neutral gray midpoint, then the other arm.

```text
#A50000 > #cf3f3a > #e6e8ec > #2f92cb > #0e5883
```

- **The midpoint is neutral gray, never a hue.** A colored midpoint reads as a third category.
- Keep the same number of steps on each arm, and **centre the scale on the real baseline** rather than on the midpoint of the data.

**Status colors are reserved.** `--ok`, `--warn`, `--bad`, and `--info` mean state, and a series wears them only when the series genuinely means good or bad, such as a failure rate. A series that is merely the third one wears a categorical slot. Never both in one chart, and always pair a status color with a label or an icon, per [[uix.component.md]].

## Marks, Axes, and Labels

- **Lines are 2px. Markers are at least 8px.** Bars carry a 2px gap of surface color between adjacent fills and between stacked segments, so the boundary is visible without a border.
- Grid lines are `--line2`, axis lines and ticks are `--ink3`, and neither competes with the data.
- Axis and tick labels are `--ink2`; the chart title is `--ink` at 600 weight.
- **Text always wears an ink token, never a series color.** The colored mark beside a label carries the identity; a value printed in the series hue is unreadable at small sizes and fails contrast.
- **Direct-label selectively:** the last point of a line, the largest bar, the series the chart is about. Never a number on every point.
- Money and counts use `tabular-nums` and align right, per [[uix.component.md]].
- **Start a bar value axis at zero, without exception.** This is a guardrail, not a default to be weighed against the look of the chart.

### One Axis

**Never build a dual axis chart.** Two y-scales on one plot invite the reader to compare two things that share no unit, and the apparent crossing point is an artifact of the scales chosen.

When two measures of different magnitude belong on one screen, use two charts stacked, small multiples, or index both to a common base of 100. This is the same conclusion [[analytics.rules.md]] reaches from the other direction: combining is good, and a dual axis is not a combination, it is a coincidence of scale.

## Legend, Hover, and the Table View

- **A chart with two or more series always carries a legend, expanded, with every series visible.**
- With four or fewer series, direct-label as well, so identity never rests on color alone.
- Ship the hover layer. Keep a unified hover on line and area charts and a per-mark tooltip on bar, scatter, and heatmap. **Write the hover template** rather than accepting the raw one, so it shows a formatted number and a real label instead of a trace index.
- **Every chart has a table view of the same data**, either beside it or behind a toggle. It is how a screen reader user reads the chart, how someone copies a number, and the relief channel for any color sitting near a contrast floor.
- Filters sit in one row above the charts, and **every filter is reflected in the URL**, per [[refresh.component.md]], so a filtered report survives a refresh and can be sent to someone else.

## Dashboard Layout

- **Lead with the headline:** a hero figure or a KPI row of stat tiles, then the charts, then the detail tables.
- Stat cards use the four-column grid and charts the two-column grid, both collapsing to one column below 900px, per [[uix.component.md]].
- **Each chart container sizes to show all of its data.** A container that cannot fit its data scrolls its chart region; it never crops and it never shrinks the figure until the labels collide.
- **One chart answers one question.** A chart that needs a paragraph to explain it is two charts.
- **Give every chart a title that states the finding, not the mechanism.** "Requests Awaiting Approval by Team" is a title; "Request Data Chart" is not.
- Do not exceed roughly six charts on one page. Past that it is a report to be split by section or by tab.
- A dashboard is read on a phone too. Below 900px a chart keeps its height, scrolls horizontally inside its wrapper if it must, and **never shrinks its labels below 12px**.

## Data Tables

Every table on a dashboard is a paginated table, governed by [[pagination.component.md]] and [[table.component.md]]. A dashboard never invents its own table behaviour, and it never renders an unpaginated list of rows because the set happened to look small during development.

- **A chart and the table beneath it read the same query result**, not two queries against the same source. Two queries drift the moment a filter is applied to one and not the other, and the reader has no way to tell which number is stale.
- A filter applied above the charts applies to the table in the same render.
- **Changing the table page never re-renders or re-scales the chart.** The chart shows the whole filtered set; the table pages through it. They answer different questions about the same data.
- The table is also the accessibility path for its chart, so it carries every series the chart draws, with no column hidden on load.

## Reporting

A report is the printable form of a dashboard, and it is a defined artifact rather than whatever the page happened to look like.

Every report carries, in this order:

1. **A header** with the product name per [[title.header.component.md]], the report title, and the scope it covers.
2. **The generation timestamp**, ISO 8601 with an explicit offset per [[api.rules.md]], plus who generated it.
3. **The active filters, written out.** A report without its filters printed is a report whose numbers cannot be reproduced.
4. **Every chart on the page**, in page order, each with its title.
5. **Every table on the page, in full**, across all pages, not only the page that was on screen.
6. **A page footer** with a page number and the total page count.

A report that silently omits the table pages the user was not looking at is the export version of collapsing, and it is the easiest of all these rules to break by accident, because the naive implementation exports what is rendered. **The exporter reads the full result set, not the DOM.**

## PDF Export

Export asks each canvas for its own image, assembled into the document.

```text
canvas > canvas.toDataURL("image/png") > addImage > save
```

- Render every chart at `devicePixelRatio: 2`, so the canvas is already at twice the density and the export returns a raster that is not soft when the PDF is zoomed or printed. **There is no second render at export time.** Charts are images in the export; text and tables are drawn as real text, so they stay selectable and searchable.
- **Take the image's aspect ratio from the canvas's own `width` and `height`, not from its CSS size**, or the figure is squashed in the document.
- **Ask each canvas for its own image. Never screenshot the viewport:** a screenshot captures the crop, which is precisely what these rules forbid. Compositing several canvases into one image is not a screenshot, and it is how a facet grid is exported.
- Tables are written from the full result set, paged across as many PDF pages as they need.
- Every dependency is pinned to a major version, per [[stacks.rules.md]].

Two alternatives were considered and rejected. A print stylesheet driven by the browser print dialog needs no dependency and keeps text selectable, but the output depends on the browser, the margins and headers are outside the app's control, and a paged table prints only its current page unless the app renders a second full copy for print anyway. Server-side rendering is the most consistent of the three, and it was rejected on cost: it means another always-on service to run and pay for, which the budgets in [[deploy.rules.md]] do not have room for.

> [!warning]
> Whatever is exported must equal what the guardrails require on screen: every series, every category, every row, every axis starting where it should. An export path that quietly differs from the screen is worse than no export, because a PDF is what gets forwarded and archived, and the reader of the file has no dashboard to check it against.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Read the chart type off [[analytics.rules.md]] | Pick a chart because it looks good and justify it after |
| Set `beginAtZero: true` on bar value axes | Let the library fit the axis to the data |
| Keep every series visible on load | Ship a dataset as hidden |
| Facet or tabulate past six series | Fold the remainder into an "Other" bucket |
| Overlay a smoothed line on the raw points | Decimate a dense series |
| Scroll a chart region that cannot fit | Crop it with hidden overflow |
| Export by asking each figure for an image | Screenshot the viewport |
| Export every page of every table | Export what is currently rendered |
| Draw a donut with its total in the centre, in HTML | Draw a pie, or a donut with an empty hole |
| Page a facet grid and pair it with its table | Put forty facets on one screen |
| Register only the controllers the project draws | Import the auto bundle |
| Build a tooltip from `textContent` | Build it from `innerHTML` |

## Deviations

A deviation is allowed only when it is documented in the project README, names the rule it departs from, and gives the reason. An undocumented deviation is a defect.

## Conflict Resolution

When this standard and [[analytics.rules.md]] disagree about whether a chart may be used, the analytics document wins: it owns selection and this one owns rendering.

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[analytics.rules.md]], on chart selection
5. [[uix.component.md]]
6. This dashboard standard
7. Existing project conventions

## Related

- [[analytics.rules.md]]
- [[pagination.component.md]]
- [[table.component.md]]
- [[uix.component.md]]
- [[loading.component.md]]
- [[skeleton.component.md]]
- [[scrollbar.component.md]]
- [[refresh.component.md]]
- [[title.header.component.md]]
- [[stacks.rules.md]]
