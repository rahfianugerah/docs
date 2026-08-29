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

This standard extends [[uix.component.md]]. It does not redefine the token set; every color, radius, and shadow used here is already defined in that file's `:root` block.

A new project copies this markup and this CSS. It does not rebuild an equivalent, it does not substitute its own icon set, and it does not adjust a size to suit its own module. Every pixel value is fixed by the "Sizing Reference" table below.

## Required Structure

The form is a single centered card on a clean background. Build it in this order, with these classes:

1. `div.login-wrap`, holding one `form.login-card`. **The form element is the card itself**, so pressing Enter in any field submits.
2. `div.lg`: the logo asset at 44 by 44, then `div.nm` with the product name and `div.by` with the organization line.
3. `h1` reading the sign-in heading, then `p.sub` naming what the user is signing into.
4. `div.login-err`, rendered only when there is something to say.
5. `div.field` for the identifier.
6. `div.field` for the password, with the input inside `div.pwd-wrap` and a `button.pwd-toggle` for show and hide.
7. `button.btn.pri`, full width, carrying the sign-in label.
8. The single sign-on block, rendered only when one is configured: `div.login-or` reading the divider word, then a full width `.btn.sso`.
9. `p.hint`, centered, telling the user where to get help.

**Do not add a section this list does not contain.** A login screen has no remember-me box, no social sign-in, no self-service registration, and no marketing copy, because access is granted by the identity source and not by the app.

Reference markup:

```html
<div class="login-wrap">
  <form class="login-card">
    <div class="lg">
      <img src="/logo.png" alt="" width="44" height="44" />
      <div>
        <div class="nm">Product Name</div>
        <div class="by">by Organization</div>
      </div>
    </div>
    <h1>Sign In</h1>
    <p class="sub">Use your work account to reach the system.</p>

    <!-- rendered only when there is an error -->
    <div class="login-err" role="alert">...</div>

    <div class="field">
      <label for="userid">User ID</label>
      <input id="userid" type="text" inputmode="numeric"
             autocomplete="username" placeholder="Example: 20230101" required />
    </div>

    <div class="field">
      <label for="password">Password</label>
      <div class="pwd-wrap">
        <input id="password" type="password" autocomplete="current-password"
               placeholder="Enter your password" required />
        <button type="button" class="pwd-toggle" aria-label="Show password" title="Show password">
          <i class="ti ti-eye"></i>
        </button>
      </div>
    </div>

    <button class="btn pri" type="submit" style="width:100%;justify-content:center;margin-top:4px">
      <i class="ti ti-login"></i> Sign In
    </button>

    <!-- rendered only when single sign-on is configured -->
    <div class="login-or">or</div>
    <button type="button" class="btn sso"><i class="ti ti-shield-lock"></i>Single Sign-On</button>

    <p class="hint" style="margin-top:14px;text-align:center">
      Use the credentials your organization issued you.
    </p>
  </form>
</div>
```

The two inline styles are part of the reference and are kept: the submit button is stretched to full width and centered with a `4px` top margin, and the hint is centered with a `14px` top margin. They are layout values local to this one screen, which [[uix.component.md]] allows an inline style for; do not move them into a shared class and do not change them.

## Icons

Every icon here comes from the project's one icon set, per [[uix.component.md]].

| Element | Icon | Size | Color |
| :- | :- | :- | :- |
| Brand row | The logo asset, not an icon | `44px` by `44px`, `object-fit: contain` | The asset's own |
| Submit button | A login glyph, before the label | `16px`, from `.btn i` | White, inherited from `.btn.pri` |
| Sign-on button | A shield-lock glyph, before the label | `16px`, from `.btn i` | `var(--ink)`, inherited from `.btn` |
| Password toggle, hidden | An eye glyph | `16px`, set explicitly | `var(--ink3)` |
| Password toggle, shown | An eye-off glyph | `16px`, set explicitly | `var(--ink3)` |

