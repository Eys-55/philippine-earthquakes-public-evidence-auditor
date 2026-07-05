#!/usr/bin/env python3
"""Build a browse-first catalog over all workflow router doors."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "data" / "agentic-repos" / "workflow-router.json"
CATALOG_JSON_PATH = ROOT / "data" / "agentic-repos" / "workflow-door-catalog.json"
CATALOG_CSV_PATH = ROOT / "data" / "agentic-repos" / "workflow-door-catalog.csv"
CATALOG_REPORT_PATH = ROOT / "reports" / "workflow-door-catalog.md"


CATEGORY_RULES = [
    ("Healthcare / Medical Workflow", {"HealthcareAdmin"}, {"healthcare"}),
    ("Education Workflow", {"EducationSupport"}, {"education"}),
    ("Evidence / Due Diligence", {"EvidenceAudit", "DueDiligence"}, {"public_evidence", "real_estate"}),
    ("Document Transformation", {"DocumentTransformation"}, {"document_processing"}),
    ("Case Intake / Legal Review", {"CaseIntake"}, {"legal"}),
    ("Automation / Queue Template", {"AutomationTemplate", "QueueProcessing", "Monitoring"}, {"automation"}),
    ("Research / Knowledge Workflow", {"ResearchOps"}, {"research"}),
    ("Skill Registry / Config Package", {"ConfigPackage", "SkillRegistry", "PatternRouter"}, {"agent_workflows"}),
    ("Source Taxonomy / Vocabulary", set(), set()),
    ("Runtime / Platform Reference", set(), set()),
    ("General Workflow Surface", set(), {"general"}),
]


def primary_category(row: dict[str, Any]) -> str:
    patterns = set(row["workflow_pattern_tags"])
    domains = set(row["domain_tags"])
    fit = row["codex_fit"]

    if fit == "source taxonomy":
        return "Source Taxonomy / Vocabulary"
    if fit == "runtime/platform inspiration" and not domains.intersection(
        {"document_processing", "education", "healthcare", "real_estate"}
    ):
        return "Runtime / Platform Reference"

    for category, pattern_match, domain_match in CATEGORY_RULES:
        if pattern_match.intersection(patterns) or domain_match.intersection(domains):
            return category
    return "General Workflow Surface"


def primary_domain(row: dict[str, Any]) -> str:
    order = [
        "healthcare",
        "education",
        "real_estate",
        "public_evidence",
        "document_processing",
        "legal",
        "finance_or_crm",
        "research",
        "automation",
        "agent_workflows",
        "general",
    ]
    tags = set(row["domain_tags"])
    for domain in order:
        if domain in tags:
            return domain
    return row["domain_tags"][0] if row["domain_tags"] else "general"


def primary_pattern(row: dict[str, Any]) -> str:
    order = [
        "HealthcareAdmin",
        "EducationSupport",
        "EvidenceAudit",
        "DueDiligence",
        "DocumentTransformation",
        "CaseIntake",
        "ComplianceSupport",
        "HumanReview",
        "QueueProcessing",
        "AutomationTemplate",
        "Monitoring",
        "ResearchOps",
        "ConfigPackage",
        "SkillRegistry",
        "PatternRouter",
        "WorkflowSurface",
    ]
    tags = set(row["workflow_pattern_tags"])
    for pattern in order:
        if pattern in tags:
            return pattern
    return row["workflow_pattern_tags"][0] if row["workflow_pattern_tags"] else "WorkflowSurface"


def browsing_use(row: dict[str, Any], category: str) -> str:
    if category == "Healthcare / Medical Workflow":
        return "patient/referral/admin packets, medical document review, regulated human-review flows"
    if category == "Education Workflow":
        return "student support, curriculum, assessment, education admin workflow ideas"
    if category == "Evidence / Due Diligence":
        return "public evidence, permit/title/source audits, due-diligence packet patterns"
    if category == "Document Transformation":
        return "OCR, PDF parsing, form extraction, document-to-structured-output patterns"
    if category == "Case Intake / Legal Review":
        return "messy intake, legal review, case setup, redline and approval workflows"
    if category == "Automation / Queue Template":
        return "batch processing, triggers, app automation, queue and notification examples"
    if category == "Research / Knowledge Workflow":
        return "literature, research, scraping, knowledge synthesis, cited research packets"
    if category == "Skill Registry / Config Package":
        return "skill/package shape, manifests, registries, reusable Codex/ECC config package ideas"
    if category == "Source Taxonomy / Vocabulary":
        return "domain vocabulary, use-case naming, source taxonomy for future workflow labels"
    if category == "Runtime / Platform Reference":
        return "execution/runtime inspiration only; translate useful patterns back into Codex/ECC"
    return "general workflow discovery and future expansion"


def expansion_status(row: dict[str, Any]) -> str:
    if row["expand_priority"] == 1 and not row["needs_second_pass"]:
        return "ready_to_classify"
    if row["expand_priority"] == 1:
        return "high_value_needs_expansion"
    if row["needs_second_pass"]:
        return "expand_on_query"
    return "reference_only"


def enriched_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for row in rows:
        category = primary_category(row)
        primary = {
            "id": row["surface_id"],
            "repo": row["repo"],
            "cluster": row["cluster"],
            "door": row["surface_name"],
            "door_level": row["surface_level"],
            "primary_category": category,
            "primary_domain": primary_domain(row),
            "primary_pattern": primary_pattern(row),
            "domain_tags": row["domain_tags"],
            "workflow_pattern_tags": row["workflow_pattern_tags"],
            "fit": row["codex_fit"],
            "priority": row["expand_priority"],
            "expansion_status": expansion_status(row),
            "browse_use": browsing_use(row, category),
            "input_contract_hint": row["input_contract_hint"],
            "output_artifact_hint": row["output_artifact_hint"],
            "human_review_boundary": row["human_review_boundary"],
            "safety_boundary": row["safety_boundary"],
            "source_url": row["source_url"],
            "needs_second_pass": row["needs_second_pass"],
            "confidence": row["confidence"],
        }
        enriched.append(primary)
    return sorted(enriched, key=lambda item: (item["primary_category"], item["repo"], item["door"]))


def md_cell(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(value)
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def write_json(rows: list[dict[str, Any]]) -> None:
    payload = {
        "generated_at": str(date.today()),
        "source": str(ROUTER_PATH.relative_to(ROOT)),
        "purpose": "Browse-first catalog of all workflow doors for future workflow discovery and classification.",
        "door_count": len(rows),
        "category_model": [
            "Healthcare / Medical Workflow",
            "Education Workflow",
            "Evidence / Due Diligence",
            "Document Transformation",
            "Case Intake / Legal Review",
            "Automation / Queue Template",
            "Research / Knowledge Workflow",
            "Skill Registry / Config Package",
            "Source Taxonomy / Vocabulary",
            "Runtime / Platform Reference",
            "General Workflow Surface",
        ],
        "rows": rows,
    }
    CATALOG_JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_csv(rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "id",
        "repo",
        "cluster",
        "door",
        "door_level",
        "primary_category",
        "primary_domain",
        "primary_pattern",
        "domain_tags",
        "workflow_pattern_tags",
        "fit",
        "priority",
        "expansion_status",
        "browse_use",
        "input_contract_hint",
        "output_artifact_hint",
        "human_review_boundary",
        "safety_boundary",
        "source_url",
        "needs_second_pass",
        "confidence",
    ]
    with CATALOG_CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            csv_row = dict(row)
            csv_row["domain_tags"] = ";".join(row["domain_tags"])
            csv_row["workflow_pattern_tags"] = ";".join(row["workflow_pattern_tags"])
            writer.writerow(csv_row)


def write_report(rows: list[dict[str, Any]]) -> None:
    category_counts = Counter(row["primary_category"] for row in rows)
    domain_counts = Counter(row["primary_domain"] for row in rows)
    pattern_counts = Counter(row["primary_pattern"] for row in rows)
    fit_counts = Counter(row["fit"] for row in rows)
    repo_counts = Counter(row["repo"] for row in rows)

    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_category[row["primary_category"]].append(row)

    lines = [
        "# Workflow Door Catalog",
        "",
        f"Generated: {date.today()}",
        "",
        "This is the browse-first catalog for all 171 workflow doors. Use it when you want to scan what the repo set contains before choosing which doors deserve deeper agent classification.",
        "",
        "## Summary",
        "",
        f"- Doors: {len(rows)}",
        f"- Repos: {len(repo_counts)}",
        f"- Categories: {len(category_counts)}",
        f"- Priority 1 doors: {sum(1 for row in rows if row['priority'] == 1)}",
        f"- Needs expansion on query: {sum(1 for row in rows if row['needs_second_pass'])}",
        "",
        "## Category Counts",
        "",
        "| Category | Doors |",
        "| --- | ---: |",
    ]

    for category, count in category_counts.most_common():
        lines.append(f"| {md_cell(category)} | {count} |")

    lines.extend(["", "## Primary Domain Counts", "", "| Domain | Doors |", "| --- | ---: |"])
    for domain, count in domain_counts.most_common():
        lines.append(f"| {md_cell(domain)} | {count} |")

    lines.extend(["", "## Primary Pattern Counts", "", "| Pattern | Doors |", "| --- | ---: |"])
    for pattern, count in pattern_counts.most_common():
        lines.append(f"| {md_cell(pattern)} | {count} |")

    lines.extend(["", "## Fit Counts", "", "| Fit | Doors |", "| --- | ---: |"])
    for fit, count in fit_counts.most_common():
        lines.append(f"| {md_cell(fit)} | {count} |")

    lines.extend(["", "## Browse By Category"])
    category_order = [
        "Healthcare / Medical Workflow",
        "Education Workflow",
        "Evidence / Due Diligence",
        "Document Transformation",
        "Case Intake / Legal Review",
        "Automation / Queue Template",
        "Research / Knowledge Workflow",
        "Skill Registry / Config Package",
        "Source Taxonomy / Vocabulary",
        "Runtime / Platform Reference",
        "General Workflow Surface",
    ]
    for category in category_order:
        category_rows = by_category.get(category, [])
        if not category_rows:
            continue
        lines.extend(
            [
                "",
                f"### {category}",
                "",
                "| ID | Door | Repo | Pattern | Fit | Priority | Use | Source |",
                "| --- | --- | --- | --- | --- | ---: | --- | --- |",
            ]
        )
        for row in category_rows:
            lines.append(
                "| {id} | {door} | {repo} | {pattern} | {fit} | {priority} | {use} | {source} |".format(
                    id=row["id"],
                    door=md_cell(row["door"]),
                    repo=md_cell(row["repo"]),
                    pattern=md_cell(row["primary_pattern"]),
                    fit=md_cell(row["fit"]),
                    priority=row["priority"],
                    use=md_cell(row["browse_use"]),
                    source=md_cell(row["source_url"]),
                )
            )

    lines.extend(
        [
            "",
            "## Full Machine-Readable Files",
            "",
            f"- JSON: `{CATALOG_JSON_PATH.relative_to(ROOT)}`",
            f"- CSV: `{CATALOG_CSV_PATH.relative_to(ROOT)}`",
        ]
    )

    CATALOG_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    router = json.loads(ROUTER_PATH.read_text(encoding="utf-8"))
    rows = enriched_rows(router["rows"])
    write_json(rows)
    write_csv(rows)
    write_report(rows)
    print(f"Wrote {len(rows)} doors")
    print(CATALOG_JSON_PATH)
    print(CATALOG_CSV_PATH)
    print(CATALOG_REPORT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
