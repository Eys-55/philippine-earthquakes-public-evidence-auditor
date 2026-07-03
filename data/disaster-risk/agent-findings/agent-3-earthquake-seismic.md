# Agent 3 - Earthquake, Fault, Liquefaction, Volcanic

## Bottom Line

PHIVOLCS public ArcGIS services are strong enough for an MVP earthquake section:
ActiveFault for nearest-fault distance and Liquefaction for point-in-polygon
exposure. GroundShaking is usable as a supplemental identify-based source after
more validation.

## High-Value Sources

- PHIVOLCS FaultFinder:
  `https://faultfinder.phivolcs.dost.gov.ph/`
- PHIVOLCS FaultFinder information page:
  `https://www.phivolcs.dost.gov.ph/information-tools/the-phivolcs-faultfinder/`
- PHIVOLCS ActiveFault MapServer:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/ActiveFault/MapServer`
- PHIVOLCS Liquefaction MapServer:
  `https://ulap-hazards.georisk.gov.ph/arcgis/rest/services/PHIVOLCSPublic/Liquefaction/MapServer`
- PHIVOLCS GroundShaking MapServer:
  `https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCSPublic/GroundShaking/MapServer`
- PHIVOLCS Tsunami MapServer:
  `https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCSPublic/Tsunami/MapServer`
- PHIVOLCS GeoHazards portal:
  `https://gisweb.phivolcs.dost.gov.ph/gisweb/earthquake-volcano-related-hazard-gis-information`
- HDX Philippines GeoHazards:
  `https://data.humdata.org/dataset/philippines-geohazards-data`
- USGS Earthquake Catalog API:
  `https://earthquake.usgs.gov/fdsnws/event/1/`

## Integration Notes

Use PHIVOLCS ActiveFault and Liquefaction services for automation. Use
FaultFinder as a manual official cross-check. Use USGS only for supplemental
event history, not as the authority for Philippine hazard classification.
