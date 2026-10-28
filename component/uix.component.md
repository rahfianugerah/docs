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
> HeroUI v3 renders every component. This file says how HeroUI is configured, in Google Sans, at 8px, in light and dark, and hands each component area to a companion. Read this one first.

## Core Requirement

This is the root of the component standard. It owns the **token contract** every component reads from, and it hands each component area to a companion file.

**HeroUI v3 renders every component**, per [[stacks.rules.md]]. This file and its companions say how HeroUI is configured and used: which component, which variant, which theme variable, and the rules HeroUI does not decide for you, such as one primary action per view or a table that pages instead of scrolling.

Where a companion shows CSS, it records the measurement the HeroUI theme or a `className` override must produce. **It is never a second, hand-built component beside the HeroUI one.**

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
| [[darkmode.component.md]] | Light and dark, both, always, and the one switch between them |
| [[card.component.md]] | The card: header, content, footer, and one level only |
| [[layout.component.md]] | The page shell, full width beside the rail |
| [[header.bar.component.md]] | The sticky bar above every page, and the slots it carries |
| [[header.page.component.md]] | The page heading: the `h1`, its description, and the page's actions |
| [[notification.component.md]] | The bell, its panel, and the toast |
| [[animation.component.md]] | What moves, for how long, and what reduced motion turns off |

Read this file first. Read a companion when the work touches the area it owns.

Every companion reads HeroUI's theme variables, through the names in "The Theme Contract" below, and none of them redefines one. A new color, radius, or shadow is added here first, then used there.

## HeroUI's Theme Is the Base

**The base is HeroUI's own light and dark themes, set in Google Sans, with every corner at 8px.** Every project starts there, and is already correct before it adds a single color of its own.

HeroUI ships a complete light theme and a complete dark theme, each with its canvas, surfaces, text, borders, one accent, and three status colors, all checked for contrast. A project adds its own palette by overriding HeroUI's variables, once per theme, per [[darkmode.component.md]].

The base changes exactly two things from HeroUI's defaults, and both are deliberate:

- **The font is Google Sans**, everywhere, per "Typography" below.
- **No corner exceeds 8px.** HeroUI's default radius is larger, and its field radius is 1.5 times the radius, so both are overridden, per "Shape and Elevation" below.

> [!warning]
> A checked base is not permission to skip contrast checks. Every variable a project overrides is checked again, in both themes, and a status color still needs a label beside it.

Minimalism here means the interface carries no mark that does not do work:

- **No decorative border.** A border separates two things, or it is removed.
- **No shadow beyond HeroUI's two.** A surface keeps HeroUI's faint surface shadow; an overlay keeps its overlay shadow. Never a heavier one, and never one invented per component.
- **No filled surface for emphasis.** Weight and spacing carry hierarchy before color does.
- **No icon without a label**, except where the icon is a universally understood control and carries an accessible name.
- **No second typeface**, and no more than four weights from the one you have.

Readability always wins over decoration. Where a project does add brand color, strong color belongs on fills, gradients, decorative shapes, and small paired status badges, never underneath body text.

## The Theme Contract

**A component never hardcodes a color, a radius, or a shadow.** It reads a HeroUI theme variable, and the project overrides that variable in one place.

The CSS entry is the whole setup. HeroUI needs no provider:

```css
/* src/index.css */
@import "tailwindcss";
@import "@heroui/styles";

@theme {
  --font-sans: "Google Sans", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --radius-xl: 0.5rem;
  --radius-2xl: 0.5rem;
  --radius-3xl: 0.5rem;
  --radius-4xl: 0.5rem;
}

/* Shape: the same in both themes */
:root {
  --radius: 0.5rem;
  --field-radius: 0.5rem;
  --gap: 8px;
}

/* Project names for HeroUI variables, so every companion reads one vocabulary */
:root {
  --font: var(--font-sans);
  --bg: var(--background);
  --ink: var(--foreground);
  --ink2: var(--muted);
  --ink3: var(--field-placeholder);
  --line: var(--border);
  --line2: var(--separator);
  --accent-soft: color-mix(in oklab, var(--accent) 15%, transparent);
  --accent-tua: color-mix(in oklab, var(--accent) 90%, var(--accent-foreground) 10%);
  --ok: var(--success);
  --warn: var(--warning);
  --bad: var(--danger);
  --info: var(--accent);
  --ok-soft: color-mix(in oklab, var(--success) 15%, transparent);
  --warn-soft: color-mix(in oklab, var(--warning) 15%, transparent);
  --bad-soft: color-mix(in oklab, var(--danger) 15%, transparent);
  --ok-tua: color-mix(in oklab, var(--success) 60%, var(--foreground));
  --warn-tua: color-mix(in oklab, var(--warning) 60%, var(--foreground));
  --bad-tua: color-mix(in oklab, var(--danger) 60%, var(--foreground));
  --r: var(--radius);
  --r-sm: var(--radius);
  --shadow: var(--surface-shadow);
  --shadow-pop: var(--overlay-shadow);
}
```

