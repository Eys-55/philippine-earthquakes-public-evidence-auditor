# Control Repo Tracker Design

Date: 2026-07-06
Status: approved for implementation planning

## Problem

This workspace is acting as a control repo: it can contain local workflows,
spawn or manage other repos, coordinate multiple Codex sessions, and preserve
the operating history across parallel projects. The current repo does not yet
have a single authoritative tracker for projects, repos, workstreams, sessions,
public updates, and GitHub upload state.

The failure mode is severe: folder names, stale docs, deleted lanes, or
foundation notes can be mistaken for active projects. That makes status answers
untrustworthy and lets untracked work sit locally without a durable GitHub copy.

The tracker must make this repo answerable as an operations system, not just as
a code folder.

## Design Principles

1. Tracker authority beats folder guessing.
   Status must come from the registry and event log first. Folder scans are only
   audit evidence.

2. Every work session leaves durable state.
   A session is not done until the tracker is updated, changes are committed,
   uploaded to GitHub, and the upload state is verified.

3. The agent acts as project manager first.
   Before doing work, the agent identifies the project, repo, workstream, and
   session context. After work, it records what changed and what remains.

4. Logs must support messy parallel work.
   Multiple Codex sessions may work on different tasks for the same project, or
   on different projects at once. The tracker must represent both cleanly.

5. External action boundaries stay explicit.
   GitHub upload is required for repo durability, but publishing posts, changing
   third-party systems, or using paid services still requires explicit approval.

6. Use plain names.
   The system is called the control repo tracker or repo tracker. Do not rename
   it into a mascot or vague product name.

## Authoritative Data Model

### Projects

Stored at `ops/registry/projects.json`.

Each project record defines:

- `id`: stable slug.
- `title`: human-readable project name.
- `status`: `active`, `paused`, `exploring`, `archived`, or `deleted`.
- `owner_intent`: short statement of what the user actually wants.
- `current_goal`: the current target artifact or capability.
- `not_projects`: stale names or surfaces that must not be reported as active.
- `repos`: related repo ids.
- `workstreams`: active or historical workstream ids.
- `last_event_id`: latest event touching the project.
- `last_uploaded_commit`: latest known GitHub-uploaded commit.

Status answers must not invent projects from directories. If a folder exists
but has no active project record, report it as an orphan or stale surface.

### Repos

Stored at `ops/registry/repos.json`.

Each repo record defines:

- `id`: stable slug.
- `path`: absolute or workspace-relative local path.
- `github_remote`: expected GitHub remote URL.
- `default_branch`: expected upload branch.
- `role`: `control`, `generated`, `reference`, or `external`.
- `owning_project`: project id or `shared`.
- `upload_policy`: `required`, `manual`, or `never`.
- `last_clean_check`: timestamp and command evidence.

The current repo should be registered as the control repo. Generated repos must
be registered before serious work continues inside them.

### Workstreams

Stored at `ops/registry/workstreams.json`.

Each workstream record defines:

- `id`: stable slug.
- `project_id`: owning project.
- `repo_id`: owning repo.
- `status`: `active`, `blocked`, `paused`, `done`, or `archived`.
- `objective`: concrete current outcome.
- `session_ids`: related sessions.
- `handoff`: path to latest handoff note.
- `open_decisions`: short list of unresolved decisions.
- `next_action`: the next concrete action.

Workstreams are allowed to move backward. If building road B reveals road A is
wrong, the tracker records that as a new event and updates `next_action`; it
does not pretend work is linear.

### Sessions

Stored under `ops/sessions/YYYY-MM-DD/session-<id>.jsonl`.

Each session log is append-only JSONL. Event types include:

- `session_started`
- `user_turn`
- `assistant_action`
- `decision`
- `file_change`
- `validation`
- `commit_created`
- `github_uploaded`
- `handoff_written`
- `session_closed`

The session log should capture enough context to answer what happened in the
last 12 hours across projects without re-reading every diff.

### Events

Stored under `ops/events/YYYY-MM-DD.jsonl`.

The event log is the cross-session timeline. It contains concise events with:

