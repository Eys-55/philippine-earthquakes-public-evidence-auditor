# Project Surface Audit

Date: 2026-07-06

## Result

The repo's project surface is inconsistent. Old lane/foundation docs made stale
or deleted work look like current projects, while the workflow-catalog/project
maker work exists on disk without a proper skill entry.

Do not use the old "Active Lanes" tables as authoritative until cleanup is done.
Use `data/project-surface-inventory.json` plus the current user correction as
the working inventory.

## Current Project Candidates

The user stated the current project count should be two. This audit treats the
following as the likely current projects, pending final user confirmation of the
names:

| Project | Classification | Evidence | Action |
| --- | --- | --- | --- |
| `philippines-building-code-evidence-auditor-v2` | active current | Has skill, data, fixtures, validators, status lock, and README current-auditor language. | Keep as current project. |
| `agent-workflow-project-maker` | active current, newly surfaced | User expected it; repo has `data/agentic-repos/`, workflow reports, query scripts, build scripts, and catalog indexes. | Promote via new skill and inventory entry. |

## Hidden Current Work

The workflow/project-maker surface was hidden from the project list:

- `data/agentic-repos/` has 197 files on disk, with most of the workflow-catalog
  series currently untracked.
- `reports/workflow-*.md` documents workflow search, router, catalog, and
  comparison outputs.
- `scripts/*workflow*` contains query/build/run tools for the catalog.
- Before this audit, there was no `skills/agent-workflow-project-maker/` skill.

This is the strongest candidate for the missing project.

## Stale Or Made-Up Surfaces

These surfaces should not be counted as current projects:

| Surface | Classification | Why It Is Suspect | Representative Paths |
| --- | --- | --- | --- |
| `address-disaster-risk-assessor` | obsolete/deleted candidate | User stated it is deleted, but it remains tracked as a full skill/data/report series. | `skills/address-disaster-risk-assessor/`, `data/disaster-risk/`, `docs/decisions/0002-lock-address-disaster-risk-assessor.md` |
| `metro-manila-source-atlas` | obsolete/deleted candidate | User rejected it as a project/foundation; it remains tracked as a skill/data/report series. | `skills/metro-manila-source-atlas/`, `data/metro-manila-source-atlas.json`, `data/agent-findings/`, `data/deep-dive/` |
| `untitled-project` | placeholder delete candidate | Placeholder lane without a real repeated job; user rejected it. | `skills/untitled-project/`, `data/untitled-project/` |
| `foundation` lane model | stale policy delete candidate | This vocabulary created false project listings. | `README.md`, `AGENTS.md`, `docs/decisions/0004-adopt-project-lanes.md`, `docs/status/2026-07-04-project-lanes-workspace-status.md` |

## Duplicate Or Predecessor Surface

`philippines-building-code-evidence-auditor` V1 remains tracked with its own
skill, data, reports, and validators. It appears to be a predecessor or
maintainer copy of the V2 auditor, not a separate current project unless the
user confirms it should count.

Representative paths:

- `skills/philippines-building-code-evidence-auditor/`
- `data/building-code-auditor/`
- `scripts/validate_building_identity_gate.py`
- `scripts/validate_audit_scope_gate.py`
- `docs/status/2026-07-04-building-code-evidence-auditor-lock.md`

## Generated Or Review-Needed Output

The workflow catalog run directories are large generated artifacts. They are
useful for reproducibility, but they should not become separate projects:

- `data/agentic-repos/workflow-catalog-runs/`
- `data/agentic-repos/workflow-catalog-cli/`
- `data/agentic-repos/workflow-catalog-internal/`

The V2 building-code audit-run files are untracked and probably related to the
current auditor, but they need validator review before staging:

- `data/philippines-building-code-evidence-auditor-v2/audit-run-schema.json`
- `data/philippines-building-code-evidence-auditor-v2/audit-run-fixtures/`

## Tracking Added

This audit added the following surfaces:

- `data/project-surface-inventory.json` - machine-readable project inventory.
- `scripts/validate_project_surface_inventory.py` - validates active project
  count, active project skill paths, owned paths, and known stale surfaces.
- `skills/project-surface-auditor/SKILL.md` - tells future Codex runs how to
  audit project ownership before answering project-list questions.
- `skills/agent-workflow-project-maker/SKILL.md` - promotes the hidden workflow
  project-maker surface into a first-class skill.

## Cleanup Batches

Do not delete anything until the user confirms the exact batch.

Recommended batches:

1. Promote the project list: update README and AGENTS.md to show only confirmed
   current projects and point to `data/project-surface-inventory.json`.
2. Remove placeholder lane: delete `skills/untitled-project/` and
   `data/untitled-project/`.
3. Remove deleted disaster-risk surface: delete or archive the
   `address-disaster-risk-assessor` skill, `data/disaster-risk/`, disaster
   docs, and disaster reports.
4. Remove rejected source-atlas surface: delete or archive
   `metro-manila-source-atlas`, `data/agent-findings/`, `data/deep-dive/`,
   metro atlas data, and metro reports.
5. Decide V1 building-code treatment: keep as history, archive it, or merge any
   useful validators into V2.
6. Decide workflow catalog artifact retention: keep full run logs or reduce to
   final indexes/reports plus source seeds.

## Verification

Run:

```bash
python3 -m json.tool data/project-surface-inventory.json >/tmp/project-surface-inventory.json
python3 scripts/validate_project_surface_inventory.py
git diff --check
```
