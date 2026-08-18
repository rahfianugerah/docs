> Up: [[README.md]]

# UI Component Standard

## Core Requirement

This is the root of the component standard. It owns the **token contract** every component reads from, and it hands each component area to a companion file.

It is deliberately framework-agnostic. The rules are about behaviour, semantics, and CSS, which are the same in React, Vue, Svelte, Angular, or plain HTML. Where markup is shown it is plain HTML; translating a `class` attribute to `className` is not a design decision.

| Companion | Owns |
| :- | :- |
| [[dropdown.component.md]] | Selects, themed listboxes, and collapsible navigation groups |
| [[calendar.component.md]] | Date fields: the trigger, the panel, and the day, month, and year views |
| [[refresh.component.md]] | What survives a page reload, and the three things that break it |
| [[sidebar.component.md]] | The navigation rail, its grouping, and the mobile drawer |
| [[login.component.md]] | The sign-in screen |
| [[loading.component.md]] | The four loading surfaces |
| [[dashboard.component.md]] | Charts, and when something is not a chart |
| [[search.component.md]] | Filter against search, and how a query is matched |
| [[scrollbar.component.md]] | Where a scrollbar must be visible |
| [[title.header.component.md]] | The product name, in one form everywhere |

Read this file first. Read a companion when the work touches the area it owns.

## Black on White Is the Base

**The base is black on white, in the system font, and every project starts there.**

Black text, black accent, white background. No brand color, no custom typeface, no gradient, no colored surface. A project adds its own palette by overriding the tokens below, and until it does, it is already correct rather than unstyled.

This is a starting point, not a ban on color. It exists because a design system that ships with a palette gets copied palette and all, and three projects then wear a fourth project's brand for a year.

> [!warning]
> Black on white is the base, not permission to skip contrast checks. A gray you add for a placeholder still has to clear the floor, and a status color still needs a label beside it.

Minimalism here means the interface carries no mark that does not do work:

- **No decorative border.** A border separates two things, or it is removed.
- **No shadow except to lift an overlay off the page.** A card sits on a hairline border, not on a shadow.
- **No filled surface for emphasis.** Weight and spacing carry hierarchy before color does.
- **No icon without a label**, except where the icon is a universally understood control and carries an accessible name.
- **No second typeface**, and no more than three weights from the one you have.

## The Token Contract

**A component never hardcodes a color, a radius, or a shadow.** It reads a custom property, and the project defines that property once at `:root`.

This file does not pick your palette. It names the **roles** a component expects to find, so a component copied between two projects works in both, and it ships the neutral base as the default value of each role.

```css
:root {
  /* Type: the system stack, so no font is downloaded and nothing shifts on load */
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
  --ok: #1a7f37;
  --warn: #9a6700;
  --bad: #b42318;
  --info: #1a1a1a;

  /* Shape */
  --r: 10px;                 /* containers: cards, panels */
  --r-sm: 7px;               /* controls: buttons, inputs, selects */

  /* Elevation */
  --shadow: none;                            /* a card takes a border, not a shadow */
  --shadow-pop: 0 8px 30px rgb(0 0 0 / .16); /* overlays only */
}
```

Rules:

1. **Every value above is a role, not a preference.** Change the hex to suit the project; do not rename the property or add a fourth ink.
2. **`--accent` must reach 4.5:1 against `--surface`.** Black clears it by definition. A bright brand color usually does not; darken it for the token and keep the bright original for fills and decoration.
3. **Text on `--accent-soft` uses `--accent-tua`**, never `--accent`. The base on a tinted background often misses the contrast floor.
4. **Status colors are the only exception to black on white**, and they are reserved for state. A series or a button never wears one because it looked better, and a status color is always paired with a label or an icon.
5. **The font stack is the system stack.** A downloaded typeface costs a request, a layout shift, and a fallback nobody tested. Add one only when the project genuinely needs it, and then set the same stack as its fallback.
6. **Two radii, not five.** `--r` for containers, `--r-sm` for controls. A full pill (`999px`) is allowed on a badge, a chip, or a scrollbar thumb; `50%` on an avatar or a round icon button. Nothing else.
7. **One elevation, for overlays only.** `--shadow-pop` belongs to a dropdown panel, a date panel, a modal, or a toast. In the base a card takes a border and no shadow at all.
8. Add a new token here first, then use it in a component. A component that invents its own value is how two projects drift apart.

## Shared Component Rules

These apply to every component, including the ones with no companion file.

- **Controls share one size.** A button, an input, a select, and a date trigger sitting in one row must have the same height and the same padding. `9px 12px` at `--r-sm` is a sane default.
- **`font-family: inherit` on every form control**, so every control reads `--font` from the page. A `button`, `input`, `select`, and `textarea` each default to a browser font rather than the page font, and the mismatch is visible.
- **Placeholder text is not a label.** It disappears the moment the user types, which is exactly when they need to check what the field wanted.
- **One icon set per project**, sized 16 to 20px, applied consistently. Never an emoji as an icon.
- **A focus ring is never removed.** Use `:focus-visible` so it appears for keyboard users without outlining every mouse click. Keep it thin, at most 2px.
- **A clickable target is at least 44px tall on a touch screen.** This includes a nav row, a table row, and a dropdown option.
- **Never rely on color alone** to communicate a state. Pair it with a label, an icon, or a shape.
- **Every list that can be empty gets an empty state.** A blank area reads as a broken page.
- **Animate `transform` and `opacity` only.** Animating `width`, `height`, `top`, or `margin` forces layout on every frame.
- **Respect `prefers-reduced-motion`.** Slow or remove a decorative animation; keep an animation that carries information.

## Overlay Layers

A floating panel is an overlay, and every overlay in a project behaves the same way.

- Render it through a **portal to `document.body`** with `position: fixed`. An absolutely positioned panel cannot escape an ancestor with `overflow: auto`, so it gets clipped or it pushes the container taller.
- Give it `--shadow-pop`, `--r`, and a `1px solid var(--line)` border.
- Close it on outside click, on `Escape`, and on selection where selection ends the interaction.
- The outside-click check must test **both** the trigger and the portal, because the panel is not a DOM descendant of the trigger.
- Position it in the open handler, not in an effect, so it never paints once in the wrong place.
- Recompute the position on scroll (with the capture phase, so a scrolling ancestor is caught) and on resize, for as long as it is open.

Every companion file that opens a panel inherits these rules rather than restating them.

## Do and Do Not

Do:

- Define every token once at `:root` and read it everywhere.
- Keep controls in a row the same height.
- Use `:focus-visible` for the focus ring.
- Portal every floating panel and give it the overlay shadow.
- Animate `transform` and `opacity`.

Do not:

- Hardcode a hex, a radius, or a shadow inside a component.
- Add a third ink, a fourth radius, or a second accent.
- Ship a brand color or a downloaded typeface in the base.
- Put a shadow on a card, or a border that separates nothing.
- Use `--accent` as text on `--accent-soft`.
- Position a floating panel with `position: absolute` inside a scrolling container.
- Remove a focus ring, or rely on color alone for a state.

## Related

- [[dropdown.component.md]]
- [[calendar.component.md]]
- [[refresh.component.md]]
- [[sidebar.component.md]]
- [[callout.rules.md]]
- [[docs.rules.md]]
- [[codes.rules.md]]
