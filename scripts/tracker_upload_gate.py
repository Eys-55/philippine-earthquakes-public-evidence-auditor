#!/usr/bin/env python3
"""Verify that the current branch HEAD is uploaded to GitHub."""

from __future__ import annotations

from dataclasses import dataclass
import errno
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
UPLOAD_STATE_PATH = ROOT / "ops" / "sync" / "github-upload-state.json"
REPOS_PATH = ROOT / "ops" / "registry" / "repos.json"
REPO_PATH = "."
JsonObject = dict[str, Any]


class GitCommandError(RuntimeError):
    """Raised when a required git command cannot be completed."""

    def __init__(self, command: list[str], stderr: str) -> None:
        super().__init__(f"{' '.join(command)} failed: {stderr.strip()}")
        self.command = command
        self.stderr = stderr


@dataclass(frozen=True)
class RepoTarget:
    repo_id: str
    expected_remote: str


@dataclass(frozen=True)
class GitSnapshot:
    status_output: str
    branch: str
    local_head: str
    remote_url: str
    expected_remote: str
    remote_head: str
    ahead_count: int | None
    untracked_file_count: int
    dirty_file_count: int

    @property
    def has_local_changes(self) -> bool:
        return self.untracked_file_count > 0 or self.dirty_file_count > 0

    @property
    def remote_matches_expected(self) -> bool:
        return remote_matches(self.remote_url, self.expected_remote)

    @property
    def is_uploaded(self) -> bool:
        return (
            not self.has_local_changes
            and self.remote_matches_expected
            and bool(self.remote_head)
            and self.local_head == self.remote_head
        )


def fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY

    fd: int | None = None
    try:
        fd = os.open(path, flags)
        os.fsync(fd)
    except OSError as exc:
        if exc.errno in {errno.EINVAL, errno.ENOTSUP}:
            return
        raise
    finally:
        if fd is not None:
            os.close(fd)


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    fsync_directory(path)
    if path.parent.exists():
        fsync_directory(path.parent)


def write_json(path: Path, payload: JsonObject) -> bool:
    ensure_directory(path.parent)
    serialized = json.dumps(payload, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == serialized:
        return False

    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=path.parent,
        encoding="utf-8",
    ) as handle:
        temp_path = Path(handle.name)
        handle.write(serialized)
        handle.flush()
        os.fsync(handle.fileno())

    try:
        temp_path.replace(path)
        fsync_directory(path.parent)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    return True


def read_json(path: Path) -> JsonObject:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top-level JSON must be an object")
    return payload


def run_git(args: list[str], *, check: bool = True) -> str:
    command = ["git", *args]
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise GitCommandError(command, result.stderr)
    return result.stdout.rstrip("\n")


def status_counts(status_output: str) -> tuple[int, int]:
    untracked_file_count = 0
    dirty_file_count = 0
    for line in status_output.splitlines():
        if not line:
            continue
        if line.startswith("?? "):
            untracked_file_count += 1
        else:
            dirty_file_count += 1
    return untracked_file_count, dirty_file_count


def strip_git_suffix(value: str) -> str:
    return value[:-4] if value.endswith(".git") else value


def normalize_remote_url(remote_url: str) -> str:
    raw_url = remote_url.strip().rstrip("/")
    if raw_url.startswith("git@"):
        host_path = raw_url[4:]
        if ":" in host_path:
            host, path = host_path.split(":", 1)
            return f"{host.lower()}/{strip_git_suffix(path.strip('/'))}"

    parsed = urlparse(raw_url)
    if parsed.scheme and parsed.netloc:
        host = (parsed.hostname or parsed.netloc).lower()
        return f"{host}/{strip_git_suffix(parsed.path.strip('/'))}"

    return strip_git_suffix(raw_url)


def remote_matches(actual_remote: str, expected_remote: str) -> bool:
    return normalize_remote_url(actual_remote) == normalize_remote_url(expected_remote)


def current_repo_target() -> RepoTarget:
    payload = read_json(REPOS_PATH)
    repos = payload.get("repos", [])
    if not isinstance(repos, list):
        raise ValueError("ops/registry/repos.json: repos must be a list")

    required_targets: list[RepoTarget] = []
    fallback_targets: list[RepoTarget] = []
    for repo in repos:
        if not isinstance(repo, dict):
            continue
        repo_id = repo.get("id")
        if not isinstance(repo_id, str) or not repo_id:
            continue
        expected_remote = repo.get("github_remote")
        if not isinstance(expected_remote, str) or not expected_remote:
            continue
        target = RepoTarget(repo_id=repo_id, expected_remote=expected_remote)
        if repo.get("path") == REPO_PATH:
            fallback_targets.append(target)
            if repo.get("upload_policy") == "required":
                required_targets.append(target)

    candidates = required_targets or fallback_targets
    if len(candidates) != 1:
        raise ValueError("expected exactly one tracker repo at path .")
    return candidates[0]


def parse_remote_head(ls_remote_output: str) -> str:
    first_line = ls_remote_output.splitlines()[0] if ls_remote_output.splitlines() else ""
    parts = first_line.split()
    return parts[0] if parts else ""


def ahead_count(local_head: str, remote_head: str) -> int | None:
    if not local_head or not remote_head:
        return None
    output = run_git(["rev-list", "--count", f"{remote_head}..{local_head}"], check=False)
    try:
        return int(output)
    except ValueError:
        return None


