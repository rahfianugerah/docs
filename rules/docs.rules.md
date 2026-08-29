---
tags:
  - kind/rule
  - layer/docs
  - topic/workflow
---

> Up: [[README.md]]

# Documentation Standard

> [!important]
> Every documentation file starts from a template in [template/](../template/), keeps that template's section order, and follows the formatting restrictions below.

## Core Requirement

Documentation is written for the person who arrives with no context, which is usually you in six months.

Everything in this vault is written in **English**: every document, every heading, every comment, every commit, every identifier. A project's own documentation is written in the language its readers use, which is a different question and is settled in [[prd.rules.md]].

The template is the single source of truth for structure, section order, formatting, and content scope. Read it before writing, not after.

## What Every Project Documents

Five files, and no more unless something genuinely needs one.

| File | Holds |
| :- | :- |
| `README.md` | What it is, how to run it, what it needs. The only file most readers open |
| `PRD.md` | The problem, the users, and the non-goals, per [[prd.rules.md]] |
| `API.md` | The endpoints, if the project has any |
| `MODEL.md` | The model card, if the project trains one |
| `.env.example` | Every variable name with a placeholder, per [[env.rules.md]] |

A project that needs a sixth document usually needs a shorter README instead.

## The README Is the Contract

A reader must be able to go from a clone to a running project using only the README. If they cannot, the README is incomplete regardless of how much it contains.

Required, in this order:

1. Title, then the badge row per [[badge.rules.md]].
2. One paragraph: what this is and what it is for.
3. Setup: the exact commands, copy and paste, including the environment activation.
4. Usage: the smallest example that does something real.
5. Configuration: the variable names, never a real value.
6. Project structure, if the layout is not obvious.

Write the setup commands as a block that can be pasted whole. Do not describe the steps in prose and leave the reader to assemble them.

## The Shape of a Project Document

**A project document opens with the title, then the badge row, then one paragraph that says what the thing is and why it exists, then the Table of Contents.** Nothing else comes before those four.

```markdown
# Project Name

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2EA043)

A one-line description of what it is, then the sentence that says **why it exists**, with the
claim that matters in bold.

## Table of Contents
```

> [!important]
> **A project document carries no YAML frontmatter and no `---` anywhere in it.** Frontmatter belongs to a vault document, where the tag axes below need it. A README, a PRD, an `API.md`, and a `MODEL.md` open with `# Title` and nothing above it.

### The Lead Paragraph Says Why, Not What

The first paragraph is the only one most readers finish. **Say what it is in one line, then say why it exists**, because the second is the part nobody can reconstruct from the code.

Weak, because it describes the mechanism and stops:

```text
A CLI that reads markdown files and writes them into a vector database.
```

Strong, because it names the problem being solved and puts the surprising claim in bold:

```text
A plug-and-play memory for coding agents. Point it at a folder of markdown and that folder
becomes a brain the agent searches over MCP. **No chat model anywhere in it**: the agent
asking the question already has one.

It exists because an agent with no memory relearns the same context every session and pays
for that in tokens every time.
```

### The Table of Contents

**Every project document carries one, directly under the lead paragraph**, as a numbered list linking to each top-level section.

```markdown
## Table of Contents

1. [Setup](#setup)
2. [Usage](#usage)
3. [Configuration](#configuration)
```

- **It lists the `##` headings only.** A `###` in the contents makes the contents longer than the reader's patience.
- **It is updated in the same commit that adds or renames a section.** A contents entry pointing at a heading that no longer exists is the first thing a reader tries and the first thing that fails.
- A document short enough to read without scrolling does not need one. That is roughly one screen, and almost nothing real is that short.

### Name a Section for the Question It Answers

**A heading is a question the reader already has, answered.** Not a category the writer filed it under.

| Write | Not |
| :- | :- |
| `Four Commands` | `Commands` |
| `No Chat Model` | `Architecture Notes` |
| `Nothing Is Written Into a Digested Folder` | `File Handling` |
| `Known Limitations` | `Notes` |
| `One Stack or Several` | `Deployment Options` |

A heading that states the answer means a reader scanning the contents already learns something, and a reader who needs the detail knows exactly which section holds it.

