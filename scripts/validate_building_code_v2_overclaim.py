#!/usr/bin/env python3
"""Validate V2 Gate 4 overclaim audit fixtures."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
V2_DATA_DIR = ROOT / "data/philippines-building-code-evidence-auditor-v2"
FIXTURE_DIR = V2_DATA_DIR / "overclaim-fixtures"

ALLOWED_LANES = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review_evidence",
    "post_earthquake_tag_status",
    "clearance_after_damage_or_tag",
}

BROAD_V1_SCOPE_PHRASES = {
    "permit occupancy records",
    "permit or occupancy records",
    "incident damage history",
    "incident damage closure repair retrofit history",
    "contractor professional developer",
    "contractor professional developer operator evidence",
    "standards context only",
    "standards or process context only",
    "broad public evidence packet",
    "broad public evidence scope",
    "broad packet lane",
}

NO_EVIDENCE_STATUSES = {
    "no_public_evidence_found",
    "no_public_answer_found",
}

OFFICIAL_OR_PROFESSIONAL_CLASSES = {
    "official_record",
    "professional_record",
}

OPERATOR_CLASSES = {
    "operator_corporate_claim",
}

WEAK_LEAD_CLASSES = {
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

FORBIDDEN_MISSING_EVIDENCE_PHRASES = {
    "earthquake safe",
    "earthquake unsafe",
    "is safe",
    "is unsafe",
    "safe for occupancy",
    "unsafe for occupancy",
    "is compliant",
    "is noncompliant",
    "non compliant",
    "non-compliant",
    "no tag",
    "no tag exists",
    "is cleared",
    "has clearance",
    "no permit exists",
    "not reviewed",
    "unpermitted",
    "no compliance concern",
}

FORBIDDEN_MISSING_EVIDENCE_STATUS_WORDS = {
    "cleared",
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
    "compliant",
    "safe",
    "unsafe",
}

OFFICIAL_CLEARANCE_CLAIM_PHRASES = {
    "official clearance found",
    "official clearance was found",
    "official clearance exists",
    "building was cleared",
    "building is cleared",
    "cleared after the event",
    "cleared for occupancy",
}

CHECKLIST_KEYS = {
    "exact_building_match_confirmed",
    "claim_source_urls_checked",
    "official_professional_evidence_separated_from_weak_leads",
    "operator_corporate_claims_not_treated_as_clearance",
    "missing_evidence_not_converted_to_conclusion",
    "red_yellow_tag_evidence_preserved",
    "unresolved_exceptions_preserved",
    "query_log_present_for_no_evidence",
}

PARENT_CHECKLIST_KEYS = {
    "exact_building_match_confirmed",
    "each_lane_packet_audited",
    "parent_summary_audited",
    "missing_evidence_not_converted_to_conclusion",
    "unresolved_exceptions_preserved",
}


def fail(message: str) -> int:
    print(f"building-code v2 overclaim validation failed: {message}", file=sys.stderr)
    return 1


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def normalize(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return re.sub(r"\s+", " ", value).strip()


def contains_phrase(text: str, phrase: str) -> bool:
    normalized_text = normalize(text)
    normalized_phrase = normalize(phrase)
    if not normalized_phrase:
        return False
    return re.search(rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)", normalized_text) is not None


def strings_in(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(strings_in(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(strings_in(item))
        return strings
    return []


def text_blob(value: object) -> str:
    return " ".join(strings_in(value))


def claim_text(packet: dict) -> str:
    result = packet.get("packet_result")
    boundary = packet.get("overclaim_boundary")
    result_obj = result if isinstance(result, dict) else {}
    boundary_obj = boundary if isinstance(boundary, dict) else {}
    return text_blob(
        {
            "packet_result": {
                "summary": result_obj.get("summary"),
                "answer_semantics": result_obj.get("answer_semantics"),
            },
            "overclaim_boundary": {
                "allowed_conclusion": boundary_obj.get("allowed_conclusion"),
                "missing_evidence_statement": boundary_obj.get("missing_evidence_statement"),
            },
        }
    )


def add_error(errors: list[tuple[str, str]], code: str, message: str) -> None:
    errors.append((code, message))


def evidence_items(packet: dict) -> list[dict]:
    items: list[dict] = []
    for key in ("document_inventory", "physical_condition_public_evidence"):
        value = packet.get(key)
        if isinstance(value, list):
            items.extend(item for item in value if isinstance(item, dict))
    return items


def is_eligible_positive_evidence_item(item: dict) -> bool:
    return (
        item.get("is_positive_evidence") is True
        and is_http_url(item.get("source_url"))
        and item.get("target_match_status") == "exact_target_match"
        and item.get("evidence_strength") not in INELIGIBLE_POSITIVE_EVIDENCE_STRENGTHS
        and item.get("source_curation_class") not in INELIGIBLE_POSITIVE_SOURCE_CLASSES
    )


def checklist_value(checklist: dict, key: str) -> object:
    return checklist.get(key)


def validate_fixture_shape(fixture: object, path: str, errors: list[tuple[str, str]]) -> tuple[dict, dict, dict] | None:
    if not isinstance(fixture, dict):
        add_error(errors, "fixture_shape", f"{path}: fixture must be an object")
        return None

    expected_valid = fixture.get("expected_valid")
    if not isinstance(expected_valid, bool):
        add_error(errors, "fixture_shape", f"{path}.expected_valid: must be boolean")

    expected_codes = fixture.get("expected_error_codes")
    if not isinstance(expected_codes, list) or not all(isinstance(code, str) for code in expected_codes):
        add_error(errors, "fixture_shape", f"{path}.expected_error_codes: must be an array of strings")

    checklist = fixture.get("gate4_checklist")
    if not isinstance(checklist, dict):
        add_error(errors, "fixture_shape", f"{path}.gate4_checklist: must be an object")
        checklist = {}

    missing_checklist_keys = sorted(CHECKLIST_KEYS - set(checklist))
    if missing_checklist_keys:
        add_error(errors, "fixture_shape", f"{path}.gate4_checklist: missing keys {missing_checklist_keys}")

    packet = fixture.get("packet")
    if not isinstance(packet, dict):
        add_error(errors, "fixture_shape", f"{path}.packet: must be an object")
        packet = {}

    return fixture, checklist, packet


def validate_exact_building(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    building = packet.get("confirmed_building")
    if not isinstance(building, dict):
        add_error(errors, "exact_building_match_not_confirmed", f"{path}: missing confirmed_building object")
        return

    if checklist_value(checklist, "exact_building_match_confirmed") is not True:
        add_error(errors, "exact_building_match_not_confirmed", f"{path}: Gate 4 checklist did not confirm exact match")

    required = ("display_name", "candidate_id", "city")
    for key in required:
        if not isinstance(building.get(key), str) or not building[key].strip():
            add_error(errors, "exact_building_match_not_confirmed", f"{path}.confirmed_building.{key}: missing")
    if building.get("country") != "Philippines":
        add_error(errors, "exact_building_match_not_confirmed", f"{path}.confirmed_building.country: must be Philippines")
    if building.get("gate_1_status") != "confirmed_by_user":
        add_error(
            errors,
            "exact_building_match_not_confirmed",
            f"{path}.confirmed_building.gate_1_status: must be confirmed_by_user",
        )


def validate_scope(packet: dict, path: str, errors: list[tuple[str, str]]) -> None:
    lane = packet.get("locked_earthquake_lane")
    if lane not in ALLOWED_LANES:
        add_error(errors, "invalid_locked_scope", f"{path}.locked_earthquake_lane: unsupported lane {lane!r}")

    blob = text_blob(packet)
    for phrase in sorted(BROAD_V1_SCOPE_PHRASES):
        if contains_phrase(blob, phrase):
            add_error(errors, "broad_v1_scope", f"{path}: contains broad V1 scope phrase {phrase!r}")


def validate_positive_claim_sources(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    if checklist_value(checklist, "claim_source_urls_checked") is not True:
        add_error(errors, "positive_claim_missing_source_url", f"{path}: source URL checklist was not confirmed")

    items = evidence_items(packet)
    sourced_positive_items = [
        item
        for item in items
        if item.get("is_positive_evidence") is True and is_http_url(item.get("source_url"))
    ]
    eligible_positive_items = [
        item for item in sourced_positive_items if is_eligible_positive_evidence_item(item)
    ]
    result = packet.get("packet_result")
    result_status = result.get("status") if isinstance(result, dict) else None
    if result_status == "positive_evidence_found" and not sourced_positive_items:
        add_error(
            errors,
            "positive_claim_missing_source_url",
            f"{path}: positive_evidence_found requires at least one positive evidence item with an http(s) source_url",
        )
    elif result_status == "positive_evidence_found" and not eligible_positive_items:
        add_error(
            errors,
            "positive_claim_not_target_specific",
            f"{path}: positive_evidence_found requires exact-target evidence beyond process context or weak leads",
        )

    for index, item in enumerate(items):
        if item.get("is_positive_evidence") is True and not is_http_url(item.get("source_url")):
            add_error(
                errors,
                "positive_claim_missing_source_url",
                f"{path}.evidence_items[{index}].source_url: positive claims require http(s) source URL",
            )


def validate_weak_lead_separation(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    if checklist_value(checklist, "official_professional_evidence_separated_from_weak_leads") is not True:
        add_error(errors, "weak_lead_not_separated", f"{path}: weak leads are not separated by checklist")

    items = evidence_items(packet)
    positive_items = [item for item in items if item.get("is_positive_evidence") is True]
    operator_positive = [
        item for item in positive_items if item.get("source_curation_class") in OPERATOR_CLASSES
    ]
    official_or_professional_positive = [
        item for item in positive_items if item.get("source_curation_class") in OFFICIAL_OR_PROFESSIONAL_CLASSES
    ]

    packet_status = packet.get("packet_result", {}).get("status") if isinstance(packet.get("packet_result"), dict) else None
    packet_source_class = packet.get("source_curation_class")
    if operator_positive and not official_or_professional_positive:
        if packet_status == "positive_evidence_found" or packet_source_class not in WEAK_LEAD_CLASSES:
            add_error(
                errors,
                "weak_lead_not_separated",
                f"{path}: operator/corporate-only evidence cannot be promoted above weak-lead status",
            )


def validate_operator_clearance(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    if checklist_value(checklist, "operator_corporate_claims_not_treated_as_clearance") is not True:
        add_error(
            errors,
            "operator_claim_treated_as_official_clearance",
            f"{path}: operator/corporate clearance checklist failed",
        )

    items = evidence_items(packet)
    positive_items = [item for item in items if item.get("is_positive_evidence") is True]
    operator_positive = [
        item for item in positive_items if item.get("source_curation_class") in OPERATOR_CLASSES
    ]
    official_or_professional_positive = [
        item for item in positive_items if item.get("source_curation_class") in OFFICIAL_OR_PROFESSIONAL_CLASSES
    ]
    if not operator_positive or official_or_professional_positive:
        return

    clearance_claim_text = claim_text(packet)
    for phrase in sorted(OFFICIAL_CLEARANCE_CLAIM_PHRASES):
        if contains_phrase(clearance_claim_text, phrase):
            add_error(
                errors,
                "operator_claim_treated_as_official_clearance",
                f"{path}: operator/corporate claim is presented as official clearance via {phrase!r}",
            )


def validate_missing_evidence_boundary(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    result = packet.get("packet_result")
    result_status = result.get("status") if isinstance(result, dict) else None
    no_evidence = (
        packet.get("evidence_strength") == "not_found_after_reasonable_search"
        or result_status in NO_EVIDENCE_STATUSES
    )
    if not no_evidence:
        return

    if checklist_value(checklist, "missing_evidence_not_converted_to_conclusion") is not True:
        add_error(errors, "missing_evidence_overclaim", f"{path}: missing-evidence checklist failed")

    boundary_text = claim_text(packet)
    for phrase in sorted(FORBIDDEN_MISSING_EVIDENCE_PHRASES):
        if contains_phrase(boundary_text, phrase):
            add_error(
                errors,
                "missing_evidence_overclaim",
                f"{path}: missing evidence converted into forbidden conclusion {phrase!r}",
            )
    for word in sorted(FORBIDDEN_MISSING_EVIDENCE_STATUS_WORDS):
        if contains_phrase(boundary_text, word):
            add_error(
                errors,
                "missing_evidence_overclaim",
                f"{path}: missing evidence converted into final status/conclusion {word!r}",
            )


def validate_tag_preservation(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    items = evidence_items(packet)
    evidence_text = text_blob(items)
    has_red_or_yellow_tag = contains_phrase(evidence_text, "red tag") or contains_phrase(evidence_text, "yellow tag")
    if not has_red_or_yellow_tag:
        return

    if checklist_value(checklist, "red_yellow_tag_evidence_preserved") is not True:
        add_error(errors, "red_yellow_tag_not_preserved", f"{path}: red/yellow tag checklist failed")

    result_and_boundary = claim_text(packet)
    if not (contains_phrase(result_and_boundary, "tag") or contains_phrase(result_and_boundary, "tag status")):
        add_error(errors, "red_yellow_tag_not_preserved", f"{path}: tag evidence is absent from final audit text")


def validate_unresolved_exceptions(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    status = packet.get("packet_result", {}).get("status") if isinstance(packet.get("packet_result"), dict) else None
    should_preserve = status in {"positive_evidence_found", "weak_lead_only"} or bool(packet.get("manual_request_targets"))
    if not should_preserve:
        return

    if checklist_value(checklist, "unresolved_exceptions_preserved") is not True:
        add_error(errors, "unresolved_exceptions_erased", f"{path}: unresolved-exception checklist failed")

    exceptions = packet.get("unresolved_exceptions")
    if not isinstance(exceptions, list) or not exceptions:
        add_error(errors, "unresolved_exceptions_erased", f"{path}.unresolved_exceptions: expected preserved exceptions")


def validate_query_log(packet: dict, checklist: dict, path: str, errors: list[tuple[str, str]]) -> None:
    result = packet.get("packet_result")
    result_status = result.get("status") if isinstance(result, dict) else None
    no_evidence = (
        packet.get("evidence_strength") == "not_found_after_reasonable_search"
        or result_status in NO_EVIDENCE_STATUSES
    )
    if not no_evidence:
        return

    if checklist_value(checklist, "query_log_present_for_no_evidence") is not True:
        add_error(errors, "query_log_missing_for_no_evidence", f"{path}: query-log checklist failed")

    query_log = packet.get("query_log")
    if not isinstance(query_log, list) or not query_log:
        add_error(errors, "query_log_missing_for_no_evidence", f"{path}.query_log: no-evidence outcomes need query log")


def validate_packet(packet: dict, checklist: dict, path: str) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []
    validate_exact_building(packet, checklist, path, errors)
    validate_scope(packet, path, errors)
    validate_positive_claim_sources(packet, checklist, path, errors)
    validate_weak_lead_separation(packet, checklist, path, errors)
    validate_operator_clearance(packet, checklist, path, errors)
    validate_missing_evidence_boundary(packet, checklist, path, errors)
    validate_tag_preservation(packet, checklist, path, errors)
    validate_unresolved_exceptions(packet, checklist, path, errors)
    validate_query_log(packet, checklist, path, errors)
    return errors


def validate_parent_audit_run(run: dict, checklist: dict, path: str) -> list[tuple[str, str]]:
    errors: list[tuple[str, str]] = []

    building = run.get("confirmed_building")
    if not isinstance(building, dict) or building.get("gate_1_status") != "confirmed_by_user":
        add_error(errors, "exact_building_match_not_confirmed", f"{path}: parent run must have confirmed building")
    if checklist.get("exact_building_match_confirmed") is not True:
        add_error(errors, "exact_building_match_not_confirmed", f"{path}: parent checklist did not confirm exact match")

    selected = run.get("selected_earthquake_lanes")
    if not isinstance(selected, list) or not selected:
        add_error(errors, "invalid_locked_scope", f"{path}: parent run must select one or more lanes")
        selected = []
    invalid = sorted(set(selected) - ALLOWED_LANES)
    if invalid:
        add_error(errors, "invalid_locked_scope", f"{path}: unsupported parent lanes {invalid}")

    packets = run.get("lane_packets")
    if not isinstance(packets, list) or not packets:
        add_error(errors, "parent_lane_packet_missing", f"{path}: parent run must include lane packet summaries")
        packets = []
    packet_lanes = [packet.get("lane_id") for packet in packets if isinstance(packet, dict)]
    if sorted(packet_lanes) != sorted(selected):
        add_error(errors, "parent_lane_packet_missing", f"{path}: lane packet summaries must match selected lanes")

    if checklist.get("each_lane_packet_audited") is not True:
        add_error(errors, "parent_lane_packet_missing", f"{path}: each lane packet audit checklist failed")
    if checklist.get("parent_summary_audited") is not True:
        add_error(errors, "parent_summary_overclaim", f"{path}: parent summary audit checklist failed")
    if checklist.get("unresolved_exceptions_preserved") is not True:
        add_error(errors, "unresolved_exceptions_erased", f"{path}: parent unresolved-exception checklist failed")

    overall = run.get("overall_summary")
    summary_text = ""
    if not isinstance(overall, dict):
        add_error(errors, "parent_summary_overclaim", f"{path}: missing parent overall_summary")
    else:
        summary_text = str(overall.get("source_bounded_summary", ""))
        if not summary_text.strip():
            add_error(errors, "parent_summary_overclaim", f"{path}: parent source_bounded_summary is required")

    missing_evidence_result = any(
        isinstance(packet, dict)
        and packet.get("packet_result_status") in {"no_public_evidence_found", "no_public_answer_found"}
        for packet in packets
    )
    if missing_evidence_result:
        if checklist.get("missing_evidence_not_converted_to_conclusion") is not True:
            add_error(errors, "missing_evidence_overclaim", f"{path}: parent missing-evidence checklist failed")
        for phrase in sorted(FORBIDDEN_MISSING_EVIDENCE_PHRASES):
            if contains_phrase(summary_text, phrase):
                add_error(
                    errors,
                    "missing_evidence_overclaim",
                    f"{path}: parent summary converts missing evidence into {phrase!r}",
                )
        for word in sorted(FORBIDDEN_MISSING_EVIDENCE_STATUS_WORDS):
            if contains_phrase(summary_text, word):
                add_error(
                    errors,
                    "missing_evidence_overclaim",
                    f"{path}: parent summary converts missing evidence into {word!r}",
                )

    final = run.get("final_overclaim_status")
    if not isinstance(final, dict):
        add_error(errors, "parent_summary_overclaim", f"{path}: missing final_overclaim_status")
    elif final.get("status") == "passed" and overall and overall.get("status") != "ready_for_operator_use":
        add_error(errors, "parent_summary_overclaim", f"{path}: passed parent audit must be ready for operator use")

    return errors


def validate_parent_fixture_shape(
    fixture: object,
    path: str,
    errors: list[tuple[str, str]],
) -> tuple[dict, dict, dict] | None:
    if not isinstance(fixture, dict):
        add_error(errors, "fixture_shape", f"{path}: fixture must be an object")
        return None
    expected_valid = fixture.get("expected_valid")
    if not isinstance(expected_valid, bool):
        add_error(errors, "fixture_shape", f"{path}.expected_valid: must be boolean")
    expected_codes = fixture.get("expected_error_codes")
    if not isinstance(expected_codes, list) or not all(isinstance(code, str) for code in expected_codes):
        add_error(errors, "fixture_shape", f"{path}.expected_error_codes: must be an array of strings")
    checklist = fixture.get("gate4_checklist")
    if not isinstance(checklist, dict):
        add_error(errors, "fixture_shape", f"{path}.gate4_checklist: must be an object")
        checklist = {}
    missing_keys = sorted(PARENT_CHECKLIST_KEYS - set(checklist))
    if missing_keys:
        add_error(errors, "fixture_shape", f"{path}.gate4_checklist: missing parent keys {missing_keys}")
    audit_run = fixture.get("audit_run")
    if not isinstance(audit_run, dict):
        add_error(errors, "fixture_shape", f"{path}.audit_run: must be an object")
        audit_run = {}
    return fixture, checklist, audit_run


def validate_expected_result(
    fixture: dict,
    actual_errors: list[tuple[str, str]],
    path: str,
    harness_errors: list[str],
) -> None:
    expected_valid = fixture.get("expected_valid")
    expected_codes = set(fixture.get("expected_error_codes", []))
    actual_codes = {code for code, _ in actual_errors}

    if not isinstance(expected_valid, bool):
        detail = "; ".join(f"{code}: {message}" for code, message in actual_errors) or "no shape error recorded"
        harness_errors.append(f"{path}: expected_valid must be boolean; actual validation detail: {detail}")
        return

    if expected_valid is True:
        if actual_errors:
            detail = "; ".join(f"{code}: {message}" for code, message in actual_errors)
            harness_errors.append(f"{path}: expected valid but failed with {detail}")
        if expected_codes:
            harness_errors.append(f"{path}: valid fixtures must not declare expected_error_codes")
        return

    if expected_valid is False:
        if not actual_errors:
            harness_errors.append(f"{path}: expected invalid but validator accepted it")
            return
        missing_codes = sorted(expected_codes - actual_codes)
        unexpected_codes = sorted(actual_codes - expected_codes)
        if missing_codes:
            detail = "; ".join(f"{code}: {message}" for code, message in actual_errors)
            harness_errors.append(
                f"{path}: expected invalid reason codes {missing_codes} were not produced; actual {detail}"
            )
        if unexpected_codes:
            detail = "; ".join(f"{code}: {message}" for code, message in actual_errors)
            harness_errors.append(
                f"{path}: produced unexpected invalid reason codes {unexpected_codes}; actual {detail}"
            )


def main() -> int:
    harness_errors: list[str] = []

    fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixture_paths:
        return fail(f"{FIXTURE_DIR.relative_to(ROOT)}: must contain overclaim JSON fixtures")

    expected_fixture_names = {
        "valid-no-public-evidence-nscp.json",
        "valid-corporate-weak-lead.json",
        "valid-red-yellow-tag-preserved.json",
        "valid-official-clearance-found.json",
        "invalid-missing-evidence-safe-conclusion.json",
        "invalid-corporate-treated-official-clearance.json",
        "invalid-unresolved-exceptions-erased.json",
        "invalid-broad-v1-scope.json",
        "invalid-positive-without-sourced-evidence.json",
        "invalid-process-context-positive-evidence.json",
        "valid-parent-audit-run.json",
        "invalid-parent-summary-overclaim.json",
    }
    fixture_names = {path.name for path in fixture_paths}
    missing = sorted(expected_fixture_names - fixture_names)
    if missing:
        harness_errors.append(f"{FIXTURE_DIR.relative_to(ROOT)}: missing fixtures {missing}")

    expected_invalid_count = 0
    expected_valid_count = 0

    for fixture_path in fixture_paths:
        path = fixture_path.relative_to(ROOT).as_posix()
        try:
            fixture = read_json(fixture_path)
        except json.JSONDecodeError as exc:
            harness_errors.append(f"{path}: invalid JSON: {exc}")
            continue

        shape_errors: list[tuple[str, str]] = []
        if isinstance(fixture, dict) and "audit_run" in fixture:
            shaped_parent = validate_parent_fixture_shape(fixture, path, shape_errors)
            if shaped_parent is None:
                harness_errors.extend(f"{path}: {code}: {message}" for code, message in shape_errors)
                continue
            fixture_obj, checklist, audit_run = shaped_parent
            actual_errors = shape_errors + validate_parent_audit_run(audit_run, checklist, path)
        else:
            shaped = validate_fixture_shape(fixture, path, shape_errors)
            if shaped is None:
                harness_errors.extend(f"{path}: {code}: {message}" for code, message in shape_errors)
                continue
            fixture_obj, checklist, packet = shaped
            actual_errors = shape_errors + validate_packet(packet, checklist, path)

        if fixture_obj.get("expected_valid") is True:
            expected_valid_count += 1
        elif fixture_obj.get("expected_valid") is False:
            expected_invalid_count += 1

        validate_expected_result(fixture_obj, actual_errors, path, harness_errors)

    if expected_valid_count < 1:
        harness_errors.append("overclaim fixtures: must include at least one expected-valid fixture")
    if expected_invalid_count < 4:
        harness_errors.append("overclaim fixtures: must include at least four expected-invalid fixtures")

    if harness_errors:
        return fail("\n- " + "\n- ".join(harness_errors))

    print(
        "validated V2 Gate 4 overclaim audit: "
        f"{expected_valid_count} expected-valid fixtures, {expected_invalid_count} expected-invalid fixtures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
