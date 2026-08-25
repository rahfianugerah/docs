---
tags:
  - kind/rule
  - layer/frontend
---

> Up: [[README.md]]

# PWA Standard Policy

> [!note]
> The PWA layer of a frontend: the manifest, the icon set, and offline behavior.

## Core Requirement

When building, modifying, or reviewing the frontend of a project, you must follow the rules in this policy.

Every internal app must be installable as a Progressive Web App, so staff can use it from a phone without an app store, while the app stays a single web codebase.

## Required Components

| Component | Standard |
| :- | :- |
| `manifest.webmanifest` | Include `name`, `short_name`, `description`, `start_url`, `display: standalone`, `theme_color`, `background_color` |
| Icons | Provide 192x192 and 512x512 sizes, including a maskable icon. Keep the app icon consistent with the project's identity, per `uix.component.md` |
| Service worker | Generate through `vite-plugin-pwa`, per `stacks.rules.md`. Do not hand-write a service worker unless a specific need requires it |
| HTTPS | Required for a service worker to run. This is already satisfied by the nginx host, per `security.rules.md` |
| iOS support | Add an `apple-touch-icon` and the `apple-mobile-web-app-capable` meta tag, since Safari does not read the full manifest |

## Cache Strategy

| Source | Strategy |
| :- | :- |
| App shell (JS, CSS, fonts, icons) | Precache with a cache-first strategy, for a fast and offline-capable load |
| API calls (`/api/...`) | Network-first or network-only. Never cache-first. Stale business data is dangerous, for example an old balance or an old approval status shown as current |
| Offline fallback | Show a simple "you are offline" page when the app shell has not been cached yet |

- Configure service worker updates with `registerType: 'autoUpdate'` and show a prompt that a new version is available. Never leave a user stuck on an old version without knowing it.
- Never cache a response that contains personal data in the service worker cache, per `security.rules.md`.

## Deliberate Scope Limits

- Full offline operation is not a goal. These apps are data-driven. The PWA target is installability, speed, and a graceful degradation when offline, not working fully without a connection.
- Push notifications are out of scope for now. The notification channel is WhatsApp, plus an in-app action center. This design does not block adding Web Push in a later phase.

## Definition of Done

Before treating a PWA task as complete, confirm:

- The Lighthouse PWA category reports the app as installable, with a valid manifest, service worker, and icon set.
- The app can be added to the home screen on Android and iOS, and opens in standalone mode.
- API calls are never served cache-first, and an offline fallback exists.
- An app update is detected and prompts a reload, without requiring a manual cache clear.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This PWA policy
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[security.rules.md]]
- [[stacks.rules.md]]
- [[uix.component.md]]