def git_snapshot(target: RepoTarget) -> GitSnapshot:
    status_output = run_git(["status", "--porcelain=v1", "--untracked-files=all"])
    untracked_file_count, dirty_file_count = status_counts(status_output)
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    local_head = run_git(["rev-parse", "HEAD"])
    remote_url = run_git(["remote", "get-url", "origin"])
    remote_head = parse_remote_head(run_git(["ls-remote", "origin", f"refs/heads/{branch}"]))
    return GitSnapshot(
        status_output=status_output,
        branch=branch,
        local_head=local_head,
        remote_url=remote_url,
        expected_remote=target.expected_remote,
        remote_head=remote_head,
        ahead_count=ahead_count(local_head, remote_head),
        untracked_file_count=untracked_file_count,
        dirty_file_count=dirty_file_count,
    )


def upload_status(
    *,
    has_local_changes: bool,
    remote_matches_expected: bool,
    local_head: str,
    remote_head: str,
    count_ahead: int | None,
) -> str:
    if not remote_matches_expected:
        return "wrong_remote"
    if has_local_changes:
        return "pending_local_changes"
    if not remote_head:
        return "remote_missing"
    if local_head == remote_head:
        return "uploaded"
    if count_ahead is not None and count_ahead > 0:
        return "ahead_of_remote"
    return "pending_upload"


def refreshed_upload_state(
    *,
    repo_id: str,
    branch: str,
    local_head: str,
    remote_url: str,
    expected_remote: str,
    remote_matches_expected: bool,
    remote_head: str,
    status: str,
    untracked_file_count: int,
    dirty_file_count: int,
    count_ahead: int | None,
    now: str,
    last_verification_command: str,
) -> JsonObject:
    existing_payload = read_json(UPLOAD_STATE_PATH) if UPLOAD_STATE_PATH.exists() else {}
    existing_repos = existing_payload.get("repos", {})
    if not isinstance(existing_repos, dict):
        existing_repos = {}

    clean_and_uploaded = (
        untracked_file_count == 0
        and dirty_file_count == 0
        and remote_matches_expected
        and bool(remote_head)
        and local_head == remote_head
    )
    updated_repos = {
        key: value
        for key, value in existing_repos.items()
        if isinstance(key, str) and key != repo_id
    }
    updated_repos[repo_id] = {
        "local_branch": branch,
        "local_head": local_head,
        "remote_url": remote_url,
        "expected_remote": expected_remote,
        "remote_matches_expected": remote_matches_expected,
        "remote_branch": branch,
        "remote_head": remote_head,
        "status": status,
        "untracked_file_count": untracked_file_count,
        "dirty_file_count": dirty_file_count,
        "ahead_count": count_ahead,
        "last_successful_upload": now if clean_and_uploaded else None,
        "last_verification_command": last_verification_command,
    }

    return {
        "schema_version": 1,
        "generated_at": now,
        "repos": dict(sorted(updated_repos.items())),
    }


def main() -> int:
    repo_target = current_repo_target()
    snapshot = git_snapshot(repo_target)
    if snapshot.is_uploaded:
        # Clean success is no-write: a tracked upload-state file cannot
        # self-certify the commit that contains its own updated hash.
        print("uploaded to GitHub")
        return 0

    remote_ref = f"refs/heads/{snapshot.branch}"
    ls_remote_command = f"git ls-remote origin {remote_ref}"
    status = upload_status(
        has_local_changes=snapshot.has_local_changes,
        remote_matches_expected=snapshot.remote_matches_expected,
        local_head=snapshot.local_head,
        remote_head=snapshot.remote_head,
        count_ahead=snapshot.ahead_count,
    )
    now = datetime.now().astimezone().replace(microsecond=0).isoformat()

    write_json(
        UPLOAD_STATE_PATH,
        refreshed_upload_state(
            repo_id=repo_target.repo_id,
            branch=snapshot.branch,
            local_head=snapshot.local_head,
            remote_url=snapshot.remote_url,
            expected_remote=snapshot.expected_remote,
            remote_matches_expected=snapshot.remote_matches_expected,
            remote_head=snapshot.remote_head,
            status=status,
            untracked_file_count=snapshot.untracked_file_count,
            dirty_file_count=snapshot.dirty_file_count,
            count_ahead=snapshot.ahead_count,
            now=now,
            last_verification_command=ls_remote_command,
        ),
    )

    post_write_snapshot = git_snapshot(repo_target)
    post_write_status = upload_status(
        has_local_changes=post_write_snapshot.has_local_changes,
        remote_matches_expected=post_write_snapshot.remote_matches_expected,
        local_head=post_write_snapshot.local_head,
        remote_head=post_write_snapshot.remote_head,
        count_ahead=post_write_snapshot.ahead_count,
    )
    post_write_remote_ref = f"refs/heads/{post_write_snapshot.branch}"
    post_write_ls_remote_command = f"git ls-remote origin {post_write_remote_ref}"
    write_json(
        UPLOAD_STATE_PATH,
        refreshed_upload_state(
            repo_id=repo_target.repo_id,
            branch=post_write_snapshot.branch,
            local_head=post_write_snapshot.local_head,
            remote_url=post_write_snapshot.remote_url,
            expected_remote=post_write_snapshot.expected_remote,
            remote_matches_expected=post_write_snapshot.remote_matches_expected,
            remote_head=post_write_snapshot.remote_head,
            status=post_write_status,
            untracked_file_count=post_write_snapshot.untracked_file_count,
            dirty_file_count=post_write_snapshot.dirty_file_count,
            count_ahead=post_write_snapshot.ahead_count,
            now=datetime.now().astimezone().replace(microsecond=0).isoformat(),
            last_verification_command=post_write_ls_remote_command,
        ),
    )

    print("local changes still need upload")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GitCommandError, OSError, ValueError, json.JSONDecodeError) as exc:
        print("local changes still need upload")
        print(f"tracker upload gate error: {exc}", file=sys.stderr)
        raise SystemExit(2)
