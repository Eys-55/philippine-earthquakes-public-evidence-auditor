#!/usr/bin/env python3
"""Record a Workflow Run checkpoint."""

from __future__ import annotations

import argparse
from datetime import datetime
import sys

from tracker_workflow_lib import ROOT
from tracker_workflow_lib import WORKFLOW_RUN_STATUSES
from tracker_workflow_lib import append_jsonl
from tracker_workflow_lib import load_workflow_registry
from tracker_workflow_lib import required_clean_value
from tracker_workflow_lib import required_values
from tracker_workflow_lib import update_workflow_run
from tracker_workflow_lib import workflow_run_by_id
from tracker_workflow_lib import write_workflow_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a Workflow Run checkpoint.")
    parser.add_argument("--workflow-run-id", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--current-skill")
    parser.add_argument("--status", choices=sorted(WORKFLOW_RUN_STATUSES))
    parser.add_argument("--artifact", action="append")
    parser.add_argument("--owned-path", action="append")
    parser.add_argument("--validation-command", action="append")
    parser.add_argument("--blocker")
    parser.add_argument("--waiting-reason")
    parser.add_argument("--decision")
    return parser.parse_args()


def checkpoint_workflow_run(args: argparse.Namespace) -> str:
    workflow_run_id = required_clean_value(args.workflow_run_id, "workflow_run_id")
    summary = required_clean_value(args.summary, "summary")
    next_action = required_clean_value(args.next_action, "next_action")
    registry = load_workflow_registry(ROOT)
    run = workflow_run_by_id(workflow_run_id, registry, ROOT)
    now = datetime.now().astimezone().replace(microsecond=0)

    status = args.status or run.get("status", "open")
    if status == "blocked" and not args.blocker:
        raise ValueError("blocked checkpoints require --blocker")
    if status == "waiting_on_user" and not args.waiting_reason:
        raise ValueError("waiting_on_user checkpoints require --waiting-reason")
    if status == "abandoned" and not args.decision:
        raise ValueError("abandoned checkpoints require --decision")

    updates = {
        "status": status,
        "last_checkpoint_at": now.isoformat(),
        "next_action": next_action,
    }
    current_skill = args.current_skill
    if current_skill:
        updates["current_skill"] = required_clean_value(current_skill, "current_skill")
    if args.owned_path:
        updates["owned_paths"] = required_values(args.owned_path, "owned_paths")
    if args.validation_command:
        updates["validation_commands"] = required_values(
            args.validation_command,
            "validation_commands",
        )
    if args.artifact:
        updates["artifacts"] = required_values(args.artifact, "artifacts")
    if args.blocker:
        updates["blocker"] = required_clean_value(args.blocker, "blocker")
    if args.waiting_reason:
        updates["waiting_reason"] = required_clean_value(args.waiting_reason, "waiting_reason")
    if args.decision:
        updates["decision"] = required_clean_value(args.decision, "decision")

    updated_registry, updated_run = update_workflow_run(registry, workflow_run_id, updates)
    event = {
        "event_type": "checkpoint",
        "timestamp": now.isoformat(),
        "workflow_run_id": workflow_run_id,
        "summary": summary,
        "next_action": next_action,
        "status": status,
    }
    for key in (
        "current_skill",
        "owned_paths",
        "validation_commands",
        "artifacts",
        "blocker",
        "waiting_reason",
        "decision",
    ):
        if key in updates:
            event[key] = updates[key]

    append_jsonl(ROOT / str(updated_run["log_path"]), event)
    write_workflow_registry(updated_registry, ROOT)
    return workflow_run_id


def main() -> int:
    try:
        workflow_run_id = checkpoint_workflow_run(parse_args())
    except (OSError, ValueError) as exc:
        print(f"tracker_workflow_checkpoint: {exc}", file=sys.stderr)
        return 1

    print(workflow_run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
