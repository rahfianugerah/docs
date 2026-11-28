# Lesson Entry Format

Every edit the harness-improver probes, kept or rejected, becomes one entry appended to `harness/lessons.md`. An entry is a heading and four lines, in this order, and nothing else:

```markdown
### <cue>
Lesson: <what to do, or not do, in that situation, naming the harness component>
Evidence: <the motivating run, the probe runs per side, and their numbers>
Confidence: <low, medium, or high>
Verdict: <helped, hurt, no observed effect, or confounded>
```

| Line | Holds | Rule |
| :- | :- | :- |
| `### ` heading | The cue: the shape of situation the lesson applies to | A pattern that can recur in another task, not this task's facts. "A verifier brief that names no test command", not "T-03 of login-otp" |
| `Lesson:` | The operation, and the component it lives in | One sentence. For a rejected edit, what not to do, or that the edit changed nothing |
| `Evidence:` | The runs behind the verdict | The report path or usage log of the motivating moment, then per side: the runs, the passes, the fix rounds, and the tokens per successful task |
| `Confidence:` | `low`, `medium`, or `high` | Set by the table below |
| `Verdict:` | `helped`, `hurt`, `no observed effect`, or `confounded` | As measured in the probe, never as hoped |

## Confidence

| Value | When |
| :- | :- |
| `low` | The runs on a side disagree, the difference is within noise, or the verdict is `confounded` |
| `medium` | Two or more runs per side agree, on one task |
| `high` | The runs agree on two or more different tasks |

## Rules

- One entry per probed edit. An edit probed again gets a new entry, and the newest entry for a cue is the one that holds.
- Each line is one line, however long; never wrap it.
- Record every verdict, `hurt` and `no observed effect` included: a rejected edit on record is what stops the next round proposing it again.
- A lesson resting only on a `confounded` probe claims nothing beyond what the runs show.
- No secret, token, environment value, or personal data. Name the file, never paste the value.
- Where `harness/lessons.md` does not exist yet, create it with the title `# Harness Lessons` and append the first entry below it.

## Example

```markdown
### A verifier brief that names no test command
Lesson: Put the project's test command in the verify field of every reviewer brief, so the verifier does not search the repository for one.
Evidence: Motivating moment ~/agentic/report/shop-backend/report-verifier-to-user-login-otp-20261120-09_02_44.md, 41k tokens spent finding the test runner. Probe on login-otp W-1, 2 runs per side: base 2 of 2 Pass, 0 fix rounds, 63k and 66k tokens per successful task; edited 2 of 2 Pass, 0 fix rounds, 38k and 40k.
Confidence: medium
Verdict: helped
```