`--surface` and `--accent` need no alias: HeroUI already uses those names.

Rules:

1. **HeroUI's variables are the contract.** `--background`, `--foreground`, `--surface`, `--overlay`, `--muted`, `--accent`, `--success`, `--warning`, `--danger`, `--border`, `--separator`, `--focus`, and their `-foreground` pairs. A project changes a color by overriding one of them, per theme, never by restyling a component.
2. **The names in the second block never get a value of their own.** They exist so the CSS in every companion reads one vocabulary, and each one resolves through a HeroUI variable so it follows the active theme. Assign one a hex and it stops switching.
3. **`--field-radius` is overridden with `--radius`, always.** HeroUI derives it as 1.5 times the radius, so a project that sets only `--radius` ships every input, select, and search field at 12px. This is the regression to check for first.
4. **The Tailwind radius scale is capped at 8px** in `@theme`, so a `rounded-2xl` written in a hurry still lands on the same corner.
5. **`--accent` reaches 4.5:1 against `--surface` in both themes.** HeroUI's own accent does. An overridden one is checked twice.
6. **Status colors are reserved for state.** A series or a button never wears one because it looked better, and a status color is always paired with a label or an icon.
7. **One font family, set once**, as `--font-sans`. See "Typography" below.
8. **Two shadows, both HeroUI's.** `--surface-shadow` for a surface, `--overlay-shadow` for an overlay.
9. Add a new variable here first, then use it in a component. A component that invents its own value is how two projects drift apart.

## Color Rules

### The Color Pattern

Every hue in HeroUI, including the accent, follows the same pattern, which is what makes a palette swap mechanical instead of a redesign.

| Step | Variable | Role |
| :- | :- | :- |
| Base | `--x` | A solid fill, and text or an icon on `--surface` |
| Foreground | `--x-foreground` | Text on a solid `--x` fill |
| Soft | Derived by HeroUI, 15% of `--x` | A tinted background: an active row, a chip, a badge |
| Hover | Derived by HeroUI | Hover on a solid `--x` fill |

**A bright brand hex is a fill, not a value for text.** When a project brings a palette, each brand hue produces a step that reaches 4.5:1 on the surface, per theme, and that step becomes the base variable. The pure brand hex stays available for fills, gradients, and decorative shapes.

### Contrast Rules

Most of any bright palette is too light for text on a white background. This is a hard constraint, not a preference.

- Text meets **4.5:1** at normal size and **3:1** at large size.
- A bright hue is fill, gradient, and decoration only. Never text on white, and never a background behind dark body text without checking it.
- White text on a solid fill is allowed only when that fill itself reaches 4.5:1 against white.
- Do not use `--ink3` below 12px. It clears the floor at body size and stops clearing it as the text shrinks.
- **Never rely on color alone** to communicate a state. Pair it with a label, an icon, or a shape.

### Status Badges

**A status badge is a HeroUI `Chip`** with `variant="soft"` and the color for the state. Never a hardcoded color per page, and never a badge built by hand.

| State | `color` | Reads as |
| :- | :- | :- |
| Done | `success` | Active, approved, done |
| Attention | `warning` | Locked, pending, needs attention |
| Failed | `danger` | Voided, rejected, failed |
| Awaiting | `accent` | Requested, submitted, awaiting this user, informational |
| Neutral | `default` | Inactive, archived, not applicable |

- **Soft is the default.** HeroUI derives the tint and the text from the one color, in both themes.
- **Solid, `variant="primary"`, only where one status must win** against a column of soft badges. A table where every row is solid has no emphasis left to give.
- **One color means one state across the whole project.** `danger` is never also "urgent but fine".
- A dot is the same color vocabulary at 9px with no label, for a row whose status text already sits in the next column.

