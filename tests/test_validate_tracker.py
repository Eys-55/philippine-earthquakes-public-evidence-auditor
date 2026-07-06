from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_tracker import validate_tracker_root


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def seed_valid_tracker(root: Path) -> None:
    write_json(
        root / "ops/registry/projects.json",
        {
            "projects": [
                {
                    "id": "agent-workflow-project-maker",
                    "title": "Agent Workflow Project Maker",
                    "status": "active",
                    "owner_intent": "Create reusable ECC workflow project packs.",
                    "current_goal": "Track workflow creation work.",
                    "repos": ["control-repo"],
                    "workstreams": ["tracker-build"],
                    "not_projects": [],
                    "last_event_id": None,
                    "last_uploaded_commit": None,
                }
            ],
            "non_projects": [
                {
                    "id": "metro-manila-source-atlas",
                    "reason": "Stale foundation surface; do not report as active.",
                }
            ],
        },
    )
    write_json(
        root / "ops/registry/repos.json",
        {
            "repos": [
                {
                    "id": "control-repo",
                    "path": ".",
                    "github_remote": "https://github.com/example/repo.git",
                    "default_branch": "main",
                    "role": "control",
                    "owning_project": "shared",
                    "upload_policy": "required",
                    "last_clean_check": None,
                }
            ]
        },
    )
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
                    "session_ids": [],
                    "handoff": "ops/handoffs/latest.md",
                    "open_decisions": [],
                    "next_action": "Implement tracker scripts.",
                }
            ]
        },
    )
    write_json(
        root / "ops/registry/workflow-runs.json",
        {
            "schema_version": 1,
            "generated_at": "2026-07-06T00:00:00Z",
            "workflow_runs": [],
        },
    )
    write_json(
        root / "ops/sync/github-upload-state.json",
        {
            "repos": {
                "control-repo": {
                    "local_branch": "main",
                    "local_head": "abc123",
                    "remote_branch": "main",
                    "remote_head": "abc123",
                    "status": "clean",
                    "untracked_file_count": 0,
                    "last_successful_upload": "2026-07-06T00:00:00Z",
                    "last_verification_command": "git ls-remote origin refs/heads/main",
                }
            }
        },
    )
    (root / "ops/events").mkdir(parents=True)
    (root / "ops/sessions").mkdir(parents=True)
    (root / "ops/workflow-runs").mkdir(parents=True)


