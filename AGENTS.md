# Address Disaster Risk Assessor - ECC Instructions

This repo is an ECC-aligned, read-only disaster-risk assessment workspace. The
active product is a reusable address-based disaster risk assessor for Metro
Manila / NCR.

## Core Rules

- Agent-first: split broad research into independent source categories before
  integration.
- Security-first: no credentials, no auth bypass, no signup flows, no paid
  actions, and no third-party writes without explicit user approval.
- Plan before execute: define source categories, validation checks, and output
  schemas before collecting or merging data.
- Source attribution: every important claim in reports must cite a source URL.
- Immutability: preserve raw agent findings and validation logs; integration
  outputs should be new files or new rows, not destructive rewrites.
- Workflow surface: put reusable workflows under `skills/` first. Avoid
  `commands/` unless a compatibility shim is explicitly needed.

## ECC Agentic Workflow Contract

Before designing or implementing any new agentic workflow in this repo, route the
work through ECC rather than starting from a topic idea alone.

Define the workflow contract first:

- repeated real-world job: what task will a person run more than once;
- trigger and scope: when the skill should activate and when it should refuse;
- input contract: files, links, addresses, APIs, records, prompts, or other
  inspectable inputs;
- agent lanes: independent source, validation, integration, and review roles;
- tool and action space: narrow read/search/parse/query actions with explicit
  third-party write boundaries;
- raw evidence surface: preserved findings, logs, source responses, and caveats;
- integrated output: report, JSON packet, brief, atlas, dataset, or visual card;
- validation loop: freshness, reachability, source URL, schema checks, and
  expected failure cases;
- safety contract: secrets, auth, paid actions, publishing, and irreversible
  operations are blocked unless explicitly approved;
- reusable skill surface: document the workflow under `skills/<name>/SKILL.md`
  before adding scripts, app surfaces, scheduled runs, or compatibility shims.

Start with input and output only after naming the repeated job. If the repeated
job is vague, clarify that first. If the job is clear, lock the input contract,
then the output artifact, then the agent lanes and validation loop.

## Current Project Scope

The current geography is Metro Manila / NCR. The current job is to turn validated
public hazard and geography sources into an address-in, risk-packet-out workflow.
Generic market research and city scoring are out of scope unless the user
explicitly reopens them.

2026-07-04 update: the user explicitly reopened the project direction for a
new ECC agent-building target: the **Philippines Building Code Evidence
Auditor**. Treat this as the active next workflow unless superseded. The
disaster-risk work remains valid foundation context, but the current build goal
is an audit-only public-evidence workflow for Philippine buildings,
establishments, malls, hotels, and similar facilities.

Priority sources:

- HazardHunterPH / GeoRiskPH for official multi-hazard assessment context.
- Project NOAH / BetterGov hazard layers for flood, landslide, and storm-surge
  zones.
- PHIVOLCS FaultFinder and public hazard services for active fault and
  liquefaction exposure.
- MMDA ArcGIS for Metro Manila boundaries, flood-prone points, rivers, and local
  risk overlays.
- HDX geohazards and administrative boundaries for downloadable geospatial
  fallback data.
- OpenStreetMap / Geofabrik for waterways, roads, access, facilities, and weak
  service-risk proxies.

## Validation Standard

For each high-priority source, record:

- reachability and HTTP status;
- access method and format;
- freshness signal;
- Metro Manila relevance method;
- address or coordinate assessment method;
- license or terms;
- auth/gating status;
- sample query or download command;
- risks and caveats.

Statuses should use: `active`, `reachable but stale`, `manual-only`,
`auth-gated`, `commercial`, or `dead`.

## Repo Map

- `README.md` - project index and artifact map.
- `reports/` - human-readable integrated reports.
- `data/metro-manila-source-atlas.json` - ranked inventory.
- `data/disaster-risk/` - canonical disaster-risk source priorities and future
  assessor outputs.
- `data/agent-findings/` - raw six-agent findings.
- `data/deep-dive/` - structured validation and qualification outputs.
- `docs/decisions/` - durable project decisions.
- `docs/plans/` - product and workflow design documents.
- `skills/address-disaster-risk-assessor/` - active reusable ECC workflow for
  address-based disaster assessment.
- `skills/metro-manila-source-atlas/` - reusable ECC workflow for refreshing or
  extending the foundation atlas.

## Verification

Before committing, run:

```bash
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
python3 -m json.tool data/disaster-risk/source-priorities.json >/tmp/disaster-risk-source-priorities.json
git diff --check
```

For docs-only changes, JSON parsing and whitespace checks are the required gate.
For future code, add tests before implementation and keep ECC's 80% coverage
target.
