from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_validate_tracker import seed_valid_tracker
from tests.test_validate_tracker import write_json


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name: str, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "TRACKER_ROOT": root.as_posix()}
    return subprocess.run(
        ["python3", (REPO_ROOT / "scripts" / script_name).as_posix(), *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def seed_tracker_with_session(root: Path) -> None:
    seed_valid_tracker(root)
    write_json(
        root / "ops/registry/workstreams.json",
        {
            "workstreams": [
                {
                    "id": "tracker-build",
                    "project_id": "agent-workflow-project-maker",
                    "repo_id": "control-repo",
                    "status": "active",
                    "objective": "Build the control repo tracker.",
                    "session_ids": ["session-1"],
                    "handoff": "ops/handoffs/latest.md",
                    "open_decisions": [],
                    "next_action": "Implement tracker scripts.",
                }
            ]
        },
    )


class WorkflowRunCommandTests(unittest.TestCase):
    def test_start_checkpoint_and_close_workflow_run(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_tracker_with_session(root)

            started = run_script(
                "tracker_workflow_start.py",
                root,
                "--project-id",
                "agent-workflow-project-maker",
                "--session-id",
                "session-1",
                "--title",
                "Implement workflow run commands",
                "--flow-id",
                "tracker_ops",
                "--current-skill",
                "implement",
                "--owned-path",
                "scripts/tracker_workflow_start.py",
                "--validation-command",
                "python3 scripts/validate_tracker.py",
                "--next-action",
                "Checkpoint the run.",
            )

            self.assertEqual("", started.stderr)
            self.assertEqual(0, started.returncode)
            workflow_run_id = started.stdout.strip()
            registry = read_json(root / "ops/registry/workflow-runs.json")
            runs = registry["workflow_runs"]
            self.assertIsInstance(runs, list)
            self.assertEqual(workflow_run_id, runs[0]["id"])
            self.assertEqual("open", runs[0]["status"])
            self.assertTrue((root / runs[0]["log_path"]).is_file())

            checkpointed = run_script(
                "tracker_workflow_checkpoint.py",
                root,
                "--workflow-run-id",
                workflow_run_id,
                "--summary",
                "Recorded command progress.",
                "--next-action",
                "Close the run.",
                "--artifact",
                "scripts/tracker_workflow_checkpoint.py",
            )

            self.assertEqual("", checkpointed.stderr)
            self.assertEqual(0, checkpointed.returncode)
            registry = read_json(root / "ops/registry/workflow-runs.json")
            self.assertEqual("Close the run.", registry["workflow_runs"][0]["next_action"])
            self.assertEqual(
                ["scripts/tracker_workflow_checkpoint.py"],
                registry["workflow_runs"][0]["artifacts"],
            )

            closed = run_script(
                "tracker_workflow_close.py",
                root,
                "--workflow-run-id",
                workflow_run_id,
                "--status",
                "completed",
                "--summary",
                "Implemented command slice.",
                "--next-action",
                "Move to status board work.",
                "--artifact",
                "scripts/tracker_workflow_start.py",
                "--validation-result",
                "python3 scripts/validate_tracker.py: passed",
                "--review-state",
                "not-required-for-test",
            )

            self.assertEqual("", closed.stderr)
            self.assertEqual(0, closed.returncode)
            registry = read_json(root / "ops/registry/workflow-runs.json")
            self.assertEqual("completed", registry["workflow_runs"][0]["status"])
            self.assertEqual(
                "Implemented command slice.",
                registry["workflow_runs"][0]["final_summary"],
            )

    def test_workflow_start_refuses_missing_owned_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_tracker_with_session(root)

            result = run_script(
                "tracker_workflow_start.py",
                root,
                "--project-id",
                "agent-workflow-project-maker",
                "--session-id",
                "session-1",
                "--title",
                "Broken start",
                "--flow-id",
                "tracker_ops",
                "--current-skill",
                "implement",
                "--validation-command",
                "python3 scripts/validate_tracker.py",
                "--next-action",
                "Should fail.",
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("--owned-path", result.stderr)

    def test_project_situation_reports_risky_parallel_work(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_tracker_with_session(root)
            started = run_script(
                "tracker_workflow_start.py",
                root,
                "--project-id",
                "agent-workflow-project-maker",
                "--session-id",
                "session-1",
                "--title",
                "Existing run",
                "--flow-id",
                "tracker_ops",
                "--current-skill",
                "implement",
                "--owned-path",
                "scripts/",
                "--validation-command",
                "python3 scripts/validate_tracker.py",
                "--next-action",
                "Keep working.",
            )
            self.assertEqual(0, started.returncode)

            situation = run_script(
                "tracker_project_situation.py",
                root,
                "--project-id",
                "agent-workflow-project-maker",
                "--owned-path",
                "scripts/tracker_workflow_start.py",
            )

            self.assertEqual(2, situation.returncode)
            self.assertIn("Result: risky", situation.stdout)
            self.assertIn("User approval: required", situation.stdout)

    def test_workflow_intake_is_not_a_python_command_surface(self) -> None:
        self.assertFalse((REPO_ROOT / "scripts/tracker_workflow_intake_start.py").exists())
        self.assertFalse((REPO_ROOT / "scripts/workflow_skill_slash_surface.py").exists())

        skill = (REPO_ROOT / "skills/agent-workflow-project-maker/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Plain chat is the primary trigger", skill)
        self.assertIn("create or lock the tracker run internally", skill)
        self.assertIn("first context-aware grilling question", skill)


if __name__ == "__main__":
    unittest.main()
