> Up: [[README.md]] · [[uix.component.md]]

# Refresh and State Standard

> [!note]
> State that survives a reload: the URL as the source of truth, the SPA fallback, and the session gate.

## Core Requirement

**A refresh returns the user to exactly where they were.** Pressing F5, hitting reload, restoring a closed tab, or opening a bookmark lands on the same page, with the same tab, the same filters, and the same record open.

A refresh never drops the user on the home page, never shows a login screen to someone whose session is still valid, and never quietly clears what they had narrowed down.

This is not polish. Someone who refreshes a filtered report and lands on the dashboard has to rebuild the whole view by hand, and the reasonable conclusion is that the app lost their work.

This policy extends [[uix.component.md]]. Read it whenever the work touches routing, a filter, a tab, or anything a user can get back to by typing a URL.

## The URL Is the State

**If it is not in the URL, it does not survive a refresh.** Everything else in this file follows from that one line.

The browser already has a place to store where the user is, and it is shared by the address bar, the back button, a bookmark, and a link pasted to a colleague. Anything held only in component state is gone the moment the page reloads.

| State | Where it goes | Example |
| :- | :- | :- |
| The page | Path | `/reports` |
| The record being viewed | Path | `/reports/1042` |
| The active tab | Query | `?tab=summary` |
| A search query | Query | `?q=invoice` |
| Every filter | Query | `?status=open&owner=3` |
| Page number and size | Query | `?page=4&size=50` |
| Sort column and direction | Query | `?sort=name&dir=asc` |

Rules:

- **Write with a replace, not a push,** while a value is still changing. A search box that pushes per keystroke turns the back button into an undo log; one that replaces leaves back meaning "the previous page".
- **Read the initial state from the URL on mount.** Do not initialise from a default and then write the URL, which discards whatever the user opened.
- **Omit a parameter at its default.** `?page=1&dir=asc` on every page is noise in a shared link.
- **Keep parameter names stable and readable.** They become part of the app's public surface the moment somebody bookmarks one.
- Use the platform `URLSearchParams` rather than hand-parsing, so encoding is handled and a value containing `&` does not break the next parameter.

## Never Restore From Storage

- **Never store the current route in `localStorage` and redirect to it on boot.** It fights the back button, it breaks every deep link, and it sends a person who clicked your link to whatever page *they* last had open. The URL is already the store.
- Never restore a page from a server-side "last visited" field, for the same reason.
- Never put application state in a hash fragment that a query parameter should hold.
- Never rely on `sessionStorage` for anything a user should be able to bookmark or share.

## The Three Things That Break a Refresh

All three are **refresh-only** failures. Clicking around the app never triggers them, which is exactly why they survive testing and reach production.

### 1. The Server Must Serve the App on Every Path

A single-page app has one HTML file. When the browser asks the server for `/reports/1042` directly, the server must return that HTML and let the client router take over. Without it, a refresh on any route except `/` returns 404.

```nginx
# nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

```apache
# Apache
FallbackResource /index.html
```

Most hosts have a "single-page app" or "rewrite all to index.html" switch; it is the same thing. Keep static assets on a rule that 404s properly, so a missing file is a missing file rather than a copy of the HTML served with a JavaScript content type, which fails much later and much more confusingly.

### 2. The Auth Check Must Finish Before Any Redirect

On a refresh the app boots knowing nothing about the user until the session is checked. **A guard that redirects while that check is still in flight sends a signed-in user to the login screen on every single refresh.**

Session state has three values, not two: `loading`, `authenticated`, `anonymous`.

- While `loading`, render a hold: a spinner or a skeleton. Not the login screen, not the protected page.
- Decide the redirect only once the check has **settled**. Never on the not-yet-known state.
- Apply the same hold on the login route, so an already-signed-in user refreshing there is not shown a login form before being bounced away.

Treating `loading` as `anonymous` is the single most common cause of "it logs me out when I refresh".

### 3. The Catch-All Route Must Be Last and Rare

Most routers end with a catch-all that redirects unknown paths home. That is correct for a genuinely unknown path, and it is also the most common way a refresh silently sends someone to the dashboard: **a page that exists in the app but was never registered in the router matches the catch-all instead.**

- Keep the catch-all last, after every real route.
- Register the route in the same change that adds the page.
- Prefer a real "not found" page over a silent redirect. A mistyped URL should say so, not pretend the user asked for the home page.

## After a Login Redirect, Return to the Attempted Page

When a session has genuinely expired, the user goes to the login screen and, after signing in, returns to **the page they were trying to reach**.

- Carry the attempted location through the redirect, in router state or a `?next=` parameter.
- **Preserve the query string with the path**, or the user lands on an unfiltered version of the page they asked for.
- **Validate the target before redirecting to it.** Accept only a same-origin relative path. An unchecked `?next=` is an open redirect, and it is a phishing vector, per [[security.rules.md]].

## What Survives and What Does Not

| State | Survives | Why |
| :- | :- | :- |
| Page, record, tab, filters, search, sort, pagination | Yes | It is in the URL |
| Which navigation group is expanded | Yes | Derive it from the current route |
| The session | Yes | It is a cookie or a token, not component state |
| A detail panel that is a real destination | Yes, once it has a URL | Give it a path or a query parameter |
| A confirmation dialog, a toast, a transient sheet | No, and it must not | Re-showing a confirmation nobody asked for is worse than losing it |
| Unsaved form input | No | See below |

Give a modal a URL when it is **a place the user can be**, such as a record detail. Leave it out of the URL when it is a momentary interruption.

## Unsaved Input

A refresh loses what is typed and not submitted. That is expected; the fix is a warning, not silent persistence.

- Warn with `beforeunload` **only while the form is genuinely dirty**, and remove the handler the moment it is saved or reset. A page that always warns trains people to dismiss the warning.
- **Never silently mirror form input into `localStorage`.** It is an unaudited store of whatever the user typed, it goes stale against the record, and on many forms it is personal data, per [[security.rules.md]].
- A long form that genuinely must survive is saved as a draft through the API, deliberately and visibly, not as a side effect of typing.

## Scroll Position

- Going back restores the previous scroll position. The browser does this; do not defeat it.
- A new navigation starts at the top.
- A refresh restores the browser's own scroll position. **Do not force a scroll to top on mount**, which undoes it.
- Most routers expose a scroll restoration setting. Configure it once rather than scattering scroll calls through components.

## Definition of Done

Verify by actually doing it, not by reasoning about it:

- Open a page, apply filters, switch tab, press refresh. The same view comes back.
- Copy the URL into a new tab. It opens the same view.
- Refresh while signed in. The login screen never appears.
- Refresh on a deep route such as `/reports/1042`. It loads, rather than 404 or the home page.
- Sign out, open a deep link, sign in. You land on the deep link, with its query string intact.
- Change a filter, then press back. It goes to the previous page, not through every keystroke.

## Do and Do Not

Do:

- Put the page, record, tab, search, filters, sort, and pagination in the URL.
- Read initial state from the URL on mount.
- Treat session state as three values, and hold the route while it loads.
- Configure the server to serve the app on every path.
- Register a route in the same change that adds the page.
- Validate a redirect target as a same-origin relative path.

Do not:

- Store the route in `localStorage` and restore it on boot.
- Redirect on a session state that has not settled.
- Push a history entry per keystroke.
- Force a scroll to top on mount.
- Mirror form input into `localStorage`.
- Let the catch-all route absorb a page that was simply never registered.

## Related

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[calendar.component.md]]
- [[security.rules.md]]
