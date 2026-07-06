# Workflow To PRD Command Prompt: /workflow-to-prd

This is a Codex-facing slash prompt. The operator should not run terminal commands.

Use this prompt only after grilling has reached shared understanding and the
operator asks to move to PRD.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - the relevant repo skill under `skills/<skill-id>/SKILL.md`
   - `.agents/skills/to-prd/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Checkpoint the active run to `current_skill=to-prd`.
5. Follow `.agents/skills/to-prd/SKILL.md`: synthesize from existing context,
   explore the repo if needed, and check testing seams with the operator.

## Do Not

- Do not interview from scratch.
- Do not publish or create external issues unless the operator explicitly asks.
- Do not skip tracker checkpointing.

## Arguments

$ARGUMENTS: optional PRD focus.
