# Project Pause Handoff - 2026-07-03

## Current Product Direction

This project is paused as an address-based disaster risk assessor for Metro Manila / NCR. The target product remains:

- input: an address or coordinate;
- process: query official or public hazard/geography sources;
- output: a source-attributed risk packet with official findings first, then clearly labeled screening interpretation.

The immediate working example is Malacanang Palace, Manila.

## Important Working Rule

For flood risk, the report must not invent official scores. Official outputs should be shown as official hazard or susceptibility classifications. Any internal scoring must be labeled non-official and should stay out of formal reports unless explicitly requested.

## Files Added During This Work Session

- `reports/official-flood-risk-assessment-methods.html`
  - Formal flood hazard screening report for Malacanang Palace.
  - Includes official methods, actual site findings, map plates, limitations, and source links.
  - Includes a Google Maps iframe for orientation only, not as a hazard source.
- `reports/assets/malacanang-flood-overview.svg`
  - Derived overview map from queried public geometry.
- `reports/assets/malacanang-waterway-closeup.svg`
  - Derived close-up map showing nearby waterways.
- `reports/assets/malacanang-flood-points.svg`
  - Derived map showing nearby MMDA flood-prone points.
- `data/disaster-risk/malacanang-palace-flood-screening-evidence.json`
  - Structured evidence gathered for the Malacanang Palace flood screening.

These files were still untracked at pause time.

## Malacanang Palace Site Basis

- Place: Malacanang Palace / Malacanang complex, San Miguel, Manila.
- Analysis coordinate: latitude `14.593947`, longitude `120.994349`.
- Address context: Jose P. Laurel Street, San Miguel, Manila.
- Admin boundary result: City of Manila, NCR.
- City PSGC from MMDA query: `PH133901000`.

## Actual Flood-Related Findings Collected

MGB / GeoRiskPH flood susceptibility:

- ArcGIS source: `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/MGBPublic/Flood/MapServer`
- Point-in-polygon result: `fscode=02`.
- Interpretation: Moderate Flood Susceptibility.
- Object ID captured: `121954`.
- Last edited timestamp captured from service: `2025-11-05T02:04:09Z`.

GeoRiskPH / HazardHunterPH live assessment for the same coordinate:

- Flood: `Prone`; `Moderate Susceptibility; 0.5 to 1 meter flood height and/or 1 to 3 days flooding`.
- Storm surge: `Prone`; greater than 2 meter category.
- Liquefaction: High Potential.
- Tsunami: Prone; inundation depth 2 to 2.99 meters.
- Ground shaking: Prone; Intensity VIII.
- Active fault: Safe; approximately 8.1 km west of Valley Fault System: West Valley Fault.
- Active volcano context: approximately 64.5 km north of Taal.

MMDA flood-prone points:

- Query radius: 3 km.
- Records returned: 93.
- Nearest captured record: Magsaysay/Pureza (WB), 2021, amount 0.25 m, approximately 1,381.5 m from the analysis point.
- Repeated nearby cluster: Around Manila City Hall and vicinity, with records in 2019, 2022, 2023, and 2024, approximately 1,405.8 m away.

MMDA river line:

- Query radius: 2 km.
- Features returned: 76.
- Nearest captured waterway: Pasig River, approximately 51.9 m from the analysis point.
- Other nearby waterways: Pasig River segments, Estero de San Sebastian, Estero de San Ibanez.

Project NOAH / BetterGov:

- Source inspected as official/public hazard-map context.
- No point query has been implemented yet in this repo for Malacanang Palace.
- Treat as pending scenario validation, not as a completed site result.

## How Flood Risk Is Being Framed

Use this distinction consistently:

- Flood hazard / susceptibility: the physical likelihood or expected severity at a location under official maps or model scenarios.
- Exposure: the buildings, people, facilities, or services located inside or near the hazard zone.
- Vulnerability: how easily those exposed assets are damaged or disrupted.
- Risk: the combined judgment from hazard, exposure, vulnerability, and confidence.

For this project, official hazard classifications should come first. The product may then add an explicitly labeled expert screening interpretation based on proximity to rivers, local flood-prone records, drainage context, and scenario maps.

## HazardHunterPH Understanding Captured

The HazardHunterPH app was inspected directly at:

- `https://hazardhunter.georisk.gov.ph/map#`

Key implementation details:

- It is a Laravel/PHP web app using Leaflet, Esri Leaflet, AdminLTE/CoreUI, and GeoRiskPH services.
- It supports location assessment by current location, coordinate modal, and map interaction.
- The visible assessment table is primarily populated through GeoRiskPH assessment APIs, not only by client-side ArcGIS layer queries.
- The app obtains runtime config and bearer credentials through its own public web flow. Do not store, print, or commit tokens.
- The main hazard assessment endpoint observed was `https://api.georisk.gov.ph/api/assessments/hazards`.
- The report endpoint pattern observed was `https://ulap-reports.georisk.gov.ph/api/reports/hazard-assessments/{longitude}/{latitude}`.
- Useful app JavaScript files inspected:
  - `https://hazardhunter.georisk.gov.ph/js/indexjs/UseCoordinates.js`
  - `https://hazardhunter.georisk.gov.ph/js/indexjs/ProcessAssessment_v1.2.js`
  - `https://hazardhunter.georisk.gov.ph/js/indexjs/ArcgisServicesHydromet.js`
  - `https://hazardhunter.georisk.gov.ph/js/indexjs/ArcgisServicesSeismic.js`

## Methodology Correction Captured

The generated SVG maps are not official flood maps. They are derived GIS visualizations from queried public layers.

Official flood maps are created through agency workflows such as:

- MGB geohazard assessment and mapping using remote sensing, thematic map interpretation, ground truthing, geomorphology/geology, and local accounts.
- Project NOAH / DREAM hydrologic and hydraulic modeling using elevation/topographic inputs, rainfall return periods, and flood model outputs.
- HazardHunterPH / GeoRiskPH aggregation of official agency hazard layers and assessment services.

## Open Items When Resuming

1. Decide whether the formal report should keep the broad multi-hazard HazardHunterPH results or return to flood-only.
2. Implement a repeatable address-to-coordinate-to-HazardHunterPH workflow without storing tokens.
3. Add Project NOAH point extraction if a reliable local PMTiles or vector query workflow is selected.
4. Convert the Malacanang workflow into the reusable `check-flood-risk` skill under `skills/address-disaster-risk-assessor/`.
5. Add validation docs for data sources, especially freshness, license/terms, access method, and caveats.
6. If reports need scoring, define it as non-official screening and keep it separate from official classification tables.

## Verification To Run Before Commit

```bash
python3 -m json.tool data/disaster-risk/malacanang-palace-flood-screening-evidence.json >/tmp/malacanang-palace-flood-screening-evidence.json
git diff --check
```

For broader repo validation, also run the JSON checks listed in `AGENTS.md`.
