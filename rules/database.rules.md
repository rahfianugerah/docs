> Up: [[README.md]]

# Database Standard

## Core Requirement

PostgreSQL, accessed through **SQLAlchemy 2.x**, migrated through **Alembic**.

Two query methods are sanctioned, and each has cases it owns. The ORM is the default; raw SQL is the deliberate exception, chosen for a reason you can name. **Neither method ever builds SQL by string formatting.**

## Engine

- **PostgreSQL** for anything deployed, anything with concurrent writers, and anything with a real schema.
- **SQLite** is fine for a local, single-process, single-user project: an analysis script, a small CLI, a cache of scraped data. It is genuinely simpler and needs no server.
- SQLite stops being fine the moment there are concurrent writers or a deployment. It locks the whole database on write, and the migration to Postgres later is more work than starting there.
- **A parquet file on disk is not a worse database than Postgres for a dataset that is read whole and never updated.** Do not put a static training set in a database because it feels more professional; a database earns its place when you need queries, constraints, or concurrent writes.
- Any other engine is a written decision, not a default.

## ORM or Raw SQL

The ORM is where you start. Reach for raw SQL when one of the cases below applies, and say why in a comment.

| Use the **ORM** for | Use **raw SQL** for |
| :- | :- |
| CRUD on a single entity | Aggregation and analytics: window functions, CTEs, `GROUPING SETS` |
| Anything that maps to objects and relationships | Bulk insert, bulk upsert, `COPY` |
| Writes inside a transaction, where the unit of work handles ordering and rollback | Extracting a dataframe for analysis or training |
| A query whose shape changes with user filters | A Postgres feature the ORM expresses awkwardly: `DISTINCT ON`, JSONB operators, array operators, full-text search |
| Anything the next reader must understand without knowing the schema deeply | A query the ORM generates slowly, where `EXPLAIN ANALYZE` shows the plan is the problem |
| Anything Alembic autogenerate needs to see | A one-off migration backfill |

### Why the ORM Is the Default

- It parameterizes automatically, so the most common security bug cannot happen by accident.
- It gives you transactions, identity mapping, and relationship loading without hand-writing them.
- It survives a schema change: rename a column in the model and the queries follow. Raw SQL silently breaks and only fails at runtime.
- Alembic autogenerate reads the models. A table only ever touched by raw SQL drifts out of the migration history.

```python
stmt = select(Run).where(Run.dataset_id == dataset_id).order_by(Run.created_at.desc())
runs = session.scalars(stmt).all()
```

### Why Raw SQL Earns Its Place

Some queries are clearer, faster, or only possible in SQL. Forcing them through the ORM produces something slower and harder to read than the SQL it generates.

```python
# Raw: a window function per group. The ORM can express this, but the result reads
# worse than the SQL and nobody maintaining it would prefer the ORM version.
sql = text("""
    SELECT dataset_id, run_id, metric,
           RANK() OVER (PARTITION BY dataset_id ORDER BY metric DESC) AS rank
    FROM runs
    WHERE created_at >= :since
""")
rows = session.execute(sql, {"since": since}).mappings().all()
```

```python
# Raw: straight to a dataframe. Hydrating ORM objects only to convert them is
# pure waste, and for an ML project this is the common path.
import polars as pl
df = pl.read_database(
    "SELECT feature_a, feature_b, label FROM samples WHERE split = :split",
    connection=engine,
    execute_options={"parameters": {"split": "train"}},
)
```

### Rules for Raw SQL

1. **Always bind parameters.** `:name` with a dictionary, never an f-string, never `%`, never `+`, never `.format()`.
2. **An identifier cannot be bound.** A table name, a column name, or a sort direction that comes from user input is matched against an allowlist in Python, and anything not on the list is rejected.
3. **It lives in the data-access layer**, in a named constant or a `.sql` file next to the repository that uses it. Never inline in a route, a view, or a notebook cell that gets copied.
4. **Name the reason in a comment.** "Raw: window function" or "Raw: ORM plan was a seq scan, see EXPLAIN". A raw query with no reason gets rewritten as ORM by the next person, or worse, copied.
5. **Measure before switching.** "The ORM is slow" is almost always an N+1, not the ORM. Fix the loading strategy first; if it is still slow, then reach for SQL.
6. **A raw query is still code.** It gets a test, because nothing else will catch it when the schema moves.

