# Python Surface Minimization Audit

Date: 2026-07-06
Workflow run: `wfr-20260706-152928-b37a`
Status: active reduction pass

## Objective

Reduce Python files to the minimum needed for this workspace while keeping
skills as the workflow surface. The user operates through Codex chat and skills,
not Python scripts.

## Result So Far

- Starting Python files: 41 total.
- Current Python files: 26 total.
- Removed Python files: 16.
- Added Python guard tests: 1.
- Net reduction: 15 Python files.
- Current script adapters: 18.
- Current Python test files: 8.

## Removed Files

These files were command-era or predecessor-surface Python and were removed:

- `scripts/tracker_workflow_intake_start.py`
- `scripts/workflow_skill_slash_surface.py`
- `scripts/workflow_catalog_cli_run.py`
- `scripts/workflow_catalog_remaining_cli_run.py`
- `scripts/workflow_catalog_tools.py`
- `scripts/tracker_start_work.py`
- `scripts/query_workflow_catalog.py`
- `scripts/query_workflow_router.py`
- `scripts/validate_building_identity_gate.py`
- `scripts/validate_audit_scope_gate.py`
- `scripts/validate_audit_scope_source_reality.py`
- `scripts/tracker_daily_rollup.py`
- `scripts/tracker_log_event.py`
- `scripts/build_workflow_door_catalog.py`
- `scripts/build_workflow_router.py`
- `scripts/build_workflow_search_index.py`

## Remaining Script Adapter Inventory

These remain because they currently preserve validation, build, tracker, or
active V2 evidence gates.

| File | Keep Reason |
| --- | --- |
| `scripts/export_tracker_ui_data.py` | Required by `npm run build` to generate the tracker UI snapshot. |
| `scripts/tracker_project_situation.py` | Internal parallel-work assessment adapter. |
| `scripts/tracker_repo_audit.py` | Internal stale-surface audit adapter. |
| `scripts/tracker_session_handoff.py` | Internal handoff adapter. |
| `scripts/tracker_session_start.py` | Internal session-start adapter. |
| `scripts/tracker_status.py` | Internal tracker status adapter and upload truth view. |
| `scripts/tracker_upload_gate.py` | Internal GitHub upload verification adapter. |
| `scripts/tracker_workflow_checkpoint.py` | Internal workflow-run checkpoint adapter. |
| `scripts/tracker_workflow_close.py` | Internal workflow-run closeout adapter. |
| `scripts/tracker_workflow_lib.py` | Shared tracker adapter library. |
| `scripts/tracker_workflow_start.py` | Internal workflow-run start adapter. |
| `scripts/validate_building_code_v2_earthquake_scope_gate.py` | Active V2 earthquake scope validator. |
| `scripts/validate_building_code_v2_evidence_packet.py` | Active V2 evidence-packet validator. |
| `scripts/validate_building_code_v2_identity_gate.py` | Active V2 identity validator. |
| `scripts/validate_building_code_v2_overclaim.py` | Active V2 overclaim validator. |
| `scripts/validate_progress_docs.py` | Progress-chart/table validator. |
| `scripts/validate_project_surface_inventory.py` | Project inventory validator. |
| `scripts/validate_tracker.py` | Tracker invariant validator. |

## Remaining Test Inventory

These remain because the repo still uses Python for the internal adapter test
suite:

- `tests/__init__.py`
- `tests/test_python_surface_minimum.py`
- `tests/test_skills_first_chat_contract.py`
- `tests/test_tracker_astro_monitor.py`
- `tests/test_tracker_runtime.py`
- `tests/test_validate_tracker.py`
- `tests/test_workflow_run_commands.py`
- `tests/test_workflow_skill_slash_surface.py`

## Current Rule

No new Python file should be added unless it is one of these:

- internal tracker adapter;
- internal validator for an active skill;
- internal build/export adapter required by the UI;
- test coverage for the above.

Workflow intake, slash routing, workflow catalog lookup, and user-facing
workflow operation must live in skills and committed data, not Python command
surfaces.