### Gradients

A project with a brand may use gradients built from its palette for a hero background, a decorative shape, a footer, empty-state art, or a login backdrop.

- **A gradient never sits directly behind small body text.** Put the text on a clean surface, or on a solid area of the gradient that has been contrast-checked.
- Keep gradients smooth. A hard color stop reads as banding in print and on a low-bit display.
- Where a gradient marks a specific feature, it marks only that feature. A gradient reserved for one thing and then used decoratively stops meaning anything.

### Dark Mode

**Both themes ship, always**, per [[darkmode.component.md]]. Every rule in this file holds in light and in dark, and every value a project overrides is checked in both. A screen that works in one theme only is unfinished.

## Typography

**One family, everywhere: Google Sans.** Headings, body text, UI labels, buttons, form controls, tables, numerals, and every other string a user reads.

Google Sans is drawn for interface text. It holds up at 12px in a dense table, and its letterforms stay open and distinct at small sizes. That is the whole requirement, and one family that meets it is better than two that split the job, because the second family is always the one somebody forgets to set.

Set it once, on `body`, and let everything inherit:

```css
body {
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
```

The shell carries `bg-background text-foreground`, so the canvas and the ink follow the theme, per [[darkmode.component.md]]. Tailwind's preflight already sets form controls to inherit the font; never remove the preflight.

The system stack behind Google Sans in `--font` is the fallback for the moment before the webfont loads, not an alternative. Never set it deliberately.

### Loading Google Sans

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

- **Load exactly the four weights and no others.** Every extra weight is a file the user downloads and never sees.
- Keep `display=swap`, so text renders in the fallback immediately rather than staying invisible while the webfont downloads.
- Keep both `preconnect` links. Without them the font request waits on a fresh connection to a second origin.
- **Set Tailwind's `--font-sans` to Google Sans in `@theme`**, as in "The Theme Contract" above. HeroUI's components, Tailwind's preflight, and every `font-sans` utility all resolve to it, so one line sets the family everywhere. A stack left at Tailwind's default renders HeroUI in the system font while `body` looks correct.
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
- **The gap between cards is always 8px.** It is the same value as the radius below, so a gap and a corner never have to be reconciled.
- Maximum content width is 1280px, centered, shared by the page and the primary navigation.
- Navigation depends on the surface. A public or marketing page uses a horizontal topbar. An internal console may use a sidebar when the section count makes a topbar impractical; the choice is consistent inside one project. Its collapsible groups follow [[dropdown.component.md]].
- Use a two-column grid for forms and detail views, and a four-column grid for stat cards. Both collapse to a single column below 900px.

## Shape and Elevation

### One Radius, 8px, Everywhere

**Every rounded corner is `8px`.** Since 27 September 2026 there is one radius, and `8px` is the maximum any corner takes.

HeroUI carries the radius in two variables, and both are set to the same value:

| Variable | Value | Reaches |
| :- | :- | :- |
| `--radius` | `0.5rem` | Every surface and overlay: a card, a modal, a drawer, a popover, a table container |
| `--field-radius` | `0.5rem` | Every field: an input, a select, a search field, a date field. HeroUI would otherwise derive it as 1.5 times `--radius` |

The project names `--r` and `--r-sm` both resolve to `--radius`, so a companion's CSS lands on the same corner.

- **Size does not change the value.** A full-width card, a stat tile, a modal, and every control inside them all carry `8px`.
- **Containment is carried by the border, the background, and the shadow, not by the curve.** A card and the button inside it share a corner, and the card still reads as the container through its hairline border, its surface color against the canvas, and its `--shadow` lift. **Do not bring back a larger radius to make a container stand out.**
- **HeroUI's `--radius` and `--field-radius` are both `0.5rem`**, and Tailwind's radius scale is capped at `0.5rem` from `xl` upward, per "The Theme Contract" above. A HeroUI component and a utility class then land on the same corner.
- **A mark is not a surface, and neither token reaches it.** A color swatch, a legend key, a chart bar, a progress segment, a status dot: anything under about `12px` whose job is to carry a color rather than to contain something. These take `2px` to `4px`, or a full circle.

