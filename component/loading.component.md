---
tags:
  - kind/component
  - layer/frontend
  - topic/state
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Loading Standard

> [!note]
> Four loading surfaces, and which wait each one serves. Every one of them pairs an indicator with visible text.

## Core Requirement

Every loading state uses one of **four surfaces**: a route gate that holds a whole page, a button that is submitting, a section inside a page that is still fetching, and a skeleton standing in for content whose shape is already known.

**Every one of them pairs an indicator with visible text naming what is being waited on.** A bare spinner announces nothing to a screen reader and tells a sighted user nothing either.

This standard does not redefine a token. A loading state that introduces its own hex value or its own animation timing, instead of reading the tokens in [[uix.component.md]] and the values in this file, is not following it.

**One indicator per wait.** A route gate does not sit above a section that is also loading.


## Choosing the Right Surface

| The wait | Surface | Why |
| :- | :- | :- |
| The session is being checked before the first paint | Route gate | Nothing can be drawn yet, and the wrong screen must not flash |
| A form the user just submitted | Button loading | The wait belongs to the control the user pressed |
| A section of an already-drawn page is fetching | Inline section loader | The rest of the page stays usable |
| A component whose layout is already known is fetching | Skeleton, per [[skeleton.component.md]] | The page does not jump when the data lands |

The test between the last two is whether the shape is genuinely known before the data arrives. A table with fixed columns and a known page size passes. A search result that might return nothing does not.

## Case 1: Route Gate

A route gate is a full-page hold shown while the app decides what the user is allowed to see, most often while the session is being checked on the first paint. It exists to stop the app flashing the login form at a user who is already signed in, and to stop it flashing a protected page at a user who is not.

```tsx
import { Spinner } from "@heroui/react";

<div className="grid min-h-svh place-items-center content-center gap-4 bg-background p-8 text-muted" role="status" aria-live="polite">
  <Spinner size="lg" aria-hidden />
  <p className="text-sm">Checking your session...</p>
</div>
```

- **The gate holds the full viewport with `100svh`, not `100vh`**, so mobile browser chrome does not push the indicator off centre.
- **The spinner is HeroUI's `Spinner`**, and the background is `bg-background`, so the gate follows the active theme. Never a gradient and never a decorative shape. A gate is a hold, not a screen to be designed.
- The spinner is `28px` here. **This is the one place a loader may exceed the 16 to 20px icon range** in [[uix.component.md]], because it is the only thing on the page.
- The gate always carries visible text saying what is being waited on.
- **Render the gate before the redirect decision, never after it.** A gate that runs after the redirect has already happened is the flash it was meant to prevent, per [[refresh.component.md]].

## Case 2: Button Loading

A button that has submitted shows the wait on itself. It is the only correct place for the wait, because it is the control the user just used.

```tsx
<Button type="submit" variant="primary" isPending={isSubmitting}>
  {isSubmitting ? "Signing in..." : "Sign In"}
</Button>
```

- **`isPending` is the whole mechanism.** HeroUI draws the spinner, refuses a second press, and announces the busy state, so a second submit cannot be sent.
- **The label is replaced with the loading label, not appended to it.**
- **Never hand-build a spinner inside a button**, and never write a second rotation keyframe for one.
- **The button keeps its own width and padding while loading.** A button that shrinks to fit the loading label makes the page jump under the cursor.
- **Never replace the whole form with a route gate while a submit is in flight.** The user must keep seeing what they typed.

## Case 3: Inline Section Loading

A section of a page that is already drawn shows its own wait in place, and the rest of the page stays usable.

```tsx
<p className="flex items-center gap-2 text-sm text-muted" role="status" aria-live="polite">
  <Spinner size="sm" aria-hidden />
  Loading your profile...
</p>
```

- The spinner is HeroUI's `Spinner` at `size="sm"`, and the text is `text-muted`.
- **The text names what is loading**, so a page with two sections loading does not show the same sentence twice.
- **The loading row, the error state, and the loaded content are mutually exclusive.** Guard each on the others, so an error is never shown under a spinner.
- **Never collapse the section to zero height while it loads** if that moves the rest of the page. Use a skeleton instead.

## Case 4: Skeleton Placeholder

Skeletons are owned by [[skeleton.component.md]], which covers the class, the per-component shapes, the row counts, and what happens on a refetch. This file keeps only the rule that decides between them.

> [!important]
> A component whose layout is already known shows a skeleton in its own place. It never hands the wait up to the page. The route gate above holds the whole viewport and exists for one thing, checking the session before the first paint; using it for a table that is fetching blanks a page the reader could have been reading.

