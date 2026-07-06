#!/usr/bin/env python3
"""Skills-first workflow router and slash compatibility surface."""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
import sys
from typing import Any


CANONICAL_SKILL = "skills/agent-workflow-project-maker/SKILL.md"
CONTEXT_MANIFEST_TEMPLATE = "ops/workflow-runs/{date}/{workflow_run_id}-context.md"

ECC_BASE_FILES = [
    "AGENTS.md",
    ".agents/skills/ask-matt/SKILL.md",
    ".agents/skills/grilling/SKILL.md",
    ".agents/skills/to-prd/SKILL.md",
    ".agents/skills/to-issues/SKILL.md",
    "skills/control-repo-manager/SKILL.md",
    "CONTEXT.md",
    "docs/adr/0001-track-workflow-runs-as-session-scoped-operations.md",
]

WORKFLOW_CONTEXT_FILES = [
    "skills/agent-workflow-project-maker/SKILL.md",
    "ops/registry/workflow-runs.json",
    "docs/plans/2026-07-06-workflow-run-tracker-prd.md",
    "tests/test_workflow_run_commands.py",
    "tests/test_workflow_skill_slash_surface.py",
]

CONCEPT_DOCS = {
    "loop": {
        "terms": ["loop", "loops"],
        "files": [
            "docs/plans/2026-07-05-building-code-agent-loop.md",
            ".agents/skills/loop-me/SKILL.md",
        ],
        "meaning": (
            "In ECC, a loop has a locked objective, small work units, an eval "
            "gate after each unit, explicit stop conditions, and a handoff."
        ),
    },
    "gate": {
        "terms": ["gate", "gates"],
        "files": [
            "skills/philippines-building-code-evidence-auditor-v2/SKILL.md",
            "docs/plans/2026-07-05-building-code-gates-1-4-ecc-implementation-plan.md",
        ],
        "meaning": (
            "In ECC, a gate owns a narrow objective, input, output, eval, "
            "handoff, human boundary, and safety risks."
        ),
    },
    "handoff": {
        "terms": ["handoff", "handoffs"],
        "files": [
            ".agents/skills/ask-matt/SKILL.md",
            "skills/control-repo-manager/SKILL.md",
        ],
        "meaning": (
            "In ECC, a handoff preserves what happened, what is safe to assume, "
            "and the next action for another session or operator."
        ),
    },
    "eval": {
        "terms": ["eval", "evals", "validation", "validator", "validators"],
        "files": [
            "AGENTS.md",
            "docs/plans/2026-07-06-workflow-run-tracker-prd.md",
        ],
        "meaning": (
            "In ECC, validation is a pass/fail gate that proves an output is "
            "usable before it is treated as complete."
        ),
    },
    "lane": {
        "terms": ["lane", "lanes"],
        "files": [
            "AGENTS.md",
            "skills/philippines-building-code-evidence-auditor-v2/SKILL.md",
        ],
        "meaning": (
            "In ECC, lanes split independent source or agent work while keeping "
            "integration and boundaries explicit."
        ),
    },
    "human_boundary": {
        "terms": ["human boundary", "human-boundary", "human in the loop", "hitl"],
        "files": [
            "AGENTS.md",
            "skills/philippines-building-code-evidence-auditor-v2/SKILL.md",
        ],
        "meaning": (
            "In ECC, the human boundary names what the user must confirm or "
            "decide before the workflow can safely continue."
        ),
    },
    "source_evidence": {
        "terms": ["source evidence", "source", "sources", "evidence"],
        "files": [
            "AGENTS.md",
            "skills/philippines-building-code-evidence-auditor-v2/SKILL.md",
        ],
        "meaning": (
            "In ECC, raw evidence and source URLs are preserved separately from "
            "integrated conclusions to prevent overclaiming."
        ),
    },
}

NEW_WORKFLOW_CONFIRMATIONS = {
    "create a new workflow for this",
    "this is not a continuation. start a new workflow.",
    "this is not a continuation start a new workflow",
}


def command_registry() -> list[dict[str, Any]]:
    return [
        {
            "slash": "/tracker workflow",
            "purpose": (
                "Start tracker-backed workflow intake for an operator who is "
                "building or debugging a workflow."
            ),
            "mode": "start",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "none",
        },
        {
            "slash": "/tracker status",
            "purpose": "Alias tracker-backed project and workflow status.",
            "mode": "status",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "none",
        },
        {
            "slash": "/tracker closeout",
            "purpose": "Alias tracker validation, upload safety, and continuation closeout.",
            "mode": "closeout",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "before-external-action",
        },
        {
            "slash": "/workflow-find",
            "purpose": "Find existing workflow surfaces before creating anything new.",
            "mode": "read",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "none",
        },
        {
            "slash": "/workflow-router",
            "purpose": "Route a raw workflow problem through ECC-loaded workflow intake.",
            "mode": "read",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "none",
        },
        {
            "slash": "/workflow-contract",
            "purpose": "Draft or inspect an ECC workflow contract for a workflow idea.",
            "mode": "draft",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "before-file-write",
        },
        {
            "slash": "/workflow-create-skill",
            "purpose": "Create draft workflow scaffold files after explicit confirmation.",
            "mode": "write",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "before-file-write",
        },
        {
            "slash": "/workflow-status",
            "purpose": "Show tracker-backed workflow status and current next actions.",
            "mode": "status",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "none",
        },
        {
            "slash": "/workflow-closeout",
            "purpose": "Check validation, GitHub upload safety, and continuation readiness.",
            "mode": "closeout",
            "canonical_skill": CANONICAL_SKILL,
            "operator_command": True,
            "approval_boundary": "before-external-action",
        },
    ]


