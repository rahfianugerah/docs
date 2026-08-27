---
tags:
  - kind/template
  - layer/frontend
  - layer/docs
---

> Up: [[README.md]]

# Frontend README Template

> [!example]
> Every `[bracketed]` passage below is guidance to be replaced, not structure to be kept. Remove each one once the real content is in place, and keep the headings and their order exactly as they are.

Copy everything from the `# Title` line down into the frontend repository's `README.md`.

```markdown
# [Project Name]

![React](https://img.shields.io/badge/React-VERSION-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-VERSION-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-VERSION-646CFF?logo=vite&logoColor=white)
![Node](https://img.shields.io/badge/Node-VERSION-5FA04E?logo=nodedotjs&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Managed-4285F4?logo=googlecloud&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-VALUE-5A0FC8?logo=pwa&logoColor=white)
![Testing](https://img.shields.io/badge/Testing-VALUE-COLOR)
![Status](https://img.shields.io/badge/Status-VALUE-COLOR)
![License](https://img.shields.io/badge/License-VALUE-COLOR)
```

Follow [[badge.rules.md]] for the row. Remove a badge only when the project genuinely has no equivalent value to report; never invent one.

## Table of Contents

1. Project Overview
2. Technology Stack
3. Frontend Architecture
4. Project Structure
5. Configuration
6. Routing, Pages, and Components
7. State and Data Management
8. Authentication, Styling, and Accessibility
9. Testing, Errors, and Performance
10. Development and Deployment

## 1. Project Overview

`[One paragraph: what this frontend is, who uses it, and what it is for.]`

**Do not include endpoint details.** API documentation lives in `API.md`.

## 2. Technology Stack

| Category | Technology | Version |
| :- | :- | :- |
| Runtime | `[Runtime]` | `[Version]` |
| Framework | `[Framework]` | `[Version]` |
| Language | `[Language]` | `[Version]` |
| Build tool | `[Tool]` | `[Version]` |
| Router | `[Library]` | `[Version]` |
| Data fetching | `[Library]` | `[Version]` |
| Styling | `[Method]` | `[Version]` |
| Icons | `[Set]` | `[Version]` |
| Testing | `[Tool]` | `[Version]` |
| Deployment | `[Platform]` | `[Version or Not applicable]` |

Use this status when a technology is not used:

```html
<code style="color: red">Not Used</code>
```

## 3. Frontend Architecture

### Architecture Type

`[Single-page app, server-rendered, static, or hybrid]`

### Architecture Description

`[How the frontend is organized]`

### Main Layers

| Layer | Responsibility |
| :- | :- |
| `[Layer]` | `[Responsibility]` |

### Application Flow

```text
Route > Layout > Page > Component > Data Service > API
```

### User Interaction Flow

```text
User Action > Handler > State Update > Render
```

### Rendering Strategy

`[Client-side, server-side, static generation, or mixed]`

## 4. Project Structure

```text
[The relevant directory structure]
```

### Directory Explanation

| Directory | Purpose |
| :- | :- |
| `[Path]` | `[Purpose]` |

Include only the directories needed to understand the system.

## 5. Configuration

### Configuration Files

| File | Purpose |
| :- | :- |
| `.env.example` | Environment variable reference |
| `[File]` | `[Purpose]` |

### Environment Variables

| Variable | Required | Description | Example |
| :- | :- | :- | :- |
| `[VITE_VARIABLE]` | `[Yes or No]` | `[Description]` | `[Placeholder]` |

> [!danger]
> **Every build-time variable ends up inside the bundle the browser downloads.** It is public the moment it ships. Never put a token, a key, or any secret in one, per [[secret.rules.md]].

**Changing a build-time value means rebuilding, not redeploying**, per [[deploy.rules.md]].

### Feature Flags

| Flag | Default | Purpose |
| :- | :- | :- |
| `[Flag]` | `[Value]` | `[Purpose]` |

### Environments

| Environment | Purpose |
| :- | :- |
| Development | Local development |
| Staging | Pre-production verification |
| Production | Live |

## 6. Routing, Pages, and Components

### Routing Method

`[Routing library or framework routing]`

### Main Routes

| Route | Page or layout | Access |
| :- | :- | :- |
| `[Pattern]` | `[Page]` | `[Public, authenticated, role-based]` |

Document frontend routes only. **Do not include API endpoint definitions.**

### Main Pages

| Page | Route | Purpose | Layout |
| :- | :- | :- | :- |
| `[Page]` | `[Route]` | `[Purpose]` | `[Layout]` |

### Main Layouts

| Layout | Purpose | Used by |
| :- | :- | :- |
| `[Layout]` | `[Purpose]` | `[Pages or route group]` |

### Main Components

| Component | Category | Responsibility |
| :- | :- | :- |
| `[Component]` | `[Layout, feature, shared, form]` | `[Responsibility]` |

### Important Component Details

#### `[Component Name]`

Purpose: `[Purpose]`

| Property | Type | Required | Description |
| :- | :- | :- | :- |
| `[prop]` | `[Type]` | `[Yes or No]` | `[Description]` |

Repeat only for important reusable or complex components. A component that implements a standard in [component/](../component/) says which one, rather than restating it.

## 7. State and Data Management

### State Management Method

`[Context, hooks, store, or local state]`

### State Categories

| Category | Storage method | Purpose |
| :- | :- | :- |
| Local UI state | `[Method]` | `[Purpose]` |
| Global state | `[Method]` | `[Purpose]` |
| Server state | `[Method]` | `[Purpose]` |
| Persistent state | `[Method]` | `[Purpose]` |

Include only the categories the project uses.

### State Flow