Fixed values outside the tokens, used only where listed: a full pill (`999px`) for a tag, badge, chip, nav badge, header pill, or scrollbar thumb; `8px 8px 0 0` for a bottom sheet; and `50%` for an avatar, a round icon button, a dot, or a decorative circle. **A pill and a circle keep their shape; the 8px maximum does not reach them**, because neither is a corner radius on a rectangle. Do not introduce any other value.

> [!warning]
> A hard-coded pixel radius in a component stylesheet is a defect, even when it happens to equal a token. It is how a second and third curve arrive: each one looks locally reasonable and nothing compares them.

### A Card Does Not Hold a Card

**The default is one level of card.** A card holds content: a heading, text, a table, a chart, a stat, controls. It does not hold another card.

This follows from the single radius. There is no longer a second curve to say which box contains which, so two borders stacked inside each other read as a rendering fault rather than as a hierarchy. Two borders and two paddings spend a line and 16px of inset to communicate nothing.

What to build instead:

- **A group of things is a grid of cards laid on the page**, not cards inside a wrapper card. The page canvas is the container, and the 8px gap is what groups them.
- **A section inside a card is a heading and a divider**, not a nested surface. A card that needs three sections needs three headings, or it needs to be three cards.
- **A modal holds its content directly.** It is already a surface; putting cards inside it stacks two.
- **A page panel is a card.** Do not wrap a set of cards in a panel to title them; put the title above them on the page.

A genuinely recursive structure, such as a comment thread or a nested board, is the one case that cannot be flattened. Document it in the project README, per "Deviations", and separate the levels with indentation and the `--line2` rail rather than with a second border.

### A Box Inset Inside a Surface

An image, a media block, or a code block set a few pixels inside a card is not a card, so it is allowed. Its corner is read directly against the card's corner, and it does not repeat it. It subtracts the inset:

```text
inner radius = outer radius - inset
```

| Outer | Inset | Inner |
| -: | -: | -: |
| 8px | 2px | 6px |
| 8px | 4px | 4px |
| 8px | 8px | 0 |

- **A control standing in a surface's ordinary content padding keeps the `8px` of the tokens** and computes nothing. The formula is only for a box inset tightly enough that the two corners are seen together.
- A negative result means the inset is larger than the radius, and there the inner box is square rather than rounded by a leftover value.
- **A grid that fills its container to the edge is the one case with no inset to subtract.** There the cells at the container's corners take the container's radius minus its border width, so the two curves sit concentric; every other cell stays square. A month calendar is the worked example: only the two bottom cells are rounded, and only on their outward corners.

### A Mark Is Not a Surface

The scale does not reach a mark: a color swatch, a legend key, a chart bar, a progress segment, a status dot. Anything under about `12px` whose job is to carry a color rather than to contain something.

These take `2px` to `4px`, or a full circle. Applying `--r-sm` to a `10px` swatch turns it into a circle, which then reads as a status dot rather than a color key, so the scale would be actively misleading rather than merely oversized.

### Elevation

- **A card is a HeroUI `Card`, with HeroUI's faint surface shadow and nothing heavier**, per [[card.component.md]].
- **The overlay shadow belongs to overlays only:** a popover, a dropdown panel, a date panel, a modal, a drawer, a toast. HeroUI applies it; never add it to a surface.
- A pill shape marks a tag, badge, chip, or nav link. **Never apply it to a content container** such as a card, sheet, or table.

## Component Rules

These apply to every component, including the ones with no companion file.

