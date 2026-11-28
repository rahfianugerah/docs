> Up: [[harness/README.md]]

# Harness Lessons

> [!info]
> Every entry here is backed by a real run. The harness-improver writes one after it probes an edit, and `sync_agents.py --check` rejects an entry with no evidence.

Each entry is a `###` heading that holds the cue, followed by four one-line paragraphs: `Lesson:`, `Evidence:`, `Confidence:` (low, medium, or high), and `Verdict:` (helped, hurt, no observed effect, or confounded). A verdict of confounded is the honest one when a single run stands behind the difference.

## Lessons

### A one-file task whose only build step is a few lines

Lesson: Do not expect tier routing to lower the cost of a task this small; the orchestrator and the three reviewers on the deep tier are the spend, so cut their context before touching the build tier.

Evidence: Task dockerignore-env-files on cloud/gcp/deploy.rules.md, 1 run per side, logs harness/usage/routed.json and harness/usage/all-deep.json. Routed: Pass by all three reviewers, 0 fix rounds, 1.268 USD, of which the build agent on the build tier was 0.077 USD. Every agent on the deep tier: Pass by all three reviewers, 0 fix rounds, 1.235 USD. The orchestrator alone read about 690k cached tokens over 10 calls in both runs, and the reviewers' call counts differed between the runs by more than the build agent's whole cost.

Confidence: low

Verdict: confounded
