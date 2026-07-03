# Agent 5 - Business, Economy, and Market Proxies

Focus: market-signal datasets for establishments, procurement, jobs, real estate,
POIs, and financial access.

## Best Sources

| Source | Access | Metro Manila/NCR method | Notes |
|---|---|---|---|
| PSA OpenSTAT | `https://openstat.psa.gov.ph/PXWeb/api/v1/en/` | Use NCR geography in relevant tables | Official aggregated economic, price, labor, and establishment statistics. |
| PhilGEPS public API/dashboard | `https://api.philgeps.gov.ph/bid/loadRunningBids` | Filter agency/supplier location strings for NCR cities | Procurement demand signal; endpoint stability undocumented. |
| OpenStreetMap Overpass API | `https://overpass-api.de/api/interpreter` | NCR bbox or area; filter tags | POI density, competitors, malls, banks, retail clusters. |
| Geofabrik Philippines OSM extracts | `https://download.geofabrik.de/asia/philippines.html` | Clip to NCR and filter POI tags | Scalable alternative to Overpass for heavier ETL. |
| Santos Knight Frank reports | `https://santosknightfrank.com/wp-json/wp/v2/search?search=Metro%20Manila%20Office%20Market%20Q1%202026` | Already Metro Manila report metadata | WordPress JSON metadata plus PDF reports; report contents are PDF/manual extraction. |
| BSP physical network statistics | `https://www.bsp.gov.ph/SitePages/Statistics/BSPhysicalNetwork.aspx` | Filter workbook rows for NCR/city | Financial access/branch concentration proxy; direct XLS URL not exposed in static HTML. |
| SEC API Marketplace | `https://portal.sec.gov.ph/home/` | Requires known SEC number and account/API access | Entity verification; not a bulk-open source. |
| DTI BNRS statistics | `https://bnrs.dti.gov.ph/resources/bn-statistics` | Dashboard geography filters if available | Business-name registration proxy; machine-readability uncertain. |
| PhilJobNet vacancies | `https://philjobnet.gov.ph/job-vacancies/` | Location strings for NCR/cities | Current labor demand proxy; no documented API. |

## Live-Check Notes

- BSP FSAP/physical-network page returned HTTP 200 locally.
- Overpass returned 406 locally for initial GET/POST attempts; keep as active based on public docs but validate exact query form before pipeline use.
- PhilGEPS and Santos Knight Frank should receive endpoint checks before using in a production scraper.

