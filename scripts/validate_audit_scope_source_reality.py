#!/usr/bin/env python3
"""Validate Gate 2 earthquake source-reality matrix."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REALITY_PATH = ROOT / "data/building-code-auditor/audit-scope-source-reality.json"

SCOPE_IDS = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
}

LANE_TYPES = {"availability_only", "availability_and_answer"}

STATUS_VALUES = {
    "public_target_document_possible",
    "public_process_only",
    "manual_request_likely",
    "not_assessable_from_public_web",
}

REQUIRED_SCOPE_KEYS = {
    "scope_id",
    "question",
    "lane_type",
    "applicable_in_philippines",
    "primary_source_types",
    "example_sources",
    "automation_status",
    "required_user_inputs",
    "expected_public_result_shape",
    "not_enough_if_only_found",
    "limitations",
    "forbidden_claims",
    "manual_follow_up_triggers",
}

REQUIRED_SOURCE_KEYS = {
    "name",
    "url",
    "source_type",
    "automation_status",
    "access_notes",
}

FORBIDDEN_EVIDENCE_KEYS = {
    "evidence_results",
    "building_specific_findings",
    "searched_place",
    "claims",
    "compliance_result",
    "safety_result",
}

OVERCLAIM_TERMS = {
    "compliant",
    "compliance",
    "safe",
    "unsafe",
    "fit for occupancy",
    "no permit",
    "unpermitted",
    "earthquake-proof",
}


def fail(message: str) -> int:
    print(f"audit scope source-reality validation failed: {message}", file=sys.stderr)
    return 1


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def expect_string_array(
    value: object,
    path: str,
    errors: list[str],
    *,
    allowed: set[str] | None = None,
    require_non_empty: bool = True,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    if require_non_empty and not value:
        errors.append(f"{path}: must not be empty")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{item_path}: must be a non-empty string")
            continue
        if allowed is not None and item not in allowed:
            errors.append(f"{item_path}: must be one of {sorted(allowed)!r}")


def validate_source(source: object, path: str, errors: list[str]) -> None:
    if not isinstance(source, dict):
        errors.append(f"{path}: must be an object")
        return
    missing = sorted(REQUIRED_SOURCE_KEYS - set(source))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    extra_evidence_keys = sorted(FORBIDDEN_EVIDENCE_KEYS & set(source))
    if extra_evidence_keys:
        errors.append(f"{path}: must not include Gate 3 evidence keys {extra_evidence_keys}")

    for key in ("name", "source_type", "access_notes"):
        value = source.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}.{key}: must be a non-empty string")

    url = source.get("url")
    if not isinstance(url, str) or not is_http_url(url):
        errors.append(f"{path}.url: must be an HTTP/HTTPS URL")

    status = source.get("automation_status")
    if status not in STATUS_VALUES:
        errors.append(f"{path}.automation_status: must be one of {sorted(STATUS_VALUES)!r}")


def validate_scope(scope: object, path: str, errors: list[str]) -> str | None:
    if not isinstance(scope, dict):
        errors.append(f"{path}: must be an object")
        return None

    missing = sorted(REQUIRED_SCOPE_KEYS - set(scope))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    extra_evidence_keys = sorted(FORBIDDEN_EVIDENCE_KEYS & set(scope))
    if extra_evidence_keys:
        errors.append(f"{path}: must not include Gate 3 evidence keys {extra_evidence_keys}")

    scope_id = scope.get("scope_id")
    if scope_id not in SCOPE_IDS:
        errors.append(f"{path}.scope_id: must be one of {sorted(SCOPE_IDS)!r}")
    lane_type = scope.get("lane_type")
    if lane_type not in LANE_TYPES:
        errors.append(f"{path}.lane_type: must be one of {sorted(LANE_TYPES)!r}")
    if not isinstance(scope.get("applicable_in_philippines"), bool):
        errors.append(f"{path}.applicable_in_philippines: must be a boolean")
    if not isinstance(scope.get("question"), str) or not scope.get("question", "").strip():
        errors.append(f"{path}.question: must be a non-empty string")

    expect_string_array(scope.get("primary_source_types"), f"{path}.primary_source_types", errors)
    expect_string_array(
        scope.get("automation_status"),
        f"{path}.automation_status",
        errors,
        allowed=STATUS_VALUES,
    )
    expect_string_array(scope.get("required_user_inputs"), f"{path}.required_user_inputs", errors)
    expect_string_array(scope.get("expected_public_result_shape"), f"{path}.expected_public_result_shape", errors)
    expect_string_array(scope.get("not_enough_if_only_found"), f"{path}.not_enough_if_only_found", errors)
    expect_string_array(scope.get("limitations"), f"{path}.limitations", errors)
    expect_string_array(scope.get("forbidden_claims"), f"{path}.forbidden_claims", errors)
    expect_string_array(scope.get("manual_follow_up_triggers"), f"{path}.manual_follow_up_triggers", errors)

    claims = scope.get("forbidden_claims")
    if isinstance(claims, list):
        joined = " ".join(item.lower() for item in claims if isinstance(item, str))
        if not any(term in joined for term in OVERCLAIM_TERMS):
            errors.append(f"{path}.forbidden_claims: must block safety/compliance/permit overclaims")

    if lane_type == "availability_and_answer":
        required_text = "no public official"
        joined_shape = " ".join(scope.get("expected_public_result_shape", [])).lower()
        if required_text not in joined_shape:
            errors.append(f"{path}.expected_public_result_shape: lanes 3-4 must include no-public-answer shape")

    sources = scope.get("example_sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{path}.example_sources: must be a non-empty array")
    else:
        for index, source in enumerate(sources):
            validate_source(source, f"{path}.example_sources[{index}]", errors)

    return scope_id if isinstance(scope_id, str) else None


def validate_root(document: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["<root>: must be a JSON object"]

    if document.get("schema_version") != "1.0.0":
        errors.append("<root>.schema_version: must be '1.0.0'")
    if document.get("workflow_gate") != "audit_scope_lock":
        errors.append("<root>.workflow_gate: must be 'audit_scope_lock'")
    expect_string_array(
        document.get("source_status_values"),
        "<root>.source_status_values",
        errors,
        allowed=STATUS_VALUES,
    )

    extra_evidence_keys = sorted(FORBIDDEN_EVIDENCE_KEYS & set(document))
    if extra_evidence_keys:
        errors.append(f"<root>: must not include Gate 3 evidence keys {extra_evidence_keys}")

    scopes = document.get("scope_reality")
    if not isinstance(scopes, list):
        errors.append("<root>.scope_reality: must be an array")
        return errors

    seen_scope_ids: list[str] = []
    for index, scope in enumerate(scopes):
        scope_id = validate_scope(scope, f"<root>.scope_reality[{index}]", errors)
        if scope_id is not None:
            seen_scope_ids.append(scope_id)

    seen_set = set(seen_scope_ids)
    missing = sorted(SCOPE_IDS - seen_set)
    extra = sorted(seen_set - SCOPE_IDS)
    duplicates = sorted(scope_id for scope_id in seen_set if seen_scope_ids.count(scope_id) > 1)
    if missing:
        errors.append(f"<root>.scope_reality: missing required scopes {missing}")
    if extra:
        errors.append(f"<root>.scope_reality: unexpected scopes {extra}")
    if duplicates:
        errors.append(f"<root>.scope_reality: duplicate scopes {duplicates}")
    if len(scopes) != len(SCOPE_IDS):
        errors.append(f"<root>.scope_reality: must contain exactly {len(SCOPE_IDS)} scopes")

    ecc_review = document.get("ecc_review")
    if not isinstance(ecc_review, dict):
        errors.append("<root>.ecc_review: must be an object")
    else:
        for key in ("objective", "handoff", "overclaim_boundary"):
            value = ecc_review.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"<root>.ecc_review.{key}: must be a non-empty string")
        for key in ("inputs", "outputs", "eval", "human_boundary", "safety_risks"):
            expect_string_array(ecc_review.get(key), f"<root>.ecc_review.{key}", errors)

    return errors


def main() -> int:
    try:
        document = read_json(SOURCE_REALITY_PATH)
    except FileNotFoundError:
        return fail(f"missing {SOURCE_REALITY_PATH.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    errors = validate_root(document)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return fail(f"{len(errors)} error(s)")

    print("validated Gate 2 earthquake source-reality matrix")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
