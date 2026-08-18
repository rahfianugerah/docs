> Up: [[README.md]] · [[uix.component.md]]

# Scrollbar Standard

## Core Requirement

**A region that scrolls must show that it scrolls.**

This is the rule everything else here serves, and it is the one most often broken. A hidden scrollbar on a region with more content below it produces a page where the remaining content simply does not exist as far as the user is concerned.

This extends [[uix.component.md]] and uses its tokens.

## A Scrollbar Is an Affordance, Not Decoration

Hiding a scrollbar is styling that removes information. The scrollbar answers two questions nothing else on the screen answers: is there more, and how much more.

- **Never set `scrollbar-width: none` or hide the WebKit scrollbar** on a region a user scrolls.
- Never rely on a fade or a shadow alone to imply more content. It says something is below; it does not say how much, and it disappears on the platforms that need it most.
- A custom scrollbar is allowed. An absent one is not.

## The Shared Scrollbar

One scrollbar style for the whole product, defined once beside the token set and applied wherever a region scrolls.

- The thumb uses the border token, and darkens to the secondary text token on hover.
- The track is transparent or the page background, never a contrasting stripe.
- Round the thumb by half its width.
- Keep the thumb wide enough to grab with a mouse. A two-pixel hairline is a decorative line, not a control.
- Style both the standard properties and the WebKit pseudo-elements, so the same region looks the same across browsers.
- Never animate the thumb's size or position. The browser owns that.

## The Scrollbar Belongs to the Component

**The region that scrolls owns its scrollbar**, and the page does not scroll on its behalf.

- Put the overflow on the element whose content overflows, not on an ancestor.
- A modal body scrolls inside the modal. The page behind it does not scroll at the same time.
- **Lock the background when a modal or drawer is open**, and restore the scroll position when it closes, per [[refresh.component.md]].
- Never nest two vertical scroll regions. The user cannot tell which one their wheel will move, and neither can the browser.

## Tables

A wide table is the most common horizontal scroll in a product, and the most commonly broken.

- **The table scrolls inside its own container**, with the overflow on that container. The page body never scrolls horizontally.
- Keep the header row visible while the body scrolls vertically.
- Where the first column identifies the row, pin it while the rest scrolls horizontally, or the numbers stop meaning anything.
- Give the container a maximum height only when the surrounding layout genuinely needs one. A table free to grow inside a scrolling page is easier to read than one squeezed into a small window.
- The horizontal scrollbar on a table must be visible without hovering, because there is no other cue that columns continue.

## Where It Applies

Anywhere content can exceed its box: a sidebar nav, a modal body, a table container, a long select list, a code block, a chart container, a card list with a fixed height.

### The Two Exceptions

- **A carousel or a snap track** that moves by control rather than by dragging a bar may hide its scrollbar, provided the controls are visible and the position is shown some other way, such as dots.
- **A single-line horizontally scrolling strip of chips**, where the content is obviously cut and the gesture is the only interaction, may hide it. Fade the trailing edge so the cut is visible.

Everything else shows its scrollbar.

## Accessibility

- **A scrollable region must be reachable and scrollable by keyboard.** Give it `tabindex="0"` where it holds no focusable child, so arrow keys work.
- Give it an accessible name where it is a distinct region, so a screen reader user knows what they are scrolling.
- Never trap the wheel or override the platform's scrolling behaviour.
- Respect `prefers-reduced-motion` on any programmatic scroll: jump rather than smooth-scroll.
- The thumb keeps enough contrast against the track to be seen, in both light and dark.

## Do and Do Not

Do:

- Show a scrollbar on every region that scrolls.
- Put the overflow on the element that actually overflows.
- Scroll a wide table inside its own container.
- Keep a table header visible while the body scrolls.
- Make a scroll region keyboard reachable.

Do not:

- Hide a scrollbar for looks.
- Nest two vertical scroll regions.
- Let the page body scroll horizontally.
- Use a fade alone to signal more content.
- Style the thumb so thin it cannot be grabbed.

## Related

- [[uix.component.md]]
- [[refresh.component.md]]
- [[dashboard.component.md]]
- [[sidebar.component.md]]
