# Metro Manila Data Source Atlas

ECC-aligned source atlas for Metro Manila/NCR market research.

The project tracks machine-readable data sources: public APIs, CSV/GeoJSON/ZIP
downloads, ArcGIS services, CKAN-style portals, and actively maintained datasets.

## Artifacts

- `reports/metro-manila-data-source-atlas.md` - decision-ready integrated report.
- `reports/metro-manila-source-deep-dive.md` - qualification pass over the strongest buildable sources.
- `data/metro-manila-source-atlas.json` - machine-readable ranked inventory.
- `data/source-schema.json` - row schema for source inventory entries.
- `data/verification-log.md` - live checks performed during source validation.
- `data/deep-dive/local-validation-summary.json` - structured record of live checks for the deep dive.
- `data/deep-dive/source-qualification-matrix.json` - build-readiness matrix for the strongest source groups.
- `data/agent-findings/` - raw findings from the six parallel research streams.
- `docs/decisions/0001-city-level-prototype-first.md` - accepted decision to build city-level scoring before barangay scoring.
- `skills/metro-manila-source-atlas/SKILL.md` - reusable ECC workflow for refreshing or extending the atlas.

## Current Build Direction

The next build should be a city-level Metro Manila market scoring prototype:
17 city rows, PSGC normalization, MMDA geometry, PSA indicators, OSM POI counts,
MMDA risk/facility summaries, and confidence columns for every score component.

Barangay-level scoring is intentionally deferred until PSGC, HDX, MMDA, and
OpenSTAT crosswalks are validated.

## Verification

```bash
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
git diff --check
```

## ECC Boundaries

- Research is read-only.
- No credentials, signups, writes to third-party systems, or auth bypasses.
- Every important claim in the integrated report links to a source URL.
- Raw findings are preserved separately from the integrated atlas.