- **Do not substitute an equivalent icon from another set.** One set per project, per [[uix.component.md]].
- **The toggle swaps between two glyphs.** It does not stay on one icon and change color, and it never uses a crossed-out variant from a different family.
- The sign-on button's icon sits directly against its label in the source; the `7px` gap on `.btn` provides the separation.
- **The logo is the project's one logo asset.** Never redraw the mark, and never substitute an icon glyph for it.

Nothing sets a font size on the password toggle's icon, so it would inherit the `14px` body size, below the 16 to 20px icon range [[uix.component.md]] sets. Set it explicitly:

```css
.pwd-toggle i { font-size: 16px; }
```

## Reference CSS

```css
.login-wrap{min-height:100vh;display:grid;place-items:center;padding:24px;background:var(--bg)}
.login-card{width:100%;max-width:412px;background:var(--surface);border:1px solid var(--line);
  border-radius:var(--r-sm);box-shadow:var(--shadow-pop);padding:32px}
.login-card .lg{display:flex;align-items:center;gap:12px;margin-bottom:24px}
.login-card .lg img{width:44px;height:44px;object-fit:contain;flex-shrink:0}
.login-card .lg .nm{font-weight:600;font-size:15px;line-height:1.25;letter-spacing:-.01em}
.login-card .lg .by{font-size:11.5px;font-weight:500;color:var(--ink3);margin-top:2px}
.login-card h1{font-size:22px;font-weight:700;letter-spacing:-.02em}
.login-card p.sub{color:var(--ink2);font-size:13.5px;margin:6px 0 24px}
.pwd-wrap{position:relative}
.pwd-wrap input{padding-right:44px}
.pwd-toggle{position:absolute;top:50%;right:6px;transform:translateY(-50%);width:32px;height:32px;
  border:none;background:none;border-radius:50%;color:var(--ink3);cursor:pointer;
  display:grid;place-items:center}
.pwd-toggle:hover{color:var(--ink2);background:var(--line2)}
.pwd-toggle:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.pwd-toggle i{font-size:16px}
.login-err{background:var(--bad-soft);color:var(--bad-tua);border:1px solid var(--bad);
  font-size:12.5px;font-weight:500;padding:9px 12px;border-radius:var(--r-sm);margin-bottom:14px}
.login-or{display:flex;align-items:center;gap:10px;margin:16px 0;color:var(--ink3);
  font-size:12px;text-transform:uppercase;letter-spacing:.04em}
.login-or::before,.login-or::after{content:"";flex:1;height:1px;background:var(--line)}
.btn.sso{width:100%;justify-content:center}
@media(max-width:900px){ .login-card{padding:24px} }
```

The form controls are not restyled by the login block. They come from the shared `.field` and `.btn` classes that apply everywhere, reproduced here so the whole screen can be checked against one page:

```css
.field{margin-bottom:14px}
.field label{display:block;font-size:12.5px;font-weight:600;color:var(--ink2);margin-bottom:6px}
.field input{width:100%;border:1px solid var(--line);border-radius:var(--r-sm);padding:9px 12px;
  font-size:13.5px;font-family:inherit;outline:none;background:var(--surface);box-sizing:border-box}
.field input:focus{border-color:var(--accent)}
.btn{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:var(--surface);
  color:var(--ink);font-weight:600;font-size:13px;padding:9px 14px;border-radius:var(--r-sm);
  cursor:pointer;font-family:inherit}
.btn:hover{background:var(--line2)}
.btn:disabled{opacity:.55;cursor:default}
.btn.pri{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.pri:hover{background:var(--accent-tua)}
.btn i{font-size:16px}
.hint{font-size:11.5px;color:var(--ink3);margin-top:5px}
```

## Typography on This Screen

The login card uses the same one family as every other screen, per [[uix.component.md]]. There is no display face here and no second family anywhere in the project.

Where a project does carry a brand display face for a lockup, **set the family on the wrapper, never on the elements inside it.** Declaring it on the product name alone leaves the organization line in the interface face, and the mismatch is invisible until the two lines are read together. On this screen that would mean `.login-card`, so the heading, the description, the field labels, the button, and the footer hint all inherit it without one of them being missed.

## Sizing Reference

Every size on this screen is fixed. Do not round one to a neater number, and do not scale one to suit a longer product name.

