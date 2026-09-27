---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Page Header Standard

> [!important]
> Two different things are called a header. The bar above the content carries the hamburger, the page name, and the account chrome, and it never changes shape. The page heading inside the content carries the `h1`, the description, and the page's actions.

## Core Requirement

**A project using the shared shell renders one header bar, 60px tall and sticky, above the content.**

The bar is identical on every route. Only the page name text and which right-cluster slots are present ever differ. A bar that changes with the route stops being the one fixed landmark on the screen, which is the only job it has beyond saying where the user is.

This extends [[uix.component.md]] and defines no token of its own. Every colour, radius, and size named here is already in that file's `:root` block.

[[sidebar.component.md]] owns the rail to the left of this bar, and the two are measured together: the brand block is fixed at the same 60px, so the two bottom borders form one unbroken line across the top of the shell. **Changing the height of one without the other breaks that line.**

## The Header Is Not the Page Heading

Confusing the two is the most common way this standard gets broken.

| | The header bar, `.topbar` | The page heading, `.ph` |
| :- | :- | :- |
| Where | Above the content, sticky, one per project | Inside the content, at the top of the page body |
| Carries | Hamburger, page name, account chrome | The `h1`, its description, and the page's actions |
| Changes with the route | Only the page name text | Entirely |
| Owned by | This file | The page itself, styled by [[uix.component.md]] |

```css
.ph { display: flex; align-items: flex-start; justify-content: space-between;
  gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
.ph h1 { font-size: 21px; font-weight: 600; letter-spacing: -.02em; }
.ph p { color: var(--ink2); font-size: 13.5px; margin-top: 2px; }
```

- **The `h1` lives in `.ph`, never in the bar.** The bar carries a small breadcrumb label, not a page title. An `h1` in the bar leaves the page with two competing titles at two sizes, and it pushes the account chrome onto a second visual line at a narrow width.
- **A page action belongs in `.ph`, never in the bar.** A New, Export, or Filter button sits on the right of the page heading, where [[button.component.md]] puts the one primary action per view. In the bar it would change on every route, which is the one thing the bar must not do.
- **A page filter belongs in the page.** A chip showing the active project or the selected month goes above the content, not into the bar.
- The `h1` is the page name, never the product name, per [[title.header.component.md]]. The rail already says which product this is.

## Anatomy

The bar is a single flex row of exactly five slots, in this order:

1. The hamburger, rendered only below the drawer breakpoint.
2. The breadcrumb, naming the page.
3. A spacer, an empty `flex: 1` element.
4. The right cluster: at most one context picker, then the notification bell.
5. The account link, always last.

Nothing else goes in the bar. **No search box, no product switcher, no theme toggle, no language switcher, no help button, no environment label, and no logo.** The logo and the product name live in the sidebar brand block, per [[sidebar.component.md]], and repeating them here spends the bar's width saying what the rail already says. The environment chip is the sidebar's, per [[title.header.component.md]].

```css
.topbar { height: 60px; display: flex; align-items: center; gap: 14px;
  padding: 0 22px; background: var(--surface);
  border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 20; }
.spacer { flex: 1; }
```

**The order is fixed even when a slot is absent.** A project with no context picker renders the bell where the bell goes, not shifted left into the picker's place, because the account block sits at the same distance from the right edge in every project built on this shell.

## The Breadcrumb

The breadcrumb names the page the user is on, in one line, at 13px.

```css
.crumb { font-size: 13px; color: var(--ink2); font-weight: 500;
  min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.crumb b { color: var(--ink); font-weight: 600; }
```

- **The label comes from a route-to-label map, not from the URL.** Keep one object keyed by path and read through it. Deriving `Invoice Lines` from `/invoice-lines` by replacing dashes produces a label nobody wrote and nobody reviewed.
- **The label matches the sidebar row that leads to the page**, word for word. Two names for one destination make the user check whether they are in the same place.
- A detail page appends its parent with ` > `, as `Clients > Detail`. **Two levels, never three.**
- **The current page is the last segment and is the only bold one.** An ancestor stays in `--ink2`.
- **The product name is not part of the breadcrumb.** `Invoices`, never `Product > Invoices`. The rail already says which product this is, and [[title.header.component.md]] keeps the same rule for the browser tab.
- An unmapped route falls back to the product name rather than rendering an empty bar.
- **Never put a record's identifier in the label.** `Invoices > Detail`, not `Invoices > INV-2026-0912`, which is unbounded in length and truncates on a phone.
- The breadcrumb truncates with an ellipsis rather than wrapping, at every width. The bar is one row.

## The Right Cluster

There are exactly three slot types after the spacer, and no fourth. Each is present or absent per project; none may be reordered, and nothing else may be added.

| Slot | Present when | Order |
| :- | :- | :- |
| Context picker | The project scopes its whole view by one entity, period, or clock | First |
| Notification bell | The project has notifications | Second |
| Account | Always | Last |

### Context Picker

