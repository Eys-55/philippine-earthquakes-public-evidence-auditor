# Control Repo Manager Internal Adapter Reference

This is an Internal Adapter Reference, not operator instructions. Do not tell the user to run these commands. Codex chat and skills are the user-facing
surface; these adapters exist only so Codex can persist and verify tracker
state internally.

## /project-status

Codex internal adapter: inspect tracker status with
`npm run tracker:status`.

## /session-start

Codex internal adapter: start or lock a session with
`node scripts/control-repo.mjs tracker-session-start ...`.

## /sync-now

Codex internal adapter: run validation, commit intended changes, upload to
GitHub, then verify with `npm run tracker:upload-gate`.

## /session-handoff

Codex internal adapter: write the handoff with
the Node control adapter, then perform the internal
sync flow.

## /repo-register

Codex internal adapter: add a repo to `ops/registry/repos.json`, then validate
with `npm run validate`.

## /repo-audit

Codex internal adapter: audit repo surfaces with
`npm run validate`.