### Show the Real Thing

- **A command in a document is the command that runs**, copied from a shell where it worked. Not a paraphrase, and not a placeholder where a real value could be shown.
- **A table for anything with two or more parallel attributes.** A list of things that each have a name, a purpose, and a default is a table, and reading it as prose is work the writer pushed onto the reader.
- **A code block carries a language tag**, and shows the smallest thing that does something real.
- **Bold the sentence that carries the point**, inline, where the reader is. A paragraph whose claim is buried in the third line is a paragraph most readers leave before reaching it.

### A Setup Section Is a Numbered Walkthrough

**Setup is numbered steps with a bolded name, not a wall of commands.** Each step is a short line saying what it is, then the block that runs, then anything the reader needs to know before the next one.

````markdown
**1. Environment.** Conda, an environment named `env`, Python 3.13.

```bash
conda env update -f environment.yml
conda activate env
```

Never use bare `pip` or bare `python` outside the activated environment. On this machine they
resolve to different interpreters, and an install lands somewhere the code cannot import it.

**2. Configuration.** Copy the template and fill it in by hand.
````

- **Say what the step is before the command**, in one line. A block with no lead is a block the reader has to run to understand.
- **Number the steps, and say up front which are already done.** "Steps 1 and 2 are done; step 3 onward needs your keys" tells a returning reader where to start.
- Where the walkthrough is long enough that the steps need their own headings, they become numbered `###` headings and the contents entry points at each one.

### State the Trap Where It Bites

**The gotcha goes directly under the command that triggers it, in bold, with the mechanism.** Not in a Troubleshooting section at the bottom, where it is found only after the reader has already hit it.

```markdown
**Step 3 has to come first.** `compose.yaml` declares `.env` as a required env file, so
`docker compose up` without it fails with `env file ... not found`. That is deliberate: made
optional, the service would start on its embedded defaults and quietly serve the wrong database.
```

Three parts, and all three are needed:

1. **The rule, in bold**, as a sentence the reader can act on.
2. **The mechanism**: what the tool actually does, and the error it produces.
3. **Why it is that way**, where the behaviour is deliberate rather than a bug. That is what stops the next reader "fixing" it.

**Quote the real error text.** A reader who is already staring at `env file ... not found` finds the answer by matching the string, and a paraphrase does not match.

### Say What Is Committed and What Is Not

A project document carries a **Data** section, or a row inside Project Structure, that says where each thing lives and whether it is in git.

```markdown
| Item | Location | Notes |
| :- | :- | :- |
| Code maps | `graph/<project>/` | Gitignored. Produced by `pmb map` |
| The memory itself | `<vault>/memory/` | Committed, human-authored, the source of truth |
```

**"Gitignored" and "committed" are the two words that matter**, and the reader is looking for exactly one of them. A path with no such note is a path somebody will commit.

### Two Sections Every Project Document Ends With

**Known Limitations.** What the thing does not do, what it is bad at, and the ceiling of each part. This is the section everybody skips writing and every reader needs, and it is what separates a document from a sales page. State the limit and the reason:

```markdown
- **Only markdown is digested.** Obsidian is the viewer and markdown is the substrate, so PDF,
  docx, and csv are not read. Convert first if you need them.
- **1024 dimensions is a ceiling, not a preference.** The index will not build above 2000, and
  it does not fail loudly; it just leaves every search doing a sequential scan.
```

**Deviations From the Standards.** Where the project departs from a rule in this vault, **numbered, each naming the rule it departs from, the reason, and the cost accepted.** Several standards already require a deviation to be written down; this is the one place it goes.

```markdown
1. **Not Cloud Run.** [[deploy.rules.md]] requires every deployed project to ship to Cloud Run.
   This runs as one Docker stack on a flat-cost VM instead, because an always-on database has
   no idle state to scale down to. The exception does not generalise.
```

A project with no deviations writes the heading and one line saying so. **An empty section is information; a missing one is a question.**

Which document carries which:

