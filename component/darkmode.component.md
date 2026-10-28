---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
  - topic/accessibility
---

> Up: [[README.md]] · [[uix.component.md]]

# Dark Mode Standard

> [!important]
> Every project ships a light theme and a dark theme, both, from the first screen. One class on `<html>` switches every color at once, because every color reads a HeroUI theme variable.

## Core Requirement

**Light and dark are both required, in every project, on every screen.** A theme switch that leaves part of the app light, or a screen added later that only works in one theme, is a defect.

HeroUI makes this cheap. Its components read their colors from theme variables on the root element, and HeroUI ships a complete light theme and a complete dark theme. Switching is one class and one attribute on `<html>`; nothing else has to know which theme is active.

This standard owns only what changes when the theme flips. The variables themselves, the contrast floor, and every component rule stay in [[uix.component.md]] and its companions.

## How the Switch Works

HeroUI applies a theme from the root element. It responds to a class and to a `data-theme` attribute, and HeroUI's own controller sets both:

```html
<html lang="en" class="dark" data-theme="dark">
  <body class="bg-background text-foreground">
```

- **`bg-background` and `text-foreground` sit on the app shell**, so the page canvas changes with the theme and not only the components on it.
- **Keep the class and the attribute in sync.** HeroUI's controller writes both. Anything that writes only one leaves a selector matching the wrong theme.

## The Controller

**One controller per app.** Two controllers fight over `<html>` and the theme flickers between them.

| App | Controller |
| :- | :- |
| A Vite or other plain React app, the default stack | `useTheme("system")` from `@heroui/react` |
| A Next.js app, only where one is justified | `next-themes`, with `attribute="class"` |

HeroUI's `useTheme` stores the choice in `localStorage` under the key `heroui-theme`, resolves `"system"` from the operating system's preference, and writes both the class and `data-theme` to `<html>`.

**Three choices, and System is the default:**

- **Light** and **Dark** pin the theme.
- **System** follows the operating system, live, so a viewer whose machine switches at dusk gets the switch without touching the app.
- A choice the viewer never made is the system's choice, which is itself a choice the viewer made at the operating system level.

The theme is a per-viewer display preference. Keeping it in browser storage does not break the rule in [[refresh.component.md]] that page state lives in the URL, because a theme is not page state.

## No Flash on Load

`useTheme` runs after React mounts, so on its own the first paint is light and a dark-mode viewer sees a white flash on every load. **An inline script in `index.html` sets the theme before the first paint**, reading the same key the hook writes:

```html
<script>
  (() => {
    const saved = localStorage.getItem("heroui-theme") ?? "system";
    const dark = saved === "dark" || (saved === "system" && matchMedia("(prefers-color-scheme: dark)").matches);
    const theme = dark ? "dark" : "light";
    document.documentElement.classList.add(theme);
    document.documentElement.setAttribute("data-theme", theme);
  })();
</script>
```

- **It goes in `<head>`, inline, before any stylesheet.** An external file or a deferred script runs after the paint it was meant to prevent.
- **It reads `heroui-theme` and nothing else.** A second key is a second source of truth, and the two disagree on the first visit after a change.
- If a project ever changes the controller, it changes this script in the same commit.

## One Mechanism, Never Per-Element Variants

**Dark mode is the theme variables changing, and nothing else.** Never give a component its own dark color with a `dark:` variant or a per-component dark rule.

> [!failure]
> A dark mode built from per-element `dark:` classes has to be remembered on every element of every new screen, forever. One large app carried well over a thousand of them across dozens of files, and every screen that forgot rendered half light in the middle of a dark app. The fix was deleting all of them and letting the variables do the work.

That is only possible because the light theme is already disciplined:

- **Every color in every component reads a variable.** A hardcoded hex does not listen to the theme and stays light on a dark screen, per [[uix.component.md]].
- **Every translucent surface mixes from variables**, such as a skeleton shimmer built with `color-mix` over `--surface`. A fixed light grey is the one part of a dark screen that still glows.
- **Tailwind color utilities name a HeroUI variable**, such as `bg-surface` or `text-muted`, never a palette step such as `bg-gray-100`.

## Overriding a Color Per Theme

A project that changes a color overrides the HeroUI variable **once for each theme**, in two blocks, light first:

```css
.light, [data-theme="light"] {
  --accent: oklch(0.45 0.15 255);
  --accent-foreground: oklch(0.99 0 0);
}

.dark, [data-theme="dark"] {
  --accent: oklch(0.75 0.14 255);
  --accent-foreground: oklch(0.15 0 0);
}
```

