# Verification Log

Date: 2026-07-03

Mode: read-only live checks from `/Users/acecanacan/Documents/market-research-agent`.

## Successful Checks

| Check | Result | Use |
|---|---:|---|
| `curl https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB` | HTTP 200 JSON, 1,381 bytes | Confirms OpenSTAT API root is live. |
| `curl https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO/0011A6DPHH0.px` | HTTP 200 JSON, 3,968 bytes | Confirms population table metadata is live. |
| `curl https://psgc.gitlab.io/api/regions.json` | HTTP 200 JSON, 2,232 bytes | Confirms PSGC mirror root list is live. |
| `curl https://psgc.gitlab.io/api/regions/130000000/barangays.json` | HTTP 200 JSON, 452,604 bytes | Confirms no-auth NCR barangay hierarchy. |
| `curl https://data.humdata.org/api/3/action/package_show?id=cod-ab-phl` | HTTP 200 JSON, 15,768 bytes | Confirms HDX COD-AB package and downloadable resources. |
| `curl https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/` | HTTP 200 HTML, 56,000 bytes | Confirms MMDA Hub is live. |
| ArcGIS org search for `orgid:Jlef2HFcOgOf9c7u` | HTTP 200 JSON, 27 services | Confirms public MMDA ArcGIS service inventory. |
| MMDA boundary layer metadata | HTTP 200 JSON; fields include `RegionPSGC`, `CityMunicipalityPSGC` | Confirms usable NCR boundary schema. |
| MMDA boundary count query | HTTP 200 JSON count `17` | Confirms city/municipality feature count. |
| MMDA schools count query | HTTP 200 JSON count `2747` | Confirms facility layer responds. |
| QC Open Data Dashboard page | HTTP 200 HTML | Confirms page is live; page text states QC e-Services login requirement. |
| SafeTravelPH data inventory | HTTP 200 HTML | Confirms page is live but not directly API-backed. |
| Geofabrik Philippines page | HTTP 200 HTML | Confirms OSM extract page is live. |
| BSP financial service access page | HTTP 200 HTML | Confirms BSP page is live. |

## Caveats / Failed Checks

| Check | Result | Interpretation |
|---|---:|---|
| `https://openstat.psa.gov.ph/API-Documentation` via plain curl | HTTP 403 Cloudflare page | Documentation page blocks plain curl; API endpoints still work. |
| PSA PSGC documentation/publication pages via plain curl | HTTP 403 Cloudflare page | Browser/source access is documented, but plain curl is blocked in this environment. |
| PSADA catalog via plain curl | HTTP 403 Cloudflare page | Treat as browser/request workflow, not clean API ingestion. |
| GeoRiskPH Barangay MapServer layer metadata | HTTP 503 | Keep as monitored fallback rather than primary boundary source. |
| BetterGov `/api/3/action/package_search` | HTTP 404 JSON | BetterGov is not CKAN-compatible at that path; use `/api/v1`. |
| Open Data Philippines `/api/3/action/package_search` | HTTP 200 SPA HTML | Portal is not CKAN-compatible at that path. |
| MMDA Hub DCAT feed | HTTP 200 JSON with empty dataset array | Use ArcGIS org/search/item endpoints instead of relying on DCAT feed. |
| Overpass initial GET/POST checks | HTTP 406 | Query formatting/client issue; use documented Overpass syntax and consider Geofabrik for bulk ETL. |
