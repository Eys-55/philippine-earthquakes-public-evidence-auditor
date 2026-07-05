---
name: control-repo-manager
description: Use before answering project status or ending any session in this repo. Reads tracker truth from ops registries and event logs, distinguishes live upload verification from recorded sync evidence, and prevents stale folders or lane tables from being reported as active projects.
---

# Control Repo Manager

Use this skill before answering project status in this repo. Use it before
ending any session in this repo.

## Source Of Truth

Project, repo, workstream, session, handoff, daily rollup, and sync status comes
from:

- `ops/registry/*.json`
- `ops/events/*.jsonl`

Folder scans, lane tables, README sections, AGENTS.md sections, and project
surface inventories are audit evidence only. They can help explain drift, stale
surfaces, or cleanup candidates, but they do not make a project active.

Deleted or stale surfaces must not be reported as active projects. If an old
folder or stale lane table disagrees with the tracker, say that it is stale
audit evidence and use tracker status as the active project answer.

## Required Commands

Before answering project status, run:

```bash
python3 scripts/tracker_status.py
```

When auditing stale project surfaces, run:

```bash
python3 scripts/tracker_repo_audit.py
```

Before ending a session, run the tracker gates that match the work performed:

```bash
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
python3 scripts/tracker_upload_gate.py
```

## Session Completion Rule

A session is not complete until all of these are true:

1. Tracker records are current.
2. Intended changes are committed.
3. The commit has been uploaded to GitHub.
4. Upload verification has succeeded.

Do not treat a local clean tree or a recorded sync event as enough by itself.

## Upload Truth

`python3 scripts/tracker_status.py` may use live git state for upload truth.
Recorded `ops/sync` state is evidence, not self-certifying truth.

Use this distinction when reporting status:

- live upload gate/status result: current upload truth;
- recorded `ops/sync` entries: historical evidence that still needs live
  verification;
- local folders or stale docs: audit evidence only.

If `python3 scripts/tracker_upload_gate.py` reports local changes still need
upload, say the session is not uploaded yet and do not report upload completion.
