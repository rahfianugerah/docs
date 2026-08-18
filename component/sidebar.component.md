> Up: [[README.md]] · [[uix.component.md]]

# Sidebar Standard

## Core Requirement

Every project whose navigation uses a sidebar follows this file. It covers the whole rail: the brand block, the navigation list, the grouping of features into collapsible dropdowns, the notification markers, the account footer, and the mobile drawer.

This extends [[uix.component.md]] and does not redefine the token set. Every color, radius, and size named here is a token already defined there.

A project adopts the sidebar by copying this structure. It does not rebuild an equivalent, and it does not restyle the rail to suit its own modules. **A sidebar is the one surface a user sees on every screen**, so it is the same on every screen.

[[dropdown.component.md]] owns the collapsible group itself, including the icon placement rule and the chevron. This file owns everything around it.

## Anatomy

The sidebar is a column of exactly three parts, in this order:

1. A brand block, fixed at the same height as the topbar so the two bottom borders line up.
2. A nav region, which scrolls and takes the remaining height.
3. A footer, pinned at the bottom, holding the account link and sign out.

Nothing else goes in the rail. No search box, no app switcher, no promotional block, no collapse-to-icons toggle.

## Navigation Rows

There are exactly three kinds of row, and no fourth.

| Row | Carries |
| :- | :- |
| Flat link | An icon, a label, and an optional count badge |
| Group title | An icon, a label, an optional dot, and a chevron |
| Group child | A label and an optional count badge, and no icon |

The icon placement rule is fixed by [[dropdown.component.md]]: the icon belongs to the group title, and a child is text only, because the indent and the rail already mark it as a child.

## Grouping

**A feature list in the sidebar is a dropdown group.** A flat list of every page is not acceptable once there are more than a handful, because the rail becomes a wall of equally weighted links that has to be read top to bottom every time.

- Group related features under one collapsible title.
- A top level destination belonging to no group stays a flat link. The dashboard is the usual one.
- **Do not nest a group inside a group.** The sidebar is two levels: title and child. A third level means the grouping is wrong, not that the sidebar needs another level.
- A group title is a label, never a destination. Clicking it opens or closes the group and navigates nowhere.
- Keep a group open when one of its children is the current route, so a reload does not collapse the section the user is working in.
- Order groups by how often they are used, not alphabetically.

## Notification Markers

The sidebar carries exactly two markers, both in the token for a negative or urgent state, and there is no third form.

| Marker | Sits on | Shows |
| :- | :- | :- |
| Count badge | A flat link or a group child | A number, capped at `99+` |
| Dot | A group title, only while the group is closed | Nothing, it is a small circle |

- **Never render a badge at zero.** A zero badge is noise: it pulls the eye toward the one menu that needs nothing. The component returns nothing rather than rendering an empty circle.
- Cap the number at `99+`, so a large count cannot widen the badge and push the label out of the row.
- The badge is a pill, not a fixed circle. A minimum width equal to its height, with a radius of half that height, makes a one digit count a circle and lets `99+` grow sideways without changing height.
- The dot appears on a group title **only while that group is closed**, and only when its children have a non-zero total. Once the group is open the numbers are visible on the children, so the dot would repeat what the user can already see.
- The marker on a group title is a dot rather than a number on purpose. The title row is fixed at exactly two icons, so the marker says "there is something inside" and the number follows on the child.
- The automatic margin sits on the dot, and the chevron takes a fixed gap. Two automatic margins would split the free space and leave the dot floating in the middle of the row.
- **Give every marker an accessible name stating what it counts.** [[uix.component.md]] forbids relying on color alone, and a bare colored circle says nothing to a screen reader.

Keep the topbar's notification marker identical to the sidebar's dot. This is one marker vocabulary across the product, not two.

### Where the Counts Come From

- Fetch every count in **one request** for the whole sidebar, returning an object keyed by menu key. Never fetch a count per menu; a sidebar with ten badges must not make ten requests on every page load.
- A group's dot is the sum of its children's counts, computed in the component. Do not ask the backend for a separate group total.
- **A count is a number of things waiting for the signed-in user to act**, not a number of records that exist. Twelve next to a menu means twelve items awaiting this user, not twelve rows in a table.
- Treat a missing key as zero, so a backend that has not shipped a counter yet renders nothing rather than `undefined`.

## Section Labels

A small uppercase label above a run of rows, for a project with enough groups that they need dividing further.

The label is uppercased in CSS and kept in Title Case in the source, per the capitalization rule in [[uix.component.md]], so a screen reader and the code both read it normally.

## Permission Filtering

The sidebar shows only what the signed-in user may open. **This is presentation, not a control**; the server still enforces the permission, per [[security.rules.md]].

- Give every destination a stable key, and match it against the menu list the backend returns.
- A destination the user has no right to is never rendered. Do not render it disabled, and do not render it and fail on click.
- **A group whose children are all filtered out disappears entirely.** It must never render as a dropdown that opens onto nothing.
- Recompute the visible rows from the permission list rather than hardcoding a per-role sidebar, so a permission change takes effect without a frontend release.

## Account Footer

The footer is pinned below the scrolling nav and holds two rows: the account link with a small avatar, and sign out in the negative token.

- The footer never scrolls with the nav. Sign out is always reachable without scrolling.
- Sign out is the only destructive-looking row in the rail, so nothing else borrows that color.

## Mobile Drawer

Below the layout breakpoint the rail becomes a drawer over the content.

- The drawer opens from the same edge the rail occupies on a wide screen.
- An overlay sits behind the drawer and closes it on click.
- Closing happens on: the overlay, the close control, `Escape`, and a completed navigation. A drawer that stays open after navigating hides the page the user just asked for.
- Move focus into the drawer on open and return it to the trigger on close, per [[uix.component.md]].
- The drawer holds the same three parts in the same order. It is the same component at a different width, not a second navigation.

## Sizing

Take every value from the token set in [[uix.component.md]]. What matters here is the relationship, not the number:

- The brand block matches the topbar height exactly, so the borders align.
- The nav region takes the remaining height and is the only part that scrolls.
- A row is tall enough to be a comfortable touch target, and a group child is indented by one step with a rail marking the group.

## Accessibility

- The rail is a `nav` landmark with an accessible name.
- The current route is marked with `aria-current="page"`, not by color alone.
- A group title is a `button` with `aria-expanded`, and it is reachable and operable by keyboard.
- Every marker carries text naming what it counts.
- The drawer is a modal dialog on mobile: focus is trapped, and `Escape` closes it.

## Do and Do Not

Do:

- Group features, and keep the group open on the active route.
- Fetch every count in one request.
- Hide what the user cannot open, and hide an empty group with it.
- Pin the footer, so sign out never needs scrolling.

Do not:

- Nest a group inside a group.
- Render a badge at zero, or a number on a group title.
- Put a search box, an app switcher, or a collapse toggle in the rail.
- Rely on color alone to mark the current route or a notification.
- Rebuild the rail per project.

## Related

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[title.header.component.md]]
- [[refresh.component.md]]
- [[security.rules.md]]
