#!/usr/bin/env python3
"""Run the full Gates 1-4 regression suite for the building-code auditor."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

REGRESSION_CASES = ROOT / "data/building-code-auditor/gate-4-regression-cases.json"
SKILL_PATH = ROOT / "skills/philippines-building-code-evidence-auditor/SKILL.md"

REQUIRED_CASE_CATEGORIES = {
    "gate_1_confirmed_place",
    "gate_2_scope_lock",
    "gate_3_availability_only_no_public_evidence",
    "gate_3_availability_and_answer_no_public_answer",
    "gate_3_confirmed_public_evidence",
    "gate_3_manual_follow_up",
    "unsafe_claim_blocked",
    "invalid_source_url_blocked",
}

REQUIRED_SKILL_PHRASES = (
    "Gate 1 Place Lock",
    "Gate 2 Earthquake Audit Scope Lock",
    "Gate 3 Evidence Packet Loop",
    "Gate 4 Regression Test Gate",
    "Missing public evidence never",
    "Validation Commands",
)

DISALLOWED_ACTIVE_SKILL_PHRASES = (
    "Permit or occupancy records - usually",
    "Broad public-evidence packet - combines",
)

VALID_PACKET_FIXTURES = (
    "data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json",
    "data/building-code-auditor/samples/evidence-packet-q2-confirmed-obo-review.json",
    "data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json",
    "data/building-code-auditor/samples/evidence-packet-q4-clearance-found.json",
)

INVALID_PACKET_FIXTURES = (
    "data/building-code-auditor/samples/evidence-packet-invalid-overclaim.json",
    "data/building-code-auditor/samples/evidence-packet-invalid-source-url.json",
)


def suite_fail(message: str) -> int:
    print(f"building code gate suite: FAIL: {message}", file=sys.stderr)
    return 1


def run_command(args: list[str], *, expect_success: bool = True) -> str | None:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    output = "\n".join(part for part in (proc.stdout.strip(), proc.stderr.strip()) if part)
    if expect_success and proc.returncode != 0:
        return f"{' '.join(args)} failed with exit {proc.returncode}\n{output}"
    if not expect_success and proc.returncode == 0:
        return f"{' '.join(args)} was expected to fail but passed\n{output}"
    return None


def validate_regression_cases() -> str | None:
    try:
        data = json.loads(REGRESSION_CASES.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return f"missing {REGRESSION_CASES.relative_to(ROOT)}"
    except json.JSONDecodeError as exc:
        return f"invalid JSON in {REGRESSION_CASES.relative_to(ROOT)}: {exc}"

    if data.get("schema_version") != "1.0.0":
        return "gate-4 regression cases schema_version must be 1.0.0"
    if data.get("workflow_step") != "gate_4_regression_cases":
        return "gate-4 regression cases workflow_step must be gate_4_regression_cases"

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return "gate-4 regression cases must include a non-empty cases array"

    categories = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            return f"cases[{index}] must be an object"
        for key in ("case_id", "category", "description", "input_packet_path", "expected_result", "expected_checks"):
            if key not in case:
                return f"cases[{index}] missing {key}"
        categories.add(case["category"])
        if case["expected_result"] not in {"pass", "fail"}:
            return f"cases[{index}].expected_result must be pass or fail"
        if not isinstance(case["expected_checks"], list) or not case["expected_checks"]:
            return f"cases[{index}].expected_checks must be non-empty"
        packet_path = ROOT / case["input_packet_path"]
        if not packet_path.exists():
            return f"cases[{index}].input_packet_path does not exist: {case['input_packet_path']}"

    if categories != REQUIRED_CASE_CATEGORIES:
        return f"gate-4 categories must be exactly {sorted(REQUIRED_CASE_CATEGORIES)!r}; got {sorted(categories)!r}"
    return None


def validate_skill_surface() -> str | None:
    try:
        skill = SKILL_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"missing {SKILL_PATH.relative_to(ROOT)}"

    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill:
            return f"skill is missing required phrase {phrase!r}"
    for phrase in DISALLOWED_ACTIVE_SKILL_PHRASES:
        if phrase in skill:
            return f"skill appears to contain old active Gate 2 behavior: {phrase!r}"
    return None


def main() -> int:
    checks: list[str | None] = [
        validate_regression_cases(),
        validate_skill_surface(),
        run_command([PYTHON, "scripts/validate_building_identity_gate.py"]),
        run_command([PYTHON, "scripts/validate_audit_scope_gate.py"]),
        run_command([PYTHON, "scripts/validate_audit_scope_source_reality.py"]),
    ]

    for fixture in VALID_PACKET_FIXTURES:
        checks.append(run_command([PYTHON, "scripts/validate_building_code_packet.py", fixture]))

    checks.append(run_command([PYTHON, "scripts/validate_progress_docs.py"]))

    for fixture in INVALID_PACKET_FIXTURES:
        checks.append(run_command([PYTHON, "scripts/validate_building_code_packet.py", fixture], expect_success=False))

    for error in checks:
        if error is not None:
            return suite_fail(error)

    print("building code gate suite: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
