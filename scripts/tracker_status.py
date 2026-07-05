#!/usr/bin/env python3
"""Print control repo project status from tracker registries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UPLOADED_STATUSES = {"clean", "uploaded", "verified"}
PENDING_STATUS_PREFIXES = ("pending", "dirty", "ahead")
DIRTY_COUNT_KEYS = ("untracked_file_count", "dirty_file_count", "ahead_count")
JsonObject = dict[str, Any]


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


def has_dirty_upload_indicator(state: JsonObject) -> bool:
    status = state.get("status")
    normalized_status = status.lower() if isinstance(status, str) else ""
    if normalized_status.startswith(PENDING_STATUS_PREFIXES):
        return True
    if any(positive_int(state.get(key)) for key in DIRTY_COUNT_KEYS):
        return True
    return bool(state.get("pending_reason"))


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


def print_upload_state(upload_payload: JsonObject) -> None:
    print("## GitHub Upload State")
    repos = upload_payload.get("repos", {})
    if not isinstance(repos, dict) or not repos:
        print("- No upload state recorded.")
        return

    for repo_id in sorted(repos):
        state = repos[repo_id]
        if not isinstance(state, dict):
            print(f"- `{repo_id}`: not uploaded (invalid upload state)")
            continue
        marker = upload_marker(state)
        status = state.get("status", "unknown")
        local_branch = state.get("local_branch", "unknown")
        remote_branch = state.get("remote_branch", "unknown")
        print(f"- `{repo_id}`: {marker} ({status}; {local_branch} -> {remote_branch})")


def main() -> int:
    projects_payload = read_json(ROOT / "ops/registry/projects.json")
    workstreams_payload = read_json(ROOT / "ops/registry/workstreams.json")
    upload_payload = read_json(ROOT / "ops/sync/github-upload-state.json")

    print_active_projects(projects_payload, workstreams_payload)
    print_not_active_projects(projects_payload)
    print_upload_state(upload_payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
