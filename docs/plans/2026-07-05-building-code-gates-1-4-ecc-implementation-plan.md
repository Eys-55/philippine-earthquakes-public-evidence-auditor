# Building Code Gates 1-4 ECC Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build Gates 1-4 of the Philippines Building Code Evidence Auditor as a reusable ECC skill and Python-first harness that locks place identity, locks the earthquake audit question, validates structured evidence packets, and blocks unsafe claims before any output is treated as complete.

**Architecture:** This is a skill-first, contract-first workflow harness, not a live web-search crawler yet. The reusable workflow surface in `skills/philippines-building-code-evidence-auditor/`, `agents/openai.yaml`, and repo `AGENTS.md` is the primary product surface for future agents; schemas, fixtures, and validators are the deterministic enforcement layer. Gate 1 and Gate 2 produce locked input packets; Gate 3 produces a structured evidence packet from agent/operator findings; Gate 4 validates packet quality, citations, answerability, manual follow-up, and overclaim boundaries.

**Tech Stack:** Python 3 standard library, JSON fixtures and JSON-schema-style documents, Markdown reports, Mermaid charts, existing repo validators, Kroki or `mmdc` for Mermaid validation. No cron, no scheduler, no `.mjs`, no live search runner in this phase.

---

## Execution Discipline

This plan must be implemented with Superpowers and ECC discipline:

- Use `superpowers:using-git-worktrees` before implementation if starting from a shared or dirty branch.
- Use `superpowers:executing-plans` to execute this file in batches, defaulting to three tasks per batch.
- Use ECC contract language for every gate: objective, inputs, outputs, eval, handoff, human boundary, and safety risks.
- Treat the reusable skill and agent metadata as implementation artifacts, not documentation cleanup. Build the skill surface before refactoring the gate schemas so future agents know the contract they are implementing.
- Use eval-driven development: add or update fixtures first, run the validator to see the expected failure, then update implementation.
- Keep live web search out of v1. Gate 3 validates structured evidence gathered by an agent/operator; it does not fetch the web itself.
- Do not commit unless the user explicitly asks for commits during execution.

Definition of done:

- Gate 1 validator still passes.
- Gate 2 validator reflects the four earthquake audit questions, not the old five-scope building-code menu.
- Gate 3 has a final packet schema, valid sample packets, and a deterministic packet validator.
- Gate 4 has a single suite command that runs all gate checks.
- The skill instructions, `agents/openai.yaml`, root `AGENTS.md`, progress table, and chart docs agree with the same Gate 1-4 workflow.
- No validator permits unsupported claims that a building is safe, unsafe, earthquake-proof, NSCP-compliant, noncompliant, fit for occupancy, or unpermitted.

## ECC Gate Map

| Gate | ECC concept | Built artifact | Must not do |
|---|---|---|---|
| Gate 1 Place Lock | Human confirmation boundary and input contract | Confirmed place packet and validator | Search permits, incidents, safety, compliance, or earthquake evidence |
| Gate 2 Audit Scope Lock | Intent/scope contract and handoff | Earthquake question scope packet and validator | Search evidence or preserve old broad five-scope menu |
| Gate 3 Evidence Packet | Dynamic workflow harness output | Structured evidence packet, sample packets, renderer, validator | Certify safety/compliance or keep searching forever |
| Gate 4 Test Gate | Eval gate and regression harness | Full gate suite validator and regression fixtures | Treat unchecked evidence packets as complete |

## Reusable Skill Surface Map

The repo is meant to be handed off and reused, so the skill surface is not a final documentation task. It is the first real product contract that every later schema and validator must follow.

| Surface | Purpose | Required standard |
|---|---|---|
| `AGENTS.md` | Repo-wide operating policy | Names the active lane, states skills-first workflow surface, blocks disaster-risk scope drift, and defines GitHub/repo handoff expectations |
| `skills/philippines-building-code-evidence-auditor/SKILL.md` | Reusable agent workflow | Contains trigger/refusal rules, Gate 1-4 contracts, exact user prompts, source boundaries, and validation commands |
| `skills/philippines-building-code-evidence-auditor/agents/openai.yaml` | Agent UI metadata | Human-readable name, short description, and default prompt match the Gate 1-4 skill |
| `data/building-code-auditor/` | Machine contract | Schemas, fixtures, source-reality matrices, and sample packets enforce the skill |
| `scripts/` | Eval harness | Deterministic validators prove the skill can be rerun reliably |

## Canonical Four Gate 2 Questions

Use these exact menu options everywhere:

1. `nscp_seismic_design_evidence` - NSCP / seismic design evidence.
2. `obo_structural_permit_review` - OBO structural permit or plan-review evidence.
3. `latest_post_earthquake_status` - Latest post-earthquake official tag or inspection status.
4. `latest_clearance_after_tag` - Latest clearance after damage, tag, closure, or restriction.
5. `all` - Run all four lanes.

Lane behavior:

- Lanes 1 and 2 are `availability_only`.
- Lanes 3 and 4 are `availability_and_answer`.
- If no public evidence remains for lanes 1 or 2, the answer is: no public evidence found.
- If no public evidence remains for lanes 3 or 4, the result is: no public answer found; manual follow-up is needed.

