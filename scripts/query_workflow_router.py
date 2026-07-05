#!/usr/bin/env python3
"""Query the workflow router and return ranked workflow surfaces."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "data" / "agentic-repos" / "workflow-router.json"


QUERY_EXPANSIONS = {
    "earthquake": ["public_evidence", "real_estate", "document_processing", "EvidenceAudit", "DueDiligence", "ComplianceSupport", "HumanReview"],
    "building": ["public_evidence", "real_estate", "EvidenceAudit", "DueDiligence"],
    "permit": ["public_evidence", "real_estate", "EvidenceAudit", "DueDiligence"],
    "health": ["healthcare", "document_processing", "HealthcareAdmin", "ComplianceSupport", "HumanReview"],
    "healthcare": ["healthcare", "document_processing", "HealthcareAdmin", "ComplianceSupport", "HumanReview"],
    "patient": ["healthcare", "document_processing", "HealthcareAdmin", "DocumentTransformation", "HumanReview"],
    "referral": ["healthcare", "document_processing", "HealthcareAdmin", "DocumentTransformation", "HumanReview"],
    "education": ["education", "EducationSupport"],
    "student": ["education", "EducationSupport"],
    "real estate": ["real_estate", "public_evidence", "DueDiligence", "EvidenceAudit", "DocumentTransformation"],
    "property": ["real_estate", "public_evidence", "DueDiligence", "EvidenceAudit"],
    "due diligence": ["real_estate", "public_evidence", "DueDiligence", "EvidenceAudit", "ComplianceSupport"],
    "document": ["document_processing", "DocumentTransformation", "HumanReview"],
    "pdf": ["document_processing", "DocumentTransformation"],
    "human review": ["HumanReview", "ComplianceSupport", "document_processing"],
    "compliance": ["ComplianceSupport", "HumanReview", "public_evidence"],
    "monitoring": ["Monitoring", "QueueProcessing"],
    "automation": ["automation", "AutomationTemplate", "QueueProcessing"],
    "codex": ["ConfigPackage", "SkillRegistry", "Codex-native or Codex-adjacent"],
    "config package": ["ConfigPackage", "SkillRegistry", "Codex-native or Codex-adjacent"],
}

STOPWORDS = {
    "agent",
    "agents",
    "find",
    "like",
    "me",
    "my",
    "thing",
    "workflow",
    "workflows",
}


def tokenize(value: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", value.lower()) if len(token) > 1 and token not in STOPWORDS]


def build_query_terms(query: str) -> tuple[list[str], list[str]]:
    normalized = query.lower()
    tokens = tokenize(query)
    expanded: list[str] = []
    for phrase, values in QUERY_EXPANSIONS.items():
        if phrase in normalized:
            expanded.extend(values)
    return tokens, list(dict.fromkeys(expanded))


def score_row(row: dict[str, Any], query: str, tokens: list[str], expanded: list[str]) -> tuple[int, list[str]]:
    haystack_fields = [
        row["surface_name"],
        row["repo"],
        row["surface_level"],
        row["codex_fit"],
        row["input_contract_hint"],
        row["output_artifact_hint"],
        row["human_review_boundary"],
        row["safety_boundary"],
        " ".join(row["domain_tags"]),
        " ".join(row["workflow_pattern_tags"]),
    ]
    haystack = " ".join(haystack_fields).lower()
    score = 0
    reasons: list[str] = []
    expanded_match = False

    for token in tokens:
        if token in haystack:
            score += 2
            if len(reasons) < 4:
                reasons.append(f"text:{token}")

    for term in expanded:
        if term in row["domain_tags"]:
            score += 8
            reasons.append(f"domain:{term}")
            expanded_match = True
        elif term in row["workflow_pattern_tags"]:
            score += 8
            reasons.append(f"pattern:{term}")
            expanded_match = True
        elif term.lower() in row["codex_fit"].lower():
            score += 5
            reasons.append(f"fit:{term}")
            expanded_match = True

    # Prefer high-priority doors, but do not hide exact query matches.
    score += {1: 6, 2: 3, 3: 0}.get(row["expand_priority"], 0)

    if row["needs_second_pass"]:
        score += 1

    # A direct phrase match is strong.
    query_lower = query.lower()
    if query_lower and query_lower in row["surface_name"].lower():
        score += 10
        reasons.append("surface-name")
        expanded_match = True

    if expanded and not expanded_match:
        return 0, []

    return score, sorted(set(reasons))


def format_markdown(matches: list[dict[str, Any]]) -> str:
    lines = [
        "| Rank | Surface | Repo | Domains | Patterns | Fit | Priority | Expand |",
        "| ---: | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for index, item in enumerate(matches, start=1):
        row = item["row"]
        lines.append(
            "| {rank} | {surface} | {repo} | {domains} | {patterns} | {fit} | {priority} | {expand} |".format(
                rank=index,
                surface=md_cell(row["surface_name"]),
                repo=row["repo"],
                domains=", ".join(row["domain_tags"]),
                patterns=", ".join(row["workflow_pattern_tags"]),
                fit=md_cell(row["codex_fit"]),
                priority=row["expand_priority"],
                expand=md_cell(row["expand_when"]),
            )
        )
    return "\n".join(lines)


def md_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    payload = json.loads(ROUTER_PATH.read_text(encoding="utf-8"))
    tokens, expanded = build_query_terms(args.query)
    matches = []
    for row in payload["rows"]:
        score, reasons = score_row(row, args.query, tokens, expanded)
        if score > 0:
            matches.append({"score": score, "reasons": reasons, "row": row})

    matches.sort(key=lambda item: (-item["score"], item["row"]["expand_priority"], item["row"]["repo"], item["row"]["surface_name"]))
    matches = matches[: args.limit]

    if args.json:
        print(json.dumps({"query": args.query, "expanded_terms": expanded, "matches": matches}, indent=2))
    else:
        print(f"Query: {args.query}")
        print(f"Expanded terms: {', '.join(expanded) if expanded else '(none)'}")
        print()
        print(format_markdown(matches))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
