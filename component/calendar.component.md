> Up: [[README.md]] · [[uix.component.md]]

# Calendar Standard

## Core Requirement

Every date field follows this policy: the trigger that shows the chosen date, the panel that opens, and the day, month, and year views inside it.

This policy extends [[uix.component.md]] and reads every color, radius, and shadow from its token contract.

## Native Input or Custom Panel

Unlike a `select`, where native is the default, a date field is a genuine judgement call. Decide with this table rather than by habit.

| Use `<input type="date">` when | Build a custom panel when |
| :- | :- |
| The form is simple and the design is flexible | The panel must match the design system |
| A locale-driven display format is acceptable | The display format must be the same for every user |
| Nothing beyond a single date is needed | You need a range, a preset, disabled dates, or a marker on a day |
| You want zero JavaScript and free accessibility | The field sits beside a themed select and must match it |

The trade is real in both directions.

**A native date input** gives you keyboard entry, a screen reader implementation, and the platform picker on mobile, all for free and all better than most hand-built versions. But its picker cannot be styled at all, and its **displayed format follows the machine's locale**, so the same field reads `03/04/2026` to one user and `04/03/2026` to another. On a form where that ambiguity matters, native is disqualified on correctness, not on looks.

Do not try to split the difference. An `appearance` reset with `::-webkit-calendar-picker-indicator` styles the closed control and never the panel, and support diverges by platform. Pick one path.

## Value and Display Are Different Things

This is the rule that prevents the most bugs.

- **The value the component holds and emits is an ISO date: `yyyy-mm-dd`.** That is what goes to the API and into storage.
- **The value shown to the user is formatted**, by one shared formatter in the project, never inline in a component.
- The two never mix. A component that emits a display-formatted string, or shows a raw ISO string to a user, is not following this policy.
- Use `Intl.DateTimeFormat` for display rather than hand-built month arrays, so the project gets a locale for free without a lookup table per language.
- **Beware the timezone trap.** `new Date("2026-03-04")` parses as UTC midnight, which is the *previous day* in any negative offset. Construct with `new Date(y, m, d)` for a calendar date, or keep the value as a string and never let it become a `Date` at all.
- A date without a time is a calendar date, not an instant. Do not store it as a timestamp and do not apply a timezone to it.

## The Trigger

The trigger looks like every other form control, so a date field and a select in one row read as the same kind of thing.

```html
<button class="datetrig" aria-haspopup="dialog" aria-expanded="false">
  <span class="icon" aria-hidden="true"></span>
  <span class="value">04/03/2026</span>
  <span class="chev" aria-hidden="true"></span>
</button>
```

- A leading calendar icon, the value or a placeholder, a trailing chevron.
- The placeholder shows the **format**, such as `dd/mm/yyyy`, in `--ink3`. A placeholder reading "Select a date" wastes the one chance to say which order the numbers go in.
- **The chevron rotates exactly like a select's**, per [[dropdown.component.md]]. Two dropdown-shaped controls side by side must move the same way; a still arrow next to a turning one makes them read as different kinds of control.
- It is a real `button` with `aria-haspopup="dialog"` and `aria-expanded`.

## The Panel

An overlay layer, following the overlay rules in [[uix.component.md]]: portalled to `body`, `position: fixed`, `--shadow-pop`, `--r`.

```css
.datepop {
  position: fixed; z-index: 80; padding: 12px;
  background: var(--surface);
  border: 1px solid var(--line); border-radius: var(--r);
  box-shadow: var(--shadow-pop);
}
.datepop-head { display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-bottom: 8px; }
.datepop-nav { padding: 5px; border: none; background: none; border-radius: 6px; color: var(--ink2); cursor: pointer; }
.datepop-nav:hover { background: var(--line2); color: var(--ink); }
.datepop-nav:disabled { opacity: .3; pointer-events: none; }
.datepop-title { font: inherit; font-weight: 600; color: var(--ink); border: none; background: none;
                 padding: 5px 9px; border-radius: var(--r-sm); cursor: pointer; }
.datepop-title:hover { background: var(--line2); }

.datepop-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; text-align: center; }
.datepop-grid.months, .datepop-grid.years { grid-template-columns: repeat(3, 1fr); gap: 4px; }
.datepop-dayname { font-size: .66rem; font-weight: 600; color: var(--ink3); padding: 4px 0; }
.datepop-cell { padding: 6px 0; border: none; background: none; border-radius: 6px;
                font: inherit; font-size: .8rem; color: var(--ink); cursor: pointer; }
.datepop-cell:hover { background: var(--line2); }
.datepop-cell[aria-selected="true"] { background: var(--accent); color: #fff; font-weight: 700; }
.datepop-cell:disabled { color: var(--ink3); pointer-events: none; }
```

The selected cell is the one place a solid `--accent` fill with white text appears inside a panel. The `6px` cell radius is the small nested radius; do not raise it to `--r`.

## Panel Width Matches the Trigger

**The panel is exactly as wide as its trigger.** Not a fixed width, not a clamped approximation, and never a width chosen to suit the seven columns inside it.

The calendar then reads as the trigger opening downward into a taller version of itself, with both edges lined up at every viewport size. A panel narrower than its trigger looks detached from the control that opened it; a wider one overhangs the field and lines up with nothing.

