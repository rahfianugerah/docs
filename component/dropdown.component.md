> Up: [[README.md]] · [[uix.component.md]]

# Dropdown Standard

> [!note]
> Every dropdown: the sidebar list, the native select, and the shared themed listbox.

## Core Requirement

Every dropdown follows this policy. It covers two cases that look alike and are not the same thing:

| Case | What it is | Built from |
| :- | :- | :- |
| **Form dropdown** | Picks one value from a set of options | A native `select`, or a themed listbox |
| **Navigation group** | A collapsible group of links in a sidebar | A disclosure button and a nested list |

A navigation group is never a `select`, and a form dropdown is never a disclosure. Mixing them produces a control that announces the wrong thing to a screen reader.

This policy extends [[uix.component.md]] and reads every color, radius, and shadow from its token contract.

## Native Select Is the Default

**Start with `<select>`.** It ships keyboard navigation, screen reader support, form integration, and the platform's own picker on mobile, and it needs no JavaScript to work.

Style it with the same tokens as a text input, so a select looks identical to every other field:

```css
select {
  width: 100%;
  padding: 9px 12px;
  font: inherit;                    /* a select defaults to a browser font */
  color: var(--ink);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  outline: none;
}
select:hover { border-color: var(--accent); }
select:focus-visible { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
select:disabled { background: var(--line2); color: var(--ink3); cursor: default; }
```

`font: inherit` is the line people forget. Without it the select renders in the browser's UI font and sits visibly apart from the inputs beside it.

## When a Native Select Is Not Enough

A native `select` renders its **open option list** using the operating system's own control. CSS cannot reach inside it: no border, no radius, no hover color, no per-option icon, and the result differs across Windows, macOS, iOS, and Android.

Do not try to fix that. An `appearance: none` reset with a fake arrow styles the closed control, not the list. A vendor-prefixed pseudo-element does not reach the list either, and support diverges by platform. A browser sniff is not a design system.

Replace the native select with a **themed listbox** only when the open list itself must be styled:

- Options need their own hover and selected colors
- An option needs an icon, a description line, or a secondary value
- The list needs a search box or a trailing action such as "add new"
- Options are grouped with styled headers

**Plain is correct for most dropdowns.** Reaching for a custom listbox because the native one "looks basic" costs you every accessibility behaviour it gave you for free, and you have to rebuild all of it.

## The Themed Listbox

Build it once per project and reuse it. Never a second implementation.

Required structure and behaviour:

```html
<button class="selectbox" role="combobox"
        aria-expanded="false" aria-controls="opt-list" aria-haspopup="listbox">
  <span class="value">Choose one</span>
  <span class="chev" aria-hidden="true"></span>
</button>

<!-- portalled to <body>, position: fixed -->
<ul class="selectpop" id="opt-list" role="listbox">
  <li role="option" aria-selected="true">Option A</li>
  <li role="option" aria-selected="false">Option B</li>
</ul>
```

```css
.selectbox {
  display: flex; align-items: center; gap: 8px; width: 100%;
  min-height: 38px; padding: 9px 12px; box-sizing: border-box;
  font: inherit; color: var(--ink); background: var(--surface);
  border: 1px solid var(--line); border-radius: var(--r-sm);
  cursor: pointer; outline: none;
}
.selectbox:hover { border-color: var(--accent); }
.selectbox:focus-visible,
.selectbox[aria-expanded="true"] { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
.selectbox:disabled { background: var(--line2); color: var(--ink3); cursor: default; }

.selectpop {
  position: fixed; z-index: 80; overflow-y: auto; padding: 4px;
  background: var(--surface);
  border: 1px solid var(--line); border-radius: var(--r);
  box-shadow: var(--shadow-pop);
}
.selectpop li { padding: 9px 11px; border-radius: var(--r-sm); font-size: .875rem; color: var(--ink); cursor: pointer; }
.selectpop li.active { background: var(--line2); }                        /* keyboard cursor */
.selectpop li[aria-selected="true"] { color: var(--accent-tua); font-weight: 600; }
.selectpop li[aria-selected="true"].active { background: var(--accent-soft); }
```

Rules:

1. **The trigger is a real `button`.** A `div` with a click handler is not focusable, not operable by keyboard, and announces nothing.
2. **The panel is portalled**, `position: fixed`, per the overlay rules in [[uix.component.md]]. A dropdown inside a modal or a scrolling table is the normal case, not the edge case.
3. **The panel matches the trigger width.** Measure the trigger and set the panel to it, so the two line up on both edges.
4. **Full keyboard support**, and this is the part that is always half-finished:

| Key | Does |
| :- | :- |
| `Enter`, `Space`, `Alt+Down` | Open, and move the cursor to the selected option |
| `Up`, `Down` | Move the cursor, without selecting |
| `Home`, `End` | First and last option |
| Typing a letter | Jump to the next option starting with it |
| `Enter` | Select the cursor option and close |
| `Escape` | Close without selecting, and return focus to the trigger |
| `Tab` | Close and move on |

5. **The keyboard cursor is separate from hover.** `.active` follows the arrow keys; hover follows the mouse. One state for both makes the mouse steal the keyboard's place.
6. **Selection is announced by `aria-selected`, not by color alone.** Add a check icon or a weight change so it survives greyscale and colorblindness.
7. **Focus returns to the trigger on close.** Leaving focus on a removed node drops the user to the top of the page.

