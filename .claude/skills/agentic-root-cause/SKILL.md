---
name: agentic-root-cause
description: Analyses a bug to its root cause before any fix, and forbids a patch fix. Reproduce it, state the symptom and the expected behaviour, trace back to the first wrong state, find every caller of the code about to change, name the cause in one sentence with evidence, then fix where every caller routes through, behind a regression test that failed first. Use before fixing any bug, on a verifier's Fail, or on a quick-fix flag from /agentic-no-slop. Stops and escalates when the honest fix is larger than the task allows.
---

# Root Cause

A bug report names a symptom. The fix goes where the system first did something wrong, not where the damage showed. A patch at the symptom leaves the cause in place and every other caller still broken.

## Steps

1. **Reproduce it.** Write the smallest repro, a failing test when one can be written:

   ```bash
   pytest test/<area>/test_<module>.py::test_<case> -q
   npx playwright test test/e2e/<flow>.spec.ts
   ```

   Otherwise, the exact command or clicks and the output they give. Run it and watch it fail. A bug you have not seen fail is not ready to fix: report what you tried, with status `Blocked`.

2. **State the symptom and the expected behaviour**, one line each, in terms anyone can observe:

   ```text
   Symptom:  POST /api/v1/orders returns 500 when the cart is empty.
   Expected: 422 with the standard error shape.
   ```

3. **Trace from the symptom back to the first wrong state**: the first value, row, or decision that differs from what it should be.
   - Read the real state, never a guess: a debugger, a temporary log line removed afterwards, a query against the test database.
   - Ask why at each hop until the answer is a wrong decision in the code, not another symptom.
   - Decide whether the state that triggered it is legitimate. If the system must accept it, such as an empty cart, handle it where the code first mishandles it. If it must never exist, a check where it surfaced only hides it: keep tracing to whatever produced it.

4. **Find every caller of the code about to change.**

   ```bash
   rg -n -w <function_or_class> .
   ```

   Add the callers a search misses: route and task registration, string lookups, signal handlers, and the frontend calls of an endpoint. For each caller, note whether the same bug reaches it. Then search for the same faulty pattern elsewhere, because a fault written once is often written twice.

5. **Name the root cause in one sentence, with the evidence.**

   ```text
   Root cause: order_total() returns None for an empty cart, and every caller passes it to the tax step.
   Evidence:   test_empty_cart fails with TypeError at app/orders/service.py:42; trace in the report.
   ```

   If you cannot write that sentence and point at the evidence, you have not found the cause: go back to step 3.

6. **Check the honest fix fits the task.** It does not fit when it crosses a boundary, changes an API contract or a migration, touches a path the brief forbids, or is larger than the task. Then stop, change nothing, and report to the advisor, or to the owner when you are the advisor:
   - the root cause and its evidence
   - the honest fix, its files, and its size
   - what a smaller patch would hide

   Return `Needs Decision`. Never ship a patch in the meantime. "That would be a larger change" is a reason to escalate, never a reason to patch.

7. **Write the regression test first.** It encodes the expected behaviour at the level of the cause, not the symptom. Run it and watch it fail for the stated reason, not for an import error or a typo.

8. **Fix at the one place every caller routes through.** Then run the regression test, which now passes, and the tests of every caller from step 4.

## Patches That Are Not Fixes

- A guard, a default, or a `try` at the symptom that makes the bad state silent.
- A sleep, a retry, or a zero-delay timer.
- A skipped, loosened, or deleted test.
- A suppression comment: `noqa`, `type: ignore`, `@ts-ignore`, `eslint-disable`.
- A special case for the one input in the report.
- A value clamped or discarded instead of finding what produced it.

A guard is a fix only when the state it handles is legitimate and the guard sits where that state first enters, such as input validation at the API boundary.

## When the Dig Was Long

If finding the deciding fact took a long trace, propose one cheap, always-on signal that would have shown it at first look: a log line carrying the request id, an assertion at the boundary, or a narrower type. Propose it; the owner decides.

## Output

```text
Symptom:      POST /api/v1/orders returns 500 when the cart is empty
Expected:     422 with the standard error shape
Repro:        pytest test/orders/test_service.py::test_empty_cart -q   (failed: TypeError)
First wrong:  app/orders/service.py:42, order_total() returns None for no lines
Callers:      3, all affected: app/orders/router.py:18, app/orders/jobs.py:30, app/billing/service.py:77
Root cause:   order_total() returns None for an empty cart, and every caller passes it on
Evidence:     the failing test, the trace, line 42
Fix:          app/orders/service.py:42, the one place all three callers route through
Regression:   test_empty_cart failed before the fix and passes after it
Status:       Done
```

Or the step 6 report with status `Needs Decision`, and no code changed.
