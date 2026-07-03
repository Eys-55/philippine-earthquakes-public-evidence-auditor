---
name: metro-manila-source-atlas
description: Refresh or extend the ECC-aligned Metro Manila/NCR source atlas with read-only, source-attributed, validated public data sources.
---

# Metro Manila Source Atlas

Use this skill when refreshing the source atlas, adding new data sources,
rerunning a deep dive, or turning validated sources into a scoring prototype.

## Boundaries

- Read-only network access only.
- No signups, credentials, paid actions, scraping behind auth, or terms bypass.
- Prefer machine-readable APIs, ArcGIS services, CKAN APIs, GeoJSON, CSV, ZIP,
  PBF, or documented downloads.
- Keep PDF-only and scrape-only sources separate from clean machine-readable
  sources.
- Preserve raw findings separately from integrated outputs.

## Research Lanes

Run independent lanes before integration:

1. Official statistics: PSA OpenSTAT, PSGC, census, income, prices,
   establishments, regional accounts.
2. Geography and boundaries: PSA PSGC, HDX COD-AB, MMDA boundaries, PSGC/HDX
   crosswalks.
3. Metro Manila and LGU data: MMDA GIS Hub, city dashboards, open data pages.
4. Transport and mobility: GTFS, OSM roads/transit tags, MMDA mobility sources.
5. Business and market proxies: procurement, jobs, real estate, malls, POIs,
   directories.
6. Portal and API infrastructure: BetterGov, HDX CKAN, ArcGIS search, Open Data
   Philippines, Overpass, Geofabrik.

## Source Row Schema

Every inventory row should include:

`name`, `owner`, `coverage`, `data_type`, `access_method`,
`endpoint_or_download_url`, `formats`, `auth_required`, `rate_limits`,
`last_updated_signal`, `freshness_grade`, `Metro Manila filter method`,
`sample_query`, `market_research_use_cases`, `license_or_terms`, `risks`,
`source_url`.

## Validation Checklist

For high-priority sources:

- GET metadata or a lightweight endpoint before deeper calls.
- Confirm Metro Manila coverage through PSGC codes, NCR labels, city names,
  bounding boxes, or spatial joins.
- Record freshness from API metadata, modified timestamps, release dates, or
  response titles.
- Record gating accurately: public, auth-gated, manual-only, commercial, or
  dead.
- Capture at least one sample API/download command when allowed by terms.
- Do not rely on snippets alone for endpoint claims; live-check when feasible.

## Integration And Ranking

Deduplicate by stable source identity first: owner, endpoint, item id, dataset
id, or download URL. Rank by:

- accessibility;
- freshness;
- Metro Manila specificity;
- automation value;
- license clarity;
- market signal quality.

## Current Build Decision

The strongest next artifact is a city-level Metro Manila market scoring
prototype. Use 17 city rows first because current source joins are strongest at
city grain. Move to barangay only after the PSGC/HDX/MMDA/OpenSTAT crosswalk is
validated.

Recommended source order:

`PSGC -> boundary polygons -> PSA denominators -> OSM/MMDA overlays -> proxy sources`

## Required Outputs

Use these paths unless the user requests a different target:

- Raw lane findings: `data/agent-findings/`
- Integrated source inventory: `data/metro-manila-source-atlas.json`
- Validation record: `data/verification-log.md`
- Deep-dive structured evidence: `data/deep-dive/`
- Human-readable synthesis: `reports/`
- Durable decisions: `docs/decisions/`

## Verification Commands

```bash
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
git diff --check
```
