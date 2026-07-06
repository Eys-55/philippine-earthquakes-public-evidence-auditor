# Track workflow runs as session-scoped operations

Status: accepted

This repo will track Matt Pocock workflow work as explicit workflow runs attached to tracked work sessions. A run starts manually with a project, title, flow ID, owned paths, and validation commands; risky parallel work pauses for a project situation check and requires explicit user approval before proceeding.

Workflow runs can complete inside a session when their flow-specific end state is reached, validation passes, and required review is recorded. The tracked work session is the commit boundary: a session is complete only after its runs are resolved or handed off, tracker state is current, validation passes, and the session changes are committed. Upload verification is tracked separately as the synced-session boundary.

2026-07-06 update: Skills are the operator interface. Codex chat is the operator surface. The user never runs tracker scripts; scripts are internal adapters. The "manual" start above means the user states intent in chat and Codex performs the tracker persistence internally. It does not mean the user opens a terminal, runs Python, or operates tracker commands directly.

The internal adapter layer may use `scripts/control-repo.mjs` as the Node tracker adapter for session, workflow-run, status, validation, upload, and UI-export primitives. These are implementation details behind the skill surface, not operator instructions.

Considered options: automatic hooks were rejected because Codex cannot reliably fire a hook on every skill invocation; user-run commands are rejected as the operator interface because this workspace runs through Codex chat and skills; workflow-run-only commits were rejected because one session may contain several small runs; warning-only parallel work was rejected because overlapping owned paths, schemas, registry records, workflow instructions, validation gates, or external side effects can collide across sessions.
