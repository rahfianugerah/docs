---
name: agentic-no-slop
description: Removes comments that restate the code and dead code, and flags quick-fix patterns (a zero-delay timer, a sleep or retry that hides a failure, a broad catch, a skipped test, a suppression with no reason) in the current diff or a given path. Use before a handoff or a review, when a diff carries narration comments or leftovers, or when asked to clean up slop. Reports counts and open items.
---

# No Slop

Cut what a reader has to skip, and surface what a reader must not miss. A deleted comment costs nothing; a hidden workaround costs a bug later, so a hidden workaround is reported, never deleted.

## Scope

The paths the caller names. Otherwise every file changed against the base branch, plus untracked files:

```bash
git diff --name-only --merge-base main
git ls-files --others --exclude-standard
```

Edit only files in scope. Search the whole repository when proving something is unused.

## Steps

1. **Collect candidates with tools before reading anything.**

   ```bash
   ruff check --no-fix --output-format concise --select F401,F841,ERA001,BLE001,E722,S110,PGH003,PGH004,RUF100,FIX001,FIX003,FIX004,ASYNC251 <paths>
   npx tsc --noEmit --noUnusedLocals --noUnusedParameters
   npx eslint --report-unused-disable-directives <paths>
   rg -n -e 'setTimeout\([^)]*,\s*0\s*\)' -e 'setTimeout\(\s*\w+\s*\)' -e 'asyncio\.sleep\(0\)' -e 'time\.sleep|asyncio\.sleep|waitForTimeout' -e 'retry|retries|tenacity|flaky|reruns' -e '\.(skip|only|fixme)\(' -e 'pytest\.(mark\.)?(skip|xfail)' -e 'noqa|type: ignore|@ts-ignore|@ts-expect-error|eslint-disable' -e 'catch\s*(\([^)]*\))?\s*\{\s*\}' -e 'except\s*(Exception|BaseException)?\s*:' <paths>
   ```

   Skip a command whose language the scope does not contain.

2. **Classify every comment in scope**, one row of this table each:

   | The comment | Action |
   | :- | :- |
   | Restates the code, narrates a change ("added", "fixed", "now uses"), names a ticket with no why, or is a banner or divider | Delete |
   | Is commented-out code | Delete; git keeps it |
   | Contradicts the code | Delete it, and report the mismatch when the code may be the wrong half |
   | Gives a non-obvious why: a constraint, an invariant, or a workaround with a link to the issue or upstream bug | Keep, cut to one line |
   | Is the one-line file header, or a public symbol's one-line docstring, that the project requires | Keep; shorten it if it repeats the signature |
   | Hides a workaround or a suppression: "hack", "temporary", "for now", "workaround" with no link, or text that explains away a suppression | Finding: keep it and report it open |
   | Guards a constraint: "do not remove", "do not change", "keep in sync with", "ask X before changing" | Step 4 |

   A `TODO(<owner>): <action>` line is kept. A bare TODO, FIXME, XXX, or HACK is a finding.

3. **Remove dead code**: unused imports, variables, parameters, and functions, unreachable branches, flags that never change, and commented-out code.
   - Prove a symbol is unused before deleting it: `rg -n -w <name>` over the whole repository returns only its definition.
   - Check dynamic use too: route and task registration, string lookups, `__all__`, and package exports.
   - A symbol another repository may import (a public package export, an endpoint) is reported, not deleted.

4. **Turn each constraint comment into a check.** Find what it protects, then propose the cheapest encoding:
   - a type: `Literal`, `Enum`, `Final`, `readonly`, or a union
   - a test that fails when the constraint breaks
   - a lint rule; an import constraint goes to `/agentic-boundaries`

   Ask the owner. Approved: write the encoding, show it failing on a deliberate break, then delete the comment. Not approved, or running unattended: keep the comment and report the constraint open.

5. **Flag quick-fix patterns, and fix none of them here.** Each is a symptom whose cause nobody found:

   | Pattern | Why it is a finding |
   | :- | :- |
   | `setTimeout(fn, 0)`, `setTimeout(fn)`, `asyncio.sleep(0)` | Reorders work to dodge a race instead of fixing the order |
   | A sleep, a wait, or a retry added where a failure was seen | Makes a timing bug rarer, not gone |
   | `except Exception`, a bare `except`, an empty `catch {}` | Turns a crash with a trace into silent wrong state |
   | A skipped or `only` test, `xfail`, `fixme`, rerun on failure | Removes the signal instead of the bug |
   | `noqa`, `type: ignore`, `@ts-ignore`, or `eslint-disable` with no specific rule and no reason | Silences the tool that found the problem |

   A suppression that names one rule and gives a one-line reason, such as `// eslint-disable-next-line no-console -- CLI output`, is kept. A retry that is part of the design, such as a backoff on a network call with a documented limit, is kept. Every flag is routed to `/agentic-root-cause`.

6. **Check the edits changed no behaviour.** Rerun the step 1 linters, then the formatter and type check on the edited files:

   ```bash
   ruff format <paths> && ruff check <paths>
   npx eslint <paths> && npx tsc --noEmit
   ```

   A deletion that breaks a check is restored and reported. The test suite runs at verify, not here.

## Output

```text
Scope: 14 files, diff against main
Comments: 23 deleted, 6 kept, 2 findings
Dead code: 4 symbols removed, 61 lines
Quick-fix flags: 3
Constraints: 1 encoded as a test, 1 open
Open items:
- app/orders/service.py:88  broad except swallows the payment error; route: /agentic-root-cause
- src/features/cart/useCart.ts:40  setTimeout(fn, 0) before the refetch; route: /agentic-root-cause
- app/billing/models.py:12  "keep in sync with the invoice template": encoding not approved
```

Every open item carries a file, a line, what it is, and where it goes next.
