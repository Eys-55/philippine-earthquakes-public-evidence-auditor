# Address Disaster Risk Assessor

ECC-aligned project for a reusable address-based disaster risk assessor.

The product goal is simple: given an address, return a source-attributed disaster
risk packet covering flood, river proximity, liquefaction, active fault
proximity, landslide or storm-surge relevance where applicable, and confidence
notes for each signal.

The earlier Metro Manila source atlas remains the foundation data inventory. The
active project direction is now disaster-risk assessment only, not broad market
research or generic city scoring.

## Artifacts

- `docs/plans/2026-07-03-address-disaster-risk-assessor-design.md` - locked product design.
- `docs/decisions/0002-lock-address-disaster-risk-assessor.md` - accepted decision to focus this repo on disaster risk.
- `docs/status/2026-07-03-ecc-handoff-summary.md` - restart summary of the ECC work, current goal shape, and next decision.
- `skills/address-disaster-risk-assessor/SKILL.md` - reusable ECC workflow for address-in, risk-packet-out assessment.
- `data/disaster-risk/source-priorities.json` - canonical source priority list for the disaster assessor.
- `data/disaster-risk/disaster-source-atlas.json` - ranked machine-readable disaster-source atlas from the six-agent run.
- `data/disaster-risk/local-validation-summary.json` - live endpoint checks for high-priority disaster sources.
- `data/disaster-risk/agent-findings/` - preserved raw findings from the six disaster research agents.
- `reports/disaster-risk-data-source-atlas.md` - integrated disaster-source report and MVP source order.
- `reports/metro-manila-data-source-atlas.md` - decision-ready integrated report.
- `reports/metro-manila-source-deep-dive.md` - qualification pass over the strongest buildable sources.
- `data/metro-manila-source-atlas.json` - machine-readable ranked inventory.
- `data/source-schema.json` - row schema for source inventory entries.
- `data/verification-log.md` - live checks performed during source validation.
- `data/deep-dive/local-validation-summary.json` - structured record of live checks for the deep dive.
- `data/deep-dive/source-qualification-matrix.json` - build-readiness matrix for the strongest source groups.
- `data/agent-findings/` - raw findings from the six parallel research streams.
- `docs/decisions/0001-city-level-prototype-first.md` - superseded market-scoring decision retained for history.
- `skills/metro-manila-source-atlas/SKILL.md` - reusable ECC workflow for refreshing or extending the atlas.

## Current Build Direction

Build the first product as an **Address Disaster Risk Assessor**:

- Input: address or coordinates.
- Output: disaster risk packet with source links and confidence labels.
- First geography: Metro Manila / NCR.
- First risk classes: flood, historical flood-prone points, river proximity,
  liquefaction, active fault proximity, landslide or storm-surge relevance where
  data supports it.
- Later/weak class: waste-management or drainage-service risk only when a clean
  source or defensible proxy is validated.

Do not build generic market scoring unless the user explicitly reopens that
direction.

## Verification

```bash
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
python3 -m json.tool data/disaster-risk/source-priorities.json >/tmp/disaster-risk-source-priorities.json
python3 -m json.tool data/disaster-risk/disaster-source-atlas.json >/tmp/disaster-source-atlas.json
python3 -m json.tool data/disaster-risk/local-validation-summary.json >/tmp/disaster-local-validation-summary.json
git diff --check
```

## ECC Boundaries

- Research is read-only.
- No credentials, signups, writes to third-party systems, or auth bypasses.
- Every important claim in the integrated report links to a source URL.
- Raw findings are preserved separately from the integrated atlas.