| Element | Property | Value |
| :- | :- | :- |
| `.login-wrap` | Min height, padding, background | `100vh`, `24px`, `var(--bg)` |
| `.login-card` | Max width | `412px` |
| `.login-card` | Padding | `32px`, dropping to `24px` below 900px |
| `.login-card` | Border radius | `var(--r-sm)` |
| `.login-card` | Border, shadow | `1px solid var(--line)`, `var(--shadow-pop)` |
| `.lg` | Gap, bottom margin | `12px`, `24px` |
| `.lg img` | Size, fit | `44px` by `44px`, `object-fit: contain` |
| `.lg .nm` | Font | `600`, `15px`, line height `1.25`, letter spacing `-.01em` |
| `.lg .by` | Font, color, top margin | `500`, `11.5px`, `var(--ink3)`, `2px` |
| `h1` | Font | `700`, `22px`, letter spacing `-.02em` |
| `p.sub` | Font, color, margin | `13.5px`, `var(--ink2)`, `6px 0 24px` |
| `.login-err` | Font, padding, radius, bottom margin | `500` `12.5px`, `9px 12px`, `var(--r-sm)`, `14px` |
| `.field` | Bottom margin | `14px` |
| `.field label` | Font, color, bottom margin | `600` `12.5px`, `var(--ink2)`, `6px` |
| `.field input` | Padding, font, radius | `9px 12px`, `13.5px`, `var(--r-sm)` |
| `.field input:focus` | Border | `var(--accent)`, and no ring |
| `.pwd-wrap input` | Right padding | `44px`, clearing the toggle |
| `.pwd-toggle` | Size, offset, radius | `32px` by `32px`, `right: 6px`, `50%` |
| `.pwd-toggle i` | Font size | `16px`, set explicitly |
| `.btn` | Padding, font, gap, radius | `9px 14px`, `600` `13px`, `7px`, `var(--r-sm)` |
| `.btn i` | Font size | `16px` |
| `.btn:disabled` | Opacity | `.55` |
| Submit button | Width, top margin | `100%`, `4px` |
| `.login-or` | Font, gap, margin | `12px` uppercase, letter spacing `.04em`, gap `10px`, margin `16px 0` |
| `.btn.sso` | Width | `100%`, centered |
| `.hint` | Font, color, top margin | `11.5px`, `var(--ink3)`, `14px` on this screen |

Notes on values that look like exceptions and are not:

- **The card carries `--r-sm`, not `--r`.** It contains fields and buttons, not other cards, so it is a leaf surface under the radius rule in [[uix.component.md]]. What separates it from the page is its shadow and its width, not its curve.
- The card is capped at `412px` and drops to `24px` padding below the single 900px breakpoint. **Do not widen it to fill a desktop viewport.**
- The background is plain, with no gradient and no decorative shapes, even though [[uix.component.md]] permits a gradient on a login backdrop. Color on this screen appears on the primary button. Keep it that way.

## Fields

Login is by **the identity key and a password against the identity source**, never by an account the app creates itself, per [[auth.rules.md]].

| Field | Rules |
| :- | :- |
| Identifier | `type="text"` with `inputmode="numeric"` where the key is numeric, so a mobile keypad opens without losing a leading zero. `autocomplete="username"`. `required`. The placeholder shows a real *shape*, never a real value |
| Password | `autocomplete="current-password"`. `required`. Always inside `.pwd-wrap` with a `.pwd-toggle` |

- **Every input carries an `id` and every label a matching `for`.** A label that is only visually next to its input is not linked to it.
- **Trim the identifier before sending it, and never trim the password.**
- The password field must have the show and hide toggle. Relying on the browser's own is not a substitute, because it does not exist in every browser.
- The toggle is `type="button"`, so it never submits the form, and its `aria-label` and `title` change with the state.
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

- The error sits in `.login-err` above the fields, carries `role="alert"`, and is announced once.
- **Clear the password field after a failed attempt and leave the identifier in place**, so a retype is one field, not two.
- **A session that expired is a notice, not an error.** Render it in the same slot with `role="status"`, only when there is no real error to show.

## Loading

