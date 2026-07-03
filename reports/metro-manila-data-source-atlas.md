# Metro Manila Data Source Atlas

Date: 2026-07-03

Scope: Metro Manila/NCR machine-readable data sources for repeatable market
research. This is a source atlas, not a market insight report.

## Executive Summary

The strongest first-pass source stack is:

1. **PSA OpenSTAT PXWeb API** for official population, income, price, economic,
   and establishment indicators.
2. **PSGC JSON/API sources** for code/name normalization, with the official PSA
   API/publication as authority and the no-auth GitLab mirror as the practical
   ingestion path.
3. **HDX Philippines COD-AB** and **MMDA ArcGIS FeatureServers** for boundaries,
   schools, floods, rivers, and local GIS overlays.
4. **OSM via Geofabrik/Overpass** for POIs, roads, retail clusters, amenities,
   and competitor mapping.
5. **BetterGov**, **PhilGEPS**, and selected commercial-report APIs for market
   proxy discovery.

The weakest category is LGU open data outside MMDA: QC has a promising dashboard
but requires e-Services login, Makati GIS is public but direct REST access was
unreliable, and many city sources are dashboard/manual rather than clean APIs.

## Ranked Top Sources

| Rank | Source | Status | Why it matters | Source |
|---:|---|---|---|---|
| 1 | PSA OpenSTAT PXWeb API | active | Official market denominators: population, income, prices, sectors, establishments | https://openstat.psa.gov.ph/API-Documentation |
| 2 | PSGC GitLab API mirror | active | No-auth NCR barangay/city code hierarchy for joins | https://psgc.gitlab.io/api/ |
| 3 | HDX Philippines COD-AB | active | Downloadable GeoJSON/SHP/GDB/XLSX admin boundaries | https://data.humdata.org/dataset/cod-ab-phl |
| 4 | MMDA city/municipality boundary FeatureServer | active | Verified 17-feature NCR polygon layer with PSGC fields | https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MMDAOAGMP_MetroManilaCityMunicipalityBoundary/FeatureServer/0 |
| 5 | MMDA ArcGIS FeatureServices | active | Schools, flood-prone areas, rivers, establishments, and local GIS overlays | https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/ |
| 6 | BetterGov Open Data Portal API | active | Community API for dataset discovery and Philippine public data resources | https://data.bettergov.ph/ |
| 7 | Geofabrik Philippines OSM extracts | active | Bulk OSM road/POI/landuse extraction for heavier ETL | https://download.geofabrik.de/asia/philippines.html |
| 8 | OpenStreetMap Overpass API | active | Targeted live POI extraction by Metro Manila bbox/tags | https://wiki.openstreetmap.org/wiki/Overpass_API |
| 9 | TUMI Datahub Manila GTFS | reachable but stale | Static transit feed for route/station catchment analysis | https://hub.tumidata.org/dataset/5dc13962-f732-4a74-959a-dbe44d21ce5e/resource/37dda9a8-b5b6-4b39-a1df-3069fb43e753 |
| 10 | PhilGEPS public procurement endpoints | active | Government demand and supplier-market proxy | https://www.philgeps.gov.ph/ |
| 11 | Santos Knight Frank WordPress report API | active | Metro Manila commercial real-estate proxy via report metadata/PDFs | https://santosknightfrank.com/ |
| 12 | Open Data Philippines | auth-gated | Official catalog lead, but not CKAN-compatible and API appears key-gated | https://data.gov.ph/ |
| 13 | QC Open Data Dashboard | auth-gated | Useful QC program datasets, but requires QC e-Services login | https://quezoncity.gov.ph/program/qc-open-data-dashboard/ |
| 14 | GeoRiskPH PSA Barangay MapServer | reachable but stale | Useful fallback barangay geometry; local check returned 503 and layer is older | https://portal.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer |
| 15 | BSP Physical Network / FSAP | manual-only | Bank/financial-access proxy; public page is live but not clean API | https://www.bsp.gov.ph/SitePages/Statistics/BSPhysicalNetwork.aspx |

Full machine-readable details are in `data/metro-manila-source-atlas.json`.

## Recommended Ingestion Order

Start with the clean, no-auth sources:

1. Pull PSGC NCR barangays from `https://psgc.gitlab.io/api/regions/130000000/barangays.json`.
2. Pull PSA OpenSTAT table metadata for population, income/expenditure, retail prices, and services establishments.
3. Pull HDX COD-AB metadata and download GeoJSON/SHP resources.
4. Pull MMDA boundary, schools, flood, river, and establishment FeatureServer counts/schema before full downloads.
5. Use Geofabrik for bulk OSM extraction; reserve Overpass for small targeted POI checks.
6. Add PhilGEPS and real-estate report metadata as market proxies after terms and rate behavior are reviewed.

## ECC Alignment

- **Agent-first:** six independent research streams were run and archived under `data/agent-findings/`.
- **Security-first:** no credentials, no signup, no auth bypass, no third-party writes.
- **Input validation:** representative endpoints/download pages were live-checked in `data/verification-log.md`.
- **Source attribution:** ranked report rows and JSON entries include source URLs.
- **Immutability:** raw findings were preserved separately from the integrated JSON/report.
- **Workflow surface:** no `commands/` shim was created; if this becomes reusable, the next step should be a `skills/` workflow.

## Main Caveats

- PSA documentation pages may block plain `curl`, but the PXWeb API endpoints validated directly.
- Open Data Philippines is active but not CKAN-compatible at `/api/3/action`; its public API appears key-gated.
- MMDA Hub’s DCAT/OGC dataset feed returned an empty dataset list, while ArcGIS item search and item-level FeatureServers worked.
- Some high-value sources are not clean open APIs: QC Open Data, BSP FSAP, DTI BNRS, SEC APIs, and commercial real-estate reports.
- OSM-derived sources carry ODbL obligations and should be handled carefully in redistributed datasets.
