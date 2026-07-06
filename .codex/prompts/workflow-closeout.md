# Workflow Closeout Command Prompt: /workflow-closeout

This is a Codex-facing slash prompt. The operator should not run terminal commands.

Use this prompt to close or hand off a tracked workflow run.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - the relevant repo skill under `skills/<skill-id>/SKILL.md`
3. Run the internal gates that match the work:
   - `npm test`
   - `npm run validate`
   - `npm run build` when UI or dashboard data changed
   - `git diff --check`
4. Close or checkpoint the tracker run with validation results.
5. Commit and push when changes are intended for the repo.
6. Run `npm run tracker:upload-gate` and report live upload truth.

## Do Not

- Do not claim upload completion without the live upload gate.
- Do not leave completed work in an open run.
- Do not ask the operator to run terminal commands.

## Arguments

$ARGUMENTS: workflow run id or closeout focus.
