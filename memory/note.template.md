> Up: [[README.md]] · [[memory/README.md]]

# Note Template

Every memory note uses this shape. Copy the block for the type you need into the matching folder, and name the file after a kebab-case slug of its title.

The protocol is [[memory.rules.md]].

## Fact

`memory/fact/<slug>.md`

```markdown
---
type: fact
created: 2026-02-11
updated: 2026-02-11
tags: [project-x, environment]
status: current
---

# Project X runs in the conda env `projectx-ml`

The environment is defined by `environment.yml` at the repository root and pins Python 3.13.

**Why:** the project depends on CUDA builds that pip cannot resolve correctly.
**Applies to:** any setup, run, or CI step for project X.

Related: [[codes.rules.md]]
```

## Decision

`memory/decision/<slug>.md`

```markdown
---
type: decision
created: 2026-02-11
updated: 2026-02-11
tags: [project-x, data]
status: current
---

# The loader uses Polars, not pandas

**Decision:** read the raw parquet with Polars in streaming mode.

**Why:** the file is 40GB and pandas loads it fully into memory, which the machine does not have.

**Rejected:** pandas with chunking, which worked but ran 6x slower and needed manual chunk joins.

**Cost accepted:** a second dataframe library in the project, and Polars syntax in the loader only.

Related: [[fact/project-x-env.md]]
```

## Session

`memory/session/YYYY-MM-DD-<slug>.md`

```markdown
---
type: session
created: 2026-02-11
updated: 2026-02-11
tags: [project-x, bug]
status: current
---

# Found the scaler leak in preprocess.py

The validation score was 0.94 and the test score 0.71. The scaler was fitted on the full
dataset before the split, so the test distribution reached training.

**Fix:** moved the split above the fit. Test score is now 0.78, which is the real number.

**Lesson:** a validation score far above the test score is a leak until proven otherwise.

Related: [[decision/loader-uses-polars.md]]
```

A session note is what Graphiti ingests as an episode, so its `created` date is the valid time of what it describes, not the day it was typed up.

## Reference

`memory/reference/<slug>.md`

```markdown
---
type: reference
created: 2026-02-11
updated: 2026-02-11
tags: [project-x, data]
status: current
---

# Dataset X licence and terms

https://example.org/dataset-x/licence

**Why it matters:** attribution is required and redistribution is not permitted, so the raw
data never goes into a public repository or a model hub.

Related: [[secret.rules.md]]
```

## Related

- [[memory.rules.md]]
- [[memory/README.md]]
- [[docs.rules.md]]
