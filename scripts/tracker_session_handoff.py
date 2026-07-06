#!/usr/bin/env python3
"""Generate the latest control tracker handoff from a session log."""

from __future__ import annotations

import argparse
import errno
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

try:
    from tracker_workflow_lib import render_run_line
except ImportError:  # pragma: no cover - used when imported as scripts.tracker_session_handoff
    from scripts.tracker_workflow_lib import render_run_line


ROOT = Path(__file__).resolve().parents[1]
WORKSTREAM_REGISTRY_LOCK_PATH = ROOT / "ops/sessions/.session-start.lock"
JsonObject = dict[str, Any]


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
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


def acquire_workstream_registry_lock() -> Path:
    ensure_directory(WORKSTREAM_REGISTRY_LOCK_PATH.parent)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(WORKSTREAM_REGISTRY_LOCK_PATH, flags, 0o600)
    except FileExistsError as exc:
        raise ValueError(
            f"workstream registry lock exists at {display_path(WORKSTREAM_REGISTRY_LOCK_PATH)}; "
            "another session start or handoff may be running"
        ) from exc

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
            handle.flush()
            os.fsync(handle.fileno())
        fsync_directory(WORKSTREAM_REGISTRY_LOCK_PATH.parent)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        WORKSTREAM_REGISTRY_LOCK_PATH.unlink(missing_ok=True)
        fsync_directory(WORKSTREAM_REGISTRY_LOCK_PATH.parent)
        raise

    return WORKSTREAM_REGISTRY_LOCK_PATH


def release_workstream_registry_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
        fsync_directory(lock_path.parent)
    except FileNotFoundError:
        return


def write_text(path: Path, text: str) -> None:
    ensure_directory(path.parent)
    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=path.parent,
        encoding="utf-8",
    ) as handle:
        temp_path = Path(handle.name)
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())

    try:
        temp_path.replace(path)
        fsync_directory(path.parent)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def write_json(path: Path, payload: JsonObject) -> None:
    write_text(path, json.dumps(payload, indent=2) + "\n")


def required_clean_value(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} must not be empty or whitespace")
    return cleaned


def clean_args(args: argparse.Namespace) -> argparse.Namespace:
    session_id = required_clean_value(args.session_id, "session_id")
    if "/" in session_id or "\\" in session_id:
        raise ValueError("session_id must not contain path separators")
    return argparse.Namespace(
        session_id=session_id,
        next_action=required_clean_value(args.next_action, "next_action"),
    )


def find_session_path(session_id: str) -> Path:
    sessions_dir = ROOT / "ops/sessions"
    if not sessions_dir.exists():
        raise ValueError("missing ops/sessions")

    expected_stem = f"session-{session_id}"
    matches = [
        path
        for path in sorted(sessions_dir.rglob("session-*.jsonl"))
        if path.is_file() and path.stem == expected_stem
    ]
    if not matches:
        raise ValueError(f"unknown session_id {session_id}")
    if len(matches) > 1:
        labels = ", ".join(display_path(path) for path in matches)
        raise ValueError(f"duplicate session_id {session_id}: {labels}")
    return matches[0]


def read_session_events(path: Path) -> list[JsonObject]:
    events: list[JsonObject] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{display_path(path)}:{line_number}: invalid JSONL: {exc}"
                ) from exc
            if not isinstance(payload, dict):
                raise ValueError(
                    f"{display_path(path)}:{line_number}: JSONL event must be an object"
                )
            events.append(payload)
    if not events:
        raise ValueError(f"{display_path(path)}: session log is empty")
    return events


def session_started_event(events: list[JsonObject], session_id: str) -> JsonObject:
    started_events = [
        event
        for event in events
        if event.get("event_type") == "session_started"
        and event.get("session_id") == session_id
    ]
    if not started_events:
        raise ValueError(f"session_id {session_id} has no session_started event")
    if len(started_events) > 1:
        raise ValueError(f"session_id {session_id} has duplicate session_started events")

    started = started_events[0]
    for key in ("project_id", "repo_id", "workstream_id"):
        value = started.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"session_id {session_id} missing {key} in session_started event")
    return started


def validate_registry_links(
    project_id: str,
    repo_id: str,
    workstream_id: str,
    projects_by_id: dict[str, JsonObject],
    repos_by_id: dict[str, JsonObject],
    workstreams_by_id: dict[str, JsonObject],
) -> JsonObject:
    if project_id not in projects_by_id:
        raise ValueError(f"unknown project_id {project_id}")
    if repo_id not in repos_by_id:
        raise ValueError(f"unknown repo_id {repo_id}")
    if workstream_id not in workstreams_by_id:
        raise ValueError(f"unknown workstream_id {workstream_id}")

    workstream = workstreams_by_id[workstream_id]
    if workstream.get("project_id") != project_id:
        raise ValueError(
            f"workstream_id {workstream_id} belongs to project_id "
            f"{workstream.get('project_id')}, not {project_id}"
        )
    if workstream.get("repo_id") != repo_id:
        raise ValueError(
            f"workstream_id {workstream_id} belongs to repo_id "
            f"{workstream.get('repo_id')}, not {repo_id}"
        )
    return workstream


def required_workstream_session_ids(workstream: JsonObject, workstream_id: str) -> list[str]:
    if "session_ids" not in workstream:
        raise ValueError(f"workstream_id {workstream_id} missing session_ids")

    raw_session_ids = workstream["session_ids"]
    if not isinstance(raw_session_ids, list):
        raise ValueError(f"workstream_id {workstream_id} session_ids must be a list")

    session_ids: list[str] = []
    for index, session_id in enumerate(raw_session_ids):
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError(
                f"workstream_id {workstream_id} session_ids[{index}] "
                "must be a non-empty string"
            )
        session_ids.append(session_id)
    return session_ids


