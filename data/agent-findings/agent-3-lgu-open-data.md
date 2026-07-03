# Agent 3 - Metro Manila / LGU Open Data

Focus: MMDA and Metro Manila LGU sources with public APIs, ArcGIS services,
dashboards, or downloadable data.

## Best Sources

| Source | Access | Metro Manila/NCR method | Notes |
|---|---|---|---|
| Metro Manila GIS Hub | `https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/datasets` | Hub is NCR-scoped | Public Hub is live, but DCAT/feed enumeration was empty locally. |
| MMDA boundary FeatureServer | `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MMDAOAGMP_MetroManilaCityMunicipalityBoundary/FeatureServer/0` | Already NCR-scoped | Core city/municipality geometry. |
| MMDA flood-prone areas | `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/Flood_Prone_Areas_WFL1/FeatureServer/0` | Query `CityMunic` | Site-risk and logistics-risk overlay; historical, not live flood status. |
| MMDA schools | `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MM_Schools/FeatureServer/0` | Query `CITY_MUNIC` | Verified 2,747 features locally. |
| MMDA public establishments | `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/Public_Establishment/FeatureServer/0` | Query `LGU` | Potential POI enrichment; sample records should be quality-checked. |
| QC Open Data Dashboard | `https://quezoncity.gov.ph/program/qc-open-data-dashboard/` | QC-only | Page states datasets from 2019 onward, but access requires QC e-Services login. |
| Makati GIS maps | `https://www.makati.gov.ph/Gismap/Index` | Makati-only | Public app exists; direct ArcGIS JSON endpoint was unreliable in agent check. |

## Live-Check Notes

- MMDA Hub homepage returned HTTP 200 locally.
- ArcGIS org search returned 27 public MMDA Feature/Map services.
- QC dashboard page returned HTTP 200; page text states QC e-Services login is required.