class ValidateTrackerTests(unittest.TestCase):
    def test_valid_tracker_seed_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)

            result = validate_tracker_root(root)

            self.assertTrue(result.ok)
            self.assertEqual([], result.errors)
            self.assertEqual([], result.warnings)

    def test_project_repo_and_workstream_references_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_json(
                root / "ops/registry/projects.json",
                {
                    "projects": [
                        {
                            "id": "broken-project",
                            "title": "Broken Project",
                            "status": "active",
                            "owner_intent": "Exercise bad references.",
                            "current_goal": "Fail validation.",
                            "repos": ["missing-repo"],
                            "workstreams": ["missing-workstream"],
                            "not_projects": [],
                            "last_event_id": None,
                            "last_uploaded_commit": None,
                        }
                    ],
                    "non_projects": [],
                },
            )
            write_json(
                root / "ops/registry/repos.json",
                {
                    "repos": [
                        {
                            "id": "control-repo",
                            "path": ".",
                            "github_remote": "https://github.com/example/repo.git",
                            "default_branch": "main",
                            "role": "control",
                            "owning_project": "missing-owner",
                            "upload_policy": "optional",
                            "last_clean_check": None,
                        }
                    ]
                },
            )
            write_json(
                root / "ops/registry/workstreams.json",
                {
                    "workstreams": [
                        {
                            "id": "bad-workstream",
                            "project_id": "missing-project",
                            "repo_id": "missing-repo",
                            "status": "active",
                            "objective": "Broken reference.",
                            "session_ids": [],
                            "handoff": "ops/handoffs/latest.md",
                            "open_decisions": [],
                            "next_action": "Fix registry.",
                        }
                    ]
                },
            )

            result = validate_tracker_root(root)

            self.assertIn("broken-project: unknown repo missing-repo", result.errors)
            self.assertIn(
                "broken-project: unknown workstream missing-workstream", result.errors
            )
            self.assertIn("control-repo: unknown owning_project missing-owner", result.errors)
            self.assertIn("bad-workstream: unknown project_id missing-project", result.errors)
            self.assertIn("bad-workstream: unknown repo_id missing-repo", result.errors)
            self.assertFalse(result.ok)

    def test_workstream_project_and_repo_ids_must_be_strings(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_json(
                root / "ops/registry/workstreams.json",
                {
                    "workstreams": [
                        {
                            "id": "bad-project-ref",
                            "project_id": ["agent-workflow-project-maker"],
                            "repo_id": "control-repo",
                            "status": "active",
                            "objective": "Broken project reference type.",
                            "session_ids": [],
                            "handoff": "ops/handoffs/latest.md",
                            "open_decisions": [],
                            "next_action": "Fix registry.",
                        },
                        {
                            "id": "bad-repo-ref",
                            "project_id": "agent-workflow-project-maker",
                            "repo_id": {"id": "control-repo"},
                            "status": "active",
                            "objective": "Broken repo reference type.",
                            "session_ids": [],
                            "handoff": "ops/handoffs/latest.md",
                            "open_decisions": [],
                            "next_action": "Fix registry.",
                        },
                    ]
                },
            )

            result = validate_tracker_root(root)

            self.assertIn(
                "bad-project-ref: project_id must be a non-empty string",
                result.errors,
            )
            self.assertIn(
                "bad-repo-ref: repo_id must be a non-empty string",
                result.errors,
            )

    def test_missing_required_registry_arrays_fail(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_json(root / "ops/registry/projects.json", {"non_projects": []})
            write_json(root / "ops/registry/repos.json", {"schema_version": 1})
            write_json(root / "ops/registry/workstreams.json", {"schema_version": 1})
            write_json(root / "ops/registry/workflow-runs.json", {"schema_version": 1})

            result = validate_tracker_root(root)

            self.assertIn(
                "ops/registry/projects.json: missing required projects array",
                result.errors,
            )
            self.assertIn(
                "ops/registry/repos.json: missing required repos array",
                result.errors,
            )
            self.assertIn(
                "ops/registry/workstreams.json: missing required workstreams array",
                result.errors,
            )
            self.assertIn(
                "ops/registry/workflow-runs.json: missing required workflow_runs array",
                result.errors,
            )

    def test_valid_workflow_run_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
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
            write_text(
                root / "ops/workflow-runs/2026-07-06/wfr-1.jsonl",
                '{"event_type": "workflow_started", "workflow_run_id": "wfr-1"}\n',
            )
            write_json(
                root / "ops/registry/workflow-runs.json",
                {
                    "schema_version": 1,
                    "generated_at": "2026-07-06T00:00:00Z",
                    "workflow_runs": [
                        {
                            "id": "wfr-1",
                            "project_id": "agent-workflow-project-maker",
                            "session_id": "session-1",
                            "title": "Add Workflow Run registry validation",
                            "flow_id": "tracker_ops",
                            "status": "open",
                            "current_skill": "implement",
                            "owned_paths": ["ops/registry/workflow-runs.json"],
                            "validation_commands": ["python3 scripts/validate_tracker.py"],
                            "started_at": "2026-07-06T00:00:00Z",
                            "last_checkpoint_at": "2026-07-06T00:00:00Z",
                            "next_action": "Implement validation.",
                            "log_path": "ops/workflow-runs/2026-07-06/wfr-1.jsonl",
                        }
                    ],
                },
            )

            result = validate_tracker_root(root)

            self.assertTrue(result.ok)
            self.assertEqual([], result.errors)

    def test_workflow_run_required_fields_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_json(
                root / "ops/registry/workflow-runs.json",
                {
                    "schema_version": 1,
                    "generated_at": "2026-07-06T00:00:00Z",
                    "workflow_runs": [
                        {
                            "id": "wfr-bad",
                            "project_id": "missing-project",
                            "session_id": "missing-session",
                            "title": "Broken workflow run",
                            "flow_id": "",
                            "status": "unknown",
                            "current_skill": "implement",
                            "owned_paths": [],
                            "validation_commands": [],
                            "started_at": "2026-07-06T00:00:00Z",
                            "last_checkpoint_at": "2026-07-06T00:00:00Z",
                            "next_action": "Fix it.",
                            "log_path": "ops/workflow-runs/2026-07-06/missing.jsonl",
                        }
                    ],
                },
            )

            result = validate_tracker_root(root)

            self.assertIn("wfr-bad: unknown project_id missing-project", result.errors)
            self.assertIn("wfr-bad: unknown session_id missing-session", result.errors)
            self.assertIn("wfr-bad: flow_id must be a non-empty string", result.errors)
            self.assertIn("wfr-bad: invalid status unknown", result.errors)
            self.assertIn("wfr-bad: owned_paths must contain at least one entry", result.errors)
            self.assertIn(
                "wfr-bad: validation_commands must contain at least one entry",
                result.errors,
            )
            self.assertIn(
                "wfr-bad: log_path does not exist: ops/workflow-runs/2026-07-06/missing.jsonl",
                result.errors,
            )

    def test_workflow_run_logs_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_text(root / "ops/workflow-runs/2026-07-06/bad.jsonl", "not-json\n")

            result = validate_tracker_root(root)

            self.assertIn(
                "ops/workflow-runs/2026-07-06/bad.jsonl:1: invalid JSONL",
                result.errors,
            )

    def test_required_upload_state_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_json(root / "ops/sync/github-upload-state.json", {"repos": {}})

            result = validate_tracker_root(root)

            self.assertIn("control-repo: required repo missing upload state", result.errors)

    def test_pending_upload_state_allows_local_remote_head_mismatch(self) -> None:
        allowed_statuses = (
            "pending_upload",
            "ahead_of_remote",
            "remote_missing",
            "pending_local_changes",
        )

        for upload_status in allowed_statuses:
            with self.subTest(upload_status=upload_status):
                with tempfile.TemporaryDirectory() as raw_tmp:
                    root = Path(raw_tmp)
                    seed_valid_tracker(root)
                    write_json(
                        root / "ops/sync/github-upload-state.json",
                        {
                            "repos": {
                                "control-repo": {
                                    "local_branch": "main",
                                    "local_head": "abc123",
                                    "remote_branch": "main",
                                    "remote_head": (
                                        "" if upload_status == "remote_missing" else "def456"
                                    ),
                                    "status": upload_status,
                                    "untracked_file_count": 0,
                                    "last_successful_upload": None,
                                    "last_verification_command": (
                                        "git ls-remote origin refs/heads/main"
                                    ),
                                }
                            }
                        },
                    )

                    result = validate_tracker_root(root)

                    self.assertNotIn(
                        "control-repo: local_head differs from remote_head",
                        result.errors,
                    )
                    self.assertTrue(result.ok)

    def test_uploaded_state_rejects_local_remote_head_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_json(
                root / "ops/sync/github-upload-state.json",
                {
                    "repos": {
                        "control-repo": {
                            "local_branch": "main",
                            "local_head": "abc123",
                            "remote_branch": "main",
                            "remote_head": "def456",
                            "status": "uploaded",
                            "untracked_file_count": 0,
                            "last_successful_upload": None,
                            "last_verification_command": "git ls-remote origin refs/heads/main",
                        }
                    }
                },
            )

            result = validate_tracker_root(root)

            self.assertIn("control-repo: local_head differs from remote_head", result.errors)

    def test_json_and_jsonl_logs_under_events_and_sessions_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            seed_valid_tracker(root)
            write_text(root / "ops/events/good.jsonl", '{"event_id": "evt-1"}\n')
            write_text(root / "ops/events/bad.jsonl", '{"event_id": "evt-2"}\nnot-json\n')
            write_text(root / "ops/sessions/good.json", '{"session_id": "ses-1"}\n')
            write_text(root / "ops/sessions/bad.json", '{"session_id": ')

            result = validate_tracker_root(root)

            self.assertIn("ops/events/bad.jsonl:2: invalid JSONL", result.errors)
            self.assertIn("ops/sessions/bad.json: invalid JSON", result.errors)
            self.assertNotIn("ops/events/good.jsonl: invalid JSONL", result.errors)
            self.assertNotIn("ops/sessions/good.json: invalid JSON", result.errors)


if __name__ == "__main__":
    unittest.main()
