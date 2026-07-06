# Workflow Router Command Prompt: /workflow-router

Use this prompt as the front door for every workflow, project, bug, issue, edit,
change, fix, update, continuation, or workflow-building request in
`/Users/acecanacan/Documents/market-research-agent`.

This is a Codex-facing slash prompt. The operator should not run terminal
commands. Codex must run tracker adapters internally.

## Required First Actions

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `CONTEXT.md`
   - `skills/control-repo-manager/SKILL.md`
   - `skills/agent-workflow-project-maker/SKILL.md`
   - `.agents/skills/grilling/SKILL.md`
   - `.agents/skills/to-prd/SKILL.md`
   - `.agents/skills/to-issues/SKILL.md`
   - `.agents/skills/implement/SKILL.md`
   - `.agents/skills/code-review/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Identify whether this is:
   - a new workflow,
   - a continuation of an existing workflow,
   - a bug in workflow behavior,
   - an edit/change/fix/update to a tracked project,
   - or a request to move phases.
5. Create or lock tracker state internally before asking questions.
6. Write or attach a context manifest proving loaded ECC, repo skill, tracker,
   and Matt Pocock phase files.
7. Checkpoint to `current_skill=grilling`.
8. Ask one context-aware grilling question only.

## Required Response Shape

- Loaded ECC proof
- Loaded project/workflow skill proof
- Loaded Matt Pocock phase file proof
- Tracker session/run proof
- Premise lock
- One grilling question

## Hard Stops

- If the Matt Pocock files were not loaded, stop and load them.
- If tracker state was not created or locked, stop and create or lock it.
- If the run is still `workflow_intake` after the context manifest exists,
  checkpoint it to `grilling`.
- Do not implement until grilling reaches shared understanding and the operator
  explicitly moves to PRD, issues, implementation, or review.

## Arguments

$ARGUMENTS: raw workflow report or operator request.
