#!/usr/bin/env python3
"""Run all remaining workflow catalog doors through Codex CLI agents."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "workflow_catalog_cli_run.py"
PREVIOUS_RUN = ROOT / "data" / "agentic-repos" / "workflow-catalog-runs" / "2026-07-05-priority1-cli-10x5"
RUN_DIR = ROOT / "data" / "agentic-repos" / "workflow-catalog-runs" / "2026-07-05-remaining-cli-25x5"
CHUNKS_DIR = RUN_DIR / "chunks"
OUTPUTS_DIR = RUN_DIR / "outputs"
PROMPTS_DIR = RUN_DIR / "prompts"
LOGS_DIR = RUN_DIR / "logs"
SCHEMA_PATH = RUN_DIR / "classification-output.schema.json"
MANIFEST_PATH = RUN_DIR / "manifest.json"
PROGRESS_PATH = RUN_DIR / "progress.json"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("workflow_catalog_cli_run_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.RUN_DIR = RUN_DIR
    module.CHUNKS_DIR = CHUNKS_DIR
    module.OUTPUTS_DIR = OUTPUTS_DIR
    module.PROMPTS_DIR = PROMPTS_DIR
    module.LOGS_DIR = LOGS_DIR
    module.SCHEMA_PATH = SCHEMA_PATH
    module.MANIFEST_PATH = MANIFEST_PATH
    module.PROGRESS_PATH = PROGRESS_PATH
    module.RAW_PATH = RUN_DIR / "workflow-classifications.raw.json"
    module.FINAL_PATH = RUN_DIR / "workflow-classifications.json"
    module.REPORT_PATH = RUN_DIR / "report.md"
    return module


base = load_base()


def load_remaining() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name in ["remaining-priority1.json", "remaining-priority2.json", "remaining-priority3.json"]:
        rows.extend(json.loads((PREVIOUS_RUN / name).read_text(encoding="utf-8")))
    return rows


def prepare() -> None:
    for path in [CHUNKS_DIR, OUTPUTS_DIR, PROMPTS_DIR, LOGS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    rows = load_remaining()
    chunks = base.chunked(rows, 5)
    base.write_schema()

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
            "doors": doors,
            "output_path": str(output_path.relative_to(ROOT)),
            "prompt_path": str(prompt_path.relative_to(ROOT)),
            "log_path": str(log_path.relative_to(ROOT)),
        }
        chunk_path.write_text(json.dumps(chunk_payload, indent=2) + "\n", encoding="utf-8")
        prompt_path.write_text(build_remaining_prompt(agent_id, doors), encoding="utf-8")
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

    manifest = {
        "run_id": "2026-07-05-remaining-cli-25x5",
        "created_at": base.now(),
        "source_run": str(PREVIOUS_RUN.relative_to(ROOT)),
        "purpose": "Classify all 121 remaining workflow doors into normalized catalog rows.",
        "selection_rule": "remaining-priority1, remaining-priority2, and remaining-priority3 from the first CLI run",
        "selected_door_count": len(rows),
        "chunk_count": len(chunks),
        "doors_per_chunk": "5 except final chunk may have fewer",
        "unassigned_priority1_count": 0,
        "remaining_priority2_count": 0,
        "remaining_priority3_count": 0,
        "command_template": (
            "codex exec -m gpt-5.5 -c model_reasoning_effort='\"low\"' "
            "-c approval_policy='\"never\"' -s read-only "
            f"-C {ROOT} --output-schema {SCHEMA_PATH.relative_to(ROOT)} "
            "-o <output-path> - < <prompt-path>"
        ),
        "schema_path": str(SCHEMA_PATH.relative_to(ROOT)),
        "chunks": chunk_meta,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    progress = {
        "run_id": manifest["run_id"],
        "updated_at": base.now(),
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
    print(f"Prepared {len(chunks)} chunks for {len(rows)} remaining doors under {RUN_DIR.relative_to(ROOT)}")


def build_remaining_prompt(agent_id: str, doors: list[dict[str, Any]]) -> str:
    return f"""You are classifying workflow-catalog doors for a reusable Codex/ECC lookup catalog.

Workspace: {ROOT}

Use read-only behavior. Do not edit files. Read the linked source pages or obvious canonical repo paths if needed. Classify exactly these {len(doors)} doors:

{json.dumps(doors, indent=2)}

Return only JSON matching the provided output schema. No Markdown, no prose outside JSON.

Rules:
- Keep every row evidence-grounded to the source link or a clearly stated fallback.
- If source access is unavailable, use the supplied local catalog hints as fallback context, mark source_url_status honestly, and lower confidence.
- If a source link is broken, shallow, or sparse, check the repository README or obvious canonical nested path once.
- Set source_url_status to one of: exact_page_reachable, exact_page_sparse, broken, canonicalized.
- Set canonical_source_url to the original source_url unless you found a better canonical source.
- Set evidence_basis to a short phrase: exact page, README fallback, raw skill file, repo index, category folder, local catalog fallback, or source sparse.
- Do not invent workflow behavior when evidence is sparse. Say sparse and lower confidence.
- This is cataloging only. Do not design a new skill.
- Do not include the names of outdated agent frameworks.
- The rows must preserve the input workflow_id values exactly.
"""


def launch_all() -> None:
    progress = base.load_progress()
    by_id = {chunk["agent_id"]: chunk for chunk in progress["chunks"]}
    for chunk in progress["chunks"]:
        chunk["status"] = "running"
        chunk["started_at"] = base.now()
        chunk["completed_at"] = None
        chunk["exit_code"] = None
    base.write_progress(progress)

    processes = {}
    for item in json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["chunks"]:
        agent_id = item["agent_id"]
        prompt_path = ROOT / item["prompt_path"]
        output_path = ROOT / item["output_path"]
        log_path = ROOT / item["log_path"]
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
        progress = base.load_progress()
        by_id = {chunk["agent_id"]: chunk for chunk in progress["chunks"]}
        by_id[agent_id]["completed_at"] = base.now()
        by_id[agent_id]["exit_code"] = int(exit_code)
        by_id[agent_id]["status"] = "completed" if exit_code == 0 else "failed"
        by_id[agent_id]["row_count"] = base.count_rows(OUTPUTS_DIR / f"{agent_id}.md")
        base.write_progress(progress)
        print(f"{agent_id}: exit={exit_code} rows={by_id[agent_id]['row_count']}")


def main() -> int:
    parser = base.argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "launch-all", "parse", "retry-failed"])
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "launch-all":
        launch_all()
    elif args.command == "parse":
        base.parse_all()
    elif args.command == "retry-failed":
        base.retry_failed()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
