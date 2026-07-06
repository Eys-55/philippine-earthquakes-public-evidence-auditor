#!/usr/bin/env python3
"""Generate a daily Markdown rollup for the control repo tracker."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

try:
    from tracker_workflow_lib import render_run_line
except ImportError:  # pragma: no cover - used when imported as scripts.tracker_daily_rollup
    from scripts.tracker_workflow_lib import render_run_line


ROOT = Path(__file__).resolve().parents[1]
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
JsonObject = dict[str, Any]


class RollupError(Exception):
    """Raised for user-fixable rollup input errors."""


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_date(value: str) -> str:
    if not DATE_PATTERN.fullmatch(value):
        raise RollupError(f"invalid --date {value!r}; expected YYYY-MM-DD")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise RollupError(f"invalid --date {value!r}; expected a real YYYY-MM-DD date") from exc
    return value


def read_json_object(path: Path) -> JsonObject:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RollupError(f"missing required file {display_path(path)}") from exc
    except json.JSONDecodeError as exc:
        raise RollupError(f"{display_path(path)}: invalid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise RollupError(f"{display_path(path)}: top-level JSON must be an object")
    return payload


def read_events(path: Path) -> list[JsonObject]:
    events: list[JsonObject] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise RollupError(
                        f"{display_path(path)}:{line_number}: invalid JSONL: {exc.msg}"
                    ) from exc
                if not isinstance(payload, dict):
                    raise RollupError(
                        f"{display_path(path)}:{line_number}: invalid JSONL: entry must be an object"
                    )
                events.append(payload)
    except FileNotFoundError as exc:
        raise RollupError(f"missing required file {display_path(path)}") from exc
    return events


def require_string(record: JsonObject, key: str, source: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise RollupError(f"{source}: missing required non-empty {key}")
    return value


def records_array(payload: JsonObject, key: str, source: str) -> list[JsonObject]:
    records = payload.get(key)
    if not isinstance(records, list):
        raise RollupError(f"{source}: missing required {key} array")

    objects: list[JsonObject] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise RollupError(f"{source}: {key}[{index}] must be an object")
        objects.append(record)
    return objects


def text_items(value: object) -> list[str]:
    if value in (None, False, "", []):
        return []
    if value is True:
        return ["true"]
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    return [str(value)]


def blocked_items(events: list[JsonObject], workstreams: list[JsonObject]) -> list[str]:
    items: list[str] = []
    for event in events:
        event_label = require_string(event, "event_id", "event")
        event_summary = require_string(event, "summary", f"event {event_label}")
        if event.get("status") == "blocked":
            items.append(f"{event_label}: {event_summary}")
        for key in ("blocked", "blocker", "blockers"):
            for item in text_items(event.get(key)):
                if item == "true":
                    items.append(f"{event_label}: {event_summary}")
                else:
                    items.append(f"{event_label}: {item}")

    for workstream in workstreams:
        if workstream.get("status") != "blocked":
            continue
        workstream_id = require_string(workstream, "id", "workstream")
        next_action = require_string(workstream, "next_action", f"workstream {workstream_id}")
        items.append(f"{workstream_id}: {next_action}")
    return items


def public_progress_candidates(events: list[JsonObject]) -> list[str]:
    candidates: list[str] = []
    for event in events:
        event_label = require_string(event, "event_id", "event")
        event_summary = require_string(event, "summary", f"event {event_label}")
        for key in (
            "public_progress_candidate",
            "public_progress_candidates",
            "public_candidate",
            "public_candidates",
        ):
            for item in text_items(event.get(key)):
                if item == "true":
                    candidates.append(f"{event_label}: {event_summary}")
                else:
                    candidates.append(f"{event_label}: {item}")
    return candidates


def upload_status_label(state: JsonObject, generated_at: object) -> str:
    status = state.get("status")
    label = status if isinstance(status, str) and status else "unknown"
    if isinstance(generated_at, str) and generated_at:
        return f"recorded state: {label}; generated_at: {generated_at}"
    return f"recorded state: {label}"


def markdown_list(items: list[str]) -> list[str]:
    if not items:
        return ["- None"]
    return [f"- {item}" for item in items]


def workflow_run_items(workflow_runs_payload: JsonObject) -> list[str]:
    records = workflow_runs_payload.get("workflow_runs", [])
    if not isinstance(records, list):
        return []
    return [render_run_line(record) for record in records if isinstance(record, dict)]


def build_markdown(
    rollup_date: str,
    events: list[JsonObject],
    workstreams: list[JsonObject],
    upload_payload: JsonObject,
    workflow_runs_payload: JsonObject,
) -> str:
    projects_moved: list[str] = []
    for event in events:
        event_id = require_string(event, "event_id", "event")
        project_id = require_string(event, "project_id", f"event {event_id}")
        summary = require_string(event, "summary", f"event {event_id}")
        next_action = require_string(event, "next_action", f"event {event_id}")
        projects_moved.append(f"{project_id}: {summary} Next action: {next_action}")

    upload_repos = upload_payload.get("repos", {})
    if not isinstance(upload_repos, dict):
        raise RollupError("ops/sync/github-upload-state.json: repos must be an object")
    github_uploads: list[str] = []
    upload_generated_at = upload_payload.get("generated_at")
    for repo_id in sorted(upload_repos):
        state = upload_repos[repo_id]
        if not isinstance(state, dict):
            raise RollupError(f"ops/sync/github-upload-state.json: {repo_id} state must be an object")
        github_uploads.append(f"{repo_id}: {upload_status_label(state, upload_generated_at)}")

    next_actions: list[str] = []
    for workstream in workstreams:
        workstream_id = require_string(workstream, "id", "workstream")
        next_action = require_string(workstream, "next_action", f"workstream {workstream_id}")
        next_actions.append(f"{workstream_id}: {next_action}")

    lines = [
        f"# Daily Control Repo Rollup - {rollup_date}",
        "",
        "## Projects Moved",
        "",
        *markdown_list(projects_moved),
        "",
        "## GitHub Uploads",
        "",
        *markdown_list(github_uploads),
        "",
        "## Blocked",
        "",
        *markdown_list(blocked_items(events, workstreams)),
        "",
        "## Workflow Runs",
        "",
        *markdown_list(workflow_run_items(workflow_runs_payload)),
        "",
        "## Public Progress Candidates",
        "",
        *markdown_list(public_progress_candidates(events)),
        "",
        "## Next Actions",
        "",
        *markdown_list(next_actions),
        "",
    ]
    return "\n".join(lines)


def fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temp_path = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temp_path.replace(path)
        fsync_directory(path.parent)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def generate_rollup(rollup_date: str) -> Path:
    events_path = ROOT / "ops" / "events" / f"{rollup_date}.jsonl"
    workstreams_path = ROOT / "ops" / "registry" / "workstreams.json"
    upload_path = ROOT / "ops" / "sync" / "github-upload-state.json"
    workflow_runs_path = ROOT / "ops" / "registry" / "workflow-runs.json"
    output_path = ROOT / "ops" / "daily" / f"{rollup_date}.md"

    events = read_events(events_path)
    workstreams_payload = read_json_object(workstreams_path)
    upload_payload = read_json_object(upload_path)
    workflow_runs_payload = read_json_object(workflow_runs_path)
    workstreams = records_array(workstreams_payload, "workstreams", display_path(workstreams_path))

    markdown = build_markdown(
        rollup_date,
        events,
        workstreams,
        upload_payload,
        workflow_runs_payload,
    )
    atomic_write_text(output_path, markdown)
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="Rollup date in YYYY-MM-DD format.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        rollup_date = parse_date(args.date)
        output_path = generate_rollup(rollup_date)
    except RollupError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {display_path(output_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
