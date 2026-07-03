# ECC Handoff Summary

Date: 2026-07-03

Use this as the restart point when the project feels overwhelming.

## Current Goal

The repo is now focused on a **Place Disaster Risk Skills** suite.

The core idea:

> People can assess the disaster risk of a place in whatever way they define
> that place.

The place can be:

- an address;
- coordinates;
- a map pin;
- a barangay or city;
- a property listing;
- a drawn or uploaded boundary later.

The project should not be treated as only a web app yet. The current category is
**skill suite**: one suite made of narrow reusable standalone skills.

## Confirmed Checkpoints

### Checkpoint 1: Exact Thing

Build a flexible place-based disaster risk assessor.

### Checkpoint 2: Build Category

Build a skill suite, not a single app/dashboard/report yet.

This follows the pattern of narrow professional skills:

- verify manuscript references;
- audit reporting guidelines;
- improve clinical ASR;
- process DICOM files.

The equivalent here is a disaster-risk suite where each skill has one clear
real-life purpose.

## ECC Workflow Used

The work followed the ECC rules in `AGENTS.md`:

- **Agent-first:** ran parallel research agents for source discovery and then a
  second six-agent disaster-source pass.
- **Security-first:** all external research was read-only; no credentials,
  signups, auth bypass, posting, third-party writes, or paid actions.
- **Plan-before-execute:** first built the atlas, then narrowed it to disaster
  risk, then documented reusable skills.
- **Source attribution:** important source claims are linked in reports and JSON
  rows.
- **Immutability:** raw agent findings were preserved separately from integrated
  outputs.
- **Workflow surface:** reusable workflow lives under `skills/`, not `commands/`.

## Repo Timeline

Recent commits:

- `ee12109 docs: add metro manila data source atlas`
- `2f086e5 docs: add metro manila source deep dive`
- `06ccb97 docs: add ecc repo guidance`
- `727d17a docs: lock disaster risk assessor direction`
- `83dd21e docs: add disaster risk source atlas`

## What Exists Now

### Project Direction

- `README.md` explains the active disaster-risk focus.
- `docs/decisions/0002-lock-address-disaster-risk-assessor.md` locks the repo
  away from broad market scoring and toward disaster risk.
- `docs/plans/2026-07-03-address-disaster-risk-assessor-design.md` describes the
  first address-risk workflow.

### Reusable Skills

- `skills/address-disaster-risk-assessor/SKILL.md` is the current core skill.
- `skills/metro-manila-source-atlas/SKILL.md` is retained for source-atlas
  refreshes.

### Disaster Data Atlas

- `reports/disaster-risk-data-source-atlas.md` is the readable integrated
  disaster-source report.
- `data/disaster-risk/disaster-source-atlas.json` is the ranked machine-readable
  disaster-source inventory.
- `data/disaster-risk/source-priorities.json` is the priority source stack for
  the disaster assessor.
- `data/disaster-risk/local-validation-summary.json` records live endpoint
  validation checks.
- `data/disaster-risk/agent-findings/` preserves the raw six-agent disaster
  research findings.

### Earlier Atlas Foundation

- `reports/metro-manila-data-source-atlas.md`
- `reports/metro-manila-source-deep-dive.md`
- `data/metro-manila-source-atlas.json`
- `data/deep-dive/local-validation-summary.json`
- `data/deep-dive/source-qualification-matrix.json`
- `data/agent-findings/`

These remain useful as background, but the active product direction is disaster
risk.

## Best Data Stack

The strongest first sources are:

1. MGB flood susceptibility.
2. MMDA flood-prone points.
3. MMDA river lines.
4. PHIVOLCS liquefaction.
5. PHIVOLCS active faults.
6. Project NOAH / BetterGov hazard maps.
7. HDX administrative boundaries.
8. OSM / Geofabrik support layers.

Live validation already confirmed:

