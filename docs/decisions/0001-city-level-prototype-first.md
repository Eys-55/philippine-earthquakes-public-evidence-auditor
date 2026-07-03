# 0001 - Build City-Level Prototype Before Barangay Scoring

Date: 2026-07-03

## Status

Accepted

## Context

The atlas and deep-dive pass validated that the strongest clean source groups
are PSA/OpenSTAT, PSGC/HDX/MMDA geography, MMDA ArcGIS layers,
OpenStreetMap/Geofabrik, BetterGov, and related discovery APIs.

These sources support city-level joins better than barangay-level joins. Metro
Manila has 17 cities/municipality rows that can be connected across PSGC, MMDA
city polygons, PSA city or HUC indicators, OSM POI counts, and MMDA flood,
river, and school layers.

Barangay-level scoring is still attractive, but it needs a validated crosswalk
because PSGC 9-digit codes, PSGC 10-digit codes, HDX P-codes, MMDA fields, and
OpenSTAT labels do not line up mechanically.

## Decision

Build the first scoring artifact at city grain:

- 17 Metro Manila city/municipality rows.
- Canonical PSGC normalization.
- MMDA city geometry.
- PSA population, household, income, expenditure, price, and establishment
  indicators where validated.
- OSM POI category counts and competitor-density primitives.
- MMDA school, flood, and river summaries by city.
- Confidence columns for every score component.

Do not start barangay-level scoring until the source crosswalk is validated and
the resulting coverage gaps are measured.

## Consequences

This gets to a usable map or dashboard faster because the data is automatable
now. It also keeps confidence labels honest: city-level scores can be presented
as defensible screening signals, while barangay-level precision remains a later
phase.

The tradeoff is lower spatial precision in the first prototype. That is
acceptable because false precision would be worse than a clear city-level
screening model.
