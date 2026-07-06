---
name: control-repo-manager
description: Use before answering project status or ending any session in this repo. Reads tracker truth from ops registries and event logs, distinguishes live upload verification from recorded sync evidence, and prevents stale folders or lane tables from being reported as active projects.
---

# Control Repo Manager

Use this skill before answering project status in this repo. Use it before
ending any session in this repo.

## Skills-First Chat Contract

Contract phrase: Skills are the operator interface. Codex chat is the operator surface. The user never runs tracker scripts; scripts are internal adapters.

Skills are the operator interface. Codex chat is the operator surface. The user
never runs tracker scripts; scripts are internal adapters that Codex may invoke
after this skill decides tracker state is required.

Do not tell the user to run tracker commands, open a terminal, or execute
Python. Codex performs tracker checks internally and reports the project status,
sync status, blockers, and next workflow action in chat.

## Source Of Truth

Project, repo, workstream, session, workflow-run, handoff, and sync status comes
from:

- `ops/registry/*.json`
- `ops/sessions/*.jsonl`
- `ops/workflow-runs/*.jsonl`

Folder scans, lane tables, README sections, AGENTS.md sections, and project
surface inventories are audit evidence only. They can help explain drift, stale
surfaces, or cleanup candidates, but they do not make a project active.

Deleted or stale surfaces must not be reported as active projects. If an old
folder or stale lane table disagrees with the tracker, say that it is stale
audit evidence and use tracker status as the active project answer.

## Internal Adapter Actions

Before answering project status, Codex internally checks tracker status:

```bash
npm run tracker:status
```

Before starting implementation work, Codex internally checks the project
situation for the target project and proposed owned paths:

```bash
node scripts/control-repo.mjs tracker-status
```

If the situation check reports risky parallel work, pause and ask the user
whether to continue, join the existing run, or wait.

Use these Workflow Run internal adapters for Matt Pocock workflow work:

```bash
node scripts/control-repo.mjs tracker-session-start ...
node scripts/control-repo.mjs tracker-workflow-start ...
node scripts/control-repo.mjs tracker-workflow-checkpoint ...
node scripts/control-repo.mjs tracker-workflow-close ...
```

When auditing stale project surfaces, Codex internally runs:

```bash
npm run validate
```

Before ending a session, Codex internally runs the tracker gates that match the
work performed:

```bash
npm test
npm run validate
npm run tracker:upload-gate
```

## Session Completion Rule

A session is not complete until all of these are true:

1. Tracker records are current.
2. Workflow runs are completed, handed off, blocked, or abandoned.
3. Intended changes are committed.
4. The commit has been uploaded to GitHub.
5. Upload verification has succeeded.

Do not treat a local clean tree or a recorded sync event as enough by itself.

## Upload Truth

`npm run tracker:status` may use live git state for upload truth.
Recorded `ops/sync` state is evidence, not self-certifying truth.

Use this distinction when reporting status:

- live upload gate/status result: current upload truth;
- recorded `ops/sync` entries: historical evidence that still needs live
  verification;
- local folders or stale docs: audit evidence only.

If `npm run tracker:upload-gate` reports local changes still need
upload, say the session is not uploaded yet and do not report upload completion.

## Workflow Currency

This repo uses the installed Matt Pocock skills as the tracker workflow
currency. Do not use Superpowers planning or execution skills as the default
process for tracker work. Workflow runs should record the Matt Pocock flow ID,
current skill, owned paths, validation commands, checkpoints, and closeout
state.
