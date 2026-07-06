#!/usr/bin/env python3
"""Friendly wrapper for starting tracked work on a project."""

from __future__ import annotations

import argparse
import sys

import tracker_session_start
from tracker_workflow_lib import ROOT
from tracker_workflow_lib import find_workstream_for_project


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start tracked work for a project.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--repo-id")
    parser.add_argument("--workstream-id")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        workstream = find_workstream_for_project(args.project_id, ROOT)
        repo_id = args.repo_id or workstream.get("repo_id")
        workstream_id = args.workstream_id or workstream.get("id")
        if not isinstance(repo_id, str) or not repo_id:
            raise ValueError(f"project_id {args.project_id} has no repo_id")
        if not isinstance(workstream_id, str) or not workstream_id:
            raise ValueError(f"project_id {args.project_id} has no workstream_id")
        session_path = tracker_session_start.start_session(
            argparse.Namespace(
                project_id=args.project_id,
                repo_id=repo_id,
                workstream_id=workstream_id,
                objective=args.objective,
            )
        )
    except (OSError, ValueError) as exc:
        print(f"tracker_start_work: {exc}", file=sys.stderr)
        return 1

    print(session_path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
