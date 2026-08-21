> Up: [[README.md]]

# Analytics Standard Policy

> [!important]
> This policy owns the reasoning behind every chart: which chart a shape of data earns, and what may never be done to that data on the way to the screen. It renders nothing. Rendering is [[dashboard.component.md]] and tabular data is [[pagination.component.md]].

## Core Requirement

Every visualization in a project is justified against the data it represents, before it is drawn and before a single color is chosen. A chart that does not match its data shape is a spec violation, not a matter of taste.

The order is fixed and never runs backwards:

1. **State the analytical question.** What must the reader be able to do after looking at this: compare, follow, locate, or decide.
2. **Name the data shape.** How many measures, across what kind of dimension, at what density.
3. **Read the row off the matrix.** The question plus the shape select the chart. The chart never selects itself, and it is never chosen because it looked good in another dashboard.
4. **Declare the row.** The component records which matrix row it satisfies, so a reviewer can check the choice instead of guessing at it.

> [!warning]
> Picking the chart first and fitting the question to it afterwards is the most common way a dashboard becomes decorative. A bar chart nobody can state a question for is not a neutral choice; it is a claim that the comparison matters, made without anyone deciding that it does.

## Chart Selection Matrix

| Data shape | Analytical question | Chart | Why this chart |
| :- | :- | :- | :- |
| One measure across discrete categories, nominal or ordinal | Which is larger, and by how much? | Bar chart | Length on a common baseline is the most accurate comparison a human eye makes, and nothing else in this table is read as precisely. Use horizontal bars when labels are long or categories run past about seven, because rotated labels cost more legibility than the extra width does. |
| Part to whole, at most five or six parts that sum to a meaningful total | What share does each part take, and out of how much? | Donut chart | Communicates composition at a glance, and the centre states the total as a number instead of leaving the reader to infer it. Past six parts, or when parts must be compared precisely against each other, fall back to a bar chart, because arc and area are read poorly. Never use a donut for time, for negative values, or for parts that do not sum to anything. |
| One measure over a continuous or ordered dimension, usually time | How is it changing? | Line chart | Slope carries rate of change directly, which no other form does. Connect only genuinely continuous series: a line drawn between unrelated categories asserts a progression that does not exist. |
| Dense timestamped data, enough points that a pattern can appear | Is there a trend, a season, or an anomaly? | Time series analysis | Trend, seasonality, and outliers are three different findings, and this is the only row that separates them. Moving averages and bands are drawn on top of the raw points, never in place of them. |

> [!failure]
> A chart that fits no row on this matrix is not shipped. Add a row, with its reasoning column filled in and the owner's agreement, or pick an existing row. A one-off chart with no row behind it is how a dashboard stops being comparable across apps.

### The Donut Chart

The donut is the only part-to-whole form in this standard. The plain pie chart is not used.

> [!failure]
> Never ship a pie chart. Every part-to-whole question is answered by the donut, and a pie is that same chart with its centre thrown away. There is no case where a pie is the right answer and a donut is not, so there is nothing for it to be an option for.

The donut replaces a blanket ban on circular part-to-whole charts that stood in [[dashboard.component.md]], which held that angles are read poorly and that a horizontal stacked bar always says the same thing better.

The ban was right about the reading and wrong about the scope. Arc and angle genuinely are read poorly, which is why the row caps parts at six and sends any precise comparison to a bar chart. What the ban missed is the one thing a circular form is uniquely good at: showing that a set of parts is a whole. A stacked bar shows the same numbers, but the reader has to be told the bar is complete; a circle says so by its shape.

