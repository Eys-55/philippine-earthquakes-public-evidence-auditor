# Market Research Agent - ECC Instructions

This repo is an ECC-aligned, read-only market research workspace for building a
source-attributed Metro Manila/NCR data atlas and follow-on scoring prototypes.

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

## Current Project Scope

The current geography is Metro Manila / NCR. The current job is source discovery
and validation, not a final market insight report.

Priority sources:

- PSA OpenSTAT and PSGC for official demographic, income, price, establishment,
  and geography attributes.
- HDX, MMDA ArcGIS, and BetterGov for boundaries, GIS layers, and discovery.
- Geofabrik/OpenStreetMap for POIs, roads, and competitor-density primitives.
- PhilGEPS, BSP, real-estate reports, and jobs data as proxy sources only after
  terms, schema, and freshness are validated.

## Validation Standard

For each high-priority source, record:

- reachability and HTTP status;
- access method and format;
- freshness signal;
- Metro Manila relevance method;
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
- `data/agent-findings/` - raw six-agent findings.
- `data/deep-dive/` - structured validation and qualification outputs.
- `docs/decisions/` - durable project decisions.
- `skills/metro-manila-source-atlas/` - reusable ECC workflow for refreshing or
  extending the atlas.

## Verification

Before committing, run:

```bash
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
git diff --check
```

For docs-only changes, JSON parsing and whitespace checks are the required gate.
For future code, add tests before implementation and keep ECC's 80% coverage
target.
