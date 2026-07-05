#!/usr/bin/env python3
"""Validate V2 Gate 2 earthquake scope fixtures.

Gate 2 defaults to all four earthquake lanes after identity confirmation. The
user may narrow to one or more lanes, but the workflow must never add a fifth
lane or start evidence search during Gate 2.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V2_DATA_DIR = ROOT / "data/philippines-building-code-evidence-auditor-v2"
SCOPE_CASES_PATH = V2_DATA_DIR / "earthquake-scope-test-cases.json"
COMPATIBILITY_PATHS = [
    V2_DATA_DIR / "audit-scope-test-cases.json",
    V2_DATA_DIR / "audit-scope-source-reality.json",
    V2_DATA_DIR / "gate-2-six-establishment-menu-matrix.json",
    V2_DATA_DIR / "source-landscape.json",
]

ALLOWED_SCOPE_IDS = [
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review_evidence",
    "post_earthquake_tag_status",
    "clearance_after_damage_or_tag",
]

REQUIRED_MENU_LABELS = [
    "NSCP / seismic design evidence",
    "OBO structural permit or review evidence",
    "Latest post-earthquake tag / status",
    "Latest clearance after damage or tag",
]

REQUIRED_CATEGORIES = {
    "default_all_lanes",
    "narrowed_single_lane",
    "narrowed_multiple_lanes",
    "ambiguous_scope",
    "unsupported_broad_scope",
}

STATUS_VALUES = {
    "all_lanes_defaulted",
    "selected_scopes_confirmed",
    "needs_scope_clarification",
    "unsupported_scope",
}

ANSWER_SOURCES = {
    "not_answered_default_all",
    "number",
    "label",
    "natural_language",
}

BLOCKERS = {
    "ambiguous_earthquake_scope",
    "unsupported_non_earthquake_scope",
}

FORBIDDEN_V1_SCOPE_IDS = {
    "permit_occupancy_records",
    "incident_damage_history",
    "contractor_professional_developer",
    "standards_context_only",
    "broad_public_evidence_packet",
}

FORBIDDEN_PRESEARCH_KEYS = {
    "evidence_results",
    "sources_checked",
    "claims",
    "citations",
    "search_results",
    "document_inventory",
    "query_log",
    "packet_result",
    "evidence_strength",
}


def fail(message: str) -> int:
    print(f"building-code v2 earthquake scope validation failed: {message}", file=sys.stderr)
    return 1


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def require_object(value: object, path: str, errors: list[str]) -> dict | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: must be an object")
        return None
    return value


def expect_string(value: object, path: str, errors: list[str], *, allow_null: bool = False) -> None:
    if value is None and allow_null:
        return
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")


def expect_string_array(
    value: object,
    path: str,
    errors: list[str],
    *,
    expected: list[str] | None = None,
    allowed: set[str] | None = None,
    allow_empty: bool = True,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    if not allow_empty and not value:
        errors.append(f"{path}: must not be empty")
    if expected is not None and value != expected:
        errors.append(f"{path}: must equal {expected!r}")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}[{index}]: must be a non-empty string")
        elif allowed is not None and item not in allowed:
            errors.append(f"{path}[{index}]: must be one of {sorted(allowed)!r}")


def scan_for_forbidden_strings(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for forbidden in sorted(FORBIDDEN_V1_SCOPE_IDS):
        if forbidden in text:
            errors.append(f"{path.relative_to(ROOT)}: contains forbidden V1 scope ID {forbidden!r}")


def scan_for_forbidden_presearch_keys(value: object, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        forbidden = sorted(FORBIDDEN_PRESEARCH_KEYS & set(value))
        if forbidden:
            errors.append(f"{path}: Gate 2 must not include pre-search keys {forbidden}")
        for key, child in value.items():
            scan_for_forbidden_presearch_keys(child, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_for_forbidden_presearch_keys(child, f"{path}[{index}]", errors)


def validate_confirmed_place(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    for key in ("display_name", "candidate_id", "city"):
        expect_string(obj.get(key), f"{path}.{key}", errors)
    if obj.get("country") != "Philippines":
        errors.append(f"{path}.country: must be 'Philippines'")
    if obj.get("gate_1_status") != "confirmed_by_user":
        errors.append(f"{path}.gate_1_status: must be 'confirmed_by_user'")


def validate_menu(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    if len(value) != 4:
        errors.append(f"{path}: must contain exactly four menu options")
        return

    numbers: list[int] = []
    scope_ids: list[str] = []
    labels: list[str] = []
    for index, item in enumerate(value):
        obj = require_object(item, f"{path}[{index}]", errors)
        if obj is None:
            continue
        numbers.append(obj.get("number") if isinstance(obj.get("number"), int) else -1)
        scope_id = obj.get("scope_id")
        if isinstance(scope_id, str):
            scope_ids.append(scope_id)
        label = obj.get("label")
        if isinstance(label, str):
            labels.append(label)

    if numbers != [1, 2, 3, 4]:
        errors.append(f"{path}: menu numbers must be [1, 2, 3, 4]")
    if scope_ids != ALLOWED_SCOPE_IDS:
        errors.append(f"{path}: menu scope order must be {ALLOWED_SCOPE_IDS!r}")
    if labels != REQUIRED_MENU_LABELS:
        errors.append(f"{path}: menu labels must be {REQUIRED_MENU_LABELS!r}")


def validate_user_intake(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    expect_string(obj.get("raw_user_scope_request"), f"{path}.raw_user_scope_request", errors, allow_null=True)
    expect_string_array(
        obj.get("interpreted_scopes"),
        f"{path}.interpreted_scopes",
        errors,
        allowed=set(ALLOWED_SCOPE_IDS),
    )
    if obj.get("answer_source") not in ANSWER_SOURCES:
        errors.append(f"{path}.answer_source: must be one of {sorted(ANSWER_SOURCES)!r}")


def validate_selected_scope(scope: object, path: str, errors: list[str]) -> str | None:
    obj = require_object(scope, path, errors)
    if obj is None:
        return None
    scope_id = obj.get("scope_id")
    if scope_id not in ALLOWED_SCOPE_IDS:
        errors.append(f"{path}.scope_id: must be one of {ALLOWED_SCOPE_IDS!r}")
        return None
    expected_label = REQUIRED_MENU_LABELS[ALLOWED_SCOPE_IDS.index(scope_id)]
    if obj.get("label") != expected_label:
        errors.append(f"{path}.label: must be {expected_label!r}")
    expect_string(obj.get("output_intent"), f"{path}.output_intent", errors)
    return scope_id


def validate_confirmation(value: object, path: str, errors: list[str]) -> list[str]:
    obj = require_object(value, path, errors)
    if obj is None:
        return []

    status = obj.get("status")
    if status not in STATUS_VALUES:
        errors.append(f"{path}.status: must be one of {sorted(STATUS_VALUES)!r}")
    expect_string(obj.get("user_facing_prompt"), f"{path}.user_facing_prompt", errors)
    expect_string_array(obj.get("clarifying_questions"), f"{path}.clarifying_questions", errors)
    expect_string_array(obj.get("blockers"), f"{path}.blockers", errors, allowed=BLOCKERS)
    if not isinstance(obj.get("can_proceed_to_evidence_search"), bool):
        errors.append(f"{path}.can_proceed_to_evidence_search: must be a boolean")

    selected_scopes = obj.get("selected_scopes")
    if not isinstance(selected_scopes, list):
        errors.append(f"{path}.selected_scopes: must be an array")
        return []

    selected_ids: list[str] = []
    for index, scope in enumerate(selected_scopes):
        scope_id = validate_selected_scope(scope, f"{path}.selected_scopes[{index}]", errors)
        if scope_id is not None:
            selected_ids.append(scope_id)

    if len(selected_ids) != len(set(selected_ids)):
        errors.append(f"{path}.selected_scopes: duplicate lanes are not allowed")

    if obj.get("can_proceed_to_evidence_search") is True:
        if status not in {"all_lanes_defaulted", "selected_scopes_confirmed"}:
            errors.append(f"{path}: proceed=true requires defaulted or selected confirmed status")
        if not selected_ids:
            errors.append(f"{path}.selected_scopes: proceed=true requires at least one selected lane")
    elif selected_ids:
        errors.append(f"{path}.selected_scopes: must be empty when evidence search cannot proceed")

    if status == "all_lanes_defaulted" and selected_ids != ALLOWED_SCOPE_IDS:
        errors.append(f"{path}.selected_scopes: all_lanes_defaulted must select all four lanes")

    return selected_ids


def validate_safety(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    if obj.get("evidence_search_started") is not False:
        errors.append(f"{path}.evidence_search_started: Gate 2 must not start evidence search")
    expect_string_array(obj.get("blocked_work"), f"{path}.blocked_work", errors)


def validate_packet(packet: object, path: str, errors: list[str]) -> list[str]:
    obj = require_object(packet, path, errors)
    if obj is None:
        return []
    scan_for_forbidden_presearch_keys(obj, path, errors)
    required = {
        "schema_version",
        "workflow_step",
        "confirmed_place",
        "user_intake",
        "scope_menu",
        "scope_confirmation",
        "safety",
    }
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    if obj.get("schema_version") != "2.1.0":
        errors.append(f"{path}.schema_version: must be '2.1.0'")
    if obj.get("workflow_step") != "earthquake_scope_lock":
        errors.append(f"{path}.workflow_step: must be 'earthquake_scope_lock'")

    validate_confirmed_place(obj.get("confirmed_place"), f"{path}.confirmed_place", errors)
    validate_user_intake(obj.get("user_intake"), f"{path}.user_intake", errors)
    validate_menu(obj.get("scope_menu"), f"{path}.scope_menu", errors)
    selected_ids = validate_confirmation(obj.get("scope_confirmation"), f"{path}.scope_confirmation", errors)
    validate_safety(obj.get("safety"), f"{path}.safety", errors)
    return selected_ids


def validate_scope_case(case: object, path: str, errors: list[str]) -> None:
    obj = require_object(case, path, errors)
    if obj is None:
        return

    category = obj.get("category")
    if category not in REQUIRED_CATEGORIES:
        errors.append(f"{path}.category: must be one of {sorted(REQUIRED_CATEGORIES)!r}")

    selected_ids = validate_packet(obj.get("sample_packet"), f"{path}.sample_packet", errors)
    expected_selected = obj.get("expected_selected_scope_ids")
    if not isinstance(expected_selected, list):
        errors.append(f"{path}.expected_selected_scope_ids: must be an array")
    elif selected_ids != expected_selected:
        errors.append(f"{path}: selected scopes do not match expected_selected_scope_ids")

    packet = obj.get("sample_packet")
    confirmation = packet.get("scope_confirmation") if isinstance(packet, dict) else None
    if not isinstance(confirmation, dict):
        return
    if confirmation.get("status") != obj.get("expected_status"):
        errors.append(f"{path}: status does not match expected_status")
    if confirmation.get("can_proceed_to_evidence_search") is not obj.get(
        "expected_can_proceed_to_evidence_search"
    ):
        errors.append(f"{path}: can_proceed_to_evidence_search does not match expected value")
    if set(confirmation.get("blockers", [])) != set(obj.get("expected_blockers", [])):
        errors.append(f"{path}: blockers do not match expected_blockers")

    if category == "default_all_lanes" and selected_ids != ALLOWED_SCOPE_IDS:
        errors.append(f"{path}: default_all_lanes must select all four lanes")
    if category == "narrowed_single_lane" and len(selected_ids) != 1:
        errors.append(f"{path}: narrowed_single_lane must select exactly one lane")
    if category == "narrowed_multiple_lanes" and len(selected_ids) <= 1:
        errors.append(f"{path}: narrowed_multiple_lanes must select at least two lanes")
    if category in {"ambiguous_scope", "unsupported_broad_scope"} and selected_ids:
        errors.append(f"{path}: blocked cases must not select lanes")


def validate_scope_cases(document: object) -> list[str]:
    errors: list[str] = []
    root = require_object(document, "<scope_cases>", errors)
    if root is None:
        return errors
    if root.get("schema_version") != "2.1.0":
        errors.append("<scope_cases>.schema_version: must be '2.1.0'")
    if root.get("workflow_gate") != "earthquake_scope_lock":
        errors.append("<scope_cases>.workflow_gate: must be 'earthquake_scope_lock'")
    expect_string_array(root.get("allowed_scope_ids"), "<scope_cases>.allowed_scope_ids", errors, expected=ALLOWED_SCOPE_IDS)
    expect_string_array(
        root.get("required_menu_labels"),
        "<scope_cases>.required_menu_labels",
        errors,
        expected=REQUIRED_MENU_LABELS,
    )
    declared_categories = root.get("required_case_categories")
    if set(declared_categories if isinstance(declared_categories, list) else []) != REQUIRED_CATEGORIES:
        errors.append("<scope_cases>.required_case_categories: must declare exactly the required categories")

    cases = root.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("<scope_cases>.cases: must be a non-empty array")
        return errors
    categories = {case.get("category") for case in cases if isinstance(case, dict)}
    missing = sorted(REQUIRED_CATEGORIES - categories)
    if missing:
        errors.append(f"<scope_cases>.cases: missing categories {missing}")
    for index, case in enumerate(cases):
        validate_scope_case(case, f"<scope_cases>.cases[{index}]", errors)
    return errors


def validate_compatibility_pointer(path: Path, errors: list[str]) -> None:
    try:
        data = read_json(path)
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: missing compatibility pointer")
        return
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return

    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)}: compatibility pointer must be an object")
        return
    if data.get("active_scope_ids") != ALLOWED_SCOPE_IDS:
        errors.append(f"{path.relative_to(ROOT)}.active_scope_ids: must equal the four permanent lanes")


def main() -> int:
    errors: list[str] = []
    try:
        document = read_json(SCOPE_CASES_PATH)
        scan_for_forbidden_strings(SCOPE_CASES_PATH, errors)
        errors.extend(validate_scope_cases(document))
    except FileNotFoundError:
        errors.append(f"{SCOPE_CASES_PATH.relative_to(ROOT)}: missing test cases")
    except json.JSONDecodeError as exc:
        errors.append(f"{SCOPE_CASES_PATH.relative_to(ROOT)}: invalid JSON: {exc}")

    for path in COMPATIBILITY_PATHS:
        scan_for_forbidden_strings(path, errors)
        validate_compatibility_pointer(path, errors)

    if errors:
        return fail("\n- " + "\n- ".join(errors))

    print("validated V2 Gate 2 earthquake scope: default-all plus narrowed multi-select fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
