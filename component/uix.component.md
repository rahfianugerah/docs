---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]]

# UI Component Standard

> [!note]
> The palette, tokens, typography, spacing, shape, and elevation every other component reads from. Read this one first.

## Core Requirement

This is the root of the component standard. It owns the **token contract** every component reads from, and it hands each component area to a companion file.

It is deliberately framework-agnostic. The rules are about behaviour, semantics, and CSS, which are the same in React, Vue, Svelte, Angular, or plain HTML. Where markup is shown it is plain HTML; translating a `class` attribute to `className` is not a design decision.

| Companion | Owns |
| :- | :- |
| [[button.component.md]] | The six button variants, the icon before the label, and one primary action per view |
| [[dropdown.component.md]] | Selects, themed listboxes, and collapsible navigation groups |
| [[calendar.component.md]] | Date fields: the trigger, the panel, and the day, month, and year views |
| [[table.component.md]] | The table itself: wrapper, header, rows, cells, and the row actions |
| [[pagination.component.md]] | Paging rather than scroll, adaptive page size, controls, and the data binding |
| [[refresh.component.md]] | What survives a page reload, and the three things that break it |
| [[sidebar.component.md]] | The navigation rail, its grouping, and the mobile drawer |
| [[login.component.md]] | The sign-in screen |
| [[loading.component.md]] | The four loading surfaces |
| [[skeleton.component.md]] | The loading state a component shows in its own place, instead of holding the page |
| [[dashboard.component.md]] | Charts, and when something is not a chart |
| [[search.component.md]] | Filter against search, and how a query is matched |
| [[scrollbar.component.md]] | Where a scrollbar must be visible |
| [[title.header.component.md]] | The product name, in one form everywhere |

Read this file first. Read a companion when the work touches the area it owns.

Every companion reads its values from the `:root` block below and none of them redefines a token. Adding a companion does not move a value out of this file, so a new color, radius, or shadow is still added here first, then used there.

## Black on White Is the Base

**The base is black on white, in Inter, and every project starts there.**

Black text, black accent, white background. No brand color, no gradient, no colored surface. A project adds its own palette by overriding the tokens below, and until it does, it is already correct rather than unstyled.

This is a starting point, not a ban on color. It exists because a design system that ships with a palette gets copied palette and all, and three projects then wear a fourth project's brand for a year.

> [!warning]
> Black on white is the base, not permission to skip contrast checks. A gray you add for a placeholder still has to clear the floor, and a status color still needs a label beside it.

Minimalism here means the interface carries no mark that does not do work:

- **No decorative border.** A border separates two things, or it is removed.
- **No shadow except to lift an overlay off the page.** A card sits on a hairline border, not on a shadow.
- **No filled surface for emphasis.** Weight and spacing carry hierarchy before color does.
- **No icon without a label**, except where the icon is a universally understood control and carries an accessible name.
- **No second typeface**, and no more than four weights from the one you have.

Readability always wins over decoration. Where a project does add brand color, strong color belongs on fills, gradients, decorative shapes, and small paired status badges, never underneath body text.

## The Token Contract

**A component never hardcodes a color, a radius, or a shadow.** It reads a custom property, and the project defines that property once at `:root`.

This file does not pick your palette. It names the **roles** a component expects to find, so a component copied between two projects works in both, and it ships the neutral base as the default value of each role.

