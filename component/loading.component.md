> Up: [[README.md]] · [[uix.component.md]]

# Loading Standard

> [!note]
> Every loading state: the route gate, the button spinner, the inline section loader, and the skeleton.

## Core Requirement

Every wait a user can see uses one of the four surfaces below, chosen by what is waiting and where.

A wait with no feedback is indistinguishable from a broken page, and a user who cannot tell the difference clicks again. Most double submissions are a loading problem, not a validation problem.

This extends [[uix.component.md]] and uses its tokens. It defines no color of its own.

## Choosing the Right Surface

The question is not "is it loading" but **what part of the screen cannot be trusted yet**.

| The wait | Surface |
| :- | :- |
| The route itself, before anything can render | Route gate |
| A user action, started by a control | Button loading |
| One region of an otherwise usable page | Inline section loading |
| Content whose shape is known before its data | Skeleton placeholder |

Pick one per wait. Two surfaces for one wait, such as a skeleton inside a gated route, means the page is telling the user twice.

## Case 1: Route Gate

A full-surface state shown while the route decides whether it can render at all: an authentication check, a permission check, the first fetch a page cannot exist without.

- It replaces the page content, never overlays it.
- It holds a centered spinner and one line of text.
- **It resolves into the page or into an error, never into an empty screen.** A gate that finishes with nothing to show is the most common way a blank page ships.
- The authentication check must complete before any redirect, per [[refresh.component.md]]. Redirecting while the check is still pending is what sends a signed-in user to the login screen on refresh.

## Case 2: Button Loading

The control that started the work shows the work.

- **Disable the control while the request is in flight.** This is the double submission fix, and it belongs on the control rather than on a guard in the handler.
- Replace the label with a spinner and a verb, or keep the label and place a spinner before it. Choose one and use it everywhere.
- **Keep the button's width stable.** A button that shrinks to fit "Saving" moves everything beside it, and the user's next click lands somewhere else.
- Re-enable on both success and failure. A control left disabled after an error strands the user on a form they cannot resubmit.

## Case 3: Inline Section Loading

One region is waiting while the rest of the page works: a panel, a table body, a chart.

- The spinner sits inside that region's own bounds and nothing outside it changes.
- **Reserve the region's height before the load.** A section that grows when its data arrives pushes the page down under a cursor that was already moving.
- Never lock the whole page for a region. If the rest of the page is usable, it stays usable.

## Case 4: Skeleton Placeholder

Used when the shape of the content is known in advance: a list of rows, a card grid, a table.

- The skeleton matches the real layout's dimensions, so nothing jumps when the content replaces it.
- Show the number of rows the page usually holds, not one and not fifty.
- Use a skeleton only where the shape really is predictable. A skeleton that does not match what arrives is worse than a spinner, because it promised a layout and then changed it.
- Prefer a skeleton over a spinner for content, and a spinner over a skeleton for an action. Content has a shape; an action does not.

## Text Rules

- Say what is happening, in a verb: loading, saving, checking. Never a bare "please wait".
- One line. A wait is not the place for an explanation.
- **Never show a fake percentage.** A progress bar that is not driven by real progress is a lie the user will time.
- After an unusually long wait, say what is slow rather than continuing to spin silently.

## Animation

- One spinner for the whole product, in one direction, at one speed.
- Respect `prefers-reduced-motion`: replace the spin with a static or fading indicator rather than removing the feedback entirely.
- Do not animate the page's background or layout while waiting.

## Accessibility

- A loading region carries `aria-busy="true"` while it waits.
- Announce the state with a live region, so the wait is not visual only.
- A disabled loading button keeps an accessible name that says it is working.
- Move focus to the new content when a route gate resolves, so a keyboard user is not left at the top of a page that changed underneath them.

## Do and Do Not

Do:

- Disable the control that started the work.
- Reserve space before the content arrives.
- Say what is loading, in a verb.
- Resolve every gate into content or an error.

Do not:

- Show two loading surfaces for one wait.
- Let a button change width when its label changes.
- Fake a percentage.
- Leave a control disabled after a failure.
- Overlay the whole page for a region that is loading.

## Related

- [[uix.component.md]]
- [[refresh.component.md]]
- [[dashboard.component.md]]
