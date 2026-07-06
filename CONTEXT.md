# Market Research Agent Control Repo

This context defines the operating language for the control repo tracker and
workflow project surfaces in this workspace.

## Language

**Workflow Run**:
A tracked lifecycle instance that begins when an agent workflow skill is invoked and remains open until it is completed, abandoned, or explicitly handed off.
_Avoid_: Plan, issue, session

**Stale Workflow Run**:
A workflow run that remains open after its checkpoint deadline without a completion, handoff, blocker, or explicit abandon decision.
_Avoid_: Forgotten task, failed run

**Checkpoint**:
A durable tracker event that updates a workflow run's phase, artifact path, decision, blocker, waiting state, next action, completion, handoff, or abandon status.
_Avoid_: Chat update, progress vibe

**Workflow Run Status**:
The stored lifecycle state of a workflow run: open, waiting_on_user, blocked, completed, handed_off, or abandoned. Stale is derived from checkpoint age rather than stored as the primary status.
_Avoid_: Progress label, task state

**Manual Workflow Start**:
A workflow run begins only when the user or agent explicitly declares that feature, fix, research, or workflow work is being started for a project.
_Avoid_: Automatic skill hook, invisible start

**Tracked Work Session**:
A tracker session begins when the user starts work and names the project they are working on; workflow runs and checkpoints then attach to that session as work unfolds.
_Avoid_: Chat transcript, context window

**Concurrent Workflow Runs**:
Multiple workflow runs may be active for the same project across one or more tracked work sessions. The tracker must show both the current run in a session and other active runs that may affect the same project.
_Avoid_: One session one run, one project one task

**Project Situation Check**:
A required tracker review before building that shows the project's active sessions, open workflow runs, recent checkpoints, stale runs, blockers, and risky parallel work.
_Avoid_: Quick status, folder scan

**Parallel Work Assessment**:
The decision step in a project situation check that determines whether a new workflow run can safely proceed alongside existing active runs, should join an existing run, or should wait.
_Avoid_: Collision warning, merge guess

**Parallel Risk**:
Parallel workflow runs are risky when they touch the same owned paths, registry records, schemas, data contracts, workflow instructions, validation gates, or external side effects.
_Avoid_: Merge conflict only, vague overlap

**Workflow Run Registry**:
The current-state JSON surface that lists workflow runs and their active status, current skill, owned paths, last checkpoint, and next action for status reporting.
_Avoid_: Run log, audit trail

**Workflow Run Log**:
The append-only JSONL history for a workflow run, recording starts, checkpoints, parallel assessments, handoffs, completions, blockers, and abandon decisions.
_Avoid_: Current status file, mutable notes

**Owned Paths**:
The files, directories, registry records, schemas, or other repo surfaces a workflow run expects to read or change. Owned paths are required at workflow start and may be refined by later checkpoints.
_Avoid_: Scope notes, files probably touched

**Owned Path Refusal**:
The tracker must refuse to start a workflow run without at least one declared owned path.
_Avoid_: Unknown scope, unspecified files

**Validation Command**:
A command declared at workflow start that can verify the run's intended change or artifact. At least one validation command is required before a workflow run may start.
_Avoid_: Check later, manual confidence

**Workflow Completion**:
A workflow run is complete only after its flow-specific final stage is reached, required validation passes, review is recorded when the flow calls for it, and the work is committed.
_Avoid_: Code written, locally done