## Task 1: Establish Implementation Baseline

**ECC concept:** Discover current state before changing the workflow.

**Files:**
- Read: `docs/plans/gate-1-place-lock-chart.md`
- Read: `docs/plans/gate-2-audit-scope-lock-chart.md`
- Read: `docs/plans/gate-3-evidence-packet-chart.md`
- Read: `docs/plans/gate-4-regression-tests-chart.md`
- Read: `skills/philippines-building-code-evidence-auditor/SKILL.md`
- Read: `data/building-code-auditor/earthquake-safety-answerability-matrix.json`
- Read: `data/building-code-auditor/nscp-compliance-evidence-map.json`

**Step 1: Run current validators**

Run:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
python3 scripts/validate_progress_docs.py
git diff --check
```

Expected:

- Existing validators may pass even though Gate 2 still uses the old five-scope menu.
- Record this as baseline behavior; do not treat the old Gate 2 as final.

**Step 2: Inspect current repo surfaces**

Run:

```bash
find docs/plans data/building-code-auditor skills/philippines-building-code-evidence-auditor scripts -maxdepth 3 -type f | sort
```

Expected:

- Existing Gate 1 and Gate 2 Python validators are present.
- No Gate 3 packet validator exists yet.
- No Gate 4 suite validator exists yet.
- No cron or `.mjs` helper exists.

**Step 3: Commit checkpoint only if requested**

Suggested commit message if the user asks for commits:

```bash
git commit -m "chore: record building-code gate baseline"
```

## Task 1A: Lock The Reusable Skill And Agent Surface First

**ECC concept:** Reusable skill extraction. This is the handoff surface future agents will actually read, so it must be created before the schema/code refactor proceeds.

**Files:**
- Modify: `AGENTS.md`
- Modify: `skills/philippines-building-code-evidence-auditor/SKILL.md`
- Modify: `skills/philippines-building-code-evidence-auditor/agents/openai.yaml`

**Step 1: Update root repo instructions**

In `AGENTS.md`, ensure the active lane says:

```markdown
- `philippines-building-code-evidence-auditor` is the active lane.
- `address-disaster-risk-assessor` is deprecated/paused foundation context for this build.
- Reusable workflow behavior must be captured in `skills/philippines-building-code-evidence-auditor/SKILL.md` before adding scripts, cron, live search, or compatibility shims.
- Gate 1-4 are the current product boundary: place lock, earthquake audit scope lock, evidence packet loop, and regression test gate.
```

Acceptance checks:

- `AGENTS.md` does not describe the disaster-risk assessor as the active current build target.
- `AGENTS.md` says `skills/` is the canonical workflow surface.
- `AGENTS.md` says cron/live search comes after the deterministic harness.

**Step 2: Rewrite `SKILL.md` as the core agent contract**

The skill body must be concise enough for repeated loading and should avoid duplicating long matrices that already live in `data/` or `reports/`.

Required sections, in this order:

```markdown
# Philippines Building Code Evidence Auditor

## Trigger

## Refuse Or Pause When

## Gate 1 Place Lock

## Gate 2 Earthquake Audit Scope Lock

## Gate 3 Evidence Packet Loop

## Gate 4 Regression Test Gate

## Source And Claim Boundaries

## Validation Commands
```

Required behavior:

- Gate 1 confirms exact place identity only.
- Gate 2 asks the four earthquake questions only.
- Gate 3 runs the per-lane loop selected by Gate 2.
- Gate 4 runs deterministic validators before any packet is final.
- Missing public evidence never becomes unsafe, noncompliant, unpermitted, or no permit.
- The skill points to detailed data files instead of embedding huge reference matrices.

**Step 3: Add exact trigger/refusal language**

`SKILL.md` frontmatter description must trigger when the user asks about:

- Philippine building, mall, hotel, establishment, tower, tenant, complex, or facility;
- earthquake safety evidence;
- NSCP/seismic evidence;
- OBO structural permit or plan-review evidence;
- post-earthquake tags, inspections, or clearances.

It must refuse or pause when:

- exact place is not confirmed;
- the user wants legal/engineering certification;
- the user asks for "earthquake-proof" claims;
- the answer would require non-public OBO/operator/professional records and no manual request path is accepted.

**Step 4: Update agent metadata**

`skills/philippines-building-code-evidence-auditor/agents/openai.yaml` should be:

```yaml
interface:
  display_name: "Philippines Building Code Evidence Auditor"
  short_description: "Lock a Philippine building, choose an earthquake audit question, and validate evidence packets without unsafe safety claims"
  default_prompt: "Use this skill to run Gates 1-4 of the Philippine earthquake building-code evidence auditor: place lock, audit scope lock, evidence packet loop, and regression checks."
