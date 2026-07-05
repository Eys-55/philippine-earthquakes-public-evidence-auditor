from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import tracker_repo_audit
from scripts import tracker_status
from scripts import tracker_upload_gate
from tests.test_validate_tracker import write_json


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{' '.join(command)} failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout.strip()


def seed_gate_repo(root: Path, *, expected_remote: str) -> None:
    write_json(
        root / "ops/registry/repos.json",
        {
            "repos": [
                {
                    "id": "control-repo",
                    "path": ".",
                    "github_remote": expected_remote,
                    "default_branch": "main",
                    "role": "control",
                    "owning_project": "shared",
                    "upload_policy": "required",
                    "last_clean_check": None,
                }
            ]
        },
    )
    write_json(root / "ops/sync/github-upload-state.json", {"schema_version": 1, "repos": {}})


def init_uploaded_repo(root: Path, remote: Path) -> None:
    run(["git", "init", "--initial-branch=main"], root)
    run(["git", "config", "user.email", "tracker-test@example.com"], root)
    run(["git", "config", "user.name", "Tracker Test"], root)
    run(["git", "init", "--bare", str(remote)], root)
    run(["git", "remote", "add", "origin", str(remote)], root)
    run(["git", "add", "."], root)
    run(["git", "commit", "-m", "seed"], root)
    run(["git", "push", "-u", "origin", "main"], root)


class TrackerRuntimeTests(unittest.TestCase):
    def test_upload_gate_rejects_wrong_origin_even_when_heads_match(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            base = Path(raw_tmp)
            root = base / "repo"
            remote = base / "wrong-remote.git"
            root.mkdir()
            seed_gate_repo(root, expected_remote="https://github.com/example/expected.git")
            init_uploaded_repo(root, remote)

            with (
                mock.patch.object(tracker_upload_gate, "ROOT", root),
                mock.patch.object(
                    tracker_upload_gate,
                    "UPLOAD_STATE_PATH",
                    root / "ops/sync/github-upload-state.json",
                ),
                mock.patch.object(
                    tracker_upload_gate,
                    "REPOS_PATH",
                    root / "ops/registry/repos.json",
                ),
            ):
                self.assertNotEqual(0, tracker_upload_gate.main())

    def test_upload_gate_rejects_untracked_files_hidden_by_git_config(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            base = Path(raw_tmp)
            root = base / "repo"
            remote = base / "origin.git"
            root.mkdir()
            seed_gate_repo(root, expected_remote=str(remote))
            init_uploaded_repo(root, remote)
            run(["git", "config", "status.showUntrackedFiles", "no"], root)
            (root / "hidden-local-file.txt").write_text("not uploaded\n", encoding="utf-8")

            with (
                mock.patch.object(tracker_upload_gate, "ROOT", root),
                mock.patch.object(
                    tracker_upload_gate,
                    "UPLOAD_STATE_PATH",
                    root / "ops/sync/github-upload-state.json",
                ),
                mock.patch.object(
                    tracker_upload_gate,
                    "REPOS_PATH",
                    root / "ops/registry/repos.json",
                ),
            ):
                self.assertNotEqual(0, tracker_upload_gate.main())

    def test_repo_audit_does_not_promote_inventory_only_active_projects(self) -> None:
        projects_payload = {
            "projects": [
                {
                    "id": "registry-active",
                    "status": "active",
                }
            ]
        }
        inventory_payload = {
            "active_current_projects": [
                {"slug": "registry-active"},
                {"slug": "inventory-only-active"},
            ]
        }

        sources = tracker_repo_audit.active_project_ids(
            projects_payload,
            inventory_payload,
        )

        self.assertIn("registry-active", sources)
        self.assertNotIn("inventory-only-active", sources)

    def test_status_live_check_rejects_wrong_remote_and_uses_strict_status(self) -> None:
        calls: list[list[str]] = []

        def fake_run_git(args: list[str]) -> str:
            calls.append(args)
            if args == ["status", "--porcelain=v1", "--untracked-files=all"]:
                return ""
            if args == ["rev-parse", "--abbrev-ref", "HEAD"]:
                return "main"
            if args == ["rev-parse", "HEAD"]:
                return "abc123"
            if args == ["remote", "get-url", "origin"]:
                return "https://github.com/example/wrong.git"
            if args == ["ls-remote", "origin", "refs/heads/main"]:
                return "abc123\trefs/heads/main"
            if args == ["rev-list", "--count", "abc123..abc123"]:
                return "0"
            raise AssertionError(f"unexpected git command: {args}")

        repo = {"github_remote": "https://github.com/example/expected.git"}
        with mock.patch.object(tracker_status, "run_git", fake_run_git):
            check = tracker_status.live_git_check(repo)
            marker, reason = tracker_status.live_upload_marker(check)

        self.assertEqual("not uploaded", marker)
        self.assertEqual("origin remote differs from expected GitHub remote", reason)
        self.assertIn(["status", "--porcelain=v1", "--untracked-files=all"], calls)


if __name__ == "__main__":
    unittest.main()
