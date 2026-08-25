---
tags:
  - kind/rule
  - layer/docs
---

> Up: [[README.md]]

# Badge Standard

> [!info]
> Every README opens with a badge row, in the shields.io regular style, shaped logo then name then version. This standard owns that row, and it owns how a product name and a state value are written.

## Core Requirement

A badge answers one question at a glance: what is this built with, and which version. A row of badges is the fastest thing on a README to read and the fastest thing to let rot, so both the shape and the spelling are fixed here rather than decided per project.

This applies to every project README, and to this vault's own README. A README with no badge row is not following this standard; nor is one whose badges disagree with what the repository actually ships.

## The Two Kinds

A badge is one of two kinds, and mixing their shapes is what makes a row look untidy even when every badge is individually correct.

### Technology Badge

The name is the label and the version is the value. The color is the technology's own brand hex, and the logo is its simple-icons slug.

```text
[ logo ][ name ][ version ]
```

```text
https://img.shields.io/badge/<Name>-<Version>-<Hex>?logo=<slug>&logoColor=white
```

```markdown
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)
```

> [!danger]
> Never write a technology badge as `Framework-React_19`. That puts a category in the label slot, so the row reads as a list of categories rather than a list of technologies, and two projects will file the same tool under two different categories. The name goes in the label.

### State Badge

The label is what is being reported and the value is the state. There is no logo and no brand color; the color carries the state.

```markdown
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![Testing](https://img.shields.io/badge/Testing-None_Yet-lightgrey)
![License](https://img.shields.io/badge/License-MIT-750014)
```

## Writing a Product Name

A product is written the way the product writes itself, with any file-extension suffix dropped.

| Written | Not |
| :- | :- |
| `React` | `react`, `React.js`, `ReactJS` |
| `Next` | `next.js`, `Next.js`, `NextJS` |
| `Vite` | `vite.js`, `ViteJS` |
| `Node` | `Node.js`, `NodeJS` |
| `FastAPI` | `Fastapi`, `fast-api` |
| `PostgreSQL` | `Postgresql`, `postgres` |
| `SQLAlchemy` | `Sqlalchemy`, `SQLalchemy` |
| `TypeScript` | `Typescript`, `TS` |
| `Tailwind CSS` | `TailwindCSS`, `tailwind` |
| `PyTorch` | `Pytorch`, `pyTorch` |

The suffix comes off because it names the file format, not the product, and because it is written three different ways by the people who use it. `React` and `Vite` are unambiguous without it.

> [!warning]
> Three products keep a lowercase name, because that is their own branding rather than an oversight: `npm`, `pytest`, and `pandas`. Do not Title Case them. They are the only three, and a fourth lowercase name in a badge row is a mistake to fix, not a precedent to follow.

## Writing a State

**Every label and every state value is Title Case.** Never `status`, never `wip`, never `active`.

| Written | Not |
| :- | :- |
| `Status-Active` | `status-active` |
| `Status-WIP` | `Status-wip`, `Status-Wip` |
| `Testing-None_Yet` | `Testing-None_yet` |
| `Cache-Not_Used` | `Cache-Not_used`, `cache-not-used` |
| `Styling-Shared_CSS` | `Styling-Shared_css` |

Capitalize each word except a short joining word such as `and`, `or`, `of`, `for`, `in`, `to`, or `per`, unless it opens the value. That is the same Title Case rule [[uix.component.md]] sets for the interface, so a state reads the same in a README as it does on a screen.

An initialism stays fully capitalized: `WIP`, `API`, `CSS`, `PWA`, `SSO`, `UAT`, `ML`. Title Case never lowercases the tail of an initialism.

An identifier keeps its exact form, because it is a literal something else has to match. A cloud region is `asia-southeast1`, a resource allocation is `1_vCPU_1Gi`, an API version is `v1`, and a release is `1.0.0`. Title Casing any of those makes the badge state a value that does not exist. The label in front of them is still Title Case: `Region-asia--southeast1`, not `region-asia--southeast1`.

One state has one spelling across every project. Three repositories writing `Not Used`, `Not used`, and `Unused` for the same thing is three states as far as a reader scanning two READMEs is concerned.

## Shape Rules

1. **Regular style is the default.** It is what shields.io returns with no `style` parameter, so omit the parameter. Never `style=for-the-badge`, `plastic`, or `social`, and never a hand-drawn image.
2. **A technology badge always carries its logo**, `?logo=<slug>`, using the simple-icons slug: the lowercase name with spaces and dots removed, such as `react`, `nodedotjs`, `postgresql`, `tailwindcss`, `scikitlearn`.
3. **Always set `logoColor=white`.** Most brand hexes are dark and a default-colored logo disappears into the background. A light brand color such as Ruff's or Hugging Face's takes `logoColor=black` instead, or the logo vanishes.
4. **Always carry a version** where one exists. `React-19`, not a bare `React`. A badge with no version says nothing a reader could not guess from the file listing.
5. **Use the brand hex without the `#`.** shields.io reads `61DAFB`, not `#61DAFB`.
6. **Escape a hyphen in a name** by doubling it: `Scikit--learn`. A single hyphen is the field separator and splits the badge.
7. **Encode a space as `_`**, which shields.io renders as a space. `%20` also works and is harder to read in a diff.
8. **The alt text is the badge label**, so the row still reads when images are blocked.

