> Up: [[README.md]]

# Code Standard

## Core Requirement

Code is read far more often than it is written, usually by someone who has forgotten writing it. Optimize for the reader.

Three principles decide every judgement call, in this order:

| Principle | The question it answers |
| :- | :- |
| **YAGNI** | Does this need to exist at all? |
| **KISS** | Is this the simplest thing that works? |
| **DRY** | Is this knowledge written down more than once? |

They are ordered on purpose. Code that does not exist cannot be complex, and code that is not complex rarely needs deduplicating.

## YAGNI: You Are Not Going To Need It

Build what the task needs today. Not what it might need.

- No abstraction with one implementation. No interface for one class, no factory for one product, no plugin system for one plugin.
- No configuration option for a value that has never changed.
- No parameter no caller passes. No branch no caller reaches.
- No "we might want to swap the database later." Swap it later, when later arrives and you know what it swaps to.
- Delete dead code instead of commenting it out. Git remembers it.

The cost of a wrong abstraction is higher than the cost of writing the thing twice. Two duplicated blocks are easy to merge once you can see what they share; one wrong abstraction has to be unpicked from every caller.

> [!warning]
> Two blocks that look alike but change for different reasons are not duplication. Merging them is how a shared helper grows four boolean flags to serve four callers.

## KISS: Keep It Simple

The simplest solution that works is the correct one.

Climb this ladder and stop at the first rung that holds:

1. Does it need to exist? Skip it.
2. Does something in this project already do it? Reuse it.
3. Does the standard library do it? Use it.
4. Does an already-installed dependency do it? Use it.
5. Can it be one function? Write one function.

Never add a dependency for something a few lines of standard library covers. Never write fifty lines for something the standard library already solved.

Concretely:

- Prefer a function to a class. Prefer a class to a class hierarchy.
- Prefer a flat sequence of steps to nested conditionals. Return early instead of nesting an `else`.
- Prefer an explicit loop to a clever comprehension nobody can read at a glance.
- A function does one thing. If the name needs "and", it is two functions.
- Keep a function short enough to read without scrolling. This is a smell test, not a line count.
- Boring beats clever. Clever is what somebody decodes at 3am while something is broken.

## DRY: Do Not Repeat Yourself

DRY is about **knowledge**, not about characters.

- One piece of knowledge lives in one place: a business rule, a magic number, a validation, a file path convention.
- Two blocks that look alike but change for different reasons are **not** duplication. Leave them apart.
- Two blocks that look different but must change together **are** duplication. Merge them.
- A constant used twice is a named constant. A constant used once is fine where it is.

The test is not "do these lines match" but "if this rule changed, how many places would I have to edit?" More than one is the problem.

Do not apply DRY so hard that it fights KISS. A shared helper with four boolean flags to serve four callers is worse than four small functions.

## Readability

The rules above shape the structure. These shape the surface.

- **Names say what a thing is.** `active_users` not `au`, not `data`, not `temp`. A long clear name beats a short cryptic one.
- **A boolean reads as a statement.** `is_valid`, `has_permission`, `should_retry`.
- **A function name says what it does.** `calculate_total` not `process`. `process` means nothing.
- **Comments say why, never what.** The code already says what. If a comment explains what, rewrite the code instead.
- **A comment that explains a non-obvious decision is worth keeping.** A workaround, a chosen trade-off, a reason a naive approach fails; write those down, they are the ones nobody can reconstruct.
- **No commented-out code.** Delete it.
- **Consistent formatting is not negotiable.** Run the formatter; do not argue with it.
- **Type hints on every public function.** They are documentation the interpreter checks.

## Python

Python 3.13. Written in **English**: every identifier, every comment, every docstring, every commit, every document.

### Environment

Two managers, and the project decides which one:

| Use | When |
| :- | :- |
| **Conda (Miniconda)** | Any machine-learning or data project. Native dependencies, CUDA, and scientific packages install correctly through conda and break through pip alone |
| **`.venv`** | A plain Python project with pure-Python dependencies: a script, a CLI, a small API |

Conda is the default for this stack, since these are ML projects. Reach for `.venv` when a project genuinely has no native dependency.

Rules:

- **Never install into the base environment.** One environment per project, named after the project.
- A conda project commits an `environment.yml`. A `.venv` project commits a `pyproject.toml` or a `requirements.txt`.
- Inside a conda environment, install through conda first; use pip only for packages conda does not carry, and record them in the same `environment.yml` under a `pip:` block.
- Pin the Python version in the environment file. Pin the major version of every direct dependency; do not float on latest.
- `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, and model weights never enter git.
- The project README states the exact activation command, so setup is copy and paste.

```yaml
# environment.yml
name: my-project
channels: [conda-forge]
dependencies:
  - python=3.13
  - numpy
  - pandas
  - pip
  - pip:
      - some-package-conda-lacks
```

### Style

- Follow PEP 8. Do not hand-format; run **Ruff** for both linting and formatting, and let it settle every argument.
- `snake_case` for functions and variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants.
- Type hints on public functions. `list[str]`, not `List[str]`; the builtin generics are standard now.
- Docstrings on anything whose purpose is not obvious from the signature. One line is usually enough.
- Prefer `pathlib.Path` to string paths, f-strings to `%` and `.format()`, and a `dataclass` to a dictionary of fixed keys.
- Never use a mutable default argument. `def f(x: list | None = None)` and default it inside.
- Never catch bare `except:`. Catch the exception you can actually handle.
- Never leave `print()` in library code; use `logging`.

### Machine Learning

An AI project follows [[ai/README.md]] in addition to this file. That folder owns the environment, reproducibility, data handling, experiments, and evaluation, because those rules are specific enough to be worth their own place and long enough to bury the general ones if kept here.

The one line worth repeating in both: **a model is quietly wrong rather than broken.** Ordinary code errors; a model returns a plausible number and says nothing. Everything in [[ai.rules.md]] exists to make that silence impossible.

## Testing

A test is what lets you change code without fear.

- Test behaviour, not implementation. A test that breaks when you rename a private method is a liability.
- Test the non-obvious: a branch, a boundary, a parser, a calculation. A one-line passthrough does not need a test.
- One failing assertion should say what broke. Prefer several small tests to one that asserts twelve things.
- Use `pytest`. No fixtures, no factories, and no test base classes until plain functions genuinely stop being enough.
- A bug fix comes with the test that would have caught it.

YAGNI applies to tests too. Full coverage of trivial code is work that buys nothing.

## Do and Do Not

Do:

- Delete more than you add.
- Reuse what the project already has before writing something new.
- Name things so the next reader does not have to guess.
- Write the comment that explains why a decision was made.
- Pin dependencies and commit the environment file.
- Set and record every random seed.

Do not:

- Build an abstraction for a second case that does not exist yet.
- Add a dependency for what the standard library already does.
- Merge two blocks that merely look alike.
- Leave commented-out code, dead branches, or unused parameters.
- Install into the base conda environment.
- Commit data, weights, or checkpoints.
- Let a notebook become the thing that runs in production.

## Applies To

- [[docs.rules.md]]
- [[env.rules.md]]
- [[security.rules.md]]
- [[commit.rules.md]]
