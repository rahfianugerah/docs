> Up: [[README.md]] · [[uix.component.md]]

# Login Standard

## Core Requirement

The sign-in screen is the first thing a user sees and the one screen where a mistake is most expensive. It follows this file everywhere.

This extends [[uix.component.md]] and uses its tokens. It defines no color and no font of its own.

## Structure

The screen is a centered card on a plain background, holding these parts in this order:

1. The product name, as text, per [[title.header.component.md]].
2. One line saying what this signs the user into, when it is not obvious.
3. The identifier field.
4. The password field, with a reveal toggle.
5. The submit button, full width.
6. An error region, which occupies no space until there is an error.
7. An optional federated sign-in block, below a divider.

Nothing else. No marketing copy, no feature list, no illustration carrying meaning, no link to anything but account recovery.

## Fields

- **The identifier field is whatever the system actually authenticates on**, and it is labelled with that word. Never label it "username" when the system wants an email.
- Set `autocomplete` correctly on both fields. Getting this wrong is why a password manager fails to fill, and a user who cannot autofill types a weaker password.
- Set `inputmode` and `type` to match the identifier, so a phone keyboard shows the right keys.
- **The password field has a reveal toggle**, and the toggle is a `button` with an accessible name that changes with its state.
- Never impose a maximum length below what the hash accepts, and never strip characters from a password. Both silently break a correct password.
- Autofocus the identifier field on load, and only there.

## Copy

- The button says what happens: sign in. Never "submit".
- Say nothing that reveals whether an account exists.
- Keep every string in one place, because this screen gets translated first.

## Errors

**One message for every authentication failure**, identical in wording and in timing:

- The same text whether the identifier is unknown, the password is wrong, or the account is disabled. A different message for each is an account enumeration oracle, per [[security.rules.md]].
- The message appears in the error region above the button, not as a toast that disappears before it is read.
- Distinguish only what the user can act on: a network failure and a rate limit are different from a credential failure and may say so.
- **A validation error is not an authentication error.** An empty field is caught client-side and says which field, before any request is sent.
- Clear the error when the user edits either field.

## Loading

The submit button follows [[loading.component.md]]: disabled while in flight, stable width, re-enabled on both success and failure.

**Never leave the button disabled after a failed attempt.** The user is on a form they must be able to resubmit.

## Federated Sign-In Block

When the product offers an external identity provider, it sits below a divider, under the primary form.

- The primary credential form stays first. A federated button placed above it retrains users to click the wrong thing.
- Each provider is one button with that provider's name.
- A failed federated sign-in returns to this screen with an error in the same region, never to a blank page or a provider error page.

## Security

Everything here is presentation. The controls live on the server, per [[security.rules.md]].

- **Never store a token in `localStorage`** where a cookie will do, and never store a password anywhere at all.
- Never log the identifier or the password, not even at debug level, per [[repository.rules.md]].
- Never put a credential in a URL, a query parameter, or a redirect.
- Rate limiting and lockout are enforced server-side. A client-side attempt counter is not a control.
- Redirect to the originally requested page after signing in, and validate that path is internal. An unvalidated redirect target is an open redirect.
- The whole screen is served over TLS, or it is not served.

## Accessibility

- The card is a `form` and submits on `Enter` from either field.
- Every field has a real `label`, not a placeholder standing in for one.
- The error region is a live region, so the failure is announced rather than only seen.
- The error is associated with the form through `aria-describedby`.
- Focus moves to the error region when an attempt fails, so a screen reader user is told why nothing happened.
- Never rely on color alone to mark a field as invalid.

## Do and Do Not

Do:

- Use one identical message for every authentication failure.
- Set `autocomplete` so password managers work.
- Give the password field a reveal toggle that is a real button.
- Validate the post-login redirect target is internal.
- Keep the credential form above any federated block.

Do not:

- Say whether the account exists.
- Cap or strip password characters.
- Log a credential at any level.
- Leave the button disabled after a failure.
- Put marketing content on this screen.

## Related

- [[uix.component.md]]
- [[loading.component.md]]
- [[title.header.component.md]]
- [[refresh.component.md]]
- [[security.rules.md]]