```css
:root {
  /* Type: one family, everywhere */
  --font: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;

  /* Surfaces */
  --surface: #ffffff;        /* a card, a panel, an input background */
  --bg: #ffffff;             /* the page behind the surfaces */

  /* Text, dark to light */
  --ink: #000000;            /* body text */
  --ink2: #4a4a4a;           /* secondary text, labels; 8.9:1 on white */
  --ink3: #767676;           /* placeholder, disabled, decorative icons; 4.5:1 on white */

  /* Lines */
  --line: #d4d4d4;           /* a border */
  --line2: #f0f0f0;          /* a hover fill, a divider, a rail */

  /* One accent, three steps. Black, because the base carries no brand */
  --accent: #000000;         /* the action color; must reach 4.5:1 on --surface */
  --accent-soft: #f0f0f0;    /* a tinted background */
  --accent-tua: #000000;     /* text on --accent-soft, hover on a solid --accent fill */

  /* Status. The only colors in the base, because state cannot be read from black alone */
  --ok: #1a7f37;   --ok-soft: #e8f5ee;   --ok-tua: #12784a;
  --warn: #9a6700; --warn-soft: #fbf3e6; --warn-tua: #8a5a10;
  --bad: #b42318;  --bad-soft: #fcecec;  --bad-tua: #96201a;
  --info: #1a1a1a; --info-soft: #f0f0f0; --info-tua: #000000;

  /* Shape: two values, and the gap that makes them concentric */
  --r: 16px;                 /* a surface that wraps other cards */
  --r-sm: 8px;               /* a leaf card, and every control */
  --gap: 8px;                /* the gap and the inset, everywhere */

  /* Elevation */
  --shadow: none;                            /* a card takes a border, not a shadow */
  --shadow-pop: 0 8px 30px rgb(0 0 0 / .16); /* overlays only */
}
```

Rules:

1. **Every value above is a role, not a preference.** Change the hex to suit the project; do not rename the property or add a fourth ink.
2. **`--accent` must reach 4.5:1 against `--surface`.** Black clears it by definition. A bright brand color usually does not; darken it for the token and keep the bright original for fills and decoration.
3. **Text on `--accent-soft` uses `--accent-tua`**, never `--accent`. The base on a tinted background often misses the contrast floor.
4. **Status colors are the only colors in the base**, and they are reserved for state. A series or a button never wears one because it looked better, and a status color is always paired with a label or an icon.
5. **One font family, set once.** See "Typography" below.
6. **Two radii, plus one gap.** See "Shape and Elevation" below.
7. **One elevation, for overlays only.** `--shadow-pop` belongs to a dropdown panel, a date panel, a modal, or a toast. In the base a card takes a border and no shadow at all.
8. Add a new token here first, then use it in a component. A component that invents its own value is how two projects drift apart.

## Color Rules

### The Three-Step Pattern

Every hue in the system, including the accent, carries the same three tokens. This is what makes a palette swap mechanical instead of a redesign.

| Step | Role | Contrast requirement |
| :- | :- | :- |
| Base, `--x` | Text and icons on `--surface`; a solid fill under white text | 4.5:1 on `--surface` |
| `--x-soft` | A tinted background: an active nav row, a chip, a badge, a hero icon | Carries no text of its own |
| `--x-tua` | Text on `--x-soft`; hover on a solid `--x` fill | 4.5:1 on `--x-soft` |

**A bright brand hex is a fill, not a value for text.** When a project brings a palette, each brand hue produces a darkened derivative that reaches 4.5:1 on white, and that derivative becomes the base token. The pure brand hex stays available for fills, gradients, and decorative shapes.

That single rule is what keeps a colorful brand accessible: the color a user sees on a fill is the bright one, and the color a user reads is its darkened sibling, and both come from the same hue so nobody perceives them as two colors.

### Contrast Rules

Most of any bright palette is too light for text on a white background. This is a hard constraint, not a preference.

- Text meets **4.5:1** at normal size and **3:1** at large size.
- A bright hue is fill, gradient, and decoration only. Never text on white, and never a background behind dark body text without checking it.
- White text on a solid fill is allowed only when that fill itself reaches 4.5:1 against white.
- Do not use `--ink3` below 12px. It clears the floor at body size and stops clearing it as the text shrinks.
- **Never rely on color alone** to communicate a state. Pair it with a label, an icon, or a shape.

### Status Badges

A status badge is one shared component plus one hue class. Never a hardcoded color per page.

| Hue | Class | Reads as |
| :- | :- | :- |
| Green | `.t-ok` | Active, approved, done |
| Amber | `.t-warn` | Locked, pending, needs attention |
| Red | `.t-bad` | Voided, rejected, failed |
| Blue or neutral | `.t-info` | Informational, in progress |
| Accent | `.t-acc` | Requested, submitted, awaiting this user |
| Muted | `.t-mut` | Inactive, archived, not applicable |