| Document | Known Limitations | Deviations |
| :- | :- | :- |
| `README.md` | Yes | Yes |
| `API.md` | Yes | Only where the API itself departs from a standard |
| `MODEL.md` | Yes | Only where the training or evaluation departs from one |
| `PRD.md` | No; its non-goals section already does this work | No |
| The agent entry point | No; it is instructions, not a description | No |

The README is the one document that speaks for the whole project, so it is the one that always carries both.

## Template Usage Rules

You must:

1. Read the template before creating or editing any project documentation.
2. Follow the exact section order the template uses.
3. Use only the headings and sections the template includes.
4. Keep the documentation within the scope the template defines.
5. Preserve the template structure unless the user explicitly asks to change the template itself.
6. Write the documentation directly into the template's sections.
7. Preserve the placeholders, tables, and formatting patterns the template defines.
8. Remove instructional placeholder text once real project information has replaced it.

You must not:

- Add a section the template does not include.
- Add an appendix, a summary, a note, a recommendation, or an extra explanation that is not already in the template.
- Expand the documentation beyond what the template asks for.
- Replace the template with a different structure.
- Remove a required section.
- Invent a project detail that the repository or the user does not support.
- Put endpoint documentation in the main project documentation when the project has a separate `API.md`.

If information for a required section is unavailable, write:

```text
To be confirmed
```

Do not fill a gap with an assumption.

## Writing

- **Short sentences.** One idea per sentence.
- **Active voice.** "The loader reads the file", not "the file is read by the loader".
- **Say what it does, then why.** The why is the part nobody can reconstruct.
- **No filler.** Delete "basically", "simply", "just", "in order to", "it should be noted that". "Simply" is a lie whenever the thing is not simple.
- **Concrete over abstract.** Name the file, the function, the value.
- **Write the failure.** The command that fails and what the error looks like is worth more than three paragraphs of happy path.
- **If the explanation is longer than the code, delete the explanation** and make the code clearer instead.
- **Consistent terminology.** One name per concept, for the whole document.
- Do not repeat the same information in two sections unless the template requires it.
- Avoid a technical explanation the project does not need. Where a technical term is unavoidable, explain it once, briefly, in plain language.

## Formatting

- ATX headings (`#`), sentence-case or title-case consistently within a file.
- Fenced code blocks with a language tag.
- Tables for anything with two or more parallel attributes.
- A bullet list for items, a numbered list only for genuine ordered steps.
- One blank line between blocks. No trailing whitespace.
- A path, a filename, a variable, a command, and a value all wear backticks.
- **One paragraph is one line.** Never hard-wrap a paragraph across several source lines. Markdown reflows a paragraph to the reader's width, so the wrap adds nothing to the rendered page and it ruins a diff: reflowing one sentence rewrites every line after it, so a one-word change shows up as a rewritten paragraph.

Do not use:

- Emoji.
- An em dash, a left arrow, or a right arrow.
- Smart quotation marks where normal ones work.
- A macOS-specific symbol or format.
- A decorative Unicode symbol that is not required.
- ALL CAPS for emphasis.
- A wall of bold text. If everything is bold, nothing is.

The replacements, since each banned character has exactly one:

| Instead of | Write |
| :- | :- |
| An em dash | `-` |
| A left arrow | `<` |
| A right arrow | `>` |
| A smart quote | `"` |

### Flow Examples

A flow is written with the plain angle bracket, in both directions.

Incorrect, using arrows:

```text
Client [right arrow] API [right arrow] Database
Database [left arrow] API
```

Correct:

```text
Client > API > Database
Database < API
```

Incorrect, using an em dash to join a clause:

```text
The service handles authentication [em dash] including token validation.
```

Correct:

```text
The service handles authentication - including token validation.
```

### No Horizontal Rules

Never place a `---` horizontal rule in a document body. Headings already mark where one section ends and the next begins, so a rule on top of them is decoration that carries no meaning, and a document that leans on it reads as a stack of fragments rather than one continuous piece. Add one only when the owner asks for it directly.

**A project document carries no `---` at all**, because it carries no frontmatter either, per "The Shape of a Project Document" above. In a vault document the ban covers the body only, and does not touch two things that look the same:

