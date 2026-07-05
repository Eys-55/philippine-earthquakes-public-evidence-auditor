# Control Repo Manager Commands

## /project-status

Run `python3 scripts/tracker_status.py`.

## /session-start

Run `python3 scripts/tracker_session_start.py ...`.

## /sync-now

Run validation, commit intended changes, upload to GitHub, then run
`python3 scripts/tracker_upload_gate.py`.

## /session-handoff

Run `python3 scripts/tracker_session_handoff.py ...`, then `/sync-now`.

## /repo-register

Add a repo to `ops/registry/repos.json`, then run
`python3 scripts/validate_tracker.py`.

## /repo-audit

Run `python3 scripts/tracker_repo_audit.py`.