- **Soft is the default:** `--x-soft` background with `--x-tua` text.
- **Solid is `--x-tua` as the background** with white text, not the base color. White on a mid-tone green or amber typically lands between 3.5:1 and 4.1:1, under the 4.5:1 a small label needs; the `-tua` step carries every hue past it, so one rule holds with no exception.
- Soft text is `-tua` for the same reason: a base color on its own soft background often falls just short.
- Reach for solid only where one status must win against a column of soft badges. A table where every row is solid has no emphasis left to give.
- A `.dot` is the same hue vocabulary at 9px with no label, for a row whose status text already sits in the next column.

### Gradients

A project with a brand may use gradients built from its palette for a hero background, a decorative shape, a footer, empty-state art, or a login backdrop.

- **A gradient never sits directly behind small body text.** Put the text on a clean surface, or on a solid area of the gradient that has been contrast-checked.
- Keep gradients smooth. A hard color stop reads as banding in print and on a low-bit display.
- Where a gradient marks a specific feature, it marks only that feature. A gradient reserved for one thing and then used decoratively stops meaning anything.

### Dark Mode

Dark mode is not part of the base. Adding it is a deliberate project decision that redefines every token under a media query and a `[data-theme]` selector together, not a partial pass over a few surfaces. A half-converted dark mode is worse than none, because the unconverted half is unreadable rather than merely off-brand.

## Typography

**One family, everywhere: Inter.** Headings, body text, UI labels, buttons, form controls, tables, numerals, and every other string a user reads.

Inter is drawn for interface text. It holds up at 12px in a dense table, its digits line up, and its letterforms stay distinct at small sizes. That is the whole requirement, and one family that meets it is better than two that split the job, because the second family is always the one somebody forgets to set.

Set it once, on `body`, and let everything inherit:

```css
body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--ink);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

button, input, select, textarea { font-family: inherit }
```

The system stack behind Inter in `--font` is the fallback for the moment before the webfont loads, not an alternative. Never set it deliberately.

### Loading Inter

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

- **Load exactly the four weights and no others.** Every extra weight is a file the user downloads and never sees.
- Keep `display=swap`, so text renders in the fallback immediately rather than staying invisible while the webfont downloads.
- Keep both `preconnect` links. Without them the font request waits on a fresh connection to a second origin.
- **Set the utility framework's sans stack to Inter as well.** A framework's preflight applies its own stack to `html`, and every `sans` utility resolves to it, so a stack that still names something else sends any later use of that utility to the wrong family, silently, while `body` keeps the visible result correct.
- **Self-hosting is preferred** for a project that must work offline or that has a privacy requirement. Keep the same family and the same weights either way.
- Every component inherits the family. Do not re-declare a family on a component; a control that sets its own is how a button ends up on the browser default.

### Weight and Size Roles

Four weights, and they are the whole set.

| Weight | Used for |
| :- | :- |
| `400` | Body text and paragraphs |
| `500` | UI labels, nav rows, secondary lines, and table cells |
| `600` | Headings, buttons, field labels, table column headers, and the active nav row |
| `700` | A page title, a login heading, and a count badge |

The size scale is fixed, on the same 4px grid as spacing. Base is `14px`, set once on `body`.

| Size | Weight | Used for |
| :- | :- | :- |
| `24px` | `700` | Page title |
| `20px` | `600` | Section heading, modal title |
| `16px` | `600` | Card header, login heading |
| `14px` | `400` | Body text, table cell, input value |
| `14px` | `600` | Button label, field label, active nav row |
| `13px` | `500` | Secondary line, nav row, helper text |
| `12px` | `500` | Table column header, chip, meta line |
| `11.5px` | `600` | Status badge label |

- **Never a weight above `700`**, and never one the project has not loaded. A missing weight renders as a synthetic bold, which is heavier and blurrier than the real thing.
- **Never introduce an ad hoc size.** A size not on the scale is a decision nobody else can reproduce.
- **Money and any aligned numeric column use `tabular-nums`** and are right-aligned, so digits line up down the column.
- Create emphasis with size, weight, and color, in that order. Do not use an all-caps heading as the emphasis mechanism.

