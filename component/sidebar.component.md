---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Sidebar Standard

> [!note]
> The whole rail: the brand block, the grouped navigation, the two notification markers, the account footer, and the mobile drawer.

## Core Requirement

Every project whose navigation uses a sidebar follows this standard. A sidebar is the one surface a user sees on every screen, so it is the same on every screen and in every project that shares this system.

This standard extends [[uix.component.md]]. It does not redefine the token set; every color, radius, and size used here is already defined in that file's `:root` block.

[[dropdown.component.md]] owns the collapsible group itself, including the icon placement rule and the chevron. This file owns everything around it. Read both when working on a sidebar.

## Anatomy

The sidebar is a column of exactly three parts, in this order:

1. `div.brand`, fixed at the same 60px height as the topbar so the two bottom borders line up.
2. `nav.nav`, which scrolls and takes the remaining height.
3. `div.navfoot`, pinned at the bottom, holding the account link and the sign-out link.

**Nothing else goes in the rail.** No search box, no app switcher, no promotional block, no collapse-to-icons toggle.

## Navigation Rows

There are exactly three kinds of row, and no fourth.

| Row | Class | Carries |
| :- | :- | :- |
| Flat link | `.nav a` | An icon, a label, and an optional count badge |
| Group title | `.nav .navparent` | An icon, a label, an optional pip, and a chevron |
| Group child | `.nav .subnav a` | A label and an optional count badge, and no icon |

The icon placement rule is fixed by [[dropdown.component.md]]: **the icon belongs to the group title**, and a child inside `.subnav` is text only, because the indent and the `--line2` rail already mark it as a child.

## Grouping

**A feature list in the sidebar is a dropdown group.** A flat list of every page is not acceptable once the project has more than a handful, because the rail becomes a wall of equally weighted links that has to be read top to bottom every time.

- Group related features under one collapsible title.
- A top-level destination that belongs to no group stays a flat link. A dashboard is the usual one.
- **Do not nest a group inside a group.** The sidebar is two levels: title and child. A third level means the grouping is wrong, not that the sidebar needs another level.
- **A group title is a label, never a destination.** Clicking it opens or closes the group and navigates nowhere.
- **Keep a group open when one of its children is the current route**, so a reload does not collapse the section the user is working in.
- Order groups by how often they are used, not alphabetically.

## Link States

A nav link has three states, and each one is carried by **both the icon and the label together**. A state that colors only the label leaves the icon reading as inactive next to text that says otherwise, and the row reads as half-lit.

| State | Background | Icon and label |
| :- | :- | :- |
| Rest | none | Label `--ink2`, icon `--ink3` |
| Hover | none | Both `--accent` |
| Active | `--accent-soft` | Label `--accent-tua`, icon `--accent` |

```css
.nav a:hover { color: var(--accent); }
.nav a:hover i { color: var(--accent); }
.nav .navparent:hover { color: var(--accent); }
.nav .navparent:hover i { color: var(--accent); }
```

- **Hover moves the icon as well as the label.** The second rule in each pair is not optional: `.nav a i` sets its own color, so it does not inherit the hover color from the row and stays grey without it.

> [!warning]
> **Hover paints no background.** Only the label and the icon change color. The filled block is reserved for the active row, so at any moment exactly one row in the rail carries a background, and it is always the page the user is on. A rail where the hovered row and the current row are both filled makes the user check the shade to find out where they are.

- Hover uses `--accent` while active uses `--accent-tua`. That difference carries the whole distinction on its own, which is why the two must not be collapsed into one token.
- A group title behaves exactly as a flat link on hover, chevron included. The chevron is excluded only in the open state, where it would compete with the title's own emphasis.

> [!note]
> The rail is one column, with groups that expand in place. A two-column layout, where a narrow icon strip sits beside a second panel of links, is not part of this standard. Two levels of navigation chrome make the user read two things to find one.

## Notification Markers

The sidebar carries exactly two markers. Both are `--bad`, and there is no third form.

| Marker | Class | Sits on | Shows |
| :- | :- | :- | :- |
| Count badge | `.badge` | A flat link or a group child | A number, capped at `99+` |
| Pip | `.pip` | A group title, only while the group is closed | Nothing, it is a 7px circle |

```css
.nav a .badge {
  margin-left: auto; background: var(--bad); color: #fff;
  font-size: 10px; font-weight: 700; min-width: 18px; height: 18px;
  border-radius: 999px; display: grid; place-items: center; padding: 0 5px;
}
.nav .navparent .pip {
  margin-left: auto; width: 7px; height: 7px; border-radius: 50%;
  background: var(--bad); flex: none;
}
.nav .navparent .pip + i.chev { margin-left: 8px; }
```

