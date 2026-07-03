# Address Disaster Risk Assessor Design

Date: 2026-07-03

## Purpose

Build one reusable workflow: given an address, produce a source-attributed
disaster risk packet. The first version is for Metro Manila / NCR.

This follows the same pattern as narrow professional skills such as medical
reference verification or reporting-guideline audits: one repeated job, one
clear input, one narrow output, deterministic checks where possible, and explicit
limitations.

## User Workflow

1. User provides an address, or coordinates if already known.
2. The assessor normalizes the location and records geocoding confidence.
3. The assessor identifies city and, when reliable, barangay context.
4. The assessor checks relevant hazard layers.
5. The assessor calculates proximity and exposure signals.
6. The assessor emits a risk packet with source links, confidence, and caveats.

## First Risk Classes

- Flood exposure from hazard zones and MMDA flood-prone points.
- Historical local flood signal from MMDA flood-prone records.
- River or waterway proximity from MMDA river layers and OSM where appropriate.
- Liquefaction exposure from PHIVOLCS public hazard services.
- Active fault proximity from PHIVOLCS FaultFinder or geohazard files.
- Landslide and storm-surge relevance from Project NOAH / GeoRiskPH / HDX when
  the layer applies to the address.

## Later Or Weak Risk Classes

Waste management, drainage maintenance, and local service reliability are not
first-class MVP signals yet. They can be added only after validating a clean
source or a defensible proxy, such as official LGU collection schedules,
complaint datasets, sanitation facilities, drainage incidents, or OSM waste and
waterway tags.

## Data Sources

Priority source list lives in `data/disaster-risk/source-priorities.json`.

The first source stack:

- HazardHunterPH / GeoRiskPH for official multi-hazard context.
- Project NOAH hazard maps through BetterGov for flood, landslide, and storm
  surge zones.
- PHIVOLCS FaultFinder and public ArcGIS services for active faults and
  liquefaction.
- MMDA ArcGIS layers for Metro Manila boundaries, flood-prone points, and rivers.
- HDX geohazards and boundaries for downloadable fallback layers.
- OSM / Geofabrik for waterways, roads, access, and weak service proxies.

## Output Shape

Each risk packet should include:

- `input_address`
- `normalized_address`
- `coordinates`
- `geocode_confidence`
- `city`
- `barangay`
- `overall_risk_label`
- `risk_components`
- `source_links`
- `data_gaps`
- `limitations`
- `generated_at`

Every component should carry:

- risk label;
- raw evidence;
- distance or overlap method;
- source URL;
- freshness signal;
- confidence grade.

## ECC Guardrails

- Read-only research and data access.
- No credentials or auth bypass.
- No claim of official certification.
- Source attribution for every important claim.
- Preserve raw source checks separately from integrated packets.
- Use `skills/` first for reusable workflow logic.

## First Build Target

Create the `address-disaster-risk-assessor` skill and then implement a prototype
that can produce one Metro Manila address risk packet from manually supplied
coordinates. Address geocoding can be added after the risk-layer pipeline is
stable.