- YAML frontmatter on a **vault** document, where the opening and closing `---` are what make a rule, a component standard, a pattern, or a memory note readable by Obsidian and by the memory indexer. Removing those breaks the file rather than tidying it, and they are the only `---` permitted anywhere in this vault.
- A `---` inside a fenced code block, which is sample content being shown, not formatting being applied.

## Tags

Every rule and every component standard opens with YAML frontmatter carrying its tags. Tags connect two documents that never link to each other: a wikilink says "read that one next", a tag says "these belong to the same concern", and only the second one surfaces the file you did not know to look for.

```markdown
---
tags:
  - kind/component
  - layer/frontend
  - topic/ux
---

> Up: [[README.md]]
```

The frontmatter is the first thing in the file, before the breadcrumb. The breadcrumb keeps its place directly under it.

### The Three Axes

A tag comes from one of three axes, and the axis is the prefix. Nesting them this way makes them group in the Obsidian tag pane instead of arriving as one flat alphabetical list.

| Axis | Values | Answers |
| :- | :- | :- |
| `kind/` | `rule`, `component`, `runbook`, `template`, `pattern`, `journal` | What this document is |
| `layer/` | `frontend`, `backend`, `database`, `infra`, `docs` | Where it applies |
| `topic/` | `security`, `accessibility`, `data`, `ux`, `state`, `workflow`, `deploy`, `memory`, `performance` | The concern it belongs to |
| `project/` | The project folder name | Which project the work touched. Journals only |

Every document carries exactly one `kind/`. Most carry one `layer/`, and a document that genuinely applies everywhere, such as the commit or branch standard, carries none rather than a wrong one. One or two `topic/` tags is the working range.

The `project/` axis exists for a journal and is empty on a rule or a component. A rule that named one project would be a rule that does not apply to the rest, which is a contradiction; a journal is always about specific work on a specific project, and work that spans two carries both, per [[journal.rules.md]].

> [!warning]
> Two `topic/` tags is the ceiling in practice, and three is a signal the document holds more than one thing. A standard tagged with five concerns is a standard nobody looking for any of them will find, because the tag has stopped narrowing anything.

### Adding a Value

The lists above are closed. Adding a value to an axis is a change to that table first, made deliberately, and never a tag invented inside one file.

An invented tag is worse than a missing one: `topic/auth` beside the existing `topic/security` splits one concern across two names, and a reader who filters on either now sees half the documents with no way to know that.

## Command Restrictions

A command is written the way it is typed, and the way it is typed is by name.

> [!failure]
> Never write an absolute path to an executable. Write `openssl`, not the full path into a toolchain's `usr\bin`. Write `python`, not `C:\path\to\envs\name\python.exe`. This applies to a command in documentation and to a command an agent runs.

An absolute path fails three ways at once, and all three are invisible to whoever wrote it:

- **It is wrong on every other machine.** A path under one person's home directory runs for exactly one person, and the next reader gets `The term is not recognized` with no hint that the path was the problem rather than the tool being missing.
- **It leaks who wrote it.** A home directory carries a username into a document everyone reads, and for a public repository, everyone else too.
- **It hides a real setup problem.** Someone reached for the full path because the tool was not on `PATH`. Writing the path around it fixes one command on one machine and leaves the same failure waiting in every other command that needs the same tool.

Fix the environment once instead. If a toolchain ships a binary the shell cannot find, its `bin` directory belongs on `PATH`: one change on one machine, against a path repeated in every runbook.

That rule covers a command. [[path.rules.md]] covers every other path: in source, in configuration, and in a document.

### The Two Exceptions

- **A variable that names an interpreter or a file is a path by definition.** `CLOUDSDK_PYTHON` points at an interpreter and `--key-file` points at a file. Those take paths because that is what they are for. Write them as a placeholder such as `C:\path\to\python.exe`, never as a real path from the machine the document was written on.
- **A path inside the repository is relative and stays relative.** `./scripts/migrate.py`, not the absolute form of the same file.

## Code Comment Restrictions

These apply to comments inside source code, not only to Markdown.

