![Abstract seismic evidence banner](assets/philippines-earthquake-public-evidence-auditor-header.png)

# Philippines Earthquake Public Evidence Auditor

A Codex/ECC workflow for checking what public evidence exists about a specific
Philippine building's earthquake-related records. It does not certify safety,
compliance, or fitness for occupancy. It locks the exact building first, runs
all four earthquake evidence lanes by default unless the user narrows the run,
then produces a source-bounded packet with unresolved gaps preserved.

## What It Audits

This workflow only searches four earthquake evidence lanes:

1. NSCP / seismic design evidence
2. OBO structural permit or review evidence
3. Latest post-earthquake tag / status
4. Latest clearance after damage or tag

Questions outside these lanes belong in a separate workflow. The auditor should
not silently broaden a request into general permits, fire safety, accessibility,
business permits, contractor research, or generic building-code compliance.

## How The Workflow Runs

1. Gate 1 confirms the exact building, branch, tenant, wing, or complex.
2. Gate 2 defaults to all four earthquake evidence lanes and lets the user
   narrow to one or more lanes.
3. Gate 3 builds a parent audit run with one child evidence packet per selected
   lane.
4. Gate 4 audits each lane packet and the parent summary for overclaims before
   anything is treated as a finding.

The workflow is intentionally narrow. Its job is to preserve what can be shown
from public evidence and to keep missing, weak, or unresolved evidence visible.

## Evidence Rules

The auditor separates evidence by source strength:

- official records and notices;
- signed or sealed professional records;
- operator or corporate claims;
- reputable news leads;
- process or standards context;
- weak public leads such as marketing pages, booking availability, directory
  pages, or social posts.

Positive findings need exact-target evidence and a source URL. Operator claims,
process pages, and weak leads can guide follow-up, but they do not become
official clearance or engineering evidence by themselves.

Missing public evidence is not evidence of safety, non-safety, compliance,
noncompliance, clearance, no tag, no permit, or no review.

## No-Evidence Semantics

For NSCP/seismic design evidence and OBO structural review evidence, a complete
but unsuccessful search means: `No public evidence found.`

For post-earthquake tag/status and clearance after damage or tag, a complete but
unsuccessful search means: `No public answer found.`

Neither result should be converted into a claim that the building is safe,
unsafe, compliant, noncompliant, cleared, tagged, untagged, permitted, or
unreviewed.

## Evidence Packet Output

The output is designed for operators who need to see what was searched, what was
found, and what remains unresolved. The parent audit run records:

- confirmed building identity;
- selected earthquake lanes;
- source ingestion policy;
- child lane packet summaries;
- cross-lane unresolved exceptions;
- final overclaim status.

Each child lane packet records:

- locked earthquake lane;
- document inventory;
- evidence strength;
- source curation class;
- physical-condition public evidence;
- unresolved exceptions;
- manual request targets;
- overclaim boundary;
- query log;
- packet result.

Public-source ingestion stores metadata plus short snippets only: URL, source
label, source class, date or freshness signal when visible, short excerpt, query
used, and lane relevance. It does not mirror whole public pages by default.

This makes the output auditable. Another operator should be able to tell which
claims are supported, which leads are weak, and which documents still need manual
request or professional review.

## Operator Checklist

Before presenting a packet, check that:

- the exact building match is confirmed;
- selected lanes are one or more of the four earthquake lanes;
- every positive finding has a source URL;
- official and professional records are separated from weak leads;
- operator or corporate claims are not treated as official clearance;
- unresolved exceptions are preserved;
- no missing evidence has been converted into a safety or compliance conclusion;
- the parent summary does not overstate any child lane result.

If any item fails, the packet should be revised before it is treated as a
finding.

## Manual Request Handoff

Some outcomes are valid even when the public web does not answer the question.
In those cases, the workflow should name the likely custodian and the exact
document family to request, instead of guessing.

Common handoff targets include the relevant building official or structural
record custodian, the owner or operator, and the professional record holder. The
handoff should stay document-specific: ask for the record that would answer the
selected lane, not for a general assurance that a building is safe.

## Workspace Notes

This repo is an ECC-aligned multi-lane workspace. Multiple agentic workflows may
live here at the same time, but each workflow stays in its own project lane so
instructions, schemas, evidence, reports, and safety boundaries do not mix.

## Run The Validators

Use these checks for the current auditor:

```bash
find data/philippines-building-code-evidence-auditor-v2 -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/tmp/building-code-v2-json-parse.txt
python3 scripts/validate_building_code_v2_identity_gate.py
python3 scripts/validate_building_code_v2_earthquake_scope_gate.py
python3 scripts/validate_building_code_v2_evidence_packet.py
python3 scripts/validate_building_code_v2_overclaim.py
python3 scripts/validate_progress_docs.py
git diff --check
```

For maintainer checks that preserve the earlier broad building-code workflow:

```bash
python3 scripts/validate_building_identity_gate.py
python3 scripts/validate_audit_scope_gate.py
python3 scripts/validate_audit_scope_source_reality.py
```

## Repo Map

- Current auditor skill: `skills/philippines-building-code-evidence-auditor-v2/SKILL.md`
- Current auditor data: `data/philippines-building-code-evidence-auditor-v2/`
- README design: `docs/plans/2026-07-05-earthquake-auditor-readme-design.md`
- README implementation plan: `docs/plans/2026-07-05-earthquake-auditor-readme-implementation-plan.md`
- Status lock: `docs/status/2026-07-05-philippines-building-code-evidence-auditor-v2-lock.md`

## Active Lanes