## The Row

- The row sits immediately under the `# Title`, before any prose, one badge per source line so a diff shows which badge changed.
- Order: language, framework, key libraries, tooling, then the state badges last.
- Five to ten badges. A wall of twenty is decoration nobody reads, and every extra badge is another thing that can go stale.
- One badge per fact. Do not carry both `Framework-React_19` and `React-19`.

```markdown
# Project Name

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deploy-4285F4?logo=googlecloud&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![License](https://img.shields.io/badge/License-MIT-750014)
```

## Brand Hex Reference

Use these rather than looking one up per project, so the same technology is the same color everywhere.

**Language and backend:**

| Technology | Slug | Hex |
| :- | :- | :- |
| Python | `python` | `3776AB` |
| FastAPI | `fastapi` | `009688` |
| SQLAlchemy | `sqlalchemy` | `D71F00` |
| PostgreSQL | `postgresql` | `4169E1` |
| pytest | `pytest` | `0A9EDC` |
| Ruff | `ruff` | `D7FF64` (use `logoColor=black`) |

**Frontend:**

| Technology | Slug | Hex |
| :- | :- | :- |
| React | `react` | `61DAFB` |
| TypeScript | `typescript` | `3178C6` |
| Vite | `vite` | `646CFF` |
| Node | `nodedotjs` | `5FA04E` |
| npm | `npm` | `CB3837` |
| Tailwind CSS | `tailwindcss` | `06B6D4` |
| Tabler Icons | `tabler` | `206BC4` |
| Playwright | `playwright` | `2EAD33` |
| PWA | `pwa` | `5A0FC8` |

**Data and machine learning:**

| Technology | Slug | Hex |
| :- | :- | :- |
| PyTorch | `pytorch` | `EE4C2C` |
| TensorFlow | `tensorflow` | `FF6F00` |
| NumPy | `numpy` | `013243` |
| pandas | `pandas` | `150458` |
| scikit-learn | `scikitlearn` | `F7931E` (write it `Scikit--learn`) |
| Hugging Face | `huggingface` | `FFD21E` (use `logoColor=black`) |
| Jupyter | `jupyter` | `F37626` |
| Conda | `anaconda` | `44A833` |

**Infrastructure and tooling:**

| Technology | Slug | Hex |
| :- | :- | :- |
| Docker | `docker` | `2496ED` |
| Cloud Run | `googlecloud` | `4285F4` |
| Git | `git` | `F05032` |
| GitHub | `github` | `181717` |
| Obsidian | `obsidian` | `7C3AED` |

## State Colors

A state badge uses a shields.io named color or a plain hex, never a brand color.

| Badge | Values |
| :- | :- |
| Status | `Active-2EA043`, `WIP-D29922`, `Archived-6E7681` |
| License | `MIT-750014`, `Apache_2.0-D22128`, `GPL_v3-A42E2B` |
| Coverage | Green above 80, amber 60 to 80, red below |
| Anything absent | `lightgrey` |

The shorthand names work too: `green` for a healthy state, `yellow` for in progress, `red` for a failing one, `lightgrey` for absent or not applicable.

## Keeping a Badge Honest

> [!warning]
> **A badge is a claim, and a stale badge is a lie.** A badge stating a version the repository does not ship is worse than no badge, because it is read as fact and checked by nobody. A `React-18` badge on a project running React 19 will be believed for as long as it stands.

- Update the badge in the same commit as the upgrade it describes, never in a later tidy-up commit.
- A state badge is checked whenever the state changes: a project that gains tests updates `Testing` that day.
- Never add a badge for something aspirational. `Testing-Playwright` on a project with no Playwright suite is a claim, not a plan.
- Do not add a coverage or build badge unless it is wired to something real. A hardcoded `coverage-98%` is worse than no badge.
- Remove a badge rather than leaving it stale. An absent badge tells a reader nothing; a wrong one tells them something false.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Put the product name in the label slot | Put a category there and the name in the value |
| Write `React`, `Next`, `Vite` | Write `react`, `next.js`, `vite.js` |
| Title Case every label and state value | Ship `status-active` or `Testing-None_yet` |
| Keep `npm`, `pytest`, and `pandas` lowercase | Title Case a brand that lowercases itself |
| Keep an identifier in its exact form | Title Case `asia-southeast1` into something that does not exist |
| Set `logoColor=white`, or `black` on a light brand | Leave a dark logo on a dark brand hex |
| Double a hyphen inside a name | Let a single hyphen split the badge |
| Use one spelling of a state across every project | Write `Not Used` here and `Unused` there |
| Update the badge in the upgrade commit | Leave a version badge one release behind |
| Carry five to ten badges | Build a wall of twenty |

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This badge standard
4. Existing project conventions

## Applies To

- [[docs.rules.md]]
- [[uix.component.md]]
- [[repository.rules.md]]
- [[stacks.rules.md]]
- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]