### Capitalization

Two cases only, chosen by what the text is, not by where it sits.

- **Title Case** for anything that names a thing: page titles, card headers, table column headers, form field labels, button labels, tab labels, chip labels, menu and nav items, status badges, and modal titles. Capitalize each word except a short joining word, unless one opens the string.
- **Sentence case** for anything that reads as prose: page descriptions, help text under a field, empty-state messages, toast and error messages, confirmation body text, tooltips, and table cell content. Capitalize the first letter only, plus proper nouns.

A proper noun, an acronym, and a product name keep their own casing in both modes. **Do not use ALL CAPS as an emphasis device.** Where a label is visually uppercased, do that in CSS with `text-transform` and keep the source string in Title Case, so it stays readable to a screen reader and in code.

## Layout and Spacing

- **Base spacing unit is 4px**, using the fixed scale: 4, 8, 12, 16, 24, 32, 40.
- **The gap between cards is always 8px**, and so is the inset of a card inside another card. That single value is what makes the radius scale below concentric without arithmetic.
- Maximum content width is 1280px, centered, shared by the page and the primary navigation.
- Navigation depends on the surface. A public or marketing page uses a horizontal topbar. An internal console may use a sidebar when the section count makes a topbar impractical; the choice is consistent inside one project. Its collapsible groups follow [[dropdown.component.md]].
- Use a two-column grid for forms and detail views, and a four-column grid for stat cards. Both collapse to a single column below 900px.

## Shape and Elevation

### The Radius Says What Contains What

**The scale is two values, and which one applies is decided by nesting, not by the kind of element.**

| Token | Value | Belongs to |
| :- | :- | :- |
| `--r-sm` | `8px` | **The leaf.** A card that contains no other card, however large. Every control: a button, an input, a select, a textarea, a nav row, a menu item, a calendar cell, a skeleton |
| `--r` | `16px` | **A surface that wraps other cards.** An outer card holding a grid of cards, a page panel containing sections, a modal that holds cards |

- **A single card on a page is a leaf, so it takes `8px`.** Size does not change this; a full-width card with nothing inside it is still a leaf.
- **When one card wraps others, the outer takes `16px` and the inner ones take `8px`.** That difference is what says which contains which, before anything else on the screen is read.
- **The gap and the inset are always `8px`**, which is exactly what makes the two values concentric: `16px` outer minus an `8px` inset is `8px`, so the nesting formula below resolves onto the scale with no arithmetic in the common case.
- **Deeper nesting is not designed for.** A third level would need `0` for the middle surface, which is the signal to flatten the layout rather than to invent a third radius.

Fixed values outside the scale, used only where listed: a full pill (`999px`) for a tag, badge, chip, nav badge, or scrollbar thumb; `16px 16px 0 0` for a bottom sheet; and `50%` for an avatar, a round icon button, or a decorative circle. Do not introduce a radius that is not on this list or produced by the nesting rule.

> [!warning]
> A hard-coded pixel radius in a component stylesheet is a defect, even when it happens to equal a token. It is how a third and fourth curve arrive: each one looks locally reasonable and nothing compares them.

### Nested Radius

A rounded box inside another rounded box does not repeat the outer radius. It subtracts the padding between them:

```text
inner radius = outer radius - padding
```

Two curves separated by a gap are only concentric when the inner one is tighter by exactly that gap. Give the inner box the same radius as the outer and its corner sits inside the outer curve with a widening sliver between them, which reads as a misprint rather than as a design.

| Outer | Padding | Inner |
| -: | -: | -: |
| 24px | 8px | 16px |
| 16px | 8px | 8px |
| 8px | 8px | 0 |

The scale is built so the formula usually resolves onto it. Reach for the arithmetic only when a surface deliberately departs from `16px`, or when the padding is not `8px`.

A grid that fills its container to the edge is the one case the formula does not cover, because there is no padding to subtract. There the cells at the container's corners take the container's radius minus its border width, so the two curves sit concentric; every other cell stays square. A month calendar is the worked example: only the two bottom cells are rounded, and only on their outward corners.

A negative result means the padding is larger than the outer radius, and there the inner box is square rather than rounded by a leftover value.

