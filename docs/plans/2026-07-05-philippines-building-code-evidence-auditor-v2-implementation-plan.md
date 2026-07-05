# Philippines Building Code Evidence Auditor V2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create an isolated V2 workflow lane by copying V1 100%, then revamping the copy into a stricter four-lane earthquake public-evidence auditor.

**Architecture:** V1 remains untouched. V2 gets its own skill, data surface, validators, fixtures, and docs entries. V2 keeps the Gate 1-4 workflow shape but permanently limits Gate 2 to exactly four earthquake evidence searches.

**Tech Stack:** Markdown skills, JSON schemas and fixtures, Python validators, ECC lane docs, repo-local verification scripts.

---

## Non-Negotiable Scope Invariant

V2 Gate 2 has exactly these four searchable lanes forever:

1. `nscp_seismic_design_evidence`
2. `obo_structural_permit_review_evidence`
3. `post_earthquake_tag_status`
4. `clearance_after_damage_or_tag`

No fifth option. No broad public-evidence scope. No general permit, contractor, standards, fire, accessibility, business-permit, or generic building-code scope in V2.

The Gate 3 evidence packet is an output format for the four lanes, not a Gate 2 lane.

## Task 1: Copy V1 Into Isolated V2 Surfaces

**Files:**
- Create: `skills/philippines-building-code-evidence-auditor-v2/`
- Create: `data/philippines-building-code-evidence-auditor-v2/`
- Copy from: `skills/philippines-building-code-evidence-auditor/`
- Copy from: `data/building-code-auditor/`

**Step 1: Create the V2 skill and data directories**

Run:

```bash
mkdir -p skills/philippines-building-code-evidence-auditor-v2 data/philippines-building-code-evidence-auditor-v2
```

**Step 2: Copy V1 into V2**

Run:

```bash
cp -R skills/philippines-building-code-evidence-auditor/. skills/philippines-building-code-evidence-auditor-v2/
cp -R data/building-code-auditor/. data/philippines-building-code-evidence-auditor-v2/
```

**Step 3: Verify V1 remains untouched**

Run:

```bash
git diff -- skills/philippines-building-code-evidence-auditor data/building-code-auditor
```

Expected: no diff.

## Task 2: Rewrite V2 Skill Metadata And Top-Level Contract

**Files:**
- Modify: `skills/philippines-building-code-evidence-auditor-v2/SKILL.md`
- Modify: `skills/philippines-building-code-evidence-auditor-v2/agents/openai.yaml`

**Step 1: Rename V2 metadata**

Set the skill name to `philippines-building-code-evidence-auditor-v2`.

Set the display name to `Philippines Building Code Evidence Auditor V2`.

**Step 2: Add the V2 scope contract**

State that V2 is an isolated copy-and-revamp of V1.

State that V1 remains the broad building-code evidence auditor.

State that V2 is the four-lane earthquake public-evidence auditor.

**Step 3: Remove broad V1 Gate 2 language from V2**

Delete or rewrite copied V1 text that offers:

- permit or occupancy records as a broad standalone lane;
- incident, damage, closure, repair, or retrofit history as a broad standalone lane;
- contractor, professional, developer, or operator evidence as a standalone lane;
- standards or process context only as a standalone lane;
- broad public-evidence packet as a Gate 2 choice.

Expected: V2 `SKILL.md` contains only the four earthquake lanes as Gate 2 choices.

## Task 3: Implement V2 Gate 1 Identity Lock

**Files:**
- Modify: `skills/philippines-building-code-evidence-auditor-v2/SKILL.md`
- Use: `data/philippines-building-code-evidence-auditor-v2/building-identity-schema.json`
- Use: `data/philippines-building-code-evidence-auditor-v2/samples/*.json`
- Create: `scripts/validate_building_code_v2_identity_gate.py`

**Step 1: Keep the V1 identity packet shape**

Gate 1 still requires exact place confirmation before audit search.

**Step 2: Add earthquake-specific identity limits**

Gate 1 identity evidence must not prove:

- earthquake safety;
- NSCP/seismic design;
- OBO structural review;
- post-earthquake tag/status;
- clearance;
- compliance;
- current fitness for occupancy.

**Step 3: Add the V2 identity validator**

Copy the V1 validator pattern, point it at `data/philippines-building-code-evidence-auditor-v2/`, and add V2-specific forbidden conclusion checks.

**Step 4: Run the validator**

Run:

```bash
python3 scripts/validate_building_code_v2_identity_gate.py
```

Expected: pass.

## Task 4: Implement V2 Gate 2 Four-Lane Earthquake Scope Lock

**Files:**
- Create: `data/philippines-building-code-evidence-auditor-v2/earthquake-scope-test-cases.json`
- Create: `data/philippines-building-code-evidence-auditor-v2/earthquake-source-reality.json`
- Create: `scripts/validate_building_code_v2_earthquake_scope_gate.py`

**Step 1: Create the only allowed Gate 2 scope IDs**

Use exactly:

```text
nscp_seismic_design_evidence
obo_structural_permit_review_evidence
post_earthquake_tag_status
clearance_after_damage_or_tag
```

**Step 2: Create the V2 Gate 2 menu**

Use exactly four options:

```text
For [confirmed place], which earthquake evidence search should run?
1. NSCP / seismic design evidence
2. OBO structural permit or review evidence
3. Latest post-earthquake tag / status
4. Latest clearance after damage or tag
```

**Step 3: Add V2 Gate 2 fixtures**

Add cases for:

- menu prompt;
- each of the four locked scopes;
- ambiguous scope;
- unsupported broad V1 scope.

**Step 4: Add the V2 Gate 2 validator**

The validator must fail if:

