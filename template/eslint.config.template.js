// ESLint flat config for a Vite React TypeScript project. Copy it to eslint.config.js at the project root.
// Dev dependencies: eslint, @eslint/js, typescript-eslint, typescript, globals, eslint-plugin-react-hooks, eslint-plugin-react-refresh.
// typescript-eslint 8 supports TypeScript below 6.1 only, so pin typescript to ~6.0 while the type-aware rules are on.
// A required reason on every eslint-disable comment needs an extra plugin, so that check is left to review.
import js from '@eslint/js'
import { defineConfig, globalIgnores } from 'eslint/config'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import globals from 'globals'
import tseslint from 'typescript-eslint'

// The one file allowed to defer work to the next macrotask, so every deliberate deferral is in one place.
const deferAllowlist = ['src/lib/defer.ts']

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommendedTypeChecked,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2023,
      globals: globals.browser,
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    linterOptions: { reportUnusedDisableDirectives: 'error' },
    rules: {
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
      'no-empty': 'error',
      'no-restricted-syntax': [
        'error',
        {
          selector:
            "CallExpression:matches([callee.name='setTimeout'], [callee.property.name='setTimeout']):matches([arguments.length<2], [arguments.1.value=0])",
          message: 'A zero-delay setTimeout hides an ordering bug. Fix the order, or defer through src/lib/defer.ts.',
        },
      ],
    },
  },
  {
    files: deferAllowlist,
    rules: { 'no-restricted-syntax': 'off' },
  },
  {
    // A later block replaces the options an earlier block gave the same rule, so keep one boundary block per folder.
    files: ['src/components/**'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['**/pages/**'],
              message: 'A shared component may not import from a page, not even a type. Move the shared type to src/shared/.',
            },
          ],
        },
      ],
    },
  },
])
