---
tags:
  - kind/template
  - layer/docs
---

> Up: [[README.md]]

# Project README Template

> [!example]
> Every `[bracketed]` passage below is guidance to be replaced, not structure to be kept. Remove each one once the real content is in place, and keep the section order.

Copy the block below into a new project's `README.md`. **The block carries no frontmatter and no `---`**, per the project document shape in [[docs.rules.md]]; this file has frontmatter because it is a vault document and the block is not.

Delete a section only when it genuinely does not apply. **Known Limitations and Deviations From the Standards are never deleted**: an empty section is information, a missing one is a question.

````markdown
# [Project Name]

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-[Version]-EE4C2C?logo=pytorch&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![License](https://img.shields.io/badge/License-MIT-750014)

[One or two sentences: what this is and what it does, with **the claim that matters in bold**.]

[Then one sentence saying why it exists: the problem it solves, or the cost of not having it.
This is the line nobody can reconstruct from the code, so it is the one that has to be written.]

## Table of Contents

1. [Setup](#setup)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [Data](#data)
5. [Project Structure](#project-structure)
6. [Development](#development)
7. [Known Limitations](#known-limitations)
8. [Deviations From the Standards](#deviations-from-the-standards)
9. [License](#license)

## Setup

[Say up front which steps are already done and where a returning reader starts.]

**1. Environment.** [Which manager, which environment name, which Python.]

```bash
conda env create -f environment.yml
conda activate [env-name]
```

[Any trap this step carries, in bold, with the mechanism and the real error text. Delete if
there is none; do not invent one.]

**2. Configuration.** Copy the template and fill it in by hand.

```bash
cp .env.example .env
```

[Which variables are required, and where each value comes from. Names only, never a value.]

**3. [Next step].** [What it is.]

```bash
[command]
```

## Usage

[The smallest thing that does something real, as the command that actually runs.]

```bash
python -m [package].[entrypoint] --input data/raw --output data/processed
```

[What it produces and where it lands.]

## Configuration

Every variable the project reads. Names only, never a real value; see [[env.rules.md]].

| Variable | Required | Description |
| :- | :- | :- |
| `[VAR_NAME]` | Yes | [What it points at, and where the value comes from] |
| `[VAR_NAME]` | No | [What it changes, and the default] |

## Data

[Where the data comes from and what version is in use.] **Nothing here is committed.**

| Item | Location | Notes |
| :- | :- | :- |
| Raw | `data/raw/` | Gitignored. [How to obtain it] |
| Processed | `data/processed/` | Gitignored. Produced by `[command]` |
| [Weights] | `[path]` | Gitignored. [How to regenerate] |

## Project Structure

```text
[package]/
  data/          # loading and preprocessing
  models/        # model definitions
  train.py       # entrypoint
notebooks/       # exploration only, nothing that runs twice
tests/
```

## Development

```bash
ruff check .          # lint
ruff format .         # format
pytest                # tests
```

## Known Limitations

[What this does not do and what it is bad at. The section everybody skips writing and every
reader needs. Each item is the claim in bold, then the mechanism, then the workaround where
one exists.]

- **[The limit, as a claim.]** [Why it is that way, and what it costs. Name the ceiling and
  whether it fails loudly or quietly.]
- **[The limit.]** [The mechanism, and what to do instead.]

## Deviations From the Standards

[Where this project departs from a rule in the vault. Numbered, each naming the rule, the
reason, and the cost accepted. A project with none writes one line saying so.]

1. **[What is different.]** `[rule].rules.md` requires [what]. This does [what] instead,
   because [reason]. The cost accepted: [what is given up]. [Whether it generalises.]

[Name a vault rule in backticks, not as a wikilink. A project repository is not the vault, so a
wikilink resolves to nothing there, and it leaves a phantom node in the vault graph.]

## License

[MIT, Apache 2.0, or none. "None" means default copyright, all rights reserved, and that is a
choice worth stating rather than leaving blank.]
````

## Related

- [[docs.rules.md]]
- [[badge.rules.md]]
- [[api.template.md]]
- [[model.template.md]]
- [[agent.template.md]]
- [[backend.template.md]]
- [[frontend.template.md]]
- [[env.rules.md]]
