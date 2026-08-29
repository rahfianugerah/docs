---
tags:
  - kind/rule
  - layer/docs
  - topic/workflow
---

> Up: [[README.md]]

# Journal Standard

> [!important]
> A journal records one piece of work after it is finished: what was wrong, what was found, what was done, and what changed as a result. It is written as a story with numbers in it, not as a changelog.

## Core Requirement

A journal is written when a piece of work ends: a fix that took real digging, a feature that shipped, a migration that landed, an incident that was resolved. It goes in `journal/` at the workspace root, **one file per project per day**.

**A journal records the author's own commits and nobody else's.** Work by another person in the same repository belongs to that person's journal, so a day whose commits are entirely someone else's gets no journal at all.

It answers four questions in order, and a journal missing any of them is incomplete:

1. **What was wrong**, in the words the person who reported it used.
2. **What was actually found**, including the wrong turns, because the wrong turn is the part a future reader repeats.
3. **What was done**, with the real commit and the real file.
4. **What changed**, as a number measured before and after.

> [!warning]
> A journal is not a commit log. `git log` already lists every change and does it better. A journal exists for the part git cannot hold: why the obvious explanation was wrong, what the error message pointed at versus what actually broke, and what the fix cost.

## Three Kinds of Record, and Which One This Is

The vault holds three ways of writing down what was learned, and they are not interchangeable.

| Kind | Answers | Ages |
| :- | :- | :- |
| A **journal**, here | What happened on this day, to this project, with numbers | Never. It is dated and describes one moment |
| A **memory note**, per [[memory.rules.md]] | What is true now, and why it was decided | When the file it names changes |
| A **pattern**, per [[pattern/README.md]] | A mechanism that repeats, generalized away from where it happened | When the technology does |

**A journal is the raw material for the other two.** A finding worth carrying past the day it was found becomes a memory note; a mechanism worth carrying past the project becomes a pattern. Writing the journal first is what makes those two possible, because the detail they distil is gone within a week otherwise.

## One Journal Per Project Per Day

**There is one journal per project per day, and no second kind of journal file.** Work that has a single cause, a single fix, and a measurable result is written as an `## In Depth` section inside that day's journal, not as a file of its own.

The reason is that a slug in a filename splits one day's record into two places, and a reader looking for what happened on a date then has to know a second name to find half of it.

A day of work has no single measurement, and demanding one would mean inventing it. `## Problems Solved` measures each problem separately instead. **The requirement for one measured before and after applies only inside an `## In Depth` section**, where the work genuinely has a single result.

### What a Journal Must Hold

**A list of commit subjects is not a journal.** `git log --oneline` already produces that, and produces it better. A journal a reader could have generated with one command was not worth writing.

A journal tells what the day was spent on, in prose, and then accounts for every problem it closed. It carries these sections, in this order:

| Section | Holds |
| :- | :- |
| `## The Day` | The story. What was being worked on, what state it was in when the day started, and where it ended up. Two to five paragraphs |
| `## Problems Solved` | One row per problem actually closed that day: what was wrong, what was done about it, and what that changed |
| `## Impact` | What the day left behind that was not there in the morning. Numbers where the commits carry them |
| `## In Depth: <title>` | Optional. One cause, one fix, and a result measured before and after, when the day holds work that has all three |
| `## Commits` | Every commit, hash and subject, so each claim above is traceable |

Every claim in the prose is traceable to a commit, a commit body, or a diff. Where a commit body explains a decision, that explanation belongs in the story rather than in a quote block, because the story is what a reader came for.

**A day with two small commits does not get five paragraphs stretched out of it.** It gets a short `## The Day`, whatever rows `## Problems Solved` honestly has, and the commit list. Padding a quiet day is the same failure as summarising a busy one.

### The In Depth Section

An `## In Depth` section is written only when the work has one cause, one fix, and a result that can be stated as a number before and a number after. It carries its own headings one level down: `### Summary`, `### How It Was Found`, `### What Was Wrong`, `### The Fix`, `### Results`, `### What To Take From This`, and `### Files Touched`.

**When no measurement was taken at the time, say so and list only what can still be checked today.** Do not reconstruct a number after the fact and present it as one that was measured.

It may describe work spanning more than the one day it sits in, and when it does, it goes in the journal of the day that work finished.

## Naming

```text
journal/<YYYY-MM-DD>.<project>.journal.md
```

One flat folder. **The name is the project folder name exactly, with nothing appended**, so a filename can be derived from a date and a repository without anyone having to look up what the file was called. The date comes first so the listing sorts chronologically across every project at once and a week of work reads in one screen.

The date is the day the commits carry. The `.journal.md` suffix carries the kind into every place a filename appears on its own, the same reason a memory note carries its type, per [[memory.rules.md]].

## A Journal Is a Vault Document

**A journal carries YAML frontmatter with tags.** It is a vault document, not a project document, so the rule in [[docs.rules.md]] banning frontmatter from a README does not apply to it.

The split is about who reads the file. A README is read by someone evaluating a repository, and frontmatter there is noise in front of the thing they came for. A journal is read months later by someone asking "have we hit this before", and **that question is answered by a tag, not by a title**.

Tags come from the axes in [[docs.rules.md]]:

```markdown
---
tags:
  - kind/journal
  - project/loader
  - topic/performance
---

> Up: [[README.md]]
```