**The centre is what earns the donut its place, and accuracy is not the argument.** A part-to-whole question has two halves, what share each part takes and what the whole amounts to. The hole is where the second half goes: the total is printed as a number instead of remaining a shape the reader has to infer. That is the same reasoning [[analytics.rules.md#Combine Before You Simplify]] applies everywhere else, and it is why a donut with an empty centre is not sanctioned either.

> [!warning]
> Do not defend the donut on readability. The research is contested and the argument against it is credible: removing the centre removes the angle cue and leaves only arc length and area, which is if anything slightly harder to read. Readability is not what makes this row safe. The four constraints do that, and they are unchanged.

> [!warning]
> Every constraint on that row is load bearing: six parts, summing to a real total, no time, no negatives. A donut that breaks one of them is worse than the bar chart it replaced, because it now also implies a completeness that is not there.

## Combine Before You Simplify

A chart earns its place by how much a reader learns from it, and a single bare measure on an axis is usually the least informative thing the data can produce. Before drawing one series, ask what second piece of data would turn the number into a finding.

| One measure alone answers | The same measure combined with | Now answers |
| :- | :- | :- |
| How many this month | The same month last year | Whether this is normal |
| Total per category | The target per category | Which categories are behind |
| A count today | The running series behind it | Whether today is a spike or a level |
| A value per branch | The headcount per branch | Whether the branch is efficient or merely large |

The rule of thumb: a number is a fact, a comparison is information. A dashboard full of standalone totals makes the reader do the joining in their head, and most readers will not, so the finding stays invisible while the data sits right there.

Ways to combine that stay within the matrix:

- **Overlay a second series** on the same axes when both share a unit and a dimension, such as actual against target.
- **Add a reference line or band** for a target, an average, or a normal range, so a value is read against something rather than in isolation.
- **Encode a second variable** on an existing mark: color for a category, size for a magnitude, position for the measure. Three encodings on one mark is the ceiling.
- **Place a small multiple**, the same chart repeated once per group on a shared scale, when a single chart would need more than about seven series.
- **Pair the chart with its table**, per [[pagination.component.md#Table Data Source]]. The chart carries the shape and the table carries the exact values, and neither has to compromise to do the other one's job.

> [!warning]
> Combining is not the same as crowding, and the guardrails below are the limit. If fitting a second series onto a chart would require folding categories, truncating an axis, thinning points, cropping, or hiding a series on load, the combination is not allowed. Split it into two charts on a shared scale instead. Informativeness never buys an exception to the guardrails; a denser chart that distorts is less informative than two honest ones.

The shared scale matters when splitting. Two charts of the same measure drawn on different axes invite exactly the comparison they make wrong, which is the same failure as a truncated baseline wearing a different shape.

## Guardrails

These are hard requirements. Each names a specific way data gets distorted between the query and the screen, and each is prohibited by default.

### No Silent Aggregation

Categories are never folded into an Other, Misc, or Lainnya bucket by the renderer. A bucket invented at render time deletes the distinction the query was written to preserve, and it does so invisibly: the reader sees a category that never existed in the data and cannot tell what went into it.

Grouping is allowed only when the user asks for it, through an explicit control, and only when the grouped members stay reachable. A hover, a drill-down, or an adjacent table all qualify. A tooltip reading `Other: 412` with no way to open it does not.

### No Axis Truncation

A bar chart value axis starts at zero, always.

> [!failure]
> A truncated baseline exaggerates differences by an arbitrary factor chosen by whoever set the axis. Two bars at 98 and 100 drawn from a baseline of 97 look like a threefold difference. This is not a styling preference; it is the most widely documented way a correct number becomes a false impression, and on a bar chart it is prohibited without exception.

A line chart may use a non-zero axis, because slope rather than bar length is what the reader is reading. When it does, the axis is labeled so the baseline is visible, and the chart declares it.

### No Downsampling

No point is dropped from a series to make it render faster. Decimation changes the data: the single-sample spikes, the outliers, and the brief gaps are exactly what gets thinned first, and those are usually the finding.

A series too dense to read is handled by drawing a smoothed line over the raw points and keeping both. The raw points may be lightened, made smaller, or given lower opacity. They may not be removed.

### No Clipping

A chart container sizes to show all of its data. When it cannot, the chart region scrolls, following [[scrollbar.component.md]]. It never crops.

Hidden overflow is the worst of the five, because it leaves no trace. A truncated axis at least shows its own numbers and a folded category at least shows a bucket. Clipped data shows nothing at all, and the chart looks complete.

### No Hidden Series On Load

Every series renders visible on first paint, and every legend renders expanded. The user may toggle a series off afterwards; nothing starts off.

A series hidden at load is a decision made for the reader by whoever wrote the config, and the reader has no way to know it was made. A legend collapsed behind a control is the same problem with an extra click in front of it.

## No 3D

No chart is drawn in three dimensions: not a 3D bar, not a 3D donut, not a surface, not a rotated anything.

The reason is the one that bans axis truncation. The third dimension adds perspective, perspective changes apparent size by distance rather than by value, and the resulting comparison is wrong in a way the reader cannot correct for. Occlusion makes it worse, because the marks nearest the camera hide the ones behind them.

> [!question]
> If a requirement seems to call for a 3D chart, stop and ask the owner before building anything. This is a gate, not a default, and the answer is not automatically no: a genuine three-variable surface may be the real need. What is prohibited is reaching for 3D without asking, and the usual honest answer turns out to be a small multiple, a heatmap, or a second chart.

## Color and Legibility

- The categorical palette, the sequential ramps, and the diverging ramps live in [[dashboard.component.md]] and are validated against the common forms of color vision deficiency. Do not derive a new series color here or anywhere else.
- Never carry meaning in hue alone. A series identified only by color is unreadable to roughly one man in twelve, and unreadable to everyone once the report is printed in grayscale. Pair hue with a direct label, a marker shape, or a dash pattern.
- Label values directly on the mark wherever a reader would otherwise have to measure against an axis, which is most bar charts carrying fewer than about a dozen bars.
- A chart needing a legend of more than about seven entries is the wrong chart for the data. That is the matrix saying the categories exceed what color can carry: move to a table, or to a table beside a chart.

## Declaring the Row

Every chart component records the matrix row it satisfies, in a comment above the component or in a prop the shared wrapper reads.

This is the cheapest review mechanism available. A reviewer reads one line and checks whether the declared question matches the chart on screen, instead of reconstructing the author's reasoning from the config. It also makes the failure mode visible: a chart nobody can label is a chart nobody could justify.

## Reference Implementation

> [!note]
> This standard has no reference implementation yet. No frontend in this standard currently renders a chart with the sanctioned library, so the first app to build one becomes the source every later app copies from, per the rule in [[uix.component.md]].

Until that exists, this policy and [[dashboard.component.md]] are the only source, and the usual "the stylesheet is correct when the two disagree" clause has nothing to point at.

## Related

- [[dashboard.component.md]] renders what this policy sanctions, and owns Chart.js, the palette, layout, and PDF export
- [[dashboard.component.md#Chart Rendering]] is where the guardrails above become Chart.js configuration
- [[pagination.component.md]] owns every table, including the tables that sit beside these charts
- [[pagination.component.md#Table Data Source]] is where a chart and its table are kept on the same data
- [[uix.component.md]] owns the tokens every chart color is derived from
- [[scrollbar.component.md]] owns the scrollbar a chart region uses rather than cropping
