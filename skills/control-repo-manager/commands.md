# Control Repo Manager Internal Adapter Reference

This is an Internal Adapter Reference, not operator instructions. Do not tell the user to run these commands. Codex chat and skills are the user-facing
surface; these adapters exist only so Codex can persist and verify tracker
state internally.

## /project-status

Codex internal adapter: inspect tracker status with
`python3 scripts/tracker_status.py`.

## /session-start

Codex internal adapter: start or lock a session with
`python3 scripts/tracker_session_start.py ...`.

## /sync-now

Codex internal adapter: run validation, commit intended changes, upload to
GitHub, then verify with `python3 scripts/tracker_upload_gate.py`.

## /session-handoff

Codex internal adapter: write the handoff with
`python3 scripts/tracker_session_handoff.py ...`, then perform the internal
sync flow.

## /repo-register

Codex internal adapter: add a repo to `ops/registry/repos.json`, then validate
with `python3 scripts/validate_tracker.py`.

## /repo-audit

Codex internal adapter: audit repo surfaces with
`python3 scripts/tracker_repo_audit.py`.
