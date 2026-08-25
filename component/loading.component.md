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

Every wait in a project uses one of the four surfaces below, and **every one of them pairs an indicator with visible text naming what is being waited on.** A bare spinner announces nothing to a screen reader and tells a sighted user nothing either.

**One indicator per wait.** A route gate does not sit above a section that is also loading.

This standard extends [[uix.component.md]] and does not redefine a token.

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

```css
.gate {
  min-height: 100svh; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 16px; padding: 32px;
  color: var(--ink2); background: var(--surface);
}
.gate p { font-size: 13.5px; }
.gate-spin { color: var(--accent); animation: gate-rotate .9s linear infinite; }
@keyframes gate-rotate { to { transform: rotate(360deg); } }
```

```html
<div class="gate" role="status" aria-live="polite">
  <i class="ti ti-loader-2 gate-spin" style="font-size:28px" aria-hidden="true"></i>
  <p>Checking your session...</p>
</div>
```

- **The gate holds the full viewport with `100svh`, not `100vh`**, so mobile browser chrome does not push the indicator off centre.
- **The background is `--surface`**, never a gradient and never a decorative shape. A gate is a hold, not a screen to be designed.
- The spinner is `28px` here. **This is the one place a loader may exceed the 16 to 20px icon range** in [[uix.component.md]], because it is the only thing on the page.
- The gate always carries visible text saying what is being waited on.
- **Render the gate before the redirect decision, never after it.** A gate that runs after the redirect has already happened is the flash it was meant to prevent, per [[refresh.component.md]].

## Case 2: Button Loading

A button that has submitted shows the wait on itself. It is the only correct place for the wait, because it is the control the user just used.

```html
<button type="submit" class="btn pri" disabled>
  <i class="ti ti-loader-2 gate-spin" style="font-size:17px" aria-hidden="true"></i>
  Signing in...
</button>
```

- **The button is disabled for the whole wait**, with the `disabled` attribute present and not only the styling, so a second submit cannot be sent.
- **The label is replaced with the loading label, not appended to it**, and the spinner sits before the label.
- The spinner is `17px`, sized to the label next to it, and it reuses the shared rotation. **Do not write a second rotation keyframe for a button.**
- **The button keeps its own width and padding while loading.** A button that shrinks to fit the loading label makes the page jump under the cursor.
- **Never replace the whole form with a route gate while a submit is in flight.** The user must keep seeing what they typed.

## Case 3: Inline Section Loading

A section of a page that is already drawn shows its own wait in place, and the rest of the page stays usable.

```html
<p class="muted" role="status" aria-live="polite">
  <i class="ti ti-loader-2 gate-spin" style="font-size:16px" aria-hidden="true"></i>
  Loading your profile...
</p>
```

- The spinner is `16px` and the text uses `--ink2`.
- **The text names what is loading**, so a page with two sections loading does not show the same sentence twice.
- **The loading row, the error state, and the loaded content are mutually exclusive.** Guard each on the others, so an error is never shown under a spinner.
- **Never collapse the section to zero height while it loads** if that moves the rest of the page. Use a skeleton instead.

## Case 4: Skeleton Placeholder

Skeletons are owned by [[skeleton.component.md]], which covers the class, the per-component shapes, the row counts, and what happens on a refetch. This file keeps only the rule that decides between them.

> [!important]
> A component whose layout is already known shows a skeleton in its own place. It never hands the wait up to the page. The route gate above holds the whole viewport and exists for one thing, checking the session before the first paint; using it for a table that is fetching blanks a page the reader could have been reading.

## The Loader Icon and Its Animation

- **The loader is one glyph from the project's one icon set**, per [[uix.component.md]]. Never an emoji, an animated GIF, a third-party spinner library, or a glyph from a second icon set.
- **The rotation is `.9s linear infinite` through a single shared keyframe.** Every spinner in a project turns at the same speed, so two spinners on one screen never look like two different states.
- **The spinner color is `--accent`.** It is the only color a loader takes; **a loader never carries a semantic hue**, because a wait is not a success, a warning, or an error.
- **Do not add a second animation to a loading state:** no pulsing opacity behind the spinner, no bouncing dots, no progress bar that is not tied to real progress.

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

Every loading state reads its values from here. Do not hardcode any of the right-hand values.

| Property | Surface | Value |
| :- | :- | :- |
| Spinner color | All | `var(--accent)` |
| Spinner size | Route gate | `28px` |
| Spinner size | Button | `17px` |
| Spinner size | Inline section | `16px` |
| Rotation | All spinners | `.9s linear infinite` |
| Text color | Route gate, inline section | `var(--ink2)` |
| Font size | Route gate, inline section | `13.5px` |
| Background | Route gate | `var(--surface)` |
| Height | Route gate | `100svh` |
| Gap, padding | Route gate | `16px`, `32px` |

## Accessibility

Accessibility ranks above the design standard itself, per [[uix.component.md]].

- **Every loading state pairs the indicator with visible text.** A rotating icon announces nothing on its own.
- **Wrap the loading region in `role="status"` with `aria-live="polite"`**, so the wait is announced without interrupting what the user is doing. **Do not use `role="alert"`;** a wait is not an error.
- **Mark the spinner itself `aria-hidden="true"`** when the text next to it already says the same thing, so the state is announced once.
- A disabled submit button keeps its `disabled` attribute rather than only looking disabled, so it is skipped correctly by keyboard and by assistive technology.
- **Honour a reduced motion preference. Slow the rotation rather than removing the indicator**, because the indicator is the information:

```css
@media (prefers-reduced-motion: reduce) {
  .gate-spin { animation-duration: 2.4s; }
}
```

- **Never trap the keyboard behind a loading state, and never move focus onto a spinner.** When a route gate resolves, focus stays where the user left it.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Copy the shared gate, spinner, and keyframe rather than writing a new one per project | Write a second rotation keyframe for one surface |
| Show the route gate while the session is being checked | Let the login form flash at a signed-in user |
| Show the wait on the button the user pressed, and disable it for the whole wait | Replace the form with a full-page gate |
| Name what is loading, in sentence case, ending in three periods | Ship a bare spinner, or a single-character ellipsis |
| Use a skeleton when the layout is known and a spinner when it is not | Promise a layout the data will not match |
| Keep one indicator per wait | Run a route gate above a section that is also loading |
| Slow the rotation under reduced motion | Remove the indicator entirely |
| Colour the spinner `--accent` | Give a loader a success, warning, or error hue |

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

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
