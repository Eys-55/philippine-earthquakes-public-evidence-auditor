#!/usr/bin/env python3
"""Query the clean workflow search index."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "agentic-repos" / "workflow-search-index.json"

QUERY_EXPANSIONS = {
    "health": ["healthcare", "healthcare_admin", "document_transformation", "compliance_human_review"],
    "healthcare": ["healthcare", "healthcare_admin", "document_transformation", "compliance_human_review"],
    "medical": ["healthcare", "healthcare_admin"],
    "patient": ["healthcare", "healthcare_admin", "document_transformation"],
    "referral": ["healthcare", "document_transformation", "case_intake_review"],
    "education": ["education", "education_support"],
    "student": ["education", "education_support"],
    "real estate": ["real_estate", "evidence_due_diligence"],
    "property": ["real_estate", "evidence_due_diligence"],
    "due diligence": ["evidence_due_diligence", "real_estate", "public_evidence"],
    "public evidence": ["public_evidence", "evidence_due_diligence", "source_taxonomy"],
    "permit": ["public_evidence", "evidence_due_diligence", "compliance_human_review"],
    "document": ["document_processing", "document_transformation"],
    "pdf": ["document_processing", "document_transformation"],
    "ocr": ["document_processing", "document_transformation"],
    "human review": ["compliance_human_review", "case_intake_review"],
    "approval": ["compliance_human_review", "case_intake_review"],
    "case intake": ["case_intake_review", "legal_casework"],
    "legal": ["legal_casework", "case_intake_review"],
    "automation": ["automation", "automation_queue"],
    "queue": ["automation_queue", "automation"],
    "monitoring": ["monitoring", "automation_queue"],
    "research": ["research", "research_knowledge"],
    "codex": ["codex_config_candidate", "config_package_registry", "skill_package_reference"],
    "config package": ["codex_config_candidate", "config_package_registry"],
    "skill": ["skill_package_reference", "config_package_registry"],
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "find",
    "like",
    "me",
    "my",
    "of",
    "the",
    "to",
    "workflow",
    "workflows",
}

TIER_WEIGHT = {"gold": 14, "silver": 9, "bronze": 4, "needs_verification": 0}
USEFULNESS_WEIGHT = {
    "copy_or_adapt_now": 10,
    "strong_reference": 7,
    "translate_pattern_only": 4,
    "use_with_caution": 2,
    "verify_source_first": 0,
}


def tokenize(value: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", value.lower()) if len(token) > 1 and token not in STOPWORDS]


def expand_terms(query: str) -> list[str]:
    normalized = query.lower()
    expanded: list[str] = []
    for phrase, terms in QUERY_EXPANSIONS.items():
        if phrase in normalized:
            expanded.extend(terms)
    return list(dict.fromkeys(expanded))


def score_row(row: dict[str, Any], tokens: list[str], expanded: list[str], include_low: bool) -> tuple[int, list[str]]:
    if not include_low and row["quality_tier"] == "needs_verification":
        return 0, []

    haystack = row["searchable_text"]
    score = TIER_WEIGHT.get(row["quality_tier"], 0) + USEFULNESS_WEIGHT.get(row["codex_usefulness"], 0)
    reasons: list[str] = []

    for term in expanded:
        if term in {
            row["normalized_domain"],
            row["workflow_family"],
            row["fit"],
            row["quality_tier"],
            row["codex_usefulness"],
        }:
            score += 18
            reasons.append(term)
        elif term in haystack:
            score += 10
            reasons.append(term)

    for token in tokens:
        if token in haystack:
            score += 3
            if len(reasons) < 8:
                reasons.append(token)

    if row["source_url_status"] in {"exact_page_reachable", "canonicalized"}:
        score += 3
    if row["confidence"] in {"high", "medium-high"}:
        score += 4

    return score, sorted(set(reasons))


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def format_markdown(matches: list[dict[str, Any]]) -> str:
    lines = [
        "| Rank | ID | Workflow | Repo | Domain | Family | Tier | Usefulness | Copy | Source |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, item in enumerate(matches, start=1):
        row = item["row"]
        lines.append(
            "| {rank} | {id} | {name} | {repo} | {domain} | {family} | {tier} | {usefulness} | {copy} | {source} |".format(
                rank=index,
                id=row["workflow_id"],
                name=md_cell(row["workflow_name"]),
                repo=md_cell(row["source_repo"]),
                domain=row["normalized_domain"],
                family=row["workflow_family"],
                tier=row["quality_tier"],
                usefulness=row["codex_usefulness"],
                copy=md_cell(row["what_to_copy"][:160]),
                source=md_cell(row["canonical_source_url"]),
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--domain")
    parser.add_argument("--family")
    parser.add_argument("--include-low", action="store_true", help="Include needs_verification rows")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    tokens = tokenize(args.query)
    expanded = expand_terms(args.query)
    matches = []
    for row in payload["rows"]:
        if args.domain and row["normalized_domain"] != args.domain:
            continue
        if args.family and row["workflow_family"] != args.family:
            continue
        score, reasons = score_row(row, tokens, expanded, args.include_low)
        if score > 0 and (reasons or not tokens):
            matches.append({"score": score, "reasons": reasons, "row": row})

    matches.sort(
        key=lambda item: (
            -item["score"],
            ["gold", "silver", "bronze", "needs_verification"].index(item["row"]["quality_tier"]),
            item["row"]["source_repo"],
            item["row"]["workflow_name"],
        )
    )
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
