#!/usr/bin/env python3
"""Append a control tracker event and update project status."""

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


ROOT = Path(__file__).resolve().parents[1]
JsonObject = dict[str, Any]


def read_json(path: Path) -> JsonObject:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {path.relative_to(ROOT).as_posix()}") from exc
    except json.JSONDecodeError as exc:
        label = path.relative_to(ROOT).as_posix()
        raise ValueError(f"{label}: invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        label = path.relative_to(ROOT).as_posix()
        raise ValueError(f"{label}: top-level JSON must be an object")
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


def append_jsonl(path: Path, payload: JsonObject) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    fsync_directory(path.parent)


def write_json(path: Path, payload: JsonObject) -> None:
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


def existing_event_ids(events_dir: Path) -> set[str]:
    if not events_dir.exists():
        return set()

    event_ids: set[str] = set()
    for path in sorted(events_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(payload, dict):
                    continue
                for key in ("event_id", "id"):
                    event_id = payload.get(key)
                    if isinstance(event_id, str) and event_id:
                        event_ids.add(event_id)
    return event_ids


def short_suffix(length: int = 4) -> str:
    return secrets.token_hex(max(1, length // 2))[:length]


def generate_event_id(now: datetime, event_ids: set[str]) -> str:
    base_event_id = f"evt-{now:%Y%m%d-%H%M%S}"
    for _ in range(20):
        candidate = f"{base_event_id}-{short_suffix()}"
        if candidate not in event_ids:
            return candidate
    raise ValueError(f"could not generate unique event id for {base_event_id}")


def required_clean_value(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} must not be empty or whitespace")
    return cleaned


def clean_args(args: argparse.Namespace) -> argparse.Namespace:
    # Session ids are free-form until Task 6 adds the session registry.
    return argparse.Namespace(
        project_id=required_clean_value(args.project_id, "project_id"),
        repo_id=required_clean_value(args.repo_id, "repo_id"),
        workstream_id=required_clean_value(args.workstream_id, "workstream_id"),
        session_id=required_clean_value(args.session_id, "session_id"),
        actor=required_clean_value(args.actor, "actor"),
        summary=required_clean_value(args.summary, "summary"),
        next_action=required_clean_value(args.next_action, "next_action"),
    )


def update_project_last_event(
    projects_payload: JsonObject,
    project_id: str,
    event_id: str,
) -> JsonObject:
    projects = projects_payload.get("projects")
    if not isinstance(projects, list):
        raise ValueError("projects registry missing projects array")

    updated_projects: list[object] = []
    project_found = False
    for project in projects:
        if not isinstance(project, dict):
            updated_projects.append(project)
            continue
        if project.get("id") != project_id:
            updated_projects.append(project)
            continue

        updated_project = dict(project)
        updated_project["last_event_id"] = event_id
        updated_projects.append(updated_project)
        project_found = True

    if not project_found:
        raise ValueError(f"unknown project_id {project_id}")

    updated_payload = dict(projects_payload)
    updated_payload["projects"] = updated_projects
    return updated_payload


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
    project_repos = project.get("repos", [])
    if isinstance(project_repos, list) and repo_id not in project_repos:
        raise ValueError(f"project_id {project_id} does not list repo_id {repo_id}")

    project_workstreams = project.get("workstreams", [])
    if isinstance(project_workstreams, list) and workstream_id not in project_workstreams:
        raise ValueError(
            f"project_id {project_id} does not list workstream_id {workstream_id}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append an event to the control tracker.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--workstream-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--next-action", required=True)
    return parser.parse_args()


def log_event(args: argparse.Namespace) -> str:
    clean = clean_args(args)
    projects_path = ROOT / "ops/registry/projects.json"
    projects_payload = read_json(projects_path)
    repos_payload = read_json(ROOT / "ops/registry/repos.json")
    workstreams_payload = read_json(ROOT / "ops/registry/workstreams.json")

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
    event_id = generate_event_id(now, existing_event_ids(ROOT / "ops/events"))
    event = {
        "event_id": event_id,
        "timestamp": now.isoformat(),
        "project_id": clean.project_id,
        "repo_id": clean.repo_id,
        "workstream_id": clean.workstream_id,
        "session_id": clean.session_id,
        "actor": clean.actor,
        "summary": clean.summary,
        "next_action": clean.next_action,
        "evidence": [],
    }

    append_jsonl(ROOT / f"ops/events/{now:%Y-%m-%d}.jsonl", event)
    write_json(
        projects_path,
        update_project_last_event(projects_payload, clean.project_id, event_id),
    )
    return event_id


def main() -> int:
    try:
        event_id = log_event(parse_args())
    except ValueError as exc:
        print(f"tracker_log_event: {exc}", file=sys.stderr)
        return 1

    print(event_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