```js
const r = trigger.getBoundingClientRect();
const w = Math.round(Math.min(r.width, window.innerWidth - 16));
const left = Math.max(8, Math.min(r.left, window.innerWidth - w - 8));
```

- Measure on open, and **re-measure on resize** while open, so the panel tracks the trigger as the form reflows.
- No minimum and no maximum on the panel. The floor comes from the trigger: give form controls a sensible `min-width` and the panel can never be too narrow.
- The viewport is the only cap. A trigger wider than the screen gets a panel capped to the viewport minus an `8px` edge margin, shifted inward.
- **No CSS change is needed to support this.** The grid is `repeat(7, 1fr)` and `repeat(3, 1fr)`, so cells divide whatever width they are given. Never set a fixed cell width or add a media query to the panel.

On mobile a form field is full width, so the calendar is full width and its day cells get *larger*. That is the behaviour this rule exists for.

## Positioning

1. **Anchor to the input box, not to the field wrapper.** The wrapper also holds the label above and the hint below, so anchoring to it leaves the panel visibly detached from the control.
2. Keep the panel inside the viewport horizontally, with an `8px` edge margin.
3. Open downward when there is enough room below, roughly `280px`. Otherwise flip upward.
4. **When flipping upward, pin the panel's bottom edge, not its top.** The three views have different heights; pinning the bottom keeps the distance to the field constant without the code having to guess a height in advance.
5. Compute the position in the open handler, not in an effect, so the panel never paints once in the wrong place.
6. Recompute position and width on scroll (capture phase, so a scrolling ancestor is caught) and on resize, while open.

## Three Views

The header title is a button that cycles: day to month, month to year, year back to day.

| View | Grid | Title shows | Arrows move by |
| :- | :- | :- | :- |
| Day | 7 columns | `March 2026` | One month |
| Month | 3 columns | `2026` | One year |
| Year | 3 columns, scrolling | `2018 - 2038` | One block of years |

- Picking a month returns to the day view. Picking a year returns to the month view. **The user is always walked back down to a day**, never left stranded in a year grid.
- The title carries an affordance icon so it reads as openable rather than as a label.
- Day names start on the week's first day **for the locale**, which is Sunday in some and Monday in others. `Intl.Locale.prototype.getWeekInfo` gives it; hardcoding Sunday is wrong half the world.

## Clamp the Year Range

Clamp both the year a user can navigate to and the year the component initialises from.

Two real failures make this necessary. Without a clamp, the year view's arrows page by a whole block with no floor, so a user reaches year 0 and then negative years, and such a date saves without anything rejecting it. Separately, a stored value with a broken year makes date parsing return `NaN`, and the panel then fails to render at all for the one record that most needs fixing.

- Pick a range the domain justifies. A birth date needs the past; a contract expiry needs the future. Do not default to "a few years around now" without checking.
- **Validate the incoming value before rendering.** If it does not parse, fall back to today so a bad record can still be opened and corrected.
- At the edge of the range, move the year only and leave the month alone rather than silently jumping.
- **Disable the arrow that has reached the edge**, at `0.3` opacity with pointer events off. A button that still looks clickable but changes nothing is worse than one that visibly cannot be used.

## Closing

- Clicking outside closes it. The check tests **both** the trigger and the portal, because the panel is not a DOM child of the trigger; a single `contains` test on the wrapper closes the panel the instant a date is clicked.
- `Escape` closes without selecting and returns focus to the trigger.
- Picking a day closes. Picking a month or a year does not; it advances to the next view.

## Accessibility

A custom date panel replaces a native control that was fully accessible. Everything it gave you has to be rebuilt, and this is the section most implementations skip.

- The trigger is a `button` with `aria-haspopup="dialog"` and `aria-expanded`.
- The panel is a `dialog`. The day grid is a `grid`, each day a `gridcell`, each carrying **its full date as an accessible name**. A bare number announces nothing useful.
- Keyboard map: arrows move by day, `PageUp`/`PageDown` by month, `Home`/`End` to the start and end of the week, `Enter` or `Space` to pick, `Escape` to close.
- The selected day carries `aria-selected`, and the focused day carries real focus. Never rely on the accent fill alone.
- Focus moves into the panel on open and back to the trigger on close, never left on a detached node.
- The trigger is at least 44px tall on a touch screen.
- A disabled date is `disabled` or `aria-disabled`, not merely greyed out.

## Do and Do Not

Do:

- Choose native or custom deliberately, using the table, and write down which.
- Hold and emit `yyyy-mm-dd`, and format for display through one shared formatter.
- Show the format in the placeholder.
- Set the panel to the trigger's measured width, and re-measure on resize.
- Let `1fr` columns divide whatever width the panel gets.
- Clamp the year range and validate the incoming value.
- Disable an arrow that has hit the edge.

Do not:

- Mix native and custom date fields in one project.
- Let a display-formatted string become the value.
- Parse a calendar date with `new Date("yyyy-mm-dd")` and expect the local day.
- Give the panel its own fixed, minimum, or maximum width.
- Set a fixed cell width, or add a media query to the panel.
- Guess the panel height when flipping upward; pin the bottom edge.
- Hardcode Sunday as the first day of the week.
- Ship a custom panel without the keyboard map and the ARIA structure.

## Related

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[refresh.component.md]]
