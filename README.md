# Personal Project Standards

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?logo=obsidian&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deploy-4285F4?logo=googlecloud&logoColor=white)
![Rules](https://img.shields.io/badge/Rules-11-4C1D95)
![Templates](https://img.shields.io/badge/Templates-5-4C1D95)
![Status](https://img.shields.io/badge/Status-Active-2EA043)

The source of truth for how I build things. One set of standards across every personal project, and a shared memory every AI model can read.

## What This Is

Two halves that serve each other:

- **[rules/](rules/) and [template/](template/)** decide how code, commits, documents, and secrets are handled. Every project follows them, so no project needs its own conventions.
- **[gcp/](gcp/)** holds the deploy standard, the Cloud Run runbook, and the Cloud Build templates.
- **[memory/](memory/)** is a portable AI memory: plain markdown, indexed by Cognee for semantic recall and Graphiti for temporal recall, read by any model with file access.

This repository is an Obsidian vault. Open the folder in Obsidian and the graph is already wired.

## Using It With a Model

Point the assistant at this repository and give it [[CLAUDE.md]] or [[AGENTS.md]] as its entry point. Both import this file, so the rules and the memory load together.

Nothing here is model-specific. A different assistant reads the same markdown and gets the same context, which is the reason the memory is files rather than a vendor's store.

## Stack

| Layer | Choice |
| :- | :- |
| Language | Python 3.13, English identifiers and English documentation |
| Environment | Conda (Miniconda) for machine learning, `.venv` for plain Python |
| Lint and format | Ruff |
| Tests | pytest |
| Vault | Obsidian, with Cognee and Graphiti over the same files |

## Index

### Rules

- [[codes.rules.md]]
- [[commit.rules.md]]
- [[branch.rules.md]]
- [[pr.rules.md]]
- [[docs.rules.md]]
- [[badge.rules.md]]
- [[env.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]

### Deploy

- [[deploy.rules.md]]
- [[deploy.cloud.md]]
- [[cloudbuild.service.template.yaml]]
- [[cloudbuild.job.template.yaml]]

### Templates

- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]

### Memory

- [[memory/README.md]]
- [[memory.rules.md]]
- [[note.template.md]]

### Configuration

- [[CLAUDE.md]]
- [[AGENTS.md]]

## Rules at a Glance

| Document | Owns |
| :- | :- |
| [[codes.rules.md]] | YAGNI, KISS, DRY, readability, Python and ML conventions, the environment |
| [[commit.rules.md]] | Conventional Commits, and what never enters a commit |
| [[branch.rules.md]] | `main` plus short-lived branches; trunk-based, no staging |
| [[pr.rules.md]] | When a pull request is worth opening, and what it records |
| [[docs.rules.md]] | What every project documents, how it is written, Obsidian conventions |
| [[badge.rules.md]] | shields.io flat badges: logo, name, version, brand color |
| [[env.rules.md]] | Why a real environment file is never read, in any format |
| [[secret.rules.md]] | Which values are secrets, and where each one lives |
| [[security.rules.md]] | The OWASP secure coding checklist, and the review procedure |
| [[deploy.rules.md]] | What runs on Cloud Run, what does not, and how not to overspend |
| [[deploy.cloud.md]] | The copy-and-paste Cloud Run runbook |

## Keeping It Honest

A standard nobody follows is worse than no standard, because it makes the codebase look governed when it is not.

- When the code and a rule disagree, fix one of them in the same session. Never leave both.
- A rule that has been broken three times is a rule that is wrong. Change it.
- These documents follow their own rules, including [[docs.rules.md]] and [[badge.rules.md]].
