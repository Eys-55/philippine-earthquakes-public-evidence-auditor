# Market Research Agent Workspace

ECC-aligned workspace for multiple source-attributed agent workflows. Each
workflow lives in its own project lane so instructions, schemas, evidence,
reports, and safety boundaries stay separate.

## Active Lanes

| Lane | Status | Purpose | Start Here |
| --- | --- | --- | --- |
| `philippines-building-code-evidence-auditor` | active | Confirm a Philippine building, establishment, mall, hotel, or facility, then prepare audit-only public evidence about permits, occupancy, incidents, earthquake damage, contractors, and standards context. | `skills/philippines-building-code-evidence-auditor/SKILL.md` |
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
For example, the Building Code Evidence Auditor currently uses
`data/building-code-auditor/`.

See `docs/decisions/0004-adopt-project-lanes.md` and
`docs/status/2026-07-04-project-lanes-workspace-status.md`.

## Building Code Evidence Auditor

Current active lane:

- Skill: `skills/philippines-building-code-evidence-auditor/SKILL.md`
- Status: `docs/status/2026-07-04-building-code-evidence-auditor-lock.md`
- Decision: `docs/decisions/0003-lock-philippines-building-code-evidence-auditor.md`
- Data: `data/building-code-auditor/`
- Current gate: building identity confirmation before any permit, contractor,
  incident, compliance, safety, or earthquake evidence search.

This lane is an evidence auditor, not a compliance certifier. It must not claim
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

## Verification

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
