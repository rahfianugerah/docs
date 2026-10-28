---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Animation Standard

> [!note]
> Motion shows the user that something changed, and where. It answers an action, it is short, it fades by default, and reduced motion turns it off everywhere, including in JavaScript.

## Core Requirement

Every animation in a project follows this standard: changing page, swapping a section inside a page, and everything that appears or disappears, such as a panel, a modal, a toast, or a new item in a list.

Motion has one job: **to show the user that something changed, and where**. A page that fades in tells the user they arrived somewhere new without a jump; a panel that grows from its button tells them where it came from. Motion that does neither is decoration, and this standard has no place for it.

Six principles hold everywhere:

1. **Motion answers an action.** Nothing animates on its own, on the first load of a page, or when data refreshes in the background.
2. **Fade is the default shape.** Opacity, sometimes with a slight scale. A slide is kept for what physically enters from an edge: a drawer and a toast.
3. **Short.** Every animation is between `120ms` and `250ms`. Anything longer starts to feel like waiting.
4. **Enter animates; exit is instant, except at the edge.** A page does not fade out before the next one fades in. A drawer slides back out and a toast fades out, because both leave toward where they came from. Nothing ever makes the user wait on an animation before they can act.
5. **Only `opacity` and `transform` animate.** Animating `width`, `height`, `top`, `margin`, or `padding` forces layout on every frame and stutters on a slow laptop.
6. **Reduced motion is honored everywhere**, per "Reduced Motion" below.

## Built On HeroUI

**HeroUI's components keep their own motion.** A `Popover`, a `Modal`, a `Drawer`, a `Toast`, a `Tooltip`, and the indicator of a `Select` all animate as HeroUI ships them, and that motion already respects reduced motion. Never override it, slow it, or add a second animation on top.

This standard governs what the project builds itself: the page fade, the section fade, the sidebar drawer, and a new item joining a list. Those take their durations from "The Motion Scale" below, so they sit beside HeroUI's motion without looking like a second app.

## The Motion Scale

| Duration | Easing | Used for |
| :- | :- | :- |
| `120ms` | `ease-out` to enter, `ease-in` to leave | A hover or press color, a toast fading out |
| `160ms` | `ease-out` | A rotating chevron, a toast sliding in |
| `200ms` | `ease-out` | **Content fading in**: a page, a section inside a page, a new item in a list, the theme color |
| `240ms` | `ease` | A drawer sliding in and out, and its backdrop |
| `250ms` | `cubic-bezier(0.32, 0.72, 0, 1)` | A modal panel scaling in, the one movement allowed to settle |

A new duration is added to this table first, with its reason, and only then used. A one-off `300ms` in one component is how a project ends up feeling like three projects.

## Changing Page

Every navigation to another page fades the content pane in over `200ms`. The header bar and the rail stay perfectly still, so the eye reads the change in exactly the place that changed.

- **Fade in only.** The old page disappears at once and the new one fades in from `opacity: 0`. There is no fade out, so a click never waits on the old page.
- **The path decides, the query does not.** The fade runs when `pathname` changes. A filter, a page number, a sort, or a tab written into the query string is the same page with different data, and it does not fade, per [[refresh.component.md]].
- **The first render does not fade.** A load, a refresh, or a deep link opens the page as it is.
- **It does not move focus or scroll.** It changes opacity only.

The fade lives once, in the shell, never in each page:

```tsx
// Fade the content pane on navigation; skip the first render and reduced motion
const first = useRef(true);
useEffect(() => {
  if (first.current) { first.current = false; return; }
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  paneRef.current?.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200, easing: "ease-out" });
}, [location.pathname]);
```

- **`element.animate` rather than a CSS class.** Replaying a CSS animation needs the page remounted with a new `key`, which throws away its state and refetches its data. `animate` replays on the same element without touching the React tree.
- **The `matchMedia` check is required.** The global reduced-motion rule in CSS does not reach an animation started from JavaScript.

## Changing a Section Inside a Page

A HeroUI `Tabs`, a segmented control, or a filter chip that swaps the section below it fades that section in over `200ms`, the same fade as a page, applied to the section only.

- **The section fades; the control does not.** The selected tab changes at once, so the user sees their click land before the content arrives.
- **A `key` on the section, never on the page**, so only the swapped content remounts.
- **One fade utility for the whole project.** Do not write a second.

## Opening and Closing a Drawer

A drawer is a HeroUI `Drawer`, or the sidebar rail below the breakpoint, per [[sidebar.component.md]]. It **slides in and slides out** from its own edge, with its backdrop fading over the same time.

