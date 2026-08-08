> Up: [[README.md]]

# Badge Standard

## Core Requirement

Every project README opens with a row of badges. A badge answers one question at a glance: what is this built with, and which version.

**Use shields.io, flat style, with a logo, a name, and a version.** Never for-the-badge style, never a plain unstyled badge, never a hand-drawn image.

## The Shape

```text
[ logo ][ name ][ version ]
```

One badge, three parts: the technology's own logo, its name, and the version in use, on the technology's own brand color.

```text
https://img.shields.io/badge/<NAME>-<VERSION>-<HEX>?logo=<SLUG>&logoColor=white
```

```markdown
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5-EE4C2C?logo=pytorch&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
```

Rules:

1. **Flat is the default style.** It is what shields.io returns when no `style` parameter is given, so simply omit the parameter. Never pass `style=for-the-badge`, `plastic`, or `social`.
2. **Always include the logo.** `?logo=<slug>` using the simple-icons slug, which is the lowercase name with spaces removed: `python`, `pytorch`, `scikitlearn`, `jupyter`, `huggingface`.
3. **Always set `logoColor=white`.** Most brand colors are dark, and a logo left at its default disappears into the background.
4. **Always include a version** where one exists. `Python-3.13`, not a bare `Python`. A badge with no version says nothing a reader could not guess.
5. **Use the brand hex without the `#`.** shields.io reads `3776AB`, not `#3776AB`.
6. **Escape a hyphen in a label** by doubling it: `Scikit--learn`. A single hyphen is the field separator and will split the badge.
7. **Encode a space as `%20`**, or use `_`, which shields.io renders as a space.

## Badge Row

- Put the badges immediately under the `# Title`, before any prose, one per line in the source so a diff shows which badge changed.
- Keep the row short. Five to eight badges. A wall of twenty is decoration nobody reads.
- Order them: language, then framework, then key libraries, then tooling, then status and license last.
- The alt text is the technology name, so the row still reads when images are blocked.

```markdown
# Project Name

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5-EE4C2C?logo=pytorch&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![License](https://img.shields.io/badge/License-MIT-750014)
```

## Brand Colors

Use the technology's real brand color. These are the ones this stack uses.

| Technology | Slug | Hex | Example |
| :- | :- | :- | :- |
| Python | `python` | `3776AB` | `Python-3.13-3776AB` |
| PyTorch | `pytorch` | `EE4C2C` | `PyTorch-2.5-EE4C2C` |
| TensorFlow | `tensorflow` | `FF6F00` | `TensorFlow-2.18-FF6F00` |
| NumPy | `numpy` | `013243` | `NumPy-2.1-013243` |
| pandas | `pandas` | `150458` | `pandas-2.2-150458` |
| scikit-learn | `scikitlearn` | `F7931E` | `Scikit--learn-1.5-F7931E` |
| Hugging Face | `huggingface` | `FFD21E` | `Transformers-4.46-FFD21E` |
| Jupyter | `jupyter` | `F37626` | `Jupyter-Lab-F37626` |
| Anaconda / Conda | `anaconda` | `44A833` | `Conda-Miniconda-44A833` |
| FastAPI | `fastapi` | `009688` | `FastAPI-0.115-009688` |
| Docker | `docker` | `2496ED` | `Docker-27-2496ED` |
| PostgreSQL | `postgresql` | `4169E1` | `PostgreSQL-17-4169E1` |
| Git | `git` | `F05032` | `Git-2.47-F05032` |
| GitHub | `github` | `181717` | `GitHub-Actions-181717` |
| Obsidian | `obsidian` | `7C3AED` | `Obsidian-Vault-7C3AED` |
| Ruff | `ruff` | `D7FF64` | `Ruff-linted-D7FF64` (use `logoColor=black`) |
| pytest | `pytest` | `0A9EDC` | `pytest-8.3-0A9EDC` |

Two exceptions to `logoColor=white`: a light brand color such as Ruff's or Hugging Face's needs `logoColor=black`, or the logo vanishes.

## Status and License Badges

These carry no logo, because they represent a state rather than a technology. They keep the same flat style.

| Badge | Colors |
| :- | :- |
| Status | `Active-2EA043`, `WIP-D29922`, `Archived-6E7681` |
| License | `MIT-750014`, `Apache_2.0-D22128`, `GPL_v3-A42E2B` |
| Coverage | Green above 80, amber 60 to 80, red below |

## Keeping a Badge Honest

**A badge is a claim, and a stale badge is a lie.** It is the first thing a reader sees and the last thing anybody remembers to update.

- Update the version badge in the same commit that changes the version. If Python moves to 3.14, the badge moves with it.
- Do not add a badge for something the project does not actually use.
- Do not add a coverage or build badge unless it is wired to something real. A hardcoded `coverage-98%` is worse than no badge.
- Delete a badge whose technology has been removed.

## Do and Do Not

Do:

- Use flat style, with a logo, a name, and a version.
- Set `logoColor=white`, or `black` on a light brand color.
- Use the technology's own brand hex.
- Double a hyphen inside a label.
- Update a badge in the same commit that makes it wrong.

Do not:

- Use `for-the-badge`, `plastic`, or `social` style.
- Ship a badge with no version where a version exists.
- Include the `#` in a hex color.
- Fake a coverage or build number.
- Stack twenty badges nobody will read.

## Applies To

- [[docs.rules.md]]
- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]
