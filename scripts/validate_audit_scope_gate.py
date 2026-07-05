#!/usr/bin/env python3
"""Validate Gate 2 earthquake audit-scope lock test cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_CASES_PATH = ROOT / "data/building-code-auditor/audit-scope-test-cases.json"

REQUIRED_CATEGORIES = {
    "menu_prompt",
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
    "all",
    "ambiguous_scope",
}

LANE_SCOPE_IDS = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
}

SCOPE_IDS = LANE_SCOPE_IDS | {"all"}

MENU_SCOPE_IDS = [
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
]

MENU_LABELS = {
    "nscp_seismic_design_evidence": "NSCP / seismic design evidence",
    "obo_structural_permit_review": "OBO structural permit or plan-review evidence",
    "latest_post_earthquake_status": "Latest post-earthquake official tag or inspection status",
    "latest_clearance_after_tag": "Latest clearance after damage, tag, closure, or restriction",
}

LANE_TYPES = {
    "nscp_seismic_design_evidence": "availability_only",
    "obo_structural_permit_review": "availability_only",
    "latest_post_earthquake_status": "availability_and_answer",
    "latest_clearance_after_tag": "availability_and_answer",
}

STATUSES = {
    "needs_user_scope_choice",
    "needs_scope_clarification",
    "scope_confirmed",
}

ANSWER_SOURCES = {
    "not_answered",
    "number",
    "label",
    "natural_language",
    "all",
}

BLOCKERS = {
    "waiting_for_scope_choice",
    "waiting_for_scope_confirmation",
    "ambiguous_scope",
}

FORBIDDEN_PRESEARCH_KEYS = {
    "evidence_results",
    "sources_checked",
    "claims",
    "citations",
    "search_results",
}

FORBIDDEN_SOURCE_REALITY_CLAIMS = {
    "is compliant",
    "is noncompliant",
    "is unsafe",
    "is fit for occupancy",
    "has no permit",
    "has no incident",
    "is unlicensed",
    "earthquake-proof",
    "earthquake proof",
}


def fail(message: str) -> int:
    print(f"audit scope gate validation failed: {message}", file=sys.stderr)
    return 1


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def require_object(value: object, path: str, errors: list[str]) -> dict | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: must be an object")
        return None
    return value


def require_keys(value: dict, path: str, required: set[str], errors: list[str]) -> None:
    missing = sorted(required - set(value))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")


def forbid_extra_keys(value: dict, path: str, allowed: set[str], errors: list[str]) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        errors.append(f"{path}: unexpected keys {extra}")


def expect_string(value: object, path: str, errors: list[str], allow_null: bool = False) -> None:
    if allow_null and value is None:
        return
    if not isinstance(value, str):
        errors.append(f"{path}: must be a string")


def expect_bool(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, bool):
        errors.append(f"{path}: must be a boolean")


def expect_enum(value: object, path: str, allowed: set[str], errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{path}: must be one of {sorted(allowed)!r}")


def expect_string_array(
    value: object,
    path: str,
    errors: list[str],
    allowed: set[str] | None = None,
    *,
    require_non_empty: bool = False,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    if require_non_empty and not value:
        errors.append(f"{path}: must not be empty")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{path}[{index}]: must be a string")
        elif allowed is not None and item not in allowed:
            errors.append(f"{path}[{index}]: must be one of {sorted(allowed)!r}")


def validate_confirmed_place(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"display_name", "candidate_id", "city", "country", "gate_1_status"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("display_name"), f"{path}.display_name", errors)
    expect_string(obj.get("candidate_id"), f"{path}.candidate_id", errors)
    expect_string(obj.get("city"), f"{path}.city", errors)
    if obj.get("country") != "Philippines":
        errors.append(f"{path}.country: must be 'Philippines'")
    if obj.get("gate_1_status") != "confirmed_by_user":
        errors.append(f"{path}.gate_1_status: must be 'confirmed_by_user'")


def validate_user_intake(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"raw_user_scope_request", "interpreted_scope", "answer_source"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("raw_user_scope_request"), f"{path}.raw_user_scope_request", errors, allow_null=True)
    interpreted = obj.get("interpreted_scope")
    if interpreted is not None:
        expect_enum(interpreted, f"{path}.interpreted_scope", SCOPE_IDS, errors)
    expect_enum(obj.get("answer_source"), f"{path}.answer_source", ANSWER_SOURCES, errors)


def validate_menu(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    if len(value) != 4:
        errors.append(f"{path}: must contain exactly four menu options")
        return

    numbers: list[int] = []
    scope_ids: list[str] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        obj = require_object(item, item_path, errors)
        if obj is None:
            continue
        allowed = {"number", "scope_id", "label", "lane_type"}
        require_keys(obj, item_path, allowed, errors)
        forbid_extra_keys(obj, item_path, allowed, errors)

        number = obj.get("number")
        if not isinstance(number, int):
            errors.append(f"{item_path}.number: must be an integer")
        else:
            numbers.append(number)

        scope_id = obj.get("scope_id")
        expect_enum(scope_id, f"{item_path}.scope_id", LANE_SCOPE_IDS, errors)
        if isinstance(scope_id, str):
            scope_ids.append(scope_id)
            if obj.get("label") != MENU_LABELS[scope_id]:
                errors.append(f"{item_path}.label: must be {MENU_LABELS[scope_id]!r}")
            if obj.get("lane_type") != LANE_TYPES[scope_id]:
                errors.append(f"{item_path}.lane_type: must be {LANE_TYPES[scope_id]!r}")

    if numbers != [1, 2, 3, 4]:
        errors.append(f"{path}: menu numbers must be [1, 2, 3, 4]")
    if scope_ids != MENU_SCOPE_IDS:
        errors.append(f"{path}: menu scope order must be {MENU_SCOPE_IDS!r}")


def validate_locked_scope(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"scope_ids", "selected_lanes", "requires_timeframe", "requires_target_subscope", "output_intent"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)

    scope_ids = obj.get("scope_ids")
    selected_lanes = obj.get("selected_lanes")
    expect_string_array(scope_ids, f"{path}.scope_ids", errors, LANE_SCOPE_IDS, require_non_empty=True)
    expect_string_array(selected_lanes, f"{path}.selected_lanes", errors, LANE_SCOPE_IDS, require_non_empty=True)
    if isinstance(scope_ids, list) and isinstance(selected_lanes, list) and scope_ids != selected_lanes:
        errors.append(f"{path}: scope_ids and selected_lanes must match")
    if isinstance(scope_ids, list) and len(scope_ids) == 4 and scope_ids != MENU_SCOPE_IDS:
        errors.append(f"{path}.scope_ids: all-scope order must be {MENU_SCOPE_IDS!r}")
    expect_bool(obj.get("requires_timeframe"), f"{path}.requires_timeframe", errors)
    expect_bool(obj.get("requires_target_subscope"), f"{path}.requires_target_subscope", errors)
    expect_string(obj.get("output_intent"), f"{path}.output_intent", errors)


def validate_confirmation(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {
        "status",
        "locked_scope",
        "user_facing_prompt",
        "clarifying_questions",
        "can_proceed_to_evidence_search",
        "blockers",
    }
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_enum(obj.get("status"), f"{path}.status", STATUSES, errors)
    if obj.get("locked_scope") is not None:
        validate_locked_scope(obj.get("locked_scope"), f"{path}.locked_scope", errors)
    expect_string(obj.get("user_facing_prompt"), f"{path}.user_facing_prompt", errors)
    expect_string_array(obj.get("clarifying_questions"), f"{path}.clarifying_questions", errors)
    expect_bool(obj.get("can_proceed_to_evidence_search"), f"{path}.can_proceed_to_evidence_search", errors)
    expect_string_array(obj.get("blockers"), f"{path}.blockers", errors, BLOCKERS)

    prompt = obj.get("user_facing_prompt")
    questions = obj.get("clarifying_questions")
    text_parts = [prompt] if isinstance(prompt, str) else []
    if isinstance(questions, list):
        text_parts.extend(item for item in questions if isinstance(item, str))
    combined_text = " ".join(text_parts).lower()
    for forbidden in FORBIDDEN_SOURCE_REALITY_CLAIMS:
        if forbidden in combined_text:
            errors.append(f"{path}: source-reality wording must not claim {forbidden!r}")

    if obj.get("status") == "scope_confirmed":
        if obj.get("locked_scope") is None:
            errors.append(f"{path}.locked_scope: must be present when scope is confirmed")
        if obj.get("can_proceed_to_evidence_search") is not True:
            errors.append(f"{path}.can_proceed_to_evidence_search: must be true when scope is confirmed")
        if obj.get("blockers") != []:
            errors.append(f"{path}.blockers: must be empty when scope is confirmed")
    else:
        if obj.get("locked_scope") is not None:
            errors.append(f"{path}.locked_scope: must be null until scope is confirmed")
        if obj.get("can_proceed_to_evidence_search") is not False:
            errors.append(f"{path}.can_proceed_to_evidence_search: must be false until scope is confirmed")


def validate_safety(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"evidence_search_started", "blocked_work"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    if obj.get("evidence_search_started") is not False:
        errors.append(f"{path}.evidence_search_started: must be false in Gate 2 fixtures")
    expect_string_array(obj.get("blocked_work"), f"{path}.blocked_work", errors)


def validate_packet_shape(packet: object) -> list[str]:
    errors: list[str] = []
    obj = require_object(packet, "<root>", errors)
    if obj is None:
        return errors
    allowed = {
        "schema_version",
        "workflow_step",
        "confirmed_place",
        "user_intake",
        "scope_menu",
        "scope_confirmation",
        "safety",
    }
    require_keys(obj, "<root>", allowed, errors)
    forbid_extra_keys(obj, "<root>", allowed, errors)
    forbidden_present = sorted(FORBIDDEN_PRESEARCH_KEYS & set(obj))
    if forbidden_present:
        errors.append(f"<root>: pre-search Gate 2 packet must not include {forbidden_present}")
    if obj.get("schema_version") != "1.0.0":
        errors.append("schema_version: must be '1.0.0'")
    if obj.get("workflow_step") != "audit_scope_lock":
        errors.append("workflow_step: must be 'audit_scope_lock'")
    validate_confirmed_place(obj.get("confirmed_place"), "confirmed_place", errors)
    validate_user_intake(obj.get("user_intake"), "user_intake", errors)
    validate_menu(obj.get("scope_menu"), "scope_menu", errors)
    validate_confirmation(obj.get("scope_confirmation"), "scope_confirmation", errors)
    validate_safety(obj.get("safety"), "safety", errors)
    return errors


def validate_case(case: dict) -> list[str]:
    errors: list[str] = []
    case_id = case.get("case_id", "<missing case_id>")
    packet = case.get("sample_packet")
    shape_errors = validate_packet_shape(packet)
    errors.extend(f"{case_id}: packet shape: {message}" for message in shape_errors)
    if shape_errors or not isinstance(packet, dict):
        return errors

    confirmation = packet.get("scope_confirmation", {})
    if not isinstance(confirmation, dict):
        return errors

    expected_status = case.get("expected_status")
    actual_status = confirmation.get("status")
    if actual_status != expected_status:
        errors.append(f"{case_id}: expected status {expected_status!r}, got {actual_status!r}")

    expected_can_proceed = case.get("expected_can_proceed_to_evidence_search")
    actual_can_proceed = confirmation.get("can_proceed_to_evidence_search")
    if actual_can_proceed is not expected_can_proceed:
        errors.append(
            f"{case_id}: expected can_proceed_to_evidence_search "
            f"{expected_can_proceed!r}, got {actual_can_proceed!r}"
        )

    expected_blockers = case.get("expected_blockers")
    actual_blockers = confirmation.get("blockers")
    if actual_blockers != expected_blockers:
        errors.append(f"{case_id}: expected blockers {expected_blockers!r}, got {actual_blockers!r}")

    expected_scope_ids = case.get("expected_locked_scope_ids")
    locked_scope = confirmation.get("locked_scope")
    if expected_scope_ids is not None:
        if not isinstance(locked_scope, dict):
            errors.append(f"{case_id}: expected locked scope, got null")
        elif locked_scope.get("scope_ids") != expected_scope_ids:
            errors.append(
                f"{case_id}: expected locked scope ids {expected_scope_ids!r}, "
                f"got {locked_scope.get('scope_ids')!r}"
            )

    if confirmation.get("status") == "scope_confirmed":
        locked = confirmation.get("locked_scope")
        if isinstance(locked, dict):
            scope_ids = locked.get("scope_ids", [])
            if any(scope_id in {"latest_post_earthquake_status", "latest_clearance_after_tag"} for scope_id in scope_ids):
                if locked.get("requires_timeframe") is not True:
                    errors.append(f"{case_id}: lanes 3-4 must require timeframe")

    return errors


def validate_root(document: object) -> list[str]:
    errors: list[str] = []
    root = require_object(document, "<root>", errors)
    if root is None:
        return errors
    if root.get("schema_version") != "1.0.0":
        errors.append("<root>.schema_version: must be '1.0.0'")
    if root.get("workflow_gate") != "audit_scope_lock":
        errors.append("<root>.workflow_gate: must be 'audit_scope_lock'")
    required_categories = root.get("required_case_categories")
    if required_categories != sorted(REQUIRED_CATEGORIES):
        if set(required_categories or []) != REQUIRED_CATEGORIES:
            errors.append("<root>.required_case_categories: must list all required Gate 2 categories")
    cases = root.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("<root>.cases: must be a non-empty array")
        return errors
    seen_categories: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"<root>.cases[{index}]: must be an object")
            continue
        category = case.get("category")
        if category in REQUIRED_CATEGORIES:
            seen_categories.add(category)
        else:
            errors.append(f"<root>.cases[{index}].category: unexpected {category!r}")
        errors.extend(validate_case(case))
    missing = sorted(REQUIRED_CATEGORIES - seen_categories)
    if missing:
        errors.append(f"<root>.cases: missing required categories {missing}")
    return errors


def main() -> int:
    try:
        document = read_json(TEST_CASES_PATH)
    except FileNotFoundError:
        return fail(f"missing {TEST_CASES_PATH.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    errors = validate_root(document)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return fail(f"{len(errors)} error(s)")

    cases = document["cases"] if isinstance(document, dict) else []
    print(f"validated {len(cases)} Gate 2 earthquake audit-scope cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
