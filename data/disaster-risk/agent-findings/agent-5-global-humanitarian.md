# Agent 5 - Global / Humanitarian / Open Data

## Bottom Line

Global and humanitarian sources are strong for boundaries, basemap context,
event history, rainfall, and exposure layers. They are mostly supplemental for
Metro Manila parcel screening because Philippine official hazard layers are more
specific.

## High-Value Sources

- HDX Philippines catalog API:
  `https://data.humdata.org/api/3/action/package_search?fq=groups:phl`
- HDX Philippines administrative boundaries:
  `https://data.humdata.org/dataset/cod-ab-phl`
- HDX HAPI rainfall:
  `https://hapi.humdata.org/api/v2/climate/rainfall`
- HDX PhilSA flood extent example:
  `https://data.humdata.org/dataset/philippines-flood-20250706`
- Geofabrik Philippines OSM extract:
  `https://download.geofabrik.de/asia/philippines.html`
- OpenAerialMap API:
  `http://api.openaerialmap.org/meta`
- NASA GPM IMERG:
  `https://gpm.nasa.gov/data/imerg`
- NASA NRT Global Flood Products:
  `https://www.earthdata.nasa.gov/data/instruments/viirs/near-real-time-data/nrt-global-flood-products`
- NASA LHASA:
  `https://github.com/nasa/LHASA`
- NASA Global Landslide Catalog:
  `https://data.nasa.gov/dataset/global-landslide-catalog-export`
- NOAA CMORPH CDR:
  `https://www.ncei.noaa.gov/products/climate-data-records/precipitation-cmorph`
- JAXA GSMaP:
  `https://sharaku.eorc.jaxa.jp/GSMaP/`
- WorldPop Philippines:
  `https://hub.worldpop.org/geodata/summary?id=6316`

## Integration Notes

Use HDX COD-AB and Geofabrik/OSM in the MVP support stack. Keep NASA, JAXA,
NOAA, Copernicus, and WorldPop as supplemental or future expansion sources
because they are coarser or require additional accounts/workflows.