- **Never render a badge at zero.** A zero badge is noise: it pulls the eye toward the one menu that needs nothing. The component returns nothing rather than rendering an empty circle.
- **Cap the number at `99+`**, so a large count cannot widen the badge and push the label out of the row.
- **The badge is a pill, not a fixed circle.** `min-width: 18px` with `height: 18px` and `border-radius: 999px` makes a one-digit count a circle and lets a three-character `99+` grow sideways without changing height. The radius is written as `999px` rather than as half the height, so the shape stays fully round if the height ever changes; `9px` only looked round because it happened to match this one height.
- **The pip appears on a group title only while that group is closed**, and only when its children have a non-zero total. Once the group is open the numbers are visible on the children themselves, so the pip would repeat what the user can already see.
- The marker on a group title is a pip rather than a number on purpose. [[dropdown.component.md]] fixes the title row at exactly two icons, the title icon and the chevron, so the marker here is kept as small as it can be: it says "there is something inside", and the number follows on the child.
- `margin-left: auto` sits on the pip, and the chevron takes a fixed `8px`. **Two automatic margins would split the free space between them** and leave the pip floating in the middle of the row.
- **Give every marker an accessible name stating what it counts**, such as "3 awaiting action". [[uix.component.md]] forbids relying on color alone, and a bare red circle says nothing to a screen reader.

A topbar notification button uses the same 7px marker with a `1.5px` border in `--surface` so it reads clearly against the icon underneath. Keep the two consistent; this is one marker vocabulary across the project, not two.

### Where the Counts Come From

- **Fetch every count in one request** for the whole sidebar, returning an object keyed by menu key. Never fetch a count per menu; a sidebar with ten badges must not make ten requests on every page load.
- **A group's pip is the sum of its children's counts, computed in the component.** Do not ask the backend for a separate group total.
- **A count is a number of things waiting for the signed-in user to act**, not a number of records that exist. `12` next to a menu means twelve items awaiting this user, not twelve rows in the table.
- **Treat a missing key as zero**, so a backend that has not shipped a counter yet renders nothing rather than `undefined`.

## Section Labels

`.nav .grp` renders a small uppercase label above a run of rows, for a project with enough groups that they need dividing further.

```css
.nav .grp { font-size: 10.5px; font-weight: 600; color: var(--ink3);
  text-transform: uppercase; letter-spacing: .06em; padding: 10px 10px 4px; }
```

The label is **uppercased in CSS and kept in Title Case in the source**, per the capitalization rule in [[uix.component.md]], so a screen reader and the code both read it normally.

## Row Density

The rail is compact. A nav row takes `5px` of vertical padding, a subnav row `4px`, and a section label `10px` above and `4px` below. Horizontal padding stays at `10px` throughout, so an icon never sits against the rail edge.

**Density is the point, not an accident of the numbers.** The sidebar is chrome, not content: every pixel it spends on air is a pixel the page beneath it does not get, and the spacing above a section label repeats for every group and so accumulates down the whole rail.

The one exception is touch. Below the breakpoint every nav row returns to a `44px` minimum height, the same floor [[uix.component.md]] sets for any clickable row, because a 30px target is comfortable for a cursor and not for a thumb.

```css
@media (max-width: 900px) {
  .nav a, .nav .navparent, .nav .subnav a { min-height: 44px; }
}
```

**Accessibility outranks density.** Never remove that media query to make the mobile rail shorter.

## Permission Filtering

The sidebar shows only what the signed-in user may open. **This is presentation, not a control**; the server still enforces the permission, per [[security.rules.md]].

- Give every destination a stable key, and match it against the menu list the backend returns.
- **A destination the user has no right to is never rendered.** Do not render it disabled, and do not render it and fail on click.
- **A group whose children are all filtered out disappears entirely.** It must never render as a dropdown that opens onto nothing.
- **Recompute the visible rows from the permission list** rather than hardcoding a per-role sidebar, so a permission change takes effect without a frontend release.

## Account Footer

`.navfoot` is pinned below the scrolling nav and holds two rows: the account link with a small avatar, and the sign-out link in `--bad`.

```css
.navfoot { padding: 8px 10px; border-top: 1px solid var(--line2); }
.navfoot-a { display: flex; align-items: center; gap: 10px; padding: 8px 10px;
  border-radius: var(--r-sm); cursor: pointer; }
.navfoot-a:hover { background: var(--line2); }
.navfoot-a.active { background: var(--accent-soft); }
.navfoot-a .av-sm { width: 30px; height: 30px; border-radius: 50%;
  background: var(--accent-tua); color: #fff; display: grid; place-items: center;
  font-weight: 600; font-size: 12px; flex-shrink: 0; }
.navfoot-a .t { font-size: 13px; font-weight: 600; line-height: 1.2; }
.navfoot-a .d { font-size: 11px; color: var(--ink3); }
```

- **The avatar is the user's initials, at most two letters**, on `--accent-tua`. Never load a photo here.
- The footer shows the name and the identity key the project signs in with, per [[login.component.md]].
- **Sign-out is the only red text in the rail.** It is a text link in `--bad`, not a danger button.

## Mobile Drawer

Below the breakpoint the rail becomes a drawer over the content.