```css
.ent { display: flex; align-items: center; gap: 8px; border: 1px solid var(--line);
  border-radius: 999px; padding: 6px 12px; cursor: pointer; font-weight: 600;
  font-size: 13px; background: var(--surface); min-width: 0; }
.ent .chev { color: var(--ink3); font-size: 15px; }
.ent:hover { border-color: var(--accent); background: var(--accent-soft); }
```

- **At most one.** A second pill in the bar means one of the two is a page filter and belongs in the page.
- It is a pill, not a button and not a select. The radius is `999px`, so it stays fully round if the height ever changes. A pill is one of the fixed shapes in [[uix.component.md]] and is exempt from the `8px` maximum, because it is a shape rather than a corner radius.
- An interactive pill opens a panel governed by [[dropdown.component.md]] and carries the chevron.
- **A read-only pill sets `cursor: default`, carries no chevron, and keeps the same shape**, so the bar reads as one row of chrome rather than two kinds of thing. A server clock is the usual case.
- A read-only pill states its meaning in `title`. A clock that explains it is showing server time, and reports the device offset, is what makes a disagreement between the two diagnosable rather than confusing.
- **A pill reflecting live server state renders a distinct state while it is still resolving**, and switches its icon to a `--bad` variant on failure rather than silently showing a stale value.
- Numbers in the pill use `font-variant-numeric: tabular-nums`, so a ticking clock does not shift the row width every second.
- The pill truncates with an ellipsis rather than wrapping.

### Notification Bell

```css
.iconbtn { width: 38px; height: 38px; border-radius: var(--r-sm);
  border: 1px solid var(--line); background: var(--surface);
  display: grid; place-items: center; cursor: pointer;
  position: relative; color: var(--ink2); }
.iconbtn:hover { background: var(--line2); }
.iconbtn .dot { position: absolute; top: 8px; right: 9px; width: 7px; height: 7px;
  border-radius: 50%; background: var(--bad); border: 1.5px solid var(--surface); }
```

- **The marker is a dot, never a number.** This is the marker vocabulary [[sidebar.component.md]] defines: a 7px `--bad` circle, here with a `1.5px` border in `--surface` so it reads clearly against the icon underneath. **A count belongs on the sidebar row that leads to the thing being counted.**
- Render the dot only when the unread count is above zero. There is no empty-circle state.
- The panel it opens is a dropdown panel with a header and list rows, per [[dropdown.component.md]], showing at most three items and a link to the full page. **The bar is not where a notification list is read.**
- Give the button an accessible name that states the count, such as `Notifications, 3 unread`. [[uix.component.md]] forbids relying on colour alone, and a red circle says nothing to a screen reader.
- **The bell is the only icon button in the bar.** A second one starts a toolbar, which is what the page heading is for.

### Account

```css
.who { display: flex; align-items: center; gap: 9px; padding-left: 6px; }
.who .av { width: 34px; height: 34px; border-radius: 50%; background: var(--accent-tua);
  color: #fff; display: grid; place-items: center; font-weight: 600; font-size: 13px;
  flex-shrink: 0; }
.who .nm { font-size: 13px; font-weight: 600; line-height: 1.2; }
.who .rl { font-size: 11px; color: var(--ink3); }
```

- **The account block is a link to the account page, not a dropdown menu.** One click reaches the page, and sign-out lives in the sidebar footer where [[sidebar.component.md]] puts it.
- The avatar is the user's initials, at most two letters, uppercased, on `--accent-tua`. **Never load a photo here.**
- Two lines: the name in `--ink`, the role label beneath it in `--ink3`.
- **The role is a human label, not the stored value.** Map the stored key through a lookup, and fall back to the least privileged label rather than rendering a raw key.
- **Every field falls back rather than rendering empty.** A header that loses its avatar while the profile request is in flight makes the whole bar jump.
- The avatar here is `34px` while the sidebar footer avatar is `30px`. That difference is deliberate and both are fixed; do not unify them.

## Responsive

The bar uses the single 900px breakpoint from [[uix.component.md]] and adds none of its own.

```css
.menu-btn { display: none; width: 38px; height: 38px; border-radius: var(--r-sm);
  border: 1px solid var(--line); background: var(--surface); place-items: center;
  cursor: pointer; color: var(--ink2); }

@media (max-width: 900px) {
  .topbar { gap: 8px; padding: 0 14px; }
  .menu-btn { display: grid; }
  .who .nm, .who .rl { display: none; }
}
```

- **The account block keeps its avatar and drops only its two text lines.** It is not removed. The avatar is the affordance that says an account page exists, and hiding the whole block leaves a phone with no route to it.
- **The breadcrumb and the pill truncate rather than wrap, at every width**, which is why neither needs a second breakpoint. The bar is one row at every size.
- The 900px value matches the sidebar drawer breakpoint, because the hamburger only makes sense once the rail becomes a drawer. **Keep the two numbers equal**, and do not introduce a third.
- **Nothing in the bar is removed at any width.** Every slot either shrinks or drops a secondary line.

## Sizing Reference

Every value is read from here or from [[uix.component.md]]. Do not hardcode a right-hand value elsewhere.

