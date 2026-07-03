# Disaster Risk Data Source Atlas

Date: 2026-07-03

## What We Can Build

We have enough public data for a strong Metro Manila **Address Disaster Risk
Assessor** MVP.

The durable MVP should answer:

- Is the address in or near an official flood susceptibility layer?
- Is it close to a known MMDA flood-prone point?
- Is it near a river or mapped waterway?
- Is it inside a PHIVOLCS liquefaction polygon?
- How far is it from the nearest active fault?
- Are landslide, storm surge, or tsunami relevant to this address?
- Are there weak drainage or waste-service signals, clearly labeled as proxies?

It should not claim official certification, engineering adequacy, insurance
eligibility, or waste-management quality without direct evidence.

## Best Machine-Readable Sources

| Rank | Source | Why It Matters | Status |
|---:|---|---|---|
| 1 | [MGBPublic Flood MapServer](https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/MGBPublic/Flood/MapServer) | Official flood susceptibility polygons; live query returned 87,968 features. | active |
| 2 | [PHIVOLCSPublic Liquefaction MapServer](https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/Liquefaction/MapServer) | Official liquefaction polygons; live query returned 239 features. | active |
| 3 | [PHIVOLCSPublic ActiveFault MapServer](https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/ActiveFault/MapServer) | Official active fault lines; live query returned 6,582 features. | active |
| 4 | [MMDA Flood-Prone Areas](https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/Flood_Prone_Areas_WFL1/FeatureServer/0) | Metro Manila-specific historical/local flood-prone points; live query returned 593 features. | active |
| 5 | [MMDA River Line](https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MMDAOAGMP_River/FeatureServer) | Metro Manila river/waterway proximity; live query returned 6,908 features. | active |
| 6 | [Project NOAH Hazard Maps on BetterGov](https://data.bettergov.ph/datasets/22) | Flood, landslide, debris flow, and storm surge package; 2026-04-11 latest version and ODC-ODbL license. | active, large |
| 7 | [HDX Philippines Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-phl) | City/barangay/admin joins; metadata modified 2026-06-24. | active |
| 8 | [OpenStreetMap Philippines via Geofabrik](https://download.geofabrik.de/asia/philippines.html) | Waterways, roads, facilities, and weak service proxies; current bulk extracts. | active |

## Manual Or Reference Sources

- [HazardHunterPH](https://hazardhunter.georisk.gov.ph/) is the official
  multi-hazard reference and cross-check surface, but should remain manual-first
  unless a public API contract is documented.
- [PHIVOLCS FaultFinder](https://faultfinder.phivolcs.dost.gov.ph/) is the
  official fault-proximity user experience. Automate nearest-fault distance with
  the PHIVOLCS ActiveFault layer instead.
- [PHIVOLCS GeoHazards Portal](https://gisweb.phivolcs.dost.gov.ph/gisweb/earthquake-volcano-related-hazard-gis-information)
  is useful for downloadable/manual map products.
- [MMDA GIS Hub](https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/)
  is useful as a catalog, but direct ArcGIS FeatureServer endpoints are more
  reliable for automation.
- LGU DRRMO/CDRA pages, such as the [Quezon City CDRA report](https://quezoncity.gov.ph/wp-content/uploads/2023/08/Quezon-City-CDRA-Report.pdf),
  are useful for local context but are mostly PDF/manual.

## Weak Or Later Sources

Waste-management and drainage-service quality remain weak.

Useful signals exist, but they are proxies:

- MMDA flood-prone points and river proximity can support drainage-risk context.
- [BetterGov flood-control project data discovery](https://data.bettergov.ph/api/v1/datasets?search=flood&limit=10)
  can identify flood-control or drainage project context.
- [DPWH transparency data](https://transparency.dpwh.gov.ph/) and the
  [BetterGov/Hugging Face DPWH mirror](https://huggingface.co/datasets/bettergovph/dpwh-transparency-data)
  can support infrastructure-proxy analysis after field validation.
- [Quezon City sanitation](https://quezoncity.gov.ph/departments/department-of-sanitation-and-cleanup-works-of-quezon-city/)
  and [Pasig services](https://pasigcity.gov.ph/services) pages can show service
  availability, but not reliability.
- FOI request paths, such as [MMDA flood incident and waste-management data](https://www.foi.gov.ph/agencies/mmda/request-for-flood-incident-and-waste-management-data-2018present/),
  may become strong sources if public files are obtained.

The product should emit `supported`, `weak_proxy`, or `unknown` for waste and
drainage service signals. It should not say "bad waste management" from schedules
or OSM absence alone.

## Suggested MVP Pipeline

1. Normalize address and coordinates.
2. Join to NCR/city/barangay using HDX COD-AB or MMDA boundaries.
3. Run point-in-polygon checks:
   - MGB flood susceptibility.
   - PHIVOLCS liquefaction.
   - MGB rain-induced landslide when applicable.
   - Project NOAH PMTiles after schema inspection.
4. Run nearest-distance checks:
   - PHIVOLCS active faults.
   - MMDA flood-prone points.
   - MMDA rivers and OSM waterways.
5. Run coastal/supplemental checks only when relevant:
   - PHIVOLCS tsunami.
   - Project NOAH storm surge.
   - PAGASA live FFWS as current context, not historical risk.
6. Produce a report with confidence grades, source links, and caveats.

## Sample Commands

```bash
curl 'https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/MGBPublic/Flood/MapServer/0/query?where=1%3D1&geometry=120.8,14.3,121.3,14.9&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=true&f=geojson'
```

```bash
curl 'https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/Liquefaction/MapServer/0/query?f=json&where=1%3D1&geometry=120.9842,14.5995&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=lccode,liqcode,province,publishdate,datemapped&returnGeometry=false'
```

```bash
curl 'https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/Flood_Prone_Areas_WFL1/FeatureServer/0/query?f=geojson&where=CityMunic%3D%27Pasig%20City%27&outFields=*'
```

```bash
curl 'https://data.bettergov.ph/api/v1/resources?dataset_id=22&limit=100'
```

## Decision

Build the first reusable product around natural hazards, not generic market
research and not waste-service scoring. The immediate source stack is:

1. MGB flood susceptibility.
2. MMDA flood-prone points.
3. MMDA rivers.
4. PHIVOLCS liquefaction.
5. PHIVOLCS active faults.
6. BetterGov/Project NOAH after PMTiles schema inspection.
7. HDX boundaries.
8. OSM/Geofabrik support layers.

Everything else is a cross-check, manual context, or future candidate.
