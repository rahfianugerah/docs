---
tags:
  - kind/component
  - layer/frontend
  - topic/data
---

> Up: [[README.md]] · [[uix.component.md]]

# Search and Filter Standard

> [!note]
> Two halves of one feature: filters, which narrow a list by exact criteria, and search, which finds rows by text a human typed and probably mistyped.

## Core Requirement

Every search box and every filter follows this standard.

The two halves are not the same problem and do not use the same technique. **A filter is an exact predicate. A search is a ranked guess.** Mixing them produces the two failures this standard exists to prevent: a filter that quietly matches the wrong record, and a search that finds nothing because the user spelled a word the way it sounds.

This standard sits under [[uix.component.md]] for the search box itself, and depends on [[database.rules.md]] for the query underneath it. Every query rule here runs on the stack fixed by [[stacks.rules.md]]: PostgreSQL with SQLAlchemy 2.x.

## Filter or Search

Decide per column, not per screen.

| Column holds | Technique | Fuzzy allowed |
| :- | :- | :- |
| Free text a human wrote: name, title, subject, address, description | Search ladder, below | Yes |
| An identifier: employee number, contract number, invoice number, plate number | Exact, or prefix for a lookup field | Never |
| A number or an amount of money | Equality or a range | Never |
| A date or a timestamp | A half-open range | Never |
| An enum, a boolean, or a foreign key | Equality, or `IN` for a multi-select | Never |

> [!warning]
> **Fuzzy matching applies only to free text a human wrote.** An identifier, a number, a date, and an enum are matched exactly, always. Returning the wrong person because an identifier was one digit off is worse in every case than returning nothing, and a near-miss on a contract number is a data integrity problem rather than a convenience.

Everything in the right-hand column of that table, except the first row, is an indexed exact predicate and nothing more. The rest of this standard is mostly about the first row.

## The Search Ladder

A text search runs as a ladder of stages. Each stage is cheap, indexed, and answers on its own. **A stage runs only when the stage above it returned nothing.**

| Stage | Matches | Index | Catches |
| :- | :- | :- | :- |
| 0 | Nothing, the query never reaches the database | None | Empty, too short, or absurdly long input |
| 1 | Exact, on the normalized column | B-tree | The user typed it correctly |
| 2 | Prefix, `LIKE 'q%'` on the normalized column | B-tree with `text_pattern_ops` | The user typed the start of it |
| 3 | Trigram similarity on the phonetic column | GIN with `gin_trgm_ops` | A typo, a transposition, a missing letter, a spelling variant |

Stage 3 is where two spellings of the same sound meet, and it is the last stage. **There is no stage that scans the table.**

Climbing down the ladder is what "fail fast" means here: the common case, a correctly typed query, is answered by an index lookup and never pays for the fuzzy machinery; and the uncommon case reaches the fuzzy stage in one step rather than after a sequence of increasingly desperate `LIKE` patterns.

## Stage 0: Fail Fast Before the Database

These checks run in the application, before any SQL is built. A query that fails one of them never reaches the database.

- **An empty query applies no search predicate at all.** It does not return an empty list; it returns the unfiltered page. A search box the user has not typed in is not a filter.
- **A query shorter than 2 characters after normalization is rejected** the same way. A single letter matches most of the table and the fuzzy stage would rank thousands of rows for nothing.
- **A query longer than 100 characters is truncated or rejected.** A pathological string turns a trigram lookup into a long scan.
- **Set a statement timeout on the search query**, so a query that does go wrong fails in a bounded time instead of holding a connection open.
- Never run the next stage when the previous stage returned rows. **Never run all stages and merge them.**

## Normalization

Two derived values back the ladder. Both are generated columns, both are indexed, and both are produced by shared SQL functions rather than in application code, so the same rules apply to the stored value and to the query.

`norm` folds a string to a comparable form: lowercased, accents stripped, punctuation collapsed to single spaces, edges trimmed. Stages 1 and 2 use it.

`fon` folds a string to a phonetic key, described in the next section. Stage 3 uses it.

