# PRD: Workflow Run Tracker

## Problem Statement

The control repo can track projects, workstreams, sessions, handoffs, and upload state, but it does not yet track the actual Matt Pocock workflow runs that happen inside a session. When a user starts building a feature, sharpening a design, running research, implementing a slice, or reviewing work, that activity can disappear into chat history unless the agent manually writes a summary later.

The missing capability is an operations-level view of what is being built right now, what workflow it is following, what paths it owns, what validation proves it, whether it has gone stale, and whether it is safe to run in parallel with other work on the same project.

## Solution

Add workflow-run tracking to the control repo. A tracked work session starts when the user names the project being worked on. Within that session, one or more workflow runs can be started manually. Each workflow run records its project, session, title, explicit flow ID, current skill or phase, owned paths, validation commands, status, last checkpoint, next action, and append-only event history.

Before implementation work begins, the agent runs a project situation check. The check reports active sessions, open workflow runs, stale workflow runs, waiting work, blockers, owned-path overlap, and risky parallel work. If risky parallel work exists, the agent pauses and asks the user whether to continue, join an existing run, or wait.

Workflow run completion is separate from session completion. A workflow run completes when its flow-specific final stage is reached, required validation passes, and review is recorded when the flow calls for it. A tracked work session completes only when its runs are completed, handed off, blocked, or abandoned; tracker state is current; validation passes; and the session changes are committed. Upload verification remains the synced-session boundary.

## User Stories

1. As the repo owner, I want to start a tracked work session by naming the project, so that the tracker knows what project is currently being worked on.
2. As the repo owner, I want to start a workflow run when a feature, fix, research task, review, or workflow-design effort begins, so that work is visible before it is completed.
3. As the repo owner, I want each workflow run to require an explicit flow ID, so that the tracker knows which workflow template the run is following.
4. As the repo owner, I want each workflow run to require owned paths, so that parallel work can be assessed before files, schemas, or tracker state collide.
5. As the repo owner, I want each workflow run to require validation commands, so that vague work cannot be marked as tracked without a verification path.
6. As the repo owner, I want a workflow run to refuse to start when owned paths are missing, so that unknown scope does not enter the tracker.
7. As the repo owner, I want a workflow run to refuse to start when validation commands are missing, so that untestable work does not enter the tracker.
8. As the repo owner, I want checkpoint events during a workflow run, so that progress, decisions, blockers, artifacts, and next actions are durable.
9. As the repo owner, I want casual chat to not reset stale timing, so that only real tracker checkpoints keep a run fresh.
10. As the repo owner, I want open workflow runs to become stale after a time threshold without checkpoint activity, so that forgotten work is surfaced.
11. As the repo owner, I want waiting-on-user work to be reported separately from stale work, so that a valid pause does not look like a failed run.
12. As the repo owner, I want blocked runs to record a named blocker, so that the next agent can see why the run stopped.
13. As the repo owner, I want abandoned runs to require an explicit abandon decision, so that unfinished work is not silently discarded.
14. As the repo owner, I want completed runs to record their final phase, validation results, review state when required, artifacts, and next action, so that completion is auditable.
15. As the repo owner, I want one session to contain multiple workflow runs, so that design, implementation, review, and handoff can all happen in one tracked session.
16. As the repo owner, I want multiple sessions to work on the same project, so that parallel development is possible.
17. As the repo owner, I want the tracker to surface other active work on the same project before a new run starts, so that agents do not build blindly.
18. As the repo owner, I want a parallel work assessment before implementation, so that overlapping owned paths, schemas, registry records, validation gates, workflow instructions, and external side effects are caught early.
19. As the repo owner, I want risky parallel work to pause and report by default, so that the user controls whether parallel work proceeds.
20. As the repo owner, I want explicit user approval to override a risky parallel assessment, so that intentional parallelism is recorded.
21. As the repo owner, I want current-state workflow-run reporting, so that status answers show what is active now.
22. As the repo owner, I want append-only workflow-run logs, so that the history of a run is not lost when current status changes.
23. As the repo owner, I want tracker status to include active sessions, open workflow runs, stale workflow runs, waiting work, blockers, and next actions, so that the repo behaves like an operations board.
24. As the repo owner, I want Matt Pocock workflow skills to be the tracker workflow currency, so that planning, PRD, issue slicing, implementation, review, and handoff use one coherent workflow model.
25. As the repo owner, I want Superpowers to stop being the default workflow currency for this tracker, so that the tracker does not mix incompatible planning systems.
26. As an agent, I want a friendly session-start command, so that starting tracked work does not require remembering low-level tracker fields.
27. As an agent, I want separate workflow-run commands for start, checkpoint, close, and situation checks, so that each operation is explicit and testable.
28. As an agent, I want tracker validation to reject malformed workflow-run state, so that broken registry or log records are caught before commit.
29. As an agent, I want session completion to require a commit, so that session work has a durable git boundary.
30. As an agent, I want synced-session state to remain separate from completion, so that local completion and remote upload verification are not confused.

