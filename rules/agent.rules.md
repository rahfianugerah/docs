---
tags:
  - kind/rule
  - layer/docs
  - topic/memory
  - topic/workflow
---

> Up: [[README.md]]

# Agentic Session Standard

> [!important]
> A generation is one continuous stretch of work on one concern, summarized as it ends into its own memory note.

## Core Requirement

When an agentic coding tool such as Claude Code or Codex works in a repository, the work it does across a session must end up in the memory, not only in the transcript.

A transcript is lost when the window closes. A memory note survives, is searchable, and is what the next session reads instead of asking the same questions again. This policy decides when a note is written, how many, and what happens when a session ran long before anyone asked.

It governs the agent's behaviour. [[memory.rules.md]] governs the shape of the note it writes, and this file does not repeat it.

## A Generation Is the Unit

A **generation** is one continuous stretch of work on one concern: a feature built, a bug traced to its cause, a migration run, an investigation that reached an answer. It usually spans several turns, and a long session holds more than one.

A generation is not a turn. Ten turns spent on one bug are one generation, and one turn that answers three unrelated questions is three.

The boundary is the concern, not the clock. A generation ends when the thing being worked on is finished, abandoned, or replaced by something unrelated.

## Summarize at the End of Every Generation

**When a generation ends, summarize it before starting the next one.** Do not wait to be asked, and do not carry an unsummarized generation into new work.

A summary at this point is cheap: the reasoning is still in context, the rejected approaches are still known, and the reason a thing was done a particular way has not yet been compressed into "it works". An hour later all of that has to be reconstructed from a diff, and the reconstruction loses exactly the part worth keeping.

The summary is held in the session, not written to disk. It becomes a note when the user asks to save the memory.

## Report the Generation in Bahasa Indonesia

> [!important]
> **Every explanation of what was generated is written in Bahasa Indonesia.** The summary at the end of a generation, the report of what changed, what was skipped, and why: all of it, always, without being asked.

This is about **what the agent says to the person**, not about what it writes to disk. The two are separate and the distinction is the whole rule.

| Written in Bahasa Indonesia | Stays as its own standard says |
| :- | :- |
| The end-of-generation summary | Code identifiers, which are English per [[codes.rules.md]] |
| The report of what was created, changed, or deleted | Commit messages, which are English per [[commit.rules.md]] |
| What was deliberately not done, and why | Pull request titles and bodies, per [[pr.rules.md]] |
| A finding, a trade-off, or a rejected approach | A vault document, which is English per [[docs.rules.md]] |
| A question back to the user, and any warning | A project document, which follows its readers' language per [[prd.rules.md]] |
| The reason a rule was followed or a deviation was taken | A memory note, which follows [[memory.rules.md]] |

**A technical term keeps its original form.** A library name, a framework, a command, a file name, a variable, a database field, a route path, and an error message are quoted as they are. Writing "berkas konfigurasi lingkungan" where the thing is called `.env.example` makes the sentence longer and the reference harder to find.

Rules:

1. **Report in Bahasa Indonesia even when the work was entirely in English.** Rewriting a rules document, which is an English artifact, is still explained in Bahasa Indonesia, because the explanation is for the person and the artifact is for the repository.
2. **Do not translate the artifact to match the report.** The report being Indonesian never licenses renaming an identifier, retitling a commit, or rewriting a vault document.
3. **Name the file and the section in their real form.** `rules/docs.rules.md`, not a translated description of it, so the path in the report is the path the reader opens.
4. **Say what was skipped, in the same language.** A generation that produced nothing durable, a rule that could not be satisfied, or a check that was not run is reported as plainly as the work that succeeded.
5. **A warning is reported before the work it concerns, not after.** Where a request conflicts with a standard, say which standard in Bahasa Indonesia and say it first, per the conflict resolution every rules document carries.

## On "Save the Memory"

When the user says to save the memory, write the notes and digest them, per [[memory.rules.md]].

How many notes depends on how many generations went unsummarized:

| State when the user asks | Write |
| :- | :- |
| One generation, summarized as it ended | One note |
| Several generations, each summarized as it ended | One note per generation |
| **Several generations, none summarized** | **One separate note per generation, reconstructed** |

> [!warning]
> **An unsummarized run does not collapse into one note.** Writing one note is faster than writing three, which is exactly why this rule is the one most often broken.

If a first, second, and third generation all went by without a summary, the result is three notes, not one covering all three.

A single note spanning three concerns cannot be corrected, superseded, or linked to precisely, and it will rot as one unit the moment any part of it stops being true. That is the same reason [[memory.rules.md]] says one note holds one thing.

Reconstructing three notes late is worse than writing three summaries on time, and it is still better than one note that mixes them. Where a generation genuinely cannot be reconstructed, say so rather than guessing: a note invented from a diff is a note the next session will trust.

## Applying the Test

Each generation is tested on its own against [[memory.rules.md]]: **would the next session waste time without this?**

- A generation that fails the test is not written. Three generations do not mean three notes if two of them produced nothing durable.
- A generation that fails still gets said out loud. "Nothing worth keeping from the refactor" is an answer; silence looks like an omission.
- Never write a note per turn. A memory full of turn-level noise is a memory nobody reads.
- Never write the transcript. A note carries the finding and the reason, not the sequence of what was tried.

## What Each Note Carries

Beyond the shape [[memory.rules.md]] fixes, a note from a generation carries the part a diff cannot show:

- **The reason**, in the `**Why:**` line. What the code does is in the code; why it does it that way is only in someone's head until it is written down.
- **What was rejected**, in a `decision` note. The approach that did not work is what stops it being tried again next quarter.
- **The symptom that misled**, where the work was a bug. The error that pointed at the wrong file is worth more than the fix.
- **Nothing the code and git history already say.** A note restating a diff is noise with a date on it.

## Keeping a Working Script

Where a generation produced a script worth running again, the script goes in `memory/codes/` and its note goes beside it, per [[memory/codes.rules.md]]. The note is what the memory holds and what `recall` finds; the script is the attachment.

This is the one case where a generation produces two files instead of one, and it is still one note.

## Reading Before Answering

An agent that answers from general knowledge when the memory holds the answer has wasted the memory. Follow the recall order in [[memory.rules.md]]: the note if its name is known, then semantic search, then the code map, then the code itself.

Call `recall` before answering anything about a project's rules, decisions, architecture, or history. Pass the brain, which is the folder's own name lowercased.

## Do and Do Not

Do:

- Summarize a generation as it ends, before starting the next one.
- Write one note per generation when the user asks to save the memory.
- Reconstruct a separate note per generation when several ran unsummarized.
- Test each generation on its own, and say when one produced nothing worth keeping.
- Digest after writing, so recall can find the notes.

Do not:

- Collapse several unsummarized generations into one note.
- Write a note per turn.
- Write the transcript, or restate what the diff already shows.
- Write into the index directly. It is derived, and a direct write is gone at the next rebuild.
- Invent a note for a generation you cannot actually reconstruct.

## Definition of Done

- Every generation in the session was summarized as it ended, or reconstructed at the end.
- The number of notes matches the number of generations that passed the test.
- No note covers two concerns, and no note covers a single turn.
- Every note follows [[memory.rules.md]]: one thing, frontmatter, the reason written down, one paragraph per line.
- The memory was digested after the notes were written.
- Any generation that produced nothing durable was named as such rather than left unmentioned.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This agentic session policy
4. [[memory.rules.md]]
5. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[memory.rules.md]]
- [[memory/codes.rules.md]]
- [[note.template.md]]
- [[commit.rules.md]]
- [[pr.rules.md]]
