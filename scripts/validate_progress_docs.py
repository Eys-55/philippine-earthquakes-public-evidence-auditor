#!/usr/bin/env python3
"""Validate the two canonical building-code progress Markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHART_PATH = ROOT / "docs/plans/building-code-progress-chart.md"
TABLE_PATH = ROOT / "docs/plans/building-code-progress-table.md"
VIEW_PATH = ROOT / "reports/building-code-progress-view.html"
SVG_PATH = ROOT / "reports/assets/building-code-progress-chart.svg"

REQUIRED_TABLE_PHRASES = (
    "1. Place lock | Implemented",
    "1a. Place-lock tests | Done",
    "1b. Place-lock samples | Done",
    "1c. Real-place run | Done",
    "2. Audit scope lock | Implemented",
    "3. Evidence packet | Implemented",
    "4. Regression test gate | Implemented",
    "9. Broader scanning | Deferred",
    "data/building-code-auditor/audit-scope-schema.json",
    "data/building-code-auditor/audit-scope-source-reality.json",
    "data/building-code-auditor/evidence-packet-schema.json",
    "data/building-code-auditor/gate-4-regression-cases.json",
    "scripts/validate_building_code_packet.py",
    "scripts/validate_building_code_gate_suite.py",
    "scripts/validate_audit_scope_source_reality.py",
)

DISALLOWED_CHART_PATTERNS = {
    "stateDiagram": "state diagrams are fragile in the Codex rich viewer",
    "flowchart": "use graph TD/LR for the most compatible Mermaid profile",
    "classDef": "style classes can make the viewer fall back to plaintext",
    "class ": "style classes can make the viewer fall back to plaintext",
    "%%{": "Mermaid init directives can make the viewer fall back to plaintext",
    "![](": "the chart file must stay Mermaid source, not an embedded image",
}

REQUIRED_CHART_PHRASES = (
    "Phase 1 Place Lock",
    "Ready for real<br/>place clue",
    "User gives<br/>place clue",
    "Record exact<br/>user words",
    "Check name<br/>place clues",
    "Exact place<br/>identified?",
    "Ask one<br/>missing detail",
    "Show best match<br/>or options",
    "User confirms<br/>exact place?",
    "Lock place<br/>identity",
    "Phase 2 Audit Scope Lock",
    "Show audit<br/>scope menu",
    "User chooses<br/>scope",
    "Record exact<br/>answer",
    "Scope clear<br/>enough?",
    "Ask one<br/>scope detail",
    "Lock audit<br/>scope",
)

DISALLOWED_CHART_PHRASES = (
    "Test fixtures",
    "Sample packets",
    "Skill instructions",
    "workflow direction",
    "source landscape",
    "Gate one place",
    "Run identity",
    "Test cases",
    "Regression tests",
    "Move to<br/>intent gate",
    "Phase 2 Intent Lock",
    "User states<br/>audit intent",
    "Intent scope<br/>confirmed?",
    "Lock intent<br/>scope",
)

NODE_LABEL_PATTERN = re.compile(
    r'^[A-Z][A-Z0-9_]*\["(.*?)"\]$|'
    r'^[A-Z][A-Z0-9_]*\{"(.*?)"\}$|'
    r'^[A-Z][A-Z0-9_]*\[(.*?)\]$|'
    r'^[A-Z][A-Z0-9_]*\{(.*?)\}$|'
    r'^subgraph [A-Z][A-Z0-9_]*\["(.*?)"\]$|'
    r'^subgraph [A-Z][A-Z0-9_]*\[(.*?)\]$'
)
MAX_NODE_LABEL_LINE_LENGTH = 24


def fail(message: str) -> int:
    print(f"progress-doc validation failed: {message}", file=sys.stderr)
    return 1


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def mermaid_blocks(markdown: str) -> list[str]:
    pattern = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)
    return pattern.findall(markdown)


def validate_chart() -> int:
    try:
        markdown = read(CHART_PATH)
    except FileNotFoundError:
        return fail(f"missing {CHART_PATH.relative_to(ROOT)}")

    blocks = mermaid_blocks(markdown)
    if len(blocks) != 1:
        return fail("chart file must contain exactly one ```mermaid block")

    outside = re.sub(r"```mermaid\n.*?\n```", "", markdown, flags=re.DOTALL).strip()
    if outside:
        return fail("chart file must contain only the Mermaid block")

    diagram = blocks[0]
    first_line = next((line.strip() for line in diagram.splitlines() if line.strip()), "")
    if first_line not in {"graph TD", "graph LR"}:
        return fail("chart Mermaid must start with graph TD or graph LR")

    for pattern, reason in DISALLOWED_CHART_PATTERNS.items():
        if pattern in diagram:
            return fail(f"chart contains {pattern!r}: {reason}")

    for phrase in REQUIRED_CHART_PHRASES:
        if phrase not in diagram:
            return fail(f"chart must preserve human-flow label: missing {phrase!r}")

    for phrase in DISALLOWED_CHART_PHRASES:
        if phrase in diagram:
            return fail(f"chart must not use artifact-progress label {phrase!r}")

    for raw_line in diagram.splitlines():
        line = raw_line.strip()
        match = NODE_LABEL_PATTERN.match(line)
        if not match:
            continue
        label = next(group for group in match.groups() if group is not None)
        for label_line in label.split("<br/>"):
            if len(label_line) > MAX_NODE_LABEL_LINE_LENGTH:
                return fail(
                    f"chart label line {label_line!r} is too long; keep manual "
                    f"label lines under {MAX_NODE_LABEL_LINE_LENGTH + 1} "
                    "characters to avoid wrapping"
                )

    return 0


def validate_table() -> int:
    try:
        markdown = read(TABLE_PATH)
    except FileNotFoundError:
        return fail(f"missing {TABLE_PATH.relative_to(ROOT)}")

    if "```mermaid" in markdown:
        return fail("table file must not contain Mermaid")
    if "![](" in markdown:
        return fail("table file must not embed images")

    table_lines = [line for line in markdown.splitlines() if line.startswith("|")]
    if len(table_lines) < 3:
        return fail("table file must contain a Markdown table")
    if "Gate" not in table_lines[0] or "Status" not in table_lines[0]:
        return fail("table header must include Gate and Status")

    for phrase in REQUIRED_TABLE_PHRASES:
        if phrase not in markdown:
            return fail(f"table must keep Gates 1-4 status explicit: missing {phrase!r}")

    return 0


def validate_viewer() -> int:
    try:
        html = read(VIEW_PATH)
    except FileNotFoundError:
        return fail(f"missing {VIEW_PATH.relative_to(ROOT)}")

    if not SVG_PATH.exists() or SVG_PATH.stat().st_size == 0:
        return fail(f"missing rendered SVG at {SVG_PATH.relative_to(ROOT)}")

    required = 'src="assets/building-code-progress-chart.svg"'
    if required not in html:
        return fail("HTML viewer must embed the rendered progress SVG")

    for forbidden in ("<h1", "<h2", "<p", "<table", "<thead", "<tbody", "<th", "<td"):
        if forbidden in html:
            return fail(f"HTML viewer must be chart-only; found {forbidden}")

    if "color-scheme: dark" not in html:
        return fail("HTML viewer must default to dark mode")

    return 0


def main() -> int:
    return validate_chart() or validate_table() or validate_viewer()


if __name__ == "__main__":
    raise SystemExit(main())
