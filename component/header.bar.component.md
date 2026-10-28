---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Header Bar Standard

> [!important]
> The header bar is one 60px strip across the full width of the window, above the rail and the content. It carries the brand and the tools every page shares, and nothing that belongs to one page.

## Core Requirement

**A project using the shared shell renders one header bar**: a 60px sticky strip across the full width of the window, above both the sidebar rail and the content pane, per [[layout.component.md]].

**The bar is a utility strip and nothing else.** It carries the brand on the left and, on the right, the tools every page shares: a jump-to search, the theme control, and the notification bell. It looks the same on every page.

**When a feature is added, nothing is added to the bar.** No page title, no breadcrumb, no button for one page. A title in the bar changes with the route, competes with the page heading at a second size, and grows a little with every feature until the bar is a second navigation. Everything that names or acts on the current page belongs in the page heading, per [[header.page.component.md]].

## Built On HeroUI

HeroUI has no header bar, so it is built from HeroUI parts and theme variables:

| Slot | HeroUI component |
| :- | :- |
| Hamburger | `Button`, `isIconOnly`, `variant="ghost"` |
| Jump-to search trigger | `Button` styled as a field, with a `Kbd` hint |
| Jump-to palette | `Modal` holding an `Autocomplete`-style list, per [[dropdown.component.md]] |
| Theme control | `Button`, `isIconOnly`, opening a `Dropdown` |
| Bell | `Button`, `isIconOnly`, with a `Badge` dot, opening a `Popover` |

Exact props come from the HeroUI MCP server, per [[stacks.rules.md]].

## Anatomy

The bar is a single row of exactly six slots, in this order:

1. **The hamburger**, shown only below the drawer breakpoint.
2. **The brand**: the logo and the product name.
3. **A spacer** that takes the remaining width.
4. **The jump-to search.**
5. **The theme control.**
6. **The notification bell**, always last.

```tsx
<header className="sticky top-0 z-20 flex h-15 flex-none items-center gap-3 border-b border-border bg-background px-4">
  <Button isIconOnly variant="ghost" aria-label="Open menu" aria-expanded={open} className="md:hidden">
    <IconMenu2 size={20} />
  </Button>
  <Brand />
  <div className="flex-1" />
  <JumpTo />
  <ThemeControl />
  <Bell />
</header>
```

> [!warning]
> Nothing else goes in the bar. No page title, breadcrumb, or `h1`, no page action or page filter, no status chip, no account block, no language switcher, and no help button. The account lives in the rail footer, per [[sidebar.component.md]]. An action that belongs to one page goes in that page's heading.

**The order is fixed even when a slot has nothing to show.** A project with no notifications yet still renders the bell without a dot, so the bell sits at the same distance from the right edge on every page.

A project that scopes its whole view by one entity or one period may add **one context picker**, a HeroUI `Select`, between the spacer and the search. One, never two: a second picker in the bar is a page filter and belongs on the page.

## The Brand

The brand is the 30px logo and the product name. **It is the only place the brand is drawn inside the shell**; the rail does not repeat it.

- **The brand names the product, never the page.** It reads the product name from one constant and says the same thing on every route, per [[title.header.component.md]]. The name never comes from an environment variable.
- **The brand is a link to the default route**, with the product name as its accessible name.
- **The logo carries a dark variant** where the mark would vanish on a dark canvas, per [[darkmode.component.md]].
- **Outside production, a warning `Chip` beside the name reads the environment**, per [[title.header.component.md]]. Production carries no chip at all, so an absent chip means real data.
- Below the breakpoint the name is hidden and the logo stays.

## The Jump-To Search

Every bar carries a search trigger that looks like a field and opens a palette for jumping to any page by name. **Ctrl+K, and Cmd+K on a Mac, open it from anywhere.**

- **It is navigation, not a list search.** It finds pages the rail already offers, never a second inventory, so [[search.component.md]] does not govern it. A search over records belongs on the page that lists them.
- **The palette uses the same smart search as a dropdown**, per [[dropdown.component.md]]: case and accent insensitive, every word in any order, the obvious match first.
- **The trigger shows the shortcut** as a HeroUI `Kbd`, so the shortcut is discoverable without a help page.
- Below the breakpoint the trigger collapses to an icon-only button; the palette itself is unchanged.

## The Theme Control

Every bar carries the theme control, between the search and the bell. **It is the one place the theme is changed**, per [[darkmode.component.md]].

