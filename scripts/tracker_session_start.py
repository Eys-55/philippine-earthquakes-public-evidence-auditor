#!/usr/bin/env python3
"""Start a control tracker session and register it on a workstream."""

from __future__ import annotations

import argparse
from datetime import datetime
import errno
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
from typing import Any


ROOT = Path(os.environ.get("TRACKER_ROOT", Path(__file__).resolve().parents[1])).resolve()
SESSION_START_LOCK_PATH = ROOT / "ops/sessions/.session-start.lock"
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


def string_list(record: JsonObject, key: str, owner_id: str) -> list[str]:
    values = record.get(key, [])
    if not isinstance(values, list):
        raise ValueError(f"{owner_id}: {key} must be a list")

    strings: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            raise ValueError(f"{owner_id}: {key} entries must be non-empty strings")
        strings.append(value)
    return strings


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


def acquire_session_start_lock() -> Path:
    ensure_directory(SESSION_START_LOCK_PATH.parent)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(SESSION_START_LOCK_PATH, flags, 0o600)
    except FileExistsError as exc:
        raise ValueError(
            f"session start lock exists at {display_path(SESSION_START_LOCK_PATH)}; "
            "another session start may be running"
        ) from exc

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
            handle.flush()
            os.fsync(handle.fileno())
        fsync_directory(SESSION_START_LOCK_PATH.parent)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        SESSION_START_LOCK_PATH.unlink(missing_ok=True)
        fsync_directory(SESSION_START_LOCK_PATH.parent)
        raise

    return SESSION_START_LOCK_PATH


def release_session_start_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
        fsync_directory(lock_path.parent)
    except FileNotFoundError:
        return


def append_jsonl(path: Path, payload: JsonObject) -> None:
    ensure_directory(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    fsync_directory(path.parent)


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


def required_clean_value(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} must not be empty or whitespace")
    return cleaned


def clean_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        project_id=required_clean_value(args.project_id, "project_id"),
        repo_id=required_clean_value(args.repo_id, "repo_id"),
        workstream_id=required_clean_value(args.workstream_id, "workstream_id"),
        objective=required_clean_value(args.objective, "objective"),
    )


def existing_session_ids(workstreams_payload: JsonObject) -> set[str]:
    session_ids: set[str] = set()
    workstreams = workstreams_payload.get("workstreams")
    if not isinstance(workstreams, list):
        raise ValueError("workstreams registry missing workstreams array")

    for workstream in workstreams:
        if not isinstance(workstream, dict):
            raise ValueError("workstreams registry contains a non-object record")
        workstream_id = workstream.get("id")
        if not isinstance(workstream_id, str) or not workstream_id:
            raise ValueError("workstreams registry contains a record without an id")
        for session_id in string_list(workstream, "session_ids", workstream_id):
            if session_id in session_ids:
                raise ValueError(f"workstreams registry contains duplicate session id {session_id}")
            session_ids.add(session_id)
    return session_ids


def validate_ids(
    project_id: str,
    repo_id: str,
    workstream_id: str,
    projects_by_id: dict[str, JsonObject],
    repos_by_id: dict[str, JsonObject],
    workstreams_by_id: dict[str, JsonObject],
) -> None:
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

    project = projects_by_id[project_id]
    if repo_id not in string_list(project, "repos", project_id):
        raise ValueError(f"project_id {project_id} does not list repo_id {repo_id}")
    if workstream_id not in string_list(project, "workstreams", project_id):
        raise ValueError(
            f"project_id {project_id} does not list workstream_id {workstream_id}"
        )


def generate_session_id(now: datetime, existing_ids: set[str]) -> str:
    base_session_id = f"{now:%Y%m%d-%H%M%S}"
    for _ in range(20):
        candidate = f"{base_session_id}-{secrets.token_hex(2)}"
        session_path = ROOT / f"ops/sessions/{now:%Y-%m-%d}/session-{candidate}.jsonl"
        if candidate not in existing_ids and not session_path.exists():
            return candidate
    raise ValueError(f"could not generate unique session id for {base_session_id}")