**Both must be marked `IMMUTABLE`**, or PostgreSQL will not allow them in a generated column or an expression index. `unaccent()` is `STABLE`, not `IMMUTABLE`, because it depends on a dictionary that can be changed, so it cannot be used directly. Wrap it, naming the dictionary explicitly:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE FUNCTION imm_unaccent(text) RETURNS text
  LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT AS
$$ SELECT public.unaccent('public.unaccent', $1) $$;

CREATE FUNCTION norm(t text) RETURNS text
  LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
$$ SELECT btrim(regexp_replace(lower(imm_unaccent(coalesce(t, ''))), '[^a-z0-9]+', ' ', 'g')) $$;
```

Skipping the wrapper is the usual reason a search migration fails with "functions in index expression must be marked IMMUTABLE", and **marking `unaccent` itself immutable instead is wrong**: it lies to the planner about a function whose result really can change.

## The Phonetic Fold

Where the users write a language that spells the same sound more than one way, a text search that compares letters finds nothing when someone types what they heard. The worked example here is Indonesian, which has three separate sources of variation. Adapt the list to the language the users actually write; the mechanism is the same in any of them.

- **Foreign spellings kept alongside absorbed ones.** `scandal` and `skandal`, `photo` and `foto`, `taxi` and `taksi`, `quality` and `kualitas`, `theory` and `teori`.
- **A superseded orthography, still everywhere in names and old documents.** `Soeharto` and `Suharto`, `Djoko` and `Joko`, `Tjipto` and `Cipto`.
- **Sounds with no stable spelling.** `v` and `f` are the same sound to most speakers, so `Vica` and `Fica` are one name written two ways.

The fold maps all of these onto one key. **Its purpose is not to be a correct pronunciation of the word.** It is applied to the stored value and to the query, so the only thing that matters is that both sides land on the same key.

The fold is an ordered list of replacements. **The order is part of the specification**, because an earlier replacement feeds the next one:

| Step | Fold | Reason |
| :- | :- | :- |
| 1 | `oe` to `u` | Soeharto, Soekarno |
| 2 | `sch` to `sk`, then `sc` to `sk` | Schedule, scandal. `sch` runs first, or `sc` eats it and leaves an `h` |
| 3 | `dj` to `j`, `tj` to `c`, `nj` to `ny`, `sj` to `sy` | Superseded digraphs, before any single-letter rule can break them up |
| 4 | `ph` to `f`, `v` to `f` | Photo, Vica |
| 5 | `th` to `t`, `ch` to `k`, `kh` to `k` | Theory, Christian, khusus |
| 6 | `x` to `ks`, `q` to `k`, `z` to `s` | Taxi, Quran, zaman |
| 7 | `y` to `i`, only when not preceded by `n` or `s` | Sylvia and Silvia, while `ny` and `sy` survive step 3 |
| 8 | A doubled letter to a single one | Muhammad and Muhamad, Abdullah and Abdulah |

Write it as sequential statements rather than one nested expression, so the order stays readable:

```sql
CREATE FUNCTION fon(t text) RETURNS text
LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS $$
DECLARE s text := norm(t);
BEGIN
  s := replace(s, 'oe', 'u');                        -- 1
  s := replace(s, 'sch', 'sk');                      -- 2
  s := replace(s, 'sc', 'sk');
  s := replace(s, 'dj', 'j');                        -- 3
  s := replace(s, 'tj', 'c');
  s := replace(s, 'nj', 'ny');
  s := replace(s, 'sj', 'sy');
  s := replace(s, 'ph', 'f');                        -- 4
  s := replace(s, 'v', 'f');
  s := replace(s, 'th', 't');                        -- 5
  s := replace(s, 'ch', 'k');
  s := replace(s, 'kh', 'k');
  s := replace(s, 'x', 'ks');                        -- 6
  s := replace(s, 'q', 'k');
  s := replace(s, 'z', 's');
  s := regexp_replace(s, '(?<![ns])y', 'i', 'g');    -- 7
  s := regexp_replace(s, '(.)\1', '\1', 'g');        -- 8
  RETURN s;