```css
.app { display: grid; grid-template-columns: 236px 1fr; min-height: 100vh; }
.sidebar-backdrop { display: none; }
.menu-btn { display: none; width: 38px; height: 38px; border-radius: var(--r-sm);
  border: 1px solid var(--line); background: var(--surface); place-items: center;
  cursor: pointer; color: var(--ink2); }

@media (max-width: 900px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { position: fixed; left: 0; top: 0; z-index: 60; width: 236px;
    transform: translateX(-100%); transition: transform .24s cubic-bezier(.4,0,.2,1); }
  .sidebar.open { transform: translateX(0); box-shadow: var(--shadow-pop); }
  .sidebar-backdrop { display: block; position: fixed; inset: 0; z-index: 55;
    background: rgba(16,20,30,.42); opacity: 0; pointer-events: none;
    transition: opacity .24s ease; }
  .sidebar-backdrop.on { opacity: 1; pointer-events: auto; }
  .menu-btn { display: grid; }
}
```

- **Animate `transform`, never `left`.** A transform does not trigger layout on every frame.
- **The drawer closes when a link inside it is clicked, when the backdrop is clicked, and whenever the route changes.** All three, not one of them.
- Scroll the content back to the top on a route change, so a new page does not open halfway down.
- **The backdrop is a real element with a fade**, not a `body` class. It must be clickable to close.
- The hamburger lives in the topbar and appears only below the breakpoint.

The drawer uses the single 900px breakpoint from [[uix.component.md]]. A project that inherits a different value from an older stylesheet reconciles the two rather than carrying both.

## Sizing Reference

| Element | Property | Value |
| :- | :- | :- |
| `.app` | Grid | `236px 1fr` |
| `.sidebar` | Position, height, border | `sticky`, `100vh`, `1px solid var(--line)` on the right |
| `.brand` | Height, padding, gap | `60px`, `0 18px`, `10px` |
| `.brand .logo-img` | Size, radius | `30px` by `30px`, `var(--r-sm)` |
| `.brand .nm` | Font | `600`, `14px`, letter spacing `-.01em` |
| `.brand .sub` | Font, color | `500`, `11px`, `var(--ink3)` |
| `.nav` | Padding | `10px 10px`, scrollbar hidden |
| `.nav a`, `.navparent` | Padding, gap, font, radius | `5px 10px`, `11px`, `500` `13.5px`, `var(--r-sm)` |
| `.nav a i`, `.navparent i` | Font size, color | `18px`, `var(--ink3)` |
| `.navparent i.chev` | Font size | `15px` |
| `.subnav` | Margin, padding, rail | `1px 0 4px 19px`, `padding-left: 14px`, `1px solid var(--line2)` |
| `.subnav a` | Padding, font, gap | `4px 10px`, `12.7px`, `8px` |
| `.badge` | Size, radius, font | `min-width: 18px`, `height: 18px`, `999px`, `700` `10px` |
| `.pip` | Size, radius | `7px` by `7px`, `50%` |
| `.grp` | Font, padding | `600` `10.5px` uppercase, `10px 10px 4px` |
| `.navfoot .av-sm` | Size, font | `30px` by `30px`, `600` `12px` |
| Drawer | Width, breakpoint, transition | `236px`, `900px`, `transform .24s` |

## Accessibility

- **The rail is a `nav` element**, and the current page's link carries `aria-current="page"` in addition to the active style.
- **A group title is reachable and operable by keyboard.** A real `button` element is preferred, since it gets focus, Enter, and Space for free. Where an anchor is used instead, it needs `role="button"`, a tab index, `aria-expanded`, and a key handler for Enter and Space.
- Every marker has an accessible name saying what it counts. A red circle alone communicates nothing without sight.
- A nav row is at least 44px tall on mobile.
- **When the drawer opens, move focus into it**, and return focus to the hamburger when it closes. Escape closes it.
- Never remove the focus ring from a nav row or the hamburger.

## Do and Do Not

Do:

- Group features into collapsible dropdowns, with the icon on the group title and text-only children.
- Show a count badge on a leaf row and a pip on a closed group title, both in `--bad`.
- Hide a badge entirely at zero, and cap it at `99+`.
- Fetch every count in one request keyed by menu key.
- Remove a group whose children are all filtered out by permission.
- Close the drawer on link click, backdrop click, and route change.
- Keep the mobile 44px row height, whatever it costs in density.

Do not:

- Render a flat list of every page once the project has enough pages to group.
- Nest a group inside a group, or make a group title navigate somewhere.
- Render a zero badge, an empty circle, or a badge whose number can widen the row.
- Put a number on a group title, or leave the pip showing once the group is open.
- Add a third marker style, a second marker color, or an animated marker.
- Add a search box, an app switcher, or a collapse-to-icons toggle to the rail.
- Render a menu the user has no permission for, disabled or otherwise.
- Paint a hover background on a nav row.
- Animate the drawer with `left`, or use a `body` class instead of a real backdrop.

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. [[dropdown.component.md]], for the collapsible group itself
6. This sidebar standard
7. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements.

## Related

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[loading.component.md]]
- [[login.component.md]]
- [[title.header.component.md]]
- [[scrollbar.component.md]]
- [[security.rules.md]]