- **Use the HeroUI component wherever one exists.** A button, a field, a select, a checkbox, a switch, tabs, a modal, a drawer, a popover, a tooltip, a toast, a table, a card, a skeleton, a spinner, pagination, breadcrumbs, an avatar, a chip: every one comes from `@heroui/react`. Rebuilding one by hand forks its keyboard handling, its focus management, and its accessibility, which is the work HeroUI exists to do.
- **Look up every prop through the HeroUI MCP server**, per [[stacks.rules.md]]. A remembered API is the one that changed in the last minor version.
- **Customize through a theme variable first, a `className` second**, and never by wrapping a HeroUI component in a second component that restyles it.
- **Where HeroUI has no component**, such as the sidebar rail, the header bar, or a chart, build it from HeroUI parts and theme variables, per its companion.
- **Controls in one row share one HeroUI `size`.** A button, an input, a select, and a date trigger side by side have the same height, with a minimum of 44px on a touch screen.
- **One primary action per view.** [[button.component.md]] owns HeroUI's seven variants and which one carries it.
- **Focus is HeroUI's.** Every interactive HeroUI component draws a visible focus ring from `--focus` for keyboard users only. **Never remove it**, never hide it with `outline: none`, and never replace it with a glow.
- **Placeholder text is not a label.** It disappears the moment the user types, which is exactly when they need to check what the field wanted.
- **A password field always carries a show and hide toggle.**
- **A clickable target is at least 44px tall on a touch screen.** This includes a nav row, a table row, and a dropdown option.
- **Every list or table that can be empty gets a shared empty state**: a muted icon, a muted message, and an optional action. A blank area reads as a broken page.
- **Every table pages rather than scrolls**, per [[pagination.component.md]]. It is a HeroUI `Table` inside a container that scrolls horizontally on overflow. No zebra striping.
- **Animate `transform` and `opacity` only.** Animating `width`, `height`, `top`, or `margin` forces layout on every frame.
- **Respect `prefers-reduced-motion`.** Slow or remove a decorative animation; keep an animation that carries information.

### Icon Set

**One icon set for the whole project, and Tabler is the default.** One set means the same action carries the same glyph everywhere, so someone who learns an icon on one screen reads it correctly on the next.

- **`@tabler/icons-react` in a HeroUI project**, imported per icon so the bundle carries only what is used. Do not also load the webfont.
- **A glyph a HeroUI component draws itself is part of that component**, not a second icon set: the select chevron, the search glass, the close mark, the checkbox tick. Leave them. Every icon the project adds is Tabler.
- **Do not mix two sets**, and do not add a second set for the few glyphs the first is missing. Pick the closest glyph in the set you have.
- Self-hosting is preferred for a project that must work offline or has a privacy requirement. Keep the same version across projects.
- **Size every icon 16 to 20px.** A button icon is `16px`, a nav icon is `18px`. A route-gate spinner is the one documented exception, at `28px`, per [[loading.component.md]].
- **Never an emoji as an icon**, and never an icon as the only carrier of meaning; pair it with a label.

## The HeroUI Component Map

Which HeroUI component each area rests on. The companion is the standard; HeroUI is the implementation. Exact props come from the HeroUI MCP server, per [[stacks.rules.md]].

| Area | Companion | Built on |
| :- | :- | :- |
| Buttons | [[button.component.md]] | `Button`, `ButtonGroup`, `CloseButton`, `ToggleButton` |
| Dropdowns | [[dropdown.component.md]] | `Select`, `Autocomplete` with `SearchField`, `ListBox`, `Dropdown` |
| Date fields | [[calendar.component.md]] | `DatePicker`, `DateRangePicker`, `Calendar`, `DateField` |
| Tables | [[table.component.md]] | `Table` |
| Pagination | [[pagination.component.md]] | `Pagination` |
| Cards | [[card.component.md]] | `Card` with `Card.Header`, `Card.Content`, `Card.Footer` |
| Search and filters | [[search.component.md]] | `SearchField`, `Autocomplete` |
| Loading | [[loading.component.md]] | `Spinner`, `ProgressBar`, `Button` with `isPending` |
| Skeletons | [[skeleton.component.md]] | `Skeleton` |
| Notifications | [[notification.component.md]] | `Toast`, `Badge`, `Popover` |
| Scrollbars | [[scrollbar.component.md]] | `ScrollShadow`, and HeroUI's `--scrollbar-*` variables |
| Login | [[login.component.md]] | `Card`, `Form`, `TextField`, `Button`, `Alert` |
| Header bar | [[header.bar.component.md]] | `Toolbar`, `Breadcrumbs`, `Avatar`, `Badge`, `Dropdown` |
| Page heading | [[header.page.component.md]] | Typography, and `Button` for the page's actions |
| Sidebar | [[sidebar.component.md]] | No HeroUI rail; built from `Link`, `Disclosure`, `Badge`, `Drawer` |
| Page shell | [[layout.component.md]] | No HeroUI shell; built from `Surface` and `Separator` |
| Dashboards | [[dashboard.component.md]] | Chart.js for charts; `Card` and `Meter` around them |
| Dark mode | [[darkmode.component.md]] | `useTheme` from `@heroui/react` |
| Motion | [[animation.component.md]] | HeroUI's built-in transitions, plus the shell's |
| Product name | [[title.header.component.md]] | Text, from one constant |
| Refresh | [[refresh.component.md]] | Behaviour only; no component |

