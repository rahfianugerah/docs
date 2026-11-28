---
name: agentic-boundaries
description: Generates or updates the lint rules that enforce a project's directory boundaries, so a boundary is checked by a tool and not by prose. Reads the folders and the declared boundaries, writes each boundary as a rule (ESLint flat config no-restricted-imports and no-restricted-syntax for TypeScript, Ruff flake8-tidy-imports banned-api TID251 for Python), runs the linter, and lists the violations. Never weakens a rule to make a violation pass. Use when a project gains a layer or a feature folder, when a review finds an import that crosses a boundary, or when a constraint comment says what may not import what.
---

# Boundaries

A boundary written in a README is broken the first time nobody rereads it. A boundary written as a lint rule is checked on every run. This skill turns each declared boundary into a rule, runs it, and reports what already crosses it.

## Steps

1. **Read the folders.**

   ```bash
   git ls-files -- app src | sed 's|/[^/]*$||' | sort -u
   ```

2. **Read the declared boundaries**: the layout section of the project's README, its `AGENTS.md`, any architecture document, and the lint configuration already in place (`eslint.config.js`, `pyproject.toml`, and every nested `ruff.toml`).
   - Write each boundary as one sentence: "Files in X never import Y, because Z."
   - A boundary that is only implied by the code, such as a folder nothing outside it imports yet, is proposed to the owner, never invented. The owner decides what the boundaries are.

3. **Write each boundary as a rule.** Working configurations for both tools are in `references/examples.md`; copy their shape.

   | Boundary | TypeScript | Python |
   | :- | :- | :- |
   | Folder X never imports folder or package Y | `no-restricted-imports` with a `regex` or `group` pattern, in a block whose `files` glob covers X | `banned-api` in `X/ruff.toml`, extending the root `pyproject.toml` |
   | Import another area only through its public face | A regex that bans a path one level deeper than the index | Ban the internal module, such as `app.db.session`, in the `ruff.toml` of each folder that must not reach it |
   | A filename convention, such as no allocation in `*.hot.ts` | `no-restricted-syntax` with esquery selectors, in a block whose `files` glob is the convention | No equivalent: give the code its own folder |
   | Every import names where it goes | Ban `^\.\./`; leave a folder through the `@/` alias | `ban-relative-imports = "all"` |

   Two traps, both explained in `references/examples.md`:
   - ESLint: a later block's options for the same rule replace the earlier block's, so every block repeats the shared patterns.
   - Ruff: a nested `banned-api` table replaces the root table, so every nested file repeats the project-wide bans.

   Every rule gets a message that says what to do instead, not only what is banned.

4. **Show each rule failing once.** Add one scratch import the rule must reject, run the linter, see the message, and remove the scratch line. A rule never seen failing may match nothing.

5. **Run the linter on the whole project and list the violations.**

   ```bash
   npx eslint .
   ruff check --select TID --output-format concise .
   ```

   Group them by boundary, with `file:line` for each.

6. **Never weaken a rule to make a violation pass.** No disable comment, no `noqa`, no wider allowlist, no deleted pattern, no `per-file-ignores` entry. For each violation:
   - inside the task's paths: fix the import by moving the code to where the boundary allows it, or calling the area through its public face
   - outside them: leave it, and report it as open
   - if the boundary itself looks wrong: report it to the owner, with the violations as evidence; changing a boundary is the owner's call

7. **Rerun the linter** after any fix. The count of violations inside the task's paths must be zero.

## Output

Boundaries: 6 declared, 6 encoded (4 in `eslint.config.js`, 2 in `app/*/ruff.toml`), 0 proposed. Shown failing: 6 of 6.

| Boundary | Rule | Violations |
| :- | :- | :- |
| A router never touches the database | `app/api/ruff.toml`, `banned-api` | 2 |
| A shared component never imports a feature | `eslint.config.js`, the `src/components` block | 1 |

Fixed: 1, `src/components/Header.tsx:4`, by moving the cart total helper to `src/lib`.

Open:

- `app/api/orders.py:7` imports `app.db.repositories`; outside this task's paths.
- `app/api/reports.py:3` imports `sqlalchemy`; outside this task's paths.
