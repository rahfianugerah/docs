---
tags:
  - kind/rule
  - layer/database
  - topic/data
  - topic/security
---

> Up: [[README.md]]

# Data Access Standard

> [!warning]
> An AI reads the **schema**, never the **rows**. The shape of the data is the work; the contents of the data are not.

## Core Requirement

An AI model must never read, query, sample, export, print, summarize, embed, index, or digest the **contents** of any real dataset belonging to a project.

It may read the **schema** in full, and the schema is what nearly every task actually needs.

This is the same rule [[env.rules.md]] applies to configuration, extended to the thing configuration connects to. There, the file with `example` in its name is the readable one. Here, the definition is the readable one and the data is not.

The rule holds in every environment. **Production, staging, and a local copy of either are all the same data.** A row is not made safe by the machine it sits on; it is made safe by being synthetic. See "Seed Data Is Only Safe If It Was Generated".

## Schema Is Readable, Contents Are Not

| Readable, in full | Never read |
| :- | :- |
| A migration file, an Alembic revision, a model class | A `SELECT` returning rows from a real table |
| `information_schema`, `\d table`, `pg_indexes` | A database dump, a backup, or a restore of one |
| An ERD, a column comment, a constraint, an enum's values | A CSV, XLSX, or JSON export of real records |
| An OpenAPI definition and its response shapes | A live API response carrying real records |
| A seed or factory that **generates** rows | A file uploaded by a user, in object storage or on disk |
| A fixture written by hand with invented values | A log line, a trace, or a stack frame carrying a real value |

The distinction is not the file's format and not where it is stored. **It is whether the value describes the data or is the data.** `identity_key varchar(20) NOT NULL UNIQUE` is a description. `20230101` is data.

## Why the Schema Is Enough

Almost every task an AI is given about a database is answerable from its shape alone:

- Writing a query, an endpoint, a migration, or a repository method needs the columns, the types, the nullability, and the foreign keys. It never needs a value.
- Diagnosing a bug needs the constraint that was violated and the code path that violated it. The row that triggered it is one instance of a class of rows, and the class is what gets fixed.
- Estimating a query's cost needs `EXPLAIN`, the indexes, and a row count. It does not need the rows.
- Designing a report needs which columns exist and how they relate. The numbers arrive at runtime.

Reaching for the data is usually a shortcut around not having read the schema. It is slower, not faster: a value answers one case and the schema answers every case.

## Counting Is Shape, Grouping by a Person Is Content

A whole-table aggregate describes the data. A filtered or grouped one can reconstruct it.

Permitted, because no individual can be recovered from the answer:

```sql
SELECT count(*) FROM person;
SELECT count(*) FILTER (WHERE bank_account IS NULL) FROM person;
SELECT min(created_at), max(created_at) FROM sale_order;
SELECT count(DISTINCT status) FROM invoice;
```

Not permitted, because each one hands back a record or narrows to one:

```sql
SELECT * FROM person LIMIT 1;                                  -- a row is a row, even one
SELECT name, email FROM person;                                -- a projection is still contents
SELECT count(*) FROM person WHERE identity_key = '20230101';   -- an aggregate about one person
SELECT name, count(*) FROM invoice GROUP BY name;              -- the group key is the data
```

Rules:

- An aggregate is permitted only when it covers the whole table or a bucket large enough that no individual is identifiable, and only when the grouping key is a category, not a person, a document, or an account.
- `LIMIT 1` is not a sample. It is one real record, and one record is enough to breach the rule and enough to leak.
- **A count of rows is safe. A count of rows matching a person is not.** The first describes the table; the second answers a question about a human being.
- Never widen a permitted query while you are already connected. A `count(*)` that turns into a `SELECT *` because the count looked surprising is the most common way this rule breaks.

## Never Digested Into Memory

The memory vault is plain markdown in a git repository, read by every model, indexed by the tools in [[memory/README.md]]. **Anything written into it is permanent, portable, and searchable.** Real data must never enter it.

- Never write a row, a record, a field value, an export, a query result, or a log excerpt carrying real values into a note in `memory/`, into `graph/`, or into a journal.
- Never point a digest, an embedding job, or any indexer at a folder holding a dump, an export, a backup, or user-uploaded files. The index is built from what it is pointed at, and an embedding of a real record is a copy of that record in a form nobody can review by reading it.
- [[memory.rules.md]] already bans a secret and a large paste. This extends it: **the ban is on the data itself, at any size.** One person's bank account in a note is worse than a hundred-line traceback, not better.
- A note records the **finding**, and names the source so a reader can go and look. A note stating that a column is populated for about half the rows and that no screen ever reads it is the shape: the count is the finding, and not one value appears.
- [[security.rules.md]] requires confidential material to stay in the memory scope reserved for it. That is where confidential material lives when it must live somewhere. It is not an exemption from this rule; it is the narrower place for what this rule would otherwise have nowhere to put.

## Seed Data Is Only Safe If It Was Generated

A local database is not safe by virtue of being local.