- the menu length is not 4;
- any V1 broad scope ID appears;
- `can_proceed_to_evidence_search` is true without one of the four scopes;
- evidence search starts during Gate 2.

**Step 5: Run the validator**

Run:

```bash
python3 scripts/validate_building_code_v2_earthquake_scope_gate.py
```

Expected: pass.

## Task 5: Implement V2 Gate 3 Evidence Packet Schema

**Files:**
- Create: `data/philippines-building-code-evidence-auditor-v2/evidence-packet-schema.json`
- Create: `data/philippines-building-code-evidence-auditor-v2/evidence-packet-fixtures/*.json`
- Create: `scripts/validate_building_code_v2_evidence_packet.py`

**Step 1: Define required packet fields**

Require:

- `confirmed_building`
- `locked_earthquake_lane`
- `document_inventory`
- `evidence_strength`
- `source_curation_class`
- `physical_condition_public_evidence`
- `unresolved_exceptions`
- `manual_request_targets`
- `overclaim_boundary`
- `query_log`
- `packet_result`

**Step 2: Define evidence strength values**

Use:

- `direct_authoritative_target_evidence`
- `professional_target_evidence`
- `strong_indirect_target_evidence`
- `process_or_standards_context`
- `weak_lead_only`
- `not_found_after_reasonable_search`

**Step 3: Define source curation classes**

Use:

- `official_record`
- `professional_record`
- `operator_corporate_claim`
- `reputable_news_lead`
- `process_context`
- `weak_lead`

**Step 4: Define no-evidence semantics**

For `nscp_seismic_design_evidence` and `obo_structural_permit_review_evidence`, no findings after a reasonable search means:

```text
No public evidence found.
```

For `post_earthquake_tag_status` and `clearance_after_damage_or_tag`, no findings after a reasonable search means:

```text
No public answer found.
```

Neither may become a safety, compliance, tag, clearance, no-permit, or no-review conclusion.

**Step 5: Add packet fixtures**

Add fixtures for:

- no public evidence found for NSCP/seismic;
- no public evidence found for OBO structural review;
- no public answer found for post-earthquake tag/status;
- no public answer found for clearance;
- red/yellow tag found;
- corporate/operator claim only;
- official clearance found.

**Step 6: Run the validator**

Run:

```bash
python3 scripts/validate_building_code_v2_evidence_packet.py
```

Expected: pass.

## Task 6: Implement V2 Gate 4 Overclaim Audit

**Files:**
- Create: `data/philippines-building-code-evidence-auditor-v2/overclaim-fixtures/*.json`
- Create: `scripts/validate_building_code_v2_overclaim.py`

**Step 1: Add Gate 4 checklist validation**

The validator must require:

- exact building match confirmed;
- locked scope is one of the four earthquake lanes;
- every positive claim has a source URL;
- official/professional evidence separated from weak leads;
- operator/corporate claims not treated as official clearance;
- missing evidence not converted into safety/compliance/status conclusions;
- red/yellow tag evidence preserved when found;
- unresolved exceptions preserved;
- query log present for no-evidence outcomes.

**Step 2: Add negative fixtures**

Add fixtures that should fail when:

- a missing source is converted into `safe`;
- a corporate/operator claim is treated as official clearance;
- unresolved exceptions are erased;
- a broad V1 scope appears.

**Step 3: Run the validator**

Run:

```bash
python3 scripts/validate_building_code_v2_overclaim.py
```

Expected: pass for valid fixtures and fail internally on expected-invalid fixtures.

## Task 7: Update README And Lane Docs

**Files:**
- Modify: `README.md`
- Create: `docs/status/2026-07-05-philippines-building-code-evidence-auditor-v2-lock.md`

**Step 1: Add explicit V1 and V2 lane entries**

README must list:

- `philippines-building-code-evidence-auditor` as V1, broad building-code public-evidence auditor;
- `philippines-building-code-evidence-auditor-v2` as V2, four-lane earthquake public-evidence auditor.

**Step 2: Preserve V1 status**

Do not imply V1 is obsolete or broken.

**Step 3: Add the V2 status lock**

The status doc must state:

- V2 copied V1 first;
- V1 is untouched;
- V2 scope is permanently the four earthquake lanes;
- V2 Gate 3 output is evidence packet format, not a fifth scope.

## Task 8: Verification

**Files:**
- Check: all V2 JSON files
- Check: V1 validators
- Check: V2 validators
- Check: progress docs

**Step 1: Parse V2 JSON**

Run:

```bash
find data/philippines-building-code-evidence-auditor-v2 -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/tmp/building-code-v2-json-parse.txt
```

Expected: no JSON parse errors.

**Step 2: Run V1 validators unchanged**

Run:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
```

Expected: all pass.

**Step 3: Run V2 validators**

Run:

```bash
python3 scripts/validate_building_code_v2_identity_gate.py
python3 scripts/validate_building_code_v2_earthquake_scope_gate.py
python3 scripts/validate_building_code_v2_evidence_packet.py
python3 scripts/validate_building_code_v2_overclaim.py
```

Expected: all pass.

**Step 4: Run repo documentation and whitespace checks**

Run:

```bash
python3 scripts/validate_progress_docs.py
git diff --check
```

Expected: all pass.

## Implementation Guardrails

- Do not touch `skills/philippines-building-code-evidence-auditor/`.
- Do not touch `data/building-code-auditor/`.
- All V2 edits happen in `*-v2` paths.
- If copied V1 text conflicts with the four-lane earthquake invariant, rewrite it in V2.
- If evidence is missing after a proper search, preserve that as a valid no-evidence or no-public-answer result.
- Never convert missing public evidence into safety, compliance, clearance, tag, permit, or review conclusions.