> [!warning]
> Never override a color on a bare `:root`. HeroUI declares its themes inside a cascade layer, and an unlayered `:root` rule beats every layered rule, so the light value silently replaces the dark one too. The dark theme then shows a light-theme color that nobody checked against a dark surface.

- **The bright step of a hue is usually the right dark accent.** A color too light to read on white is often exactly right on a dark surface, and the dark accent is the lighter step, not the darker one.
- A value that is the same in both themes, such as the radius or the font, belongs on `:root`, per [[uix.component.md]]. Only colors are split.

## Native Controls Follow the Theme

Without `color-scheme`, the browser draws a scrollbar, a native date input, and an autofilled field light inside a dark app:

```css
@layer base {
  :root, .light, [data-theme="light"] { color-scheme: light; }
  .dark, [data-theme="dark"] { color-scheme: dark; }
}
```

## What Does Not Change With the Theme

| Kept | Why |
| :- | :- |
| The radius, the font, the spacing, and the 8px gap | Shape and type are not theme properties, per [[uix.component.md]] |
| A code block | It is dark in both themes, so a snippet reads the same wherever it is pasted |
| Print | The print stylesheet forces a white page and black text in both themes |

Everything else follows the theme, including the loading gate, the login screen, and every overlay. A screen that stays light while the rest of the app is dark is the defect this standard exists to prevent.

## Images, Logos, and Charts

- **A logo ships a dark variant**, or is drawn so it reads on both canvases. A black wordmark on a dark background is invisible.
- **A chart's series colors are checked against both canvases**, per [[dashboard.component.md]]. A palette validated only on white usually loses one series on dark.
- **A screenshot or an illustration** with a white background gets a border or a surface behind it in dark mode, so it does not glare.

## Contrast in Both Themes

Every contrast rule in [[uix.component.md]] applies in both themes, measured against the surface the text actually sits on:

- Text reaches 4.5:1 at normal size and 3:1 at large size, in light and in dark.
- HeroUI's own light and dark themes are checked by HeroUI. **Every variable a project overrides is checked twice**, once per theme, before it ships.
- A status color is still paired with a label or an icon in both themes. Hue alone carries even less in dark mode, where saturated colors compress.

## The Switch

**One theme control, in the header bar**, per [[header.bar.component.md]]. It offers Light, Dark, and System, and changes the theme at once with no reload.

- One control in one place. Not a second one in a settings page, the account page, or the footer.
- It is a HeroUI component, a menu or a segmented group, with an accessible name such as `Theme`.
- The change is instant. A short color transition on `body` is allowed and is cut to nothing under reduced motion, per [[animation.component.md]].

## Do and Do Not

| Do | Do not |
| :- | :- |
| Ship light and dark together, for the whole app, from the first screen | Ship one theme and add the other later |
| Use one controller: `useTheme` in a Vite app | Run two controllers against `<html>` |
| Set the theme in an inline `<head>` script before the first paint | Let a dark-mode viewer see a white flash on every load |
| Override a color in a light block and a dark block | Override a color on a bare `:root` |
| Read every color from a HeroUI variable | Write a `dark:` variant on a component |
| Check every overridden pair in both themes | Assume a light accent works on a dark surface |
| Offer Light, Dark, and System, defaulting to System | Remove the System option or hide the control |
| Set `color-scheme` per theme | Leave native controls light inside a dark app |

## Related Standards

| Document | Owns | Read it for |
| :- | :- | :- |
| [[uix.component.md]] | The HeroUI setup, the variable contract, and the contrast rules | Every variable this file switches |
| [[header.bar.component.md]] | The header bar | Where the theme control sits |
| [[dashboard.component.md]] | Charts and their palette | Checking a series palette on both canvases |
| [[animation.component.md]] | Motion | The theme transition, and reduced motion |
| [[refresh.component.md]] | What survives a reload | Why the theme may live in browser storage |

## Deviations

Any intentional deviation is recorded in the vault as a `decision` note naming this standard, the reason, and a plan to return to it, per [[memory.rules.md]]. It is never written into the project README, because this vault is private and a list of departures from it discloses the standards themselves.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Accessibility requirements, specifically the contrast floor in both themes
2. Direct user instructions
3. [[uix.component.md]]
4. This dark mode standard
5. Existing project conventions

## Related

- [[uix.component.md]]
- [[header.bar.component.md]]
- [[dashboard.component.md]]
- [[animation.component.md]]
- [[refresh.component.md]]
- [[memory.rules.md]]
