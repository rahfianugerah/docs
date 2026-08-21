# Project Standards

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deploy-4285F4?logo=googlecloud&logoColor=white)
![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Rules](https://img.shields.io/badge/Rules-20-4C1D95)
![Components](https://img.shields.io/badge/Components-11-4C1D95)
![Templates](https://img.shields.io/badge/Templates-6-4C1D95)
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
| [component/](component/) | Framework-agnostic UI component standards: tokens, dropdowns, calendars, refresh |
| [gcp/](gcp/) | The Cloud Run deploy standard, the runbook, and the Cloud Build templates |
| [template/](template/) | Documentation templates: project README, API, and model card |
| [memory/](memory/) | The portable AI memory: markdown notes, indexed by Cognee |
| [graph/](graph/) | The machine-generated half: code maps and the knowledge graph export. Rebuilt, never hand-edited |

## Rules

Grouped by when you reach for them, not by importance. A rule is not optional because it sits in a later group.

**How work moves:**

| Document | Owns |
| :- | :- |
| [[branch.rules.md]] | `main` plus short-lived branches. Trunk-based, no staging, because there is no team to coordinate |
| [[commit.rules.md]] | Conventional Commits, an `exp` type for experiments, and what never enters a commit |
| [[pr.rules.md]] | When a pull request is worth opening, and what an experiment must record to be reproducible |
| [[docs.rules.md]] | What every project documents, how it is written, and the Obsidian conventions |
| [[badge.rules.md]] | shields.io flat badges: logo, name, version, on the brand color |
| [[callout.rules.md]] | The callout types, where one is required, and where it is forbidden |

**What you build:**

| Document | Owns |
| :- | :- |
| [[codes.rules.md]] | YAGNI, KISS, DRY, readability, Python 3.13, conda and `.venv`, and the ML practices that differ |
| [[database.rules.md]] | PostgreSQL and SQLAlchemy, and which cases take the ORM and which take raw SQL |
| [[env.rules.md]] | Why a real environment file is never read, in any format, including a notebook cell |
| [[secret.rules.md]] | Which values are secrets, and where each one actually lives |
| [[security.rules.md]] | The OWASP secure coding checklist, and the plan-first review procedure |
| [[repository.rules.md]] | One deployable per repository, git hygiene, and what every project documents |
| [[stacks.rules.md]] | The stack every project starts from, and what needs a written exception |
| [[api.rules.md]] | The REST contract: versioning, the error shape, pagination, and tool endpoints |
| [[agent.rules.md]] | When an agent writes a memory note, and how many |
| [[analytics.rules.md]] | Which chart a shape of data earns, the guardrails against distortion, and the no-3D gate |
| [[prd.rules.md]] | The PRD every project carries, written before the code, and the non-goals that bound it |
| [[media.rules.md]] | Document and media upload, covering PDF and photo |
| [[pwa.rules.md]] | The PWA layer of a frontend: manifest, icons, and offline behavior |

**What you build for the web:**

| Document | Owns |
| :- | :- |
| [[uix.component.md]] | The token contract every component reads from, and the shared component rules |
| [[dropdown.component.md]] | Selects, themed listboxes, and collapsible navigation groups |
| [[calendar.component.md]] | Date fields: native or custom, the panel, and the year clamp |
| [[refresh.component.md]] | What survives a reload, and the three things that break it |
| [[sidebar.component.md]] | The navigation rail: anatomy, grouping, markers, and the mobile drawer |
| [[login.component.md]] | The sign-in screen, and why every failure reads the same |
| [[loading.component.md]] | The four loading surfaces, and which wait each one serves |
| [[dashboard.component.md]] | Charts: the form before the color, and when it is not a chart at all |
| [[search.component.md]] | Filter against search, the matching ladder, and normalization |
| [[scrollbar.component.md]] | A scrollbar is an affordance, and where it must never be hidden |
| [[title.header.component.md]] | The product name: one form, everywhere, never from configuration |
| [[pagination.component.md]] | Every table: paging rather than scroll, adaptive page size, controls, and the data binding |

**What you build with AI:**

| Document | Owns |
| :- | :- |
| [[ai.rules.md]] | Every AI project: conda-forge environments, reproducibility, data, experiments |
| [[ml.rules.md]] | Tabular and classical: pipelines, splitting, leakage, imbalance |
| [[dl.rules.md]] | Deep learning: PyTorch from conda-forge, determinism, the training loop |

**How it ships:**

| Document | Owns |
| :- | :- |
| [[deploy.rules.md]] | What runs on Cloud Run and what does not, the resource allocation, and how not to overspend |
| [[deploy.cloud.md]] | The copy-and-paste Cloud Run runbook, from project setup to rollback |

## Templates

Every documentation file starts from one of these, per [[docs.rules.md]]. Keep the section order.

| Template | Used for |
| :- | :- |
| [[project.template.md]] | A project `README.md` |
| [[model.template.md]] | A `MODEL.md` model card: data, seed, metrics, failure modes |
| [[api.template.md]] | An `API.md` documenting endpoints |
| [[agent.template.md]] | A project's `CLAUDE.md` and `AGENTS.md`, pointing agents at the map and the rules |
| [[cloudbuild.service.template.yaml]] | The Cloud Build pipeline for a Cloud Run service |
| [[cloudbuild.job.template.yaml]] | The Cloud Build pipeline for a Cloud Run job |

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
| Environment | Conda (Miniconda) for machine learning, `.venv` for plain Python |
| Database | PostgreSQL with SQLAlchemy 2.x and Alembic; SQLite for a local single-user project |
| Lint and format | Ruff |
| Tests | pytest |
| Deploy | Cloud Run, built by Cloud Build, images in Artifact Registry |
| Vault | Obsidian, with Graphify and Cognee over the same files, built by `plugmybrain` |

## Using It With a Model

Point the assistant at this repository and give it [[CLAUDE.md]] or [[AGENTS.md]] as its entry point. Both import this file and the memory protocol, so the rules and the memory load together.

Nothing here is model-specific. A different assistant reads the same markdown and arrives at the same context, which is the entire reason the memory is files.

## Index

### Rules

- [[codes.rules.md]]
- [[database.rules.md]]
- [[commit.rules.md]]
- [[branch.rules.md]]
- [[pr.rules.md]]
- [[docs.rules.md]]
- [[badge.rules.md]]
- [[callout.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]
- [[repository.rules.md]]
- [[stacks.rules.md]]
- [[api.rules.md]]
- [[agent.rules.md]]

### Deploy

- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[cloudbuild.service.template.yaml]]
- [[cloudbuild.job.template.yaml]]

### Components

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[calendar.component.md]]
- [[refresh.component.md]]
- [[sidebar.component.md]]
- [[login.component.md]]
- [[loading.component.md]]
- [[dashboard.component.md]]
- [[search.component.md]]
- [[scrollbar.component.md]]
- [[title.header.component.md]]

### AI

- [[ai/README.md]]
- [[ai.rules.md]]
- [[ml.rules.md]]
- [[dl.rules.md]]

### Templates

- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]
- [[agent.template.md]]

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
- These documents follow their own rules, including [[docs.rules.md]] and [[badge.rules.md]]. A badge here is as current as one in a project README, or this file is not credible.
