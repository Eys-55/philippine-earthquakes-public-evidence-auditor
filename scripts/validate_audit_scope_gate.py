#!/usr/bin/env python3
"""Validate Gate 2 audit-scope lock test cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_CASES_PATH = ROOT / "data/building-code-auditor/audit-scope-test-cases.json"

REQUIRED_CATEGORIES = {
    "menu_prompt",
    "permit_occupancy_records",
    "incident_damage_history",
    "contractor_professional_developer",
    "standards_context_only",
    "broad_public_evidence_packet",
    "ambiguous_scope",
}

SCOPE_IDS = {
    "permit_occupancy_records",
    "incident_damage_history",
    "contractor_professional_developer",
    "standards_context_only",
    "broad_public_evidence_packet",
}

MENU_SCOPE_IDS = [
    "permit_occupancy_records",
    "incident_damage_history",
    "contractor_professional_developer",
    "standards_context_only",
    "broad_public_evidence_packet",
]

ANNOTATED_MENU_LABELS = {
    "permit_occupancy_records": (
        "Permit or occupancy records - usually LGU/OBO process pages or manual "
        "record request; not a national public registry"
    ),
    "incident_damage_history": (
        "Incident, damage, closure, repair, or retrofit history - often publicly "
        "searchable through LGU/government/news sources, but not proof of current safety"
    ),
    "contractor_professional_developer": (
        "Contractor, professional, developer, or operator evidence - usually "
        "requires a known name, license number, project name, or source lead"
    ),
    "standards_context_only": (
        "Standards or process context only - public standards context; not "
        "building-specific compliance proof"
    ),
    "broad_public_evidence_packet": (
        "Broad public-evidence packet - combines lanes and separates public "
        "findings from manual follow-ups"
    ),
}

SOURCE_REALITY_CONFIRMATION_PHRASES = {
    "permit_occupancy_records": "not a national public registry",
    "incident_damage_history": "not proof of current safety",
    "contractor_professional_developer": "needs a known name, license number, project name, or source lead",
    "standards_context_only": "cannot prove building-specific compliance",
    "broad_public_evidence_packet": "separate public findings from manual follow-ups",
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
}

EVIDENCE_LANES = {
    "standards",
    "lgu_obo",
    "contractor_professional",
    "incident_safety_history",
    "foi_manual_requests",
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
    "is safe",
    "is unsafe",
    "is fit for occupancy",
    "has no permit",
    "has no incident",
    "is unlicensed",
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


def expect_string_array(value: object, path: str, errors: list[str], allowed: set[str] | None = None) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
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
    if len(value) != 5:
        errors.append(f"{path}: must contain exactly five menu options")
        return

    numbers: list[int] = []
    scope_ids: list[str] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        obj = require_object(item, item_path, errors)
        if obj is None:
            continue
        allowed = {"number", "scope_id", "label", "evidence_lanes"}
        require_keys(obj, item_path, allowed, errors)
        forbid_extra_keys(obj, item_path, allowed, errors)
        number = obj.get("number")
        if not isinstance(number, int):
            errors.append(f"{item_path}.number: must be an integer")
        else:
            numbers.append(number)
        scope_id = obj.get("scope_id")
        expect_enum(scope_id, f"{item_path}.scope_id", SCOPE_IDS, errors)
        if isinstance(scope_id, str):
            scope_ids.append(scope_id)
        expect_string(obj.get("label"), f"{item_path}.label", errors)
        if scope_id in ANNOTATED_MENU_LABELS and obj.get("label") != ANNOTATED_MENU_LABELS[scope_id]:
            errors.append(
                f"{item_path}.label: must preserve annotated source-reality label "
                f"{ANNOTATED_MENU_LABELS[scope_id]!r}"
            )
        expect_string_array(obj.get("evidence_lanes"), f"{item_path}.evidence_lanes", EVIDENCE_LANES)

    if numbers != [1, 2, 3, 4, 5]:
        errors.append(f"{path}: menu numbers must be [1, 2, 3, 4, 5]")
    if scope_ids != MENU_SCOPE_IDS:
        errors.append(f"{path}: menu scope order must be {MENU_SCOPE_IDS!r}")


def validate_locked_scope(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"scope_id", "label", "evidence_lanes", "blocked_lanes", "output_intent"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_enum(obj.get("scope_id"), f"{path}.scope_id", SCOPE_IDS, errors)
    expect_string(obj.get("label"), f"{path}.label", errors)
    expect_string_array(obj.get("evidence_lanes"), f"{path}.evidence_lanes", EVIDENCE_LANES)
    expect_string_array(obj.get("blocked_lanes"), f"{path}.blocked_lanes", EVIDENCE_LANES)
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

    expected_blockers = set(case.get("expected_blockers", []))
    actual_blockers = set(confirmation.get("blockers", []))
    if actual_blockers != expected_blockers:
        errors.append(
            f"{case_id}: expected blockers {sorted(expected_blockers)!r}, "
            f"got {sorted(actual_blockers)!r}"
        )

    locked_scope = confirmation.get("locked_scope")
    questions = confirmation.get("clarifying_questions", [])
    category = case.get("category")

    if actual_status == "scope_confirmed":
        if not isinstance(locked_scope, dict):
            errors.append(f"{case_id}: confirmed scope must include locked_scope")
        else:
            locked_scope_id = locked_scope.get("scope_id")
            if locked_scope_id != case.get("expected_locked_scope_id"):
                errors.append(
                    f"{case_id}: expected locked scope {case.get('expected_locked_scope_id')!r}, "
                    f"got {locked_scope_id!r}"
                )
            expected_label = ANNOTATED_MENU_LABELS.get(locked_scope_id)
            if expected_label is not None and locked_scope.get("label") != expected_label:
                errors.append(f"{case_id}: locked scope label must preserve annotated source-reality wording")
            required_reality = SOURCE_REALITY_CONFIRMATION_PHRASES.get(locked_scope_id)
            prompt = confirmation.get("user_facing_prompt", "")
            if required_reality is not None and required_reality not in prompt:
                errors.append(
                    f"{case_id}: confirmed prompt must include source-reality phrase "
                    f"{required_reality!r}"
                )
        if questions:
            errors.append(f"{case_id}: confirmed scope must not ask a clarifying question")
        if actual_blockers:
            errors.append(f"{case_id}: confirmed scope must not have blockers")
    else:
        if locked_scope is not None:
            errors.append(f"{case_id}: blocked scope cases must not include locked_scope")
        if len(questions) != 1:
            errors.append(f"{case_id}: blocked Gate 2 cases must ask exactly one focused question")
        if actual_status == "needs_user_scope_choice":
            prompt = confirmation.get("user_facing_prompt", "")
            question_text = questions[0] if len(questions) == 1 else ""
            for scope_id, label in ANNOTATED_MENU_LABELS.items():
                if label not in prompt:
                    errors.append(f"{case_id}: menu prompt missing annotated option for {scope_id}")
                if label not in question_text:
                    errors.append(f"{case_id}: menu question missing annotated option for {scope_id}")

    if category == "menu_prompt" and actual_status != "needs_user_scope_choice":
        errors.append(f"{case_id}: menu prompt case must need a user scope choice")
    if category == "ambiguous_scope" and actual_status != "needs_scope_clarification":
        errors.append(f"{case_id}: ambiguous scope case must need scope clarification")
    if category in SCOPE_IDS and actual_status != "scope_confirmed":
        errors.append(f"{case_id}: menu option case must confirm the scope")

    if actual_status != "scope_confirmed" and actual_can_proceed:
        errors.append(f"{case_id}: only scope_confirmed may proceed to evidence search")

    safety = packet.get("safety", {})
    if isinstance(safety, dict) and safety.get("evidence_search_started") is not False:
        errors.append(f"{case_id}: Gate 2 must not start evidence search")

    return errors


def main() -> int:
    test_cases = read_json(TEST_CASES_PATH)
    if not isinstance(test_cases, dict):
        return fail("audit-scope test-cases root must be a JSON object")
    if test_cases.get("workflow_gate") != "audit_scope_lock":
        return fail("workflow_gate must be 'audit_scope_lock'")

    cases = test_cases.get("cases")
    if not isinstance(cases, list) or not cases:
        return fail("audit-scope test-cases must contain a non-empty cases array")

    categories = {case.get("category") for case in cases if isinstance(case, dict)}
    missing_categories = sorted(REQUIRED_CATEGORIES - categories)
    if missing_categories:
        return fail(f"missing required case categories: {missing_categories}")

    declared_categories = set(test_cases.get("required_case_categories", []))
    missing_declared_categories = sorted(REQUIRED_CATEGORIES - declared_categories)
    if missing_declared_categories:
        return fail(f"required_case_categories omits: {missing_declared_categories}")

    errors: list[str] = []
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case entry must be a JSON object")
            continue
        errors.extend(validate_case(case))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return fail(f"{len(errors)} error(s)")

    print(f"validated {len(cases)} Gate 2 audit-scope cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
