# Workflow Code Review Command Prompt: /workflow-code-review

This is a Codex-facing slash prompt. The operator should not run terminal commands.

Use this prompt after implementation or when the operator asks for review.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load:
   - `AGENTS.md`
   - `skills/control-repo-manager/SKILL.md`
   - `.agents/skills/code-review/SKILL.md`
3. Run `node scripts/control-repo.mjs tracker-status` internally.
4. Checkpoint the active run to `current_skill=code-review`.
5. Follow `.agents/skills/code-review/SKILL.md`: review against standards and
   spec as separate axes.
6. Lead with findings, ordered by severity, with file and line references.

## Do Not

- Do not bury findings below a summary.
- Do not review without a fixed point when one is required.
- Do not skip the spec axis silently.

## Arguments

$ARGUMENTS: fixed point, branch, commit, PRD/spec path, or review focus.
