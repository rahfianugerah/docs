---
tags:
  - kind/component
  - layer/frontend
  - topic/security
---

> Up: [[README.md]] · [[uix.component.md]]

# Login Standard

> [!note]
> One centered card, a fixed section order, and one error message for every credential failure. It is not a place for a per-project identity.

## Core Requirement

Every project uses the same login form. Signing in is the one screen every user sees in every product, so it looks and behaves identically everywhere.

**It is built entirely from HeroUI components**: a `Card`, a `Form`, two `TextField`s, an `Alert`, and `Button`s. HeroUI owns the fields, the focus ring, the error wiring, and the pending state. This standard owns what goes on the screen, in what order, and what every message says.

This extends [[uix.component.md]]. Nothing on this screen has its own color, radius, or shadow; it reads HeroUI's theme variables and so follows the light and dark theme like every other screen, per [[darkmode.component.md]].

## Required Structure

The form is a single centered card on the page canvas. Build it in this order:

1. A full-height wrapper on `bg-background`, centering one HeroUI `Card`, capped at `412px`.
2. **A HeroUI `Form` inside the card**, so pressing Enter in either field submits.
3. The brand row: the logo at 44 by 44, the product name, and the organization line beneath it.
4. The heading, then one sentence naming what the user is signing into.
5. A HeroUI `Alert` with `status="danger"`, rendered only when there is something to say.
6. A `TextField` for the identifier.
7. A `TextField` for the password, with a show and hide toggle.
8. The submit `Button`, `variant="primary"`, full width.
9. The single sign-on block, rendered only when one is configured: a divider reading the divider word, then a full width `secondary` button.
10. A centered hint telling the user where to get help.

**Do not add a section this list does not contain.** A login screen has no remember-me box, no social sign-in, no self-service registration, and no marketing copy, because access is granted by the identity source and not by the app.

```tsx
import { Alert, Button, Card, FieldError, Form, Input, Label, TextField } from "@heroui/react";
import { IconEye, IconEyeOff, IconLogin } from "@tabler/icons-react";

<main className="grid min-h-svh place-items-center bg-background p-6">
  <Card className="w-full max-w-[412px]">
    <Card.Content>
      <Form onSubmit={signIn} className="flex flex-col gap-4">
        {/* brand row, heading, and one-sentence description */}
        {error && <Alert status="danger">{error}</Alert>}

        <TextField name="userid" isRequired autoComplete="username">
          <Label>User ID</Label>
          <Input placeholder="Example: 0000000" />
          <FieldError />
        </TextField>

        <TextField name="password" type={shown ? "text" : "password"} isRequired autoComplete="current-password">
          <Label>Password</Label>
          <Input placeholder="Enter your password" />
          {/* toggle: an isIconOnly ghost Button swapping IconEye and IconEyeOff */}
          <FieldError />
        </TextField>

        <Button type="submit" variant="primary" fullWidth isPending={busy}>
          <IconLogin size={16} /> {busy ? "Signing in..." : "Sign In"}
        </Button>
      </Form>
    </Card.Content>
  </Card>
</main>
```

The exact anatomy of `TextField`, `Alert`, and `Card` comes from the HeroUI MCP server, per [[stacks.rules.md]]; the order and the content above do not change.

## Icons

Every icon the screen adds is Tabler, per [[uix.component.md]].

| Element | Icon | Size |
| :- | :- | :- |
| Brand row | The logo asset, not an icon | `44px` by `44px`, `object-fit: contain` |
| Submit button | A login glyph, before the label | `16px` |
| Sign-on button | A shield-lock glyph, before the label | `16px` |
| Password toggle | An eye glyph when hidden, an eye-off glyph when shown | `16px` |

- **The toggle swaps between two glyphs.** It does not stay on one icon and change color.
- **The logo is the project's one logo asset**, with a dark variant where the mark would vanish on a dark canvas, per [[darkmode.component.md]].

