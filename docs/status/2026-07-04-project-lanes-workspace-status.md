# Project Lanes Workspace Status

Date: 2026-07-04

## Purpose

This workspace can hold multiple ECC agent workflows at the same time without
mixing their instructions, data, reports, or safety boundaries.

## Lane Selection Rule

Before work starts, identify exactly one active lane:

- If the user names a building, establishment, permit, earthquake damage,
  occupancy, contractor, or compliance evidence task, use
  `philippines-building-code-evidence-auditor`.
- If the user names address-based hazard or disaster-risk screening, use
  `address-disaster-risk-assessor`.
- If the user asks to refresh or extend the Metro Manila source inventory, use
  `metro-manila-source-atlas`.
- If the user says the project is new, untitled, vague, or only exploratory, use
  `untitled-project` until it is renamed.

If a request could belong to more than one lane, ask one short question before
editing files.

## Current Lane Table

| Lane | Status | Canonical Skill | Data Surface | Resume Rule |
| --- | --- | --- | --- | --- |
| `philippines-building-code-evidence-auditor` | active | `skills/philippines-building-code-evidence-auditor/SKILL.md` | `data/building-code-auditor/` | Start with building identity confirmation. |
| `address-disaster-risk-assessor` | paused/foundation | `skills/address-disaster-risk-assessor/SKILL.md` | `data/disaster-risk/` | Resume from `docs/status/2026-07-03-project-pause-handoff.md`. |
| `metro-manila-source-atlas` | foundation | `skills/metro-manila-source-atlas/SKILL.md` | `data/`, `data/deep-dive/`, `data/agent-findings/` | Use only for source inventory refreshes. |
| `untitled-project` | exploring | `skills/untitled-project/SKILL.md` | `data/untitled-project/` | First lock the repeated job, input, and output. |

## Untitled Project Promotion Gate

Before `untitled-project` becomes a named lane, write:

- repeated real-world job;
- trigger and refusal scope;
- input contract;
- output artifact;
- agent lanes;
- raw evidence surface;
- validation loop;
- safety boundary.

Then rename the skill and data folder to the final slug and add a decision note.

## Codex Handling

Codex should treat the repo as one workspace with multiple lanes, not as one
large blended project. The repo docs are authoritative. Memory can remind future
sessions of the lane convention, but it should not replace status files,
decision records, or `SKILL.md` instructions.
