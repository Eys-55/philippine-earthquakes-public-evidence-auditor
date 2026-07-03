# Disaster Risk Source Research Run

Date: 2026-07-03

This directory preserves the six-agent disaster-data research run that expanded
the repo from a broad Metro Manila data atlas into an address-level disaster
risk source atlas.

The integrated, deduplicated output lives in:

- `data/disaster-risk/disaster-source-atlas.json`
- `data/disaster-risk/local-validation-summary.json`
- `reports/disaster-risk-data-source-atlas.md`

## Agent Lanes

1. `agent-1-official-multihazard.md` - GeoRiskPH, HazardHunterPH, MGB, PHIVOLCS, PAGASA, GeoAnalyticsPH.
2. `agent-2-flood-storm-landslide.md` - Project NOAH, BetterGov, LiPAD, MGB, PAGASA, HDX hydromet layers.
3. `agent-3-earthquake-seismic.md` - PHIVOLCS FaultFinder, ActiveFault, Liquefaction, GroundShaking, Tsunami, volcano services, USGS.
4. `agent-4-metro-manila-local.md` - MMDA ArcGIS, PAGASA FFWS, LGU DRRMO/CDRA pages, flood management project context.
5. `agent-5-global-humanitarian.md` - HDX, OSM/Geofabrik, NASA/JAXA/Copernicus/WorldPop supplemental layers.
6. `agent-6-waste-drainage-proxies.md` - MMDA rivers/flood points, DPWH/BetterGov flood-control projects, LGU waste pages, FOI paths.

## Research Rule

Read-only external access only. Manual, PDF-only, scrape-only, auth-gated, or
weak-proxy sources are separated from clean machine-readable sources.
