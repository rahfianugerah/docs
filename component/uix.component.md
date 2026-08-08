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

Read this file first. Read a companion when the work touches the area it owns.

## The Token Contract

**A component never hardcodes a color, a radius, or a shadow.** It reads a custom property, and the project defines that property once at `:root`.

This file does not pick your palette. It names the **roles** a component expects to find, so a component copied between two projects works in both.

```css
:root {
  /* Surfaces */
  --surface: #ffffff;        /* a card, a panel, an input background */
  --bg: #f5f6f8;             /* the page behind the surfaces */

  /* Text, dark to light */
  --ink: #1a1d29;            /* body text */
  --ink2: #6b7280;           /* secondary text, labels */
  --ink3: #9aa1ad;           /* placeholder, disabled, decorative icons */

  /* Lines */
  --line: #e6e8ec;           /* a border */
  --line2: #eef0f3;          /* a hover fill, a divider, a rail */

  /* One accent, three steps */
  --accent: #1273ae;         /* the action color; must reach 4.5:1 on --surface */
  --accent-soft: #e7f3fb;    /* a tinted background */
  --accent-tua: #0e5883;     /* text on --accent-soft, hover on a solid --accent fill */

  /* Shape */
  --r: 10px;                 /* containers: cards, panels */
  --r-sm: 7px;               /* controls: buttons, inputs, selects */

  /* Elevation */
  --shadow: 0 1px 2px rgb(16 24 40 / .04), 0 1px 3px rgb(16 24 40 / .06);
  --shadow-pop: 0 8px 30px rgb(16 24 40 / .14);
}
```

Rules:

1. **Every value above is a role, not a preference.** Change the hex to suit the project; do not rename the property or add a fourth ink.
2. **`--accent` must reach 4.5:1 against `--surface`.** A bright brand color usually does not; darken it for the token and keep the bright original for fills and decoration.
3. **Text on `--accent-soft` uses `--accent-tua`**, never `--accent`. The base on a tinted background often misses the contrast floor.
4. **Two radii, not five.** `--r` for containers, `--r-sm` for controls. A full pill (`999px`) is allowed on a badge, a chip, or a scrollbar thumb; `50%` on an avatar or a round icon button. Nothing else.
5. **Two elevations.** `--shadow` is a hairline lift for a card. `--shadow-pop` belongs to overlay layers only: a dropdown panel, a date panel, a modal, a toast. A card never takes the overlay shadow.
6. Add a new token here first, then use it in a component. A component that invents its own value is how two projects drift apart.

## Shared Component Rules

These apply to every component, including the ones with no companion file.

- **Controls share one size.** A button, an input, a select, and a date trigger sitting in one row must have the same height and the same padding. `9px 12px` at `--r-sm` is a sane default.
- **`font-family: inherit` on every form control.** A `button`, `input`, `select`, and `textarea` each default to a browser font rather than the page font, and the mismatch is visible.
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
- Use `--accent` as text on `--accent-soft`.
- Position a floating panel with `position: absolute` inside a scrolling container.
- Remove a focus ring, or rely on color alone for a state.

## Related

- [[dropdown.component.md]]
- [[calendar.component.md]]
- [[refresh.component.md]]
- [[docs.rules.md]]
- [[codes.rules.md]]