```text
User Action > Handler > State Update > Component Render
```

### Data Fetching Method

`[HTTP client, query library, framework loader, or native fetch]`

### Data Request Flow

```text
Component > Data Service > API > Response Handler > State Update
```

### Loading, Empty, and Error States

| State | Interface behaviour |
| :- | :- |
| Loading | `[Behaviour]` |
| Empty | `[Behaviour]` |
| Error | `[Behaviour]` |
| Success | `[Behaviour]` |

These follow [[loading.component.md]] and [[skeleton.component.md]]. **The three are mutually exclusive**; say how they are guarded.

### Browser Storage

| Data | Storage | Purpose | Expiration |
| :- | :- | :- | :- |
| `[Data]` | `[Local, session, cookie, IndexedDB]` | `[Purpose]` | `[Expiration]` |

**No token is ever stored in browser storage**, per [[auth.rules.md]]. Nothing here is restored on boot, per [[refresh.component.md]].

## 8. Authentication, Styling, and Accessibility

### Authentication Method

`[Session, token, external provider, or other]`

### Authentication Flow

```text
User Input > Authentication Request > Session Cookie > Application Access
```

### Authorization Model

`[Role-based, permission-based, attribute-based]`

### Roles

| Role | Frontend access |
| :- | :- |
| `[Role]` | `[Access]` |

> [!warning]
> **Frontend access control is presentation, never the only security control.** The backend enforces authorization, per [[security.rules.md]]. Hiding a menu is not a permission.

### Styling Method

`[CSS, CSS modules, utility framework, or other]`

### Design System

`[Which component standards this project follows, and any recorded deviation]`

### Theme Structure

| Item | Source |
| :- | :- |
| Colors | `[File]` |
| Typography | `[File]` |
| Spacing | `[File]` |
| Breakpoints | `[File]` |

Every one of those reads from the token contract in [[uix.component.md]].

### Responsive Design

`[The responsive strategy, and the breakpoint]`

### Accessibility Practices

Include only the practices the project actually implements:

- Semantic HTML
- Keyboard navigation
- Focus management
- Form labels
- Alternative text
- Color contrast
- Screen reader support
- Accessible error messages

### Accessibility Standard

`[WCAG level, internal standard, or Not specified]`

Use these statuses where appropriate:

```html
<code style="color: green">Supported</code>
<code style="color: yellow">Partially Supported</code>
<code style="color: red">Not Used</code>
```

## 9. Testing, Errors, and Performance

### Testing Strategy

| Test type | Purpose | Tool |
| :- | :- | :- |
| Unit | `[Purpose]` | `[Tool]` |
| Component | `[Purpose]` | `[Tool]` |
| Integration | `[Purpose]` | `[Tool]` |
| End-to-end | `[Purpose]` | `[Tool]` |
| Accessibility | `[Purpose]` | `[Tool]` |

Include only the test types the project uses.

### Running Tests

```bash
[Test command]
```

### Error Categories

| Category | Description |
| :- | :- |
| Validation | Invalid user input |
| Authentication | Missing or expired authentication |
| Authorization | Insufficient access |
| Network | Connection or request failure |
| Not found | Page or resource does not exist |
| Application | Unexpected frontend failure |

### Error Flow

```text
Error > Error Handler > User Feedback > Logging or Recovery
```

### Performance Strategy

Include only the techniques the project actually applies:

- Code splitting
- Lazy loading
- Tree shaking
- Bundle optimization
- Image optimization
- Font optimization
- Caching
- Memoization
- Prefetching
- Virtualized lists

### Performance Monitoring

| Metric or area | Tool or method |
| :- | :- |
| `[Metric]` | `[Tool]` |

**Do not invent a performance result, a coverage number, or an accessibility score**, per [[badge.rules.md]].

## 10. Development and Deployment

### Requirements

- `[Runtime]`
- `[Package manager]`
- `[Supported browser]`
- `[Other]`

### Installation

```bash
[Installation command]
```

### Environment Setup

1. Copy `.env.example` to the local environment file.
2. Add the required values by hand.
3. Do not commit the local environment file.

```bash
[Setup command]
```

### Start the Development Server

```bash
[Development command]
```

Local URL: `[URL]`

### Build

```bash
[Build command]
```

### Deployment

| Item | Description |
| :- | :- |
| Platform | `[Platform]` |
| Trigger | `[Branch, tag, or manual]` |
| Build-time config | `[Which values are baked in]` |
| Health check | `[Method]` |
| Rollback process | `[Process]` |

The full procedure is the project's own `deploy.cloud.md`, copied from [[deploy.cloud.md]]. **Deploy the backend first**, because the frontend bakes its URL in at build time.

### Known Limitations

| Limitation | Impact | Planned resolution |
| :- | :- | :- |
| `[Limitation]` | `[Impact]` | `[Resolution or Not planned]` |

Use this status when there are none:

```html
<code style="color: green">No Known Limitations</code>
```


## Deviations From the Standards

[Where this project departs from a rule in the vault. Numbered, each naming the rule, the reason, and the cost accepted. A project with none writes one line saying so, because an empty section is information and a missing one is a question. Name the rule in backticks, not as a wikilink: a project repository is not the vault, so a wikilink resolves to nothing there.]

1. **[What is different.]** `[rule].rules.md` requires [what]. This does [what] instead, because [reason]. The cost accepted: [what is given up]. [Whether it generalises.]

## Related

- [[docs.rules.md]]
- [[badge.rules.md]]
- [[backend.template.md]]
- [[api.template.md]]
- [[project.template.md]]
- [[uix.component.md]]
- [[pwa.rules.md]]
- [[deploy.cloud.md]]
