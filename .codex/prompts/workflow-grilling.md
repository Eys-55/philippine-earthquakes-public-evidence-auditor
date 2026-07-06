# /workflow-grilling Slash Prompt

Continue one-question-at-a-time workflow grilling.

This is a Codex-facing slash prompt. It is only a thin command shim.
The workflow behavior lives in the repo skill named below.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Read `skills/workflow-grilling/SKILL.md` completely before acting.
3. Follow that skill exactly.
4. Run tracker adapters internally when the skill requires tracker state.
5. Do not ask the operator to run terminal commands.

## Skill To Use

- `skills/workflow-grilling/SKILL.md`

## Arguments

$ARGUMENTS: optional focus text for this slash command.
