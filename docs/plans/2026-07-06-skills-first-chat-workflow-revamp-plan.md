# Skills-First Chat Workflow Revamp Plan

Date: 2026-07-06
Status: active implementation plan
Workflow run: `wfr-20260706-152225-e480`

## Loaded Context

- ECC instructions from root `AGENTS.md`.
- Everything Claude Code skill: `/Users/acecanacan/.agents/skills/everything-claude-code/SKILL.md`.
- Workflow authority files: `AGENTS.md`, `CONTEXT.md`, `README.md`, and `docs/adr/0001-track-workflow-runs-as-session-scoped-operations.md`.
- Canonical skills: `skills/agent-workflow-project-maker/SKILL.md` and `skills/control-repo-manager/SKILL.md`.
- Compatibility references: `skills/agent-workflow-project-maker/commands.md` and `skills/control-repo-manager/commands.md`.
- Repo scope check: 413 tracked workspace files visible through the local file list.

## Problem

The repo had the right intent, but it leaked the adapter layer into the user
experience. Workflow intake, tracker status, closeout, and validation were
documented as command flows, which made it look like the user had to open a
terminal and run Python to operate the workflow system.

That is wrong for this workspace.

## Non-Negotiable Contract

Contract phrase: Skills are the operator interface. Codex chat is the operator surface. The user never runs tracker scripts; scripts are internal adapters.

Required behavior:

- The user talks in Codex chat.
- Plain chat such as "I found a bug in my workflow", "I am building a workflow", "create a workflow", or "continue this workflow" triggers workflow intake.
- Codex loads ECC and the relevant skill files before grilling or implementation.
- Codex creates or locks tracker state internally.
- Codex writes context manifests internally.
- Codex reports the loaded-context proof, premise lock, first grilling question, status, and closeout in chat.
- Scripts may remain as hidden adapters for persistence and validation, but they are not the operator UX.

## Phase 0: Stop The Wrong Surface

Change live authority files so they explicitly reject user-run terminal workflow
operation.

Acceptance:

- `AGENTS.md` defines Codex chat plus skills as the user-facing workflow
  surface.
- `CONTEXT.md` replaces command vocabulary with skill actions, validation gates,
  and internal adapters.
- The ADR records the 2026-07-06 correction that "manual" means user intent in
  chat, not user-run commands.

## Phase 1: Make Skills Canonical In Practice

Update the canonical skills so they behave as the runtime contract, not just
docs.

Acceptance:

- `skills/agent-workflow-project-maker/SKILL.md` treats plain chat workflow
  intent as the trigger.
- `skills/control-repo-manager/SKILL.md` treats tracker checks as internal Codex
  adapter actions.
- Both skills forbid telling the user to run tracker scripts.

## Phase 2: Quarantine Compatibility Commands

Keep slash and command references only as internal adapter references for Codex
and cross-harness compatibility.

Acceptance:

- `skills/agent-workflow-project-maker/commands.md` is marked as an Internal
  Adapter Reference.
- `skills/control-repo-manager/commands.md` is marked as an Internal Adapter
  Reference.
- Both files say they are not operator instructions and that Codex must not tell
  the user to run them.

## Phase 3: Add Regression Tests

Add tests that fail if future edits erase the chat-first contract or re-promote
commands as the operator interface.

Acceptance:

- `tests/test_skills_first_chat_contract.py` verifies the four contract phrases
  in authoritative docs.
- The test verifies command docs are internal adapter references.
- The test verifies the workflow-maker skill triggers on the exact plain-chat
  workflow phrases.

## Phase 4: Future Hardening

After the live contract is fixed, expand validation so generated inventories,
dashboards, and future workflow docs cannot publish command-first UX as the
recommended user path.

Proposed gates:

- Add a validator that scans canonical files for "run this command" language
  unless the section is explicitly marked internal or maintainer-only.
- Add a chat-intent fixture that describes the expected Codex response for a
  blank-session workflow bug report.
- Add a workflow intake E2E fixture that proves the first visible response is
  ECC proof plus a context-aware grilling question, not implementation.

## Internal Verification

Codex should run these gates internally before closeout:

```bash
python3 -m unittest tests.test_skills_first_chat_contract
python3 -m unittest discover
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
git diff --check
```

The command block is an internal verification record for Codex maintainers. It
is not an instruction for the user to operate workflows through a terminal.
