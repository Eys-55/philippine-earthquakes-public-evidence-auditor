# Agent 1 - Official Multi-Hazard / GeoRiskPH

## Bottom Line

The strongest official machine-readable surface is the GeoRiskPH ArcGIS REST
stack, especially public MGB and PHIVOLCS layers at
`https://ulap-hazards.georisk.gov.ph/arcgis/rest/services`.

HazardHunterPH and GeoAnalyticsPH are useful official reference tools, but they
should remain manual-first unless a public API contract is documented.

## High-Value Sources

- GeoRiskPH public ArcGIS REST root:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services?f=pjson`
- MGB flood susceptibility:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/MGBPublic/Flood/MapServer/0`
- MGB rain-induced landslide:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/MGBPublic/RainInducedLandslide/MapServer/0`
- PHIVOLCS active faults:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/ActiveFault/MapServer/0`
- PHIVOLCS liquefaction:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/Liquefaction/MapServer/0`
- PAGASA storm surge:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PAGASAPublic/StormSurge/MapServer/0`
- HazardHunterPH:
  `https://hazardhunter.georisk.gov.ph/`
- GeoAnalyticsPH:
  `https://geoanalytics.georisk.gov.ph/`

## Integration Notes

Use public ArcGIS layers for automation. Use HazardHunterPH and GeoAnalyticsPH
as official cross-checks and language sources. Do not bypass account-gated
GeoRiskPH tools such as advanced HazardHunterPH or GeoMapperPH features.
