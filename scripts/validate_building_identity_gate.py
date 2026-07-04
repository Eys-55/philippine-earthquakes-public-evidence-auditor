#!/usr/bin/env python3
"""Validate Gate 1 building identity test cases and sample packets."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "data/building-code-auditor/building-identity-schema.json"
TEST_CASES_PATH = ROOT / "data/building-code-auditor/test-cases.json"

REQUIRED_CATEGORIES = {
    "clear_candidate",
    "ambiguous_similar_places",
    "tenant_vs_building",
    "complex_vs_building",
    "weak_clue",
    "rejected_candidate",
    "confirmed_place",
}

SOURCE_TYPES = {
    "google_maps",
    "booking_page",
    "official_website",
    "social_media",
    "news",
    "receipt_or_document_link",
    "other",
}

MEDIA_KINDS = {
    "photo",
    "screenshot",
    "receipt",
    "booking_confirmation",
    "document",
    "other",
}

ENTITY_TYPES = {
    "hotel",
    "mall",
    "condominium",
    "office_building",
    "school",
    "hospital",
    "public_facility",
    "tenant_or_establishment",
    "mixed_use_complex",
    "unknown",
}

BUILDING_SCOPES = {
    "whole_building",
    "establishment_inside_building",
    "building_complex_or_campus",
    "unclear",
}

CONFIDENCE_VALUES = {"high", "medium", "low", "unknown"}
CONFIRMATION_STATUSES = {
    "needs_more_user_info",
    "candidate_ready_for_user_confirmation",
    "confirmed_by_user",
    "rejected_by_user",
}
CLARIFICATION_STYLES = {
    "best_guess_only",
    "best_guess_with_quick_negative_check",
    "top_three_options",
}
BLOCKERS = {
    "no_candidate_found",
    "multiple_similar_candidates",
    "missing_city_or_location",
    "unclear_if_whole_building_or_tenant",
    "low_address_confidence",
    "waiting_for_user_confirmation",
}


def fail(message: str) -> int:
    print(f"building identity gate validation failed: {message}", file=sys.stderr)
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


def expect_string_array(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    for index, item in enumerate(value):
        expect_string(item, f"{path}[{index}]", errors)


def expect_enum(value: object, path: str, allowed: set[str], errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{path}: must be one of {sorted(allowed)!r}")


def expect_uri(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.startswith(("https://", "http://")):
        errors.append(f"{path}: must be an http or https URI")


def validate_source_link(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"url", "label", "source_type"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_uri(obj.get("url"), f"{path}.url", errors)
    expect_string(obj.get("label"), f"{path}.label", errors, allow_null=True)
    expect_enum(obj.get("source_type"), f"{path}.source_type", SOURCE_TYPES, errors)


def validate_known_location(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"city", "province_or_region", "address_text", "nearby_landmarks"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("city"), f"{path}.city", errors, allow_null=True)
    expect_string(obj.get("province_or_region"), f"{path}.province_or_region", errors, allow_null=True)
    expect_string(obj.get("address_text"), f"{path}.address_text", errors, allow_null=True)
    expect_string_array(obj.get("nearby_landmarks"), f"{path}.nearby_landmarks", errors)


def validate_user_intake(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {
        "raw_user_request",
        "known_name_or_description",
        "known_location",
        "provided_links",
        "provided_media_or_documents",
    }
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("raw_user_request"), f"{path}.raw_user_request", errors)
    expect_string(obj.get("known_name_or_description"), f"{path}.known_name_or_description", errors)
    validate_known_location(obj.get("known_location"), f"{path}.known_location", errors)

    links = obj.get("provided_links")
    if not isinstance(links, list):
        errors.append(f"{path}.provided_links: must be an array")
    else:
        for index, link in enumerate(links):
            validate_source_link(link, f"{path}.provided_links[{index}]", errors)

    media_items = obj.get("provided_media_or_documents")
    if not isinstance(media_items, list):
        errors.append(f"{path}.provided_media_or_documents: must be an array")
    else:
        for index, item in enumerate(media_items):
            item_path = f"{path}.provided_media_or_documents[{index}]"
            media = require_object(item, item_path, errors)
            if media is None:
                continue
            allowed_media = {"kind", "description", "file_or_reference"}
            require_keys(media, item_path, allowed_media, errors)
            forbid_extra_keys(media, item_path, allowed_media, errors)
            expect_enum(media.get("kind"), f"{item_path}.kind", MEDIA_KINDS, errors)
            expect_string(media.get("description"), f"{item_path}.description", errors)
            expect_string(media.get("file_or_reference"), f"{item_path}.file_or_reference", errors, allow_null=True)


def validate_address(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"full_address", "barangay", "city", "province_or_region", "country"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("full_address"), f"{path}.full_address", errors, allow_null=True)
    expect_string(obj.get("barangay"), f"{path}.barangay", errors, allow_null=True)
    expect_string(obj.get("city"), f"{path}.city", errors, allow_null=True)
    expect_string(obj.get("province_or_region"), f"{path}.province_or_region", errors, allow_null=True)
    if obj.get("country") != "Philippines":
        errors.append(f"{path}.country: must be 'Philippines'")


def validate_coordinates(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"latitude", "longitude", "source"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    latitude = obj.get("latitude")
    longitude = obj.get("longitude")
    if latitude is not None and not isinstance(latitude, (int, float)):
        errors.append(f"{path}.latitude: must be a number or null")
    if longitude is not None and not isinstance(longitude, (int, float)):
        errors.append(f"{path}.longitude: must be a number or null")
    expect_string(obj.get("source"), f"{path}.source", errors, allow_null=True)


def validate_jurisdiction(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"lgu", "likely_obo_or_building_office"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("lgu"), f"{path}.lgu", errors, allow_null=True)
    expect_string(
        obj.get("likely_obo_or_building_office"),
        f"{path}.likely_obo_or_building_office",
        errors,
        allow_null=True,
    )


def validate_evidence(value: object, path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        obj = require_object(item, item_path, errors)
        if obj is None:
            continue
        allowed = {"claim", "source", "notes"}
        require_keys(obj, item_path, allowed, errors)
        forbid_extra_keys(obj, item_path, allowed, errors)
        expect_string(obj.get("claim"), f"{item_path}.claim", errors)
        validate_source_link(obj.get("source"), f"{item_path}.source", errors)
        expect_string(obj.get("notes"), f"{item_path}.notes", errors, allow_null=True)


def validate_candidate(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {
        "candidate_id",
        "display_name",
        "aliases",
        "entity_type",
        "building_scope",
        "address",
        "coordinates",
        "jurisdiction",
        "known_operator_or_brand",
        "known_owner_or_developer",
        "identity_confidence",
        "why_this_candidate",
        "why_it_might_not_be_this",
        "evidence",
        "ambiguities",
    }
    required = {
        "candidate_id",
        "display_name",
        "aliases",
        "entity_type",
        "building_scope",
        "address",
        "coordinates",
        "jurisdiction",
        "known_operator_or_brand",
        "known_owner_or_developer",
        "identity_confidence",
        "evidence",
        "ambiguities",
    }
    require_keys(obj, path, required, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("candidate_id"), f"{path}.candidate_id", errors)
    expect_string(obj.get("display_name"), f"{path}.display_name", errors)
    expect_string_array(obj.get("aliases"), f"{path}.aliases", errors)
    expect_enum(obj.get("entity_type"), f"{path}.entity_type", ENTITY_TYPES, errors)
    expect_enum(obj.get("building_scope"), f"{path}.building_scope", BUILDING_SCOPES, errors)
    validate_address(obj.get("address"), f"{path}.address", errors)
    validate_coordinates(obj.get("coordinates"), f"{path}.coordinates", errors)
    validate_jurisdiction(obj.get("jurisdiction"), f"{path}.jurisdiction", errors)
    expect_string(obj.get("known_operator_or_brand"), f"{path}.known_operator_or_brand", errors, allow_null=True)
    expect_string(obj.get("known_owner_or_developer"), f"{path}.known_owner_or_developer", errors, allow_null=True)
    expect_enum(obj.get("identity_confidence"), f"{path}.identity_confidence", CONFIDENCE_VALUES, errors)
    if "why_this_candidate" in obj:
        expect_string_array(obj.get("why_this_candidate"), f"{path}.why_this_candidate", errors)
    if "why_it_might_not_be_this" in obj:
        expect_string_array(obj.get("why_it_might_not_be_this"), f"{path}.why_it_might_not_be_this", errors)
    validate_evidence(obj.get("evidence"), f"{path}.evidence", errors)
    expect_string_array(obj.get("ambiguities"), f"{path}.ambiguities", errors)


def validate_confirmation(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {
        "status",
        "user_facing_confirmation_prompt",
        "clarification_style",
        "clarifying_questions",
        "can_proceed_to_audit",
        "blockers",
    }
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_enum(obj.get("status"), f"{path}.status", CONFIRMATION_STATUSES, errors)
    expect_string(obj.get("user_facing_confirmation_prompt"), f"{path}.user_facing_confirmation_prompt", errors)
    expect_enum(obj.get("clarification_style"), f"{path}.clarification_style", CLARIFICATION_STYLES, errors)
    expect_string_array(obj.get("clarifying_questions"), f"{path}.clarifying_questions", errors)
    if not isinstance(obj.get("can_proceed_to_audit"), bool):
        errors.append(f"{path}.can_proceed_to_audit: must be a boolean")
    blockers = obj.get("blockers")
    if not isinstance(blockers, list):
        errors.append(f"{path}.blockers: must be an array")
    else:
        for index, blocker in enumerate(blockers):
            expect_enum(blocker, f"{path}.blockers[{index}]", BLOCKERS, errors)


def validate_packet_shape(packet: object) -> list[str]:
    errors: list[str] = []
    obj = require_object(packet, "<root>", errors)
    if obj is None:
        return errors
    allowed = {
        "schema_version",
        "workflow_step",
        "user_intake",
        "identity_candidates",
        "selected_candidate",
        "confirmation",
    }
    require_keys(obj, "<root>", allowed, errors)
    forbid_extra_keys(obj, "<root>", allowed, errors)
    if obj.get("schema_version") != "1.0.0":
        errors.append("schema_version: must be '1.0.0'")
    if obj.get("workflow_step") != "building_identity_confirmation":
        errors.append("workflow_step: must be 'building_identity_confirmation'")
    validate_user_intake(obj.get("user_intake"), "user_intake", errors)

    candidates = obj.get("identity_candidates")
    if not isinstance(candidates, list):
        errors.append("identity_candidates: must be an array")
    else:
        if len(candidates) > 3:
            errors.append("identity_candidates: must contain at most three candidates")
        for index, candidate in enumerate(candidates):
            validate_candidate(candidate, f"identity_candidates[{index}]", errors)

    selected = obj.get("selected_candidate")
    if selected is not None:
        validate_candidate(selected, "selected_candidate", errors)
    validate_confirmation(obj.get("confirmation"), "confirmation", errors)
    return errors


def validate_case(case: dict) -> list[str]:
    errors: list[str] = []
    case_id = case.get("case_id", "<missing case_id>")
    packet_path_value = case.get("sample_packet_path")
    if not isinstance(packet_path_value, str):
        return [f"{case_id}: sample_packet_path must be a string"]

    packet_path = ROOT / packet_path_value
    if not packet_path.exists():
        return [f"{case_id}: missing sample packet {packet_path_value}"]

    shape_errors = validate_packet_shape(read_json(packet_path))
    errors.extend(f"{case_id}: packet shape: {message}" for message in shape_errors)
    if shape_errors:
        return errors

    packet = read_json(packet_path)
    if not isinstance(packet, dict):
        return [f"{case_id}: packet must be a JSON object"]

    confirmation = packet.get("confirmation", {})
    expected_status = case.get("expected_confirmation_status")
    actual_status = confirmation.get("status")
    if actual_status != expected_status:
        errors.append(f"{case_id}: expected status {expected_status!r}, got {actual_status!r}")

    expected_can_proceed = case.get("expected_can_proceed_to_audit")
    actual_can_proceed = confirmation.get("can_proceed_to_audit")
    if actual_can_proceed is not expected_can_proceed:
        errors.append(
            f"{case_id}: expected can_proceed_to_audit {expected_can_proceed!r}, "
            f"got {actual_can_proceed!r}"
        )

    expected_blockers = set(case.get("expected_blockers", []))
    actual_blockers = set(confirmation.get("blockers", []))
    if actual_blockers != expected_blockers:
        errors.append(
            f"{case_id}: expected blockers {sorted(expected_blockers)!r}, "
            f"got {sorted(actual_blockers)!r}"
        )

    selected_candidate = packet.get("selected_candidate")
    identity_candidates = packet.get("identity_candidates", [])
    category = case.get("category")
    clarifying_questions = confirmation.get("clarifying_questions", [])

    if actual_status == "confirmed_by_user":
        if clarifying_questions:
            errors.append(f"{case_id}: confirmed case must not ask another clarifying question")
    elif len(clarifying_questions) != 1:
        errors.append(f"{case_id}: blocked Gate 1 cases must ask exactly one focused question")

    if category == "clear_candidate":
        if selected_candidate is None:
            errors.append(f"{case_id}: clear candidate must select a best candidate")
        if len(identity_candidates) != 1:
            errors.append(f"{case_id}: clear candidate must have exactly one candidate")
    elif category == "ambiguous_similar_places":
        if not (2 <= len(identity_candidates) <= 3):
            errors.append(f"{case_id}: ambiguous case must have two or three candidates")
        if confirmation.get("clarification_style") != "top_three_options":
            errors.append(f"{case_id}: ambiguous case must use top_three_options")
    elif category == "tenant_vs_building":
        if not isinstance(selected_candidate, dict):
            errors.append(f"{case_id}: tenant case must select the tenant candidate")
        elif selected_candidate.get("building_scope") != "establishment_inside_building":
            errors.append(f"{case_id}: tenant case must mark establishment_inside_building")
    elif category == "complex_vs_building":
        if not isinstance(selected_candidate, dict):
            errors.append(f"{case_id}: complex case must select a best candidate")
        elif selected_candidate.get("building_scope") != "building_complex_or_campus":
            errors.append(f"{case_id}: complex case must mark building_complex_or_campus")
    elif category == "weak_clue":
        if selected_candidate is not None:
            errors.append(f"{case_id}: weak clue must not select a candidate")
        if identity_candidates:
            errors.append(f"{case_id}: weak clue must not include candidates")
    elif category == "rejected_candidate":
        if selected_candidate is not None:
            errors.append(f"{case_id}: rejected case must clear selected_candidate")
    elif category == "confirmed_place":
        if selected_candidate is None:
            errors.append(f"{case_id}: confirmed case must retain selected_candidate")
        if not actual_can_proceed:
            errors.append(f"{case_id}: confirmed case must unlock can_proceed_to_audit")

    if actual_status != "confirmed_by_user" and actual_can_proceed:
        errors.append(f"{case_id}: only confirmed_by_user may proceed to audit")
    if actual_status == "confirmed_by_user" and actual_blockers:
        errors.append(f"{case_id}: confirmed_by_user must not have blockers")

    return errors


def main() -> int:
    read_json(SCHEMA_PATH)
    test_cases = read_json(TEST_CASES_PATH)

    if not isinstance(test_cases, dict):
        return fail("test-cases root must be a JSON object")

    cases = test_cases.get("cases")
    if not isinstance(cases, list) or not cases:
        return fail("test-cases must contain a non-empty cases array")

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

    print(f"validated {len(cases)} Gate 1 place-lock cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
