# TLA+ Notes for a Statechart

The optional second step of `/agentic-statechart`: the same machine as the chart, written in TLA+ and checked by TLC. TLC visits every state the model can reach, so it finds the orderings a person drawing the chart did not think of.

## Setup

- Java 11 or later, and `tla2tools.jar` from the TLA+ project's GitHub releases.
- Set `TLA2TOOLS` to the jar's full path once per machine. The skill checks that variable before this step runs.
- Work in a scratch folder outside the repository. TLC writes its working files to `states/` beside the spec.

## From the Chart to the Model

| Chart | TLA+ |
| :- | :- |
| A state | A value of one variable, such as `state \in {"cart", "paying", "paid", "failed"}` |
| A value a guard reads | One more variable, such as `retries` |
| The start state | `Init` |
| An event | One named action: its guard is the enabling condition, and its effect sets the primed variables |
| Every event at once | `Next`, written as a disjunction of the named actions, so a trace names each step |
| A rule the reader agrees to | An `INVARIANT` for a fact about one state, a `PROPERTY` for a fact about a step or about the future |
| A correct final state | An action that is true only there and changes nothing, so TLC does not report it as a deadlock |

Write the rules from what the reader cares about, never from what the code happens to do. If the model has no variable a rule needs, add the variable.

## Example

`Checkout.tla`:

```tla
---- MODULE Checkout ----
EXTENDS Naturals

CONSTANT MaxRetries

VARIABLES state, retries

vars == <<state, retries>>

TypeOK ==
    /\ state \in {"cart", "paying", "paid", "failed"}
    /\ retries \in 0..MaxRetries

Init == state = "cart" /\ retries = 0

YouPressPay   == state = "cart" /\ state' = "paying" /\ UNCHANGED retries
BankAccepts   == state = "paying" /\ state' = "paid" /\ UNCHANGED retries
BankDeclines  == state = "paying" /\ state' = "failed" /\ UNCHANGED retries
Finished      == state = "paid" /\ UNCHANGED vars

YouPressRetry ==
    /\ state = "failed"
    /\ retries < MaxRetries
    /\ state' = "paying"
    /\ retries' = retries + 1

Next == YouPressPay \/ BankAccepts \/ BankDeclines \/ YouPressRetry \/ Finished

Spec == Init /\ [][Next]_vars

\* A paid order never leaves the paid state.
PaidIsFinal == [][state = "paid" => state' = "paid"]_vars
====
```

`Checkout.cfg`:

```text
SPECIFICATION Spec
CONSTANT MaxRetries = 2
INVARIANT TypeOK
PROPERTY PaidIsFinal
```

Check the syntax, then the model:

```bash
java -cp "$TLA2TOOLS" tla2sany.SANY Checkout.tla
java -XX:+UseParallelGC -cp "$TLA2TOOLS" tlc2.TLC -workers auto -config Checkout.cfg Checkout.tla
```

TLC reports `Deadlock reached`: after two declined retries the order sits in `failed` and no action is enabled. That is the dead end the chart should show, and the finding is "the customer is stuck on Payment failed with no retry and no cancel".

## Reading the Output

- `Model checking completed. No error has been found.` means every rule holds in every reachable state, within the constants in the config.
- An error line naming what broke, such as `Invariant TypeOK is violated.` or `Deadlock reached.`, is followed by a trace: `State 1` is the start, and each later state names the action that produced it.
- Translate the trace into the chart's words, one event per step, and replay it against the real code exactly as step 6 of the skill says. A trace that does not reproduce means the model is wrong, not the code.

## Rules That Keep the Check Honest

- **Never weaken a rule to make it pass.** A broken rule is a finding, reported with its trace.
- **Show every rule failing once**: break the model on purpose, such as dropping a guard, and confirm TLC catches it. A rule never seen failing proves nothing.
- **Keep the constants small**: two or three of each thing. Most ordering bugs show up with two requests and one retry. If the state count grows past a few hundred thousand, shrink the constants or add a `CONSTRAINT`.
- **A liveness rule needs fairness.** "Paying always ends" is `state = "paying" ~> state # "paying"`, checked as a `PROPERTY`, and holds only if the spec adds `WF_vars(BankAccepts \/ BankDeclines)`. Say in the report which fairness the model assumes.
- **State what the model leaves out**: the bounds, the merged states, and every assumption, such as the bank always answering.