## Layout Values

The few values HeroUI does not decide, fixed for this screen:

| Element | Value |
| :- | :- |
| Card width | Capped at `412px`; never widened to fill a desktop viewport |
| Wrapper | Full `100svh`, centered, `bg-background`, `24px` padding |
| Brand row | Logo `44px`, `12px` gap, `24px` below |
| Heading | `700`, `22px` |
| Field spacing | HeroUI's `Form` gap, `16px` |
| Submit and sign-on buttons | Full width |

- **The card is a leaf surface.** It holds fields and buttons, never another card, per [[card.component.md]].
- **The canvas is plain**: no gradient and no decorative shape. Color on this screen appears on the primary button.

## Fields

Login is by **the identity key and a password against the identity source**, never by an account the app creates itself, per [[auth.rules.md]].

| Field | Rules |
| :- | :- |
| Identifier | `type="text"` with `inputmode="numeric"` where the key is numeric, so a mobile keypad opens without losing a leading zero. `autocomplete="username"`. `required`. The placeholder shows a real *shape*, never a real value |
| Password | `autocomplete="current-password"`. Required. Always with the show and hide toggle |

- **Every field is a HeroUI `TextField` with its `Label`**, which links the two. A label that is only visually next to its input is not linked to it.
- **Trim the identifier before sending it, and never trim the password.**
- The password field must have the show and hide toggle. Relying on the browser's own is not a substitute, because it does not exist in every browser.
- The toggle is a `Button` with `isIconOnly`, never the submit, and its `aria-label` changes with the state.
- Do not add a field this standard does not list, and do not reorder the two that exist.

## Copy

All text follows the capitalization rule in [[uix.component.md]]: Title Case for anything that names a thing, sentence case for anything that reads as prose. The language is the project's UI language, per [[prd.rules.md]].

| Slot | String |
| :- | :- |
| Heading | `Sign In` |
| Description | One sentence naming the system |
| Identifier label | The name of the key, in the words users know it by |
| Password label | `Password` |
| Password placeholder | `Enter your password` |
| Submit, idle | `Sign In` |
| Submit, in flight | `Signing in...` |
| Divider | `or` |
| Sign-on button | `Single Sign-On` |
| Footer hint | Where to go for help |

An acronym keeps its casing. **The in-flight label ends in three periods, not the single-character ellipsis**, per [[loading.component.md]].

## Errors

Map every backend error code to one sentence that names the next step. Never print a raw backend message, a status code, or a stack trace.

| Condition | Message |
| :- | :- |
| Wrong identifier or password | The credentials are not correct. Check them and try again |
| Too many attempts | Too many sign-in attempts. Wait a few minutes and try again |
| Account is inactive | This account is no longer active. Contact the team that manages access |
| Signed in but not entitled to this app | Name the owner of the access, so the user knows who to ask |
| Server error, 500 and above | The server is having a problem. Try again shortly |
| No response at all | The server cannot be reached. Check the connection and try again |

> [!danger]
> Never reveal which half of the credential was wrong. One message covers both. This is a security requirement, not a copy preference, and it outranks any request to be more helpful here.

- The error is a HeroUI `Alert` above the fields, announced once.
- **Clear the password field after a failed attempt and leave the identifier in place**, so a retype is one field, not two.
- **A session that expired is a notice, not an error.** Render it in the same slot with `role="status"`, only when there is no real error to show.

## Loading

The login screen carries two loading states, both defined in [[loading.component.md]]:

- While the session is being checked on first paint, **the route shows the full page gate, not the form**. This is what stops the form flashing at a user who is already signed in.
- While a submit is in flight, the submit button carries `isPending` and its label changes. The form stays visible and keeps what the user typed, and the button width does not change.

## The Single Sign-On Block

> [!warning]
> The sign-on button appears only when the project actually has an identity provider configured. **A dead button on the login screen is never acceptable**, and neither is a disabled one.

