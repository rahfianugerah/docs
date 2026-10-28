---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Card Standard

> [!note]
> Every card is a HeroUI `Card`. It holds content, never another card, and a table inside it runs flush to its edges.

## Core Requirement

**A card is the standalone surface a feature draws on the page.** It holds content: a heading, text, a table, a chart, a stat, or controls. Every bordered box in a project is a HeroUI `Card`, so no box with a border and no fill melts into the page.

It owns the surface, its heading, and how its content meets its edge. It does **not** own the width it takes, which is [[layout.component.md]], the table inside it, which is [[table.component.md]], or the theme variables it reads, which are [[uix.component.md]].

## Built On HeroUI

This is HeroUI's `Card`, with `Card.Header`, `Card.Title`, `Card.Description`, `Card.Content`, and `Card.Footer`. HeroUI draws the surface, the border, the 8px corner, and the faint surface shadow, and switches all of them with the theme. Exact props come from the HeroUI MCP server, per [[stacks.rules.md]].

## Anatomy

A card is at most three parts, in this order:

1. **The header**, optional: a title on the left, at most one companion on the right such as a button or a count, and a description beneath the title when the title alone is not enough.
2. **The content**: anything the card holds, with HeroUI's padding, or a flush table, per "A Table Inside a Card Is Flush" below.
3. **The footer**, optional: the card's own actions, aligned to the end.

```tsx
import { Button, Card } from "@heroui/react";
import { IconFileUpload } from "@tabler/icons-react";

<Card>
  <Card.Header className="flex items-center justify-between gap-2">
    <Card.Title>Add Credential</Card.Title>
    <Button size="sm" variant="secondary"><IconFileUpload size={16} /> Choose File</Button>
  </Card.Header>
  <Card.Content>{/* body */}</Card.Content>
</Card>
```

## The Surface

- **`variant="default"` is the card.** HeroUI's `secondary` and `tertiary` variants are for a quieter surface inside a busy page; `transparent` is for a grouping that needs the card's spacing but no edge. Pick one per kind of content and keep it across the project.
- **The corner is HeroUI's `--radius`, 8px**, the one radius in the project, per [[uix.component.md]]. A card never takes a corner of its own.
- **The shadow is HeroUI's surface shadow and never heavier.** A pronounced shadow belongs to an overlay, never to a card.
- **Every value is a theme variable.** A card painted with a hex stays light in the dark theme and is a defect, per [[darkmode.component.md]].
- **A card spans the full width of the content area**, or one column of a grid that does, per [[layout.component.md]]. It never shrinks to its content and floats in the middle of the page.

## A Section Is a Heading and a Divider

- **A section inside a card is a heading with a `Separator` above it**, not a nested surface. A card that needs three sections needs three headings, or it needs to be three cards.
- **The title is Title Case**, per [[uix.component.md]]. The header holds the title and at most one companion, and wraps rather than squeezing either.
- The divider is HeroUI's `Separator`, one step lighter than the card's own border, so it reads as inside the card and not as a second edge.

## A Card Does Not Hold a Card

**The default is one level of card**, per [[uix.component.md]]. Two borders and two paddings stacked inside each other spend a line and an inset to say nothing the heading would not.

- **A group of things is a grid of cards laid on the page**, not cards inside a wrapper card. The page is the container, and the 8px gap is what groups them.
- **A modal holds its content directly.** It is already a surface.
- **A page panel is a card.** Do not wrap a set of cards in a panel to title them; put the title in the page heading, per [[header.page.component.md]].
- A genuinely recursive structure, such as a comment thread, separates its levels with indentation and a rail rather than a second border.

## A Table Inside a Card Is Flush

**A table inside a card needs no border or corner of its own.** The card's edge is the table's edge.

- **The table runs from card edge to card edge**, with no padding between it and the border. Its horizontal scroll stays; its own frame goes.
- **The card clips its content** with `overflow-hidden`, so the table's header band and its row hover follow the card's corner instead of showing square past it.
- **A table straight on the page, outside any card, keeps its own frame**, per [[table.component.md]].

## A Box Inset Inside a Card

An image, a media block, or a grid cell set tightly inside a card is not a card, so it is allowed. Its corner is the card's corner minus the inset, so the two curves sit concentric, per [[uix.component.md]].

- **A control in the card's ordinary padding keeps the 8px corner** and computes nothing.
- **A grid that fills the card to its edge** rounds only the cells at the card's corners, at the card's radius minus its border, and every other cell stays square. A month calendar is the worked example, per [[calendar.component.md]].

## Do and Do Not

| Do | Do not |
| :- | :- |
| Draw every bordered box as a HeroUI `Card` | Hand-build a bordered box, or paint a card with a hex |
| Use `Card.Header`, `Card.Content`, and `Card.Footer` in that order | Invent a fourth part, or put actions in the header and the footer both |
| Keep HeroUI's surface shadow and nothing heavier | Give a card an overlay's shadow |
| Split a card into sections with headings and a `Separator` | Put a card inside a card to make a section |
| Lay a group of cards out as a grid on the page | Wrap a group of cards in a titled wrapper card |
| Run a table flush inside a clipped card | Give a table inside a card its own border and corner |
| Keep the frame on a table that sits straight on the page | Strip the frame from a standalone table |
| Let the card span the full content width | Shrink a card to its content and center it |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The theme variables, the radius, and the one-level rule | Every value a card reads |
| [[layout.component.md]] | The page shell | The width a card takes |
| [[table.component.md]] | The table | The frame a standalone table keeps |
| [[dashboard.component.md]] | Charts and stat tiles | The chart card and the stat tile |
| [[darkmode.component.md]] | Light and dark | Why a card never carries a fixed color |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This card standard
6. Existing project conventions

## Related

- [[uix.component.md]]
- [[layout.component.md]]
- [[table.component.md]]
- [[dashboard.component.md]]
- [[darkmode.component.md]]
- [[header.page.component.md]]
- [[calendar.component.md]]
- [[stacks.rules.md]]
- [[memory.rules.md]]
