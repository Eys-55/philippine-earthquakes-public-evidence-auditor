"""Shared helpers for Workflow Run tracker commands."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import errno
import fnmatch
import json
import os
from pathlib import Path
import secrets
import tempfile
from typing import Any


ROOT = Path(os.environ.get("TRACKER_ROOT", Path(__file__).resolve().parents[1])).resolve()
WORKFLOW_RUN_STATUSES = {
    "open",
    "waiting_on_user",
    "blocked",
    "completed",
    "handed_off",
    "abandoned",
}
ACTIVE_WORKFLOW_RUN_STATUSES = {"open", "waiting_on_user", "blocked"}
TERMINAL_WORKFLOW_RUN_STATUSES = {"completed", "handed_off", "abandoned"}
STALE_AFTER = timedelta(hours=24)
VERY_STALE_AFTER = timedelta(days=7)
JsonObject = dict[str, Any]


@dataclass(frozen=True)
class WorkflowRunAge:
    label: str
    age: timedelta | None


def display_path(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


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


def read_json(path: Path, root: Path = ROOT) -> JsonObject:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {display_path(path, root)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{display_path(path, root)}: invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"{display_path(path, root)}: top-level JSON must be an object")
    return payload


def write_json(path: Path, payload: JsonObject) -> None:
    ensure_directory(path.parent)
    serialized = json.dumps(payload, indent=2) + "\n"
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


def append_jsonl(path: Path, payload: JsonObject) -> None:
    ensure_directory(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    fsync_directory(path.parent)


def required_clean_value(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} must not be empty or whitespace")
    return cleaned


def required_values(values: list[str] | None, label: str) -> list[str]:
    if not values:
        raise ValueError(f"{label} must contain at least one entry")
    cleaned = [required_clean_value(value, label) for value in values]
    return list(dict.fromkeys(cleaned))


def records_by_id(payload: JsonObject, key: str, label: str) -> dict[str, JsonObject]:
    records = payload.get(key)
    if not isinstance(records, list):
        raise ValueError(f"{label} registry missing {key} array")

    by_id: dict[str, JsonObject] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"{label} registry contains a non-object record")
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise ValueError(f"{label} registry contains a record without an id")
        if record_id in by_id:
            raise ValueError(f"{label} registry contains duplicate id {record_id}")
        by_id[record_id] = record
    return by_id


def registry_path(root: Path = ROOT) -> Path:
    return root / "ops/registry/workflow-runs.json"


def load_workflow_registry(root: Path = ROOT) -> JsonObject:
    return read_json(registry_path(root), root)


def workflow_runs(payload: JsonObject) -> list[JsonObject]:
    runs = payload.get("workflow_runs")
    if not isinstance(runs, list):
        raise ValueError("workflow-runs registry missing workflow_runs array")
    return [run for run in runs if isinstance(run, dict)]


def write_workflow_registry(payload: JsonObject, root: Path = ROOT) -> None:
    write_json(registry_path(root), payload)


def find_project(project_id: str, root: Path = ROOT) -> JsonObject:
    projects = records_by_id(read_json(root / "ops/registry/projects.json", root), "projects", "projects")
    if project_id not in projects:
        raise ValueError(f"unknown project_id {project_id}")
    return projects[project_id]


def find_workstream_for_project(project_id: str, root: Path = ROOT) -> JsonObject:
    project = find_project(project_id, root)
    workstream_ids = project.get("workstreams", [])
    if not isinstance(workstream_ids, list) or not workstream_ids:
        raise ValueError(f"project_id {project_id} has no workstreams")
    workstreams = records_by_id(
        read_json(root / "ops/registry/workstreams.json", root),
        "workstreams",
        "workstreams",
    )
    for workstream_id in workstream_ids:
        if isinstance(workstream_id, str) and workstream_id in workstreams:
            return workstreams[workstream_id]
    raise ValueError(f"project_id {project_id} has no known workstream")


def all_session_ids(root: Path = ROOT) -> set[str]:
    workstreams = read_json(root / "ops/registry/workstreams.json", root).get("workstreams", [])
    if not isinstance(workstreams, list):
        raise ValueError("workstreams registry missing workstreams array")
    session_ids: set[str] = set()
    for workstream in workstreams:
        if not isinstance(workstream, dict):
            continue
        values = workstream.get("session_ids", [])
        if not isinstance(values, list):
            continue
        for value in values:
            if isinstance(value, str) and value:
                session_ids.add(value)
    return session_ids


def require_known_session(session_id: str, root: Path = ROOT) -> None:
    if session_id not in all_session_ids(root):
        raise ValueError(f"unknown session_id {session_id}")


def generate_workflow_run_id(now: datetime, payload: JsonObject, root: Path = ROOT) -> str:
    existing_ids = {
        run.get("id")
        for run in workflow_runs(payload)
        if isinstance(run.get("id"), str)
    }
    base = f"wfr-{now:%Y%m%d-%H%M%S}"
    for _ in range(20):
        candidate = f"{base}-{secrets.token_hex(2)}"
        log_path = root / f"ops/workflow-runs/{now:%Y-%m-%d}/{candidate}.jsonl"
        if candidate not in existing_ids and not log_path.exists():
            return candidate
    raise ValueError(f"could not generate unique workflow run id for {base}")


def log_path_for(workflow_run_id: str, now: datetime, root: Path = ROOT) -> Path:
    return root / f"ops/workflow-runs/{now:%Y-%m-%d}/{workflow_run_id}.jsonl"


def repo_relative(path: Path, root: Path = ROOT) -> str:
    return display_path(path, root)


def update_workflow_run(
    payload: JsonObject,
    workflow_run_id: str,
    updates: JsonObject,
) -> tuple[JsonObject, JsonObject]:
    runs = payload.get("workflow_runs")
    if not isinstance(runs, list):
        raise ValueError("workflow-runs registry missing workflow_runs array")

    updated_runs: list[object] = []
    updated_run: JsonObject | None = None
    for run in runs:
        if not isinstance(run, dict):
            updated_runs.append(run)
            continue
        if run.get("id") != workflow_run_id:
            updated_runs.append(run)
            continue
        updated_run = {**run, **updates}
        updated_runs.append(updated_run)

    if updated_run is None:
        raise ValueError(f"unknown workflow_run_id {workflow_run_id}")

    updated_payload = dict(payload)
    updated_payload["workflow_runs"] = updated_runs
    return updated_payload, updated_run


def workflow_run_by_id(
    workflow_run_id: str,
    payload: JsonObject | None = None,
    root: Path = ROOT,
) -> JsonObject:
    registry = payload if payload is not None else load_workflow_registry(root)
    for run in workflow_runs(registry):
        if run.get("id") == workflow_run_id:
            return run
    raise ValueError(f"unknown workflow_run_id {workflow_run_id}")


def parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def workflow_run_age(run: JsonObject, now: datetime | None = None) -> WorkflowRunAge:
    if run.get("status") in TERMINAL_WORKFLOW_RUN_STATUSES:
        return WorkflowRunAge("resolved", None)
    if run.get("status") == "waiting_on_user":
        return WorkflowRunAge("waiting_on_user", None)

    checkpoint = parse_timestamp(run.get("last_checkpoint_at"))
    if checkpoint is None:
        return WorkflowRunAge("unknown", None)

    current = now or datetime.now(checkpoint.tzinfo).replace(microsecond=0)
    age = current - checkpoint
    if age >= VERY_STALE_AFTER:
        return WorkflowRunAge("very_stale", age)
    if age >= STALE_AFTER:
        return WorkflowRunAge("stale", age)
    return WorkflowRunAge("fresh", age)


def path_overlaps(left: str, right: str) -> bool:
    left_clean = left.strip().rstrip("/")
    right_clean = right.strip().rstrip("/")
    if not left_clean or not right_clean:
        return False
    if fnmatch.fnmatch(left_clean, right_clean) or fnmatch.fnmatch(right_clean, left_clean):
        return True
    return (
        left_clean == right_clean
        or left_clean.startswith(f"{right_clean}/")
        or right_clean.startswith(f"{left_clean}/")
    )


def risky_parallel_runs(
    *,
    project_id: str,
    owned_paths: list[str],
    exclude_workflow_run_id: str | None = None,
    root: Path = ROOT,
) -> list[JsonObject]:
    payload = load_workflow_registry(root)
    risky: list[JsonObject] = []
    for run in workflow_runs(payload):
        if run.get("id") == exclude_workflow_run_id:
            continue
        if run.get("project_id") != project_id:
            continue
        if run.get("status") not in ACTIVE_WORKFLOW_RUN_STATUSES:
            continue
        run_paths = run.get("owned_paths", [])
        if not isinstance(run_paths, list):
            continue
        if any(
            isinstance(run_path, str)
            and path_overlaps(proposed_path, run_path)
            for proposed_path in owned_paths
            for run_path in run_paths
        ):
            risky.append(run)
    return risky


def render_run_line(run: JsonObject, now: datetime | None = None) -> str:
    run_id = run.get("id", "unknown")
    title = run.get("title", "untitled")
    status = run.get("status", "unknown")
    age = workflow_run_age(run, now)
    next_action = run.get("next_action", "not recorded")
    return f"`{run_id}`: {status}/{age.label} - {title}; next action: {next_action}"