Do not use a special character as a decorator, border, or separator inside a code comment. This includes, but is not limited to, a repeated `=`, `-`, `*`, `+`, `#`, `$`, `~`, `_`, `^`, `/`, `\`, or `|` arranged into a line, a box, a banner, or a divider. Do not use extra blank lines or padding spaces to box a comment either.

A code comment states its purpose directly, in plain language, with no surrounding decoration. Readability comes from clear wording, not visual styling.

The one exception is a short code snippet inside a comment showing how something is called. That snippet keeps its own natural formatting and line breaks.

Correct:

```text
// Validates the token and returns the decoded claims
function verifyToken(token) { ... }
```

Correct, the exception:

```text
// Usage:
// const result = verifyToken(token);
function verifyToken(token) { ... }
```

Incorrect:

```text
// ==========================
// Validates the token
// ==========================
function verifyToken(token) { ... }
```

## Badges

Every README carries a badge row, and [[badge.rules.md]] owns its content: which badges, in which order, on which color, with which logo. Two rules belong here because they are about honesty rather than style:

- **Do not invent a build, test, coverage, deployment, or version status.** A green badge nothing produces is a claim the reader has no way to check.
- **Do not claim a technology the repository does not use.** The badge row is read as an inventory.

## Status Indicators

When a feature, service, module, integration, or documentation item is unused, unavailable, incomplete, active, or needs attention, mark it with an HTML `code` element carrying a color.

Three colors, and only three:

| Color | Means |
| :- | :- |
| Green | Active, available, complete, enabled, supported, successful |
| Yellow | Pending, partial, optional, under review, needs attention |
| Red | Not used, unavailable, disabled, failed, unsupported, missing |

```html
<code style="color: green">Active</code>
<code style="color: yellow">Needs Confirmation</code>
<code style="color: red">Not Used</code>
```

Rules:

1. Use the document's own language for the status text.
2. Green, yellow, or red only.
3. Lowercase color name in the `style` attribute.
4. One space after the colon.

Correct:

```html
<code style="color: red">Not Used</code>
```

Incorrect, in three different ways, the space before the colon, the missing space after it, and the wrong element:

```html
<code style="color : red">Not Used</code>
<code style="color:red">Not Used</code>
<span style="color: red">Not Used</span>
```

Do not color a normal paragraph, a heading, a technical explanation, a command, or source code. Use a status indicator only where it makes a documented condition clearer.

## Obsidian

This documentation set is an Obsidian vault, and so is the memory in [[memory/README.md]]. Three conventions keep the graph usable.

**Wikilinks with the extension:** `[[commit.rules.md]]`, not the bare `commit` form. The extension form survives being read outside Obsidian, where a bare link means nothing.

**Callouts** mark the one thing on a page a reader must not miss, and every type comes from [[callout.rules.md]]. A hard prohibition is a callout, not a bolded sentence, because a prohibition written as ordinary prose gets skipped and the reader discovers it was serious only after breaking it.

> [!warning]
> A callout is Obsidian syntax, so it renders as a plain blockquote everywhere else and is digested into the memory index verbatim. Three per document is the ceiling, because a page of callouts has no emphasis left.

**Fixed placement, so re-runs are deterministic:**

| Block | Where | Contains |
| :- | :- | :- |
| Frontmatter | The very first line | The three-axis tags |
| Breadcrumb | Directly under the frontmatter | `> Up: [[README.md]]` |
| `## Index` | `README.md` only | Every document, grouped |
| `## Applies To` | A rules document, at the end | What it governs |
| `## Related` | Any other document, at the end | Lateral links |

Update a block in place. Never append a second one.

## The Deploy Runbook Is Its Own Template

The deploy runbook is the one document whose template does not live in [template/](../template/). For a project's `deploy.cloud.md`, treat [[deploy.cloud.md]] as the template: follow its section numbering, section names, and order exactly. Keep every section even when a project does not use it, and mark the unused one with a status indicator instead of deleting it, so any two repositories stay comparable line for line.

## API Documentation

When a project has an `API.md`:

- Endpoint documentation lives only in `API.md`.
- The main project documentation does not carry an endpoint path, a request parameter, a request body example, a response payload, an endpoint-specific status code, or an endpoint-specific error response.
- The main documentation may explain the general API architecture. It must not duplicate `API.md`.