## The Loader

- **The loader is HeroUI's `Spinner`**, everywhere: the route gate, an inline section, and inside a pending `Button`. Never an icon spun with a keyframe, an emoji, an animated GIF, or a third-party spinner library.
- **One spinner, one speed.** HeroUI turns every `Spinner` at the same rate, so two on one screen never look like two different states.
- **A loader takes the accent or the muted ink, never a status color**, because a wait is not a success, a warning, or an error.
- **A determinate wait is a `ProgressBar`**, and only when the app can measure real progress, such as an upload. Never a bar that fills on a timer.
- **Do not add a second animation to a loading state:** no pulsing opacity behind the spinner and no bouncing dots.

## Text Rules

Loading text is sentence case, per [[uix.component.md]], in the project's UI language.

| Surface | String | Used for |
| :- | :- | :- |
| Route gate | `Checking your session...` | Checking the session on first paint |
| Button | `Signing in...`, `Saving...` | A form submit that is in flight |
| Inline section | `Loading <noun>...` | A section fetching its own data |

- **End the string with three periods, never with the single-character ellipsis.** [[docs.rules.md]] disallows a decorative Unicode character, and three periods read the same to a screen reader.
- **Write what is being waited on, not the mechanism.** "Loading your profile..." is correct; "Fetching /api/v1/profile..." is not.
- **Never show a percentage or a time estimate the app cannot actually measure.**

## Reference Table

| Surface | Component | Size | Text |
| :- | :- | :- | :- |
| Route gate | `Spinner` | `lg` | `text-sm text-muted`, on `bg-background`, full `100svh` |
| Button | `Button` with `isPending` | The button's own | The loading label replaces the button label |
| Inline section | `Spinner` | `sm` | `text-sm text-muted` |
| Measured progress | `ProgressBar` | Full width of its container | A label naming what is progressing |

## Accessibility

Accessibility ranks above the design standard itself, per [[uix.component.md]].

- **Every loading state pairs the indicator with visible text.** A rotating icon announces nothing on its own.
- **Wrap the loading region in `role="status"` with `aria-live="polite"`**, so the wait is announced without interrupting what the user is doing. **Do not use `role="alert"`;** a wait is not an error.
- **Mark the spinner itself `aria-hidden="true"`** when the text next to it already says the same thing, so the state is announced once.
- A pending `Button` uses `isPending` rather than only looking busy, so it is announced and cannot be pressed twice.
- **Honour a reduced motion preference without removing the indicator**, because the indicator is the information. The visible text carries the state when the motion slows, per [[animation.component.md]].

- **Never trap the keyboard behind a loading state, and never move focus onto a spinner.** When a route gate resolves, focus stays where the user left it.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Use HeroUI's `Spinner`, and `isPending` on a button | Spin an icon with a keyframe of your own |
| Show the route gate while the session is being checked | Let the login form flash at a signed-in user |
| Show the wait on the button the user pressed, and disable it for the whole wait | Replace the form with a full-page gate |
| Name what is loading, in sentence case, ending in three periods | Ship a bare spinner, or a single-character ellipsis |
| Use a skeleton when the layout is known and a spinner when it is not | Promise a layout the data will not match |
| Keep one indicator per wait | Run a route gate above a section that is also loading |
| Slow the rotation under reduced motion | Remove the indicator entirely |
| Keep the spinner in the accent or the muted ink | Give a loader a success, warning, or error hue |
| Land a failed request on an error state | Leave a spinner turning forever with no way out |
| Keep the surface plain | Put a gradient or a decorative shape on a loading surface |
| Use `100svh` for the route gate | Use `100vh`, which mobile browser chrome pushes off centre |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens, the icon set, and the icon size range | Why the route gate spinner is the one documented exception to that range |
| [[skeleton.component.md]] | The fourth surface | The class, the per-component shapes, and what happens on a refetch |
| [[button.component.md]] | The button that is submitting | The variant, and why the width must not change |
| [[table.component.md]] | How a table combines loading with empty and error | Why the three are mutually exclusive |
| [[login.component.md]] | The sign-in screen | The two waits it carries, and the gate that stops the form flashing |
| [[refresh.component.md]] | The session check on first paint | Why the gate runs before the redirect decision |
| [[docs.rules.md]] | The formatting restrictions | Why the label ends in three periods and not an ellipsis character |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This loading standard
6. Existing project conventions

## Related

- [[uix.component.md]]
- [[skeleton.component.md]]
- [[button.component.md]]
- [[table.component.md]]
- [[login.component.md]]
- [[refresh.component.md]]
- [[docs.rules.md]]
