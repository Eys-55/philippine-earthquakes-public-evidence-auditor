# 0002 - Lock Project To Address Disaster Risk Assessment

Date: 2026-07-03

## Status

Accepted

## Context

The repo started as a Metro Manila data source atlas for broad market research.
The strongest reusable product direction is narrower: an address-based disaster
risk assessor.

This better matches the validated data. The source atlas already includes
MMDA flood-prone points, rivers, city boundaries, geography joins, BetterGov,
HDX, and ArcGIS discovery surfaces. Additional public hazard sources identified
for the assessor include HazardHunterPH / GeoRiskPH, Project NOAH hazard maps,
PHIVOLCS FaultFinder, PHIVOLCS liquefaction services, and HDX geohazard files.

Natural-hazard assessment has enough public data for an MVP. Waste-management
or drainage-service quality is weaker and should remain a later optional signal
unless a clean source or defensible proxy is validated.

## Decision

This repo will focus on one reusable product:

**Address Disaster Risk Assessor**

Input:

- address string, plus optional known coordinates;
- optional property/use type, such as home, clinic, retail, school, warehouse,
  or office.

Output:

- source-attributed disaster risk packet;
- normalized location and confidence;
- flood exposure;
- historical flood-prone signal;
- river or waterway proximity;
- liquefaction exposure;
- active fault proximity;
- landslide or storm-surge relevance where data supports it;
- weak-service proxy section for waste/drainage only when evidence is available;
- limitations and non-certification disclaimer.

## Non-Goals

- Do not build a generic market scoring model.
- Do not claim engineering, insurance, legal, or official government
  certification.
- Do not bypass gated hazard systems or scrape where terms disallow automation.
- Do not invent risk precision when a layer is stale, low-resolution, or
  manually sourced.

## Consequences

The previous market-source atlas remains useful as source inventory and
geospatial foundation. Future skills, agents, reports, and schedules should
serve the address disaster risk assessor unless the user explicitly changes the
project direction.

The first implementation should be Metro Manila / NCR only, because MMDA and the
current atlas already provide practical local layers. Nationwide support can come
later after the hazard and boundary sources are validated outside NCR.
