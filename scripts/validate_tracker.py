#!/usr/bin/env python3
"""Validate the control repo tracker registries and logs."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JsonObject = dict[str, Any]
PENDING_UPLOAD_STATUSES = {
    "pending_upload",
    "ahead_of_remote",
    "remote_missing",
    "pending_local_changes",
}
WORKFLOW_RUN_STATUSES = {
    "open",
    "waiting_on_user",
    "blocked",
    "completed",
    "handed_off",
    "abandoned",
}


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path, root: Path, errors: list[str]) -> JsonObject:
    label = display_path(path, root)
    if not path.exists():
        errors.append(f"missing {label}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errors.append(f"{label}: invalid JSON")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{label}: top-level JSON must be an object")
        return {}
    return payload


def ids_for(records: object, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(records, list):
        errors.append(f"{label}s must be a list")
        return set()

    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            errors.append(f"{label} entry must be an object")
            continue

        record_id = record.get(key)
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{label} entry missing {key}")
            continue
        if record_id in seen:
            errors.append(f"duplicate {label} id {record_id}")
        seen.add(record_id)

    return seen


def required_array(payload: JsonObject, key: str, path: Path, root: Path, errors: list[str]) -> object:
    if key not in payload:
        errors.append(f"{display_path(path, root)}: missing required {key} array")
        return []
    return payload[key]


def string_list(record: JsonObject, key: str, owner_id: str, errors: list[str]) -> list[str]:
    values = record.get(key, [])
    if not isinstance(values, list):
        errors.append(f"{owner_id}: {key} must be a list")
        return []

    strings: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            errors.append(f"{owner_id}: {key} entries must be non-empty strings")
            continue
        strings.append(value)
    return strings


def non_empty_string(
    record: JsonObject,
    key: str,
    owner_id: str,
    errors: list[str],
) -> str | None:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        errors.append(f"{owner_id}: {key} must be a non-empty string")
        return None
    return value


def non_empty_string_list(
    record: JsonObject,
    key: str,
    owner_id: str,
    errors: list[str],
) -> list[str]:
    values = string_list(record, key, owner_id, errors)
    if not values:
        errors.append(f"{owner_id}: {key} must contain at least one entry")
    return values


def validate_json_file(path: Path, root: Path, errors: list[str]) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errors.append(f"{display_path(path, root)}: invalid JSON")


def validate_jsonl_file(path: Path, root: Path, errors: list[str]) -> None:
    label = display_path(path, root)
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError:
                errors.append(f"{label}:{line_number}: invalid JSONL")


def validate_log_folder(root: Path, folder_name: str, errors: list[str], warnings: list[str]) -> None:
    folder = root / "ops" / folder_name
    if not folder.exists():
        warnings.append(f"missing optional log folder ops/{folder_name}")
        return

    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix == ".json":
            validate_json_file(path, root, errors)
        elif path.suffix == ".jsonl":
            validate_jsonl_file(path, root, errors)


def validate_project_records(
    projects: object,
    project_ids: set[str],
    repo_ids: set[str],
    workstream_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(projects, list):
        return

    for project in projects:
        if not isinstance(project, dict):
            continue
        project_id = project.get("id")
        if not isinstance(project_id, str) or not project_id:
            continue

        for repo_id in string_list(project, "repos", project_id, errors):
            if repo_id not in repo_ids:
                errors.append(f"{project_id}: unknown repo {repo_id}")
        for workstream_id in string_list(project, "workstreams", project_id, errors):
            if workstream_id not in workstream_ids:
                errors.append(f"{project_id}: unknown workstream {workstream_id}")


def validate_repo_records(repos: object, project_ids: set[str], errors: list[str]) -> None:
    if not isinstance(repos, list):
        return

    for repo in repos:
        if not isinstance(repo, dict):
            continue
        repo_id = repo.get("id")
        if not isinstance(repo_id, str) or not repo_id:
            continue

        owning_project = repo.get("owning_project")
        if owning_project in (None, "shared"):
            continue
        if not isinstance(owning_project, str) or not owning_project:
            errors.append(f"{repo_id}: owning_project must be a non-empty string")
        elif owning_project not in project_ids:
            errors.append(f"{repo_id}: unknown owning_project {owning_project}")


def validate_workstream_records(
    workstreams: object,
    project_ids: set[str],
    repo_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(workstreams, list):
        return

    for workstream in workstreams:
        if not isinstance(workstream, dict):
            continue
        workstream_id = workstream.get("id")
        if not isinstance(workstream_id, str) or not workstream_id:
            continue

        project_id = workstream.get("project_id")
        repo_id = workstream.get("repo_id")
        if not isinstance(project_id, str) or not project_id:
            errors.append(f"{workstream_id}: project_id must be a non-empty string")
            project_id = None
        if not isinstance(repo_id, str) or not repo_id:
            errors.append(f"{workstream_id}: repo_id must be a non-empty string")
            repo_id = None
        if project_id is not None and project_id not in project_ids:
            errors.append(f"{workstream_id}: unknown project_id {project_id}")
        if repo_id is not None and repo_id not in repo_ids:
            errors.append(f"{workstream_id}: unknown repo_id {repo_id}")


def session_ids_for(workstreams: object, errors: list[str]) -> set[str]:
    session_ids: set[str] = set()
    if not isinstance(workstreams, list):
        return session_ids
    for workstream in workstreams:
        if not isinstance(workstream, dict):
            continue
        workstream_id = workstream.get("id")
        owner_id = workstream_id if isinstance(workstream_id, str) else "workstream"
        for session_id in string_list(workstream, "session_ids", owner_id, errors):
            session_ids.add(session_id)
    return session_ids


def validate_workflow_run_records(
    workflow_runs: object,
    project_ids: set[str],
    session_ids: set[str],
    root: Path,
    errors: list[str],
) -> None:
    if not isinstance(workflow_runs, list):
        return

    for workflow_run in workflow_runs:
        if not isinstance(workflow_run, dict):
            continue
        workflow_run_id = workflow_run.get("id")
        if not isinstance(workflow_run_id, str) or not workflow_run_id:
            continue

        project_id = non_empty_string(workflow_run, "project_id", workflow_run_id, errors)
        if project_id is not None and project_id not in project_ids:
            errors.append(f"{workflow_run_id}: unknown project_id {project_id}")

        session_id = non_empty_string(workflow_run, "session_id", workflow_run_id, errors)
        if session_id is not None and session_id not in session_ids:
            errors.append(f"{workflow_run_id}: unknown session_id {session_id}")

        for key in (
            "title",
            "flow_id",
            "current_skill",
            "started_at",
            "last_checkpoint_at",
            "next_action",
            "log_path",
        ):
            non_empty_string(workflow_run, key, workflow_run_id, errors)

        status = non_empty_string(workflow_run, "status", workflow_run_id, errors)
        if status is not None and status not in WORKFLOW_RUN_STATUSES:
            errors.append(f"{workflow_run_id}: invalid status {status}")

        non_empty_string_list(workflow_run, "owned_paths", workflow_run_id, errors)
        non_empty_string_list(
            workflow_run,
            "validation_commands",
            workflow_run_id,
            errors,
        )

        log_path = workflow_run.get("log_path")
        if isinstance(log_path, str) and log_path:
            candidate = Path(log_path)
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(f"{workflow_run_id}: log_path must be repo-relative")
            elif not (root / candidate).is_file():
                errors.append(f"{workflow_run_id}: log_path does not exist: {log_path}")


def validate_non_projects(projects_payload: JsonObject, project_ids: set[str], errors: list[str]) -> None:
    non_projects = projects_payload.get("non_projects", [])
    if not isinstance(non_projects, list):
        errors.append("non_projects must be a list")
        return

    non_project_ids = {
        item.get("id")
        for item in non_projects
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for overlap in sorted(project_ids & non_project_ids):
        errors.append(f"{overlap}: listed as both project and non_project")


def validate_upload_state(
    repos: object,
    repo_ids: set[str],
    upload_payload: JsonObject,
    errors: list[str],
) -> None:
    upload_repos = upload_payload.get("repos", {})
    if not isinstance(upload_repos, dict):
        errors.append("github-upload-state repos must be an object")
        upload_repos = {}

    for upload_repo_id in sorted(upload_repos):
        if upload_repo_id not in repo_ids:
            errors.append(f"github-upload-state: unknown repo {upload_repo_id}")

    if not isinstance(repos, list):
        return

    for repo in repos:
        if not isinstance(repo, dict):
            continue
        repo_id = repo.get("id")
        if not isinstance(repo_id, str) or not repo_id:
            continue

        state = upload_repos.get(repo_id)
        if repo.get("upload_policy") == "required" and state is None:
            errors.append(f"{repo_id}: required repo missing upload state")
            continue
        if state is None:
            continue
        if not isinstance(state, dict):
            errors.append(f"{repo_id}: upload state must be an object")
            continue

        local_head = state.get("local_head")
        remote_head = state.get("remote_head")
        if local_head is None:
            errors.append(f"{repo_id}: upload state missing local_head")
        if remote_head is None:
            errors.append(f"{repo_id}: upload state missing remote_head")
        status = state.get("status")
        mismatch_allowed = isinstance(status, str) and status in PENDING_UPLOAD_STATUSES
        if (
            local_head is not None
            and remote_head is not None
            and local_head != remote_head
            and not mismatch_allowed
        ):
            errors.append(f"{repo_id}: local_head differs from remote_head")


def validate_tracker_root(root: Path = ROOT) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    projects_payload = read_json(root / "ops/registry/projects.json", root, errors)
    repos_payload = read_json(root / "ops/registry/repos.json", root, errors)
    workstreams_payload = read_json(root / "ops/registry/workstreams.json", root, errors)
    workflow_runs_payload = read_json(
        root / "ops/registry/workflow-runs.json",
        root,
        errors,
    )
    upload_payload = read_json(root / "ops/sync/github-upload-state.json", root, errors)

    projects = required_array(
        projects_payload,
        "projects",
        root / "ops/registry/projects.json",
        root,
        errors,
    )
    repos = required_array(
        repos_payload,
        "repos",
        root / "ops/registry/repos.json",
        root,
        errors,
    )
    workstreams = required_array(
        workstreams_payload,
        "workstreams",
        root / "ops/registry/workstreams.json",
        root,
        errors,
    )
    workflow_runs = required_array(
        workflow_runs_payload,
        "workflow_runs",
        root / "ops/registry/workflow-runs.json",
        root,
        errors,
    )

    project_ids = ids_for(projects, "id", "project", errors)
    repo_ids = ids_for(repos, "id", "repo", errors)
    workstream_ids = ids_for(workstreams, "id", "workstream", errors)
    ids_for(workflow_runs, "id", "workflow_run", errors)
    session_ids = session_ids_for(workstreams, errors)

    validate_non_projects(projects_payload, project_ids, errors)
    validate_project_records(projects, project_ids, repo_ids, workstream_ids, errors)
    validate_repo_records(repos, project_ids, errors)
    validate_workstream_records(workstreams, project_ids, repo_ids, errors)
    validate_workflow_run_records(workflow_runs, project_ids, session_ids, root, errors)
    validate_upload_state(repos, repo_ids, upload_payload, errors)

    validate_log_folder(root, "events", errors, warnings)
    validate_log_folder(root, "sessions", errors, warnings)
    validate_log_folder(root, "workflow-runs", errors, warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def main() -> int:
    result = validate_tracker_root(ROOT)
    for warning in result.warnings:
        print(f"warning: {warning}")
    if result.errors:
        print("tracker validation failed:", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("tracker validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