- Read the flag from the backend where the project can change it without a rebuild; a build-time variable is acceptable where it cannot. Either way, [[secret.rules.md]] applies: a login URL is configuration, not a secret.
- **The block is hidden in full, divider included.**
- Pass the current origin as the return-to value, so the provider can return the user to where they started, and validate that target against an allowlist per [[security.rules.md]].
- The sign-on button is `variant="secondary"` and full width. It never becomes the primary button, because the credential path is the primary one.

## Security

These rank above everything else here, and [[auth.rules.md]] and [[security.rules.md]] own them in full.

- **Authenticate against the identity source.** A project must not keep its own user table for login.
- **The session is an `HttpOnly` cookie set by the backend.** No token is ever written to JavaScript, `localStorage`, or `sessionStorage`, and no token appears in a URL.
- Never log, echo, or send the password anywhere except the login request itself.
- **Never prefill an identifier or a password, and never ship a default or example credential in the placeholder.** The placeholder shows a shape, not a real value.
- Rate limiting is the backend's job. The form's job is to report it with the message above, not to retry on its own.
- Keep `autocomplete="current-password"` so the browser's password manager works. Disabling it pushes users toward weaker passwords.

## Accessibility

- The card holds a HeroUI `Form`, the submit is `type="submit"`, and Enter submits from either field.
- Every input has a linked label. The show and hide toggle carries an `aria-label` stating what it will do next.
- The error is announced as an alert; the expired-session notice is announced as a status.
- **Never remove HeroUI's focus ring**, on a field, a button, or the toggle.
- The submit button is at least 44px tall on mobile.
- The logo `img` has an empty `alt`, because the product name sits next to it in text and would otherwise be announced twice.

**An accessibility requirement outranks a reference implementation.** Where the source a project copies from lacks a label association or an `role="alert"`, the copy adds them and the source converges, rather than the copy reproducing the gap.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Build the screen from HeroUI's `Card`, `Form`, `TextField`, `Alert`, and `Button` | Hand-build a field, a toggle, or an error box |
| Keep the section order exactly as listed | Add a remember-me box, a social login, a registration link, or a reset form |
| Change only the product name and the one-line description | Redesign or rearrange the form for one project |
| Map every backend error code to one sentence that names the next step | Show a raw backend message, an error code, or an HTTP status |
| Use one message for a wrong identifier or a wrong password | Say which half of the credential was wrong |
| Hide the sign-on block in full when no provider is configured | Render a disabled or dead sign-on button |
| Keep the session in an `HttpOnly` cookie | Store a token in JavaScript, browser storage, or a URL |
| Cap the card at `412px` on a plain canvas | Widen the card, or put a gradient behind it |
| Let the screen follow the light and dark theme | Pin the login screen to one theme |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens, typography, spacing, shape, and elevation | Any value this file names but does not define, and any work outside the sign-in screen |
| [[button.component.md]] | HeroUI's seven variants | The primary button this screen stretches to full width |
| [[loading.component.md]] | The route gate and the button loading state | The two waits this screen carries |
| [[auth.rules.md]] | The identity key, the token, and the cookie | Why the session is an `HttpOnly` cookie and never browser storage |
| [[security.rules.md]] | Rate limiting, audit, and what a response may not reveal | Why every credential failure reads the same |
| [[secret.rules.md]] | What is a secret and what is configuration | Why a sign-on URL is configuration and safe to bake in |
| [[refresh.component.md]] | What survives a reload | Why the route gate runs before the redirect decision |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements, including [[security.rules.md]] and [[auth.rules.md]]
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This login standard
6. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements. If a request conflicts with this standard, tell the user which standard is affected before proceeding.

## Related

- [[uix.component.md]]
- [[button.component.md]]
- [[loading.component.md]]
- [[auth.rules.md]]
- [[security.rules.md]]
- [[secret.rules.md]]
- [[refresh.component.md]]
- [[docs.rules.md]]
