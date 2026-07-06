#!/usr/bin/env python3
"""Export control-repo tracker state for the static Astro monitor."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(os.environ.get("TRACKER_ROOT", Path(__file__).resolve().parents[1])).resolve()
DEFAULT_OUTPUT = ROOT / "tracker-ui/src/data/tracker-dashboard.json"
JsonObject = dict[str, Any]


def display_path(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> JsonObject:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {display_path(path)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{display_path(path)}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{display_path(path)}: top-level JSON must be an object")
    return payload


def records_by_id(records: object) -> dict[str, JsonObject]:
    if not isinstance(records, list):
        return {}
    indexed: dict[str, JsonObject] = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        record_id = record.get("id")
        if isinstance(record_id, str) and record_id:
            indexed[record_id] = record
    return indexed


def upload_status(upload_payload: JsonObject) -> str:
    repos = upload_payload.get("repos", {})
    if not isinstance(repos, dict) or not repos:
        return "unknown"
    statuses = {
        str(repo.get("status", "unknown"))
        for repo in repos.values()
        if isinstance(repo, dict)
    }
    if statuses == {"uploaded"}:
        return "uploaded"
    if "pending_local_changes" in statuses:
        return "pending_local_changes"
    if "not_uploaded" in statuses:
        return "not_uploaded"
    if len(statuses) == 1:
        return next(iter(statuses))
    return "mixed"


def normalize_projects(projects_payload: JsonObject, workstreams_payload: JsonObject) -> list[JsonObject]:
    workstreams_by_id = records_by_id(workstreams_payload.get("workstreams"))
    normalized: list[JsonObject] = []
    for project in projects_payload.get("projects", []):
        if not isinstance(project, dict):
            continue
        project_workstreams = []
        for workstream_id in project.get("workstreams", []):
            if isinstance(workstream_id, str) and workstream_id in workstreams_by_id:
                project_workstreams.append(workstreams_by_id[workstream_id])
        normalized.append(
            {
                "id": project.get("id"),
                "title": project.get("title"),
                "status": project.get("status"),
                "owner_intent": project.get("owner_intent"),
                "current_goal": project.get("current_goal"),
                "workstreams": project_workstreams,
            }
        )
    return normalized


def normalize_upload_repos(upload_payload: JsonObject) -> list[JsonObject]:
    repos = upload_payload.get("repos", {})
    if not isinstance(repos, dict):
        return []
    normalized: list[JsonObject] = []
    for repo_id, repo in sorted(repos.items()):
        if not isinstance(repo, dict):
            continue
        normalized.append(
            {
                "id": repo_id,
                "status": repo.get("status", "unknown"),
                "local_branch": repo.get("local_branch"),
                "local_head": repo.get("local_head"),
                "remote_branch": repo.get("remote_branch"),
                "remote_head": repo.get("remote_head"),
                "dirty": repo.get("dirty"),
                "untracked_file_count": repo.get("untracked_file_count"),
                "last_verified_at": repo.get("last_verified_at"),
                "verification_command": repo.get("verification_command"),
            }
        )
    return normalized


def build_dashboard(root: Path = ROOT) -> JsonObject:
    projects_payload = read_json(root / "ops/registry/projects.json")
    workstreams_payload = read_json(root / "ops/registry/workstreams.json")
    workflow_runs_payload = read_json(root / "ops/registry/workflow-runs.json")
    upload_payload = read_json(root / "ops/sync/github-upload-state.json")

    projects = normalize_projects(projects_payload, workstreams_payload)
    workflow_runs = [
        run for run in workflow_runs_payload.get("workflow_runs", []) if isinstance(run, dict)
    ]
    open_runs = [
        run for run in workflow_runs if run.get("status") in {"open", "waiting_on_user", "blocked"}
    ]
    upload_repos = normalize_upload_repos(upload_payload)

    return {
        "kind": "tracker_astro_monitor_dashboard",
        "generated_at": datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "source_root": display_path(root, root),
        "summary": {
            "active_projects": sum(1 for project in projects if project.get("status") == "active"),
            "workstreams": len(workstreams_payload.get("workstreams", [])),
            "workflow_runs": len(workflow_runs),
            "open_workflow_runs": len(open_runs),
            "upload_status": upload_status(upload_payload),
            "repos": len(upload_repos),
        },
        "projects": projects,
        "workflow_runs": workflow_runs,
        "upload_repos": upload_repos,
        "non_projects": projects_payload.get("non_projects", []),
    }


def without_generated_at(payload: JsonObject) -> JsonObject:
    return {key: value for key, value in payload.items() if key != "generated_at"}


def preserve_generated_at_when_unchanged(output: Path, dashboard: JsonObject) -> JsonObject:
    if not output.exists():
        return dashboard
    try:
        existing = json.loads(output.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return dashboard
    if not isinstance(existing, dict):
        return dashboard
    existing_generated_at = existing.get("generated_at")
    if (
        isinstance(existing_generated_at, str)
        and without_generated_at(existing) == without_generated_at(dashboard)
    ):
        return {**dashboard, "generated_at": existing_generated_at}
    return dashboard


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_OUTPUT.as_posix())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output

    try:
        dashboard = preserve_generated_at_when_unchanged(output, build_dashboard(ROOT))
    except ValueError as exc:
        print(str(exc), file=os.sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(dashboard, indent=2) + "\n", encoding="utf-8")
    print(display_path(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
