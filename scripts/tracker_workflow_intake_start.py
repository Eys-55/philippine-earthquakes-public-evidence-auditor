#!/usr/bin/env python3
"""Start tracker-backed workflow intake from the slash compatibility surface."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any

import tracker_session_start
from tracker_workflow_lib import ROOT
from tracker_workflow_lib import append_jsonl
from tracker_workflow_lib import find_project
from tracker_workflow_lib import find_workstream_for_project
from tracker_workflow_lib import generate_workflow_run_id
from tracker_workflow_lib import load_workflow_registry
from tracker_workflow_lib import log_path_for
from tracker_workflow_lib import repo_relative
from tracker_workflow_lib import required_clean_value
from tracker_workflow_lib import write_workflow_registry
from workflow_skill_slash_surface import build_intake_result
from workflow_skill_slash_surface import slugify


JsonObject = dict[str, Any]
BUG_TERMS = ("bug", "broken", "fail", "fails", "failing", "issue", "problem", "wrong")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--raw-report", required=True)
    parser.add_argument("--project-id", default="agent-workflow-project-maker")
    parser.add_argument("--affected-workflow")
    parser.add_argument("--new-workflow-slug")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def session_id_from_path(session_path: Path) -> str:
    stem = session_path.stem
    if not stem.startswith("session-"):
        raise ValueError(f"could not parse session id from {session_path}")
    return stem.removeprefix("session-")


def select_flow_id(*, raw_report: str, affected_workflow: str | None, new_workflow_slug: str | None) -> str:
    if new_workflow_slug:
        return "agent_workflow_project_maker"
    lowered = raw_report.lower()
    if affected_workflow or any(term in lowered for term in BUG_TERMS):
        return "workflow_specific_bug"
    return "agent_workflow_project_maker"


def owned_paths_for(
    *,
    context_manifest_path: str,
    affected_workflow: str | None,
    new_workflow_slug: str | None,
) -> list[str]:
    paths = [
        context_manifest_path,
        "ops/registry/workflow-runs.json",
        "ops/registry/workstreams.json",
    ]
    if new_workflow_slug:
        slug = slugify(new_workflow_slug)
        paths.extend(
            [
                f"skills/{slug}",
                f"data/{slug}",
                f"docs/status",
            ]
        )
    elif affected_workflow:
        slug = slugify(affected_workflow)
        paths.extend(
            [
                f"skills/{slug}",
                f"data/{slug}",
                f"docs/status",
            ]
        )
    else:
        paths.append("skills/agent-workflow-project-maker/SKILL.md")
    return list(dict.fromkeys(paths))


def manifest_text(intake: JsonObject) -> str:
    proof = intake["visible_ecc_proof"]
    ecc_files = "\n".join(f"- `{path}`" for path in proof["ecc_files_loaded"])
    workflow_files = "\n".join(
        f"- `{path}`" for path in proof["workflow_context_files_loaded"]
    )
    concepts = proof["ecc_concepts_loaded"]
    if concepts:
        concept_lines = "\n".join(
            f"- `{concept['id']}`: {concept['meaning']}" for concept in concepts
        )
    else:
        concept_lines = "- Not detected in the raw report."

    return "\n".join(
        [
            f"# Context Manifest: {intake['workflow_run_id']}",
            "",
            "## Raw User Report",
            "",
            intake["raw_user_report"],
            "",
            "## Project And Workflow",
            "",
            f"- Project: `{intake['project_id']}`",
            f"- Workflow: `{intake['affected_workflow']}`",
            f"- Workflow run: `{intake['workflow_run_id']}`",
            f"- Session: `{intake['session_id']}`",
            f"- Flow ID: `{intake['flow_id']}`",
            f"- Current skill: `{intake['current_skill']}`",
            "",
            "## Loaded ECC Context",
            "",
            ecc_files,
            "",
            "## Loaded Workflow Context",
            "",
            workflow_files,
            "",
            "## ECC Concepts Loaded",
            "",
            concept_lines,
            "",
            "## Premise Lock",
            "",
            proof["premise"],
            "",
            "## First Context-Aware Question",
            "",
            proof["first_context_aware_question"],
            "",
        ]
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def start_session(project_id: str, objective: str) -> str:
    workstream = find_workstream_for_project(project_id, ROOT)
    repo_id = workstream.get("repo_id")
    workstream_id = workstream.get("id")
    if not isinstance(repo_id, str) or not repo_id:
        raise ValueError(f"project_id {project_id} has no repo_id")
    if not isinstance(workstream_id, str) or not workstream_id:
        raise ValueError(f"project_id {project_id} has no workstream_id")

    session_path = tracker_session_start.start_session(
        argparse.Namespace(
            project_id=project_id,
            repo_id=repo_id,
            workstream_id=workstream_id,
            objective=objective,
        )
    )
    return session_id_from_path(session_path)


def start_workflow_intake(args: argparse.Namespace) -> JsonObject:
    objective = required_clean_value(args.objective, "objective")
    raw_report = required_clean_value(args.raw_report, "raw_report")
    project_id = required_clean_value(args.project_id, "project_id")
    affected_workflow = args.affected_workflow.strip() if args.affected_workflow else None
    new_workflow_slug = args.new_workflow_slug.strip() if args.new_workflow_slug else None

    find_project(project_id, ROOT)
    session_id = start_session(project_id, objective)

    now = datetime.now().astimezone().replace(microsecond=0)
    registry = load_workflow_registry(ROOT)
    workflow_run_id = generate_workflow_run_id(now, registry, ROOT)
    flow_id = select_flow_id(
        raw_report=raw_report,
        affected_workflow=affected_workflow,
        new_workflow_slug=new_workflow_slug,
    )
    intake_workflow = new_workflow_slug or affected_workflow
    intake = build_intake_result(
        raw_report=raw_report,
        workflow_run_id=workflow_run_id,
        session_id=session_id,
        project_id=project_id,
        affected_workflow=intake_workflow,
        run_date=now.date().isoformat(),
    )
    intake["flow_id"] = flow_id
    intake["rough_title"] = f"Workflow intake: {objective[:72]}"

    manifest_path = ROOT / str(intake["context_manifest_path"])
    manifest = manifest_text(intake)
    write_text(manifest_path, manifest)

    log_path = log_path_for(workflow_run_id, now, ROOT)
    owned_paths = owned_paths_for(
        context_manifest_path=str(intake["context_manifest_path"]),
        affected_workflow=affected_workflow,
        new_workflow_slug=new_workflow_slug,
    )
    validation_commands = [
        "python3 scripts/validate_tracker.py",
        "python3 scripts/tracker_status.py",
        "python3 scripts/tracker_upload_gate.py",
    ]
    run = {
        "id": workflow_run_id,
        "project_id": project_id,
        "session_id": session_id,
        "title": f"Workflow intake: {objective}",
        "flow_id": flow_id,
        "status": "open",
        "current_skill": "workflow_intake",
        "owned_paths": owned_paths,
        "validation_commands": validation_commands,
        "started_at": now.isoformat(),
        "last_checkpoint_at": now.isoformat(),
        "next_action": "Show ECC proof and ask the first context-aware grilling question.",
        "log_path": repo_relative(log_path, ROOT),
        "context_manifest_path": str(intake["context_manifest_path"]),
    }
    event = {
        "event_type": "workflow_started",
        "timestamp": now.isoformat(),
        "workflow_run_id": workflow_run_id,
        "project_id": project_id,
        "session_id": session_id,
        "title": run["title"],
        "flow_id": flow_id,
        "current_skill": "workflow_intake",
        "owned_paths": owned_paths,
        "validation_commands": validation_commands,
        "context_manifest_path": str(intake["context_manifest_path"]),
        "visible_ecc_proof": intake["visible_ecc_proof"],
        "next_action": run["next_action"],
    }

    append_jsonl(log_path, event)
    updated_registry = dict(registry)
    updated_registry["workflow_runs"] = [*registry.get("workflow_runs", []), run]
    write_workflow_registry(updated_registry, ROOT)

    return {
        "session_id": session_id,
        "workflow_run_id": workflow_run_id,
        "context_manifest_path": str(intake["context_manifest_path"]),
        "current_skill": "workflow_intake",
        "flow_id": flow_id,
        "loaded_files": intake["loaded_files"],
        "visible_ecc_proof": intake["visible_ecc_proof"],
        "manifest_preview": manifest,
        "next_command": (
            "python3 scripts/tracker_workflow_checkpoint.py "
            f"--workflow-run-id {workflow_run_id} --summary <summary> "
            "--next-action <next-action>"
        ),
    }


def main() -> int:
    args = parse_args()
    try:
        payload = start_workflow_intake(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"tracker_workflow_intake_start: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"session_id: {payload['session_id']}")
        print(f"workflow_run_id: {payload['workflow_run_id']}")
        print(f"context_manifest_path: {payload['context_manifest_path']}")
        print(f"current_skill: {payload['current_skill']}")
        print(f"flow_id: {payload['flow_id']}")
        print("loaded_files:")
        for path in payload["loaded_files"]:
            print(f"- {path}")
        proof = payload["visible_ecc_proof"]
        print(f"premise_lock: {proof['premise']}")
        print(f"first_context_aware_question: {proof['first_context_aware_question']}")
        print(f"next_command: {payload['next_command']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
