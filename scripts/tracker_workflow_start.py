#!/usr/bin/env python3
"""Start a Workflow Run and append its first event."""

from __future__ import annotations

import argparse
from datetime import datetime
import sys

from tracker_workflow_lib import ROOT
from tracker_workflow_lib import append_jsonl
from tracker_workflow_lib import generate_workflow_run_id
from tracker_workflow_lib import load_workflow_registry
from tracker_workflow_lib import log_path_for
from tracker_workflow_lib import repo_relative
from tracker_workflow_lib import required_clean_value
from tracker_workflow_lib import required_values
from tracker_workflow_lib import require_known_session
from tracker_workflow_lib import find_project
from tracker_workflow_lib import write_workflow_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start a Workflow Run.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--flow-id", required=True)
    parser.add_argument("--current-skill", required=True)
    parser.add_argument("--owned-path", action="append", required=True)
    parser.add_argument("--validation-command", action="append", required=True)
    parser.add_argument("--next-action", required=True)
    return parser.parse_args()


def start_workflow_run(args: argparse.Namespace) -> str:
    project_id = required_clean_value(args.project_id, "project_id")
    session_id = required_clean_value(args.session_id, "session_id")
    title = required_clean_value(args.title, "title")
    flow_id = required_clean_value(args.flow_id, "flow_id")
    current_skill = required_clean_value(args.current_skill, "current_skill")
    owned_paths = required_values(args.owned_path, "owned_paths")
    validation_commands = required_values(args.validation_command, "validation_commands")
    next_action = required_clean_value(args.next_action, "next_action")

    find_project(project_id, ROOT)
    require_known_session(session_id, ROOT)

    now = datetime.now().astimezone().replace(microsecond=0)
    registry = load_workflow_registry(ROOT)
    workflow_run_id = generate_workflow_run_id(now, registry, ROOT)
    log_path = log_path_for(workflow_run_id, now, ROOT)
    run = {
        "id": workflow_run_id,
        "project_id": project_id,
        "session_id": session_id,
        "title": title,
        "flow_id": flow_id,
        "status": "open",
        "current_skill": current_skill,
        "owned_paths": owned_paths,
        "validation_commands": validation_commands,
        "started_at": now.isoformat(),
        "last_checkpoint_at": now.isoformat(),
        "next_action": next_action,
        "log_path": repo_relative(log_path, ROOT),
    }
    event = {
        "event_type": "workflow_started",
        "timestamp": now.isoformat(),
        "workflow_run_id": workflow_run_id,
        "project_id": project_id,
        "session_id": session_id,
        "title": title,
        "flow_id": flow_id,
        "current_skill": current_skill,
        "owned_paths": owned_paths,
        "validation_commands": validation_commands,
        "next_action": next_action,
    }

    append_jsonl(log_path, event)
    updated_registry = dict(registry)
    updated_registry["workflow_runs"] = [*registry.get("workflow_runs", []), run]
    write_workflow_registry(updated_registry, ROOT)
    return workflow_run_id


def main() -> int:
    try:
        workflow_run_id = start_workflow_run(parse_args())
    except (OSError, ValueError) as exc:
        print(f"tracker_workflow_start: {exc}", file=sys.stderr)
        return 1

    print(workflow_run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