**A HeroUI component with no companion is used as HeroUI ships it**, themed by the variables above: `Alert`, `AlertDialog`, `Accordion`, `Avatar`, `Checkbox`, `CheckboxGroup`, `Chip`, `ColorPicker`, `Drawer`, `InputOTP`, `Kbd`, `Meter`, `Modal`, `NumberField`, `Popover`, `ProgressCircle`, `RadioGroup`, `Separator`, `Slider`, `Switch`, `Tabs`, `TagGroup`, `TextArea`, `TimeField`, `Tooltip`. A companion is written only when a project needs a rule HeroUI does not decide.

## Overlay Layers

**Every overlay is a HeroUI overlay**: `Popover`, `Modal`, `Drawer`, `Tooltip`, `Toast`, or `AlertDialog`. HeroUI portals it out of any scrolling ancestor, positions it, keeps it on screen, traps focus where a modal must, and closes it on `Escape` and outside press. **Never hand-roll one**; every one of those behaviours is a bug waiting in a home-made version.

- It carries HeroUI's overlay surface and overlay shadow, and the one 8px radius.
- It closes on selection where selection ends the interaction, such as a menu or a select.
- A modal holds its content directly. It is already a surface, so it never holds a card, per [[card.component.md]].

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

- Use the HeroUI component wherever one exists, and look its props up through the MCP server.
- Override a HeroUI variable once per theme, and read it everywhere.
- Set both `--radius` and `--field-radius` to `0.5rem`.
- Derive a text color from a brand hue rather than using the bright hex, and keep the bright one for fills.
- Give every corner `8px` and every gap `8px`, and lay a group of cards on the page rather than inside a wrapper card.
- Set Google Sans once, as Tailwind's `--font-sans`.
- Load only the four weights, and keep `display=swap` with both `preconnect` links.
- Keep controls in a row the same height.
- Keep HeroUI's focus ring on every interactive element.
- Render every status badge as a HeroUI `Chip`, soft by default.
- Use a HeroUI overlay for every floating panel.
- Ship light and dark together, per [[darkmode.component.md]].
- Animate `transform` and `opacity`.
- Check contrast before putting any color near text.

Do not:

- Hand-build a control, a field, or an overlay that HeroUI already ships.
- Override a color on a bare `:root`, where it overrides both themes at once.
- Leave `--field-radius` at HeroUI's default of 1.5 times the radius.
- Hardcode a hex, a radius, or a shadow inside a component.
- Add a third ink, a second radius, or a second accent.
- Use a bright brand hex as text on white.
- Place small body text directly on a gradient.
- Add a shadow heavier than HeroUI's, or a border that separates nothing.
- Use `--accent` as text on `--accent-soft`.
- Introduce a second typeface, or request a weight the project has not loaded.
- Introduce an ad hoc font size, or use ALL CAPS as the emphasis mechanism.
- Put a card inside a card, or wrap a set of cards in a panel to title them.
- Apply a pill shape to a content container.
- Remove a focus ring, or rely on color alone for a state.
- Mix two icon sets, or use an emoji as an icon.
- Ship one theme, or a partial dark mode.

## Related Standards

The companion components are listed in "Core Requirement" above. These are the rules outside `component/` that this file answers to.

| Document | Owns | Read it for |
| :- | :- | :- |
| [[docs.rules.md]] | Documentation formatting and the tag axes | The Title Case rule this file applies to the interface, and the ban on a decorative divider |
| [[badge.rules.md]] | The badge row and how a product name is written | The same Title Case rule, applied to a README rather than a screen |
| [[analytics.rules.md]] | Which chart a shape of data earns | Why a chart's colors come from a validated palette rather than from this token block |
| [[pwa.rules.md]] | The manifest, the icons, and offline behavior | Where the logo and the product name go outside the app itself |
| [[codes.rules.md]] | How code is written | Why a component reads a token instead of hardcoding a value |
| [[stacks.rules.md]] | The approved stack | Which icon set, which font, and which charting library this system assumes |

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

- [[darkmode.component.md]]
- [[card.component.md]]
- [[button.component.md]]
- [[calendar.component.md]]
- [[dashboard.component.md]]
- [[dropdown.component.md]]
- [[header.page.component.md]]
- [[layout.component.md]]
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