- `event_id`
- `timestamp`
- `project_id`
- `repo_id`
- `workstream_id`
- `session_id`
- `actor`
- `summary`
- `evidence`
- `next_action`

This is the source for daily summaries, project status, and public progress
drafts.

### Daily Rollups

Stored under `ops/daily/YYYY-MM-DD.md`.

Daily rollups answer:

- What changed today?
- Which projects moved?
- Which repos were uploaded to GitHub?
- What is blocked?
- What is the next action per active workstream?
- What public progress is suitable for LinkedIn or another channel?

### Public Progress

Stored at `ops/public/linkedin-posts.jsonl`.

This is a local tracker for public posting intent. It records drafted, approved,
posted, skipped, and follow-up states. It must not publish anything by itself.

### GitHub Upload State

Stored at `ops/sync/github-upload-state.json`.

Each repo tracked with `upload_policy: required` records:

- local branch
- local HEAD
- remote branch
- remote HEAD
- clean or dirty status
- untracked file count
- last successful upload timestamp
- last verification command

The invariant is simple: required repos should not finish a session with local
changes that are not uploaded to GitHub.

## Command Surface

The first command set should stay small and sharp.

### `/project-status`

Reads the registry, event log, upload state, and handoffs. It prints only
tracked projects and explicitly separates stale or orphaned surfaces from active
projects.

### `/session-start`

Creates or resumes a session log, links it to a project, repo, and workstream,
and records the first user objective for the session.

### `/sync-now`

Runs the upload gate for the current repo or all required repos:

1. inspect status;
2. update tracker;
3. stage intended tracker/code/doc changes;
4. commit if needed;
5. upload to GitHub;
6. verify remote HEAD;
7. write upload state.

### `/session-handoff`

Writes a concise handoff from the current event and session logs, then runs the
upload gate.

### `/repo-register`

Registers a repo path and GitHub remote before serious work happens there.

### `/repo-audit`

Compares tracked registry state with actual files, remotes, branches, untracked
files, and stale project surfaces. It reports discrepancies instead of silently
renaming or deleting anything.

## Required Scripts

The implementation should provide local scripts first. Slash commands can be
thin compatibility wrappers later.

- `scripts/tracker_status.py`
- `scripts/tracker_session_start.py`
- `scripts/tracker_log_event.py`
- `scripts/tracker_daily_rollup.py`
- `scripts/tracker_upload_gate.py`
- `scripts/validate_tracker.py`

The validator should fail when:

- active project ids are duplicated;
- a workstream references a missing project or repo;
- a required repo lacks upload state;
- upload state reports local commits ahead of GitHub;
- a session references unknown ids;
- JSONL lines are invalid;
- deleted or archived projects appear in active status output.

## Minimum Viable Build

The first useful version should build these capabilities in order:

1. Create registry schemas and seed the current control repo.
2. Add append-only event and session logging.
3. Add status output that refuses to infer active projects from folders.
4. Add upload-state verification against GitHub remote HEAD.
5. Add daily rollup generation.
6. Add handoff generation.
7. Add repo audit checks for stale folders, untracked files, and orphaned
   surfaces.
8. Document the workflow as `skills/control-repo-manager/SKILL.md`.

## Operating Invariant

No session is complete until:

1. the tracker records what happened;
2. relevant files are tracked in git;
3. the commit exists locally;
4. the commit is uploaded to GitHub;
5. the remote HEAD verification is written to `ops/sync/github-upload-state.json`.

If any part fails, the session must end with an explicit blocked handoff that
names the failed command and the next action.

## Non-Goals For V1

- No automatic third-party publishing.
- No paid external actions.
- No hidden daemon requirement.
- No destructive deletion of stale project files without an explicit deletion
  plan.
- No attempt to replace GitHub, Codex, or the existing ECC workflow surface.
- No mascot or renamed product identity.

## Open Decisions

1. Whether slash commands should be real files under `commands/` or documented
   Codex command prompts first.
2. Whether generated repos should always be submodules, sibling repos, or plain
   registered paths.
3. Whether session logs should include full user message text or concise
   summaries by default.
4. Whether daily rollups should be generated automatically at session close or
   only on command.

