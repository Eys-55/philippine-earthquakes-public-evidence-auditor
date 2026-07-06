# Track workflow runs as session-scoped operations

Status: accepted

This repo will track Matt Pocock workflow work as explicit workflow runs attached to tracked work sessions. A run starts manually with a project, title, flow ID, owned paths, and validation commands; risky parallel work pauses for a project situation check and requires explicit user approval before proceeding.

Workflow runs can complete inside a session when their flow-specific end state is reached, validation passes, and required review is recorded. The tracked work session is the commit boundary: a session is complete only after its runs are resolved or handed off, tracker state is current, validation passes, and the session changes are committed. Upload verification is tracked separately as the synced-session boundary.

The command surface will use `scripts/tracker_start_work.py` as the friendly session wrapper and `scripts/tracker_workflow_start.py`, `scripts/tracker_workflow_checkpoint.py`, `scripts/tracker_workflow_close.py`, and `scripts/tracker_project_situation.py` as the workflow-run primitives.

Considered options: automatic skill hooks were rejected because Codex cannot reliably fire a hook on every skill invocation; workflow-run-only commits were rejected because one session may contain several small runs; warning-only parallel work was rejected because overlapping owned paths, schemas, registry records, workflow instructions, validation gates, or external side effects can collide across sessions.