- **An icon-only `Button` that opens a `Dropdown` with three items: Light, Dark, and System.** The icon shows the theme in use: a sun, a moon, or a monitor for System.
- **The accessible name is `Theme`**, and the selected item carries HeroUI's selection indicator, so the choice is never read from the icon alone.
- **It calls HeroUI's `useTheme` and nothing else.** The storage, the class on `<html>`, and the no-flash script belong to [[darkmode.component.md]].
- One control, in one place. There is no second theme control in a settings page or in the rail.

## The Notification Bell

The bell opens the notification panel, per [[notification.component.md]].

- **The marker is a dot, never a number.** A `7px` danger dot, the same marker vocabulary [[sidebar.component.md]] defines. A count belongs on the rail row that leads to the thing being counted.
- **Render the dot only when the unread count is above zero.** There is no empty-circle state.
- **The accessible name states the count**, such as `Notifications, 3 unread`, because a red circle says nothing to a screen reader.
- **The count is fetched once a minute and when the window regains focus.** A failed fetch leaves the bell silent rather than showing an error in the bar; the panel reports failures, because the user opened it on purpose.
- **When the unread count rises, the dot pulses once**, per [[animation.component.md]], and never again until it rises again.

## Responsive

The bar uses the single breakpoint from [[uix.component.md]] and adds none of its own.

- **Below the breakpoint the hamburger appears**, the brand drops its name and keeps its logo, and the search collapses to an icon.
- **The bar is one row at every width.** Nothing wraps to a second line, and nothing is removed; every slot either shrinks or drops a secondary part.
- **The hamburger is a real button** with `aria-expanded` reflecting the rail drawer, which slides in under [[animation.component.md]].

## Sizing Reference

| Element | Value |
| :- | :- |
| Bar | `60px` tall, full window width, sticky at the top, `bg-background` with one `border-border` hairline along its bottom |
| Gap, padding | `12px`, `0 16px` |
| Logo | `30px` |
| Product name | `600`, `14px` |
| Search trigger | `34px` tall, `220px` wide above the breakpoint |
| Icon buttons | HeroUI `size="md"`, with a `20px` icon |
| Bell dot | `7px`, danger |
| Stacking | Below the rail drawer and its backdrop, so an open drawer covers the bar |

## Accessibility

- **The bar is a `header` element**, not a `div`.
- **Every icon-only button has an accessible name**: `Open menu`, `Search`, `Theme`, and a bell name that states the count.
- **The search shortcut is announced** through the trigger's name, such as `Search (Ctrl+K)`.
- **The bar is sticky, so it never grows tall enough to eat a small screen.** 60px is its height at every width.
- **A rising count is not announced on every poll.** The bell's name changes; nothing in the bar is a live region.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Span the full window width, above the rail and the content | Put the bar beside the rail, or repeat the brand in the rail |
| Keep the six slots in their fixed order | Shift the bell left when a slot is empty |
| Name the product, from one constant | Put a page title, a breadcrumb, or an `h1` in the bar |
| Offer jump-to search with a shortcut shown as a `Kbd` | Turn the bar's search into a record search |
| Offer Light, Dark, and System in one theme control | Add a second theme control anywhere else |
| Mark unread with the `7px` danger dot, only above zero | Show a count on the bell, or an empty dot |
| Put the account in the rail footer | Add an account block or sign-out to the bar |
| Keep one row at every width | Let the bar wrap or grow past 60px |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[layout.component.md]] | The page shell | Where the bar sits above the rail and the content |
| [[header.page.component.md]] | The page heading | Where a page's title and actions go instead |
| [[sidebar.component.md]] | The rail | The account footer, the drawer, and the marker vocabulary |
| [[darkmode.component.md]] | Light and dark | What the theme control switches |
| [[notification.component.md]] | The notification panel | What the bell opens |
| [[title.header.component.md]] | The product name | Why the brand never changes with the route |
| [[dropdown.component.md]] | Pickers and smart search | The palette's matching and the theme menu |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. [[layout.component.md]], for anything the shell and the bar share
6. This header bar standard
7. Existing project conventions

## Related

- [[uix.component.md]]
- [[layout.component.md]]
- [[header.page.component.md]]
- [[sidebar.component.md]]
- [[darkmode.component.md]]
- [[notification.component.md]]
- [[title.header.component.md]]
- [[dropdown.component.md]]
- [[search.component.md]]
- [[animation.component.md]]
- [[stacks.rules.md]]
- [[memory.rules.md]]