def add_session_to_workstream(
    workstreams_payload: JsonObject,
    workstream_id: str,
    session_id: str,
) -> JsonObject:
    workstreams = workstreams_payload.get("workstreams")
    if not isinstance(workstreams, list):
        raise ValueError("workstreams registry missing workstreams array")

    updated_workstreams: list[object] = []
    found = False
    for workstream in workstreams:
        if not isinstance(workstream, dict):
            raise ValueError("workstreams registry contains a non-object record")
        if workstream.get("id") != workstream_id:
            updated_workstreams.append(workstream)
            continue

        session_ids = string_list(workstream, "session_ids", workstream_id)
        if session_id in session_ids:
            raise ValueError(f"session id {session_id} is already registered")

        updated_workstream = dict(workstream)
        updated_workstream["session_ids"] = [*session_ids, session_id]
        updated_workstreams.append(updated_workstream)
        found = True

    if not found:
        raise ValueError(f"unknown workstream_id {workstream_id}")

    updated_payload = dict(workstreams_payload)
    updated_payload["workstreams"] = updated_workstreams
    return updated_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start a control tracker session.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--workstream-id", required=True)
    parser.add_argument("--objective", required=True)
    return parser.parse_args()


def start_session(args: argparse.Namespace) -> Path:
    clean = clean_args(args)
    lock_path = acquire_session_start_lock()
    session_path: Path | None = None
    session_id: str | None = None
    try:
        projects_payload = read_json(ROOT / "ops/registry/projects.json")
        repos_payload = read_json(ROOT / "ops/registry/repos.json")
        workstreams_path = ROOT / "ops/registry/workstreams.json"
        workstreams_payload = read_json(workstreams_path)

        projects_by_id = records_by_id(projects_payload, "projects", "projects")
        repos_by_id = records_by_id(repos_payload, "repos", "repos")
        workstreams_by_id = records_by_id(workstreams_payload, "workstreams", "workstreams")
        validate_ids(
            clean.project_id,
            clean.repo_id,
            clean.workstream_id,
            projects_by_id,
            repos_by_id,
            workstreams_by_id,
        )

        now = datetime.now().astimezone().replace(microsecond=0)
        session_id = generate_session_id(now, existing_session_ids(workstreams_payload))
        session_path = ROOT / f"ops/sessions/{now:%Y-%m-%d}/session-{session_id}.jsonl"
        event = {
            "event_type": "session_started",
            "timestamp": now.isoformat(),
            "session_id": session_id,
            "project_id": clean.project_id,
            "repo_id": clean.repo_id,
            "workstream_id": clean.workstream_id,
            "objective": clean.objective,
            "summary": f"Started session with objective: {clean.objective}",
        }

        append_jsonl(session_path, event)
        try:
            write_json(
                workstreams_path,
                add_session_to_workstream(
                    workstreams_payload,
                    clean.workstream_id,
                    session_id,
                ),
            )
        except Exception as exc:
            append_jsonl(
                session_path,
                {
                    "event_type": "session_error",
                    "timestamp": datetime.now().astimezone().replace(microsecond=0).isoformat(),
                    "session_id": session_id,
                    "project_id": clean.project_id,
                    "repo_id": clean.repo_id,
                    "workstream_id": clean.workstream_id,
                    "summary": (
                        "Session start failed after session log creation while updating "
                        f"workstreams registry: {exc}"
                    ),
                },
            )
            raise ValueError(
                f"created {display_path(session_path)} but failed to update "
                f"{display_path(workstreams_path)}: {exc}"
            ) from exc
        return session_path
    finally:
        release_session_start_lock(lock_path)


def main() -> int:
    try:
        session_path = start_session(parse_args())
    except (OSError, ValueError) as exc:
        print(f"tracker_session_start: {exc}", file=sys.stderr)
        return 1

    print(display_path(session_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