### A Mark Is Not a Surface

The scale does not reach a mark: a color swatch, a legend key, a chart bar, a progress segment, a status dot. Anything under about `12px` whose job is to carry a color rather than to contain something.

These take `2px` to `4px`, or a full circle. Applying `--r-sm` to a `10px` swatch turns it into a circle, which then reads as a status dot rather than a color key, so the scale would be actively misleading rather than merely oversized.

### Elevation

- **A card carries a hairline border and no shadow.** In a project that adds one, keep it faint enough to read as a hairline lift rather than a raised surface, two 1px layers at a few percent opacity.
- **A pronounced shadow belongs to overlay layers only:** a bottom sheet, a login card, a toast, a dropdown panel, a date panel, a modal.
- A pill shape marks a tag, badge, chip, or nav link. **Never apply it to a content container** such as a card, sheet, or table.

## Component Rules

These apply to every component, including the ones with no companion file.

- **Controls share one size.** A button, an input, a select, and a date trigger sitting in one row have the same height and the same padding. `9px 14px` at `--r-sm` is the default, with a minimum height of 44px on a touch screen.
- **`font-family: inherit` on every form control.** A `button`, `input`, `select`, and `textarea` each default to a browser font rather than the page font, and the mismatch is visible.
- **One primary action per view.** [[button.component.md]] owns the six variants and which one carries it.
- **A field's focus indicator is its border turning `--accent`.** No glow, no halo, no `box-shadow` ring. A soft ring reads as a shadow the field is casting, which is a depth cue reserved for overlays; on a flat form it makes one field look lifted off the page while its neighbours stay put, and the effect compounds when fields sit close together.
- **A non-text control keeps `outline: 2px solid var(--accent)` on `:focus-visible`.** An outline is a line, not a spread shadow, and it is what keeps keyboard focus visible where there is no border to recolor.
- **A focus ring is never removed.** Use `:focus-visible` so it appears for keyboard users without outlining every mouse click. Keep it at most 2px.
- **Placeholder text is not a label.** It disappears the moment the user types, which is exactly when they need to check what the field wanted.
- **A password field always carries a show and hide toggle.**
- **A clickable target is at least 44px tall on a touch screen.** This includes a nav row, a table row, and a dropdown option.
- **Every list or table that can be empty gets a shared empty state**: a muted icon, a muted message, and an optional action. A blank area reads as a broken page.
- **Every table pages rather than scrolls**, per [[pagination.component.md]], and is wrapped in a bordered container with horizontal scrolling on overflow. No zebra striping; row hover uses `--line2`.
- **Animate `transform` and `opacity` only.** Animating `width`, `height`, `top`, or `margin` forces layout on every frame.
- **Respect `prefers-reduced-motion`.** Slow or remove a decorative animation; keep an animation that carries information.

### Icon Set

**One icon set for the whole project, and Tabler is the default.** One set means the same action carries the same glyph everywhere, so someone who learns an icon on one screen reads it correctly on the next.

- The reference is the Tabler webfont, loaded once and used through an `<i class="ti ti-*">` element. The React package is an acceptable alternative where tree shaking is needed, as long as the glyph names match. Do not run both in one project.
- **Do not mix two sets**, and do not add a second set for the few glyphs the first is missing. Pick the closest glyph in the set you have.
- Self-hosting is preferred for a project that must work offline or has a privacy requirement. Keep the same version across projects.
- **Size every icon 16 to 20px.** A button icon is `16px`, a nav icon is `18px`. A route-gate spinner is the one documented exception, at `28px`, per [[loading.component.md]].
- **Never an emoji as an icon**, and never an icon as the only carrier of meaning; pair it with a label.

## What the Companions Own

Each of these is a summary. The companion file is the standard.

**Buttons**, per [[button.component.md]]: six variants and no seventh, exactly one primary action per view, the icon before the label with the gap the class already defines, and a danger variant reserved for an action that destroys or revokes.