END $$;
```

Step 7 relies on a lookbehind, which PostgreSQL's advanced regular expressions support. **Running it without the guard turns `banyak` into `baniak` and `syarat` into `siarat`**, undoing step 3.

Worked through, `scandal` and `skandal` both fold to `skandal` at step 2, and `Vica` and `Fica` both fold to `fica` at step 4. The `c` in `fica` is left alone on purpose, for the reason below.

Two rules about extending this list:

- **Never fold a bare `c` to `k`.** It is the obvious next step and it is wrong. In Indonesian `c` is the sound in `cari`, `cara`, and `cabang`, so folding it collides those words with `kari`, `kara`, and `kabang`. Only the digraphs `sc` and `ch` fold, because only they are reliably the `k` sound.
- **The list is the standard's, not the project's.** A project that adds its own fold produces a key no other project produces, and two systems searching the same data then disagree about who matches. Add a fold here first, then rebuild the generated columns everywhere that uses it.

## Columns and Indexes

**Build one searchable column per table** rather than searching several columns with `OR`. A single GIN index on one concatenated column outperforms a planner trying to combine several, and it keeps the ladder to one predicate per stage.

```sql
ALTER TABLE documents
  ADD COLUMN search_norm text GENERATED ALWAYS AS
    (norm(coalesce(title,'') || ' ' || coalesce(party,''))) STORED,
  ADD COLUMN search_fon  text GENERATED ALWAYS AS
    (fon(coalesce(title,'') || ' ' || coalesce(party,'')))  STORED;

CREATE INDEX documents_search_norm_idx ON documents (search_norm);
CREATE INDEX documents_search_pre_idx  ON documents (search_norm text_pattern_ops);
CREATE INDEX documents_search_fon_idx  ON documents USING gin (search_fon gin_trgm_ops);
```

- **Use `STORED` generated columns**, so the fold is computed on write and never per row at read time.
- **Concatenate with a separator and guard every nullable part with `coalesce`**, or one `NULL` empties the whole key.
- **`text_pattern_ops` is required for the prefix index.** A default B-tree in a non-C collation does not serve `LIKE 'q%'`.
- Every column named in a `WHERE`, `JOIN`, or `ORDER BY` of a filter is indexed, as [[database.rules.md]] already requires. The trigram index is an addition on top of that, not a replacement.
- **Every index and every generated column arrives through a migration**, per [[database.rules.md]]. Never add one by hand on a running database.

**Trigram indexes are large and slow writes.** Add one to a column a user actually searches, not to every text column in the schema.

## Ranking and Thresholds

- Stage 3 orders by similarity descending, **with a stable tiebreaker such as the primary key**, so a row never changes page between two identical requests.
- **The default similarity floor is `0.3`.** Below it the results stop resembling the query. Tune per field, and record the value in the project README when it differs.
- Use `word_similarity` instead of `similarity` when a short query is being matched inside a long title, since plain similarity punishes the length difference.
- **Never mix scores from different stages into one list.** The ladder returns the first stage that answered, not a merged set.

## Filters

- **Apply every filter in the database.** Never fetch rows and filter them in application or client code. This is a correctness rule before it is a performance rule: a filter applied after pagination filters one page and silently drops the rest.
- **Build the filters for one resource in one shared function**, used by the list endpoint, the export endpoint, and the count. Write it as a single `apply_filters` that takes a query and returns it narrowed.

> [!warning]
> That shared function exists because of a real failure. The list and the export each wrote their own filters, the export implemented only one of the five the page offered, and the framework drops an unknown query parameter without warning, so every export silently contained the whole table and nothing looked wrong.

- Combine filters with `AND`, and a multi-select within one filter with `IN`.
- **Filter a date with a half-open range on the date column**, `>= start AND < end`. Never format the column to text and pattern-match it, which cannot use the index.
- **Never cast a column to text to compare it.** The cast discards the index and changes the comparison rules.
- **Bind every value as a parameter.** Never build SQL by string concatenation, per [[security.rules.md]].
- Paginate every list, per [[pagination.component.md]]. Prefer keyset pagination on a large table; `OFFSET` degrades as the offset grows because the rows still have to be walked.
- **Run `EXPLAIN ANALYZE` on a new search or filter before shipping it**, and confirm the index is used rather than assuming it.

## The Search Box

```css
.search { flex: 1; min-width: 200px; display: flex; align-items: center; gap: 9px;
  border: 1px solid var(--line); border-radius: var(--r-sm); padding: 9px 13px; background: var(--surface); }
