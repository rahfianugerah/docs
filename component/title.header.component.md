> Up: [[README.md]] · [[uix.component.md]]

# Title and Header Standard

## Core Requirement

The product name is written as text, in one form, in every place it appears.

A name that reads three ways across a product is three products to a user who is only trying to work out which one they are in.

This extends [[uix.component.md]] and uses its tokens.

## The Form

- **One canonical spelling**, including its capitalization, decided once and used verbatim.
- It is text, not an image. A name rendered as an image cannot be selected, searched, translated, or read by a screen reader, and it blurs on a display it was not exported for.
- A logo may sit beside the name. It never replaces it.
- Never abbreviate it in one place and spell it out in another.

## Where the Name Appears

| Place | Shows |
| :- | :- |
| Browser tab | The page, then a separator, then the product name |
| Sidebar brand block | The product name |
| Sign-in screen | The product name |
| Page heading | The page name, never the product name |

The document title is the only place the two are combined, and the page comes first, because a tab is truncated from the right and the user has several open.

## The Title Never Changes With the Route

**The product name in the interface is constant.** Only the document title changes as the user navigates.

A brand block that swaps to the current section's name turns the one fixed landmark on the screen into another moving part. The user then has nothing to confirm which product they are in, which matters most in an ecosystem of products that share a design system.

The page name belongs in the page heading, where the content is, per the heading rules in [[uix.component.md]].

## The Name Is Not Configuration

**Never read the product name from an environment variable.**

- A misconfigured deployment then renders with a blank or wrong name, and the failure is invisible in review because it only appears in that environment.
- It gives the impression the name is meant to vary per deployment, and someone eventually varies it.
- It is not a secret and it is not per-environment, so it fails the test in [[secret.rules.md]] for what belongs in configuration at all.

The name is a constant in the source, in one module, imported everywhere.

## Environments

A non-production environment marks itself with a badge beside the name, never by changing the name.

- The badge says which environment, in the token for a cautionary state.
- Production carries no badge at all. An absent badge means production, and that is the only signal that cannot be mistaken.
- A user must be able to tell, at a glance, that they are about to act on real data.

## Accessibility

- The brand block is a link to the default route, with an accessible name that is the product name.
- Every page has exactly one `h1`, and it is the page name.
- The document title is updated on navigation, so history and open tabs are distinguishable.
- Where the name appears beside a logo, the logo is decorative and hidden from assistive technology, because the text already carries the name.

## Do and Do Not

Do:

- Write the name as text, in one spelling, from one constant.
- Put the page first in the document title.
- Mark a non-production environment with a badge.
- Keep exactly one `h1` per page.

Do not:

- Render the name as an image.
- Change the interface name with the route.
- Read the name from an environment variable.
- Badge production.
- Abbreviate the name in some places only.

## Related

- [[uix.component.md]]
- [[sidebar.component.md]]
- [[login.component.md]]
- [[secret.rules.md]]