| Element | Property | Value |
| :- | :- | :- |
| The bar | Height, background, border, position | `60px`, `var(--surface)`, `1px solid var(--line)` bottom, `sticky` `top: 0` `z-index: 20` |
| The bar | Gap, padding | `14px`, `0 22px`, and `8px`, `0 14px` below the breakpoint |
| Breadcrumb | Font, colour | `500` `13px` in `var(--ink2)`, current segment `600` in `var(--ink)` |
| Spacer | Flex | `1` |
| Context pill | Padding, radius, font | `6px 12px`, `999px`, `600` `13px` |
| Context pill chevron | Font size, colour | `15px`, `var(--ink3)` |
| Icon button | Size, radius, border | `38px`, `var(--r-sm)`, `1px solid var(--line)` |
| Icon button dot | Size, position, border | `7px` at `top: 8px` `right: 9px`, `1.5px solid var(--surface)` |
| Account | Gap, padding | `9px`, `padding-left: 6px` |
| Account avatar | Size, font | `34px`, `600` `13px` |
| Account name, role | Font | `600` `13px`, and `11px` in `var(--ink3)` |
| Hamburger | Size, radius | `38px`, `var(--r-sm)` |
| Breakpoint | Drawer | `900px` |

`z-index: 20` sits below the sidebar drawer at `60` and its backdrop at `55`, so an open drawer covers the bar rather than sliding under it. **Do not raise it.**

## Accessibility

- **The bar is a `header` element**, not a `div`.
- **The hamburger is a real `button`** with an `aria-label`, an `aria-expanded` reflecting the drawer state, and a focus ring. A `div` with an `onClick` is not reachable by keyboard.
- The bell and any interactive pill are buttons, with an accessible name stating what they carry, and `aria-expanded` while their panel is open.
- **Every marker has an accessible name saying what it counts.** A red circle alone communicates nothing without sight.
- The account link is reachable by keyboard and keeps its focus ring. Hiding its text below the breakpoint must not remove its accessible name.
- **A ticking clock is not announced on every tick.** Leave it out of any live region; a header that reads a new time to a screen reader every second is unusable.
- The bar is sticky, so it must never grow tall enough to eat a small screen. 60px is the height at every width.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Keep the bar one row, 60px, sticky, sharing its bottom border with the brand block | Let the bar wrap, grow past 60px, or drop a slot at a narrow width |
| Put the `h1`, its description, and the page's actions in the page heading | Put an `h1`, a page action, a page filter, or a status chip in the bar |
| Take the breadcrumb label from a route-to-label map | Build the breadcrumb by transforming the URL |
| Match the breadcrumb to the sidebar row word for word | Repeat the product name in the breadcrumb, or put a record identifier in it |
| Keep the slot order fixed even when a slot is absent | Shift the bell left into an absent picker's place |
| Show at most one context pill and exactly one icon button | Add a search box, a product switcher, a theme toggle, or the logo |
| Mark unread with the 7px `--bad` dot, and render nothing at zero | Render a count on the bell, or an empty dot at zero |
| Keep the account block a link to the account page | Turn it into a dropdown, or put sign-out in the bar |
| Render a human role label with a least-privileged fallback | Render a raw role key, or an empty line while the profile loads |
| Keep the avatar visible below the breakpoint | Remove the account block on a phone |
| Keep the bar below the drawer in the stacking order | Raise the bar's `z-index` above the drawer |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The palette, the `:root` tokens, typography, spacing, shape, and the single breakpoint | Every value this file names but does not define |
| [[sidebar.component.md]] | The navigation rail | The 60px brand block this bar lines up with, the drawer breakpoint, and the marker vocabulary |
| [[layout.component.md]] | The page shell | Where the bar sits in the grid, and why the content fills the width beneath it |
| [[dropdown.component.md]] | Every panel | The panel a context pill or the bell opens |
| [[button.component.md]] | The button variants | Why the page's one primary action sits in the page heading and not in the bar |
| [[title.header.component.md]] | The product name | Why the product name is not in the breadcrumb, and where the environment chip goes |
| [[login.component.md]] | The sign-in screen | The screen before the shell, and the identity the account block shows |

## Deviations

**A portal with no navigation rail is the one shape that does not converge.** It has no rail to carry the brand lockup and no route to name in a breadcrumb, so its bar is the only chrome it has and correctly holds the logo and the sign-out path that every other screen puts in the sidebar footer. It still takes its colours, radii, and type sizes from [[uix.component.md]]. A screen that grows a sidebar loses this exemption.

Any other intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

**Fix a drifted bar in one change, every slot at once.** A half-migrated bar is worse than a consistently wrong one, because the page then carries its title in two places.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. [[sidebar.component.md]], for anything the rail and the bar share
6. This page header standard
7. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements.

## Related

- [[uix.component.md]]
- [[sidebar.component.md]]
- [[layout.component.md]]
- [[dropdown.component.md]]
- [[button.component.md]]
- [[title.header.component.md]]
- [[login.component.md]]
