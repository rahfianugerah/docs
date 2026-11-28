# Boundary Rule Examples

Working configurations for both halves of the stack. Both were run against real files: every banned import below is reported, and every allowed one passes. Copy the shape, then replace the folder names and messages with the project's own.

## TypeScript: ESLint Flat Config

The layout these rules enforce:

```text
src/
  lib/          pure helpers: no React, and nothing else from src
  api/          the HTTP client: imports src/lib only
  components/   shared UI: never a feature or a page
  features/x/   one feature: other folders import it through features/x/index.ts only
  pages/        routes: compose features through their index
  **/*.hot.ts   code on a hot path: no allocation inside a function
```

`no-restricted-imports` matches the import string as written, never the resolved file, so `../billing/api` would walk around every rule. The first pattern therefore bans parent-relative imports: anything that leaves its folder goes through the `@/` alias, which the rules can read.

`eslint.config.js`, for ESLint 9.22 or later with `typescript-eslint`:

```js
// Lint config: the recommended rules, then the directory boundaries.
import { existsSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import tseslint from "typescript-eslint";

const featuresDir = fileURLToPath(new URL("./src/features", import.meta.url));
const features = existsSync(featuresDir)
  ? readdirSync(featuresDir, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
  : [];

const deepFeatureImport = "Import a feature through its index, @/features/<name>, never a file inside it.";

// A later block's options for a rule replace an earlier block's, so every block repeats the shared pattern.
const restrict = (...patterns) => ({
  "no-restricted-imports": [
    "error",
    {
      patterns: [
        { regex: "^\\.\\./", message: "Leave a folder through the @/ alias, so the boundary rules can read where an import goes." },
        ...patterns,
      ],
    },
  ],
});

export default defineConfig([
  globalIgnores(["dist/"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [js.configs.recommended, tseslint.configs.recommended],
  },
  { files: ["src/**/*.{ts,tsx}"], rules: restrict() },
  {
    files: ["src/lib/**/*.{ts,tsx}"],
    rules: restrict(
      { group: ["react", "react/*", "react-dom", "react-dom/*"], message: "src/lib holds pure helpers: no React." },
      { regex: "^@/(?!lib/)", message: "src/lib imports nothing from src outside src/lib." },
    ),
  },
  {
    files: ["src/api/**/*.{ts,tsx}"],
    rules: restrict({ regex: "^@/(?!lib/|api/)", message: "src/api imports only src/lib and itself." }),
  },
  {
    files: ["src/components/**/*.{ts,tsx}"],
    rules: restrict({ regex: "^@/(features|pages)(/|$)", message: "A shared component never imports a feature or a page." }),
  },
  ...features.map((name) => ({
    files: [`src/features/${name}/**/*.{ts,tsx}`],
    rules: restrict(
      { regex: "^@/pages(/|$)", message: "A feature never imports a page." },
      { regex: `^@/features/(?!${name}/)[^/]+/`, message: deepFeatureImport },
    ),
  })),
  {
    files: ["src/pages/**/*.{ts,tsx}"],
    rules: restrict({ regex: "^@/features/[^/]+/", message: deepFeatureImport }),
  },
  {
    files: ["src/**/*.hot.ts"],
    rules: {
      "no-restricted-syntax": [
        "error",
        { selector: ":function NewExpression", message: "No allocation in a hot path: reuse an instance made at module level." },
        { selector: ":function ArrayExpression", message: "No allocation in a hot path: reuse an array made at module level." },
        { selector: ":function ObjectExpression", message: "No allocation in a hot path: reuse an object made at module level." },
        { selector: ":function :function", message: "No closure in a hot path: move the function to module level." },
      ],
    },
  },
]);
```

Keep the project's other blocks, such as React Hooks and React Refresh, in the same array above the boundary blocks.

The alias the rules depend on. `tsconfig.app.json`:

```json
{
  "compilerOptions": {
    "paths": { "@/*": ["./src/*"] }
  }
}
```

`vite.config.ts`:

```ts
// Vite config: React, and the @/ alias the lint boundaries rely on.
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) } },
});
```

Notes:

