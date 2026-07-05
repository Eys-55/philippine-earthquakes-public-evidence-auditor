# Building Code Evidence Auditor Progress Lock

Date: 2026-07-04

## Locked Direction

Build an ECC-aligned agentic workflow for Philippine earthquake-related
building-code evidence auditing.

Working name:

**Philippines Building Code Evidence Auditor**

The earlier disaster-risk assessor remains paused foundation context. It is not
the active current build.

## Current Product Boundary

The active build covers Gates 1-4 only:

1. Gate 1 locks the exact building/place identity.
2. Gate 2 locks one earthquake audit question from the four-question menu.
3. Gate 3 creates a structured evidence packet from selected evidence lanes.
4. Gate 4 runs deterministic regression checks before handoff.

Live web search, cron monitoring, and `.mjs` orchestration are deferred until
Gates 1-4 pass the deterministic Python harness. This prevents automating
unvalidated packet shapes or unsafe building-safety claims.

## Four Earthquake Questions

Gate 2 asks which question the user wants:

1. NSCP / seismic design evidence.
2. OBO structural permit or plan-review evidence.
3. Latest post-earthquake official tag or inspection status.
4. Latest clearance after damage, tag, closure, or restriction.

Questions 1 and 2 are availability-only lanes. If no useful public source
remains, the packet may answer that no public target-specific evidence was
found.

Questions 3 and 4 are availability-and-answer lanes. If no useful public source
remains, the packet must say no public official answer was found and list a
manual request path.

## Non-Negotiable Boundary

The product is an evidence auditor, not a compliance certifier.

It must not claim:

- the building is legally compliant;
- the building is structurally safe or unsafe;
- the building is earthquake-proof;
- the building is fit for occupancy;
- a missing public record proves noncompliance, no permit, or no incident.

It may say:

- public evidence was found;
- public evidence was partial;
- no public target-specific evidence was found;
- no public official answer was found;
- public sources conflict;
- manual OBO, OCBO, LGU, owner, operator, or professional follow-up is needed;
- the issue is not assessable from public web evidence.

## Implemented Artifacts

- Gate 1 schema and validator:
  `data/building-code-auditor/building-identity-schema.json`,
  `scripts/validate_building_identity_gate.py`.
- Gate 2 schema, fixtures, source-reality matrix, and validators:
  `data/building-code-auditor/audit-scope-schema.json`,
  `data/building-code-auditor/audit-scope-test-cases.json`,
  `data/building-code-auditor/audit-scope-source-reality.json`,
  `scripts/validate_audit_scope_gate.py`,
  `scripts/validate_audit_scope_source_reality.py`.
- Gate 3 packet schema, sample packets, validator, renderer, and sample report:
  `data/building-code-auditor/evidence-packet-schema.json`,
  `data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json`,
  `data/building-code-auditor/samples/evidence-packet-q2-confirmed-obo-review.json`,
  `data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json`,
  `data/building-code-auditor/samples/evidence-packet-q4-clearance-found.json`,
  `scripts/validate_building_code_packet.py`,
  `scripts/render_building_code_packet.py`,
  `reports/sample-building-code-earthquake-evidence-packet.md`.
- Gate 4 regression cases and suite:
  `data/building-code-auditor/gate-4-regression-cases.json`,
  `data/building-code-auditor/samples/evidence-packet-invalid-overclaim.json`,
  `data/building-code-auditor/samples/evidence-packet-invalid-source-url.json`,
  `scripts/validate_building_code_gate_suite.py`.
- Reusable skill surface:
  `skills/philippines-building-code-evidence-auditor/SKILL.md`,
  `skills/philippines-building-code-evidence-auditor/agents/openai.yaml`.

## Validation

Run before handoff:

```bash
python3 -m json.tool data/building-code-auditor/building-identity-schema.json >/tmp/building-identity-schema.json
python3 -m json.tool data/building-code-auditor/audit-scope-schema.json >/tmp/audit-scope-schema.json
python3 -m json.tool data/building-code-auditor/audit-scope-test-cases.json >/tmp/audit-scope-test-cases.json
python3 -m json.tool data/building-code-auditor/audit-scope-source-reality.json >/tmp/audit-scope-source-reality.json
python3 -m json.tool data/building-code-auditor/evidence-packet-schema.json >/tmp/evidence-packet-schema.json
python3 -m json.tool data/building-code-auditor/gate-4-regression-cases.json >/tmp/gate-4-regression-cases.json
python3 scripts/validate_building_code_gate_suite.py
python3 scripts/validate_progress_docs.py
git diff --check
```

Expected suite signal:

```text
building code gate suite: PASS
```

## Resume Prompt

If work resumes from this note, start with a live Gate 3 run using a
Gate-1-confirmed place and a Gate-2-locked earthquake question. Do not add cron,
monitoring, or live-search automation until the packet from that run passes
`scripts/validate_building_code_gate_suite.py`.
