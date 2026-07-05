#!/usr/bin/env python3
"""Prepare, run, and parse the priority workflow catalog CLI batch."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "agentic-repos" / "workflow-door-catalog.json"
RUN_DIR = ROOT / "data" / "agentic-repos" / "workflow-catalog-runs" / "2026-07-05-priority1-cli-10x5"
CHUNKS_DIR = RUN_DIR / "chunks"
OUTPUTS_DIR = RUN_DIR / "outputs"
PROMPTS_DIR = RUN_DIR / "prompts"
LOGS_DIR = RUN_DIR / "logs"
SCHEMA_PATH = RUN_DIR / "classification-output.schema.json"
MANIFEST_PATH = RUN_DIR / "manifest.json"
PROGRESS_PATH = RUN_DIR / "progress.json"
RAW_PATH = RUN_DIR / "workflow-classifications.raw.json"
FINAL_PATH = RUN_DIR / "workflow-classifications.json"
REPORT_PATH = RUN_DIR / "report.md"

FIELDS = [
    "workflow_id",
    "workflow_name",
    "source_repo",
    "source_url",
    "source_url_status",
    "canonical_source_url",
    "evidence_basis",
    "domain",
    "workflow_type",
    "real_life_job",
    "input_contract",
    "output_artifact",
    "trigger",
    "tools_or_sources",
    "validation_gate",
    "human_review_boundary",
    "safety_boundary",
    "codex_package_relevance",
    "what_to_copy",
    "what_to_ignore",
    "tags",
    "confidence",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_catalog() -> list[dict[str, Any]]:
    payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return payload["rows"]


def chunked(rows: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [rows[index : index + size] for index in range(0, len(rows), size)]


def compact_door(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "door": row["door"],
        "repo": row["repo"],
        "source_url": row["source_url"],
        "primary_category": row["primary_category"],
        "primary_domain": row["primary_domain"],
        "primary_pattern": row["primary_pattern"],
        "fit": row["fit"],
        "browse_use": row["browse_use"],
        "input_contract_hint": row["input_contract_hint"],
        "output_artifact_hint": row["output_artifact_hint"],
        "human_review_boundary": row["human_review_boundary"],
        "safety_boundary": row["safety_boundary"],
    }


def write_schema() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["agent_id", "rows", "quality_note"],
        "properties": {
            "agent_id": {"type": "string"},
            "quality_note": {"type": "string"},
            "rows": {
                "type": "array",
                "minItems": 1,
                "maxItems": 5,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": FIELDS,
                    "properties": {
                        field: {"type": "string"} for field in FIELDS
                    },
                },
            },
        },
    }
    SCHEMA_PATH.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")


def build_prompt(agent_id: str, doors: list[dict[str, Any]]) -> str:
    rows_json = json.dumps([compact_door(row) for row in doors], indent=2)
    return f"""You are classifying workflow-catalog doors for a reusable Codex/ECC lookup catalog.

Workspace: {ROOT}

Use read-only behavior. Do not edit files. Read the linked source pages or obvious canonical repo paths if needed. Classify exactly these 5 doors:

{rows_json}

Return only JSON matching the provided output schema. No Markdown, no prose outside JSON.

