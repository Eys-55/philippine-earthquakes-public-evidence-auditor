#!/usr/bin/env python3
"""Close a Workflow Run with explicit evidence."""

from __future__ import annotations

import argparse
from datetime import datetime
import sys

from tracker_workflow_lib import ROOT
from tracker_workflow_lib import append_jsonl
from tracker_workflow_lib import load_workflow_registry
from tracker_workflow_lib import required_clean_value
from tracker_workflow_lib import required_values
from tracker_workflow_lib import update_workflow_run
from tracker_workflow_lib import workflow_run_by_id
from tracker_workflow_lib import write_workflow_registry


FINAL_STATUSES = {"completed", "handed_off", "blocked", "abandoned"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Close a Workflow Run.")
    parser.add_argument("--workflow-run-id", required=True)
    parser.add_argument("--status", required=True, choices=sorted(FINAL_STATUSES))
    parser.add_argument("--summary", required=True)
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--artifact", action="append")
    parser.add_argument("--validation-result", action="append")
    parser.add_argument("--review-state")
    parser.add_argument("--blocker")
    parser.add_argument("--handoff")
    parser.add_argument("--decision")
    return parser.parse_args()


def close_workflow_run(args: argparse.Namespace) -> str:
    workflow_run_id = required_clean_value(args.workflow_run_id, "workflow_run_id")
    summary = required_clean_value(args.summary, "summary")
    next_action = required_clean_value(args.next_action, "next_action")
    status = required_clean_value(args.status, "status")
    registry = load_workflow_registry(ROOT)
    run = workflow_run_by_id(workflow_run_id, registry, ROOT)
    now = datetime.now().astimezone().replace(microsecond=0)

    if status == "completed":
        artifacts = required_values(args.artifact, "artifacts")
        validation_results = required_values(args.validation_result, "validation_results")
        review_state = required_clean_value(args.review_state or "", "review_state")
    else:
        artifacts = required_values(args.artifact, "artifacts") if args.artifact else []
        validation_results = (
            required_values(args.validation_result, "validation_results")
            if args.validation_result
            else []
        )
        review_state = args.review_state

    if status == "blocked" and not args.blocker:
        raise ValueError("blocked closeout requires --blocker")
    if status == "handed_off" and not args.handoff:
        raise ValueError("handed_off closeout requires --handoff")
    if status == "abandoned" and not args.decision:
        raise ValueError("abandoned closeout requires --decision")

    updates = {
        "status": status,
        "last_checkpoint_at": now.isoformat(),
        "next_action": next_action,
        "final_summary": summary,
        "closed_at": now.isoformat(),
    }
    if artifacts:
        updates["artifacts"] = artifacts
    if validation_results:
        updates["validation_results"] = validation_results
    if review_state:
        updates["review_state"] = review_state
    if args.blocker:
        updates["blocker"] = required_clean_value(args.blocker, "blocker")
    if args.handoff:
        updates["handoff"] = required_clean_value(args.handoff, "handoff")
    if args.decision:
        updates["decision"] = required_clean_value(args.decision, "decision")

    updated_registry, updated_run = update_workflow_run(registry, workflow_run_id, updates)
    event = {
        "event_type": "workflow_closed",
        "timestamp": now.isoformat(),
        "workflow_run_id": workflow_run_id,
        "status": status,
        "summary": summary,
        "next_action": next_action,
    }
    for key in (
        "artifacts",
        "validation_results",
        "review_state",
        "blocker",
        "handoff",
        "decision",
    ):
        if key in updates:
            event[key] = updates[key]

    append_jsonl(ROOT / str(updated_run["log_path"]), event)
    write_workflow_registry(updated_registry, ROOT)
    return workflow_run_id


def main() -> int:
    try:
        workflow_run_id = close_workflow_run(parse_args())
    except (OSError, ValueError) as exc:
        print(f"tracker_workflow_close: {exc}", file=sys.stderr)
        return 1

    print(workflow_run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
