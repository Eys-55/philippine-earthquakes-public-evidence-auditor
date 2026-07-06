from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_export(root: Path, output: Path) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "TRACKER_ROOT": root.as_posix()}
    return subprocess.run(
        [
            "python3",
            (REPO_ROOT / "scripts/export_tracker_ui_data.py").as_posix(),
            "--output",
            output.as_posix(),
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def seed_tracker(root: Path) -> None:
    write_json(
        root / "ops/registry/projects.json",
        {
            "projects": [
                {
                    "id": "agent-workflow-project-maker",
                    "title": "Agent Workflow Project Maker",
                    "status": "active",
                    "owner_intent": "Create reusable ECC workflow project packs.",
                    "current_goal": "Monitor workflow creation work.",
                    "repos": ["control-repo"],
                    "workstreams": ["control-repo-tracker"],
                    "not_projects": [],
                    "last_event_id": "evt-test",
                    "last_uploaded_commit": None,
                }
            ],
            "non_projects": [
                {
                    "id": "untitled-project",
                    "reason": "Placeholder surface; do not report as active.",
                }
            ],
        },
    )
    write_json(
        root / "ops/registry/workstreams.json",
        {
            "workstreams": [
                {
                    "id": "control-repo-tracker",
                    "project_id": "agent-workflow-project-maker",
                    "repo_id": "control-repo",
                    "status": "active",
                    "objective": "Build tracker monitor UI.",
                    "session_ids": ["session-test"],
                    "handoff": "ops/handoffs/latest.md",
                    "open_decisions": ["Decide refresh cadence."],
                    "next_action": "Build the first Astro monitor.",
                }
            ]
        },
    )
    write_json(
        root / "ops/registry/workflow-runs.json",
        {
            "workflow_runs": [
                {
                    "id": "wfr-test",
                    "project_id": "agent-workflow-project-maker",
                    "session_id": "session-test",
                    "title": "Build monitor",
                    "flow_id": "agent_workflow_project_maker",
                    "status": "open",
                    "current_skill": "implement",
                    "owned_paths": ["tracker-ui"],
                    "validation_commands": ["npm run build"],
                    "started_at": "2026-07-06T14:52:20+08:00",
                    "last_checkpoint_at": "2026-07-06T14:52:20+08:00",
                    "next_action": "Render dashboard.",
                    "log_path": "ops/workflow-runs/2026-07-06/wfr-test.jsonl",
                    "artifacts": [],
                }
            ]
        },
    )
    write_json(
        root / "ops/sync/github-upload-state.json",
        {
            "repos": {
                "control-repo": {
                    "status": "uploaded",
                    "local_branch": "main",
                    "local_head": "abc123",
                    "remote_branch": "main",
                    "remote_head": "abc123",
                    "dirty": False,
                    "untracked_file_count": 0,
                    "last_verified_at": "2026-07-06T14:50:00+08:00",
                    "verification_command": "git rev-parse HEAD",
                }
            }
        },
    )


class TrackerAstroMonitorTests(unittest.TestCase):
    def test_export_command_writes_dashboard_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_tracker(root)
            output = root / "tracker-ui/src/data/tracker-dashboard.json"

            result = run_export(root, output)

            self.assertEqual("", result.stderr)
            self.assertEqual(0, result.returncode)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("tracker_astro_monitor_dashboard", payload["kind"])
            self.assertEqual(1, payload["summary"]["active_projects"])
            self.assertEqual(1, payload["summary"]["open_workflow_runs"])
            self.assertEqual("uploaded", payload["summary"]["upload_status"])
            self.assertEqual(
                "Build the first Astro monitor.",
                payload["projects"][0]["workstreams"][0]["next_action"],
            )
            self.assertEqual("wfr-test", payload["workflow_runs"][0]["id"])
            self.assertEqual("untitled-project", payload["non_projects"][0]["id"])

    def test_astro_route_uses_exported_dashboard_snapshot(self) -> None:
        page = (REPO_ROOT / "tracker-ui/src/pages/index.astro").read_text(encoding="utf-8")

        self.assertIn("../data/tracker-dashboard.json", page)
        self.assertIn("Workflow Runs", page)
        self.assertIn("Upload State", page)
        self.assertIn("No 3D", page)


if __name__ == "__main__":
    unittest.main()
