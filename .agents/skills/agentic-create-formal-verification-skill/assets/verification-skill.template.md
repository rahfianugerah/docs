---
name: agentic-verify-{{area}}
description: Checks that {{the property, in one plain sentence}}, using {{tool}} over {{module}}. Use before finishing any change to {{covered paths}}, and when a bug report touches {{area in plain words}}.
---

# Verify {{Area in Title Case}}

{{The property, in one plain sentence.}} If it breaks, {{the harm to a user, in one plain sentence.}}

## Does the Change Touch It

```bash
git diff --name-only {{sync commit}} -- {{covered paths, space separated}}
```

Any output means the covered code changed since the model was last confirmed against it. Run the check, and read "When a Change Is Intended" below if the change was on purpose.

## Coverage

| Model part | Code it stands for |
| :- | :- |
| `{{variable, action, or definition}}` | `{{path}}:{{function}}` |

Synced at commit `{{sha}}` on {{YYYY-MM-DD}}. Move it forward only after confirming that the model still describes the code at the new commit.

## Scope

- **Verified:** {{what holds, in plain words}}.
- **Bounds:** {{the constants: how many requests, retries, items}}.
- **Assumes:** {{what the model takes as given, such as the database serializing row locks}}.
- **Not covered:** {{what is left out}}.

## Run

From this skill's folder:

```bash
{{the one rerun command}}
```

- Tool: {{tool and pinned version, and how to install it}}.
- A pass prints: `{{the pass line}}`.
- It runs in about {{duration}}.

## Read the Result

- **Pass:** the property holds within the bounds above, and nothing more is claimed.
- **Fail:** {{how a counterexample appears for this tool}}. Tell it as steps in the code's words, such as: {{a short example sequence}}.
- **Before calling it a bug**, replay the steps against the real code as a test. If they do not reproduce, the model is wrong: fix the model, and say so in the report.
- **A real bug** is reported with its steps. The property is never weakened to make the check pass.

## When a Change Is Intended

1. Update the model to match the new code, part by part, and update the coverage table.
2. Rerun every broken variant below. Each must still fail.
3. Rerun the check, then move the sync commit forward.

## Broken Variants It Catches

| Change to the code | What the check reports |
| :- | :- |
| {{a deliberate break, such as removing the row lock in path:function}} | {{the failure, such as NoDoubleCharge violated in 4 steps}} |
