# Workflow Implement Command Prompt: /workflow-implement

This is a Codex-facing slash prompt. The operator should not run terminal commands.

Use this prompt only when the operator explicitly asks to implement approved
workflow work.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - the relevant repo skill under `skills/<skill-id>/SKILL.md`
   - `.agents/skills/implement/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Confirm the active run has already passed grilling and, when applicable,
   PRD/issues.
5. Checkpoint the active run to `current_skill=implement`.
6. Implement only the approved scope.
7. Run the relevant gates and prepare for code review.

## Do Not

- Do not implement from a raw first message.
- Do not implement from a first grilling answer.
- Do not skip validation.

## Arguments

$ARGUMENTS: approved implementation scope, PRD, issue, or workflow run id.
