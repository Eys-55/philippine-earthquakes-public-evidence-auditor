#!/usr/bin/env python3
"""Print control repo project status from tracker registries."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
UPLOADED_STATUSES = {"clean", "uploaded", "verified"}
PENDING_STATUS_PREFIXES = ("pending", "dirty", "ahead")
DIRTY_COUNT_KEYS = ("untracked_file_count", "dirty_file_count", "ahead_count")
JsonObject = dict[str, Any]


class GitCommandError(RuntimeError):
    """Raised when a read-only git status check fails."""


@dataclass(frozen=True)
class LiveGitCheck:
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


def read_json(path: Path) -> JsonObject:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top-level JSON must be an object")
    return payload


def as_records(payload: JsonObject, key: str) -> list[JsonObject]:
    records = payload.get(key, [])
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict)]


def active_projects(projects_payload: JsonObject) -> list[JsonObject]:
    return [
        project
        for project in as_records(projects_payload, "projects")
        if project.get("status") == "active"
    ]


def workstreams_by_project(workstreams_payload: JsonObject) -> dict[str, list[JsonObject]]:
    by_project: dict[str, list[JsonObject]] = {}
    for workstream in as_records(workstreams_payload, "workstreams"):
        project_id = workstream.get("project_id")
        if not isinstance(project_id, str) or not project_id:
            continue
        by_project.setdefault(project_id, []).append(workstream)
    return by_project


def repos_by_id(repos_payload: JsonObject) -> dict[str, JsonObject]:
    repos: dict[str, JsonObject] = {}
    for repo in as_records(repos_payload, "repos"):
        repo_id = repo.get("id")
        if isinstance(repo_id, str) and repo_id:
            repos[repo_id] = repo
    return repos


def positive_int(value: object) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value > 0
    if isinstance(value, str):
        try:
            return int(value) > 0
        except ValueError:
            return False
    return False


def run_git(args: list[str]) -> str:
    command = ["git", *args]
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise GitCommandError(str(exc)) from exc
    if result.returncode != 0:
        raise GitCommandError(result.stderr.strip() or f"{' '.join(command)} failed")
    return result.stdout.rstrip("\n")


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


def parse_remote_head(ls_remote_output: str) -> str:
    first_line = ls_remote_output.splitlines()[0] if ls_remote_output.splitlines() else ""
    parts = first_line.split()
    return parts[0] if parts else ""


def ahead_count(local_head: str, remote_head: str) -> int | None:
    if not local_head or not remote_head:
        return None
    try:
        output = run_git(["rev-list", "--count", f"{remote_head}..{local_head}"])
    except GitCommandError:
        return None
    try:
        return int(output)
    except ValueError:
        return None


def live_git_check(repo: JsonObject) -> LiveGitCheck:
    expected_remote = repo.get("github_remote")
    if not isinstance(expected_remote, str) or not expected_remote:
        raise GitCommandError("registered repo is missing github_remote")

    status_output = run_git(["status", "--porcelain=v1", "--untracked-files=all"])
    untracked_file_count, dirty_file_count = status_counts(status_output)
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    local_head = run_git(["rev-parse", "HEAD"])
    remote_url = run_git(["remote", "get-url", "origin"])
    remote_head = parse_remote_head(run_git(["ls-remote", "origin", f"refs/heads/{branch}"]))
    return LiveGitCheck(
        branch=branch,
        local_head=local_head,
        remote_url=remote_url,
        expected_remote=expected_remote,
        remote_head=remote_head,
        ahead_count=ahead_count(local_head, remote_head),
        untracked_file_count=untracked_file_count,
        dirty_file_count=dirty_file_count,
    )


def has_dirty_upload_indicator(state: JsonObject) -> bool:
    status = state.get("status")
    normalized_status = status.lower() if isinstance(status, str) else ""
    if normalized_status.startswith(PENDING_STATUS_PREFIXES):
        return True
    if any(positive_int(state.get(key)) for key in DIRTY_COUNT_KEYS):
        return True
    return bool(state.get("pending_reason"))


def recorded_status(state: JsonObject) -> str:
    status = state.get("status")
    return status if isinstance(status, str) and status else "unknown"


def upload_marker(state: JsonObject) -> str:
    status = state.get("status")
    local_head = state.get("local_head")
    remote_head = state.get("remote_head")
    same_head = bool(local_head and remote_head and local_head == remote_head)
    if has_dirty_upload_indicator(state):
        return "pending"
    if status in UPLOADED_STATUSES and same_head:
        return "uploaded"
    return "not uploaded"


def live_upload_marker(check: LiveGitCheck) -> tuple[str, str]:
    if not check.remote_matches_expected:
        return "not uploaded", "origin remote differs from expected GitHub remote"
    if check.has_local_changes:
        return "pending", "dirty/untracked"
    if not check.remote_head:
        return "not uploaded", "remote branch missing"
    if check.local_head == check.remote_head:
        return "uploaded", "HEAD matches remote"
    if check.ahead_count is not None and check.ahead_count > 0:
        return "pending", "local HEAD ahead of remote"
    return "not uploaded", "local HEAD differs from remote"


def upload_source_marker(
    *,
    repo: JsonObject | None,
    state: JsonObject,
) -> tuple[str, str, str, str]:
    local_branch = state.get("local_branch", "unknown")
    remote_branch = state.get("remote_branch", "unknown")
    if repo is not None and repo.get("path") == ".":
        try:
            check = live_git_check(repo)
        except GitCommandError:
            return (
                upload_marker(state),
                f"recorded {recorded_status(state)}",
                str(local_branch),
                str(remote_branch),
            )
        marker, live_reason = live_upload_marker(check)
        return (
            marker,
            f"live git check: {live_reason}; recorded {recorded_status(state)}",
            check.branch,
            check.branch,
        )
    return (
        upload_marker(state),
        f"recorded {recorded_status(state)}",
        str(local_branch),
        str(remote_branch),
    )


def project_workstreams(
    project: JsonObject,
    grouped_workstreams: dict[str, list[JsonObject]],
) -> list[JsonObject]:
    assigned_ids = project.get("workstreams", [])
    if not isinstance(assigned_ids, list) or not assigned_ids:
        return []

    project_id = project.get("id")
    if not isinstance(project_id, str):
        return []

    assigned_id_set = {item for item in assigned_ids if isinstance(item, str)}
    return [
        workstream
        for workstream in grouped_workstreams.get(project_id, [])
        if workstream.get("id") in assigned_id_set
    ]


def print_active_projects(
    projects_payload: JsonObject,
    workstreams_payload: JsonObject,
) -> None:
    grouped_workstreams = workstreams_by_project(workstreams_payload)

    print("# Project Status")
    print()
    for project in active_projects(projects_payload):
        project_id = project.get("id", "unknown")
        print(f"## {project.get('title', project_id)}")
        print(f"- ID: `{project_id}`")
        print(f"- Status: {project.get('status', 'unknown')}")
        print(f"- Current goal: {project.get('current_goal', 'not recorded')}")

        assigned_workstreams = project_workstreams(project, grouped_workstreams)
        if assigned_workstreams:
            for workstream in assigned_workstreams:
                workstream_id = workstream.get("id", "unknown")
                status = workstream.get("status", "unknown")
                next_action = workstream.get("next_action", "not recorded")
                print(f"- Workstream `{workstream_id}`: {status}; next action: {next_action}")
        else:
            print("- Workstream: none recorded")
        print()


def print_not_active_projects(projects_payload: JsonObject) -> None:
    non_projects = as_records(projects_payload, "non_projects")
    if not non_projects:
        return

    print("## Not Active Projects")
    for item in non_projects:
        item_id = item.get("id", "unknown")
        reason = item.get("reason", "not recorded")
        print(f"- `{item_id}`: {reason}")
    print()


def print_upload_state(upload_payload: JsonObject, repos_payload: JsonObject) -> None:
    print("## GitHub Upload State")
    repos = upload_payload.get("repos", {})
    if not isinstance(repos, dict) or not repos:
        print("- No upload state recorded.")
        return

    registry_repos = repos_by_id(repos_payload)
    for repo_id in sorted(repos):
        state = repos[repo_id]
        if not isinstance(state, dict):
            print(f"- `{repo_id}`: not uploaded (invalid upload state)")
            continue
        marker, source, local_branch, remote_branch = upload_source_marker(
            repo=registry_repos.get(repo_id),
            state=state,
        )
        print(f"- `{repo_id}`: {marker} ({source}; {local_branch} -> {remote_branch})")


def main() -> int:
    projects_payload = read_json(ROOT / "ops/registry/projects.json")
    repos_payload = read_json(ROOT / "ops/registry/repos.json")
    workstreams_payload = read_json(ROOT / "ops/registry/workstreams.json")
    upload_payload = read_json(ROOT / "ops/sync/github-upload-state.json")

    print_active_projects(projects_payload, workstreams_payload)
    print_not_active_projects(projects_payload)
    print_upload_state(upload_payload, repos_payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
