#!/usr/bin/env python3
"""Validate Gate 3 building-code earthquake evidence packets."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


LANE_IDS = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
}

LANE_TYPES = {"availability_only", "availability_and_answer"}

ANSWERABILITY_VALUES = {"answerable", "not_answerable"}

PUBLIC_EVIDENCE_STATUSES = {
    "confirmed_public_evidence",
    "partial_public_evidence",
    "not_found",
    "manual_request_needed",
    "not_assessable_from_public_web",
    "conflicting",
}

STOP_REASONS = {
    "answer_found",
    "no_more_useful_public_sources",
    "manual_record_needed",
    "target_or_timeframe_unclear",
    "professional_review_required",
    "source_conflict",
}

SOURCE_TYPES = {
    "official_lgu",
    "official_national",
    "official_obo_ocbo",
    "company_filing",
    "operator_or_developer",
    "professional_or_contractor",
    "reputable_news_lead",
    "standards_context",
    "manual_request_path",
    "other",
}

FORBIDDEN_UNSUPPORTED_PHRASES = {
    "earthquake-proof",
    "earthquake proof",
    "nscp compliant",
    "structurally safe",
    "structurally unsafe",
    "safe to occupy",
    "fit for occupancy",
    "has no permit",
    "no permit",
    "unpermitted",
}

OVERCLAIM_EXEMPT_PATH_PARTS = {
    "forbidden_claims",
    "does_not_support",
    "blocked_claims",
}


def fail(message: str) -> int:
    print(f"building code packet validation failed: {message}", file=sys.stderr)
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
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: must be a non-empty string")


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
    require_non_empty: bool = True,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return
    if require_non_empty and not value:
        errors.append(f"{path}: must not be empty")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}[{index}]: must be a non-empty string")
        elif allowed is not None and item not in allowed:
            errors.append(f"{path}[{index}]: must be one of {sorted(allowed)!r}")


def validate_source(source: object, path: str, errors: list[str]) -> None:
    obj = require_object(source, path, errors)
    if obj is None:
        return
    allowed = {
        "title",
        "url",
        "source_type",
        "publisher",
        "date_published_or_accessed",
        "target_specific",
        "supports",
        "does_not_support",
    }
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("title"), f"{path}.title", errors)
    url = obj.get("url")
    if not isinstance(url, str) or not is_http_url(url):
        errors.append(f"{path}.url: must be an HTTP/HTTPS URL")
    expect_enum(obj.get("source_type"), f"{path}.source_type", SOURCE_TYPES, errors)
    expect_string(obj.get("publisher"), f"{path}.publisher", errors)
    expect_string(obj.get("date_published_or_accessed"), f"{path}.date_published_or_accessed", errors)
    expect_bool(obj.get("target_specific"), f"{path}.target_specific", errors)
    expect_string(obj.get("supports"), f"{path}.supports", errors)
    expect_string(obj.get("does_not_support"), f"{path}.does_not_support", errors)


def validate_confirmed_place(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"display_name", "candidate_id", "city", "country", "gate_1_status"}
    require_keys(obj, path, required, errors)
    expect_string(obj.get("display_name"), f"{path}.display_name", errors)
    expect_string(obj.get("candidate_id"), f"{path}.candidate_id", errors)
    expect_string(obj.get("city"), f"{path}.city", errors)
    if obj.get("country") != "Philippines":
        errors.append(f"{path}.country: must be 'Philippines'")
    if obj.get("gate_1_status") != "confirmed_by_user":
        errors.append(f"{path}.gate_1_status: must be 'confirmed_by_user'")


def validate_locked_scope(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"scope_ids", "selected_lanes", "requires_timeframe", "requires_target_subscope", "output_intent"}
    require_keys(obj, path, required, errors)
    expect_string_array(obj.get("scope_ids"), f"{path}.scope_ids", errors, LANE_IDS)
    expect_string_array(obj.get("selected_lanes"), f"{path}.selected_lanes", errors, LANE_IDS)
    if obj.get("scope_ids") != obj.get("selected_lanes"):
        errors.append(f"{path}: scope_ids and selected_lanes must match")
    expect_bool(obj.get("requires_timeframe"), f"{path}.requires_timeframe", errors)
    expect_bool(obj.get("requires_target_subscope"), f"{path}.requires_target_subscope", errors)
    expect_string(obj.get("output_intent"), f"{path}.output_intent", errors)


def validate_target_context(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    allowed = {"target_subscope", "timeframe", "earthquake_event", "jurisdiction", "identity_caveats"}
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    expect_string(obj.get("target_subscope"), f"{path}.target_subscope", errors)
    expect_string(obj.get("timeframe"), f"{path}.timeframe", errors, allow_null=True)
    expect_string(obj.get("earthquake_event"), f"{path}.earthquake_event", errors, allow_null=True)
    jurisdiction = require_object(obj.get("jurisdiction"), f"{path}.jurisdiction", errors)
    if jurisdiction is not None:
        for key in ("lgu", "likely_obo_or_ocbo", "country"):
            expect_string(jurisdiction.get(key), f"{path}.jurisdiction.{key}", errors)
        if jurisdiction.get("country") != "Philippines":
            errors.append(f"{path}.jurisdiction.country: must be 'Philippines'")
    expect_string_array(obj.get("identity_caveats"), f"{path}.identity_caveats", errors, require_non_empty=False)


def validate_lane_result(lane: object, path: str, errors: list[str]) -> None:
    obj = require_object(lane, path, errors)
    if obj is None:
        return
    allowed = {
        "lane_id",
        "lane_type",
        "question",
        "document_targets_searched",
        "query_log",
        "best_sources",
        "answer_found",
        "answerability",
        "answer_text",
        "public_evidence_status",
        "stop_reason",
        "manual_follow_up_needed",
        "manual_custodians",
        "overclaim_risk",
    }
    require_keys(obj, path, allowed, errors)
    forbid_extra_keys(obj, path, allowed, errors)
    lane_id = obj.get("lane_id")
    lane_type = obj.get("lane_type")
    expect_enum(lane_id, f"{path}.lane_id", LANE_IDS, errors)
    expect_enum(lane_type, f"{path}.lane_type", LANE_TYPES, errors)
    expect_string(obj.get("question"), f"{path}.question", errors)
    expect_string_array(obj.get("document_targets_searched"), f"{path}.document_targets_searched", errors)
    expect_string_array(obj.get("query_log"), f"{path}.query_log", errors)
    sources = obj.get("best_sources")
    if not isinstance(sources, list):
        errors.append(f"{path}.best_sources: must be an array")
    else:
        for index, source in enumerate(sources):
            validate_source(source, f"{path}.best_sources[{index}]", errors)
    expect_bool(obj.get("answer_found"), f"{path}.answer_found", errors)
    expect_enum(obj.get("answerability"), f"{path}.answerability", ANSWERABILITY_VALUES, errors)
    expect_string(obj.get("answer_text"), f"{path}.answer_text", errors, allow_null=True)
    expect_enum(obj.get("public_evidence_status"), f"{path}.public_evidence_status", PUBLIC_EVIDENCE_STATUSES, errors)
    expect_enum(obj.get("stop_reason"), f"{path}.stop_reason", STOP_REASONS, errors)
    expect_bool(obj.get("manual_follow_up_needed"), f"{path}.manual_follow_up_needed", errors)
    expect_string_array(obj.get("manual_custodians"), f"{path}.manual_custodians", errors, require_non_empty=False)
    expect_string(obj.get("overclaim_risk"), f"{path}.overclaim_risk", errors)

    if obj.get("answer_found") is True:
        if obj.get("answerability") != "answerable":
            errors.append(f"{path}.answerability: must be answerable when answer_found is true")
        if obj.get("answer_text") is None:
            errors.append(f"{path}.answer_text: must be present when answer_found is true")
        if obj.get("stop_reason") != "answer_found":
            errors.append(f"{path}.stop_reason: must be answer_found when answer_found is true")

    if obj.get("public_evidence_status") == "confirmed_public_evidence":
        if not any(isinstance(source, dict) and source.get("target_specific") is True for source in sources or []):
            errors.append(f"{path}.best_sources: confirmed_public_evidence requires a target-specific source")

    if lane_type == "availability_and_answer" and obj.get("answer_found") is False:
        if obj.get("answerability") != "not_answerable":
            errors.append(f"{path}.answerability: lanes 3-4 with no answer must be not_answerable")
        if obj.get("answer_text") is not None:
            errors.append(f"{path}.answer_text: lanes 3-4 with no answer must use null answer_text")
        if obj.get("manual_follow_up_needed") is not True:
            errors.append(f"{path}.manual_follow_up_needed: lanes 3-4 with no answer require manual follow-up")
        if not obj.get("manual_custodians"):
            errors.append(f"{path}.manual_custodians: lanes 3-4 with no answer require custodians")

    if lane_type == "availability_only" and obj.get("answer_found") is False:
        if obj.get("answerability") != "answerable":
            errors.append(f"{path}.answerability: availability-only no-public-evidence result is still answerable")
        if obj.get("answer_text") is None:
            errors.append(f"{path}.answer_text: availability-only no-public-evidence result must record answer text")


def validate_integrated_answer(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {
        "summary",
        "selected_scope_ids",
        "answerable_scope_ids",
        "not_answerable_scope_ids",
        "public_evidence_found",
        "manual_follow_up_required",
        "citizen_safe_summary",
    }
    require_keys(obj, path, required, errors)
    expect_string(obj.get("summary"), f"{path}.summary", errors)
    expect_string_array(obj.get("selected_scope_ids"), f"{path}.selected_scope_ids", errors, LANE_IDS)
    expect_string_array(obj.get("answerable_scope_ids"), f"{path}.answerable_scope_ids", errors, LANE_IDS, require_non_empty=False)
    expect_string_array(
        obj.get("not_answerable_scope_ids"),
        f"{path}.not_answerable_scope_ids",
        errors,
        LANE_IDS,
        require_non_empty=False,
    )
    expect_bool(obj.get("public_evidence_found"), f"{path}.public_evidence_found", errors)
    expect_bool(obj.get("manual_follow_up_required"), f"{path}.manual_follow_up_required", errors)
    expect_string(obj.get("citizen_safe_summary"), f"{path}.citizen_safe_summary", errors)


def validate_manual_follow_up(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"required", "custodians", "documents_to_request"}
    require_keys(obj, path, required, errors)
    expect_bool(obj.get("required"), f"{path}.required", errors)
    expect_string_array(obj.get("custodians"), f"{path}.custodians", errors, require_non_empty=obj.get("required") is True)
    expect_string_array(
        obj.get("documents_to_request"),
        f"{path}.documents_to_request",
        errors,
        require_non_empty=obj.get("required") is True,
    )


def validate_overclaim_boundary(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"forbidden_claims", "allowed_claim"}
    require_keys(obj, path, required, errors)
    expect_string_array(obj.get("forbidden_claims"), f"{path}.forbidden_claims", errors)
    expect_string(obj.get("allowed_claim"), f"{path}.allowed_claim", errors)


def validate_validation_summary(value: object, path: str, errors: list[str]) -> None:
    obj = require_object(value, path, errors)
    if obj is None:
        return
    required = {"status", "blocked_claims"}
    require_keys(obj, path, required, errors)
    expect_string(obj.get("status"), f"{path}.status", errors)
    expect_string_array(obj.get("blocked_claims"), f"{path}.blocked_claims", errors, require_non_empty=False)


def scan_overclaims(value: object, path: str, errors: list[str]) -> None:
    if any(part in path for part in OVERCLAIM_EXEMPT_PATH_PARTS):
        return
    if isinstance(value, dict):
        for key, item in value.items():
            scan_overclaims(item, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_overclaims(item, f"{path}[{index}]", errors)
    elif isinstance(value, str):
        lowered = value.lower()
        for phrase in FORBIDDEN_UNSUPPORTED_PHRASES:
            if phrase in lowered:
                errors.append(f"{path}: unsupported overclaim phrase {phrase!r}")


def validate_root(document: object) -> list[str]:
    errors: list[str] = []
    obj = require_object(document, "<root>", errors)
    if obj is None:
        return errors
    allowed = {
        "schema_version",
        "workflow_step",
        "confirmed_place",
        "locked_scope",
        "target_context",
        "lane_results",
        "integrated_answer",
        "manual_follow_up",
        "overclaim_boundary",
        "validation_summary",
    }
    require_keys(obj, "<root>", allowed, errors)
    forbid_extra_keys(obj, "<root>", allowed, errors)
    if obj.get("schema_version") != "1.0.0":
        errors.append("<root>.schema_version: must be '1.0.0'")
    if obj.get("workflow_step") != "earthquake_evidence_packet":
        errors.append("<root>.workflow_step: must be 'earthquake_evidence_packet'")
    validate_confirmed_place(obj.get("confirmed_place"), "<root>.confirmed_place", errors)
    validate_locked_scope(obj.get("locked_scope"), "<root>.locked_scope", errors)
    validate_target_context(obj.get("target_context"), "<root>.target_context", errors)
    lanes = obj.get("lane_results")
    if not isinstance(lanes, list) or not lanes:
        errors.append("<root>.lane_results: must be a non-empty array")
    else:
        for index, lane in enumerate(lanes):
            validate_lane_result(lane, f"<root>.lane_results[{index}]", errors)
    validate_integrated_answer(obj.get("integrated_answer"), "<root>.integrated_answer", errors)
    validate_manual_follow_up(obj.get("manual_follow_up"), "<root>.manual_follow_up", errors)
    validate_overclaim_boundary(obj.get("overclaim_boundary"), "<root>.overclaim_boundary", errors)
    validate_validation_summary(obj.get("validation_summary"), "<root>.validation_summary", errors)
    scan_overclaims(obj, "<root>", errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("usage: validate_building_code_packet.py <packet.json>")
    path = Path(argv[1])
    try:
        document = read_json(path)
    except FileNotFoundError:
        return fail(f"missing {path}")
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    errors = validate_root(document)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return fail(f"{len(errors)} error(s)")

    print(f"validated building code packet: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