**Dropdowns**, per [[dropdown.component.md]]: a form dropdown starts as a native `select` styled like every other control and moves to the shared themed listbox only when the open option list itself needs styling. Never a third implementation. A sidebar dropdown is a collapsible navigation group, not a form control: the icon belongs to the title row, and the items inside are text only, marked as children by the indent and the rail. A dropdown panel is an overlay and carries the pronounced shadow; a sidebar group is inline navigation and carries none.

**Tables**, per [[table.component.md]]: one wrapper, one header treatment, one row height, and row actions in a fixed position. A money column is right-aligned with tabular numerals.

**Pagination**, per [[pagination.component.md]]: every table pages rather than scrolls, the page size adapts to the viewport, and the controls and the data binding are shared rather than rebuilt per screen.

**The product name**, per [[title.header.component.md]]: one canonical spelling, from one constant, imported everywhere it is shown. Never read from an environment variable. The interface name never changes with the route.

**The sidebar**, per [[sidebar.component.md]]: three parts and nothing else, a brand block, a scrolling nav, and a pinned account footer. Features grouped into collapsible dropdowns rather than listed flat. Exactly two notification markers, a count badge on a leaf row and a dot on a closed group title, neither ever rendered at zero. A menu the user has no permission for is not rendered at all. Below the breakpoint the rail becomes a drawer with a real backdrop, animated with `transform`.

**Refresh and state**, per [[refresh.component.md]]: a refresh returns the user to exactly the page they were on, with the same tab, filters, search, sort, and pagination. The URL is the state. The route stays behind the loading gate until the session check settles, so a signed-in user is never shown the login form on refresh. The static frontend serves `index.html` on every path, so a deep link does not 404 when reloaded.

**Dashboards and charts**, per [[dashboard.component.md]] and [[analytics.rules.md]]: one charting library wrapped in one shared component. Pick the form before the color; a single number is a stat tile, not a one-bar chart. Series colors come from the validated palette, assigned in fixed order and never cycled. Never a dual axis. Every chart with two or more series carries a legend, and every chart has a table view of the same data.

**Scrollbars**, per [[scrollbar.component.md]]: one shared scrollbar, a full pill thumb, no arrow buttons, a transparent track. It sits inside the component that scrolls, within its border and radius. The horizontal scrollbar under a wide table is always visible; it is the only cue that more columns exist.

**Date fields**, per [[calendar.component.md]]: the panel is rendered through a portal with `position: fixed`, for the same reason a select panel is. The component holds and emits one machine format and shows the user the project's display format through one shared formatter. The navigable year range is clamped, and the starting value is validated, so an impossible date can be neither reached nor rendered.

**Search and filters**, per [[search.component.md]]: a filter is an exact predicate and a search is a ranked guess. Fuzzy matching applies only to free text a human wrote, never to an identifier, an amount, a date, or an enum. A text search runs as a ladder that stops at the first stage that answers. Filtering, sorting, and pagination happen in the database, never in the client after fetching. When results came from the fuzzy stage, the UI says so, because the rows do not contain the word the user typed.

**Loading states**, per [[loading.component.md]] and [[skeleton.component.md]]: every loading state pairs an indicator with visible text naming what is being waited on. A bare spinner announces nothing to a screen reader. One indicator per wait. The spinner is the loading glyph from the project's one icon set, colored `--accent`, at one shared speed. A loader never carries a semantic hue, because a wait is not a success, a warning, or an error. Use a skeleton when the layout is already known and a spinner when it is not, so the page does not jump when data lands.

**The login screen**, per [[login.component.md]]: one centered card, capped in width, carrying the surface radius and the overlay shadow. The order is fixed and nothing is added to it. The session is an `HttpOnly` cookie, so no token is written to JavaScript or browser storage, per [[auth.rules.md]]. A sign-in block for an identity provider is hidden in full when none is configured; never render a dead button.

## Overlay Layers

A floating panel is an overlay, and every overlay in a project behaves the same way.

