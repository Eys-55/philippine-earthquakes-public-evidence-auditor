# Workflow To Issues Command Prompt: /workflow-to-issues

This is a Codex-facing slash prompt. The operator should not run terminal commands.

Use this prompt only after a PRD or plan exists and the operator asks to break
it into issues.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - the relevant repo skill under `skills/<skill-id>/SKILL.md`
   - `.agents/skills/to-issues/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Checkpoint the active run to `current_skill=to-issues`.
5. Follow `.agents/skills/to-issues/SKILL.md`: draft vertical slices, quiz the
   operator on granularity and dependencies, then publish only after approval.

## Do Not

- Do not skip the quiz.
- Do not create issues before approval.
- Do not use horizontal slices.

## Arguments

$ARGUMENTS: PRD path, plan path, issue reference, or issue-breakdown focus.
