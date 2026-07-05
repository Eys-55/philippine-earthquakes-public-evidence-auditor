#!/usr/bin/env python3
"""Validate V2 Gate 2 earthquake-only scope lock fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
V2_DATA_DIR = ROOT / "data/philippines-building-code-evidence-auditor-v2"
SCOPE_CASES_PATH = V2_DATA_DIR / "earthquake-scope-test-cases.json"
SOURCE_REALITY_PATH = V2_DATA_DIR / "earthquake-source-reality.json"
COMPATIBILITY_PATHS = [
    V2_DATA_DIR / "audit-scope-test-cases.json",
    V2_DATA_DIR / "audit-scope-source-reality.json",
    V2_DATA_DIR / "gate-2-six-establishment-menu-matrix.json",
    V2_DATA_DIR / "source-landscape.json",
]

COMPATIBILITY_POINTER_CONTRACTS = {
    V2_DATA_DIR / "audit-scope-test-cases.json": {
        "status": "redirected_to_v2_earthquake_scope_lock",
        "canonical_file": "earthquake-scope-test-cases.json",
        "allowed_keys": {
            "schema_version",
            "workflow_gate",
            "status",
            "canonical_file",
            "purpose",
            "active_scope_ids",
            "active_menu_labels",
            "guardrail",
        },
    },
    V2_DATA_DIR / "audit-scope-source-reality.json": {
        "status": "redirected_to_v2_earthquake_scope_lock",
        "canonical_file": "earthquake-source-reality.json",
        "allowed_keys": {
            "schema_version",
            "workflow_gate",
            "status",
            "canonical_file",
            "purpose",
            "active_scope_ids",
            "source_reality_summary",
            "guardrail",
        },
    },
    V2_DATA_DIR / "gate-2-six-establishment-menu-matrix.json": {
        "status": "deprecated_redirect",
        "canonical_files": [
            "earthquake-scope-test-cases.json",
            "earthquake-source-reality.json",
        ],
        "allowed_keys": {
            "schema_version",
            "workflow_gate",
            "status",
            "canonical_files",
            "purpose",
            "active_scope_ids",
            "guardrail",
        },
    },
    V2_DATA_DIR / "source-landscape.json": {
        "status": "redirected_to_v2_earthquake_source_reality",
        "canonical_file": "earthquake-source-reality.json",
        "allowed_keys": {
            "schema_version",
            "workflow_gate",
            "status",
            "canonical_file",
            "purpose",
            "active_scope_ids",
            "guardrail",
        },
    },
}

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
    "menu_prompt",
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review_evidence",
    "post_earthquake_tag_status",
    "clearance_after_damage_or_tag",
    "ambiguous_scope",
    "unsupported_broad_scope",
}

STATUS_VALUES = {
    "needs_user_scope_choice",
    "needs_scope_clarification",
    "scope_confirmed",
    "unsupported_scope",
}

ANSWER_SOURCES = {
    "not_answered",
    "number",
    "label",
    "natural_language",
}

BLOCKERS = {
    "waiting_for_earthquake_scope_choice",
    "ambiguous_earthquake_scope",
    "unsupported_non_earthquake_scope",
}

SOURCE_STATUS_VALUES = {
    "public_searchable",
    "public_process_only",
    "manual_request_needed",
    "not_publicly_provable",
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

FORBIDDEN_COMPATIBILITY_ACTIVE_DATA_KEYS = {
    "cases",
    "scope_reality",
    "matrix",
    "menu",
    "scope_menu",
    "menu_results",
    "targets",
    "sample_packet",
    "scope_confirmation",
    "evidence_results",
    "source_status_values",
    "global_safety_rule",
    "ecc_review",
}


def fail(message: str) -> int:
    print(f"building-code v2 earthquake scope validation failed: {message}", file=sys.stderr)
    return 1


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


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
    allowed: set[str] | None = None,
    expected: list[str] | None = None,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
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
    required = {"display_name", "candidate_id", "city", "country", "gate_1_status"}
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    for key in ("display_name", "candidate_id", "city"):
        expect_string(obj.get(key), f"{path}.{key}", errors)
    if obj.get("country") != "Philippines":
        errors.append(f"{path}.country: must be 'Philippines'")
    if obj.get("gate_1_status") != "confirmed_by_user":
        errors.append(f"{path}.gate_1_status: must be 'confirmed_by_user'")


def validate_user_intake(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"raw_user_scope_request", "interpreted_scope", "answer_source"}
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    expect_string(obj.get("raw_user_scope_request"), f"{path}.raw_user_scope_request", errors, allow_null=True)
    interpreted = obj.get("interpreted_scope")
    if interpreted is not None and interpreted not in ALLOWED_SCOPE_IDS:
        errors.append(f"{path}.interpreted_scope: must be one of {ALLOWED_SCOPE_IDS!r} or null")
    if obj.get("answer_source") not in ANSWER_SOURCES:
        errors.append(f"{path}.answer_source: must be one of {sorted(ANSWER_SOURCES)!r}")


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
        item_path = f"{path}[{index}]"
        obj = require_object(item, item_path, errors)
        if obj is None:
            continue
        required = {"number", "scope_id", "label"}
        missing = sorted(required - set(obj))
        if missing:
            errors.append(f"{item_path}: missing required keys {missing}")
        if set(obj) - required:
            errors.append(f"{item_path}: unexpected keys {sorted(set(obj) - required)}")
        number = obj.get("number")
        if not isinstance(number, int):
            errors.append(f"{item_path}.number: must be an integer")
        else:
            numbers.append(number)
        scope_id = obj.get("scope_id")
        if scope_id not in ALLOWED_SCOPE_IDS:
            errors.append(f"{item_path}.scope_id: must be one of {ALLOWED_SCOPE_IDS!r}")
        elif isinstance(scope_id, str):
            scope_ids.append(scope_id)
        label = obj.get("label")
        if not isinstance(label, str):
            errors.append(f"{item_path}.label: must be a string")
        else:
            labels.append(label)

    if numbers != [1, 2, 3, 4]:
        errors.append(f"{path}: menu numbers must be [1, 2, 3, 4]")
    if scope_ids != ALLOWED_SCOPE_IDS:
        errors.append(f"{path}: menu scope order must be {ALLOWED_SCOPE_IDS!r}")
    if labels != REQUIRED_MENU_LABELS:
        errors.append(f"{path}: menu labels must be {REQUIRED_MENU_LABELS!r}")


def validate_locked_scope(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"scope_id", "label", "output_intent"}
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    if set(obj) - required:
        errors.append(f"{path}: unexpected keys {sorted(set(obj) - required)}")
    scope_id = obj.get("scope_id")
    if scope_id not in ALLOWED_SCOPE_IDS:
        errors.append(f"{path}.scope_id: must be one of {ALLOWED_SCOPE_IDS!r}")
    else:
        expected_label = REQUIRED_MENU_LABELS[ALLOWED_SCOPE_IDS.index(scope_id)]
        if obj.get("label") != expected_label:
            errors.append(f"{path}.label: must be {expected_label!r}")
    expect_string(obj.get("output_intent"), f"{path}.output_intent", errors)


def validate_confirmation(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {
        "status",
        "locked_scope",
        "user_facing_prompt",
        "clarifying_questions",
        "can_proceed_to_evidence_search",
        "blockers",
    }
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    status = obj.get("status")
    if status not in STATUS_VALUES:
        errors.append(f"{path}.status: must be one of {sorted(STATUS_VALUES)!r}")
    expect_string(obj.get("user_facing_prompt"), f"{path}.user_facing_prompt", errors)
    expect_string_array(obj.get("clarifying_questions"), f"{path}.clarifying_questions", errors)
    expect_string_array(obj.get("blockers"), f"{path}.blockers", errors, allowed=BLOCKERS)
    can_proceed = obj.get("can_proceed_to_evidence_search")
    if not isinstance(can_proceed, bool):
        errors.append(f"{path}.can_proceed_to_evidence_search: must be a boolean")

    locked_scope = obj.get("locked_scope")
    if can_proceed is True:
        if status != "scope_confirmed":
            errors.append(f"{path}: can_proceed_to_evidence_search true requires status 'scope_confirmed'")
        validate_locked_scope(locked_scope, f"{path}.locked_scope", errors)
    elif locked_scope is not None:
        errors.append(f"{path}.locked_scope: must be null when Gate 2 cannot proceed")


def validate_safety(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    if obj.get("evidence_search_started") is not False:
        errors.append(f"{path}.evidence_search_started: Gate 2 must not start evidence search")
    expect_string_array(obj.get("blocked_work"), f"{path}.blocked_work", errors)


def validate_packet(packet: object, path: str, errors: list[str]) -> None:
    obj = require_object(packet, path, errors)
    if obj is None:
        return
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
    if obj.get("schema_version") != "2.0.0":
        errors.append(f"{path}.schema_version: must be '2.0.0'")
    if obj.get("workflow_step") != "earthquake_scope_lock":
        errors.append(f"{path}.workflow_step: must be 'earthquake_scope_lock'")
    validate_confirmed_place(obj.get("confirmed_place"), f"{path}.confirmed_place", errors)
    validate_user_intake(obj.get("user_intake"), f"{path}.user_intake", errors)
    validate_menu(obj.get("scope_menu"), f"{path}.scope_menu", errors)
    validate_confirmation(obj.get("scope_confirmation"), f"{path}.scope_confirmation", errors)
    validate_safety(obj.get("safety"), f"{path}.safety", errors)


def validate_scope_case(case: object, path: str, errors: list[str]) -> None:
    obj = require_object(case, path, errors)
    if obj is None:
        return
    category = obj.get("category")
    if category not in REQUIRED_CATEGORIES:
        errors.append(f"{path}.category: must be one of {sorted(REQUIRED_CATEGORIES)!r}")
    validate_packet(obj.get("sample_packet"), f"{path}.sample_packet", errors)

    packet = obj.get("sample_packet")
    if not isinstance(packet, dict):
        return
    confirmation = packet.get("scope_confirmation")
    if not isinstance(confirmation, dict):
        return
    if confirmation.get("status") != obj.get("expected_status"):
        errors.append(f"{path}: status does not match expected_status")
    if confirmation.get("can_proceed_to_evidence_search") is not obj.get("expected_can_proceed_to_evidence_search"):
        errors.append(f"{path}: can_proceed_to_evidence_search does not match expected value")
    if set(confirmation.get("blockers", [])) != set(obj.get("expected_blockers", [])):
        errors.append(f"{path}: blockers do not match expected_blockers")

    locked_scope = confirmation.get("locked_scope")
    if category in ALLOWED_SCOPE_IDS:
        if confirmation.get("status") != "scope_confirmed":
            errors.append(f"{path}: allowed scope case must be scope_confirmed")
        if not isinstance(locked_scope, dict):
            errors.append(f"{path}: allowed scope case must include locked_scope")
        elif locked_scope.get("scope_id") != obj.get("expected_locked_scope_id"):
            errors.append(f"{path}: locked scope does not match expected_locked_scope_id")
    elif confirmation.get("can_proceed_to_evidence_search") is True:
        errors.append(f"{path}: only one of the four earthquake scope categories may proceed")

    if category == "menu_prompt" and confirmation.get("status") != "needs_user_scope_choice":
        errors.append(f"{path}: menu_prompt must need user scope choice")
    if category == "ambiguous_scope" and confirmation.get("status") != "needs_scope_clarification":
        errors.append(f"{path}: ambiguous_scope must need scope clarification")
    if category == "unsupported_broad_scope" and confirmation.get("status") != "unsupported_scope":
        errors.append(f"{path}: unsupported_broad_scope must be unsupported_scope")


def validate_scope_cases(document: object) -> list[str]:
    errors: list[str] = []
    root = require_object(document, "<scope_cases>", errors)
    if root is None:
        return errors
    if root.get("schema_version") != "2.0.0":
        errors.append("<scope_cases>.schema_version: must be '2.0.0'")
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


def validate_source(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"name", "url", "source_type", "status", "use"}
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    for key in ("name", "source_type", "status", "use"):
        expect_string(obj.get(key), f"{path}.{key}", errors)
    url = obj.get("url")
    if not isinstance(url, str) or not is_http_url(url):
        errors.append(f"{path}.url: must be an HTTP/HTTPS URL")
    if obj.get("status") not in SOURCE_STATUS_VALUES:
        errors.append(f"{path}.status: must be one of {sorted(SOURCE_STATUS_VALUES)!r}")


def validate_source_scope(scope: object, path: str, errors: list[str]) -> str | None:
    obj = require_object(scope, path, errors)
    if obj is None:
        return None
    required = {
        "scope_id",
        "label",
        "source_reality",
        "accepted_evidence_types",
        "source_reality_status",
        "likely_public_sources",
        "no_evidence_semantics",
        "forbidden_claims",
        "manual_request_targets",
        "ecc_review_notes",
    }
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{path}: missing required keys {missing}")
    scope_id = obj.get("scope_id")
    if scope_id not in ALLOWED_SCOPE_IDS:
        errors.append(f"{path}.scope_id: must be one of {ALLOWED_SCOPE_IDS!r}")
    else:
        expected_label = REQUIRED_MENU_LABELS[ALLOWED_SCOPE_IDS.index(scope_id)]
        if obj.get("label") != expected_label:
            errors.append(f"{path}.label: must be {expected_label!r}")
    expect_string(obj.get("source_reality"), f"{path}.source_reality", errors)
    expect_string(obj.get("no_evidence_semantics"), f"{path}.no_evidence_semantics", errors)
    expect_string_array(obj.get("accepted_evidence_types"), f"{path}.accepted_evidence_types", errors)
    expect_string_array(
        obj.get("source_reality_status"),
        f"{path}.source_reality_status",
        errors,
        allowed=SOURCE_STATUS_VALUES,
    )
    expect_string_array(obj.get("forbidden_claims"), f"{path}.forbidden_claims", errors)
    expect_string_array(obj.get("manual_request_targets"), f"{path}.manual_request_targets", errors)
    expect_string_array(obj.get("ecc_review_notes"), f"{path}.ecc_review_notes", errors)

    sources = obj.get("likely_public_sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{path}.likely_public_sources: must be a non-empty array")
    else:
        for index, source in enumerate(sources):
            validate_source(source, f"{path}.likely_public_sources[{index}]", errors)
    return scope_id if isinstance(scope_id, str) else None


def validate_source_reality(document: object) -> list[str]:
    errors: list[str] = []
    root = require_object(document, "<source_reality>", errors)
    if root is None:
        return errors
    if root.get("schema_version") != "2.0.0":
        errors.append("<source_reality>.schema_version: must be '2.0.0'")
    if root.get("workflow_gate") != "earthquake_scope_lock":
        errors.append("<source_reality>.workflow_gate: must be 'earthquake_scope_lock'")
    expect_string_array(
        root.get("source_status_values"),
        "<source_reality>.source_status_values",
        errors,
        allowed=SOURCE_STATUS_VALUES,
    )
    expect_string(root.get("global_safety_rule"), "<source_reality>.global_safety_rule", errors)

    scopes = root.get("scope_reality")
    if not isinstance(scopes, list):
        errors.append("<source_reality>.scope_reality: must be an array")
        return errors
    if len(scopes) != 4:
        errors.append("<source_reality>.scope_reality: must contain exactly four scopes")
    seen: list[str] = []
    for index, scope in enumerate(scopes):
        scope_id = validate_source_scope(scope, f"<source_reality>.scope_reality[{index}]", errors)
        if scope_id is not None:
            seen.append(scope_id)
    if seen != ALLOWED_SCOPE_IDS:
        errors.append(f"<source_reality>.scope_reality: scope order must be {ALLOWED_SCOPE_IDS!r}")

    ecc_review = root.get("ecc_review")
    if not isinstance(ecc_review, dict):
        errors.append("<source_reality>.ecc_review: must be an object")
    else:
        for key in ("objective", "handoff", "overclaim_boundary"):
            expect_string(ecc_review.get(key), f"<source_reality>.ecc_review.{key}", errors)
        for key in ("inputs", "outputs", "eval", "human_boundary", "safety_risks"):
            expect_string_array(ecc_review.get(key), f"<source_reality>.ecc_review.{key}", errors)
    return errors


def validate_compatibility_pointer(path: Path, errors: list[str]) -> None:
    document = read_json(path)
    rel_path = str(path.relative_to(ROOT))
    obj = require_object(document, rel_path, errors)
    if obj is None:
        return

    contract = COMPATIBILITY_POINTER_CONTRACTS.get(path)
    if contract is None:
        errors.append(f"{rel_path}: missing compatibility pointer contract")
        return

    active_keys = sorted(FORBIDDEN_COMPATIBILITY_ACTIVE_DATA_KEYS & set(obj))
    if active_keys:
        errors.append(f"{rel_path}: redirect pointer must not contain active data keys {active_keys}")

    allowed_keys = contract["allowed_keys"]
    extra_keys = sorted(set(obj) - allowed_keys)
    if extra_keys:
        errors.append(f"{rel_path}: redirect pointer has unexpected keys {extra_keys}")

    if obj.get("schema_version") != "2.0.0":
        errors.append(f"{rel_path}.schema_version: must be '2.0.0'")
    if obj.get("workflow_gate") != "earthquake_scope_lock":
        errors.append(f"{rel_path}.workflow_gate: must be 'earthquake_scope_lock'")
    if obj.get("status") != contract["status"]:
        errors.append(f"{rel_path}.status: must be {contract['status']!r}")
    expect_string(obj.get("purpose"), f"{rel_path}.purpose", errors)
    expect_string(obj.get("guardrail"), f"{rel_path}.guardrail", errors)

    if "canonical_file" in contract:
        if obj.get("canonical_file") != contract["canonical_file"]:
            errors.append(f"{rel_path}.canonical_file: must be {contract['canonical_file']!r}")
        if "canonical_files" in obj:
            errors.append(f"{rel_path}.canonical_files: must not be present for single-file redirect")
    else:
        if obj.get("canonical_files") != contract["canonical_files"]:
            errors.append(f"{rel_path}.canonical_files: must be {contract['canonical_files']!r}")
        if "canonical_file" in obj:
            errors.append(f"{rel_path}.canonical_file: must not be present for multi-file redirect")

    expect_string_array(
        obj.get("active_scope_ids"),
        f"{rel_path}.active_scope_ids",
        errors,
        expected=ALLOWED_SCOPE_IDS,
    )

    if "active_menu_labels" in obj:
        expect_string_array(
            obj.get("active_menu_labels"),
            f"{rel_path}.active_menu_labels",
            errors,
            expected=REQUIRED_MENU_LABELS,
        )
    if "source_reality_summary" in obj:
        expect_string_array(obj.get("source_reality_summary"), f"{rel_path}.source_reality_summary", errors)


def main() -> int:
    errors: list[str] = []
    for path in [SCOPE_CASES_PATH, SOURCE_REALITY_PATH, *COMPATIBILITY_PATHS]:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        try:
            scan_for_forbidden_strings(path, errors)
        except UnicodeDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot read as UTF-8: {exc}")

    try:
        errors.extend(validate_scope_cases(read_json(SCOPE_CASES_PATH)))
    except json.JSONDecodeError as exc:
        errors.append(f"{SCOPE_CASES_PATH.relative_to(ROOT)}: invalid JSON: {exc}")

    try:
        errors.extend(validate_source_reality(read_json(SOURCE_REALITY_PATH)))
    except json.JSONDecodeError as exc:
        errors.append(f"{SOURCE_REALITY_PATH.relative_to(ROOT)}: invalid JSON: {exc}")

    for path in COMPATIBILITY_PATHS:
        try:
            validate_compatibility_pointer(path, errors)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return fail(f"{len(errors)} error(s)")

    print("validated V2 Gate 2 earthquake scope lock: 7 cases, 4 source-reality lanes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
