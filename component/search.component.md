> Up: [[README.md]] · [[uix.component.md]]

# Search Standard

## Core Requirement

A search that returns nothing for a correctly remembered name is worse than no search, because the user concludes the record does not exist.

This file covers both halves: how the query is matched in the database, and how the box behaves on screen. It extends [[uix.component.md]] and [[database.rules.md]].

## Filter or Search

They are different features and are built differently.

| | Filter | Search |
| :- | :- | :- |
| Input | A known set of values | Free text |
| Match | Exact, on a column | Fuzzy, across several columns |
| Result | A subset | A ranked list |
| Empty result means | Nothing matches those criteria | Possibly a spelling difference |

**A filter is not a search box.** A status filter is a select, per [[dropdown.component.md]]. Do not make the user type a status into a search field, and do not make a search field behave like an exact filter.

## The Search Ladder

Climb only as far as the data requires. Each rung costs more to build and to run.

1. **Exact match** on an identifier. Fast, unambiguous, and the right answer when the user pasted a code.
2. **Prefix match**, for a type-ahead on a name.
3. **Substring match**, when the term can appear anywhere in the value.
4. **Trigram similarity**, which tolerates a typo and a transposition.
5. **Full text search**, when the target is prose rather than a name.

Most searches over people, orders, or documents stop at rung four. Do not reach for full text search on a table of names; it stems and ranks in ways that make short names behave unpredictably.

## Fail Fast Before the Database

- **A query shorter than the minimum returns nothing, without a request.** Two characters against a large table is a sequential scan that returns a screen of noise.
- Trim and collapse whitespace before deciding the query is empty.
- Debounce the input, so typing eight characters is one request rather than eight.
- Cancel the in-flight request when the query changes, or results arrive out of order and the user sees answers to a query they already replaced.

## Normalization

Both the stored value and the query pass through the same normalization, in the same order. **A normalization applied to only one side is why a search fails on exactly the records it should find.**

- Case fold.
- Strip accents and diacritics.
- Collapse repeated whitespace, and trim.
- Remove punctuation used inside names, such as an apostrophe or a hyphen, or treat it as a space consistently.

Store the normalized form in its own column and index that. Normalizing at query time on every row is a guaranteed sequential scan.

### The Phonetic Fold

Every language has pairs of letters people spell interchangeably in names. Where the project's language has them, fold them in normalization so both spellings reach the same record.

- Decide the pairs once from the actual data, and write them down beside the code.
- Apply the fold to both the stored column and the query.
- Keep the original value intact for display. **The fold is for matching, never for showing.** A user must see the name as it was recorded.

## Columns and Indexes

- Search a named set of columns, chosen deliberately. Never every column in the table.
- Index the normalized column with a trigram index where similarity is used, per [[database.rules.md]].
- Enable the extensions through a migration, never by hand on a live database.
- Run `EXPLAIN ANALYZE` on the real query with real data volume. A search that is fast on two hundred rows says nothing about two hundred thousand.

## Ranking and Thresholds

- Rank by match quality, then by a stable tiebreaker such as a name or a date, so equal matches do not shuffle between requests.
- Put an exact match first, always, however it scores.
- Set the similarity threshold from real queries, not from the default. Too low returns noise, too high returns nothing.
- Paginate, per [[api.rules.md]]. A search endpoint returning everything it matched is the unbounded query [[database.rules.md]] forbids.

## The Search Box

- One line, with a leading search icon and an accessible label. A placeholder is not a label.
- **A clear control appears once there is text**, and returns focus to the input.
- Show the loading state inside the box, per [[loading.component.md]], not as a page-level spinner.
- `Escape` clears the query. `Enter` submits where the search is not live.
- Do not steal focus on page load unless search is the page's only purpose.
- Where results replace a list in place, keep the list's height stable while loading so the page does not jump.

### Say When the Answer Is Approximate

- An empty result says the term found nothing **and** suggests what to try: fewer characters, a different spelling, or removing a filter. A bare "no results" leaves the user with nowhere to go.
- Where fuzzy matching produced the results, say so, so a user who expected an exact match understands why a near miss appeared.
- Where a filter is narrowing the results, say that too. Most "search is broken" reports are a filter the user forgot was on.
- Highlight the matched part in each result, so the reason it matched is visible.

## Security and Privacy

- **Search only what the user may see.** Apply the permission filter in the query, not after it, or the total count leaks the existence of records they cannot open, per [[security.rules.md]].
- Parameterize the query. A search box is the most exposed input in the product, per [[database.rules.md]].
- Never log the raw query where it may carry personal data.
- Rate limit the endpoint. An unthrottled fuzzy search is an expensive query anybody can run in a loop.

## Do and Do Not

Do:

- Normalize the stored value and the query identically.
- Index the normalized column.
- Return nothing below the minimum length, without a request.
- Put an exact match first.
- Say what to try when nothing matched.

Do not:

- Build a filter as a search box.
- Search every column.
- Normalize at query time on every row.
- Return an unbounded result set.
- Show a folded or normalized value to the user.

## Related

- [[uix.component.md]]
- [[dropdown.component.md]]
- [[loading.component.md]]
- [[database.rules.md]]
- [[api.rules.md]]
- [[security.rules.md]]