| Lane | Status | Purpose | Start Here |
| --- | --- | --- | --- |
| `philippines-building-code-evidence-auditor-v2` | active current auditor | Four-lane earthquake public-evidence auditor for NSCP/seismic evidence, OBO structural review, post-earthquake tag/status, and clearance after damage or tag. | `skills/philippines-building-code-evidence-auditor-v2/SKILL.md` |
| `philippines-building-code-evidence-auditor` | active V1 maintainer lane | Broad building-code public-evidence auditor for Philippine buildings, establishments, malls, hotels, and facilities. | `skills/philippines-building-code-evidence-auditor/SKILL.md` |
| `address-disaster-risk-assessor` | paused/foundation | Given an address or coordinates, produce a source-attributed disaster-risk packet for Metro Manila / NCR. | `skills/address-disaster-risk-assessor/SKILL.md` |
| `metro-manila-source-atlas` | foundation | Refresh or extend the reusable Metro Manila data-source inventory. | `skills/metro-manila-source-atlas/SKILL.md` |
| `untitled-project` | exploring | Parking lane for the next workflow before the repeated job, input contract, and output artifact are named. | `skills/untitled-project/SKILL.md` |

Before starting work, choose one lane. If a request could belong to multiple
lanes, ask one lane-selection question before editing files.

## Lane Convention

For new lanes, use one stable slug per workflow:

- `skills/<project-slug>/SKILL.md` - canonical workflow instructions.
- `data/<project-slug>/` - schemas, fixtures, raw evidence, source notes, and
  evals.
- `reports/<project-slug>-*.md` - integrated reports and evidence packets.
- `docs/plans/YYYY-MM-DD-<project-slug>-*.md` - design and execution plans.
- `docs/decisions/000X-*.md` - durable decisions.
- `docs/status/YYYY-MM-DD-<project-slug>-*.md` - handoff and resume notes.
- `scripts/validate_<project_slug>*.py` - validation gates when useful.

Existing lanes with documented historical data surfaces can keep those paths.
For example, the V1 Building Code Evidence Auditor currently uses
`data/building-code-auditor/`.

See `docs/decisions/0004-adopt-project-lanes.md` and
`docs/status/2026-07-04-project-lanes-workspace-status.md`.

## Building Code Evidence Auditor Maintainer Context

Current earthquake auditor:

- Skill: `skills/philippines-building-code-evidence-auditor-v2/SKILL.md`
- Status: `docs/status/2026-07-05-philippines-building-code-evidence-auditor-v2-lock.md`
- Design: `docs/plans/2026-07-05-earthquake-auditor-readme-design.md`
- Implementation plan: `docs/plans/2026-07-05-earthquake-auditor-readme-implementation-plan.md`
- Data: `data/philippines-building-code-evidence-auditor-v2/`
- Scope: four earthquake evidence lanes only: NSCP/seismic design evidence, OBO
  structural permit or review evidence, latest post-earthquake tag/status, and
  latest clearance after damage or tag.

V1 maintainer lane:

- Skill: `skills/philippines-building-code-evidence-auditor/SKILL.md`
- Status: `docs/status/2026-07-04-building-code-evidence-auditor-lock.md`
- Decision: `docs/decisions/0003-lock-philippines-building-code-evidence-auditor.md`
- Data: `data/building-code-auditor/`
- Current gate: building identity confirmation before any permit, contractor,
  incident, compliance, safety, or earthquake evidence search.

These lanes are evidence auditors, not compliance certifiers. They must not claim
that a building is legally compliant, structurally safe, earthquake-safe, or fit
for occupancy unless that exact claim is supported by authoritative public
evidence.

## Disaster Risk Assessor

The earlier disaster-risk lane remains useful foundation work.

- Plan: `docs/plans/2026-07-03-address-disaster-risk-assessor-design.md`
- Decision: `docs/decisions/0002-lock-address-disaster-risk-assessor.md`
- Status: `docs/status/2026-07-03-project-pause-handoff.md`
- Skill: `skills/address-disaster-risk-assessor/SKILL.md`
- Data: `data/disaster-risk/`
- Report: `reports/disaster-risk-data-source-atlas.md`

The product goal is address-in, disaster-risk-packet-out for Metro Manila / NCR,
with source links and confidence labels.

## Source Atlas Foundation

Reusable source inventory and validation artifacts:

- `skills/metro-manila-source-atlas/SKILL.md`
- `data/metro-manila-source-atlas.json`
- `data/source-schema.json`
- `data/verification-log.md`
- `data/deep-dive/local-validation-summary.json`
- `data/deep-dive/source-qualification-matrix.json`
- `data/agent-findings/`
- `reports/metro-manila-data-source-atlas.md`
- `reports/metro-manila-source-deep-dive.md`
- `docs/decisions/0001-city-level-prototype-first.md`

## Untitled Project

Use `untitled-project` only as a temporary holding lane.

Before promoting it, lock:

- repeated real-world job;
- trigger and refusal scope;
- input contract;
- output artifact;
- agent lanes;
- raw evidence surface;
- validation loop;
- safety boundary.

Then rename `skills/untitled-project/` and `data/untitled-project/` to the final
slug and add a decision note.

## Workspace Verification

```bash
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
python3 -m json.tool data/disaster-risk/source-priorities.json >/tmp/disaster-risk-source-priorities.json
python3 -m json.tool data/disaster-risk/disaster-source-atlas.json >/tmp/disaster-source-atlas.json
python3 -m json.tool data/disaster-risk/local-validation-summary.json >/tmp/disaster-local-validation-summary.json
python3 scripts/validate_progress_docs.py
git diff --check
```

For docs-only changes, JSON parsing and whitespace checks are the required gate.
For future code, add tests before implementation and keep ECC's 80% coverage
target.

## ECC Boundaries

- Research is read-only.
- No credentials, signups, writes to third-party systems, or auth bypasses.
- Every important claim in an integrated report links to a source URL.
- Raw findings are preserved separately from integrated outputs.
