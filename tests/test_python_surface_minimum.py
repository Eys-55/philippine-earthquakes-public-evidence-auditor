from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REMOVED_COMMAND_SURFACES = {
    "scripts/tracker_workflow_intake_start.py",
    "scripts/workflow_skill_slash_surface.py",
    "scripts/workflow_catalog_cli_run.py",
    "scripts/workflow_catalog_remaining_cli_run.py",
    "scripts/workflow_catalog_tools.py",
    "scripts/tracker_start_work.py",
    "scripts/query_workflow_catalog.py",
    "scripts/query_workflow_router.py",
    "scripts/validate_building_identity_gate.py",
    "scripts/validate_audit_scope_gate.py",
    "scripts/validate_audit_scope_source_reality.py",
    "scripts/tracker_daily_rollup.py",
    "scripts/tracker_log_event.py",
    "scripts/build_workflow_door_catalog.py",
    "scripts/build_workflow_router.py",
    "scripts/build_workflow_search_index.py",
}


class PythonSurfaceMinimumTests(unittest.TestCase):
    def test_removed_command_surfaces_do_not_return(self) -> None:
        for relative_path in sorted(REMOVED_COMMAND_SURFACES):
            with self.subTest(path=relative_path):
                self.assertFalse((REPO_ROOT / relative_path).exists())

    def test_python_script_count_stays_within_current_adapter_budget(self) -> None:
        scripts = sorted((REPO_ROOT / "scripts").glob("*.py"))

        self.assertLessEqual(len(scripts), 18)

    def test_workflow_lookup_is_skill_and_data_first(self) -> None:
        skill = (REPO_ROOT / "skills/agent-workflow-project-maker/SKILL.md").read_text(
            encoding="utf-8"
        )
        catalog_readme = (REPO_ROOT / "data/agentic-repos/README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("reading the committed JSON indexes directly", skill)
        self.assertIn("Codex should read the committed JSON indexes directly", catalog_readme)


if __name__ == "__main__":
    unittest.main()
