# 0004 - Adopt Project Lanes for Multi-Workflow Organization

Date: 2026-07-04

## Status

Accepted

## Context

The repo now contains more than one useful workflow direction. The active
workflow is the Philippines Building Code Evidence Auditor, while the earlier
Address Disaster Risk Assessor and Metro Manila Source Atlas remain useful
foundation lanes. The user also wants to start another project before its exact
title or repeated job is known.

Without a lane convention, Codex can accidentally mix building-code evidence,
earthquake or permit research, disaster-risk data, and unrelated future project
notes into the same files.

## Decision

Organize this repo as one workspace with multiple project lanes.

Each new lane uses one stable slug across:

- `skills/<project-slug>/SKILL.md`;
- `data/<project-slug>/`;
- `reports/<project-slug>-*.md`;
- `docs/plans/YYYY-MM-DD-<project-slug>-*.md`;
- `docs/status/YYYY-MM-DD-<project-slug>-*.md`;
- validation scripts when needed.

Existing lanes with documented historical data surfaces can keep those paths as
long as the README and status table make the mapping explicit. For example, the
Building Code Evidence Auditor currently uses `data/building-code-auditor/`.

The repo's `AGENTS.md` is the Codex-facing source of truth for how lanes are
selected. Codex should identify the lane before editing. If the lane is unclear,
Codex should ask one lane-selection question instead of guessing and mixing
artifacts.

## Current Lanes

- `philippines-building-code-evidence-auditor` - active.
- `address-disaster-risk-assessor` - paused/foundation.
- `metro-manila-source-atlas` - foundation.
- `untitled-project` - exploring placeholder.

## Consequences

The Building Code Evidence Auditor remains isolated from future project ideas.
The `untitled-project` lane is a temporary parking area only. It should be
renamed once the repeated real-world job, input contract, and output artifact are
clear.

Project knowledge belongs in repo docs first. Codex memory may mirror the
convention as a future-session reminder, but memory is not the authoritative
project state.
