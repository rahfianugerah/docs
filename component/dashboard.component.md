> Up: [[README.md]] · [[uix.component.md]]

# Dashboard and Chart Standard

## Core Requirement

**One charting library for the whole product.** It is not a per-page choice, for the same reason there is one icon set: a chart on one screen must be readable by someone who learned to read a chart on another.

This extends [[uix.component.md]]. Every color a chart uses comes from that file's token set, and this file defines none of its own.

## Decide the Form Before the Color

### Is It Even a Chart?

Most dashboard numbers are not charts.

- **One number is a stat tile.** A single value with its label, and a comparison if one exists. A pie chart of one number is decoration.
- **Two or three numbers compared once** are a small table or a row of tiles. A chart earns its place when the shape of the data carries meaning that the numbers alone do not.
- **A chart of two categories is a sentence.** Write the sentence.

### The Job Picks the Chart

| The question | The mark |
| :- | :- |
| How does this change over time | Line, time on the horizontal axis |
| How do these categories compare | Horizontal bars, sorted by value |
| How is this distributed | Histogram or box |
| How do two measures relate | Scatter |
| What share of a whole | Stacked bar, almost never a pie |

- **Sort a categorical bar chart by value**, not alphabetically, unless the category has its own natural order such as a month.
- **Bars start at zero.** A truncated axis on a bar chart misrepresents the ratio the bars exist to show. A line chart may use a non-zero baseline, and says so on the axis.
- Use a pie only for a small number of parts of one whole, and never to compare two pies.

## Color

- **A series that is merely "the third one" wears a categorical slot**, taken in a fixed order so the same series is the same color on every screen.
- **Status tokens mean state.** The tokens for good, warning, bad, and informational are reserved for series that genuinely mean those things, such as a failure rate. Never mix status and categorical meaning in one chart.
- **Sequential** scales, for magnitude, use one hue from light to dark, with visible steps and a light end that stays distinguishable from the surface.
- **Diverging** scales, for polarity around a baseline, use two hues with a neutral midpoint.
- **Never encode meaning in color alone.** Pair it with a label, a shape, or a direct annotation, per [[uix.component.md]]. Roughly one reader in twelve cannot separate two of the most common chart hues.
- Check every palette against the surface token in both light and dark, since the chart is drawn on the card, not on white.

## Axes and Labels

- Label both axes with the measure and its unit. A number with no unit is not a data point.
- **Never build a dual axis chart.** Two scales on one plot invite a comparison between things that share no unit, and the apparent crossing point is an artifact of the scales chosen. Use two charts stacked with a shared horizontal axis.
- Format a number the way a reader reads it: thousands separated, currency with its symbol, a percentage with its sign.
- Rotate a tick label only as a last resort. Horizontal bars solve long category names without rotation.
- Annotate the point that matters directly on the chart rather than leaving the reader to find it in a legend.

## Legend, Hover, and the Table View

- Drop the legend when there is one series. It is repeating the title.
- Place the legend where it does not compress the plot, and order it to match the order of the marks.
- A tooltip carries the category, the value with its unit, and nothing the reader can already see.
- **Offer the underlying table.** Every chart is an aggregation, and someone always needs the row. It is also the accessible representation of the same data.

## Layout

- The most important tile is top left, where the eye lands first.
- A row of stat tiles above the charts, not interleaved with them.
- Every chart sits in a card, with its own title stating what the chart answers.
- Charts scroll horizontally inside their own container on a narrow screen. **The page body never scrolls horizontally.**
- Reserve the chart's height before its data arrives, per [[loading.component.md]], so the page does not jump when it loads.

## Empty, Loading, and Error

- **An empty chart says it is empty**, in words, in the plot area. A blank card reads as a bug.
- A loading chart uses a skeleton at the chart's real dimensions.
- A failed chart says the data could not be loaded and offers a retry. It never renders an empty axis as though the answer were zero.
- **Zero and missing are not the same** and never look the same.

## Accessibility

- Every chart has a text alternative describing what it shows and its headline finding, not just its title.
- The table view is reachable by keyboard and is the accessible equivalent of the chart.
- Meaning never rests on color alone.
- Respect `prefers-reduced-motion`: draw the chart in its final state rather than animating it in.

## Do and Do Not

Do:

- Use a stat tile for one number.
- Sort categorical bars by value and start them at zero.
- Take every color from the token set, in a fixed order.
- Offer the underlying table.
- Say when a chart is empty.

Do not:

- Build a dual axis chart.
- Use a pie to compare, or two pies to compare with each other.
- Encode meaning in color alone.
- Let a chart make the page scroll horizontally.
- Render missing data as zero.

## Related

- [[uix.component.md]]
- [[loading.component.md]]
- [[scrollbar.component.md]]