- **One block per feature** is generated from the folder names, because a regex cannot know which feature the linted file belongs to. A new feature folder gets its block on the next run.
- **The blocks replace, they do not merge.** When two blocks match a file and both set `no-restricted-imports`, the later block's options win whole. `restrict()` puts the shared pattern into every block, so no file loses it.
- **`regex` matches case-insensitively** unless the pattern sets `caseSensitive: true`.
- **A filename convention** is a `files` glob plus `no-restricted-syntax`. The selectors are esquery: `:function` matches any function, so `:function NewExpression` is a `new` anywhere inside one, while a buffer made at module level passes.

Run it:

```bash
npx eslint .
```

## Python: Ruff `banned-api`

The layout these rules enforce:

```text
app/
  main.py      wires the routers
  core/        settings and logging: imports no other app package
  api/         routers: call services, never the database
  services/    business logic: no FastAPI, no routers
  db/          engine, models, repositories: the only package that runs SQL
test/          mirrors app/, and may import anything
```

`TID251` bans an import everywhere its configuration applies, and Ruff uses the closest configuration file above each Python file. So a boundary is a `ruff.toml` in the folder it guards, extending the project's `pyproject.toml`.

`pyproject.toml`, the project-wide part:

```toml
[tool.ruff]
target-version = "py313"

[tool.ruff.lint]
extend-select = ["TID"]

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"psycopg2".msg = "The stack uses psycopg 3: import psycopg."
```

`ban-relative-imports = "all"` is the Python twin of the alias rule above: every import names its package, so `banned-api` can read where it goes.

`app/core/ruff.toml`:

```toml
# Boundaries for app/core: everything imports it, so it imports no other app package.
extend = "../../pyproject.toml"

[lint.flake8-tidy-imports.banned-api]
"psycopg2".msg = "The stack uses psycopg 3: import psycopg."
"app.api".msg = "app.core imports no other app package; everything imports it."
"app.services".msg = "app.core imports no other app package; everything imports it."
"app.db".msg = "app.core imports no other app package; everything imports it."
```

`app/api/ruff.toml`:

```toml
# Boundaries for app/api: a router calls services and never touches the database.
extend = "../../pyproject.toml"

[lint.flake8-tidy-imports.banned-api]
"psycopg2".msg = "The stack uses psycopg 3: import psycopg."
"sqlalchemy".msg = "A router never touches the database: call a service in app.services."
"app.db".msg = "A router never touches the database: call a service in app.services."
```

`app/services/ruff.toml`:

```toml
# Boundaries for app/services: business logic knows nothing about HTTP.
extend = "../../pyproject.toml"

[lint.flake8-tidy-imports.banned-api]
"psycopg2".msg = "The stack uses psycopg 3: import psycopg."
"fastapi".msg = "A service knows nothing about HTTP: raise a domain error, and let the router map it to a status."
"starlette".msg = "A service knows nothing about HTTP: raise a domain error, and let the router map it to a status."
"app.api".msg = "A service never imports a router."
```

`app/db/ruff.toml`:

```toml
# Boundaries for app/db: the only package that runs SQL, called by services and calling nothing above it.
extend = "../../pyproject.toml"

[lint.flake8-tidy-imports.banned-api]
"psycopg2".msg = "The stack uses psycopg 3: import psycopg."
"fastapi".msg = "The database layer knows nothing about HTTP."
"starlette".msg = "The database layer knows nothing about HTTP."
"app.api".msg = "The database layer calls nothing above it."
"app.services".msg = "The database layer calls nothing above it."
```

Notes:

- **A nested `banned-api` table replaces the root one, it does not merge.** That is why every nested file repeats the `psycopg2` ban. Leave it out, and `app/api/` may import `psycopg2` again.
- **Banning a module bans its submodules**: `"app.db"` also reports `from app.db.repositories import orders` and `import app.db.session`.
- **A boundary is a folder.** `banned-api` cannot single out a file name such as `router.py`, and `per-file-ignores` lifts every `TID251` ban from a file at once. Where a layer matters, give it a folder.

Run it:

```bash
ruff check --select TID .
```

## Show Each Rule Failing

A rule never seen failing proves nothing. For each rule, add one scratch import it must reject, run the linter, see the message, then delete the scratch line:

```bash
echo 'import { Home } from "@/pages/Home";' >> src/components/Button.tsx && npx eslint src/components/Button.tsx
echo 'from app.db.session import engine' >> app/api/orders.py && ruff check --select TID app/api/orders.py
```
