#!/usr/bin/env python3
"""Validate V2 Gate 3 earthquake evidence packet schema and fixtures."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
V2_DATA_DIR = ROOT / "data/philippines-building-code-evidence-auditor-v2"
SCHEMA_PATH = V2_DATA_DIR / "evidence-packet-schema.json"
FIXTURE_DIR = V2_DATA_DIR / "evidence-packet-fixtures"
GATE3_POINTER_PATH = V2_DATA_DIR / "gate-3-sm-moa-document-target-matrix.json"

REQUIRED_FIELDS = [
    "confirmed_building",
    "locked_earthquake_lane",
    "document_inventory",
    "evidence_strength",
    "source_curation_class",
    "physical_condition_public_evidence",
    "unresolved_exceptions",
    "manual_request_targets",
    "overclaim_boundary",
    "query_log",
    "packet_result",
]

ALLOWED_LANES = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review_evidence",
    "post_earthquake_tag_status",
    "clearance_after_damage_or_tag",
}

EVIDENCE_EXISTENCE_LANES = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review_evidence",
}

STATUS_ANSWER_LANES = {
    "post_earthquake_tag_status",
    "clearance_after_damage_or_tag",
}

ALLOWED_EVIDENCE_STRENGTHS = {
    "direct_authoritative_target_evidence",
    "professional_target_evidence",
    "strong_indirect_target_evidence",
    "process_or_standards_context",
    "weak_lead_only",
    "not_found_after_reasonable_search",
}

ALLOWED_SOURCE_CLASSES = {
    "official_record",
    "professional_record",
    "operator_corporate_claim",
    "reputable_news_lead",
    "process_context",
    "weak_lead",
}

INELIGIBLE_POSITIVE_EVIDENCE_STRENGTHS = {
    "process_or_standards_context",
    "weak_lead_only",
    "not_found_after_reasonable_search",
}

INELIGIBLE_POSITIVE_SOURCE_CLASSES = {
    "process_context",
    "weak_lead",
    "reputable_news_lead",
}

ALLOWED_TARGET_MATCH_STATUSES = {
    "exact_target_match",
    "process_context_only",
    "weak_target_lead",
    "no_target_match",
}

NO_EVIDENCE_RESULT_STATUSES = {
    "no_public_evidence_found",
    "no_public_answer_found",
}

FORBIDDEN_MISSING_EVIDENCE_PHRASES = {
    "earthquake safe",
    "earthquake unsafe",
    "is safe",
    "is unsafe",
    "safe for occupancy",
    "unsafe for occupancy",
    "is compliant",
    "is noncompliant",
    "non-compliant",
    "no tag",
    "no tag exists",
    "is cleared",
    "has clearance",
    "no permit exists",
    "not reviewed",
    "unpermitted",
}

FORBIDDEN_MISSING_EVIDENCE_STATUS_CONCLUSIONS = {
    "cleared",
    "clear",
    "open",
    "opened",
    "reopened",
    "closed",
    "operational",
    "reoccupied",
    "occupied",
    "vacant",
    "usable",
    "unusable",
}

FORBIDDEN_V1_TERMS = {
    "business permit",
    "Broad public",
    "permit_occupancy_records",
    "contractor_professional_developer",
    "standards_context_only",
    "broad_public_evidence_packet",
}

POINTER_ALLOWED_KEYS = {
    "schema_version",
    "workflow_gate",
    "status",
    "canonical_file",
    "purpose",
    "active_scope_ids",
    "required_packet_fields",
    "guardrail",
}

POINTER_FORBIDDEN_ACTIVE_KEYS = {
    "document_targets",
    "agent_results",
    "query_patterns_that_worked",
    "source_reality_status_values",
    "target",
    "run_type",
    "global_safety_rule",
    "matrix",
    "cases",
    "document_inventory",
    "packet_result",
}


def fail(message: str) -> int:
    print(f"building-code v2 evidence packet validation failed: {message}", file=sys.stderr)
    return 1


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def require_object(value: object, path: str, errors: list[str]) -> dict | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: must be an object")
        return None
    return value


def require_array(value: object, path: str, errors: list[str]) -> list | None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return None
    return value


def expect_string(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")


def normalize_for_boundary_check(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return re.sub(r"\s+", " ", normalized).strip()


def contains_normalized_phrase(text: str, phrase: str) -> bool:
    normalized_text = normalize_for_boundary_check(text)
    normalized_phrase = normalize_for_boundary_check(phrase)
    if not normalized_phrase:
        return False
    return re.search(rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)", normalized_text) is not None


def validate_schema(schema: object, errors: list[str]) -> None:
    obj = require_object(schema, "schema", errors)
    if obj is None:
        return
    required = obj.get("required")
    if required != REQUIRED_FIELDS:
        errors.append("schema.required: must equal the V2 Gate 3 required field list")

    properties = obj.get("properties")
    prop_obj = require_object(properties, "schema.properties", errors)
    if prop_obj is not None:
        missing = sorted(set(REQUIRED_FIELDS) - set(prop_obj))
        if missing:
            errors.append(f"schema.properties: missing required field definitions {missing}")

        lane_enum = (
            prop_obj.get("locked_earthquake_lane", {})
            if isinstance(prop_obj.get("locked_earthquake_lane"), dict)
            else {}
        ).get("enum")
        if set(lane_enum or []) != ALLOWED_LANES:
            errors.append("schema.locked_earthquake_lane.enum: must match the four V2 lanes exactly")

    defs = obj.get("$defs")
    defs_obj = require_object(defs, "schema.$defs", errors)
    if defs_obj is None:
        return

    evidence_enum = (
        defs_obj.get("evidence_strength", {})
        if isinstance(defs_obj.get("evidence_strength"), dict)
        else {}
    ).get("enum")
    if set(evidence_enum or []) != ALLOWED_EVIDENCE_STRENGTHS:
        errors.append("schema.evidence_strength.enum: must match allowed values exactly")

    source_enum = (
        defs_obj.get("source_curation_class", {})
        if isinstance(defs_obj.get("source_curation_class"), dict)
        else {}
    ).get("enum")
    if set(source_enum or []) != ALLOWED_SOURCE_CLASSES:
        errors.append("schema.source_curation_class.enum: must match allowed values exactly")


def validate_confirmed_building(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"display_name", "candidate_id", "city", "country", "gate_1_status"}
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing keys {missing}")
    for key in ("display_name", "candidate_id", "city"):
        expect_string(obj.get(key), f"{path}.{key}", errors)
    if obj.get("country") != "Philippines":
        errors.append(f"{path}.country: must be 'Philippines'")
    if obj.get("gate_1_status") != "confirmed_by_user":
        errors.append(f"{path}.gate_1_status: must be 'confirmed_by_user'")


def validate_evidence_item(item: object, path: str, errors: list[str]) -> None:
    obj = require_object(item, path, errors)
    if obj is None:
        return
    required = {
        "item_id",
        "description",
        "evidence_strength",
        "source_curation_class",
        "is_positive_evidence",
        "target_match_status",
    }
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing keys {missing}")
    for key in ("item_id", "description", "target_match_status"):
        expect_string(obj.get(key), f"{path}.{key}", errors)
    if obj.get("evidence_strength") not in ALLOWED_EVIDENCE_STRENGTHS:
        errors.append(f"{path}.evidence_strength: unsupported value {obj.get('evidence_strength')!r}")
    if obj.get("source_curation_class") not in ALLOWED_SOURCE_CLASSES:
        errors.append(f"{path}.source_curation_class: unsupported value {obj.get('source_curation_class')!r}")
    if not isinstance(obj.get("is_positive_evidence"), bool):
        errors.append(f"{path}.is_positive_evidence: must be boolean")
    if obj.get("target_match_status") not in ALLOWED_TARGET_MATCH_STATUSES:
        errors.append(f"{path}.target_match_status: unsupported value {obj.get('target_match_status')!r}")
    if obj.get("is_positive_evidence") is True and not is_http_url(obj.get("source_url")):
        errors.append(f"{path}.source_url: positive evidence claims must include an http(s) source_url")


def validate_evidence_array(value: object, path: str, errors: list[str]) -> None:
    items = require_array(value, path, errors)
    if items is None:
        return
    for index, item in enumerate(items):
        validate_evidence_item(item, f"{path}[{index}]", errors)


def is_eligible_positive_evidence_item(item: dict) -> bool:
    return (
        item.get("is_positive_evidence") is True
        and is_http_url(item.get("source_url"))
        and item.get("target_match_status") == "exact_target_match"
        and item.get("evidence_strength") not in INELIGIBLE_POSITIVE_EVIDENCE_STRENGTHS
        and item.get("source_curation_class") not in INELIGIBLE_POSITIVE_SOURCE_CLASSES
    )


def validate_query_log(value: object, path: str, errors: list[str]) -> None:
    entries = require_array(value, path, errors)
    if entries is None:
        return
    for index, entry in enumerate(entries):
        obj = require_object(entry, f"{path}[{index}]", errors)
        if obj is None:
            continue
        for key in ("query", "searched_surface", "result_summary"):
            expect_string(obj.get(key), f"{path}[{index}].{key}", errors)
        if obj.get("source_url") is not None and not is_http_url(obj.get("source_url")):
            errors.append(f"{path}[{index}].source_url: must be null or http(s) URL")


def validate_unresolved_exceptions(value: object, path: str, errors: list[str]) -> None:
    entries = require_array(value, path, errors)
    if entries is None:
        return
    for index, entry in enumerate(entries):
        obj = require_object(entry, f"{path}[{index}]", errors)
        if obj is None:
            continue
        for key in ("exception_id", "description", "resolution_route"):
            expect_string(obj.get(key), f"{path}[{index}].{key}", errors)


def validate_manual_targets(value: object, path: str, errors: list[str]) -> None:
    entries = require_array(value, path, errors)
    if entries is None:
        return
    for index, entry in enumerate(entries):
        obj = require_object(entry, f"{path}[{index}]", errors)
        if obj is None:
            continue
        for key in ("target", "request"):
            expect_string(obj.get(key), f"{path}[{index}].{key}", errors)


def validate_result_and_boundary(packet: dict, path: str, errors: list[str]) -> None:
    result = require_object(packet.get("packet_result"), f"{path}.packet_result", errors)
    boundary = require_object(packet.get("overclaim_boundary"), f"{path}.overclaim_boundary", errors)
    if result is None or boundary is None:
        return

    status = result.get("status")
    if status not in {"no_public_evidence_found", "no_public_answer_found", "positive_evidence_found", "weak_lead_only"}:
        errors.append(f"{path}.packet_result.status: unsupported value {status!r}")
    expect_string(result.get("summary"), f"{path}.packet_result.summary", errors)
    expect_string(boundary.get("allowed_conclusion"), f"{path}.overclaim_boundary.allowed_conclusion", errors)

    forbidden_codes = boundary.get("forbidden_conclusion_codes")
    if not isinstance(forbidden_codes, list):
        errors.append(f"{path}.overclaim_boundary.forbidden_conclusion_codes: must be an array")
    elif not all(isinstance(code, str) and code.strip() for code in forbidden_codes):
        errors.append(f"{path}.overclaim_boundary.forbidden_conclusion_codes: must contain non-empty strings")

    lane = packet.get("locked_earthquake_lane")
    strength = packet.get("evidence_strength")
    no_evidence_packet = strength == "not_found_after_reasonable_search" or status in NO_EVIDENCE_RESULT_STATUSES

    if no_evidence_packet:
        query_log = packet.get("query_log")
        if not isinstance(query_log, list) or not query_log:
            errors.append(f"{path}.query_log: no-evidence/no-public-answer packets require search entries")

        result_text = " ".join(
            str(value)
            for value in (
                result.get("summary"),
                result.get("answer_semantics"),
                boundary.get("allowed_conclusion"),
                boundary.get("missing_evidence_statement"),
            )
            if value is not None
        )
        for phrase in sorted(FORBIDDEN_MISSING_EVIDENCE_PHRASES):
            if contains_normalized_phrase(result_text, phrase):
                errors.append(f"{path}: missing evidence is converted into forbidden conclusion {phrase!r}")
        for status_word in sorted(FORBIDDEN_MISSING_EVIDENCE_STATUS_CONCLUSIONS):
            if contains_normalized_phrase(result_text, status_word):
                errors.append(
                    f"{path}: missing evidence is converted into final status conclusion {status_word!r}"
                )

        normalized_result_text = normalize_for_boundary_check(result_text)

        if lane in EVIDENCE_EXISTENCE_LANES:
            if status != "no_public_evidence_found":
                errors.append(f"{path}.packet_result.status: {lane} no-findings must be no_public_evidence_found")
            if "no public evidence found" not in normalized_result_text:
                errors.append(f"{path}: {lane} no-findings must say 'No public evidence found'")
            if "no public answer found" in normalized_result_text:
                errors.append(f"{path}: {lane} must not use no-public-answer semantics")
        elif lane in STATUS_ANSWER_LANES:
            if status != "no_public_answer_found":
                errors.append(f"{path}.packet_result.status: {lane} no-findings must be no_public_answer_found")
            if "no public answer found" not in normalized_result_text:
                errors.append(f"{path}: {lane} no-findings must say 'No public answer found'")
            if "no public evidence found" in normalized_result_text:
                errors.append(f"{path}: {lane} must not use no-public-evidence semantics")

    if status == "positive_evidence_found":
        evidence_items = []
        for key in ("document_inventory", "physical_condition_public_evidence"):
            value = packet.get(key)
            if isinstance(value, list):
                evidence_items.extend(item for item in value if isinstance(item, dict))
        if not any(is_eligible_positive_evidence_item(item) for item in evidence_items):
            errors.append(
                f"{path}: positive_evidence_found requires at least one positive evidence item "
                "with an http(s) source_url, exact_target_match, and non-context evidence strength/source class"
            )


def validate_packet(packet: object, path: str, errors: list[str]) -> None:
    obj = require_object(packet, path, errors)
    if obj is None:
        return

    missing = sorted(set(REQUIRED_FIELDS) - set(obj))
    if missing:
        errors.append(f"{path}: missing required fields {missing}")

    extra_lane = obj.get("locked_earthquake_lane")
    if extra_lane not in ALLOWED_LANES:
        errors.append(f"{path}.locked_earthquake_lane: must be one of {sorted(ALLOWED_LANES)!r}")
    if obj.get("evidence_strength") not in ALLOWED_EVIDENCE_STRENGTHS:
        errors.append(f"{path}.evidence_strength: unsupported value {obj.get('evidence_strength')!r}")
    if obj.get("source_curation_class") not in ALLOWED_SOURCE_CLASSES:
        errors.append(f"{path}.source_curation_class: unsupported value {obj.get('source_curation_class')!r}")

    validate_confirmed_building(obj.get("confirmed_building"), f"{path}.confirmed_building", errors)
    validate_evidence_array(obj.get("document_inventory"), f"{path}.document_inventory", errors)
    validate_evidence_array(
        obj.get("physical_condition_public_evidence"),
        f"{path}.physical_condition_public_evidence",
        errors,
    )
    validate_unresolved_exceptions(obj.get("unresolved_exceptions"), f"{path}.unresolved_exceptions", errors)
    validate_manual_targets(obj.get("manual_request_targets"), f"{path}.manual_request_targets", errors)
    validate_query_log(obj.get("query_log"), f"{path}.query_log", errors)
    validate_result_and_boundary(obj, path, errors)


def scan_file_for_forbidden_terms(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for term in sorted(FORBIDDEN_V1_TERMS):
        if term in text:
            errors.append(f"{path.relative_to(ROOT)}: contains forbidden broad V1 term {term!r}")


def validate_gate3_pointer(value: object, errors: list[str]) -> None:
    obj = require_object(value, "gate3_pointer", errors)
    if obj is None:
        return

    extra = sorted(set(obj) - POINTER_ALLOWED_KEYS)
    if extra:
        errors.append(f"gate3_pointer: unexpected keys {extra}")
    active_keys = sorted(POINTER_FORBIDDEN_ACTIVE_KEYS & set(obj))
    if active_keys:
        errors.append(f"gate3_pointer: must not contain active copied Gate 3 keys {active_keys}")
    if obj.get("workflow_gate") != "evidence_packet":
        errors.append("gate3_pointer.workflow_gate: must be 'evidence_packet'")
    if obj.get("status") != "redirected_to_v2_evidence_packet":
        errors.append("gate3_pointer.status: must be 'redirected_to_v2_evidence_packet'")
    if obj.get("canonical_file") != "evidence-packet-schema.json":
        errors.append("gate3_pointer.canonical_file: must point to evidence-packet-schema.json")
    if obj.get("active_scope_ids") != [
        "nscp_seismic_design_evidence",
        "obo_structural_permit_review_evidence",
        "post_earthquake_tag_status",
        "clearance_after_damage_or_tag",
    ]:
        errors.append("gate3_pointer.active_scope_ids: must equal the four V2 lanes")
    if obj.get("required_packet_fields") != REQUIRED_FIELDS:
        errors.append("gate3_pointer.required_packet_fields: must equal the V2 packet fields")


def main() -> int:
    errors: list[str] = []

    try:
        schema = read_json(SCHEMA_PATH)
        validate_schema(schema, errors)
        scan_file_for_forbidden_terms(SCHEMA_PATH, errors)
    except FileNotFoundError:
        errors.append(f"{SCHEMA_PATH.relative_to(ROOT)}: missing schema file")
    except json.JSONDecodeError as exc:
        errors.append(f"{SCHEMA_PATH.relative_to(ROOT)}: invalid JSON: {exc}")

    fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixture_paths:
        errors.append(f"{FIXTURE_DIR.relative_to(ROOT)}: must contain JSON fixtures")

    fixture_names = {path.name for path in fixture_paths}
    required_fixtures = {
        "no-public-evidence-nscp-seismic.json",
        "no-public-evidence-obo-structural-review.json",
        "no-public-answer-post-earthquake-tag.json",
        "no-public-answer-clearance.json",
        "red-yellow-tag-found.json",
        "corporate-operator-claim-only.json",
        "official-clearance-found.json",
    }
    missing_fixtures = sorted(required_fixtures - fixture_names)
    if missing_fixtures:
        errors.append(f"{FIXTURE_DIR.relative_to(ROOT)}: missing fixtures {missing_fixtures}")

    for fixture_path in fixture_paths:
        try:
            packet = read_json(fixture_path)
            scan_file_for_forbidden_terms(fixture_path, errors)
            validate_packet(packet, fixture_path.relative_to(ROOT).as_posix(), errors)
        except json.JSONDecodeError as exc:
            errors.append(f"{fixture_path.relative_to(ROOT)}: invalid JSON: {exc}")

    try:
        pointer = read_json(GATE3_POINTER_PATH)
        scan_file_for_forbidden_terms(GATE3_POINTER_PATH, errors)
        validate_gate3_pointer(pointer, errors)
    except FileNotFoundError:
        errors.append(f"{GATE3_POINTER_PATH.relative_to(ROOT)}: missing pointer file")
    except json.JSONDecodeError as exc:
        errors.append(f"{GATE3_POINTER_PATH.relative_to(ROOT)}: invalid JSON: {exc}")

    if errors:
        return fail("\n- " + "\n- ".join(errors))

    print(
        "validated V2 Gate 3 evidence packet: "
        f"{len(fixture_paths)} fixtures, {len(REQUIRED_FIELDS)} required fields"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