.search input { border: none; outline: none; flex: 1; font-size: 13.5px;
  font-family: inherit; background: transparent; }
.search i { color: var(--ink3); }
```

- **Debounce input by 300ms.** Do not send a request per keystroke.
- **Cancel the in-flight request when a newer one is sent**, so a slow early response cannot overwrite a fast later one.
- Show the loading state per [[loading.component.md]]. A search that is running is an inline section load, not a route gate; the list stays visible.
- **Keep the query in the URL**, per [[refresh.component.md]], so a search survives a refresh and can be sent to someone else.
- Show the empty state per [[uix.component.md]] when nothing matches, never a blank area.
- The filters sit next to the search box in the same toolbar and are applied together, as one request.

### Say When the Answer Is Approximate

When the ladder answered from stage 3, say so above the results. The user typed something that did not exist and is looking at rows that do not contain their word; without a line saying so, the list reads as wrong.

| Situation | Copy |
| :- | :- |
| Stage 1 or 2 answered | No message; the results are exact |
| Stage 3 answered | Showing the closest matches for "skandal" |
| Nothing answered | No results for "skandal". Check the spelling, or change the filters |

Copy is sentence case in the project's UI language, per [[uix.component.md]]. **Never show the similarity score, the stage number, or the folded key to the user.**

## Security and Privacy

- **A search runs inside the same authorization as the list it searches.** Never let a search reach a row the user could not have listed; a fuzzy match is an excellent way to confirm that a record exists without having permission to read it.
- **Never log a raw search query alongside anything identifying.** A query is often a person's name, which [[security.rules.md]] treats as personal data.
- **Rate limit the search endpoint.** It is the cheapest endpoint to call in a loop and the most expensive to serve.
- Bind every parameter. A search box is the most obvious injection surface in an app.
- **Never build a highlighted result by concatenating HTML around the matched text.** Split the string and render the parts as children, per [[security.rules.md]].

## Do and Do Not

Do:

- Decide filter or search per column, and keep fuzzy matching to free text a human wrote.
- Run the ladder in order, and stop at the first stage that answers.
- Reject an empty, too short, or absurdly long query before building any SQL.
- Generate the normalized and phonetic columns with shared `IMMUTABLE` SQL functions, and index both.
- Build one searchable column per table with one GIN trigram index, rather than an `OR` across several columns.
- Write filters for a resource once, and use that one function for the list, the export, and the count.
- Tell the user when the results are approximate.

Do not:

- Fuzzy match an identifier, a contract number, an amount, or a date.
- Fold a bare `c` to `k`, or add a project-local fold to the phonetic list.
- Use a leading-wildcard `LIKE` on a column with no trigram index.
- Filter, sort, or paginate in application or client code after fetching rows.
- Cast a column to text, or wrap it in a function, in order to compare it.
- Add a trigram index to every text column in the schema.
- Send a request per keystroke, or let a stale response overwrite a newer one.
- Show a similarity score, a stage, or a phonetic key to the user.

## Deviations

Any intentional deviation is documented in the project README, with the reason and a plan to return to the standard.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Accessibility requirements
3. Direct user instructions
4. [[database.rules.md]] and [[uix.component.md]]
5. This search standard
6. Existing project conventions

A direct user instruction must not override security, privacy, or accessibility requirements.

## Related

- [[uix.component.md]]
- [[table.component.md]]
- [[pagination.component.md]]
- [[calendar.component.md]]
- [[loading.component.md]]
- [[refresh.component.md]]
- [[database.rules.md]]
- [[api.rules.md]]
- [[security.rules.md]]
- [[stacks.rules.md]]