## Navigation Groups

A collapsible group in a sidebar: a parent row that expands to reveal nested links. It is navigation, not a form control.

```html
<button class="navparent" aria-expanded="false" aria-controls="grp-reports">
  <span class="icon" aria-hidden="true"></span>
  <span>Reports</span>
  <span class="chev" aria-hidden="true"></span>
</button>
<div class="subnav" id="grp-reports">
  <a href="/reports/daily">Daily</a>
  <a href="/reports/monthly">Monthly</a>
</div>
```

```css
.navparent {
  display: flex; align-items: center; gap: 11px; width: 100%;
  padding: 8px 10px; border: none; background: none;
  font: inherit; font-weight: 500; color: var(--ink2);
  border-radius: var(--r-sm); cursor: pointer; text-align: left;
}
.navparent .icon { color: var(--ink3); }
.navparent .chev { margin-left: auto; color: var(--ink3); }
.navparent:hover { background: var(--line2); color: var(--ink); }
.navparent[aria-expanded="true"] { color: var(--accent-tua); font-weight: 600; }
.navparent[aria-expanded="true"] .icon { color: var(--accent); }

.subnav { margin: 1px 0 4px 19px; padding-left: 14px; border-left: 1px solid var(--line2); }
.subnav a { display: block; padding: 7px 10px; font-size: .8rem; color: var(--ink2); }
.subnav a[aria-current="page"] { background: var(--accent-soft); color: var(--accent-tua); font-weight: 600; }
```

### The Icon Belongs to the Title Only

**The parent row carries an icon. The items inside it do not.**

- The parent row has exactly two icons: the group icon at the start, the chevron at the end. Nothing else.
- Every item inside the expanded list is **text only**. No leading icon, no bullet, no dot, no dash.
- A flat top-level link that is not a group keeps its own icon. The rule applies to nested items only.
- **Nesting is what marks a child as a child.** The indent and the rail on `.subnav` already say it; a per-item icon repeats that and competes with the group title for the eye.

Rules:

- The parent is a `button` with `aria-expanded` and `aria-controls`. Not an `a` with no `href`, which is neither a link nor a button.
- The current page carries `aria-current="page"`, not just a class.
- A group whose child is the current route opens by default, so a reload does not collapse the section being worked in.
- Two levels only: group and item. A third level means the grouping is wrong.
- The nested list is indented with a rail. **It never takes the overlay shadow**: it is inline navigation, not a floating panel.

## The Chevron

Every trigger that opens something carries a trailing chevron, and it **rotates 180 degrees** when open.

```css
.chev { transition: transform .16s ease; }
[aria-expanded="true"] .chev { transform: rotate(180deg); }
@media (prefers-reduced-motion: reduce) { .chev { transition: none; } }
```

- One down-pointing icon, rotated. **Never swap it for an up-pointing icon**: a swap loses the animation, and the two glyphs rarely land on the same pixels.
- One duration and one curve across the whole project, so two dropdowns opening side by side move together.
- Animate `transform` only.
- The chevron stays `--ink3` in every state. It marks *state*, not activity, so it never takes `--accent`.
- One attribute drives the border and the chevron together, so they cannot disagree about whether the panel is open.

The **one exception** is a navigation group whose collapsed arrow points *right* rather than down. A 180 degree turn cannot produce that, so it swaps `right` for `down`. Pick one convention per project and keep it.

## Reference Table

| Property | State | Value |
| :- | :- | :- |
| Font | All | `inherit` |
| Text | Default | `var(--ink)` |
| Text | Placeholder, disabled | `var(--ink3)` |
| Text | Selected option | `var(--accent-tua)` |
| Background | Trigger, panel | `var(--surface)` |
| Background | Hover, keyboard cursor | `var(--line2)` |
| Background | Selected option | `var(--accent-soft)` |
| Border | Default | `1px solid var(--line)` |
| Border | Hover, focus, open | `var(--accent)` |
| Radius | Trigger | `var(--r-sm)` |
| Radius | Panel | `var(--r)` |
| Focus ring | `:focus-visible` | `0 0 0 2px var(--accent-soft)` |
| Shadow | Open panel | `var(--shadow-pop)` |
| Shadow | Navigation group | None |
| Chevron | Any state | `var(--ink3)`, rotate 180 on open, `.16s ease` |

## Do and Do Not

Do:

- Start with a native `select` and only replace it when the open list must be styled.
- Set `font: inherit` on every native control.
- Build the themed listbox once, with the full ARIA structure and the full keyboard map.
- Keep the keyboard cursor separate from hover.
- Put the icon on a navigation group's title only, and keep its items text-only.
- Rotate one chevron rather than swapping two glyphs.

Do not:

- Build a custom listbox because the native one looks plain.
- Use a `div` as a trigger, or an `a` without `href` as a disclosure.
- Style a native select's open option list with an `appearance` hack.
- Position a panel with `position: absolute` inside a scrolling container.
- Put an icon or a bullet on an item inside a navigation group.
- Give a navigation group an overlay shadow, or a form dropdown panel none.
- Color the chevron with `--accent` when open.

## Related

- [[uix.component.md]]
- [[calendar.component.md]]
- [[refresh.component.md]]
