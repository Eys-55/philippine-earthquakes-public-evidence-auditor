# Tracker Command Prompt: /tracker-status

Use this prompt to show tracker-backed project and workflow status for
`/Users/acecanacan/Documents/market-research-agent`.

This is a Codex-facing slash prompt. Do not ask the operator to open a
terminal. Run the tracker status adapter internally and summarize the result.

## Required Behavior

1. Work from `/Users/acecanacan/Documents/market-research-agent`.
2. Load `AGENTS.md` and `skills/control-repo-manager/SKILL.md`.
3. Run:

   ```bash
   node scripts/control-repo.mjs tracker-status
   ```

4. Report active projects, open/waiting workflow runs, phase skills, next
   actions, and live GitHub upload state.
5. Treat tracker output as authoritative over folder scans or stale docs.

## Arguments

$ARGUMENTS: optional focus text for the status summary.