- `kind/journal` always, exactly once.
- `project/` for every project the work touched. Work spanning two projects carries both, which is what makes the pair findable later.
- One or two `topic/` tags, per the ceiling in [[docs.rules.md]].
- **No `layer/`.** A journal describes work, and work crosses layers.

## Structure of an In Depth Section

| Section | Holds |
| :- | :- |
| `### Summary` | The whole story in one paragraph, for a reader who stops there |
| `### How It Was Found` | Including what looked true and was not |
| `### What Was Wrong` | The defects, one subsection each |
| `### The Fix` | What was changed, with commit and file |
| `### Results` | The measurement before and after, side by side |
| `### What To Take From This` | What a future reader should carry away |
| `### Files Touched` | A table of repository and file |

**A section with nothing to say is dropped, not filled.** An In Depth section with no before measurement is one whose result cannot be checked.

### The Title States the Finding

**A title carries the result, and the number when there is one.**

| Write | Not |
| :- | :- |
| `Stock Report: Seven Minutes Down To One` | `Performance Fix` |
| `One Missing Column Emptied Five Reports` | `Report Bugfix` |
| `Login Failed On A Host-Only Cookie` | `Auth Update` |

A reader scanning a folder of journals should be able to pick the one they need from the filename alone.

## Numbers, Before and Beside After

> [!danger]
> Never write "much faster" or "a lot lighter". A journal without a measured before and after is a claim, and a claim ages into folklore that nobody can check or correct.

**Take the measurement before touching anything**, from a real run, and name where it came from: a job id, a log timestamp, a query plan. Put the after beside it in the same table so the reader compares in one glance rather than scrolling between two sections.

```markdown
| Endpoint | Before | After |
| :- | -: | -: |
| `stock_report` | 282 calls, 418 s | 34 calls, 51 s |
```

Where a number genuinely cannot be measured, say so and say why, rather than substituting an adjective.

## Write the Wrong Turn

**The part worth writing is the part that was not obvious.** A journal that goes straight from problem to solution has removed the only content a reader could not have produced themselves.

Record specifically:

- **What the error message pointed at, and what was actually broken.** Those differ more often than not, and the gap is what costs hours.
- **The explanation that looked right and was not**, and what ruled it out.
- **What was checked and found fine**, so the next reader does not check it again.

## Language and Quoting

Written in English, in full: the story, the reasoning, and the lesson, not only the technical terms. That is the same rule every vault document follows, per [[docs.rules.md]].

**Quoting is where a journal deliberately breaks the formatting rules, and it has to.**

- **An error message is quoted verbatim and never translated.** A reader matching the string finds the journal; a translation matches nothing.
- **A commit subject is quoted verbatim too**, including any character the formatting rules would otherwise ban. A subject rewritten to remove an em dash no longer matches what `git log` prints, so a reader searching for it finds nothing. **The formatting restrictions govern what a journal writes, not what it quotes.**
- **An original complaint is quoted in the language it was said in**, with a translation beside it. Translating someone's complaint removes the words they chose, and those words often point at the problem.
- A file name, a command, a table or column name, and a job title keep their original form.
- Outside a quote, every formatting restriction in [[docs.rules.md]] applies: no em dash, no arrow, no emoji, no horizontal rule in the body.
- Callouts follow [[callout.rules.md]]. A journal opens with a `[!note]` giving the date and the trigger, and uses `[!danger]` for the trap that cost time. **Three per journal is the ceiling**, like any other document.

## The Index

`journal/README.md` lists every journal, newest first, with its date, its project, and a one-line hook. **A journal that is not listed there is reachable only by knowing its filename**, which is the same failure [[memory.rules.md]] guards against in the memory folder.

The index entry is added in the same commit that writes the journal.

## Definition of Done

- The file is `journal/<YYYY-MM-DD>.<project>.journal.md`, with the project folder name exactly.
- It carries frontmatter with `kind/journal`, a `project/` tag per project touched, and at most two `topic/` tags.
- It records the author's own commits only.
- `## The Day`, `## Problems Solved`, `## Impact`, and `## Commits` are all present.
- Every claim traces to a commit, a commit body, or a diff.
- An `## In Depth` section, where present, has one cause, one fix, and a before measured beside an after.
- No claim uses an adjective where a number was available.
- The wrong turn is written down, along with what ruled it out.
- Every error message and commit subject is quoted verbatim.
- The index entry in `journal/README.md` was added in the same commit.

## Do and Do Not

| Do | Do not |
| :- | :- |
| Measure before, and put after beside it | Write "much faster" |
| Record the wrong turn and what ruled it out | Go straight from problem to solution |
| Quote the error message verbatim | Paraphrase it |
| Quote a commit subject exactly as `git log` prints it | Rewrite it to satisfy the formatting rules |
| Name the commit and the file | Say "some backend fixes" |
| Write one journal per project per day | Write one per commit, or one per problem |
| Keep a quiet day short | Pad two commits into five paragraphs |
| Add the index entry in the same commit | Leave the journal unlisted |

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements. **A journal never quotes a secret, a credential, or personal data**, even where the error message contained one, per [[secret.rules.md]]
2. Direct user instructions
3. This journal standard
4. [[docs.rules.md]], except for the quoting exemption above
5. Existing project conventions

## Applies To

- [[docs.rules.md]]
- [[callout.rules.md]]
- [[memory.rules.md]]
- [[commit.rules.md]]
- [[secret.rules.md]]
- [[pattern/README.md]]
