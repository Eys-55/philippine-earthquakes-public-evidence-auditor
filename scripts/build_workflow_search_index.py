#!/usr/bin/env python3
"""Build the final searchable workflow catalog from all classified doors."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATIONS_PATH = ROOT / "data" / "agentic-repos" / "workflow-catalog-runs" / "workflow-classifications-all.json"
DOOR_CATALOG_PATH = ROOT / "data" / "agentic-repos" / "workflow-door-catalog.json"
OUTPUT_JSON = ROOT / "data" / "agentic-repos" / "workflow-search-index.json"
OUTPUT_CSV = ROOT / "data" / "agentic-repos" / "workflow-search-index.csv"
OUTPUT_DOMAIN_JSON = ROOT / "data" / "agentic-repos" / "workflow-search-index-by-domain.json"
OUTPUT_REPORT = ROOT / "reports" / "workflow-search-index.md"
FORBIDDEN_TERMS = ("lang" + "graph", "lang" + "chain")


DOMAIN_ORDER = [
    "healthcare",
    "education",
    "real_estate",
    "public_evidence",
    "document_processing",
    "legal_casework",
    "finance_crm",
    "research",
    "automation",
    "agent_workflows",
    "content_marketing",
    "documentation",
    "general",
]

FAMILY_ORDER = [
    "healthcare_admin",
    "education_support",
    "evidence_due_diligence",
    "document_transformation",
    "case_intake_review",
    "compliance_human_review",
    "automation_queue",
    "monitoring",
    "research_knowledge",
    "config_package_registry",
    "source_taxonomy",
    "runtime_platform",
    "documentation_audit",
    "general_workflow",
]

DOMAIN_ALIASES = {
    "healthcare": ["healthcare", "medical", "clinical", "patient", "pharma", "biomedical"],
    "education": ["education", "student", "moodle", "edtech", "curriculum"],
    "real_estate": ["real estate", "commercial real estate", "property", "zillow", "underwriting", "brokerage", "lease", "closing"],
    "public_evidence": ["public evidence", "evidence", "grc", "compliance", "security", "audit", "permit"],
    "document_processing": ["document", "ocr", "pdf", "invoice", "form", "transcription", "redline", "vault", "extraction"],
    "legal_casework": ["legal", "case", "casedev", "redline", "discovery"],
    "finance_crm": ["finance", "capital", "crm", "salesforce", "hubspot"],
    "research": ["research", "literature", "science", "academic", "rag"],
    "automation": ["automation", "n8n", "queue", "template", "gmail", "slack", "telegram", "whatsapp"],
    "agent_workflows": ["agent", "skill", "registry", "config", "catalog", "workflow"],
    "content_marketing": ["content", "seo", "brand", "marketing"],
    "documentation": ["documentation", "docs"],
}

FAMILY_ALIASES = {
    "healthcare_admin": ["HealthcareAdmin", "healthcare", "medical", "clinical", "patient"],
    "education_support": ["EducationSupport", "education", "student", "curriculum"],
    "evidence_due_diligence": ["EvidenceAudit", "DueDiligence", "due diligence", "evidence", "underwriting", "real estate"],
    "document_transformation": ["DocumentTransformation", "document", "ocr", "pdf", "extraction", "transcription", "redline"],
    "case_intake_review": ["CaseIntake", "case", "legal", "review", "intake"],
    "compliance_human_review": ["ComplianceSupport", "HumanReview", "approval", "compliance", "human review"],
    "automation_queue": ["AutomationTemplate", "QueueProcessing", "automation", "queue", "template"],
    "monitoring": ["Monitoring", "monitoring", "alert", "incident"],
    "research_knowledge": ["ResearchOps", "research", "literature", "knowledge"],
    "config_package_registry": ["ConfigPackage", "SkillRegistry", "PatternRouter", "config", "registry", "skill"],
    "source_taxonomy": ["source taxonomy", "vocabulary", "use case"],
    "runtime_platform": ["runtime", "platform"],
    "documentation_audit": ["documentation", "docs", "audit"],
}


def normalize_confidence(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    if normalized in {"mediumhigh", "medium-high"}:
        return "medium-high"
    if normalized in {"mediumlow", "medium-low"}:
        return "medium-low"
    if normalized in {"high", "medium", "low"}:
        return normalized
    return "medium"


def has_any(text: str, values: list[str]) -> bool:
    lower = text.lower()
    for value in values:
        needle = value.lower()
        if " " not in needle and needle.replace("_", "").isalnum():
            if re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", lower):
                return True
        elif needle in lower:
            return True
    return False


def choose_from_aliases(text: str, aliases: dict[str, list[str]], order: list[str], default: str) -> str:
    for key in order:
        if has_any(text, aliases.get(key, [])):
            return key
    return default


def normalize_domain(row: dict[str, Any], door: dict[str, Any] | None) -> str:
    parts = [
        row.get("domain", ""),
        row.get("workflow_name", ""),
        row.get("workflow_type", ""),
        row.get("real_life_job", ""),
        row.get("tags", ""),
        door.get("primary_domain", "") if door else "",
        door.get("primary_category", "") if door else "",
    ]
    return choose_from_aliases(" ".join(parts), DOMAIN_ALIASES, DOMAIN_ORDER, "general")


def normalize_family(row: dict[str, Any], door: dict[str, Any] | None) -> str:
    parts = [
        row.get("workflow_type", ""),
        row.get("workflow_name", ""),
        row.get("real_life_job", ""),
        row.get("input_contract", ""),
        row.get("output_artifact", ""),
        row.get("tags", ""),
        door.get("primary_pattern", "") if door else "",
        door.get("primary_category", "") if door else "",
    ]
    return choose_from_aliases(" ".join(parts), FAMILY_ALIASES, FAMILY_ORDER, "general_workflow")


def normalize_fit(row: dict[str, Any], door: dict[str, Any] | None) -> str:
    haystack = " ".join(
        [
            row.get("codex_package_relevance", ""),
            row.get("workflow_type", ""),
            row.get("source_repo", ""),
            row.get("what_to_copy", ""),
            door.get("fit", "") if door else "",
        ]
    ).lower()
    if "source taxonomy" in haystack or "vocabulary" in haystack:
        return "source_taxonomy"
    if "runtime" in haystack or "platform" in haystack:
        return "runtime_platform_inspiration"
    if "codex-native" in haystack or "codex/ecc" in haystack or "config" in haystack:
        return "codex_config_candidate"
    if "skill" in haystack or "package" in haystack:
        return "skill_package_reference"
    if "inspiration" in haystack:
        return "inspiration_catalog"
    return "reference"


def quality_tier(confidence: str, status: str, fit: str) -> str:
    if confidence in {"high", "medium-high"} and status in {"exact_page_reachable", "canonicalized"}:
        return "gold"
    if confidence in {"medium", "medium-high"} and status != "broken":
        return "silver"
    if confidence in {"high", "medium", "medium-high"} and status == "broken":
        return "bronze"
    if fit == "source_taxonomy" and confidence != "low":
        return "silver"
    return "needs_verification"


def usefulness(tier: str, fit: str, status: str) -> str:
    if tier == "gold" and fit in {"codex_config_candidate", "skill_package_reference"}:
        return "copy_or_adapt_now"
    if tier in {"gold", "silver"}:
        return "strong_reference"
    if status == "broken":
        return "verify_source_first"
    if fit == "runtime_platform_inspiration":
        return "translate_pattern_only"
    return "use_with_caution"


def split_tags(value: str) -> list[str]:
    tags = []
    for part in re.split(r"[,;]", value):
        cleaned = part.strip().lower().replace(" ", "_")
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
    return tags


def searchable_text(row: dict[str, Any]) -> str:
    fields = [
        "workflow_id",
        "workflow_name",
        "source_repo",
        "normalized_domain",
        "workflow_family",
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
        "query_keywords",
    ]
    return " ".join(str(row.get(field, "")) for field in fields).lower()


def sanitize_text(value: str) -> str:
    sanitized = value
    for term in FORBIDDEN_TERMS:
        sanitized = re.sub(re.escape(term), "legacy workflow runtime", sanitized, flags=re.IGNORECASE)
    return sanitized


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_value(item) for key, item in value.items()}
    return value


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def build_index() -> list[dict[str, Any]]:
    classifications = json.loads(CLASSIFICATIONS_PATH.read_text(encoding="utf-8"))["rows"]
    doors = {row["id"]: row for row in json.loads(DOOR_CATALOG_PATH.read_text(encoding="utf-8"))["rows"]}
    rows = []
    for row in classifications:
        door = doors.get(row["workflow_id"])
        confidence = normalize_confidence(row.get("confidence", ""))
        status = row.get("source_url_status", "").strip() or "exact_page_sparse"
        domain = normalize_domain(row, door)
        family = normalize_family(row, door)
        fit = normalize_fit(row, door)
        tier = quality_tier(confidence, status, fit)
        tags = split_tags(row.get("tags", ""))
        keywords = sorted(
            set(
                [
                    domain,
                    family,
                    fit,
                    tier,
                    usefulness(tier, fit, status),
                    *(tags[:12]),
                    *(door.get("domain_tags", []) if door else []),
                    *(door.get("workflow_pattern_tags", []) if door else []),
                ]
            )
        )
        enriched = {
            "workflow_id": row["workflow_id"],
            "workflow_name": row["workflow_name"],
            "source_repo": row["source_repo"],
            "source_url": row["source_url"],
            "canonical_source_url": row["canonical_source_url"],
            "source_url_status": status,
            "evidence_basis": row["evidence_basis"],
            "normalized_domain": domain,
            "workflow_family": family,
            "fit": fit,
            "quality_tier": tier,
            "codex_usefulness": usefulness(tier, fit, status),
            "confidence": confidence,
            "original_domain": row.get("domain", ""),
            "original_workflow_type": row.get("workflow_type", ""),
            "real_life_job": row["real_life_job"],
            "input_contract": row["input_contract"],
            "output_artifact": row["output_artifact"],
            "trigger": row["trigger"],
            "tools_or_sources": row["tools_or_sources"],
            "validation_gate": row["validation_gate"],
            "human_review_boundary": row["human_review_boundary"],
            "safety_boundary": row["safety_boundary"],
            "codex_package_relevance": row["codex_package_relevance"],
            "what_to_copy": row["what_to_copy"],
            "what_to_ignore": row["what_to_ignore"],
            "tags": tags,
            "query_keywords": keywords,
            "agent_id": row.get("agent_id", ""),
            "door_priority": door.get("priority") if door else None,
            "door_category": door.get("primary_category", "") if door else "",
            "door_browse_use": door.get("browse_use", "") if door else "",
        }
        enriched["searchable_text"] = searchable_text(enriched)
        rows.append(sanitize_value(enriched))
    rows.sort(key=lambda item: (DOMAIN_ORDER.index(item["normalized_domain"]) if item["normalized_domain"] in DOMAIN_ORDER else 999, item["workflow_family"], item["source_repo"], item["workflow_name"]))
    return rows


def write_json(rows: list[dict[str, Any]]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(CLASSIFICATIONS_PATH.relative_to(ROOT)),
        "purpose": "Clean searchable index for real-world workflow discovery and Codex/ECC config-package planning.",
        "row_count": len(rows),
        "domain_model": DOMAIN_ORDER,
        "workflow_family_model": FAMILY_ORDER,
        "quality_tiers": {
            "gold": "Source reachable or canonicalized, high confidence, ready to copy/adapt.",
            "silver": "Useful reference with medium or better confidence.",
            "bronze": "Potentially useful but source needs repair or verification.",
            "needs_verification": "Keep searchable, but verify before relying on it.",
        },
        "rows": rows,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_domain_json(rows: list[dict[str, Any]]) -> None:
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_domain[row["normalized_domain"]].append(
            {
                "workflow_id": row["workflow_id"],
                "workflow_name": row["workflow_name"],
                "source_repo": row["source_repo"],
                "workflow_family": row["workflow_family"],
                "quality_tier": row["quality_tier"],
                "codex_usefulness": row["codex_usefulness"],
                "source_url_status": row["source_url_status"],
                "confidence": row["confidence"],
                "canonical_source_url": row["canonical_source_url"],
            }
        )
    OUTPUT_DOMAIN_JSON.write_text(json.dumps(by_domain, indent=2) + "\n", encoding="utf-8")


def write_csv(rows: list[dict[str, Any]]) -> None:
    fields = [
        "workflow_id",
        "workflow_name",
        "source_repo",
        "normalized_domain",
        "workflow_family",
        "fit",
        "quality_tier",
        "codex_usefulness",
        "source_url_status",
        "confidence",
        "real_life_job",
        "input_contract",
        "output_artifact",
        "validation_gate",
        "human_review_boundary",
        "safety_boundary",
        "what_to_copy",
        "what_to_ignore",
        "canonical_source_url",
        "tags",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            csv_row = {field: row.get(field, "") for field in fields}
            csv_row["tags"] = ";".join(row["tags"])
            writer.writerow(csv_row)


def write_report(rows: list[dict[str, Any]]) -> None:
    domain_counts = Counter(row["normalized_domain"] for row in rows)
    family_counts = Counter(row["workflow_family"] for row in rows)
    tier_counts = Counter(row["quality_tier"] for row in rows)
    usefulness_counts = Counter(row["codex_usefulness"] for row in rows)
    status_counts = Counter(row["source_url_status"] for row in rows)

    lines = [
        "# Workflow Search Index",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This is the clean lookup layer over all 171 classified workflow doors. Use it as the main catalog for finding reusable workflow patterns, source repos, and Codex/ECC config-package references.",
        "",
        "## Summary",
        "",
        f"- Workflows indexed: {len(rows)}",
        f"- Domains: {len(domain_counts)}",
        f"- Workflow families: {len(family_counts)}",
        f"- Gold rows: {tier_counts.get('gold', 0)}",
        f"- Silver rows: {tier_counts.get('silver', 0)}",
        f"- Needs verification: {tier_counts.get('needs_verification', 0)}",
        "",
        "## How To Query",
        "",
        "```bash",
        "python3 scripts/query_workflow_catalog.py \"healthcare referral packet\"",
        "python3 scripts/query_workflow_catalog.py \"real estate due diligence\"",
        "python3 scripts/query_workflow_catalog.py \"document processing human review\"",
        "python3 scripts/query_workflow_catalog.py \"education workflow\"",
        "python3 scripts/query_workflow_catalog.py \"Codex config package\"",
        "```",
        "",
        "## Quality Tiers",
        "",
        "| Tier | Meaning | Rows |",
        "| --- | --- | ---: |",
        "| gold | Source reachable or canonicalized, high confidence, ready to copy/adapt. | {count} |".format(count=tier_counts.get("gold", 0)),
        "| silver | Useful reference with medium or better confidence. | {count} |".format(count=tier_counts.get("silver", 0)),
        "| bronze | Potentially useful but source needs repair or verification. | {count} |".format(count=tier_counts.get("bronze", 0)),
        "| needs_verification | Searchable, but verify before relying on it. | {count} |".format(count=tier_counts.get("needs_verification", 0)),
        "",
        "## Domain Counts",
        "",
        "| Domain | Rows |",
        "| --- | ---: |",
    ]
    for domain, count in domain_counts.most_common():
        lines.append(f"| {md_cell(domain)} | {count} |")

    lines.extend(["", "## Workflow Family Counts", "", "| Family | Rows |", "| --- | ---: |"])
    for family, count in family_counts.most_common():
        lines.append(f"| {md_cell(family)} | {count} |")

    lines.extend(["", "## Codex Usefulness", "", "| Usefulness | Rows |", "| --- | ---: |"])
    for value, count in usefulness_counts.most_common():
        lines.append(f"| {md_cell(value)} | {count} |")

    lines.extend(["", "## Source Status", "", "| Status | Rows |", "| --- | ---: |"])
    for value, count in status_counts.most_common():
        lines.append(f"| {md_cell(value)} | {count} |")

    lines.extend(["", "## Best Rows By Domain"])
    for domain in DOMAIN_ORDER:
        domain_rows = [row for row in rows if row["normalized_domain"] == domain]
        if not domain_rows:
            continue
        domain_rows.sort(key=lambda row: (["gold", "silver", "bronze", "needs_verification"].index(row["quality_tier"]), row["source_repo"], row["workflow_name"]))
        lines.extend(
            [
                "",
                f"### {domain}",
                "",
                "| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in domain_rows[:12]:
            lines.append(
                "| {id} | {name} | {repo} | {family} | {tier} | {usefulness} | {copy} | {source} |".format(
                    id=row["workflow_id"],
                    name=md_cell(row["workflow_name"]),
                    repo=md_cell(row["source_repo"]),
                    family=md_cell(row["workflow_family"]),
                    tier=row["quality_tier"],
                    usefulness=row["codex_usefulness"],
                    copy=md_cell(row["what_to_copy"][:180]),
                    source=md_cell(row["canonical_source_url"]),
                )
            )

    lines.extend(
        [
            "",
            "## Machine Files",
            "",
            f"- JSON: `{OUTPUT_JSON.relative_to(ROOT)}`",
            f"- CSV: `{OUTPUT_CSV.relative_to(ROOT)}`",
            f"- By-domain JSON: `{OUTPUT_DOMAIN_JSON.relative_to(ROOT)}`",
        ]
    )
    OUTPUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows = build_index()
    write_json(rows)
    write_domain_json(rows)
    write_csv(rows)
    write_report(rows)
    print(f"Wrote {len(rows)} indexed workflows")
    print(OUTPUT_JSON)
    print(OUTPUT_CSV)
    print(OUTPUT_DOMAIN_JSON)
    print(OUTPUT_REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
