---
name: philippines-building-code-evidence-auditor
description: Use for Philippine buildings, malls, hotels, establishments, towers, tenants, complexes, or facilities when the user wants earthquake-related public evidence: exact place lock, NSCP or seismic design evidence, OBO structural permit or plan-review evidence, post-earthquake tag or inspection status, or clearance after damage/tag/closure. Refuse or pause when the exact place is not confirmed, the user wants legal or engineering certification, or the answer would require non-public OBO, owner, operator, or professional records without a manual-request path.
---

# Philippines Building Code Evidence Auditor

Use this skill to run Gates 1-4 of the Philippine earthquake building-code
evidence auditor. The workflow is an evidence auditor, not a safety certifier.
It prepares structured public-evidence packets and manual request paths.

## Trigger

Use this skill when the user asks about a Philippine building, mall, hotel,
establishment, branch, tenant, tower, complex, or facility and wants any of:

- earthquake-related building-code evidence;
- NSCP or seismic design evidence;
- OBO structural permit, civil/structural permit, or plan-review evidence;
- post-earthquake green/yellow/red tag, inspection, closure, or restriction;
- clearance, reoccupancy, repair acceptance, retrofit acceptance, or structural
  stability evidence after damage or tagging.

## Refuse Or Pause When

Pause and ask one focused question when:

- Gate 1 has not confirmed the exact place;
- the target may be a tenant, wing, tower, whole complex, or different branch;
- the Gate 2 audit question is unclear;
- lanes 3 or 4 need a specific earthquake event, tag, damage, closure,
  restriction, or timeframe.

Refuse or reframe when the user asks the agent to certify legal compliance,
engineering safety, current fitness for occupancy, or "earthquake-proof" status.
Offer an evidence-only packet or manual request path instead.

## Gate 1 Place Lock

Objective: confirm the exact Philippine place before any evidence search.

Input: user clue, exact user words, city/province/address, link, photo,
receipt, booking page, landmark, or known alias.

Output: `building_identity_confirmation` packet using
`data/building-code-auditor/building-identity-schema.json`.

Rules:

- Check identity only: name, branch, address, city, link, landmark, and
  tenant/building or complex/building relationship.
- Use at most three search queries or three source checks before asking.
- Show the best match or up to three options only when ambiguity is real.
- Ask exactly one missing detail when blocked.
- `confirmation.can_proceed_to_audit` is true only when
  `confirmation.status` is `confirmed_by_user`.
- Do not search permits, incidents, contractors, compliance, safety, hazards, or
  earthquake evidence in Gate 1.

## Gate 2 Earthquake Audit Scope Lock

Objective: lock exactly which earthquake audit question Gate 3 should run.

Input: confirmed Gate 1 place packet and the user's scope answer.

Output: `audit_scope_lock` packet using
`data/building-code-auditor/audit-scope-schema.json`.

Ask this menu:

1. NSCP / seismic design evidence.
2. OBO structural permit or plan-review evidence.
3. Latest post-earthquake official tag or inspection status.
4. Latest clearance after damage, tag, closure, or restriction.
5. All four questions.

Rules:

- Ask exactly one menu question when no scope is locked.
- Accept answers by number, label, `all`, or natural language.
- If unclear, ask exactly one scope detail and keep evidence search blocked.
- `can_proceed_to_evidence_search` is true only after explicit scope lock.
- Gate 2 does not search sources or produce evidence findings.

## Gate 3 Evidence Packet Loop

Objective: produce a structured evidence packet for the selected Gate 2 lane or
lanes. Gate 3 is the first gate where evidence collection may happen.

Input:

- confirmed Gate 1 place;
- locked Gate 2 scope;
- `target_subscope`;
- `timeframe` and `earthquake_event` when relevant;
- answerability matrix in
  `data/building-code-auditor/earthquake-safety-answerability-matrix.json`;
- NSCP evidence map in
  `data/building-code-auditor/nscp-compliance-evidence-map.json`.

Per-lane loop:

1. Search exact target documents for the selected lane.
2. Analyze whether an answer was found.
3. If an answer was found, record the answer and source limits.
4. If no answer was found, continue only while a useful public source type
   remains.
5. If no useful public source remains, branch by lane type.
6. Lanes 1-2 (`availability_only`) record the answer as no public
   target-specific evidence found.
7. Lanes 3-4 (`availability_and_answer`) record no public answer found and add
   manual follow-up.

Output: `earthquake_evidence_packet` JSON that passes
`scripts/validate_building_code_packet.py`.

## Gate 4 Regression Test Gate

Objective: prove the evidence packet is valid before it is treated as complete.

Gate 4 checks:

- packet schema and required fields;
- source URL shape;
- answerability values;
- lane-specific manual follow-up;
- unsafe claim blocking;
- skill surface consistency;
- existing Gate 1 and Gate 2 validators.

Run:

```bash
python3 scripts/validate_building_code_gate_suite.py
```

Gate 5 or live search work may begin only after Gate 4 passes.

## Source And Claim Boundaries

Missing public evidence never means unsafe, noncompliant, unpermitted, no
permit, or no incident.

Do not claim:

- earthquake-proof;
- NSCP compliant or noncompliant;
- structurally safe or unsafe;
- fit for occupancy;
- no permit or unpermitted;
- legal compliance.

Allowed language:

- public evidence was found;
- no public target-specific evidence was found;
- no public official answer was found;
- manual OBO/OCBO/LGU/owner/operator/professional follow-up is needed;
- this does not certify earthquake safety or NSCP compliance.

## Validation Commands

Run before handoff:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
python3 scripts/validate_building_code_gate_suite.py
python3 scripts/validate_progress_docs.py
git diff --check
```