- Render it through a **portal to `document.body`** with `position: fixed`. An absolutely positioned panel cannot escape an ancestor with `overflow: auto`, so it gets clipped or it pushes the container taller.
- Give it `--shadow-pop`, a `1px solid var(--line)` border, and the radius its nesting earns: `--r-sm` for a panel holding controls or menu items, `--r` only for an overlay that wraps cards, such as a modal holding a card grid.
- Close it on outside click, on `Escape`, and on selection where selection ends the interaction.
- The outside-click check must test **both** the trigger and the portal, because the panel is not a DOM descendant of the trigger.
- Position it in the open handler, not in an effect, so it never paints once in the wrong place.
- Recompute the position on scroll (with the capture phase, so a scrolling ancestor is caught) and on resize, for as long as it is open.

Every companion that opens a panel inherits these rules rather than restating them.

## Accessibility

- Text meets 4.5:1 at normal size and 3:1 at large size. The contrast rules above exist to enforce this.
- **Never leave an interactive element without a visible focus indicator.** On a text field that is the border turning `--accent`; everywhere else it is `outline: 2px solid var(--accent)` on `:focus-visible`. Removing one without putting the other in its place makes the element unreachable by keyboard in practice.
- Do not use the muted ink below 12px.
- A clickable button, nav link, or table row is at least 44px tall on a touch screen.
- **Never rely on color alone** to communicate a state; pair it with a label or an icon.
- Every page has exactly one `h1`, and headings descend without skipping a level.
- An icon that is the only content of a control carries an accessible name.

## Public and Marketing Pages

These apply to a public-facing page such as a landing page, in addition to every rule above.

- A hero may carry a bold decorative shape or gradient in the background. Hero text sits on a clean or contrast-checked area, never on the busiest part of it.
- The footer may repeat the brand motif at low contrast.
- Keep the page responsive to the same 900px breakpoint the internal screens use.

## Responsive

- **A single breakpoint at 900px:** mobile below it, desktop at or above. Do not add another without a real, documented need.
- Below 900px, a multi-column grid collapses to one column, navigation collapses into a drawer, and a table scrolls horizontally inside its wrapper instead of being cut off.
- A decorative shape or gradient scales down or is hidden on mobile rather than pushing content or forcing horizontal scroll.

## Do and Do Not

Do:

- Define every token once at `:root` and read it everywhere.
- Derive a text color from a brand hue rather than using the bright hex, and keep the bright one for fills.
- Give a leaf card `8px`, a card that wraps cards `16px`, and every gap `8px`.
- Set Inter once on `body`, and set the utility framework's sans stack to Inter as well.
- Load only the four weights, and keep `display=swap` with both `preconnect` links.
- Keep controls in a row the same height.
- Use `:focus-visible` for the focus ring, and the border for a text field.
- Render status badges through one shared component and the hue table.
- Portal every floating panel and give it the overlay shadow.
- Animate `transform` and `opacity`.
- Check contrast before putting any color near text.

Do not:

- Hardcode a hex, a radius, or a shadow inside a component.
- Add a third ink, a third radius, or a second accent.
- Use a bright brand hex as text on white.
- Place small body text directly on a gradient.
- Put a shadow on a card, or a border that separates nothing.
- Use `--accent` as text on `--accent-soft`.
- Introduce a second typeface, or request a weight the project has not loaded.
- Introduce an ad hoc font size, or use ALL CAPS as the emphasis mechanism.
- Apply a pill shape to a content container.
- Position a floating panel with `position: absolute` inside a scrolling container.
- Remove a focus ring, or rely on color alone for a state.
- Mix two icon sets, or use an emoji as an icon.
- Add a partial dark mode.

## Deviations

Any intentional deviation from this system is documented in the project's README, together with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements, specifically the contrast minimums above
3. Direct user instructions
4. This component standard
5. The companion standards, for the detail this file delegates to them
6. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Related

- [[button.component.md]]
- [[calendar.component.md]]
- [[dashboard.component.md]]
- [[dropdown.component.md]]
- [[loading.component.md]]
- [[login.component.md]]
- [[pagination.component.md]]
- [[refresh.component.md]]
- [[scrollbar.component.md]]
- [[search.component.md]]
- [[sidebar.component.md]]
- [[skeleton.component.md]]
- [[table.component.md]]
- [[title.header.component.md]]
- [[analytics.rules.md]]
- [[callout.rules.md]]
- [[codes.rules.md]]
- [[docs.rules.md]]