def require_registered_session(
    workstream: JsonObject,
    workstream_id: str,
    session_id: str,
) -> list[str]:
    session_ids = required_workstream_session_ids(workstream, workstream_id)
    if session_id not in session_ids:
        raise ValueError(
            f"session_id {session_id} is not registered on workstream_id {workstream_id}"
        )
    return session_ids


def update_workstream_next_action(
    workstreams_payload: JsonObject,
    workstream_id: str,
    next_action: str,
) -> tuple[JsonObject, JsonObject]:
    workstreams = workstreams_payload.get("workstreams")
    if not isinstance(workstreams, list):
        raise ValueError("workstreams registry missing workstreams array")

    updated_workstreams: list[object] = []
    updated_workstream: JsonObject | None = None
    for workstream in workstreams:
        if not isinstance(workstream, dict):
            raise ValueError("workstreams registry contains a non-object record")
        if workstream.get("id") != workstream_id:
            updated_workstreams.append(workstream)
            continue

        updated_workstream = dict(workstream)
        updated_workstream["next_action"] = next_action
        updated_workstreams.append(updated_workstream)

    if updated_workstream is None:
        raise ValueError(f"unknown workstream_id {workstream_id}")

    updated_payload = dict(workstreams_payload)
    updated_payload["workstreams"] = updated_workstreams
    return updated_payload, updated_workstream


def event_summary(event: JsonObject) -> str:
    event_type = event.get("event_type")
    summary = event.get("summary")
    if isinstance(summary, str) and summary.strip():
        return summary.strip()

    if event_type == "session_started":
        objective = event.get("objective")
        if isinstance(objective, str) and objective.strip():
            return f"Started session with objective: {objective.strip()}"
        return "Started session."

    if isinstance(event_type, str) and event_type:
        return f"Recorded {event_type} event."
    return "Recorded session event."


def markdown_bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def workflow_runs_for_session(session_id: str) -> list[JsonObject]:
    path = ROOT / "ops/registry/workflow-runs.json"
    if not path.exists():
        return []
    payload = read_json(path)
    records = payload.get("workflow_runs", [])
    if not isinstance(records, list):
        return []
    return [
        record
        for record in records
        if isinstance(record, dict) and record.get("session_id") == session_id
    ]


def workflow_run_lines(session_id: str) -> list[str]:
    runs = workflow_runs_for_session(session_id)
    if not runs:
        return ["None"]
    return [render_run_line(run) for run in runs]


def render_handoff(
    session_id: str,
    project_id: str,
    repo_id: str,
    workstream_id: str,
    workstream: JsonObject,
    session_ids: list[str],
    events: list[JsonObject],
    next_action: str,
) -> str:
    summaries = [event_summary(event) for event in events]
    objective = workstream.get("objective", "not recorded")
    status = workstream.get("status", "not recorded")
    session_count = len(session_ids)

    return "\n".join(
        [
            "# Latest Control Repo Handoff",
            "",
            f"Session: {session_id}",
            f"Project: {project_id}",
            f"Workstream: {workstream_id}",
            "",
            "## What Changed",
            "",
            markdown_bullets(summaries),
            "",
            "## Current State",
            "",
            f"- Workstream status: {status}",
            f"- Workstream objective: {objective}",
            f"- Repo: {repo_id}",
            f"- Registered sessions: {session_count}",
            "",
            "## Workflow Runs",
            "",
            markdown_bullets(workflow_run_lines(session_id)),
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write the latest control tracker handoff.")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--next-action", required=True)
    return parser.parse_args()


def write_handoff(args: argparse.Namespace) -> Path:
    clean = clean_args(args)
    session_path = find_session_path(clean.session_id)
    events = read_session_events(session_path)
    started = session_started_event(events, clean.session_id)

    projects_by_id = records_by_id(read_json(ROOT / "ops/registry/projects.json"), "projects", "projects")
    repos_by_id = records_by_id(read_json(ROOT / "ops/registry/repos.json"), "repos", "repos")

    project_id = str(started["project_id"])
    repo_id = str(started["repo_id"])
    workstream_id = str(started["workstream_id"])
    lock_path = acquire_workstream_registry_lock()
    try:
        workstreams_path = ROOT / "ops/registry/workstreams.json"
        workstreams_payload = read_json(workstreams_path)
        workstreams_by_id = records_by_id(
            workstreams_payload,
            "workstreams",
            "workstreams",
        )
        workstream = validate_registry_links(
            project_id,
            repo_id,
            workstream_id,
            projects_by_id,
            repos_by_id,
            workstreams_by_id,
        )
        session_ids = require_registered_session(
            workstream,
            workstream_id,
            clean.session_id,
        )
        updated_workstreams_payload, updated_workstream = update_workstream_next_action(
            workstreams_payload,
            workstream_id,
            clean.next_action,
        )
        write_json(workstreams_path, updated_workstreams_payload)

        handoff_path = ROOT / "ops/handoffs/latest.md"
        write_text(
            handoff_path,
            render_handoff(
                clean.session_id,
                project_id,
                repo_id,
                workstream_id,
                updated_workstream,
                session_ids,
                events,
                clean.next_action,
            ),
        )
        return handoff_path
    finally:
        release_workstream_registry_lock(lock_path)


def main() -> int:
    try:
        handoff_path = write_handoff(parse_args())
    except (OSError, ValueError) as exc:
        print(f"tracker_session_handoff: {exc}", file=sys.stderr)
        return 1

    print(display_path(handoff_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
