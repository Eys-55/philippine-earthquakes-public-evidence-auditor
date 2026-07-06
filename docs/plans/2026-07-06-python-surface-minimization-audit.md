# Python Surface Removal Audit

Date: 2026-07-06
Workflow run: `wfr-20260706-155039-502f`
Status: active zero-runtime pass

## Objective

Remove Python as the workflow runtime for this workspace. Skills remain the
operator-facing workflow surface. Codex chat remains the operator surface. The
user never opens a terminal to create, checkpoint, validate, or close tracker
state.

## Result

- Starting Python files before reduction: 41 tracked files.
- Previous reduction pass: 26 remaining files.
- Current Python files in the working tree: 0.
- Current internal adapter files: 1 Node file.
- Current test files: 1 Node test file.

The remaining internal adapter is:

- `scripts/control-repo.mjs`

The current test guard is:

- `tests/control-repo.test.mjs`

## Runtime Boundary

The repo no longer has separate command-era scripts for workflow intake,
workflow catalog lookup, tracker session start, workflow checkpoint, tracker
status, upload gates, validation, or UI export.

Those operations are now internal subcommands of the Node control adapter:

```bash
node scripts/control-repo.mjs tracker-status
node scripts/control-repo.mjs tracker-session-start
node scripts/control-repo.mjs tracker-workflow-start
node scripts/control-repo.mjs tracker-workflow-checkpoint
node scripts/control-repo.mjs tracker-workflow-close
node scripts/control-repo.mjs tracker-upload-gate
node scripts/control-repo.mjs validate-all
node scripts/control-repo.mjs export-tracker-ui-data
```

These are internal Codex adapters, not operator instructions.

## Operator Contract

The operator says the work in Codex chat:

- "I found a bug in my workflow."
- "I am building a workflow."
- "Continue the workflow."
- "Close this out."

Codex then uses the relevant skill, loads ECC/context, and persists tracker
state internally through the Node adapter. The user is not expected to know or
run the adapter.

## Current Package Gates

```bash
npm test
npm run validate
npm run build
git diff --check
```

`npm test` includes a filesystem guard that fails if any file with the Python
extension exists outside ignored build/dependency directories.

## Current Rule

No Python files belong in this repo. If a future workflow needs automation, add
the behavior to:

1. the canonical skill under `skills/`;
2. durable tracker/data/status artifacts under `ops/`, `data/`, or `docs/`;
3. the Node control adapter only if Codex needs an internal persistence or
   validation operation.
