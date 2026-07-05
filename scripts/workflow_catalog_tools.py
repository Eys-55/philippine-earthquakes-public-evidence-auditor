#!/usr/bin/env python3
"""Build and validate the real-world workflow catalog artifacts."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "agentic-repos"
INTERNAL_DIR = DATA_DIR / "workflow-catalog-internal"
CLI_DIR = DATA_DIR / "workflow-catalog-cli"
REPORT_PATH = ROOT / "reports" / "workflow-catalog-table.md"
REPO_SEED_PATH = DATA_DIR / "workflow-catalog-repo-seed.json"
RAW_SEED_PATH = DATA_DIR / "workflow-link-seed.raw.json"
SEED_PATH = DATA_DIR / "workflow-link-seed.json"
SEED_REPORT_PATH = ROOT / "reports" / "workflow-link-seed.md"
REPOS_PATH = DATA_DIR / "workflow-catalog-repos.json"
WORKFLOWS_PATH = DATA_DIR / "workflow-catalog-workflows.json"

REQUIRED_REPOS = [
    "sickn33/antigravity-awesome-skills",
    "agentskillexchange/skills",
    "tinh2/skills-hub-registry",
    "danielrosehill/Useful-AI-Agent-Skills",
    "msitarzewski/agency-agents",
    "ashishpatel26/500-AI-Agents-Projects",
    "mergisi/awesome-openclaw-agents",
    "jim-schwoebel/awesome_ai_agents",
    "K-Dense-AI/scientific-agent-skills",
    "FreedomIntelligence/OpenClaw-Medical-Skills",
    "ahacker-1/cre-agent-skills",
    "CaseMark/skills",
    "indranilbanerjee/contentforge",
    "marieai/marie-ai",
    "enescingoz/awesome-n8n-templates",
    "ritik-prog/n8n-automation-templates-5000",
    "api-evangelist/use-cases",
]

REQUIRED_SEED_FIELDS = [
    "id",
    "repo",
    "cluster",
    "workflow_or_skill_name",
    "candidate_type",
    "folder_or_file_url",
    "domain_hint",
    "source_index_url",
    "confidence",
    "needs_second_pass",
]

REQUIRED_WORKFLOW_FIELDS = [
    "workflow_id",
    "workflow_name",
    "source_repo",
    "source_url",
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


def read_jsonish(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


def load_seed_manifest() -> dict[str, Any]:
    return json.loads(REPO_SEED_PATH.read_text(encoding="utf-8"))


def slug_for(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def command_seed(args: argparse.Namespace) -> int:
    INTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    raw_records = []
    repo_rows: dict[str, dict[str, Any]] = {}

    for path in sorted(INTERNAL_DIR.glob("agent-*.json")):
        payload = read_jsonish(path)
        payload["_source_file"] = str(path.relative_to(ROOT))
        raw_records.append(payload)
        for row in payload.get("repo_rows", []):
            if row.get("repo"):
                repo_rows[row["repo"]] = row

    seed_manifest = load_seed_manifest()
    clusters = {item["repo"]: item["cluster"] for item in seed_manifest["repos"]}

    deduped: dict[str, dict[str, Any]] = {}
    for payload in raw_records:
        for link in payload.get("workflow_links", []):
            url = (link.get("folder_or_file_url") or "").strip()
            repo = (link.get("repo") or "").strip()
            name = (link.get("workflow_or_skill_name") or url or repo).strip()
            if not repo or not url:
                continue
            key = f"{repo}::{url}"
            existing = deduped.get(key, {})
            merged = {
                "repo": repo,
                "cluster": clusters.get(repo, ""),
                "workflow_or_skill_name": name,
                "candidate_type": link.get("candidate_type", "other"),
                "folder_or_file_url": url,
                "domain_hint": link.get("domain_hint", ""),
                "source_index_url": link.get("source_index_url", ""),
                "confidence": link.get("confidence", "medium"),
                "needs_second_pass": bool(link.get("needs_second_pass", False)),
                "aliases": sorted(set(existing.get("aliases", []) + [name])),
                "why_this_is_a_workflow": link.get("why_this_is_a_workflow", ""),
            }
            deduped[key] = merged

    rows = []
    for index, row in enumerate(sorted(deduped.values(), key=lambda r: (r["repo"], r["workflow_or_skill_name"])), start=1):
        out = {"id": f"wfseed-{index:04d}"}
        out.update({field: row.get(field, "") for field in REQUIRED_SEED_FIELDS if field != "id"})
        out["aliases"] = row.get("aliases", [])
        out["why_this_is_a_workflow"] = row.get("why_this_is_a_workflow", "")
        rows.append(out)

    RAW_SEED_PATH.write_text(json.dumps({"generated_at": str(date.today()), "agent_outputs": raw_records}, indent=2) + "\n", encoding="utf-8")
    SEED_PATH.write_text(
        json.dumps(
            {
                "generated_at": str(date.today()),
                "repo_count_expected": len(REQUIRED_REPOS),
                "repo_count_inspected": len({row.get("repo") for row in repo_rows.values()}),
                "workflow_link_count": len(rows),
                "repos": list(repo_rows.values()),
                "workflow_links": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_seed_report(list(repo_rows.values()), rows)
    print(f"wrote {SEED_PATH.relative_to(ROOT)} with {len(rows)} workflow links")
    return 0


def write_seed_report(repo_rows: list[dict[str, Any]], seed_rows: list[dict[str, Any]]) -> None:
    SEED_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    by_repo: dict[str, list[dict[str, Any]]] = {}
    for row in seed_rows:
        by_repo.setdefault(row["repo"], []).append(row)

    lines = [
        "# Workflow Link Seed",
        "",
        f"Generated: {date.today()}",
        "",
        "This is the readiness artifact from the six inside-Codex discovery agents. It captures indexed workflow, skill, template, and lane links before any external CLI classification agents are launched.",
        "",
        f"- Repos inspected: {len(repo_rows)} / {len(REQUIRED_REPOS)}",
        f"- Deduped seed links: {len(seed_rows)}",
        f"- CLI chunks at 10 links each: {math.ceil(len(seed_rows) / 10)}",
        "",
        "## Completeness Status",
        "",
        "| Repo | Seed links | Needs second pass | Inspection notes |",
        "| --- | ---: | --- | --- |",
    ]

    repo_lookup = {row.get("repo"): row for row in repo_rows}
    for repo in REQUIRED_REPOS:
        repo_info = repo_lookup.get(repo, {})
        repo_links = by_repo.get(repo, [])
        lines.append(
            "| {repo} | {count} | {needs} | {notes} |".format(
                repo=repo,
                count=len(repo_links),
                needs=str(bool(repo_info.get("needs_second_pass", False))).lower(),
                notes=md_cell(str(repo_info.get("inspection_notes", "missing repo row"))),
            )
        )

    lines.extend(
        [
            "",
            "## Seed Links",
            "",
            "| ID | Repo | Candidate | Name | Domain hint | Confidence | Needs second pass | Source |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in seed_rows:
        lines.append(
            "| {id} | {repo} | {candidate_type} | {name} | {domain} | {confidence} | {needs} | {source} |".format(
                id=row["id"],
                repo=row["repo"],
                candidate_type=row["candidate_type"],
                name=md_cell(row["workflow_or_skill_name"]),
                domain=md_cell(row["domain_hint"]),
                confidence=row["confidence"],
                needs=str(row["needs_second_pass"]).lower(),
                source=row["folder_or_file_url"],
            )
        )

    SEED_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def chunk_seed(size: int = 10) -> list[list[dict[str, Any]]]:
    payload = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    rows = payload.get("workflow_links", [])
    return [rows[i : i + size] for i in range(0, len(rows), size)]


def command_cli_prompts(args: argparse.Namespace) -> int:
    chunks = chunk_seed(args.size)
    prompt_dir = CLI_DIR / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for index, chunk in enumerate(chunks, start=1):
        prompt = {
            "task": "Read and classify these workflow/skill/template links for a real-world Codex workflow catalog. Return JSON only.",
            "agent": f"cli-agent-{index:03d}",
            "max_links": args.size,
            "output_shape": {"workflow_rows": [{field: "" for field in REQUIRED_WORKFLOW_FIELDS}]},
            "links": chunk,
            "rules": [
                "Use gpt-5.5 low reasoning and web search if needed.",
                "Classify each link independently.",
                "Do not invent details not supported by the source.",
                "Use concise phrases suitable for a queryable table.",
                "If a link is an index/category rather than one workflow, either classify the category or extract the strongest visible workflow rows, but keep the output grounded.",
            ],
        }
        path = prompt_dir / f"agent-{index:03d}.json"
        path.write_text(json.dumps(prompt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(chunks)} CLI prompts to {prompt_dir.relative_to(ROOT)}")
    print(f"agent_count_required={len(chunks)}")
    print(f"more_than_300_workflows={len(json.loads(SEED_PATH.read_text()).get('workflow_links', [])) > 300}")
    return 0


def command_synthesize(args: argparse.Namespace) -> int:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    seed_manifest = load_seed_manifest()
    repo_seed = {repo["repo"]: repo for repo in seed_manifest["repos"]}

    workflow_rows = []
    for path in sorted(CLI_DIR.glob("agent-*.json")):
        payload = read_jsonish(path)
        for row in payload.get("workflow_rows", []):
            if row.get("workflow_id") and row.get("source_url"):
                row["classification_source_file"] = str(path.relative_to(ROOT))
                workflow_rows.append(row)

    repo_rows = []
    by_repo: dict[str, list[dict[str, Any]]] = {}
    for row in workflow_rows:
        by_repo.setdefault(row.get("source_repo", ""), []).append(row)

    for repo_name in REQUIRED_REPOS:
        seed_repo = repo_seed.get(repo_name, {})
        repo_workflows = by_repo.get(repo_name, [])
        repo_rows.append(
            {
                "repo": repo_name,
                "url": seed_repo.get("url", ""),
                "cluster": seed_repo.get("cluster", ""),
                "workflow_count": len(repo_workflows),
                "domains": sorted({w.get("domain", "") for w in repo_workflows if w.get("domain")}),
                "workflow_types": sorted({w.get("workflow_type", "") for w in repo_workflows if w.get("workflow_type")}),
                "needs_second_pass": any(w.get("confidence") == "low" for w in repo_workflows) or len(repo_workflows) == 0,
            }
        )

    REPOS_PATH.write_text(json.dumps({"generated_at": str(date.today()), "repos": repo_rows}, indent=2) + "\n", encoding="utf-8")
    WORKFLOWS_PATH.write_text(json.dumps({"generated_at": str(date.today()), "workflows": workflow_rows}, indent=2) + "\n", encoding="utf-8")
    write_report(repo_rows, workflow_rows)
    print(f"wrote {REPOS_PATH.relative_to(ROOT)}")
    print(f"wrote {WORKFLOWS_PATH.relative_to(ROOT)}")
    print(f"wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


def write_report(repo_rows: list[dict[str, Any]], workflow_rows: list[dict[str, Any]]) -> None:
    domain_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for row in workflow_rows:
        for domain in str(row.get("domain", "")).split(","):
            domain = domain.strip()
            if domain:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
        workflow_type = row.get("workflow_type", "")
        if workflow_type:
            type_counts[workflow_type] = type_counts.get(workflow_type, 0) + 1

    lines = [
        "# Real-World Workflow Catalog",
        "",
        f"Generated: {date.today()}",
        "",
        f"- Repos cataloged: {len(repo_rows)}",
        f"- Workflow rows: {len(workflow_rows)}",
        f"- Domains: {len(domain_counts)}",
        f"- Workflow types: {len(type_counts)}",
        "",
        "## Repo Table",
        "",
        "| Repo | Cluster | Workflow count | Domains | Workflow types | Needs second pass |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in repo_rows:
        lines.append(
            "| {repo} | {cluster} | {workflow_count} | {domains} | {workflow_types} | {needs_second_pass} |".format(
                repo=row["repo"],
                cluster=row["cluster"],
                workflow_count=row["workflow_count"],
                domains=", ".join(row["domains"]),
                workflow_types=", ".join(row["workflow_types"]),
                needs_second_pass=str(row["needs_second_pass"]).lower(),
            )
        )

    lines.extend(
        [
            "",
            "## Workflow Table",
            "",
            "| ID | Workflow | Repo | Domain | Type | Real-life job | Input | Output | Human boundary | Source |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in workflow_rows:
        lines.append(
            "| {workflow_id} | {workflow_name} | {source_repo} | {domain} | {workflow_type} | {real_life_job} | {input_contract} | {output_artifact} | {human_review_boundary} | {source_url} |".format(
                **{key: md_cell(str(row.get(key, ""))) for key in REQUIRED_WORKFLOW_FIELDS}
            )
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def md_cell(value: str) -> str:
    return value.replace("\n", " ").replace("|", "\\|").strip()


def command_validate(args: argparse.Namespace) -> int:
    errors = []
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    seed_repos = {row.get("repo") for row in seed.get("repos", [])}
    missing_repos = sorted(set(REQUIRED_REPOS) - seed_repos)
    if missing_repos:
        errors.append(f"missing inspected repos in seed: {missing_repos}")

    for row in seed.get("workflow_links", []):
        missing = [field for field in REQUIRED_SEED_FIELDS if field not in row or row[field] in ("", None)]
        if missing:
            errors.append(f"seed row {row.get('id')} missing {missing}")

    if WORKFLOWS_PATH.exists():
        workflows = json.loads(WORKFLOWS_PATH.read_text(encoding="utf-8")).get("workflows", [])
        for row in workflows:
            missing = [field for field in REQUIRED_WORKFLOW_FIELDS if field not in row or row[field] in ("", None)]
            if missing:
                errors.append(f"workflow row {row.get('workflow_id')} missing {missing}")

    prompt_dir = CLI_DIR / "prompts"
    for prompt_path in sorted(prompt_dir.glob("agent-*.json")):
        links = json.loads(prompt_path.read_text(encoding="utf-8")).get("links", [])
        if len(links) > 10:
            errors.append(f"{prompt_path.name} owns {len(links)} links")

    queries = ["earthquake", "healthcare", "education", "real estate", "document processing", "human review", "automation templates", "Codex config package"]
    corpus = ""
    if WORKFLOWS_PATH.exists():
        corpus += WORKFLOWS_PATH.read_text(encoding="utf-8").lower()
    if REPORT_PATH.exists():
        corpus += REPORT_PATH.read_text(encoding="utf-8").lower()
    if corpus:
        for query in queries:
            if query.lower() not in corpus:
                errors.append(f"query term not represented: {query}")

    if errors:
        print("\n".join(errors))
        return 1
    print("workflow catalog validation passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed")
    prompts = sub.add_parser("cli-prompts")
    prompts.add_argument("--size", type=int, default=10)
    sub.add_parser("synthesize")
    sub.add_parser("validate")
    args = parser.parse_args()
    return globals()[f"command_{args.command.replace('-', '_')}"](args)


if __name__ == "__main__":
    sys.exit(main())
