# Workflow Intake Command Prompt: /workflow-intake

Use this prompt to create or lock tracked workflow intake in
`/Users/acecanacan/Documents/market-research-agent`.

This is a Codex-facing slash prompt. The operator should not run terminal
commands.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load `AGENTS.md`, `CONTEXT.md`, `skills/control-repo-manager/SKILL.md`, and
   the relevant repo skill under `skills/<skill-id>/SKILL.md`.
3. Load `.agents/skills/grilling/SKILL.md` because intake must hand off to
   grilling before the first question.
4. Run `node scripts/control-repo.mjs tracker-status` internally.
5. Create or lock a tracker session and workflow run internally.
6. Create or attach a context manifest under `ops/workflow-runs/`.
7. Checkpoint to `current_skill=grilling`.
8. Ask one context-aware grilling question.

## Do Not

- Do not tell the operator to run commands.
- Do not use Python.
- Do not implement during intake.

## Arguments

$ARGUMENTS: workflow report, bug, edit request, or continuation note.