The login screen carries two loading states, both defined in [[loading.component.md]]:

- While the session is being checked on first paint, **the route shows the full page gate, not the form**. This is what stops the form flashing at a user who is already signed in.
- While a submit is in flight, the submit button is disabled and its label changes. The form stays visible and keeps what the user typed, and the button width does not change.

## The Single Sign-On Block

> [!warning]
> The sign-on button appears only when the project actually has an identity provider configured. **A dead button on the login screen is never acceptable**, and neither is a disabled one.

- Read the flag from the backend where the project can change it without a rebuild; a build-time variable is acceptable where it cannot. Either way, [[secret.rules.md]] applies: a login URL is configuration, not a secret.
- **The block is hidden in full, divider included.**
- Pass the current origin as the return-to value, so the provider can return the user to where they started, and validate that target against an allowlist per [[security.rules.md]].
- The sign-on button is the secondary style and full width. It never becomes the primary button, because the credential path is the primary one.

## Security

These rank above everything else here, and [[auth.rules.md]] and [[security.rules.md]] own them in full.

- **Authenticate against the identity source.** A project must not keep its own user table for login.
- **The session is an `HttpOnly` cookie set by the backend.** No token is ever written to JavaScript, `localStorage`, or `sessionStorage`, and no token appears in a URL.
- Never log, echo, or send the password anywhere except the login request itself.
- **Never prefill an identifier or a password, and never ship a default or example credential in the placeholder.** The placeholder shows a shape, not a real value.
- Rate limiting is the backend's job. The form's job is to report it with the message above, not to retry on its own.
- Keep `autocomplete="current-password"` so the browser's password manager works. Disabling it pushes users toward weaker passwords.

## Accessibility

- The card is a real `form`, the submit is `type="submit"`, and Enter submits from either field.
- Every input has a linked label. The show and hide toggle carries an `aria-label` stating what it will do next.
- The error carries `role="alert"`; the expired-session notice carries `role="status"`.
- **Never remove the focus ring.** `.pwd-toggle` defines its own `:focus-visible` outline because it has no border of its own.
- The submit button is at least 44px tall on mobile.
- The logo `img` has an empty `alt`, because the product name sits next to it in text and would otherwise be announced twice.

**An accessibility requirement outranks a reference implementation.** Where the source a project copies from lacks a label association or an `role="alert"`, the copy adds them and the source converges, rather than the copy reproducing the gap.

## Do and Do Not

Do:

- Copy the form and the CSS as is, and change only the product name and the one-line description.
- Keep every value in the Sizing Reference table exactly as written.
- Keep the order of the sections exactly as listed.
- Map every backend error code to one sentence that names the next step.
- Hide the sign-on block in full when no provider is configured.
- Keep the login card plain, with color only on the primary button.

Do not:

- Redesign, restyle, or rearrange the login form for one project.
- Add a remember-me box, a social login, a registration link, or a password reset form.
- Say which half of the credential was wrong.
- Show a raw backend message, an error code, or an HTTP status to the user.
- Store a token in JavaScript, browser storage, or a URL.
- Widen the card, remove its shadow, or give it a radius that is not `--r-sm`.
- Render a disabled or dead sign-on button.
- Substitute an icon from a second set.
- Round, scale, or tidy a value in the Sizing Reference table, including to fit a longer product name.
- Move the inline layout styles into a shared class, or change their values.

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The tokens, typography, spacing, shape, and elevation | Any value this file names but does not define, and any work outside the sign-in screen |
| [[button.component.md]] | The six variants | The primary button this screen stretches to full width |
| [[loading.component.md]] | The route gate and the button loading state | The two waits this screen carries |
| [[auth.rules.md]] | The identity key, the token, and the cookie | Why the session is an `HttpOnly` cookie and never browser storage |
| [[security.rules.md]] | Rate limiting, audit, and what a response may not reveal | Why every credential failure reads the same |
| [[secret.rules.md]] | What is a secret and what is configuration | Why a sign-on URL is configuration and safe to bake in |
| [[refresh.component.md]] | What survives a reload | Why the route gate runs before the redirect decision |

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

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
