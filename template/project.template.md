> Up: [[README.md]]

# Project README Template

Copy the block below into a new project's `README.md` and fill in every bracket. Keep the section order; delete a section only when it genuinely does not apply.

Rules for filling it in are in [[docs.rules.md]]; the badge row follows [[badge.rules.md]].

```markdown
# [Project Name]

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-Miniconda-44A833?logo=anaconda&logoColor=white)
![[Library]](https://img.shields.io/badge/[Library]-[Version]-[HEX]?logo=[slug]&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2EA043)
![License](https://img.shields.io/badge/License-MIT-750014)

[One paragraph: what this is, what problem it solves, and who it is for. No history, no roadmap.]

## Setup

```bash
conda env create -f environment.yml
conda activate [env-name]
cp .env.example .env    # then fill in the values by hand
```

[For a plain-Python project instead:]

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

[The smallest example that does something real. A command, or a few lines of Python.]

```bash
python -m [package].[entrypoint] --input data/raw --output data/processed
```

## Configuration

Every variable the project reads. Names only, never a real value; see [[env.rules.md]].

| Variable | Required | Description |
| :- | :- | :- |
| `[VAR_NAME]` | Yes | [What it points at] |
| `[VAR_NAME]` | No | [What it changes, and the default] |

## Data

[Where the data comes from, what version is in use, and where it lives. Data is never committed.]

| Item | Location | Notes |
| :- | :- | :- |
| Raw | `data/raw/` | Gitignored. [How to obtain it] |
| Processed | `data/processed/` | Gitignored. Produced by [command] |

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

[What this does not do, and what it is bad at. The section everybody skips and every reader needs.]

## License

[MIT / Apache 2.0 / none]
```

## Related

- [[docs.rules.md]]
- [[badge.rules.md]]
- [[api.template.md]]
- [[model.template.md]]