## Implementation Decisions

- Workflow runs are the primary tracked unit below sessions. Projects and workstreams remain the higher-level organizing surfaces.
- A tracked work session can contain multiple workflow runs.
- Multiple sessions can contain active workflow runs for the same project.
- Workflow runs start manually. The tracker should not rely on automatic skill-invocation hooks.
- A workflow run cannot start without a project, session, title, flow ID, owned paths, and validation commands.
- Flow IDs are explicit. Initial supported templates should include idea-to-ship work, bugfix work, research work, review work, and tracker operations.
- Workflow-run status values are open, waiting on user, blocked, completed, handed off, and abandoned.
- Stale is derived from checkpoint age, not stored as the primary status.
- Open runs become stale after 24 hours without a checkpoint and very stale after 7 days.
- Waiting-on-user work is reported separately from stale work.
- A checkpoint is a durable tracker event that updates phase, artifact path, decision, blocker, waiting state, next action, completion, handoff, or abandon status.
- A project situation check is required before implementation work.
- Parallel work is risky when it overlaps owned paths, registry records, schemas, data contracts, workflow instructions, validation gates, or external side effects.
- Risky parallel work pauses and reports by default. The user may explicitly approve proceeding.
- Workflow run completion is not the commit boundary. Session completion is the commit boundary.
- Upload verification remains the synced-session boundary, separate from local session completion.

## Testing Decisions

- Tests should verify behavior through tracker commands and validation/reporting seams rather than internal helper functions.
- The tracker validation seam should reject malformed workflow-run registries, invalid statuses, missing flow IDs, missing owned paths, missing validation commands, unknown project IDs, unknown session IDs, and invalid log JSONL.
- The workflow command seam should verify start, checkpoint, close, and situation-check behavior using temporary repo fixtures.
- The status/reporting seam should verify that active runs, stale runs, waiting work, blockers, parallel risk, and next actions appear in status output.
- The git/upload seam should preserve the existing distinction between committed session completion and synced-session upload verification.
- Tests should cover refusal cases first: missing owned paths, missing validation commands, missing flow ID, and risky parallel work without approval.

## Out of Scope

- Automatic hooks that fire whenever a Matt Pocock skill is invoked.
- Replacing the existing project, repo, workstream, session, handoff, or upload tracker.
- Public multi-user permissions or role-based access control.
- GitHub issue publishing automation beyond the existing Matt Pocock issue-tracker setup.
- Deleting stale project surfaces.
- Changing the Philippines Building Code Evidence Auditor V2 workflow behavior.
- Using Superpowers as the default tracker workflow currency.

## Further Notes

The source design language lives in the root domain glossary and the accepted workflow-run ADR. The implementation should preserve the existing tracker style: Python standard-library scripts, JSON/JSONL storage, append-only event history, atomic writes where needed, and validation gates before commit.

The first implementation slice should add workflow-run registry validation and a seed file. The next slices should add workflow-run start, checkpoint, close, project situation reporting, and status integration.
