---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Page Heading Standard

> [!important]
> Every page opens with one page heading: its `h1`, its actions, and its description. It is the first block of the page and scrolls with it. Everything that names or acts on the current page lives here, never in the header bar.

## Core Requirement

**Every page opens with one page heading**, the first block inside the content pane, holding the page title, the page's actions, and an optional description. It scrolls away with the content, as [[layout.component.md]] draws it.

The header bar above the rail and the content is a different thing with its own standard, [[header.bar.component.md]]. The bar carries no title of any kind, so **everything that names or acts on the current page belongs here, and never in the bar.**

This extends [[uix.component.md]]. Its actions are HeroUI `Button`s, per [[button.component.md]]; its title and description are plain text in Google Sans.

## The Bar Is Not the Page Heading

Two different things are both called a header, and confusing them is the most common way either standard gets broken.

| | The header bar | The page heading |
| :- | :- | :- |
| Where | Above the rail and the content, across the window, one per project | At the top of the content pane, scrolling with it |
| Carries | Hamburger, brand, jump-to search, theme control, bell | The page's `h1`, the page's actions, and the description |
| Changes with the route | Never | Entirely |
| Owned by | [[header.bar.component.md]] | This file |

```tsx
export function PageHeading({ title, description, actions }: Props) {
  return (
    <div className="mb-6">
      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
        <h1 className="min-w-0 truncate text-xl font-semibold tracking-tight">{title}</h1>
        {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
      </div>
      {description && <p className="mt-1.5 text-sm text-muted">{description}</p>}
    </div>
  );
}
```

- **The `h1` lives in the page heading, never in the bar.** An `h1` in the bar leaves the page with two competing titles at two sizes.
- **The page heading scrolls with the content.** It is the first block of the page, not a strip pinned above the pane.
- **A page action belongs in the page heading**, on the right of the title, where [[button.component.md]] puts the one primary action per view. In the bar it would change on every route, which is the one thing the bar must not do.
- **The description sits under the title row**, in the muted ink.
- **A notice about the whole section goes under the page heading, never above the title**, as an inline `Alert`, per [[notification.component.md]].
- **A page filter belongs in the page**, above the content it filters, never in the heading's title row and never in the bar.
- **Every page has a title.** A page that draws its heading another way, such as a dashboard greeting, still renders exactly one `h1`.

## The Page Title

The title names the page the user is on, in one line.

- **The title comes from a route-to-label map, not from the URL.** Deriving `Invoice Lines` from `/invoice-lines` by replacing dashes produces a label nobody wrote and nobody reviewed.
- **The title matches the rail row that leads to the page**, word for word. Two names for one destination make the user check whether they are in the same place.
- **The title is the page's own name only.** A page inside a group is titled `Scheduled`, not `Automation > Scheduled`; the open group in the rail already shows the parent.
- **The product name is not part of the title.** The brand in the bar already says it, and [[title.header.component.md]] keeps the same rule for the browser tab.
- **A detail page is titled with its record's name**, such as the client's name on a client page. Until the record has loaded, the title shows a placeholder such as `Detail`, never an identifier like `INV-2026-0912`.
- **An unmatched route falls back to the product name** rather than rendering an empty heading.
- **The title truncates with an ellipsis rather than wrapping.** The actions may wrap under it on a narrow pane instead of squeezing it.

## Sizing Reference

| Element | Value |
| :- | :- |
| Page title | `600`, `20px`, tight tracking, one line with an ellipsis |
| Title row | Wraps, `16px` between title and actions, `8px` between wrapped lines |
| Actions | HeroUI `Button`s, `8px` apart, wrapping |
| Description | `14px` in the muted ink, `6px` under the title row |
| Heading block | `24px` above the content beneath it |

## Accessibility

- **The page title is the page's only `h1`.** The bar holds no heading, so the page heading is where a screen reader's heading list starts.
- **Headings below it descend without skipping a level**, per [[uix.component.md]].
- **An icon-only action carries an accessible name**, per [[button.component.md]].
- On the default title setting, the document title updates with the page, per [[title.header.component.md]].

## Do and Do Not

| Do | Do not |
| :- | :- |
| Open every page with one heading holding its `h1` | Put the page title in the header bar |
| Take the title from a route-to-label map | Build the title by transforming the URL |
| Match the title to the rail row word for word | Prefix the title with its group or the product name |
| Put the page's actions on the right of the title | Put a page action in the bar |
| Put the primary action last in the actions row | Put two primary actions in one heading |
| Truncate the title and let the actions wrap | Let the title wrap to a second line |
| Put a section notice under the heading | Put a notice above the title |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[header.bar.component.md]] | The header bar | What the bar carries instead |
| [[layout.component.md]] | The page shell | Where the heading sits in the content pane |
| [[button.component.md]] | The button variants | The one primary action in the actions row |
| [[title.header.component.md]] | The product name | Why the product name is not in the title |
| [[sidebar.component.md]] | The rail | The row label the title must match |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This page heading standard
6. Existing project conventions

## Related

- [[uix.component.md]]
- [[header.bar.component.md]]
- [[layout.component.md]]
- [[button.component.md]]
- [[title.header.component.md]]
- [[sidebar.component.md]]
- [[notification.component.md]]
- [[memory.rules.md]]