## Documentation Workflow

Before writing:

1. Locate and read the template.
2. Review the relevant project files.
3. Review `.env.example` when environment variables need documenting.
4. **Do not read any real environment file**, per [[env.rules.md]].
5. Identify what the repository actually supports.
6. Map that information to the template's sections.
7. Write only what those sections ask for.
8. Add the badge row per [[badge.rules.md]].
9. Use a status indicator only where a condition needs one.
10. Review for unsupported additions, prohibited characters, undocumented assumptions, and any real credential or environment value.

## Updating Existing Documentation

- Preserve valid existing content.
- Correct anything inaccurate or outdated.
- Keep the structure aligned with the template.
- Remove a section added outside the template unless the user asks otherwise.
- Do not rewrite an unrelated section for no reason.
- Update a badge only when the repository supports the new value, and replace an unsupported claim with a factual one.
- Update a status indicator when the condition it describes changes.
- Keep terminology consistent across the whole document.

## When Something Is Missing

**No template:** do not invent a replacement, do not copy a structure from another project, and do not improvise one. Say the template is missing and ask for it.

**No information:** do not guess, do not infer an unsupported value, and do not inspect a secret file. Use the template's placeholder, or `To be confirmed` where the template has none, and mark it:

```html
<code style="color: yellow">Needs Confirmation</code>
```

**No file to reference:**

```html
<code style="color: red">Not Available</code>
```

## Keeping It True

**A stale document is worse than no document**, because it is believed.

- Update the document in the same commit that makes it wrong. A README fixed "later" is a README that stays wrong.
- Delete a section describing something that no longer exists.
- A code example in a document is code: if it stops working, it is a bug.
- When the document and the code disagree, the code is right and the document gets fixed. Never the reverse.

## Machine Learning Documents

An ML project has one documentation failure the rest do not: a result nobody can reproduce.

A `MODEL.md` records, at minimum:

- What the model does, and what it must not be used for.
- The data: source, version, size, and how it was split.
- The training setup: parameters, seed, hardware, runtime.
- The metrics, with the baseline they are compared against.
- The known failure modes, and what the model is bad at.

The last one is the one everybody skips and the only one that prevents the model being misused.

An experiment's result belongs in the pull request that carried it, per [[pr.rules.md]], and its durable finding belongs in [[memory/README.md]]. A number in a notebook cell is not a record.

## Definition of Done

- Written in English, from the right template, with the template's section order.
- A project document opens with the title, the badge row, the lead paragraph, and the Table of Contents, and carries no frontmatter and no `---`.
- The Table of Contents lists every `##` heading and every entry resolves.
- Every heading names the question it answers, not the category it belongs to.
- Known Limitations is present and says what the thing is bad at.
- Deviations From the Standards is present, and names the rule, the reason, and the cost for each one.
- The README takes a reader from clone to running with no other source.
- The frontmatter carries exactly one `kind/`, and at most two `topic/` values.
- The badge row follows [[badge.rules.md]], every version is current, and no badge claims something the repository does not do.
- Every status indicator is green, yellow, or red, and uses the `code` element form.
- No real value from any environment or configuration file appears anywhere.
- No absolute path to an executable appears in a command, in the document or in what an agent runs.
- No emoji, no prohibited character, no decorative divider, and no boxed or bannered code comment.
- API detail is in `API.md`, not duplicated in the project documentation.
- Missing information is marked, not guessed.
- Every wikilink resolves.
- Nothing in the document contradicts the code.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. The template
4. This documentation standard
5. Existing project documentation
6. General repository conventions

A direct user instruction must not override security or privacy requirements. Even when following a higher-priority instruction, keep the language professional, clear, and simple, and do not use a prohibited character or format.

## Applies To

- [[project.template.md]]
- [[api.template.md]]
- [[model.template.md]]
- [[agent.template.md]]
- [[badge.rules.md]]
- [[callout.rules.md]]
- [[codes.rules.md]]
- [[env.rules.md]]
- [[prd.rules.md]]
- [[deploy.cloud.md]]
