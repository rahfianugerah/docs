---
type: reference
created: 2026-08-18
updated: 2026-08-18
tags: [plugmybrain, ingest, cost, code]
status: current
---

# A repeat digest of an unchanged folder embeds nothing

`codes/plugmybrain/2026-08-18-check-digest-is-incremental.py` digests a folder twice and prints the embedded chunk count on each side, so the question is settled by two numbers rather than by reading the pipeline.

- Measured on the `plugmybrain` folder itself: 260 chunks before the repeat digest and 260 after.
- The second run took about 20 seconds, nearly all of it container startup rather than embedding.
- It reads `DocumentChunk_text` directly, because `pmb list` reports documents rather than chunks and a document count does not move when chunks are duplicated.

**Why:** the corpus is roughly 51k embedding tokens, so whether that is paid once or on every digest changes how the tool is used day to day, and it decided against building `--code-only` and `--docs-only` flags that would have saved nothing.
**Applies to:** any decision about digest frequency, and any future change to the task list in `ingest.py`.

## Related

- [[memory/codes.rules.md]]
- [[memory.rules.md]]
