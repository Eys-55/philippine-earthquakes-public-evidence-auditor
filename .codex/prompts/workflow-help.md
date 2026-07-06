# Workflow Help Command Prompt: /workflow-help

Use this prompt to show the operator the available workflow and tracker slash
commands for `/Users/acecanacan/Documents/market-research-agent`.

This is a Codex-facing slash prompt. The operator should not run terminal
commands.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load `AGENTS.md` and `skills/control-repo-manager/SKILL.md`.
3. Run `node scripts/control-repo.mjs tracker-status` internally if current
   workflow state would help explain which slash to use next.
4. Show the available slash commands as a concise grouped list.
5. Explain which command to use next based on the current tracker state, if
   there is an obvious next command.

## Slash Commands To Show

Workflow entry:

- `/workflow-router` - route any workflow, bug, project edit, continuation, or
  phase request.
- `/workflow-intake` - explicitly create or lock workflow intake.
- `/tracker-workflow` - tracker-specific alias for workflow intake.

Workflow phases:

- `/workflow-grilling` - continue one-question-at-a-time grilling.
- `/workflow-to-prd` - move from agreed grilling context into PRD synthesis.
- `/workflow-to-issues` - break an approved PRD or plan into vertical slices.
- `/workflow-implement` - implement approved scope only.
- `/workflow-code-review` - review implementation against spec and standards.
- `/workflow-closeout` - validate, close tracker state, commit, push, and verify
  upload.

Tracker:

- `/tracker-status` - show tracker-backed project and workflow status.
- `/tracker-closeout` - close out tracker-backed work.
- `/workflow-help` - show this help.

## Do Not

- Do not tell the operator to run terminal commands.
- Do not use Python.
- Do not start a workflow phase from help unless the operator explicitly asks.

## Arguments

$ARGUMENTS: optional focus, such as "earthquake", "status", "next", or a
workflow run id.
