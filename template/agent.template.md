> Up: [[README.md]]

# Agent Entry Point Template

Copy the block below into a project's `CLAUDE.md`, then copy that file to `AGENTS.md` so the two
are byte-identical. Claude Code reads the first, Codex reads the second, and a rule that lives
in only one of them is a rule half the tools ignore.

Fill in every bracket. The point of this file is to stop an agent rediscovering the codebase by
grepping it, which costs tokens every session and gets slower as the project grows.

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

If the map is stale, rebuild it with `pmb map .` rather than reading files to compensate.

## Rules Come From the Vault, Not From Here

`[path-to-vault]/rules/` and `[path-to-vault]/memory/` are the human-authored control plane and
they win on conflict with anything inferred from this code. Read the memory for decisions
already made rather than re-deriving them.

Never read the whole vault to answer a question about this code. That is what the map is for.

## The Cognee MCP Server

Read with `recall`, always passing `datasets`, so one project's memory cannot leak into
another's answer. This project's dataset is `[dataset]`.

```json
{"query": "[a question]", "datasets": ["[dataset]"], "search_type": "CHUNKS", "top_k": 15}
```

**Never call `remember` or `forget`.** The MCP server exposes them and they write straight into
the index, which the next `pmb sync` overwrites. Write a note into the vault instead.

## Two Things Not to Do

- Do not write to Cognee directly. Write markdown into `[path-to-vault]/memory/`, then run
  `pmb sync`. A direct write is an index write and is lost on the next rebuild.
- Do not hand-edit anything under `[path-to-vault]/graph/`. It is regenerated and gitignored.
```

## Related

- [[docs.rules.md]]
- [[memory.rules.md]]
- [[graph/README.md]]
- [[project.template.md]]
