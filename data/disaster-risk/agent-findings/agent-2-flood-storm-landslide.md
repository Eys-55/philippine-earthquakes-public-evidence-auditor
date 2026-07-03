# Agent 2 - Flood, Storm Surge, Landslide, Hydromet

## Bottom Line

The best flood/storm/landslide raw material is the Project NOAH hazard package
on BetterGov, the LiPAD/UP DREAM flood layer stack, public MGB hazard services,
and selected PAGASA flood or climate services for context.

## High-Value Sources

- Project NOAH Hazard Maps on BetterGov:
  `https://data.bettergov.ph/datasets/22`
- BetterGov NOAH PMTiles resource:
  `https://huggingface.co/datasets/bettergovph/project-noah-hazard-maps/resolve/main/PMTiles/noah_hazard_maps.pmtiles`
- NOAH site:
  `https://noah.up.edu.ph/`
- LiPAD flood layers:
  `https://lipad-fmc.dream.upd.edu.ph/layers/?keywords__slug__in=flood-hazard-map&limit=100&offset=0`
- LiPAD WFS capabilities:
  `https://lipad-fmc.dream.upd.edu.ph/geoserver/ows?service=WFS&version=1.1.0&request=GetCapabilities`
- PAGASA flood hazard maps:
  `https://www.pagasa.dost.gov.ph/products-and-services/flood-hazard-maps`
- PAGASA rainfall services through GeoRisk portal:
  `https://portal.georisk.gov.ph/arcgis/rest/services/PAGASA/PAGASA/MapServer`
- HDX Philippines tropical cyclone tracks:
  `https://data.humdata.org/dataset/philippines-2024-tropical-cyclone-tracks`

## Integration Notes

BetterGov/NOAH is the cleanest license story among the hazard packages because
the dataset metadata states ODC-ODbL. LiPAD is useful but requires layer-by-layer
license and vintage checks. PAGASA live or forecast sources should not be used
as long-term parcel hazard by themselves.