```

Acceptance checks:

- `short_description` names the earthquake audit question and unsafe-claim boundary.
- `default_prompt` names Gates 1-4.
- Metadata does not imply the skill certifies safety or compliance.

**Step 5: Add a lightweight skill-surface validator to the plan**

The implementation should later add this check either to `scripts/validate_progress_docs.py` or the final Gate 4 suite:

```python
required_skill_phrases = [
    "Gate 1 Place Lock",
    "Gate 2 Earthquake Audit Scope Lock",
    "Gate 3 Evidence Packet Loop",
    "Gate 4 Regression Test Gate",
    "Missing public evidence never",
    "Validation Commands",
]
```

Expected:

- FAIL if the skill surface drifts away from the gate contracts.
- FAIL if the old five-scope Gate 2 menu is reintroduced as active behavior.

**Step 6: Run checks**

Run:

```bash
python3 scripts/validate_progress_docs.py
git diff --check
```

Expected:

- PASS.

**Step 7: Commit checkpoint only if requested**

Suggested commit message:

```bash
git add AGENTS.md skills/philippines-building-code-evidence-auditor/SKILL.md skills/philippines-building-code-evidence-auditor/agents/openai.yaml
git commit -m "docs: lock reusable building-code auditor skill surface"
```

## Task 2: Update Gate 2 Scope Contract To Earthquake-Only

**ECC concept:** Gate 2 is the audit-scope contract. It must lock what the user wants before Gate 3 searches or evaluates evidence.

**Files:**
- Create: `data/building-code-auditor/audit-scope-schema.json`
- Modify: `data/building-code-auditor/audit-scope-test-cases.json`
- Modify: `scripts/validate_audit_scope_gate.py`
- Modify: `skills/philippines-building-code-evidence-auditor/SKILL.md`

**Step 1: Write the failing Gate 2 fixtures**

Replace the old five-scope fixture categories with:

```json
[
  "menu_prompt",
  "nscp_seismic_design_evidence",
  "obo_structural_permit_review",
  "latest_post_earthquake_status",
  "latest_clearance_after_tag",
  "all",
  "ambiguous_scope"
]
```

Each sample Gate 2 packet must include:

```json
{
  "schema_version": "1.0.0",
  "workflow_step": "audit_scope_lock",
  "confirmed_place": {
    "display_name": "KCC Mall of GenSan",
    "candidate_id": "fixture-kcc-gensan",
    "city": "General Santos",
    "country": "Philippines",
    "gate_1_status": "confirmed_by_user"
  },
  "user_intake": {
    "raw_user_scope_request": "1",
    "interpreted_scope": "nscp_seismic_design_evidence",
    "answer_source": "number"
  },
  "scope_menu": [
    {
      "number": 1,
      "scope_id": "nscp_seismic_design_evidence",
      "label": "NSCP / seismic design evidence",
      "lane_type": "availability_only"
    },
    {
      "number": 2,
      "scope_id": "obo_structural_permit_review",
      "label": "OBO structural permit or plan-review evidence",
      "lane_type": "availability_only"
    },
    {
      "number": 3,
      "scope_id": "latest_post_earthquake_status",
      "label": "Latest post-earthquake official tag or inspection status",
      "lane_type": "availability_and_answer"
    },
    {
      "number": 4,
      "scope_id": "latest_clearance_after_tag",
      "label": "Latest clearance after damage, tag, closure, or restriction",
      "lane_type": "availability_and_answer"
    }
  ],
  "scope_confirmation": {
    "status": "scope_confirmed",
    "locked_scope": {
      "scope_ids": ["nscp_seismic_design_evidence"],
      "selected_lanes": ["nscp_seismic_design_evidence"],
      "requires_timeframe": false,
      "requires_target_subscope": true,
      "output_intent": "Check whether public target-specific NSCP or seismic design-review evidence exists."
    },
    "can_proceed_to_evidence_search": true,
    "blockers": []
  },
  "safety": {
    "evidence_search_started": false,
    "blocked_work": [
      "safety_claim",
      "earthquake_proof_claim",
      "nscp_compliance_claim_without_target_document"
    ]
  }
}
```

**Step 2: Run validator and confirm failure**

Run:

```bash
python3 scripts/validate_audit_scope_gate.py
```

Expected:

- FAIL because `scripts/validate_audit_scope_gate.py` still expects the old scope IDs.

**Step 3: Update `scripts/validate_audit_scope_gate.py`**

Change constants to:

```python
REQUIRED_CATEGORIES = {
    "menu_prompt",
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
    "all",
    "ambiguous_scope",
}

SCOPE_IDS = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
    "all",
}

MENU_SCOPE_IDS = [
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
]