Rules:
- Keep every row evidence-grounded to the source link or a clearly stated fallback.
- If a source link is broken, shallow, or sparse, check the repository README or obvious canonical nested path once.
- Set source_url_status to one of: exact_page_reachable, exact_page_sparse, broken, canonicalized.
- Set canonical_source_url to the original source_url unless you found a better canonical source.
- Set evidence_basis to a short phrase: exact page, README fallback, raw skill file, repo index, category folder, or source sparse.
- Do not invent workflow behavior when evidence is sparse. Say sparse and lower confidence.
- This is cataloging only. Do not design a new skill.
- Do not include the names of outdated agent frameworks.
- The rows must preserve the input workflow_id values exactly.
"""


def prepare() -> None:
    for path in [CHUNKS_DIR, OUTPUTS_DIR, PROMPTS_DIR, LOGS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    rows = load_catalog()
    priority1 = [row for row in rows if row["priority"] == 1]
    selected = priority1[:50]
    remaining_p1 = priority1[50:]
    remaining_p2 = [row for row in rows if row["priority"] == 2]
    remaining_p3 = [row for row in rows if row["priority"] == 3]
    chunks = chunked(selected, 5)

    write_schema()

    chunk_meta = []
    for index, doors in enumerate(chunks, start=1):
        agent_id = f"agent-{index:03d}"
        chunk_path = CHUNKS_DIR / f"{agent_id}.json"
        output_path = OUTPUTS_DIR / f"{agent_id}.md"
        prompt_path = PROMPTS_DIR / f"{agent_id}.txt"
        log_path = LOGS_DIR / f"{agent_id}.log"
        chunk_payload = {
            "agent_id": agent_id,
            "door_count": len(doors),
            "doors": [compact_door(row) for row in doors],
            "output_path": str(output_path.relative_to(ROOT)),
            "prompt_path": str(prompt_path.relative_to(ROOT)),
            "log_path": str(log_path.relative_to(ROOT)),
        }
        chunk_path.write_text(json.dumps(chunk_payload, indent=2) + "\n", encoding="utf-8")
        prompt_path.write_text(build_prompt(agent_id, doors), encoding="utf-8")
        chunk_meta.append(
            {
                "agent_id": agent_id,
                "chunk_path": str(chunk_path.relative_to(ROOT)),
                "prompt_path": str(prompt_path.relative_to(ROOT)),
                "output_path": str(output_path.relative_to(ROOT)),
                "log_path": str(log_path.relative_to(ROOT)),
                "door_ids": [row["id"] for row in doors],
                "door_count": len(doors),
                "status": "pending",
            }
        )

    (RUN_DIR / "remaining-priority1.json").write_text(json.dumps([compact_door(row) for row in remaining_p1], indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "remaining-priority2.json").write_text(json.dumps([compact_door(row) for row in remaining_p2], indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "remaining-priority3.json").write_text(json.dumps([compact_door(row) for row in remaining_p3], indent=2) + "\n", encoding="utf-8")

    command_template = (
        "codex exec -m gpt-5.5 -c model_reasoning_effort='\"low\"' "
        "-c approval_policy='\"never\"' -s read-only "
        f"-C {ROOT} --output-schema {SCHEMA_PATH.relative_to(ROOT)} "
        "-o <output-path> - < <prompt-path>"
    )
    manifest = {
        "run_id": "2026-07-05-priority1-cli-10x5",
        "created_at": now(),
        "source_catalog": str(CATALOG_PATH.relative_to(ROOT)),
        "purpose": "Classify 50 priority workflow doors into normalized catalog rows.",
        "selection_rule": "first 50 rows where priority == 1 in workflow-door-catalog.json order",
        "selected_door_count": len(selected),
        "chunk_count": len(chunks),
        "doors_per_chunk": 5,
        "unassigned_priority1_count": len(remaining_p1),
        "remaining_priority2_count": len(remaining_p2),
        "remaining_priority3_count": len(remaining_p3),
        "command_template": command_template,
        "schema_path": str(SCHEMA_PATH.relative_to(ROOT)),
        "chunks": chunk_meta,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    progress = {
        "run_id": manifest["run_id"],
        "updated_at": now(),
        "status": "prepared",
        "chunks": [
            {
                "agent_id": item["agent_id"],
                "status": "pending",
                "started_at": None,
                "completed_at": None,
                "exit_code": None,
                "output_path": item["output_path"],
                "log_path": item["log_path"],
                "row_count": 0,
            }
            for item in chunk_meta
        ],
    }
    PROGRESS_PATH.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(chunks)} chunks under {RUN_DIR.relative_to(ROOT)}")


def load_progress() -> dict[str, Any]:
    return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))


def write_progress(progress: dict[str, Any]) -> None:
    progress["updated_at"] = now()
    statuses = {chunk["status"] for chunk in progress["chunks"]}
    if "running" in statuses:
        progress["status"] = "running"
    elif "failed" in statuses:
        progress["status"] = "failed"
    elif statuses == {"completed"}:
        progress["status"] = "completed"
    else:
        progress["status"] = "partial"
    PROGRESS_PATH.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")


def run_agent(agent_id: str) -> int:
    prompt_path = PROMPTS_DIR / f"{agent_id}.txt"
    output_path = OUTPUTS_DIR / f"{agent_id}.md"
    log_path = LOGS_DIR / f"{agent_id}.log"
    cmd = [
        "codex",
        "exec",
        "-m",
        "gpt-5.5",
        "-c",
        "model_reasoning_effort='low'",
        "-c",
        "approval_policy='never'",
        "-s",
        "read-only",
        "-C",
        str(ROOT),
        "--output-schema",
        str(SCHEMA_PATH),
        "-o",
        str(output_path),
        "-",
    ]
    with prompt_path.open("rb") as stdin, log_path.open("wb") as log:
        process = subprocess.run(cmd, cwd=ROOT, stdin=stdin, stdout=log, stderr=subprocess.STDOUT)
    return int(process.returncode)


def launch_wave(wave: int) -> None:
    if wave not in {1, 2}:
        raise SystemExit("wave must be 1 or 2")
    agent_numbers = range(1, 6) if wave == 1 else range(6, 11)
    agent_ids = [f"agent-{index:03d}" for index in agent_numbers]
    progress = load_progress()
    by_id = {chunk["agent_id"]: chunk for chunk in progress["chunks"]}
    for agent_id in agent_ids:
        by_id[agent_id]["status"] = "running"
        by_id[agent_id]["started_at"] = now()
        by_id[agent_id]["completed_at"] = None
        by_id[agent_id]["exit_code"] = None
    write_progress(progress)

    processes = {}
    for agent_id in agent_ids:
        prompt_path = PROMPTS_DIR / f"{agent_id}.txt"
        output_path = OUTPUTS_DIR / f"{agent_id}.md"
        log_path = LOGS_DIR / f"{agent_id}.log"
        cmd = [
            "codex",
            "exec",
            "-m",
            "gpt-5.5",
            "-c",
            "model_reasoning_effort='low'",
            "-c",
            "approval_policy='never'",
            "-s",
            "read-only",
            "-C",
            str(ROOT),
            "--output-schema",
            str(SCHEMA_PATH),
            "-o",
            str(output_path),
            "-",
        ]
        stdin = prompt_path.open("rb")
        log = log_path.open("wb")
        process = subprocess.Popen(cmd, cwd=ROOT, stdin=stdin, stdout=log, stderr=subprocess.STDOUT)
        processes[agent_id] = (process, stdin, log)

    for agent_id, (process, stdin, log) in processes.items():
        exit_code = process.wait()
        stdin.close()
        log.close()
        progress = load_progress()
        by_id = {chunk["agent_id"]: chunk for chunk in progress["chunks"]}
        by_id[agent_id]["completed_at"] = now()
        by_id[agent_id]["exit_code"] = int(exit_code)
        by_id[agent_id]["status"] = "completed" if exit_code == 0 else "failed"
        by_id[agent_id]["row_count"] = count_rows(OUTPUTS_DIR / f"{agent_id}.md")
        write_progress(progress)
        print(f"{agent_id}: exit={exit_code} rows={by_id[agent_id]['row_count']}")


def retry_failed() -> None:
    progress = load_progress()
    failed = [chunk["agent_id"] for chunk in progress["chunks"] if chunk["status"] == "failed"]
    for agent_id in failed:
        chunk = next(item for item in progress["chunks"] if item["agent_id"] == agent_id)
        chunk["status"] = "running"
        chunk["started_at"] = now()
        chunk["completed_at"] = None
        write_progress(progress)
        exit_code = run_agent(agent_id)
        progress = load_progress()
        chunk = next(item for item in progress["chunks"] if item["agent_id"] == agent_id)
        chunk["completed_at"] = now()
        chunk["exit_code"] = exit_code
        chunk["status"] = "completed" if exit_code == 0 else "failed"
        chunk["row_count"] = count_rows(OUTPUTS_DIR / f"{agent_id}.md")
        write_progress(progress)
        print(f"{agent_id}: retry exit={exit_code} rows={chunk['row_count']}")


def parse_output(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"empty output: {path}")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def count_rows(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    try:
        payload = parse_output(path)
        return len(payload.get("rows", []))
    except Exception:
        return 0


def parse_all() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    raw_agents = []
    rows = []
    errors = []
    for chunk in manifest["chunks"]:
        agent_id = chunk["agent_id"]
        output_path = ROOT / chunk["output_path"]
        try:
            payload = parse_output(output_path)
            agent_rows = payload.get("rows", [])
            raw_agents.append({"agent_id": agent_id, "quality_note": payload.get("quality_note", ""), "rows": agent_rows})
            for row in agent_rows:
                normalized = {field: str(row.get(field, "")).strip() for field in FIELDS}
                normalized["agent_id"] = agent_id
                rows.append(normalized)
        except Exception as exc:  # noqa: BLE001
            errors.append({"agent_id": agent_id, "output_path": chunk["output_path"], "error": str(exc)})

    RAW_PATH.write_text(json.dumps({"agents": raw_agents, "errors": errors}, indent=2) + "\n", encoding="utf-8")
    FINAL_PATH.write_text(json.dumps({"run_id": manifest["run_id"], "row_count": len(rows), "rows": rows, "errors": errors}, indent=2) + "\n", encoding="utf-8")

    progress = load_progress()
    by_id = {chunk["agent_id"]: chunk for chunk in progress["chunks"]}
    for item in raw_agents:
        by_id[item["agent_id"]]["row_count"] = len(item["rows"])
    write_progress(progress)
    write_report(manifest, rows, raw_agents, errors)
    print(f"Parsed {len(rows)} rows with {len(errors)} errors")


def missing_fields(rows: list[dict[str, Any]]) -> dict[str, int]:
    required = [
        "workflow_id",
        "source_url_status",
        "canonical_source_url",
        "evidence_basis",
        "input_contract",
        "output_artifact",
        "validation_gate",
        "safety_boundary",
        "confidence",
    ]
    return {field: sum(1 for row in rows if not row.get(field)) for field in required}


def write_report(manifest: dict[str, Any], rows: list[dict[str, Any]], raw_agents: list[dict[str, Any]], errors: list[dict[str, Any]]) -> None:
    status_counts: dict[str, int] = {}
    for row in rows:
        status = row.get("source_url_status", "")
        status_counts[status] = status_counts.get(status, 0) + 1

    confidence_counts: dict[str, int] = {}
    for row in rows:
        confidence = row.get("confidence", "").lower()
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1

    lines = [
        "# Workflow Catalog CLI Run",
        "",
        f"Generated: {now()}",
        "",
        "## Summary",
        "",
        f"- Run ID: `{manifest['run_id']}`",
        f"- Selected doors: {manifest['selected_door_count']}",
        f"- Chunks: {manifest['chunk_count']}",
        f"- Parsed rows: {len(rows)}",
        f"- Parse errors: {len(errors)}",
        f"- Unassigned Priority 1 doors: {manifest['unassigned_priority1_count']}",
        f"- Remaining Priority 2 doors prepared: {manifest['remaining_priority2_count']}",
        f"- Remaining Priority 3 doors prepared: {manifest['remaining_priority3_count']}",
        "",
        "## Source URL Status",
        "",
        "| Status | Rows |",
        "| --- | ---: |",
    ]
    for key, value in sorted(status_counts.items()):
        lines.append(f"| {key or '(blank)'} | {value} |")

    lines.extend(["", "## Confidence", "", "| Confidence | Rows |", "| --- | ---: |"])
    for key, value in sorted(confidence_counts.items()):
        lines.append(f"| {key or '(blank)'} | {value} |")

    missing = missing_fields(rows)
    lines.extend(["", "## Required Field Gaps", "", "| Field | Missing Rows |", "| --- | ---: |"])
    for field, count in missing.items():
        lines.append(f"| `{field}` | {count} |")

    lines.extend(["", "## Agent Outputs", "", "| Agent | Rows | Quality Note |", "| --- | ---: | --- |"])
    for item in raw_agents:
        note = str(item.get("quality_note", "")).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {item['agent_id']} | {len(item['rows'])} | {note} |")

    if errors:
        lines.extend(["", "## Errors", "", "| Agent | Error |", "| --- | --- |"])
        for error in errors:
            escaped_error = str(error["error"]).replace("|", "\\|")
            lines.append(f"| {error['agent_id']} | {escaped_error} |")

    lines.extend(
        [
            "",
            "## Next Pass",
            "",
            "The remaining manifests are prepared but not executed in this run:",
            "",
            "- `remaining-priority1.json`",
            "- `remaining-priority2.json`",
            "- `remaining-priority3.json`",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prepare")
    wave = sub.add_parser("launch-wave")
    wave.add_argument("wave", type=int, choices=[1, 2])
    sub.add_parser("retry-failed")
    sub.add_parser("parse")
    args = parser.parse_args()

    if args.cmd == "prepare":
        prepare()
    elif args.cmd == "launch-wave":
        launch_wave(args.wave)
    elif args.cmd == "retry-failed":
        retry_failed()
    elif args.cmd == "parse":
        parse_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