- PHIVOLCS ActiveFault count: 6,582.
- PHIVOLCS Liquefaction count: 239.
- MGB Flood count: 87,968.
- MMDA Flood-Prone Areas count: 593.
- MMDA River Line count: 6,908.
- BetterGov Project NOAH dataset: active, latest version 2026-04-11.
- BetterGov Project NOAH PMTiles resource: active, 5.55 GB.
- BetterGov flood search: Project NOAH plus Flood Control Projects.
- HDX COD-AB boundaries: active, metadata modified 2026-06-24.

## Weak Areas

Waste-management and drainage-service quality are not strong first-class risk
signals yet.

Use labels only:

- `supported`
- `weak_proxy`
- `unknown`

Do not say an address has "bad waste management" unless there is direct evidence
from complaint data, official performance data, FOI release, or repeated
official incident evidence.

## Possible Standalone Skills

The suite can contain any of these:

1. `assess-place-disaster-risk` - general risk packet for a place.
2. `check-flood-risk` - MGB, NOAH, MMDA flood points, rivers, waterways.
3. `check-earthquake-risk` - active faults, liquefaction, ground shaking.
4. `check-liquefaction-risk` - focused liquefaction exposure check.
5. `check-fault-proximity` - nearest active fault distance.
6. `check-landslide-risk` - MGB/NOAH landslide relevance.
7. `check-storm-surge-tsunami-risk` - coastal storm surge and tsunami exposure.
8. `check-river-waterway-proximity` - waterways, rivers, drains, canals.
9. `check-live-flood-warning` - PAGASA/FFWS live warning context.
10. `generate-risk-card` - short shareable visual risk card.
11. `generate-risk-packet` - full due-diligence report with sources and JSON.
12. `compare-two-places` - compare two candidate locations.
13. `rank-many-sites` - batch rank addresses for site selection.
14. `screen-property-listing` - check real estate listings for hazard issues.
15. `tenant-home-safety-check` - plain-language renter/home buyer check.
16. `business-site-risk-check` - operational risk for shops, clinics,
    warehouses, and offices.
17. `school-hospital-exposure-check` - sensitive-facility exposure workflow.
18. `evacuation-access-check` - road/facility/access context.
19. `source-citation-audit` - verifies every hazard claim has a source.
20. `hazard-data-refresh-check` - re-validates source endpoints.
21. `boundary-normalizer` - converts place input into admin context.
22. `map-layer-inspector` - inspects ArcGIS, PMTiles, and WFS layer schemas.
23. `weak-service-signal-check` - strict waste/drainage proxy checker.
24. `disaster-risk-explainer` - converts technical results to plain language.
25. `insurance-due-diligence-precheck` - non-official screening packet.

The recommended first five are:

1. `assess-place-disaster-risk`
2. `check-flood-risk`
3. `check-earthquake-risk`
4. `generate-risk-packet`
5. `compare-two-places`

## Global Codex Skill Update

The global `goal-operating-system` skill was updated outside this repo to
recognize `skill suite` as a build category.

That update teaches the goal workflow to treat examples like standalone medical
reference verification, reporting audits, clinical ASR, DICOM processing, and
disaster-risk assessment as narrow reusable skills rather than generic apps or
dashboards.

## Do Not Do Yet

- Do not build a generic market-scoring app.
- Do not build a website before the first standalone skills are chosen.
- Do not claim official certification, engineering safety, insurance approval,
  legal advice, or government endorsement.
- Do not scrape gated hazard systems or automate hidden app endpoints.
- Do not overclaim waste or drainage-service quality.

## Next Decision

When resuming, answer this one question:

> Which first three standalone skills should we build from the 25-item list?

Recommended answer:

1. `assess-place-disaster-risk`
2. `check-flood-risk`
3. `check-earthquake-risk`

After that, create a design doc for the first three skills before implementation.

## Verification Commands

Run these before committing future source/data changes:

```bash
python3 -m json.tool data/disaster-risk/source-priorities.json >/tmp/disaster-risk-source-priorities.json
python3 -m json.tool data/disaster-risk/disaster-source-atlas.json >/tmp/disaster-source-atlas.json
python3 -m json.tool data/disaster-risk/local-validation-summary.json >/tmp/disaster-local-validation-summary.json
git diff --check
```