```python
SORT_COLUMNS = {"metric": "metric", "created": "created_at"}   # allowlist

def top_runs(session, sort_by: str, limit: int):
    column = SORT_COLUMNS.get(sort_by)
    if column is None:
        raise ValueError(f"unknown sort column: {sort_by}")
    # Raw: ORDER BY on an allowlisted identifier, which cannot be bound
    sql = text(f"SELECT * FROM runs ORDER BY {column} DESC LIMIT :limit")
    return session.execute(sql, {"limit": limit}).mappings().all()
```

That f-string is safe **only** because `column` came from the allowlist and can never be user input. It is the one place formatting into SQL is permitted, and it needs the allowlist directly above it.

## Schema

- Normalize by default. Denormalize only for a measured need, and write the reason next to the column.
- Every table has a primary key.
- Use the type that matches the data: `NUMERIC` for money, `TIMESTAMPTZ` for time, `JSONB` for genuinely unstructured data, a real type for everything else. Never a string standing in for a number, a date, or an enum.
- `snake_case` for tables and columns, one pluralization convention applied everywhere.
- Store vectors in `pgvector` if they are queried by similarity; store them in a file if they are read whole.

## Integrity

- Every relationship gets a foreign key constraint. Application code is not a constraint.
- Every required column is `NOT NULL`. An empty string is not a way of saying "no value".
- A natural key gets a `UNIQUE` constraint.
- A bounded value gets a `CHECK` constraint.
- Set `ON DELETE` explicitly on every foreign key. The default is a decision nobody made.
- A multi-step write goes in a transaction.

## Queries

- Index every foreign key, and every column in a `WHERE`, `JOIN`, or `ORDER BY` of a query you run often.
- Select the columns you need. `SELECT *` in application code breaks when a column is added.
- **Watch for N+1.** Accessing a relationship inside a loop issues one query per row. Use `selectinload` or a join.
- Paginate anything that returns a list. An unbounded query works until the table grows.
- Run `EXPLAIN ANALYZE` on a slow query before optimizing it. The plan says what is wrong; guessing does not.
- Use connection pooling, and keep the pool small: `max-instances x (pool + overflow)` must fit inside the server's `max_connections`, per [[deploy.rules.md]].
- Close connections and sessions explicitly. A leaked session holds a connection until the pool starves.

## Migrations

- Every schema change goes through an Alembic migration, committed with the code that needs it.
- Read the autogenerated migration before running it. Autogenerate misses a rename, seeing a drop and an add, which loses the data.
- Write a downgrade where the change is reversible. Where it is not, say so in the migration docstring.
- A migration that backfills data is a migration, not a script someone runs by hand and forgets.
- Never edit a migration that has already run somewhere. Write a new one.
- Migrations run as a job, never at container startup, per [[deploy.rules.md]].

## Security

- Credentials come from the environment or a secret store, never from source, per [[secret.rules.md]].
- The application connects as a least-privilege user. Not the superuser, and not the owner if a reader will do.
- No public IP on a deployed database. See [[deploy.rules.md]].
- Never format user input into SQL. [[security.rules.md]] owns this in full, and it is the single most common way an application is compromised.

> [!warning]
> An identifier cannot be bound, so a table or column name from user input passes through an allowlist in Python. That is the one place formatting into SQL is permitted, and it needs the allowlist directly above it.

## Machine Learning

- **A training extraction query is versioned code**, in the repository, not typed into a notebook. A dataset nobody can regenerate is not reproducible.
- Record the query, or a hash of it, alongside the run that used it, per [[docs.rules.md]].
- Extract to a dataframe with raw SQL. Do not hydrate a million ORM objects to build a matrix.
- Do not run experiments against a live application database. Snapshot to a file, or read a replica.
- Write features once and read them many times; a feature computed inside the training loop is computed again at inference, differently, and that is where training and serving skew comes from.

## Definition of Done

- Every query is ORM or parameterized raw SQL. No SQL is built by string formatting.
- Every raw query says in a comment why it is raw, and lives in the data-access layer.
- Any identifier from user input passes through an allowlist.
- Every foreign key, required column, natural key, and bounded value has its constraint.
- Every schema change has a reviewed Alembic migration.
- Frequent query columns are indexed, and no loop issues a query per row.
- Credentials come from the environment, and the app connects as a least-privilege user.

## Applies To

- [[codes.rules.md]]
- [[security.rules.md]]
- [[secret.rules.md]]
- [[deploy.rules.md]]
- [[deploy.cloud.md]]
