# Project Standards

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deploy-4285F4?logo=googlecloud&logoColor=white)
![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Rules](https://img.shields.io/badge/Rules-22-4C1D95)
![Components](https://img.shields.io/badge/Components-15-4C1D95)
![Templates](https://img.shields.io/badge/Templates-10-4C1D95)
![Patterns](https://img.shields.io/badge/Patterns-16-4C1D95)
![Status](https://img.shields.io/badge/Status-Active-2EA043)

> [!important]
> Every personal project applies these standards. A new project follows them from the first scaffold.

The source of truth for how I build things: one set of standards across every project, and a shared memory every AI model can read.

## Overview

A project accumulates decisions nobody wrote down. Six months later the conventions are gone, the reasoning is gone, and the next project starts from scratch with slightly different habits. This repository is the fix: the conventions live in one place, every project follows them, and no project invents its own.

The rules here are deliberately short. A standard that costs more to follow than the mistake it prevents is a standard that gets abandoned, so each one earns its place: it exists because forgetting it has actually cost something. Every rule says why, because a rule with no reason attached is dropped the first time it is inconvenient.

Alongside them sits a portable AI memory. An assistant with no memory relearns the same context every session; an assistant whose memory lives inside one vendor's product is a memory you lose when you switch models. So the memory is plain markdown in git, indexed by tools that can be rebuilt and replaced.

The whole repository is an Obsidian vault. Open the folder and the graph is already wired.

## Repository Contents

| Contents | Description |
| :- | :- |
| [rules/](rules/) | How code, commits, documents, and secrets are handled. Every project follows these |
| [ai/](ai/) | Machine learning and deep learning standards, kept separate because AI projects fail differently |
| [component/](component/) | Framework-agnostic UI component standards: tokens, buttons, tables, dropdowns, calendars, refresh |
| [gcp/](gcp/) | The Cloud Run deploy standard, the runbook, and the build templates |
| [template/](template/) | Documentation templates: backend, frontend, project README, API, model card, agent entry point |
| [pattern/](pattern/) | Lessons lifted from real incidents, generalized. A failure and its mechanism, so it is not paid for twice |
| [memory/](memory/) | The portable AI memory: markdown notes, indexed by Cognee |
| [graph/](graph/) | The machine-generated half: code maps and the knowledge graph export. Rebuilt, never hand-edited |

## Rules

Grouped by when you reach for them, not by importance. A rule is not optional because it sits in a later group.

**How work moves:**

| Document | Owns |
| :- | :- |
| [[branch.rules.md]] | The two branch shapes, trunk and promotion, and which one a project declares |
| [[commit.rules.md]] | Conventional Commits, an `exp` type for experiments, and what never enters a commit |
| [[pr.rules.md]] | When a pull request is worth opening, what an experiment must record, and when an AI may open or merge one |
| [[docs.rules.md]] | What every project documents, how it is written, the tag taxonomy, and the Obsidian conventions |
| [[badge.rules.md]] | shields.io badges: the two kinds, the product name, and Title Case on every state |
| [[callout.rules.md]] | The callout types, where one is required, and where it is forbidden |

**What you build:**

| Document | Owns |
| :- | :- |
| [[codes.rules.md]] | YAGNI, KISS, DRY, readability, Python 3.13, conda and `.venv`, and the ML practices that differ |
| [[database.rules.md]] | PostgreSQL and SQLAlchemy, which cases take the ORM and which take raw SQL, and the restore nobody tested |
| [[env.rules.md]] | Why a real environment file is never read, in any format, including a notebook cell |
| [[secret.rules.md]] | Which values are secrets, where each one lives, and why a frontend holds none |
| [[security.rules.md]] | The OWASP checklist, the stack controls it turns into, personal data, and the audit trail |
| [[auth.rules.md]] | One identity source, one identity key, one swappable abstraction, and the non-human account |
| [[repository.rules.md]] | One deployable per repository, git hygiene, and what every project documents |
| [[stacks.rules.md]] | The stack every project starts from, and what needs a written exception |
| [[api.rules.md]] | The REST contract: the route shape, the error shape, pagination, and tool endpoints |
| [[agent.rules.md]] | When an agent writes a memory note, and how many |
| [[analytics.rules.md]] | Which chart a shape of data earns, the guardrails against distortion, and the no-3D gate |
| [[prd.rules.md]] | The PRD every project carries, written before the code, and the non-goals that bound it |
| [[media.rules.md]] | Document and media upload, covering PDF and photo |
| [[pwa.rules.md]] | The PWA layer of a frontend: manifest, icons, and offline behavior |

**What you build for the web:**

| Document | Owns |
| :- | :- |
| [[uix.component.md]] | The token contract, the radius rule, Inter, and the shared component rules |
| [[button.component.md]] | The six variants, the icon before the label, and one primary action per view |
| [[table.component.md]] | The table itself: wrapper, header, rows, cells, and the row actions |
| [[pagination.component.md]] | Every table: paging rather than scroll, adaptive page size, controls, and the data binding |
| [[dropdown.component.md]] | Selects, themed listboxes, and collapsible navigation groups |
| [[calendar.component.md]] | Date fields: native or custom, the panel, the full-card grid, and the year clamp |
| [[sidebar.component.md]] | The navigation rail: anatomy, grouping, markers, and the mobile drawer |
| [[login.component.md]] | The sign-in screen, and why every failure reads the same |
| [[loading.component.md]] | The four loading surfaces, and which wait each one serves |
| [[skeleton.component.md]] | The loading state a component shows in its own place, instead of holding the page |
| [[dashboard.component.md]] | Charts: the form before the color, the validated palette, and the export |
| [[search.component.md]] | Filter against search, the matching ladder, and normalization |
| [[scrollbar.component.md]] | A scrollbar is an affordance, and where it must never be hidden |
| [[title.header.component.md]] | The product name: one form, everywhere, never from configuration |
| [[refresh.component.md]] | What survives a reload, and the three things that break it |

**What you build with AI:**

| Document | Owns |
| :- | :- |
| [[ai.rules.md]] | Every AI project: conda-forge environments, reproducibility, data, experiments |
| [[ml.rules.md]] | Tabular and classical: pipelines, splitting, leakage, imbalance |
| [[dl.rules.md]] | Deep learning: PyTorch from conda-forge, determinism, the training loop |

**How it ships:**

| Document | Owns |
| :- | :- |
| [[deploy.rules.md]] | What runs on Cloud Run and what does not, the allocation, the registry retention, and the cost |
| [[deploy.cloud.md]] | The copy-and-paste Cloud Run runbook, from project setup to rollback |

## Templates

Every documentation file starts from one of these, per [[docs.rules.md]]. Keep the section order.

| Template | Used for |
| :- | :- |
| [[backend.template.md]] | The README of a backend repository |
| [[frontend.template.md]] | The README of a frontend repository |
| [[project.template.md]] | A single-repository project `README.md` |
| [[api.template.md]] | An `API.md` documenting endpoints |
| [[model.template.md]] | A `MODEL.md` model card: data, seed, metrics, failure modes |
| [[agent.template.md]] | A project's `CLAUDE.md` and `AGENTS.md`, pointing agents at the map and the rules |
| [[cloudbuild.service.template.yaml]] | The build pipeline for a backend service |
| [[cloudbuild.frontend.template.yaml]] | The build pipeline for a static frontend |
| [[cloudbuild.job.template.yaml]] | The build pipeline for a scheduled job |
| [[cleanup-policy.template.json]] | The registry retention policy, identical for every project |

## Patterns

A pattern records a failure and its mechanism, generalized away from the system it happened in. It carries no claim about any repository in this vault, which is what separates it from a memory note.

[[pattern/README.md]] holds the shape and the sixteen written so far, grouped around deploys that fail in the wrong place, databases that isolate less than they appear to, and reports that name the wrong cause.

## Memory

A memory every model can read, because it is files rather than a vendor's store.

| Layer | Tool | Holds |
| :- | :- | :- |
| Substrate | Obsidian vault, markdown | Everything. The source of truth |
| Structural | Graphify | An AST map of a codebase, so an agent stops grepping the tree |
| Semantic | Cognee | A knowledge graph and vector index built from the markdown |

**The markdown is the only durable store.** The other two are indexes over it: delete either and rebuild it from the files. That is what makes the memory portable, diffable, and reviewable, and what makes switching embedding model or graph database a reindex rather than a migration.

Both are built by `plugmybrain`, whose command is `pmb`.

| Document | Owns |
| :- | :- |
| [[memory/README.md]] | The architecture, the note types, and how to plug each tool in |
| [[memory.rules.md]] | The write and recall protocol every model follows |
| [[memory/codes.rules.md]] | Reference code kept beside a note that explains it |
| [[note.template.md]] | The shape of a note, for each of the four types |

## Stack

| Layer | Choice |
| :- | :- |
| Language | Python 3.13, English identifiers and English documentation |
| Backend | FastAPI with Pydantic v2, `uvicorn`, `psycopg` v3 |
| Frontend | React 19 on Vite with TypeScript, TanStack Query, Tabler icons, Inter |
| Environment | Conda (Miniconda) for machine learning, `.venv` for plain Python |
| Database | PostgreSQL 18 with SQLAlchemy 2.x and Alembic; SQLite for a local single-user tool |
| Lint and format | Ruff |
| Tests | pytest, and Playwright for end-to-end flows |
| Deploy | Cloud Run, built by Cloud Build, images in Artifact Registry |
| Vault | Obsidian, with Graphify and Cognee over the same files, built by `plugmybrain` |

## Using It With a Model

Point the assistant at this repository and give it [[CLAUDE.md]] or [[AGENTS.md]] as its entry point. Both import this file and the memory protocol, so the rules and the memory load together.

Nothing here is model-specific. A different assistant reads the same markdown and arrives at the same context, which is the entire reason the memory is files.

## Index

### Rules

- [[agent.rules.md]]
- [[analytics.rules.md]]
- [[api.rules.md]]
- [[auth.rules.md]]
- [[badge.rules.md]]
- [[branch.rules.md]]
- [[callout.rules.md]]
- [[codes.rules.md]]
- [[commit.rules.md]]
- [[database.rules.md]]
- [[docs.rules.md]]
- [[env.rules.md]]
- [[media.rules.md]]
- [[pr.rules.md]]
- [[prd.rules.md]]
- [[pwa.rules.md]]
- [[repository.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]
- [[stacks.rules.md]]

### Deploy

- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[cloudbuild.service.template.yaml]]
- [[cloudbuild.frontend.template.yaml]]
- [[cloudbuild.job.template.yaml]]
- [[cleanup-policy.template.json]]

### Components

- [[uix.component.md]]
- [[button.component.md]]
- [[calendar.component.md]]
- [[dashboard.component.md]]
- [[dropdown.component.md]]
- [[loading.component.md]]
- [[login.component.md]]
- [[pagination.component.md]]
- [[refresh.component.md]]
- [[scrollbar.component.md]]
- [[search.component.md]]
- [[sidebar.component.md]]
- [[skeleton.component.md]]
- [[table.component.md]]
- [[title.header.component.md]]

### AI

- [[ai/README.md]]
- [[ai.rules.md]]
- [[ml.rules.md]]
- [[dl.rules.md]]

### Templates

- [[backend.template.md]]
- [[frontend.template.md]]
- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]
- [[agent.template.md]]

### Patterns

- [[pattern/README.md]]

### Memory

- [[memory/README.md]]
- [[memory.rules.md]]
- [[memory/codes.rules.md]]
- [[note.template.md]]
- [[graph/README.md]]

### Decisions

- [[plugmybrain-runs-on-a-flat-cost-vm.decision.memory.md]]
- [[embeddings-are-voyage-3-5-at-1024-dimensions.decision.memory.md]]
- [[postgres-holds-the-graph-as-a-demo-feature.decision.memory.md]]
- [[retrieval-returns-chunks-not-a-written-answer.decision.memory.md]]

### Configuration

- [[CLAUDE.md]]
- [[AGENTS.md]]

## Keeping It Honest

A standard nobody follows is worse than no standard, because it makes a codebase look governed when it is not.

- When the code and a rule disagree, fix one of them in the same session. Never leave both.
- **A rule broken three times is a rule that is wrong.** Change the rule, do not keep losing the argument with yourself.
- **A rule reasoned about one component breaks where a page stacks two.** Draw the stacked page before adding one, per [[pattern/README.md]].
- These documents follow their own rules, including [[docs.rules.md]] and [[badge.rules.md]]. A badge here is as current as one in a project README, or this file is not credible.