LANE_TYPES = {"availability_only", "availability_and_answer"}
```

Validator rules:

- `scope_menu` must contain exactly four options.
- Menu numbers must be `[1, 2, 3, 4]`.
- `all` is a valid locked scope but not a menu row.
- `can_proceed_to_evidence_search` is true only when status is `scope_confirmed`.
- `evidence_search_started` must remain false in all Gate 2 fixtures.
- Forbidden keys remain forbidden: `evidence_results`, `sources_checked`, `claims`, `citations`, `search_results`.
- The prompt must not claim safety, compliance, noncompliance, or current occupancy fitness.

**Step 4: Add `audit-scope-schema.json`**

Create a JSON-schema-style document that mirrors the validator. Required top-level fields:

- `schema_version`
- `workflow_step`
- `confirmed_place`
- `user_intake`
- `scope_menu`
- `scope_confirmation`
- `safety`

**Step 5: Run Gate 2 validator again**

Run:

```bash
python3 scripts/validate_audit_scope_gate.py
```

Expected:

- PASS.

**Step 6: Update skill docs**

In `skills/philippines-building-code-evidence-auditor/SKILL.md`:

- Replace the old five-option menu.
- State Gate 2 is earthquake-only.
- State Gate 2 asks one menu question.
- State Gate 2 does not search evidence.
- Add the four lane types and the `all` behavior.

**Step 7: Commit checkpoint only if requested**

Suggested commit message:

```bash
git add data/building-code-auditor/audit-scope-schema.json data/building-code-auditor/audit-scope-test-cases.json scripts/validate_audit_scope_gate.py skills/philippines-building-code-evidence-auditor/SKILL.md
git commit -m "feat: lock earthquake audit scope gate"
```

## Task 3: Normalize Gate 2 Source-Reality Context

**ECC concept:** Source reality prevents the agent from treating generic public standards as target-specific proof.

**Files:**
- Modify: `data/building-code-auditor/audit-scope-source-reality.json`
- Modify: `scripts/validate_audit_scope_source_reality.py`

**Step 1: Update source-reality scope IDs**

Replace old broad scope IDs with the four earthquake scope IDs plus `all` only where needed as an aggregate behavior.

Each scope reality entry must include:

```json
{
  "scope_id": "nscp_seismic_design_evidence",
  "question": "Is there public target-specific evidence that this building was designed or reviewed for NSCP earthquake or seismic requirements?",
  "lane_type": "availability_only",
  "expected_public_result_shape": [
    "target-specific official or professional document found",
    "no public target-specific document found",
    "manual OBO or owner/operator request needed"
  ],
  "not_enough_if_only_found": [
    "generic NSCP page",
    "operator statement",
    "booking availability",
    "reopening or mall hours"
  ],
  "manual_follow_up_triggers": [
    "no target-specific structural design analysis found",
    "no OBO structural review or approved civil/structural record found"
  ],
  "forbidden_claims": [
    "earthquake-proof",
    "NSCP compliant",
    "structurally safe",
    "fit for occupancy"
  ]
}
```

**Step 2: Run source-reality validator and confirm failure**

Run:

```bash
python3 scripts/validate_audit_scope_source_reality.py
```

Expected:

- FAIL until validator constants and JSON entries use the new scope IDs.

**Step 3: Update validator constants**

Required status values:

```python
STATUS_VALUES = {
    "public_target_document_possible",
    "public_process_only",
    "manual_request_likely",
    "not_assessable_from_public_web",
}
```

Required scope IDs:

```python
SCOPE_IDS = {
    "nscp_seismic_design_evidence",
    "obo_structural_permit_review",
    "latest_post_earthquake_status",
    "latest_clearance_after_tag",
}
```

Validator rules:

- All four scopes are present exactly once.
- Each scope includes `lane_type`.
- Each scope includes at least one manual follow-up trigger.
- Each scope includes forbidden claims blocking safety/compliance overclaims.
- No Gate 3 evidence findings are stored in this source-reality matrix.

**Step 4: Run source-reality validator again**

Run:

```bash
python3 scripts/validate_audit_scope_source_reality.py
```

Expected:

- PASS.

## Task 4: Create Gate 3 Evidence Packet Schema

**ECC concept:** Gate 3 is the dynamic workflow harness output. It records what the agent found, what it did not find, why it stopped, and what the user must manually request.

**Files:**
- Create: `data/building-code-auditor/evidence-packet-schema.json`

**Step 1: Create schema skeleton**

Required top-level fields:

```json
[
  "schema_version",
  "workflow_step",
  "confirmed_place",
  "locked_scope",
  "target_context",
  "lane_results",
  "integrated_answer",
  "manual_follow_up",
  "overclaim_boundary",
  "validation_summary"
]
```

Required constants:

```json
{
  "schema_version": "1.0.0",
  "workflow_step": "earthquake_evidence_packet"
}
```

**Step 2: Define target context**

`target_context` requires:

- `target_subscope`: string, for example whole complex, tower, wing, hotel building, tenant location, or exact affected portion.
- `timeframe`: string or null. Required for lanes 3 and 4.
- `earthquake_event`: string or null. Required for lane 3 and lane 4 if the question depends on a specific event.
- `jurisdiction`: object with `lgu`, `likely_obo_or_ocbo`, and `country`.
- `identity_caveats`: array of strings.

**Step 3: Define lane result object**

Each `lane_results[]` item requires:

```json
{
  "lane_id": "nscp_seismic_design_evidence",
  "lane_type": "availability_only",
  "question": "Is there evidence that this building was designed or reviewed for NSCP earthquake or seismic requirements?",
  "document_targets_searched": [],
  "query_log": [],
  "best_sources": [],
  "answer_found": false,
  "answerability": "not_answerable",
  "answer_text": null,
  "public_evidence_status": "not_found",
  "stop_reason": "no_more_useful_public_sources",
  "manual_follow_up_needed": true,
  "manual_custodians": [],
  "overclaim_risk": "high"
}
```

Allowed `lane_id` values:

- `nscp_seismic_design_evidence`
- `obo_structural_permit_review`
- `latest_post_earthquake_status`
- `latest_clearance_after_tag`

Allowed `lane_type` values:

- `availability_only`
- `availability_and_answer`

Allowed `answerability` values:

- `answerable`
- `not_answerable`

Allowed `public_evidence_status` values:

- `confirmed_public_evidence`
- `partial_public_evidence`
- `not_found`
- `manual_request_needed`
- `not_assessable_from_public_web`
- `conflicting`

Allowed `stop_reason` values:

- `answer_found`
- `no_more_useful_public_sources`
- `manual_record_needed`
- `target_or_timeframe_unclear`
- `professional_review_required`
- `source_conflict`

**Step 4: Define source object**

Each source object requires:

```json
{
  "title": "Davao City issues red/yellow tags on earthquake affected buildings",
  "url": "https://davaocity.gov.ph/local-government/davao-city-issues-red-yellow-tags-on-earthquake-affected-buildings/",
  "source_type": "official_lgu",
  "publisher": "City Government of Davao",
  "date_published_or_accessed": "2026-07-05",
  "target_specific": true,
  "supports": "Official red/yellow tag process and OCBO/PICE inspection context.",
  "does_not_support": "Does not prove current safety for a named building unless the exact target and tag/status are stated."
}
```

Allowed `source_type` values:

- `official_lgu`
- `official_national`
- `official_obo_ocbo`
- `company_filing`
- `operator_or_developer`
- `professional_or_contractor`
- `reputable_news_lead`
- `standards_context`
- `manual_request_path`
- `other`

**Step 5: Define integrated answer**

`integrated_answer` requires:

- `summary`: string.
- `selected_scope_ids`: array.
- `answerable_scope_ids`: array.
- `not_answerable_scope_ids`: array.
- `public_evidence_found`: boolean.
- `manual_follow_up_required`: boolean.
- `citizen_safe_summary`: string.

`citizen_safe_summary` must use evidence language, not certification language.

Allowed wording:

- "Public evidence was found for..."
- "No public target-specific evidence was found for..."
- "Manual follow-up is needed with..."
- "This does not certify earthquake safety or NSCP compliance."

Forbidden wording unless quoted as a blocked claim:

- "earthquake-proof"
- "safe"
- "unsafe"
- "NSCP compliant"
- "noncompliant"
- "fit for occupancy"
- "no permit"

## Task 5: Add Gate 3 Evidence Packet Fixtures

**ECC concept:** Eval-driven development. The validator must be built against concrete examples before it is trusted.

**Files:**
- Create: `data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json`
- Create: `data/building-code-auditor/samples/evidence-packet-q2-confirmed-obo-review.json`
- Create: `data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json`
- Create: `data/building-code-auditor/samples/evidence-packet-q4-clearance-found.json`
- Create: `data/building-code-auditor/samples/evidence-packet-invalid-overclaim.json`

**Step 1: Create Q1 no-public-evidence fixture**

Purpose:

- Proves lanes 1-2 can return a usable availability answer: no public target-specific evidence found.

Expected:

- `lane_type`: `availability_only`
- `answer_found`: false
- `answerability`: `answerable`
- `answer_text`: "No public target-specific NSCP/seismic design-review evidence was found."
- `manual_follow_up_needed`: true
- No forbidden safety/compliance claim.

**Step 2: Create Q2 confirmed OBO-review fixture**

Purpose:

- Proves an official target-tied OBO structural permit/review record can make Q2 answerable.

Expected:

- At least one `best_sources[]` item with `source_type` official or company filing if source text quotes an official record.
- `answer_found`: true
- `answerability`: `answerable`
- `public_evidence_status`: `confirmed_public_evidence` or `partial_public_evidence`
- `answer_text` reports the document evidence only.
- It must not say current safety.

**Step 3: Create Q3 no-public-answer fixture**

Purpose:

- Proves lanes 3-4 behave differently from lanes 1-2.

Expected:

- `lane_type`: `availability_and_answer`
- `answer_found`: false
- `answerability`: `not_answerable`
- `answer_text`: null
- `manual_follow_up_needed`: true
- `manual_custodians` includes OCBO/OBO/LGU or equivalent.
- Integrated answer says no public official tag/status answer was found.

**Step 4: Create Q4 clearance-found fixture**

Purpose:

- Proves the packet can record a real answer when an official clearance, reoccupancy, updated green tag, accepted repair/retrofit completion, or signed/sealed stability certificate is found.

Expected:

- `answer_found`: true
- `answerability`: `answerable`
- `answer_text` includes exact official status language and date/scope caveat.
- Manual follow-up may be false or conditional.
- No generalized safety certification.

**Step 5: Create invalid overclaim fixture**

Purpose:

- Proves Gate 4 catches unsafe claims.

Expected:

- Include a forbidden phrase such as "earthquake-proof" or "NSCP compliant" in an unsupported output field.
- The Gate 3 packet validator must fail this fixture.

## Task 6: Create Gate 3 Packet Validator

**ECC concept:** Deterministic eval gate for agent output.

**Files:**
- Create: `scripts/validate_building_code_packet.py`

**Step 1: Write failing validation command**

Run before creating the script:

```bash
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json
```

Expected:

- FAIL because the script does not exist.

**Step 2: Implement validator structure**

Use only Python standard library:

```python
#!/usr/bin/env python3
"""Validate Gate 3 building-code earthquake evidence packets."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_UNSUPPORTED_PHRASES = {
    "earthquake-proof",
    "earthquake proof",
    "nscp compliant",
    "structurally safe",
    "structurally unsafe",
    "safe to occupy",
    "fit for occupancy",
    "has no permit",
    "unpermitted",
}
```

Required validation functions:

- `read_json(path: Path) -> object`
- `fail(message: str) -> int`
- `is_http_url(value: str) -> bool`
- `require_object(value, path, errors) -> dict | None`
- `expect_enum(value, path, allowed, errors) -> None`
- `expect_string(value, path, errors, allow_null=False) -> None`
- `expect_bool(value, path, errors) -> None`
- `validate_source(source, path, errors) -> None`
- `validate_lane_result(lane, path, errors) -> None`
- `validate_integrated_answer(answer, path, errors) -> None`
- `validate_no_unsupported_overclaims(document, errors) -> None`
- `validate_root(document) -> list[str]`

**Step 3: Implement lane-specific rules**

Rules for lanes 1 and 2:

- If `lane_type` is `availability_only` and no more public sources remain:
  - `answerability` may be `answerable`.
  - `answer_text` may say no public target-specific evidence was found.
  - `manual_follow_up_needed` should be true unless direct evidence was found.

Rules for lanes 3 and 4:

- If `lane_type` is `availability_and_answer` and `answer_found` is false:
  - `answerability` must be `not_answerable`.
  - `answer_text` must be null.
  - `manual_follow_up_needed` must be true.
  - `manual_custodians` must not be empty.

Rules for all lanes:

- `query_log` must not be empty.
- `document_targets_searched` must not be empty.
- Every `best_sources[]` URL must be HTTP/HTTPS.
- If `public_evidence_status` is `confirmed_public_evidence`, at least one source must be target-specific.
- If `stop_reason` is `no_more_useful_public_sources`, the lane must still record what was searched and what was not found.

**Step 4: Implement overclaim scanner**

Scan these fields recursively:

- `answer_text`
- `integrated_answer.summary`
- `integrated_answer.citizen_safe_summary`
- `manual_follow_up`
- `validation_summary`

Fail when forbidden phrases appear unless they are inside:

- `overclaim_boundary.forbidden_claims`
- `does_not_support`
- `blocked_claims`

**Step 5: Validate sample fixtures**

Run:

```bash
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q2-confirmed-obo-review.json
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q4-clearance-found.json
```

Expected:

- PASS for all valid fixtures.

Run:

```bash
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-invalid-overclaim.json
```

Expected:

- FAIL with a clear unsupported-claim error.

## Task 7: Create Gate 3 Markdown Renderer

**ECC concept:** Separate structured machine packet from human-readable report. This preserves raw evidence and prevents hidden interpretation drift.

**Files:**
- Create: `scripts/render_building_code_packet.py`
- Create: `reports/sample-building-code-earthquake-evidence-packet.md`

**Step 1: Write failing renderer command**

Run:

```bash
python3 scripts/render_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json --output /tmp/evidence-packet.md
```

Expected:

- FAIL because the script does not exist.

**Step 2: Implement renderer behavior**

Input:

- One validated Gate 3 packet JSON path.
- Optional `--output` path.

Output sections:

```markdown
# Earthquake Evidence Packet: <confirmed place>

## Scope

## Citizen-Safe Summary

## Lane Results

## Sources

## Manual Follow-Up

## Overclaim Boundary
```

Renderer rules:

- Run the packet validator before rendering.
- If validation fails, do not write the report.
- Use source URLs from the packet.
- Preserve `does_not_support` caveats.
- Do not invent claims not present in packet fields.

**Step 3: Render sample report**

Run:

```bash
python3 scripts/render_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json --output reports/sample-building-code-earthquake-evidence-packet.md
```

Expected:

- PASS.
- Report is created.
- Report states manual follow-up is needed.
- Report does not say safe, unsafe, earthquake-proof, or NSCP-compliant.

## Task 8: Create Gate 4 Regression Cases

**ECC concept:** Gate 4 is the eval gate for the whole workflow. It proves agent output is reusable and not just plausible.

**Files:**
- Create: `data/building-code-auditor/gate-4-regression-cases.json`

**Step 1: Define regression case categories**

Required categories:

```json
[
  "gate_1_confirmed_place",
  "gate_2_scope_lock",
  "gate_3_availability_only_no_public_evidence",
  "gate_3_availability_and_answer_no_public_answer",
  "gate_3_confirmed_public_evidence",
  "gate_3_manual_follow_up",
  "unsafe_claim_blocked",
  "invalid_source_url_blocked"
]
```

**Step 2: Add case structure**

Each case:

```json
{
  "case_id": "gate4-q3-no-public-answer-001",
  "category": "gate_3_availability_and_answer_no_public_answer",
  "description": "Lane 3 without official tag/status evidence is not answerable and requires manual OCBO/OBO follow-up.",
  "input_packet_path": "data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json",
  "expected_result": "pass",
  "expected_checks": [
    "answerability is not_answerable",
    "manual_follow_up_needed is true",
    "manual_custodians is not empty",
    "no unsupported safety or compliance claim"
  ]
}
```

Invalid cases must use `expected_result: "fail"`.

## Task 9: Create Gate 4 Suite Validator

**ECC concept:** One command should tell the operator whether the workflow is safe to hand off.

**Files:**
- Create: `scripts/validate_building_code_gate_suite.py`

**Step 1: Write failing suite command**

Run:

```bash
python3 scripts/validate_building_code_gate_suite.py
```

Expected:

- FAIL because the script does not exist.

**Step 2: Implement suite runner**

The suite must run these commands:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q2-confirmed-obo-review.json
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-q4-clearance-found.json
python3 scripts/validate_progress_docs.py
```

It must also assert that invalid fixtures fail:

```bash
python3 scripts/validate_building_code_packet.py data/building-code-auditor/samples/evidence-packet-invalid-overclaim.json
```

Expected for invalid fixture:

- The child command exits non-zero.
- The suite treats that as PASS for the negative test.

**Step 3: Implement machine-readable output**

At the end, print:

```text
building code gate suite: PASS
```

On failure, print:

```text
building code gate suite: FAIL: <reason>
```

## Task 10: Final Skill Surface Consistency Review

**ECC concept:** Reusable skill extraction review. The actual skill surface was built in Task 1A; this task verifies it still matches the final schemas, validators, and Gate 1-4 behavior after implementation.

**Files:**
- Modify if needed: `AGENTS.md`
- Modify: `skills/philippines-building-code-evidence-auditor/SKILL.md`
- Modify: `skills/philippines-building-code-evidence-auditor/agents/openai.yaml`

**Step 1: Re-check skill title and description**

`agents/openai.yaml` should mention:

```yaml
interface:
  display_name: "Philippines Building Code Evidence Auditor"
  short_description: "Lock Philippine building identity, choose an earthquake audit question, and validate evidence packets without unsafe safety claims"
  default_prompt: "Use this skill to run Gates 1-4 of the Philippine earthquake building-code evidence auditor: place lock, audit scope lock, evidence packet, and regression checks."
```

**Step 2: Rewrite skill gate sections**

The skill must still have these sections in order:

- `Gate 1 Place Lock`
- `Gate 2 Earthquake Audit Scope Lock`
- `Gate 3 Evidence Packet Loop`
- `Gate 4 Regression Test Gate`
- `Forbidden Claims`
- `Validation Commands`

**Step 3: Preserve critical Gate 1 rules**

Gate 1 must keep:

- identity-only lookup;
- maximum three search queries or three source checks before asking;
- one focused clarifying question;
- no permit, safety, compliance, incident, or earthquake search.

**Step 4: Add Gate 3 loop language**

Gate 3 must say:

- For each selected lane, search exact targeted documents.
- Analyze whether an answer was found.
- If no answer was found, continue only while there is another useful public source type.
- Stop when no useful public source remains.
- For lanes 1-2, no public evidence means the availability answer is no public evidence found.
- For lanes 3-4, no public evidence means no public answer and manual follow-up needed.

## Task 11: Update Progress Docs And Mermaid Charts

**ECC concept:** Handoff artifacts must match the actual harness.

**Files:**
- Modify: `docs/plans/building-code-progress-table.md`
- Modify: `docs/plans/gate-1-place-lock-chart.md`
- Modify: `docs/plans/gate-2-audit-scope-lock-chart.md`
- Modify: `docs/plans/gate-3-evidence-packet-chart.md`
- Modify: `docs/plans/gate-4-regression-tests-chart.md`
- Modify: `README.md`
- Modify: `docs/status/2026-07-04-building-code-evidence-auditor-lock.md`

**Step 1: Keep charts Mermaid-only**

Each gate chart file must contain exactly one Mermaid block and no extra prose.

Allowed:

```markdown
```mermaid
graph TD
  ...
```
```

Not allowed:

- `flowchart`
- `classDef`
- Mermaid init directives
- images
- prose outside the Mermaid block

**Step 2: Update progress table**

Progress table must say:

- Gate 1: implemented and validated.
- Gate 2: earthquake scope lock implemented once Task 2 passes.
- Gate 3: schema, fixtures, validator, and renderer implemented once Tasks 4-7 pass.
- Gate 4: regression suite implemented once Tasks 8-9 pass.
- Cron/live search: deferred.

**Step 3: Validate Mermaid**

For each gate chart:

```bash
awk '/^```mermaid$/{flag=1; next} /^```$/{flag=0} flag {print}' docs/plans/gate-3-evidence-packet-chart.md > /tmp/gate-3-evidence-packet-chart.mmd
curl -sS -f -X POST -H "Content-Type: text/plain" --data-binary @/tmp/gate-3-evidence-packet-chart.mmd https://kroki.io/mermaid/svg -o /tmp/gate-3-evidence-packet-chart.svg
```

Expected:

- Kroki exits 0.
- SVG file exists and is non-empty.

## Task 12: Add Final Verification Checklist

**ECC concept:** Handoff must include exact eval commands and pass signals.

**Files:**
- Modify: `README.md`
- Modify: `docs/status/2026-07-04-building-code-evidence-auditor-lock.md`

**Step 1: Add final command list**

Use this final verification block:

```bash
python3 -m json.tool data/building-code-auditor/building-identity-schema.json >/tmp/building-identity-schema.json
python3 -m json.tool data/building-code-auditor/audit-scope-schema.json >/tmp/audit-scope-schema.json
python3 -m json.tool data/building-code-auditor/audit-scope-test-cases.json >/tmp/audit-scope-test-cases.json
python3 -m json.tool data/building-code-auditor/audit-scope-source-reality.json >/tmp/audit-scope-source-reality.json
python3 -m json.tool data/building-code-auditor/evidence-packet-schema.json >/tmp/evidence-packet-schema.json
python3 -m json.tool data/building-code-auditor/gate-4-regression-cases.json >/tmp/gate-4-regression-cases.json
python3 scripts/validate_building_code_gate_suite.py
git diff --check
```

Expected final signal:

```text
building code gate suite: PASS
```

**Step 2: Add deferred automation note**

Add this note to README or status:

```markdown
Live web search, cron monitoring, and `.mjs` orchestration are deferred until
Gates 1-4 pass the deterministic Python harness. This prevents automating
unvalidated packet shapes or unsafe building-safety claims.
```

## Task 13: Final Manual Review

**ECC concept:** Human review is required for safety-sensitive agent workflows.

**Files:**
- Review all changed files from Tasks 1-12.

**Step 1: Inspect diff**

Run:

```bash
git diff -- docs/plans data/building-code-auditor scripts skills README.md docs/status
```

Review for:

- old five-scope menu still appearing as active Gate 2 behavior;
- unsafe claims;
- duplicate or conflicting schema fields;
- docs saying cron/live search exists;
- missing manual follow-up for lanes 3-4;
- raw findings being treated as final certification.

**Step 2: Run final suite**

Run:

```bash
python3 scripts/validate_building_code_gate_suite.py
git diff --check
```

Expected:

- Both pass.

**Step 3: Report implementation result**

Final implementation report must include:

- files created;
- files modified;
- validation commands and results;
- explicit note that no live search/cron was added;
- next recommended work: live Gate 3 run using one confirmed sample target.

## Expected File Inventory After Completion

New files:

- `docs/plans/2026-07-05-building-code-gates-1-4-ecc-implementation-plan.md`
- `data/building-code-auditor/audit-scope-schema.json`
- `data/building-code-auditor/evidence-packet-schema.json`
- `data/building-code-auditor/gate-4-regression-cases.json`
- `data/building-code-auditor/samples/evidence-packet-q1-no-public-evidence.json`
- `data/building-code-auditor/samples/evidence-packet-q2-confirmed-obo-review.json`
- `data/building-code-auditor/samples/evidence-packet-q3-no-public-answer.json`
- `data/building-code-auditor/samples/evidence-packet-q4-clearance-found.json`
- `data/building-code-auditor/samples/evidence-packet-invalid-overclaim.json`
- `scripts/validate_building_code_packet.py`
- `scripts/render_building_code_packet.py`
- `scripts/validate_building_code_gate_suite.py`
- `reports/sample-building-code-earthquake-evidence-packet.md`

Modified files:

- `AGENTS.md`
- `data/building-code-auditor/audit-scope-test-cases.json`
- `data/building-code-auditor/audit-scope-source-reality.json`
- `scripts/validate_audit_scope_gate.py`
- `scripts/validate_audit_scope_source_reality.py`
- `skills/philippines-building-code-evidence-auditor/SKILL.md`
- `skills/philippines-building-code-evidence-auditor/agents/openai.yaml`
- `docs/plans/building-code-progress-table.md`
- `docs/plans/gate-1-place-lock-chart.md`
- `docs/plans/gate-2-audit-scope-lock-chart.md`
- `docs/plans/gate-3-evidence-packet-chart.md`
- `docs/plans/gate-4-regression-tests-chart.md`
- `README.md`
- `docs/status/2026-07-04-building-code-evidence-auditor-lock.md`

## Non-Goals

Do not add these in this implementation:

- cron;
- scheduled monitoring;
- `.mjs` orchestration;
- live web search runner;
- browser automation;
- third-party writes;
- credentials;
- official safety certification;
- legal compliance conclusions;
- engineering conclusions.

Those belong after the Python harness has a stable packet contract and the Gate 4 regression suite passes.
