#!/usr/bin/env python3
"""Render a validated Gate 3 earthquake evidence packet to Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import validate_building_code_packet


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("packet must be a JSON object")
    return data


def bullet(items: list[str]) -> str:
    if not items:
        return "- None\n"
    return "".join(f"- {item}\n" for item in items)


def render(packet: dict) -> str:
    place = packet["confirmed_place"]["display_name"]
    context = packet["target_context"]
    integrated = packet["integrated_answer"]
    manual = packet["manual_follow_up"]
    boundary = packet["overclaim_boundary"]

    lines: list[str] = [
        f"# Earthquake Evidence Packet: {place}",
        "",
        "## Scope",
        "",
        f"- Target subscope: {context['target_subscope']}",
        f"- Timeframe: {context['timeframe'] or 'Not required for selected scope'}",
        f"- Earthquake event: {context['earthquake_event'] or 'Not required for selected scope'}",
        f"- Jurisdiction: {context['jurisdiction']['lgu']}",
        "",
        "## Citizen-Safe Summary",
        "",
        integrated["citizen_safe_summary"],
        "",
        "## Lane Results",
        "",
    ]

    for lane in packet["lane_results"]:
        lines.extend(
            [
                f"### {lane['lane_id']}",
                "",
                f"- Lane type: {lane['lane_type']}",
                f"- Answerability: {lane['answerability']}",
                f"- Public evidence status: {lane['public_evidence_status']}",
                f"- Stop reason: {lane['stop_reason']}",
                f"- Answer: {lane['answer_text'] or 'No public official answer found.'}",
                "",
            ]
        )

    lines.extend(["## Sources", ""])
    source_count = 0
    for lane in packet["lane_results"]:
        for source in lane["best_sources"]:
            source_count += 1
            lines.extend(
                [
                    f"- [{source['title']}]({source['url']})",
                    f"  - Supports: {source['supports']}",
                    f"  - Does not support: {source['does_not_support']}",
                ]
            )
    if source_count == 0:
        lines.append("- No public source URL supported the target-specific answer.")

    lines.extend(
        [
            "",
            "## Manual Follow-Up",
            "",
            f"- Required: {manual['required']}",
            "",
            "Custodians:",
            bullet(manual["custodians"]).rstrip(),
            "",
            "Documents to request:",
            bullet(manual["documents_to_request"]).rstrip(),
            "",
            "## Overclaim Boundary",
            "",
            f"- Allowed claim: {boundary['allowed_claim']}",
            "",
            "Forbidden claims:",
            bullet(boundary["forbidden_claims"]).rstrip(),
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv[1:])

    packet = read_json(args.packet)
    errors = validate_building_code_packet.validate_root(packet)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    markdown = render(packet)
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