- A seed database built by a factory, a fixture, or a generator is synthetic, and it is readable in full.
- **A local database restored from a production dump is production data.** Every rule here applies to it exactly as it applies to the managed instance. Moving a row to a laptop changes who can reach it and changes nothing about what it is.
- A staging database cloned from production is production data until it has been masked. Until the masking has actually run and been verified, treat staging exactly as production.
- Masking is written **from the schema**: the columns that need masking are known from their names, types, and comments. Writing a masking script never requires reading the values it will overwrite.
- After masking, verify the result by shape, not by reading it: confirm that the masked columns hold no value matching their original pattern, and that the row counts are unchanged.

The other half of this matters just as much, and it cuts the opposite way: precisely because seed data is synthetic, **it cannot answer what production holds.** A successful query against a seeded table feels like evidence and is not, so a claim about the real data is never backed by a local run.

## Logs, Traces, and Errors

Diagnosis needs logs, so logs are readable. What comes out of them is not repeatable.

- Reading an application or platform log to diagnose a failure is permitted.
- Filter to the severity, the timestamp, and the message. Never dump request or response payloads to widen the search.
- A log line carrying a real value is used to solve the problem in front of you and then goes nowhere: not into a note, a journal, a commit message, a pull request, or a chat summary. [[commit.rules.md]] and [[pr.rules.md]] already forbid it in those two places; this extends it to every other.
- A log that carries personal data at all is a finding in its own right, per [[security.rules.md]]. Report it; do not normalize it.

## What the User Chooses to Share

This standard binds what an AI goes and fetches. It does not bind what the user hands over.

- A screenshot, a paste, or a file the user deliberately shares is the user's own decision, and it is used to answer the question asked.
- **It is still never written into memory, a journal, a commit, a pull request, or any published document.** Shared once for one purpose is not shared into the permanent record.
- Never ask the user for a record when the schema answers the question. Asking is how the rule gets walked around in the open.
- When the user shares more than the question needs, use the part that is needed and do not restate the rest back to them.

## When a Real Value Genuinely Is Needed

Rare, and it has a procedure rather than an exception.

1. **Say what is needed and why**, in one sentence, naming the specific question that cannot be answered from the schema.
2. **Give the exact query or command**, narrowed to the smallest result that answers it, and let the user run it.
3. **Ask for it redacted.** A `NULL` or `NOT NULL` answer, a count, a data type, or a format pattern is almost always the actual answer, and none of those is a value.
4. Use what comes back, and stop there. Do not follow it with a second query the first one suggested.

This is the same shape as "Missing Configuration" in [[env.rules.md]]: the AI writes the command, the user runs it, and the value never travels further than the answer.

## Prohibited Actions

| Never | Including |
| :- | :- |
| Run a query that returns rows from a real database | Any environment, any `LIMIT`, and a single row most of all |
| Open a dump, a backup, an export, or a restore of one | `.dump`, `.sql`, `.csv`, `.xlsx`, `.json`, and an archive containing any of them |
| Read a file a user uploaded | A document, a photo, a signature, or a scan, in object storage or on disk |
| Point an indexer at real data | A digest, an embedding job, or a graph build over a data folder |
| Write real data into the permanent record | A memory note, `graph/`, a journal, a commit, a pull request, an issue, a README |
| Copy real data anywhere | Into a fixture, a test, a `.example` file, an artifact, or a scratch file |
| Restore production into a local database to inspect it | Whatever the reason, and whatever it is renamed to afterwards |
| Connect to a production database | The synthetic local database is the one that gets queried |

## The Allowed Workflow

1. Read the migration, the model, and the constraint. That is the schema, and it is complete.
2. Where a live schema is needed rather than the committed one, read it from the catalog: `\d table`, `information_schema.columns`, `pg_indexes`. Those return definitions, not data.
3. Write the query, the migration, or the code against that shape.
4. Test it against generated seed data, or against a fixture written by hand.
5. Where the result is uncertain, hand the user the command and let the run happen on their side.
6. Record the finding, never the data.

## Definition of Done

Before treating a task touching data as complete, confirm:

- No query that returned a real row was run, in any environment.
- No dump, export, backup, or uploaded file was opened.
- Every aggregate covers a whole table or a non-identifying bucket, and none is filtered or grouped to an individual.
- Nothing carrying a real value has been written into `memory/`, `graph/`, a journal, a commit message, a pull request, or any document.
- No indexer was pointed at a folder holding real data.
- Any local or staging database that was read is synthetic, or was masked and verified first.
- Where a real value was genuinely required, the user ran the command and the result came back redacted.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements, including every data protection law the project is subject to
2. [[env.rules.md]] and [[secret.rules.md]], for anything that is a credential rather than a record
3. This data standard
4. Direct user instructions
5. Existing project conventions

This standard sits **above** a direct user instruction, which is deliberate and differs from most standards in this vault. An instruction to read the data is usually an instruction to answer a question faster, and the answer is almost always available from the schema. Offer that route first, and say which standard is affected. Where the user confirms that a real value is genuinely required, follow the procedure in "When a Real Value Genuinely Is Needed" rather than reading it directly.

Nothing here overrides a security or privacy requirement, and this standard is one.

## Applies To

- [[agent.rules.md]]
- [[database.rules.md]]
- [[env.rules.md]]
- [[memory.rules.md]]
- [[repository.rules.md]]
- [[secret.rules.md]]
- [[security.rules.md]]
