---
name: agentic-create-formal-verification-skill
description: Scaffolds a TLA+ or Lean check for one module and leaves it behind as a new project-local skill named agentic-verify-<area>, with one rerun command and a record of what it covers. Picks the target from the code (a promise whose break harms users and that tests rarely reach), lets the question choose the tool, shows every property failing on a broken variant, and proves the new skill catches a deliberate break. Use when concurrency, retries, locking, a state machine, a parser, or money arithmetic needs more than tests, or when asked to model-check or prove something.
---

# Create a Formal Verification Skill

A test checks the cases someone thought of. A model checker checks every ordering inside a model, and a proof checks every input. This skill verifies one property where that matters most, then writes a project-local skill so the next agent can recheck any change against it, cold, without learning the tool.

## Steps

1. **Pick the target from the code.** Ask the owner only what the code cannot answer. Start where the owner points, if they name an area or a bug.

   ```bash
   rg -n -e 'with_for_update|FOR UPDATE|advisory_lock' -e 'asyncio\.(gather|create_task)|BackgroundTasks' -e 'retry|idempoten' -e 'status\s*[:=]' -e 'Decimal|round\(' app/ src/
   ```

   A good target is a promise the code makes, whose break harms a user, and that tests rarely reach: no double charge under two concurrent requests, a retry never applied twice, a balance never negative, a parser that never accepts what it cannot print. Pick the strongest target, not the easiest one. Write the promise in one sentence and the harm in another.

2. **Let the question choose the tool**, and say why in the report:

   | The question | Tool |
   | :- | :- |
   | Can steps happen in a bad order: interleaved requests, a retry, a crash between two writes? | TLA+, checked by TLC, over a small model of the design |
   | Does one function hold for every input: a calculation, an invariant of a data structure? | Lean, over a faithful model of the function |
   | The same, but on the real code instead of a model | A verifier that runs on the language, such as CrossHair for Python |

   When no verifier runs on the code and a model would be a guess, say so, and test the real code with generated inputs instead (Hypothesis, fast-check), reported as a test, never as a proof. Prefer a tool the project's developers can install and run.

3. **Build the check to these bars:**
   - **True to the code.** Every variable, action, and definition maps to a named file and function. One atomic step in the model is one atomic step in the code, such as one transaction. Names come from the code.
   - **Able to fail.** Every property is shown failing on a deliberately broken variant: a removed lock, a reordered write, a dropped guard. A property never seen failing proves nothing.
   - **Findings stay findings.** When the current code breaks the property, report the counterexample as steps in the code's words. Never weaken the property or the model until it passes, and never change product code unless the owner asks.
   - **Honest about scope.** State what is verified, the bounds (how many requests, retries, items), the assumptions, and what is left out. A pass covers the model within its bounds, nothing more.
   - **One command reruns it**, with a pinned tool version, fast enough to run on every relevant change.

4. **Write the new skill.** Copy `assets/verification-skill.template.md` to `.agents/skills/agentic-verify-<area>/SKILL.md`, where `<area>` is a kebab-case name for the verified area. The name must start with `agentic-`, and the folder name must equal it.
   - Put the model in the skill's own `model/` folder: `<Module>.tla` and `<Module>.cfg` for TLA+, or a Lake project with its `lean-toolchain` for Lean.
   - Fill every field: the property, the harm, the coverage table, the bounds, the rerun command, how to read a failure, and the broken variants.
   - Record the sync commit with `git rev-parse HEAD`.
   - Check that no placeholder is left: `rg -n "\{\{" .agents/skills/agentic-verify-<area>/` prints nothing.
   - Add one row for the new command to the project's `AGENTS.md` skills table, because a skill nothing points at is never used.

5. **Prove the new skill works**, following only its own text, as the next agent would:
   - Make a scratch change in the real code that breaks the property, such as deleting the lock the model relies on.
   - Run the skill's command. It must catch the break.
   - Undo the scratch change exactly, confirm with `git diff --stat` that none of it remains, and rerun: the result must match where you started, passing or failing only on the findings you report.
   - If the skill misses the break or a step does not run, fix the skill or the model, never the scratch change.

## Output

```text
Verified:   no order is charged twice, in app/orders/service.py:place_order
Harm:       a customer pays twice for one order
Tool:       TLA+ with TLC 2.19, because the risk is two requests interleaving between the read and the write
Bounds:     2 concurrent requests, 1 retry each, 1 order
Assumes:    PostgreSQL serializes SELECT ... FOR UPDATE on one row
Found:      1 finding. A retry after a timeout charges again: request A times out after the charge, A retries, the charge runs twice.
Rerun:      java -XX:+UseParallelGC -cp "$TLA2TOOLS" tlc2.TLC -workers auto -config model/Orders.cfg model/Orders.tla
Not covered: refunds, the payment provider's own retries
Skill:      .agents/skills/agentic-verify-order-charge/, caught the scratch removal of with_for_update()
```

Suggest a second target only when you found a close one.
