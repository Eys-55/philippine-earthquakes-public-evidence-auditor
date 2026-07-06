# Tracker Command Prompt: /tracker-closeout

Use this prompt to close out tracker-backed work in
`/Users/acecanacan/Documents/market-research-agent`.

This is a Codex-facing slash prompt. Do not ask the operator to open a
terminal. Run validation, closeout, commit, push, and upload checks internally
when the repo work is intended to be saved.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load `AGENTS.md` and `skills/control-repo-manager/SKILL.md`.
3. Run the relevant gates:

   ```bash
   npm test
   npm run validate
   npm run build
   git diff --check
   ```

4. If a workflow run is complete, close it with
   `node scripts/control-repo.mjs tracker-workflow-close` and include
   validation results.
5. Commit and push intended repo changes.
6. Run:

   ```bash
   npm run tracker:upload-gate
   ```

7. Report upload truth from the live gate, not only from recorded sync evidence.

## Arguments

$ARGUMENTS: optional closeout focus or workflow run id.
