---
tags:
  - kind/template
  - layer/docs
  - topic/memory
---

> Up: [[README.md]]

# Agent Entry Point Template

> [!example]
> Every bracketed passage below is guidance to be replaced, not structure to be kept.

Copy the block below into a project's `CLAUDE.md`, then copy that file to `AGENTS.md` so the two are byte-identical. Claude Code reads the first, Codex reads the second, and a rule that lives in only one of them is a rule half the tools ignore.

Fill in every bracket. The point of this file is to stop an agent rediscovering the codebase by grepping it, which costs tokens every session and gets slower as the project grows.

Rules for filling it in are in [[docs.rules.md]]; the memory protocol is [[memory.rules.md]].

```markdown
# [Project Name]

[One line: what this project is.]

@README.md
@[path-to-vault]/memory/memory.rules.md

## Before You Search This Repository

**Code structure comes from the map, not from grepping.** `[path-to-map]/graph.json` is an AST
map extracted by tree-sitter, and reading it costs no model tokens. Query it instead of walking
the tree:

```bash
graphify query "[a question about this codebase]" --graph [path-to-map]/graph.json
graphify god-nodes --graph [path-to-map]/graph.json
```

If the map is stale, rebuild it with `pmb digest` rather than reading files to compensate.

## Rules Come From the Vault, Not From Here

`[path-to-vault]/rules/` and `[path-to-vault]/memory/` are the human-authored control plane and
they win on conflict with anything inferred from this code. Read the memory for decisions
already made rather than re-deriving them.

Never read the whole vault to answer a question about this code. That is what the map is for.

## The Memory Server

The memory is connected as an MCP server exposing two read-only tools:

- `recall` answers a question from the memory. **Always pass the brain**, which is the folder's
  own name lowercased, so one project's memory cannot leak into another's answer. This
  project's brain is `[brain]`.
- `brains` lists which memories exist on this machine.

Call `recall` before answering anything about this project's rules, decisions, architecture, or
history. `/pmb-map <brain>` switches which memory the session reads from when the work moves
elsewhere.

**Nothing here writes, on purpose.** To add a memory, write a markdown note under
`[path-to-vault]/memory/` and run `pmb digest`.

## Two Things Not to Do

- **Do not write to the index directly.** It is derived from the markdown, so a direct write is
  gone at the next rebuild. Write the note, then digest.
- **Do not hand-edit anything under `[path-to-vault]/graph/`.** It is regenerated and gitignored.
```

## Related

- [[docs.rules.md]]
- [[memory.rules.md]]
- [[agent.rules.md]]
- [[memory/README.md]]
- [[graph/README.md]]
- [[project.template.md]]
