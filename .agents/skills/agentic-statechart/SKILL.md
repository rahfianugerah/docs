---
name: agentic-statechart
description: Draws a feature's statechart from the code as a Mermaid stateDiagram-v2 and lists the bugs it reveals, namely state and event pairs nothing handles, states with no way out, and states nothing reaches. Each comes with the shortest event path to it, replayed against the real code before it is reported. Optionally models the same machine in TLA+ and checks it with TLC when Java and TLC are installed. Use before building a flow with complex state (checkout, auth, uploads, multi-step forms, retries, background jobs), or when a bug looks like "it only breaks if you do X while Y".
---

# Statechart

The chart shows how a feature moves between states, in the words of the person who decides whether that behaviour is right. Its value is the gaps: the event that can arrive in a state where no code decides what happens.

## Steps

1. **Bound the feature.** Name its entry points (a route, a component, a job) and the files it spans. Everything below stays inside them.

2. **List the states, the events, and the guards from the code**, each with `file:line`.

   ```bash
   rg -n -e 'Enum\)' -e 'Literal\[' -e 'status\s*[:=]' -e 'type \w*(State|Status)\w* =' -e 'useReducer|useState<' -e 'isPending|isError|isSuccess|isFetching' <paths>
   ```

   - **States**: status enums and columns, union types, and the combinations of boolean flags. Two booleans make four states; say which of the four are meant to exist.
   - **Events**: user actions, responses and failures, timeouts, background jobs, navigation and the back button, a refresh, a second click, a second tab, a concurrent request.
   - **Guards**: the conditions that decide which way an event goes.

3. **Draw the chart** as a Mermaid `stateDiagram-v2`:
   - name each state by what the user sees or cares about ("Paying", "Payment failed"), never by a variable
   - label each arrow with the event as the user experiences it ("you press pay", "the bank declines"), and a guard in brackets after it
   - about twenty arrows at most: merge states that behave the same, and drop a detail nobody decides on, but keep every state on a finding's path

   ```mermaid
   stateDiagram-v2
     [*] --> Cart
     Cart --> Paying: you press pay
     Paying --> Paid: the bank accepts
     Paying --> Failed: the bank declines
     Failed --> Paying: you press retry [fewer than 3 tries]
     Paid --> [*]
   ```

4. **Answer every state and event pair.** Build a table with one row per state and one column per event. Each cell says what the code does, with `file:line`: the next state, "ignored, correctly", or **unhandled**. A cell answered from memory instead of the code is not answered. Then list:
   - **Unhandled pairs**: an event that can arrive in a state where no code decides the outcome, such as "you press pay again while Paying".
   - **Dead ends**: a state that is not final and has no way out, such as "Failed" after the third retry.
   - **Unreachable states**: a state the code defines and no path enters.
   - **Impossible combinations the types allow**, such as `isPending` and `isError` both true.

5. **Give the shortest event path to each finding**, from the start state, in the user's words:

   ```text
   F1 Failed is a dead end: open checkout, press pay, bank declines, press retry, bank declines, press retry, bank declines.
   ```

6. **Replay each finding against the real code before reporting it**, one step per event: a pytest or Playwright test, or a live repro with the exact steps. If it reproduces, it is a finding with that evidence. If it does not, the chart is wrong: fix the chart and redo step 4. A finding that could not be replayed is listed as "not confirmed" with the reason.

7. **Optional: check the machine in TLA+.** Only when both are present:

   ```bash
   java -version
   test -f "$TLA2TOOLS" && echo "TLC found"
   ```

   Model the same states, events, and guards, write each rule the reader agrees to as an invariant, and run TLC: it finds the shortest trace to every broken rule and every dead end. Follow `references/tla.md`. When Java or TLC is missing, skip this step and say so; never install a tool unasked.

## Output

- The chart, as a `mermaid` code block.
- The state and event table, or at least its unhandled cells.
- The findings, each with its kind, its shortest path, and its replay evidence:

  ```text
  F1 dead end      Failed after 3 declines: no retry, no cancel. Replayed: test/e2e/checkout.spec.ts "third decline" fails.
  F2 unhandled     press pay while Paying sends a second charge. Replayed: test_double_submit charges twice.
  F3 not confirmed back button while Paying: needs a staging bank stub to replay.
  ```

- What the chart leaves out: merged states, hidden events, and the model's bounds if step 7 ran.
