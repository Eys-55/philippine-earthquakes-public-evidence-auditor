# Agent 2 - Geospatial Boundaries

Focus: boundary polygons, spatial joins, PSGC-compatible geometries, and ArcGIS
layers for Metro Manila/NCR.

## Best Sources

| Source | Access | Metro Manila/NCR method | Notes |
|---|---|---|---|
| HDX Philippines COD-AB | `https://data.humdata.org/api/3/action/package_show?id=cod-ab-phl` | Filter `adm1_pcode=PH13` or NCR admin name | Strongest downloadable boundary bundle; exposes SHP, GeoJSON, GDB, XLSX resources. |
| MMDA city/municipality boundary FeatureServer | `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MMDAOAGMP_MetroManilaCityMunicipalityBoundary/FeatureServer/0` | Already NCR-scoped; fields include `CityMunicipalityPSGC` | Verified 17 features locally. |
| GeoRiskPH PSA barangay MapServer | `https://portal.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer/4` | Query by NCR region fields or PSGC prefix | Useful but older and returned 503 locally; monitor as fallback. |
| ArcGIS Online Philippines Admin 4 FeatureServer | `https://services3.arcgis.com/16nyMR1mdhEaLG41/ArcGIS/rest/services/Philippines_Admin_4/FeatureServer/0/query` | `ADM1_EN='National Capital Region (NCR)'` | Fast barangay lookup; provenance is less authoritative than HDX/PSA. |
| PSGC GitLab mirror | `https://psgc.gitlab.io/api/` | `https://psgc.gitlab.io/api/regions/130000000/barangays.json` | No-auth JSON code/name hierarchy; verified NCR barangay payload locally. |
| Geofabrik Philippines OSM extracts | `https://download.geofabrik.de/asia/philippines.html` | Clip national extract to NCR | Daily OSM road/POI/boundary extract; ODbL obligations apply. |

## Live-Check Notes

- HDX package API returned HTTP 200 and resource URLs for GeoJSON/SHP/GDB/XLSX.
- MMDA boundary layer returned HTTP 200 metadata and `returnCountOnly` count `17`.
- GeoRiskPH barangay layer returned HTTP 503 locally during validation.