def find_command(slash: str) -> dict[str, Any]:
    for command in command_registry():
        if command["slash"] == slash:
            return command
    raise ValueError(f"unknown workflow slash command: {slash}")


def detected_concepts(raw_report: str) -> list[dict[str, Any]]:
    normalized = raw_report.lower()
    matches: list[dict[str, Any]] = []
    for concept_id, concept in CONCEPT_DOCS.items():
        if any(term in normalized for term in concept["terms"]):
            matches.append(
                {
                    "id": concept_id,
                    "files": list(concept["files"]),
                    "meaning": concept["meaning"],
                }
            )
    return matches


def is_new_workflow_confirmation(text: str) -> bool:
    cleaned = re.sub(r"\s+", " ", text.strip().lower())
    return cleaned in NEW_WORKFLOW_CONFIRMATIONS


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return cleaned or "untitled-workflow"


def context_manifest_path(workflow_run_id: str, run_date: str | None = None) -> str:
    return CONTEXT_MANIFEST_TEMPLATE.format(
        date=run_date or date.today().isoformat(),
        workflow_run_id=workflow_run_id,
    )


def build_intake_result(
    *,
    raw_report: str,
    workflow_run_id: str,
    session_id: str,
    project_id: str,
    affected_workflow: str | None = None,
    run_date: str | None = None,
) -> dict[str, Any]:
    report = raw_report.strip()
    if not report:
        raise ValueError("raw_report must not be empty")

    workflow = affected_workflow or "unknown"
    concepts = detected_concepts(report)
    concept_files = sorted({path for concept in concepts for path in concept["files"]})
    loaded_files = [*ECC_BASE_FILES, *WORKFLOW_CONTEXT_FILES, *concept_files]
    premise = (
        f"This appears to be a workflow-specific agentic workflow issue for "
        f"{workflow}; continue through ECC-loaded workflow_intake before grilling."
    )
    first_question = (
        "After loading the ECC and workflow context above, which part of the "
        f"{workflow} workflow is failing against the expected flow?"
    )
    if workflow == "unknown":
        first_question = (
            "After loading tracker and ECC context, which existing workflow or "
            "new workflow should this reported problem attach to?"
        )

    return {
        "flow_id": "workflow_specific_bug",
        "current_skill": "workflow_intake",
        "status": "open",
        "rough_title": f"Investigate workflow issue: {report[:72]}",
        "raw_user_report": report,
        "project_id": project_id,
        "session_id": session_id,
        "workflow_run_id": workflow_run_id,
        "affected_workflow": workflow,
        "context_manifest_path": context_manifest_path(workflow_run_id, run_date),
        "visible_ecc_proof": {
            "ecc_files_loaded": list(ECC_BASE_FILES),
            "workflow_context_files_loaded": [*WORKFLOW_CONTEXT_FILES, *concept_files],
            "ecc_concepts_loaded": concepts,
            "premise": premise,
            "first_context_aware_question": first_question,
        },
        "loaded_files": loaded_files,
        "next_action": "write context manifest, show premise lock, then begin grilling",
    }


def scaffold_plan(
    *,
    workflow_slug: str,
    workflow_run_id: str,
    run_date: str | None = None,
) -> dict[str, Any]:
    slug = slugify(workflow_slug)
    today = run_date or date.today().isoformat()
    not_reached = (
        "Status: Not reached yet. This scaffolded surface exists so the "
        "workflow shape is visible, but it has not been worked through yet."
    )
    base_marker = {
        "status": "draft",
        "progress": "0%",
        "current_phase": "not reached",
        "next_action": "return here when the previous workflow step is complete",
        "not_yet_reached_marker": not_reached,
    }
    files = [
        {
            "path": f"skills/{slug}/SKILL.md",
            **base_marker,
            "purpose": "canonical draft skill entrypoint",
        },
        {
            "path": f"data/{slug}/.gitkeep",
            **base_marker,
            "purpose": "draft data surface placeholder",
        },
        {
            "path": f"docs/status/{today}-{slug}-status.md",
            **base_marker,
            "purpose": "draft status and resume surface",
        },
        {
            "path": context_manifest_path(workflow_run_id, today),
            **base_marker,
            "purpose": "workflow-run context manifest",
        },
    ]
    return {
        "workflow_slug": slug,
        "workflow_run_id": workflow_run_id,
        "files": files,
    }


def closeout_summary(*, upload_status: str) -> dict[str, Any]:
    uploaded = upload_status.strip().lower() == "uploaded"
    return {
        "upload_status": upload_status,
        "continue_safe": uploaded,
        "next_action": (
            "continue from GitHub-backed state"
            if uploaded
            else "stop and push/upload before continuing"
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--intake-report")
    parser.add_argument("--workflow-run-id", default="wfr-draft")
    parser.add_argument("--session-id", default="session-draft")
    parser.add_argument("--project-id", default="agent-workflow-project-maker")
    parser.add_argument("--affected-workflow")
    parser.add_argument("--scaffold-slug")
    parser.add_argument("--upload-status")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command:
            payload: Any = find_command(args.command)
        elif args.intake_report:
            payload = build_intake_result(
                raw_report=args.intake_report,
                workflow_run_id=args.workflow_run_id,
                session_id=args.session_id,
                project_id=args.project_id,
                affected_workflow=args.affected_workflow,
            )
        elif args.scaffold_slug:
            payload = scaffold_plan(
                workflow_slug=args.scaffold_slug,
                workflow_run_id=args.workflow_run_id,
            )
        elif args.upload_status:
            payload = closeout_summary(upload_status=args.upload_status)
        else:
            payload = command_registry()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if isinstance(payload, list):
            for command in payload:
                print(f"{command['slash']}: {command['purpose']}")
        else:
            print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
