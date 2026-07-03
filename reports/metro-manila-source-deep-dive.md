# Metro Manila Source Deep Dive

Date: 2026-07-03

Scope: qualification pass over the top clean sources from the atlas. This moves
the project from "we know these sources exist" to "we know what each source can
actually support."

## Executive Summary

The first buildable artifact should be a **city-level Metro Manila market
scoring prototype**, not a barangay-level model yet.

Reason: the clean sources support city-level joins well. We can combine PSGC,
MMDA city polygons, PSA city/HUC indicators, MMDA risk/facility layers, and OSM
POI counts. Barangay-level scoring is possible later, but it needs a validated
crosswalk because HDX P-codes, legacy PSGC, PSGC 10-digit codes, MMDA codes, and
OpenSTAT labels do not line up mechanically.

## What We Know Now

### PSA / OpenSTAT

[PSA OpenSTAT](https://openstat.psa.gov.ph/API-Documentation) is usable, but
only after table-level validation.

Verified locally:

- Population/households endpoint returns 135 geography values and 3 parameters:
  total population, household population, and number of households
  ([metadata](https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO/0011A6DPHH0.px)).
- Income/expenditure endpoint returns 138 geography values and 3 indicators:
  number of families, average income, and average expenditure
  ([metadata](https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1E/IE/0011E3ANIE0.px)).
- Retail price endpoint uses `Geolocation=130000000` for NCR
  ([metadata](https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/2018NEW/0042M4ARN01.px)).
- Services establishment endpoint uses `Geolocation=1` for NCR and exposes 13
  business data items including establishment count, employment, and revenue
  ([metadata](https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2D/2022/0012D4BAG00.px)).

Deep-dive caveat: some PSA UI-visible table paths can return `404` through a
direct API path. A production collector must fetch metadata first, hash
variables, throttle to PSA's `10 calls / 10 seconds` limit, and keep table-level
fallbacks.

### Geography Stack

Use three geography roles:

- **PSA PSGC**: canonical attribute authority
  ([official API](https://psa.gov.ph/classifications-api/psgc)).
- **HDX COD-AB**: downloadable boundary and humanitarian P-code source
  ([dataset](https://data.humdata.org/dataset/cod-ab-phl),
  [package API](https://data.humdata.org/api/3/action/package_show?id=cod-ab-phl)).
- **MMDA FeatureServer**: practical live NCR city/municipality polygons
  ([GIS Hub](https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/)).

Important caveats:

- PSGC GitLab is useful for no-auth ingestion but is stale versus current PSA.
- HDX admin4 barangay count is not the same as PSA's full barangay universe.
- MMDA city codes use `PH` + legacy PSGC-like strings, but at least Manila needs
  manual validation.
- Preserve both PSGC 9-digit and 10-digit codes. Do not infer 10-digit PSGC by
  appending zeroes.

### MMDA ArcGIS

Production-worthy layers from the
[MMDA Metro Manila GIS Hub](https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/)
and ArcGIS org search
([Feature Service query](https://www.arcgis.com/sharing/rest/search?f=json&q=orgid:Jlef2HFcOgOf9c7u%20AND%20type:%22Feature%20Service%22&num=30)):

| Layer | Count | Geometry | Best Use |
|---|---:|---|---|
| City/municipality boundary | 17 | polygon | city polygons and spatial joins |
| Schools point layer | 2,747 | point | school density and family-demand proxy |
| Flood-prone areas | 593 | point | site-risk / flood-history proxy |
| Rivers line layer | 6,908 | polyline | hydrology and proximity risk |

Use with caution:

- Schools polygon layer is useful but duplicate-ish.
- Public establishments are too sparse to stand alone.
- Incident/MMARAS layers should remain research-only because they are operational
  and potentially sensitive.

### OSM / Geofabrik / Overpass

Use the
[Geofabrik Philippines PBF](https://download.geofabrik.de/asia/philippines-latest.osm.pbf)
as the bulk source for repeatable POI and road ETL. Use
[Overpass](https://overpass-api.de/) only for small live checks and exploratory
counts.

Useful OSM tag families:

- Retail: `shop=*`
- Food: `amenity=restaurant|fast_food|cafe|food_court`
- Health: `amenity=hospital|clinic|doctors|dentist|pharmacy`, `healthcare=*`
- Education: `amenity=school|college|university|kindergarten`
- Transport: `public_transport=*`, `railway=*`, `highway=bus_stop`
- Finance: `amenity=bank|atm`
- Office/B2B: `office=*`

Main risk: OSM data is
[ODbL](https://www.openstreetmap.org/copyright). Internal analysis is fine, but
public redistribution of enriched OSM-derived databases needs careful
attribution/share-alike handling.

### BetterGov / Discovery APIs

[BetterGov](https://data.bettergov.ph/) is stronger than the first atlas
suggested because it has an
[OpenAPI spec](https://data.bettergov.ph/openapi.json), API docs, and typed
endpoints ([docs](https://data.bettergov.ph/docs)):

- `/api/v1/datasets`
- `/api/v1/datasets/{id}`
- `/api/v1/resources`
- `/api/v1/resources/{id}`
- `/api/v1/stats`

Local check against the
[`/api/v1/stats`](https://data.bettergov.ph/api/v1/stats) endpoint found 23
datasets and 432 resources. Its dataset `limit` must be between 10 and 100. It
is useful for source discovery, not necessarily direct market scoring.

Open Data Philippines should stay gated/manual unless official API access is
granted. It is not CKAN-compatible at `/api/3/action`, and the apparent public
API returns "API Key not found" without credentials.

## Recommended Unified Model

Core grain:

`geo_unit + time_period + source_signal`

Core tables:

- `geo_unit`: canonical PSGC region/city/barangay attributes.
- `geo_source_crosswalk`: source-specific codes and names from PSA, PSGC GitLab,
  HDX, MMDA, and OpenSTAT.
- `geo_geometry`: geometry source, CRS, vintage, and quality notes.
- `indicator_value`: PSA/OpenSTAT metrics by geography and time.
- `poi_feature`: OSM and facility features, normalized into market categories.
- `risk_feature`: MMDA flood, river, and related risk overlays.
- `source_monitor`: API/resource health, freshness, schema drift, and gating.

Best join path:

`PSGC -> boundary polygons -> PSA denominators -> OSM/MMDA overlays -> proxy sources`

## Buildable Scoring Models

1. **Retail Catchment Opportunity Score**
   Uses population, households, income/expenditure, OSM retail/food/mall density,
   road access, and competitor density. High confidence at city level.

2. **Site Risk-Adjusted Market Score**
   Starts from opportunity score, then penalizes flood-prone points, river
   proximity, flood susceptibility, and weak access. Medium-high confidence for
   screening, not final site diligence.

3. **Mobility Access Score**
   Uses OSM road classes, transit-adjacent tags, and eventually GTFS if feed
   freshness is confirmed. Medium confidence because OSM roads are strong but
   GTFS freshness is weaker.

4. **B2B / Office Demand Proxy Score**
   Uses services establishments, OSM office/bank amenities, real-estate report
   metadata, and procurement signals. Medium confidence until proxy parsing is
   hardened.

5. **Public Sector Demand Score**
   Uses PhilGEPS buyer/supplier/tender signals. Medium-low confidence until
   stable schema, pagination, and terms are proven.

## What We Cannot Defensibly Score Yet

- Barangay-level income or purchasing power.
- True foot traffic, sales, rent, vacancy, lease rates, or competitor revenue.
- Real-time congestion or commute reliability.
- LGU permitting friction or service quality across all NCR cities.
- Site-level public-sector demand.

## Recommendation

Build the next artifact as a **Metro Manila City Scoring Prototype**:

- 17 city rows.
- MMDA city geometry and PSGC normalization.
- PSA population, household, income, expenditure, price, and establishment
  indicators where validated.
- OSM POI counts by category.
- MMDA school, flood, and river features summarized by city.
- Confidence columns for every score component.

This is the fastest path to a real map/dashboard later because it uses sources
that are actually automatable now.
