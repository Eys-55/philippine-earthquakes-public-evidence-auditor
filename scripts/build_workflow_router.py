#!/usr/bin/env python3
"""Build the queryable router catalog from workflow-link seed rows."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "agentic-repos" / "workflow-link-seed.json"
ROUTER_PATH = ROOT / "data" / "agentic-repos" / "workflow-router.json"
ROUTER_REPORT_PATH = ROOT / "reports" / "workflow-router.md"


SKILL_PACKAGE_REPOS = {
    "agentskillexchange/skills",
    "sickn33/antigravity-awesome-skills",
    "tinh2/skills-hub-registry",
    "CaseMark/skills",
    "ahacker-1/cre-agent-skills",
    "K-Dense-AI/scientific-agent-skills",
    "FreedomIntelligence/OpenClaw-Medical-Skills",
    "indranilbanerjee/contentforge",
}

RUNTIME_REFERENCE_REPOS = {
    "enescingoz/awesome-n8n-templates",
    "ritik-prog/n8n-automation-templates-5000",
    "marieai/marie-ai",
}


def has(text: str, *phrases: str) -> bool:
    value = text.lower()
    return any(phrase.lower() in value for phrase in phrases)


def has_word(text: str, *words: str) -> bool:
    value = text.lower()
    return any(re.search(rf"(?<![a-z0-9]){re.escape(word.lower())}(?![a-z0-9])", value) for word in words)


def add_unique(target: list[str], *values: str) -> None:
    for value in values:
        if value and value not in target:
            target.append(value)


def classify_surface(seed_row: dict[str, Any]) -> dict[str, Any]:
    text = " ".join(
        str(seed_row.get(key, ""))
        for key in [
            "repo",
            "workflow_or_skill_name",
            "candidate_type",
            "domain_hint",
            "folder_or_file_url",
        ]
    ).lower()
    repo = seed_row["repo"]
    domains: list[str] = []
    patterns: list[str] = []

    if has_word(text, "health", "healthcare", "medical", "patient", "clinical", "phi", "pharma") or "/med" in text:
        add_unique(domains, "healthcare")
        add_unique(patterns, "HealthcareAdmin", "ComplianceSupport", "HumanReview")
    if has(text, "real estate", "cre", "zillow", "property", "underwriting", "lease", "brokerage", "closing", "asset management"):
        add_unique(domains, "real_estate")
        add_unique(patterns, "DueDiligence", "EvidenceAudit")
    if has_word(text, "education", "moodle", "student", "curriculum", "assessment"):
        add_unique(domains, "education")
        add_unique(patterns, "EducationSupport")
    if has_word(text, "document", "pdf", "ocr", "transcription", "redline", "invoice", "vault", "forms") or has(text, "form extraction"):
        add_unique(domains, "document_processing")
        add_unique(patterns, "DocumentTransformation")
    if has(text, "evidence", "public records", "osint", "due diligence", "compliance", "grc", "hazard", "geospatial", "earthquake", "source taxonomy"):
        add_unique(domains, "public_evidence")
        add_unique(patterns, "EvidenceAudit", "ComplianceSupport")
    if has_word(text, "legal", "case", "redline", "vault"):
        add_unique(domains, "legal")
        add_unique(patterns, "CaseIntake", "HumanReview")
    if has_word(text, "finance", "capital", "underwriting", "salesforce", "hubspot", "crm"):
        add_unique(domains, "finance_or_crm")
    if has_word(text, "research", "science", "literature", "academic", "scraping", "rag"):
        add_unique(domains, "research")
        add_unique(patterns, "ResearchOps")
    if has_word(text, "monitoring", "incident", "sre", "alert") or has(text, "security monitoring"):
        add_unique(patterns, "Monitoring")
    if has_word(text, "queue", "batch", "templates") or has(text, "6260", "2,001", "2,055", "2,000", "313 automation"):
        add_unique(patterns, "QueueProcessing", "AutomationTemplate")
    if has_word(text, "human", "review", "approve", "redline", "compliance"):
        add_unique(patterns, "HumanReview")
    if has_word(text, "codex", "skill", "plugin", "bundle", "manifest", "catalog", "registry") or has(text, "config package"):
        add_unique(patterns, "ConfigPackage", "SkillRegistry")

    if not domains:
        if "n8n" in repo.lower():
            add_unique(domains, "automation")
        elif has_word(text, "agent", "workflow", "skill"):
            add_unique(domains, "agent_workflows")
        else:
            add_unique(domains, "general")

    if not patterns:
        if seed_row["candidate_type"] in {"manifest", "category"}:
            add_unique(patterns, "PatternRouter", "SkillRegistry")
        elif seed_row["candidate_type"] == "template":
            add_unique(patterns, "AutomationTemplate")
        else:
            add_unique(patterns, "WorkflowSurface")

    surface_level = {
        "manifest": "catalog_manifest",
        "category": "category_surface",
        "lane": "industry_lane",
        "skill": "skill_package",
        "template": "template_or_package",
        "workflow": "workflow_surface",
    }.get(seed_row["candidate_type"], "workflow_surface")

    if repo in SKILL_PACKAGE_REPOS:
        codex_fit = "skill/package reference"
    elif repo in RUNTIME_REFERENCE_REPOS:
        codex_fit = "runtime/platform inspiration"
    elif repo == "api-evangelist/use-cases":
        codex_fit = "source taxonomy"
    else:
        codex_fit = "inspiration catalog"
    if has_word(text, "codex"):
        codex_fit = "Codex-native or Codex-adjacent"

    expand_priority = score_priority(text, domains, patterns, codex_fit)
    input_contract, output_artifact = infer_contracts(domains, patterns)
    human_review, safety_boundary = infer_boundaries(domains, patterns, codex_fit)

    if seed_row.get("needs_second_pass"):
        expand_when = "expand only when query hits this domain or repo; inspect index/manifest then top leaf folders"
    else:
        expand_when = "can classify directly from this link when query matches"

    return {
        "surface_id": seed_row["id"].replace("wfseed", "surface"),
        "seed_id": seed_row["id"],
        "repo": repo,
        "cluster": seed_row.get("cluster", ""),
        "surface_name": seed_row["workflow_or_skill_name"],
        "surface_level": surface_level,
        "source_url": seed_row["folder_or_file_url"],
        "domain_tags": domains,
        "workflow_pattern_tags": patterns,
        "input_contract_hint": input_contract,
        "output_artifact_hint": output_artifact,
        "human_review_boundary": human_review,
        "safety_boundary": safety_boundary,
        "codex_fit": codex_fit,
        "expand_priority": expand_priority,
        "expand_when": expand_when,
        "needs_second_pass": bool(seed_row.get("needs_second_pass")),
        "confidence": seed_row.get("confidence", "medium"),
    }


def score_priority(text: str, domains: list[str], patterns: list[str], codex_fit: str) -> int:
    priority = 3
    if any(domain in domains for domain in ["healthcare", "real_estate", "education", "document_processing", "public_evidence", "legal"]):
        priority = 1
    elif any(domain in domains for domain in ["research", "automation", "finance_or_crm"]) or any(
        pattern in patterns for pattern in ["AutomationTemplate", "ConfigPackage", "SkillRegistry"]
    ):
        priority = 2

    if codex_fit == "runtime/platform inspiration" and not any(
        domain in domains for domain in ["healthcare", "real_estate", "education", "document_processing"]
    ):
        priority = max(priority, 2)

    if has_word(text, "engineering", "developer", "coding", "qa") or has(text, "web app", "browser automation", "saas"):
        if not any(domain in domains for domain in ["healthcare", "real_estate", "education", "document_processing", "public_evidence"]):
            priority = 3

    return priority


def infer_contracts(domains: list[str], patterns: list[str]) -> tuple[str, str]:
    if any(pattern in patterns for pattern in ["EvidenceAudit", "DueDiligence"]):
        return (
            "public records, source links, addresses, entity names, evidence files",
            "evidence packet, due-diligence brief, caveated report",
        )
    if "HealthcareAdmin" in patterns:
        return (
            "patient/referral/source documents, forms, notes",
            "clean packet, summary, checklist, review-ready draft",
        )
    if "DocumentTransformation" in patterns:
        return (
            "PDFs, forms, files, extracted text, templates",
            "structured extraction, completed draft, transformed document",
        )
    if "EducationSupport" in patterns:
        return (
            "student/course/admin context, materials, assessment data",
            "lesson/support plan, assessment artifact, admin packet",
        )
    if "AutomationTemplate" in patterns:
        return (
            "event trigger, app credentials, records, message/document source",
            "automation run, notification, transformed record, queued task",
        )
    if "agent_workflows" in domains:
        return (
            "repo docs, skill files, manifests, category indexes",
            "workflow pattern, reusable skill/package idea, router match",
        )
    return (
        "repo docs, source links, category indexes, user-provided context",
        "matched router surface and expansion plan",
    )


def infer_boundaries(domains: list[str], patterns: list[str], codex_fit: str) -> tuple[str, str]:
    if any(pattern in patterns for pattern in ["ComplianceSupport", "HumanReview"]) or any(
        domain in domains for domain in ["healthcare", "legal", "public_evidence"]
    ):
        return (
            "required before final action or conclusion",
            "must not make legal, medical, engineering, compliance, or safety conclusions without human review",
        )
    if codex_fit == "runtime/platform inspiration":
        return (
            "recommended before sending/publishing/writing externally",
            "do not treat runtime platform as Codex architecture unless explicitly chosen",
        )
    return (
        "optional unless output affects a person or external system",
        "keep as reference pattern until copied into an ECC contract",
    )


def md_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def write_router_report(rows: list[dict[str, Any]]) -> None:
    repo_counts = Counter(row["repo"] for row in rows)
    domain_counts = Counter(domain for row in rows for domain in row["domain_tags"])
    pattern_counts = Counter(pattern for row in rows for pattern in row["workflow_pattern_tags"])
    priority_counts = Counter(row["expand_priority"] for row in rows)

    lines = [
        "# Workflow Router",
        "",
        f"Generated: {date.today()}",
        "",
        "This is the durable router over the 171 seed links. Each row is a workflow surface, or door, used for fast query matching before deeper agent expansion.",
        "",
        "## Summary",
        "",
        f"- Router surfaces: {len(rows)}",
        f"- Repos: {len(repo_counts)}",
        f"- Priority 1 surfaces: {priority_counts[1]}",
        f"- Priority 2 surfaces: {priority_counts[2]}",
        f"- Priority 3 surfaces: {priority_counts[3]}",
        "",
        "## Domain Tags",
        "",
        "| Domain | Count |",
        "| --- | ---: |",
    ]
    for key, value in domain_counts.most_common():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Workflow Pattern Tags", "", "| Pattern | Count |", "| --- | ---: |"])
    for key, value in pattern_counts.most_common():
        lines.append(f"| {key} | {value} |")

    query_sections = [
        (
            "Earthquake / Public Evidence Audit",
            lambda row: "public_evidence" in row["domain_tags"]
            or "DueDiligence" in row["workflow_pattern_tags"]
            or "EvidenceAudit" in row["workflow_pattern_tags"],
        ),
        ("Healthcare / Patient Documents", lambda row: "healthcare" in row["domain_tags"]),
        ("Real Estate Due Diligence", lambda row: "real_estate" in row["domain_tags"]),
        ("Education", lambda row: "education" in row["domain_tags"]),
        (
            "Document Processing / Human Review",
            lambda row: "document_processing" in row["domain_tags"] or "HumanReview" in row["workflow_pattern_tags"],
        ),
    ]
    for title, predicate in query_sections:
        lines.extend(
            [
                "",
                f"## {title}",
                "",
                "| Surface | Repo | Domains | Patterns | Priority | Why open it |",
                "| --- | --- | --- | --- | ---: | --- |",
            ]
        )
        matches = sorted([row for row in rows if predicate(row)], key=lambda row: (row["expand_priority"], row["repo"], row["surface_name"]))
        for row in matches[:12]:
            lines.append(
                "| {surface} | {repo} | {domains} | {patterns} | {priority} | {expand} |".format(
                    surface=md_cell(row["surface_name"]),
                    repo=row["repo"],
                    domains=", ".join(row["domain_tags"]),
                    patterns=", ".join(row["workflow_pattern_tags"]),
                    priority=row["expand_priority"],
                    expand=md_cell(row["expand_when"]),
                )
            )

    lines.extend(
        [
            "",
            "## Full Router Table",
            "",
            "| ID | Surface | Repo | Level | Domains | Patterns | Codex fit | Priority | Source |",
            "| --- | --- | --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {id} | {surface} | {repo} | {level} | {domains} | {patterns} | {fit} | {priority} | {source} |".format(
                id=row["surface_id"],
                surface=md_cell(row["surface_name"]),
                repo=row["repo"],
                level=row["surface_level"],
                domains=", ".join(row["domain_tags"]),
                patterns=", ".join(row["workflow_pattern_tags"]),
                fit=md_cell(row["codex_fit"]),
                priority=row["expand_priority"],
                source=row["source_url"],
            )
        )

    ROUTER_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    rows = [classify_surface(row) for row in seed.get("workflow_links", [])]
    payload = {
        "generated_at": str(date.today()),
        "source": str(SEED_PATH.relative_to(ROOT)),
        "purpose": "Fast router over workflow surfaces; expand matching doors lazily with agents only after user approval.",
        "surface_count": len(rows),
        "rows": rows,
    }
    ROUTER_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_router_report(rows)
    print(f"wrote {ROUTER_PATH.relative_to(ROOT)} with {len(rows)} surfaces")
    print(f"wrote {ROUTER_REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