- **The exit slides because a drawer is a surface the user comes back to.** Seeing it return to its edge tells them where to reach for it again.
- **The exit never blocks.** The backdrop stops taking clicks the moment closing starts.
- **Focus returns to the trigger** when the drawer is gone. HeroUI's `Drawer` does it; a hand-built rail must too.

> [!warning]
> A drawer that unmounts on `animationend` must have its animation shortened under reduced motion, never removed. The global rule below sets the duration to `0.01ms`, so the event still fires and the drawer closes at once. A rule that sets `animation: none` leaves the drawer open for exactly the users who asked for less motion.

## Things That Appear and Disappear

| Moment | Animation |
| :- | :- |
| A popover, dropdown, or picker opens | HeroUI's own; never overridden |
| A modal opens | HeroUI's own: the backdrop fades, the panel scales in |
| A toast arrives and leaves | HeroUI's own, per [[notification.component.md]] |
| A new item joins a list, such as a chat message | Fades in over `200ms` |
| The sidebar drawer opens or closes below the breakpoint | Slides from the left edge over `240ms`, with the backdrop |
| A chevron opens | Rotates `180deg` over `160ms`, per [[dropdown.component.md]] |
| The theme changes | `body` color transitions over `200ms`, per [[darkmode.component.md]] |
| The bell's unread count rises | The dot pulses once, per [[notification.component.md]] |

A wait that is still going on, such as a skeleton shimmer or a spinner, is a loading state rather than an animation in this sense, and [[loading.component.md]] and [[skeleton.component.md]] own it.

## What Never Animates

- **The first paint of a page.** A load, a refresh, or a deep link shows the page as it is.
- **Data that changes in the background**, such as a poll, a live count, or a list refreshed every minute. Moving it pulls the eye away from what the user is doing.
- **Results that follow typing**, such as a dropdown narrowing on each keystroke. A fade per keystroke turns typing into flicker.
- **A table changing page, sort, or filter.** The rows are replaced in place, with a skeleton while they load, per [[pagination.component.md]].
- **A number counting up**, a progress bar racing to its value, or a chart drawing itself on load.
- **Layout properties**, per the principles above.

There is no bounce, spring, overshoot, parallax, or decorative loop anywhere in a project page.

## Reduced Motion

The operating system setting is respected everywhere, with one global rule:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

- **The rule reaches every CSS animation and transition**, so a fade becomes an instant change and nothing is lost.
- **It does not reach JavaScript.** An animation started with `element.animate` or a View Transition checks `matchMedia("(prefers-reduced-motion: reduce)")` itself and skips.
- **Content is never hidden waiting for an animation.** Nothing starts at `opacity: 0` from a class that only an animation removes, so a page whose script fails still shows its content.

## Accessibility

- Honor `prefers-reduced-motion` in CSS and in JavaScript.
- Nothing flashes more than three times in one second.
- An animation never moves focus. Where a navigation must move focus, the code moves it, and the animation runs on top.
- A control is usable from the first frame of its animation; nothing is disabled until an animation ends.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Keep HeroUI's own motion on every HeroUI component | Override, slow, or stack an animation on a HeroUI overlay |
| Fade the content pane in over `200ms` on navigation, from the shell, once | Fade the old page out, or make a navigation wait |
| Fade a swapped section in, keyed on the section | Key the whole page to replay a fade |
| Slide a drawer in and out from its own edge | Slide a page or a section |
| Take every duration from the motion scale | Invent a one-off duration in one component |
| Animate `opacity` and `transform` only | Animate `width`, `height`, `top`, or `margin` |
| Check reduced motion in every JavaScript animation | Rely on the CSS rule to reach JavaScript |
| Shorten a drawer's animation under reduced motion | Set `animation: none` on something that waits for `animationend` |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The HeroUI setup and the component rules | Why HeroUI's motion is kept as is |
| [[notification.component.md]] | The toast and the bell | The toast's entry and the dot's pulse |
| [[sidebar.component.md]] | The rail and its drawer | The drawer this file slides |
| [[darkmode.component.md]] | Light and dark | The theme transition |
| [[loading.component.md]] | Loading states | Why a spinner is not an animation in this sense |
| [[refresh.component.md]] | What survives a reload | Why a query change does not fade |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Accessibility requirements, specifically reduced motion and the flash limit
2. Direct user instructions
3. [[uix.component.md]]
4. This animation standard
5. Existing project conventions

## Related

- [[uix.component.md]]
- [[notification.component.md]]
- [[sidebar.component.md]]
- [[darkmode.component.md]]
- [[loading.component.md]]
- [[skeleton.component.md]]
- [[dropdown.component.md]]
- [[pagination.component.md]]
- [[refresh.component.md]]
- [[memory.rules.md]]
