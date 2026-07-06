#!/usr/bin/env python3
"""Report active Workflow Runs and parallel risk for a project."""

from __future__ import annotations

import argparse
from datetime import datetime
import sys

from tracker_workflow_lib import ROOT
from tracker_workflow_lib import append_jsonl
from tracker_workflow_lib import find_project
from tracker_workflow_lib import load_workflow_registry
from tracker_workflow_lib import render_run_line
from tracker_workflow_lib import required_clean_value
from tracker_workflow_lib import required_values
from tracker_workflow_lib import risky_parallel_runs
from tracker_workflow_lib import update_workflow_run
from tracker_workflow_lib import workflow_runs
from tracker_workflow_lib import write_workflow_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report project Workflow Run situation.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--owned-path", action="append")
    parser.add_argument("--workflow-run-id")
    parser.add_argument("--approve-parallel", action="store_true")
    return parser.parse_args()


def project_runs(project_id: str) -> list[dict[str, object]]:
    registry = load_workflow_registry(ROOT)
    return [run for run in workflow_runs(registry) if run.get("project_id") == project_id]


def record_parallel_approval(workflow_run_id: str, risky_ids: list[str]) -> None:
    registry = load_workflow_registry(ROOT)
    now = datetime.now().astimezone().replace(microsecond=0)
    updated_registry, updated_run = update_workflow_run(
        registry,
        workflow_run_id,
        {
            "parallel_approved_by_user": True,
            "parallel_approved_at": now.isoformat(),
            "parallel_risk_run_ids": risky_ids,
        },
    )
    append_jsonl(
        ROOT / str(updated_run["log_path"]),
        {
            "event_type": "parallel_assessment",
            "timestamp": now.isoformat(),
            "workflow_run_id": workflow_run_id,
            "risk": "approved",
            "risky_workflow_run_ids": risky_ids,
        },
    )
    write_workflow_registry(updated_registry, ROOT)


def main() -> int:
    args = parse_args()
    try:
        project_id = required_clean_value(args.project_id, "project_id")
        find_project(project_id, ROOT)
        proposed_paths = required_values(args.owned_path, "owned_paths") if args.owned_path else []
        risky = (
            risky_parallel_runs(
                project_id=project_id,
                owned_paths=proposed_paths,
                exclude_workflow_run_id=args.workflow_run_id,
                root=ROOT,
            )
            if proposed_paths
            else []
        )
    except (OSError, ValueError) as exc:
        print(f"tracker_project_situation: {exc}", file=sys.stderr)
        return 1

    print(f"# Project Situation: {project_id}")
    print()
    runs = project_runs(project_id)
    if not runs:
        print("- No Workflow Runs recorded for this project.")
    else:
        for run in runs:
            print(f"- {render_run_line(run)}")

    print()
    if proposed_paths:
        if risky:
            risky_ids = [str(run.get("id", "unknown")) for run in risky]
            print("## Parallel Work Assessment")
            print("- Result: risky")
            print(f"- Overlapping Workflow Runs: {', '.join(risky_ids)}")
            if args.approve_parallel:
                if args.workflow_run_id:
                    record_parallel_approval(args.workflow_run_id, risky_ids)
                print("- User approval: recorded")
                return 0
            print("- User approval: required before proceeding")
            return 2
        print("## Parallel Work Assessment")
        print("- Result: safe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
