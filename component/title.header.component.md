---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]] · [[uix.component.md]]

# Title and Header Standard

> [!note]
> The product name: one form, from one constant, on every surface it appears. It is never read from configuration.

## Core Requirement

**The product name is written as text, in one form, in every place it appears.**

A name that reads three ways across a product is three products to a user who is only trying to work out which one they are in. Where several products share one design system, the name is also the only thing telling them apart.

This extends [[uix.component.md]] and uses its tokens.

## The Form

- **One canonical spelling**, including its capitalization, decided once and used verbatim.
- **It is text, not an image.** A name rendered as an image cannot be selected, searched, translated, or read by a screen reader, and it blurs on a display it was not exported for.
- A logo may sit beside the name. **It never replaces it.**
- **Never abbreviate it in one place and spell it out in another.**
- Where the product belongs to a family, the name is derivable: know the scope, know the name. Two words is the working shape, a family word and a scope word, and the same casing rule applies to both every time.
- **An acronym stays uppercase**, in the name and everywhere else. A word is Title Case.
- The name is the same in every language. It is a proper noun and is not translated, per the capitalization rule in [[uix.component.md]].

Forbidden, with the reason each one gets tried:

| Not this | Why it is wrong |
| :- | :- |
| `Ops Control - Acme Group` | A descriptor and a company suffix. The app has a name; that is not it |
| `Legal Module` | "Module" is an implementation detail, not part of the name |
| `Legal - Contract Management` | A tagline. It belongs in the page description, not the name |
| `Legal` | Drops the family. Says nothing about which system it belongs to |
| `Acme legal`, `ACME Legal` where the family is `Acme` | Wrong casing on one of the two words |
| `Legal v2`, `Legal (Beta)` | A version or a state. It changes; the name does not |
| `Legal Dev`, `Legal Staging` | An environment. See "Environments" below |
| `Bluebird` | An internal codename. Nobody outside the project knows what it refers to |

## Where the Name Appears

**The same string in all five places. One constant per project, referenced everywhere, never retyped.**

| Surface | Where | Owned by |
| :- | :- | :- |
| Sign-in brand row | The brand block on the login card | [[login.component.md]] |
| Sidebar brand block | The brand block at the top of the rail | [[sidebar.component.md]] |
| Browser tab | The `<title>` element | This file |
| PWA manifest | `name` and `short_name` | [[pwa.rules.md]] |
| Exported document heading | The header of a generated PDF or spreadsheet | This file |

- **Define it once.** One constant, imported wherever the name is shown. Five hardcoded copies drift, and the login screen ends up disagreeing with the browser tab.
- **An organization line is a separate line, not part of the name.** It sits under the name in `--ink3` at a smaller size. It is never appended to the title, never joined with a dash, and never put in the `<title>` tag.
- **The PWA `short_name` is still the full name** where it fits. Twelve characters is well inside the limit. Do not abbreviate it.
- **The page heading is the page name, never the product name.** The product name is already on screen in the brand block.

## The Interface Name Never Changes With the Route

**The product name in the interface is constant.** A brand block that swaps to the current section's name turns the one fixed landmark on the screen into another moving part. The user then has nothing to confirm which product they are in, which matters most in an ecosystem of products that share a design system.

The page name belongs in the page heading, the breadcrumb, and the active sidebar row. Those three already tell the user where they are.

### The Document Title Is a Deliberate Choice

The `<title>` element is the one place the two can be combined, and there are two defensible settings. **Pick one per project and write it in the README.**

**Default: the page, then a separator, then the product name.** `Contracts · Legal`. The page comes first because a tab is truncated from the right and the user has several open. History entries and open tabs stay distinguishable, which is an accessibility benefit and the convention on the web.

**The alternative: a constant title, the bare product name on every page.** This suits an internal console behind a login, where there is no search engine reading the metadata and no link preview to render, so the two reasons a public site varies its title do not apply. What it buys is that a screenshot, a tab, and a history entry all say the same thing: which app this is. What it gives up is telling two tabs of the same app apart.

Whichever is chosen, these never change on a route change:

| Value | On a route change |
| :- | :- |
| The brand block in the interface | Unchanged, always |
| `<meta name="description">` | Unchanged |
| `og:title`, `og:description`, and every other Open Graph tag | Unchanged |
| `<link rel="canonical">` | Unchanged, or absent |
| The favicon | Unchanged |

- On the constant-title setting, **set the title once in the document and do not set it again from JavaScript.** Do not write an effect that sets it from the route; it is the most common way that rule gets broken, usually by someone being helpful.
- **Do not install a head-management library** for either setting. One assignment on navigation is not a problem that needs a dependency.

## The Name Is Not Configuration

**Never read the product name from an environment variable.**

- It is one deploy command away from a project that calls itself something else, in one environment only, with nothing failing and nobody noticing until a user reports a screenshot that says the wrong thing.
- A misconfigured deployment renders with a blank or wrong name, and the failure is invisible in review because it only appears in that environment.
- It gives the impression the name is meant to vary per deployment, and someone eventually varies it.
- It is not a secret and it is not per-environment, so it fails the test in [[secret.rules.md]] for what belongs in configuration at all.

**The name is a constant in the source, in one module, imported everywhere.** It changes through a commit, reviewed like anything else, not through a deploy flag.

## Environments

**A non-production environment is marked with a badge, never with the name.**

- The name stays the same in development, staging, and production.
- Where telling them apart matters, add a small chip beside the name in the sidebar or the topbar, reading the environment, in the token for a cautionary state, and render it only outside production.
- **Production carries no badge at all.** An absent badge means production, and that is the only signal that cannot be mistaken.
- A user must be able to tell, at a glance, that they are about to act on real data.
- Never `Product Staging`, never `[DEV] Product`, and never a different favicon colour standing in for a label nobody can read.

A name that varies by environment defeats the reason the name is fixed: a screenshot, a bug report, or a support message no longer identifies the product.

## Keeping an Audit

Where several products share this standard, keep a table of which ones comply and which have drifted, with the wrong value written out and the correction beside it.

**Fix a drifted name in every surface at once.** A half-renamed product is worse than a consistently wrong one, because the two names then both circulate.

## Accessibility

- The brand block is a link to the default route, with an accessible name that is the product name.
- **Every page has exactly one `h1`, and it is the page name.**
- Where the name appears beside a logo, the logo is decorative and hidden from assistive technology, because the text already carries the name.
- On the default title setting, the document title updates on navigation so history and open tabs are distinguishable.

## Do and Do Not

Do:

- Write the name as text, in one spelling, from one constant.
- Keep an acronym uppercase and a word in its established casing.
- Keep an organization line as a separate line beneath the name.
- Mark a non-production environment with a badge.
- Keep exactly one `h1` per page, and make it the page name.
- Write the document-title setting in the project README.

Do not:

- Add a descriptor, a tagline, a module word, or a company suffix to the name.
- Use a codename, a version, or an environment in the name.
- Render the name as an image.
- Change the interface name with the route.
- Read the name from an environment variable or any deploy-time value.
- Abbreviate the name in the PWA `short_name`, or in some places only.
- Hardcode the name in more than one place.
- Rename in one surface and not the others.
- Badge production.
- Change the description, an Open Graph tag, the canonical link, or the favicon on a route change.
- Install a head-management library for a one-line assignment.

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[uix.component.md]]
5. This title standard
6. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements.

## Related

- [[uix.component.md]]
- [[sidebar.component.md]]
- [[login.component.md]]
- [[pwa.rules.md]]
- [[secret.rules.md]]
- [[docs.rules.md]]
