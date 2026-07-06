# Workflow Grilling Command Prompt: /workflow-grilling

This is a Codex-facing slash prompt. The operator should not run terminal commands.

Use this prompt to continue the Matt Pocock `grilling` phase for a tracked
workflow in `/Users/acecanacan/Documents/market-research-agent`.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - the relevant repo skill under `skills/<skill-id>/SKILL.md`
   - `.agents/skills/grilling/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Ensure the active workflow run is checkpointed to
   `current_skill=grilling`.
5. Ask exactly one context-aware question.
6. Provide the recommended answer with the question.
7. If the answer can be found by reading repo files, read the files instead of
   asking.

## Do Not

- Do not ask multiple questions at once.
- Do not implement.
- Do not move to PRD, issues, implementation, or review until the operator
  explicitly confirms shared understanding or asks for the next phase.

## Arguments

$ARGUMENTS: optional focus for the grilling question.
