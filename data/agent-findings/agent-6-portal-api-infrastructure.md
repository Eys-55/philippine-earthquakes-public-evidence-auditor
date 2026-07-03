# Agent 6 - Portal and API Infrastructure

Focus: catalog APIs and infrastructure for discovering Metro Manila/NCR datasets.

## Best Sources

| Source | Access | Metro Manila/NCR method | Notes |
|---|---|---|---|
| BetterGov Open Data Portal API | `https://data.bettergov.ph/api/v1/datasets` | Search NCR, Metro Manila, barangay, city names, PSGC | Community-run API; `/api/3` CKAN path did not work, but v1 API is the likely path. |
| Open Data Philippines | `https://data.gov.ph/` and `https://api.data.gov.ph/api/public/dataset/search` | Requires legitimate API access; search NCR terms | Official portal active; public API returned API-key-required in agent check. |
| HDX CKAN API | `https://data.humdata.org/api/3/action/package_search` | Search Philippines/admin/Manila; filter resources | Strong metadata API for humanitarian/geospatial packages. |
| ArcGIS Hub global search API | `https://hub.arcgis.com/api/v3/datasets` | Query Metro Manila/NCR and inspect item metadata | Broad discovery surface; verify authority per item. |
| ArcGIS Online Sharing REST Search | `https://www.arcgis.com/sharing/rest/search` | Use `q`, `bbox`, and `type=Feature Service` | Effective way to discover public ArcGIS layers. |
| MMDA Hub OGC Records | `https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/api/search/v1/collections/dataset/items` | Native NCR site | API responded but returned zero dataset records locally. |
| PHIVOLCS public ArcGIS services | `https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCSPublic?f=pjson` | Intersect layers against NCR | Site-risk and hazard overlays. |
| OSM Overpass and Geofabrik | `https://overpass-api.de/api/interpreter`, `https://download.geofabrik.de/asia/philippines.html` | Bbox/admin clip | Main OSM live/bulk infrastructure. |

## Live-Check Notes

- BetterGov `/api/3/action/package_search` returned 404 locally; use `/api/v1`.
- Open Data Philippines `/api/3/action/package_search` returned the SPA HTML, so it is not CKAN-compatible at that path.
- MMDA Hub OGC/DCAT feed returned an empty dataset list locally.

