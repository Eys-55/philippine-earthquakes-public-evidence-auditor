# Agent 4 - Transport and Mobility

Focus: GTFS, traffic, roads, public transport, mobility APIs, and mobility-adjacent
layers for Metro Manila/NCR.

## Best Sources

| Source | Access | Metro Manila/NCR method | Notes |
|---|---|---|---|
| TUMI Manila GTFS | `https://hub.tumidata.org/dataset/5dc13962-f732-4a74-959a-dbe44d21ce5e/resource/37dda9a8-b5b6-4b39-a1df-3069fb43e753` | GTFS stops/routes inside NCR bbox | Static GTFS from transport-agency collaboration; download may be slow. |
| Sakay.ph GTFS | `https://github.com/sakayph/gtfs` | GTFS stops/routes inside NCR bbox | Useful route topology archive; service freshness must be validated. |
| MMDA ArcGIS public FeatureServices | `https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/` | NCR-scoped or query by city | Mobility-adjacent rivers/flood/boundary layers; item-level endpoints are more reliable than Hub feed. |
| SafeTravelPH data inventory | `https://www.safetravelph.org/data-inventory` | Request Metro Manila slices | Source discovery/partner lead; not directly open API. |
| Geofabrik Philippines OSM extract | `https://download.geofabrik.de/asia/philippines.html` | Clip/filter roads, rail, waterways in NCR | Strong offline road/POI/network base. |
| Overture Maps transportation | `https://docs.overturemaps.org/guides/transportation/` | Bbox `120.8466,14.2748,121.2269,14.8825` | Cloud-native GeoParquet; useful for comparable road graph data. |
| HOTOSM Philippines roads | `https://data.humdata.org/dataset/hotosm_phl_roads` | Clip country roads to NCR | OSM-derived road dataset through HDX. |

## Live-Check Notes

- TUMI resource page was still loading/slow in local curl validation; use direct ZIP check with timeout before production ingestion.
- SafeTravelPH inventory page returned HTTP 200 locally.
- Geofabrik Philippines page returned HTTP 200 locally.

