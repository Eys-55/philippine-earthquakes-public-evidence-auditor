# Tracker Command Prompt: /tracker-workflow

Use this prompt when the operator is building, debugging, continuing, editing,
or starting a workflow in `/Users/acecanacan/Documents/market-research-agent`.

This is a Codex-facing slash prompt. Do not tell the operator to open a
terminal. The tracker adapter is internal plumbing that Codex runs on behalf of
the operator.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load these files before discussing the workflow:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - `skills/agent-workflow-project-maker/SKILL.md`
   - `.agents/skills/grilling/SKILL.md`
   - `.agents/skills/to-prd/SKILL.md`
   - `.agents/skills/to-issues/SKILL.md`
   - `.agents/skills/implement/SKILL.md`
   - `.agents/skills/code-review/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Create or lock a tracker session and workflow run internally with
   `node scripts/control-repo.mjs tracker-session-start` and
   `node scripts/control-repo.mjs tracker-workflow-start`.
5. Attach a context manifest under `ops/workflow-runs/` that proves the ECC,
   repo skill, and Matt Pocock phase files were loaded.
6. Checkpoint the workflow run to `current_skill=grilling` before asking the
   operator anything.
7. Ask exactly one context-aware grilling question and wait.

## Failure Rules

- Do not run or mention Python.
- Do not ask the operator to run tracker commands.
- Do not start implementation, renaming, moving files, scaffolding, or coding
  while the run is in grilling.
- Do not proceed if the Matt Pocock phase files have not been loaded.

## Arguments

$ARGUMENTS: workflow objective, bug report, edit request, or continuation note.
