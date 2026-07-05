# Philippines Building Code Evidence Auditor V2 Lock

Date: 2026-07-05

## Status

V2 was created by copying V1 first, then editing the V2 copy into a separate
four-lane earthquake public-evidence workflow. V1 remains untouched and keeps
its own skill, data path, fixtures, and validators.

## Paths

- V1 skill: `skills/philippines-building-code-evidence-auditor/SKILL.md`
- V1 data: `data/building-code-auditor/`
- V2 skill: `skills/philippines-building-code-evidence-auditor-v2/SKILL.md`
- V2 data: `data/philippines-building-code-evidence-auditor-v2/`
- V2 plan:
  `docs/plans/2026-07-05-philippines-building-code-evidence-auditor-v2-implementation-plan.md`

## Permanent V2 Scope

V2 searches only these four earthquake evidence lanes:

1. NSCP / seismic design evidence
2. OBO structural permit or review evidence
3. Latest post-earthquake tag / status
4. Latest clearance after damage or tag

Gate 3 evidence packet is the output format for these four lanes. It is not a
fifth scope, broad packet lane, or general building-code search.

## Gate Shape

- Gate 1: confirm the exact building, establishment, mall, hotel, tenant,
  complex, or facility before any earthquake evidence search.
- Gate 2: default to all four earthquake evidence lanes unless the user narrows
  to one or more lanes.
- Gate 3: produce a parent audit run with child lane packets, document inventory, evidence
  strength, source curation class, physical-condition public evidence,
  unresolved exceptions, manual request targets, overclaim boundary, query log,
  and packet result.
- Gate 4: audit the packet for source URLs, exact target match, weak-lead
  separation, unresolved exceptions, red/yellow tag preservation, and
  no-overclaim language.

## Validators

V2 uses separate validators from V1:

- `scripts/validate_building_code_v2_identity_gate.py`
- `scripts/validate_building_code_v2_earthquake_scope_gate.py`
- `scripts/validate_building_code_v2_evidence_packet.py`
- `scripts/validate_building_code_v2_overclaim.py`

V1 validators remain separate:

- `scripts/validate_building_identity_gate.py`
- `scripts/validate_audit_scope_gate.py`
- `scripts/validate_audit_scope_source_reality.py`

## No-Overclaim Boundary

V2 must not turn missing public evidence into a conclusion that a building is
safe, unsafe, compliant, noncompliant, cleared, tagged, untagged, open, closed,
reviewed, unreviewed, permitted, or unpermitted.

Positive claims need source URLs. Official or professional records must stay
separate from operator, corporate, news, or weak-lead evidence.

## No-Evidence Semantics

For the first two lanes, a reasonable search with no findings means:

- no public evidence found for NSCP / seismic design evidence;
- no public evidence found for OBO structural permit or review evidence.

For the last two lanes, a reasonable search with no findings means:

- no public answer found for latest post-earthquake tag / status;
- no public answer found for latest clearance after damage or tag.

These are valid packet outcomes when the query log shows the search effort and
unresolved exceptions are preserved.
