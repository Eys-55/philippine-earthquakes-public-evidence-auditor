# Agent 1 - Official Statistics

Focus: PSA/OpenSTAT, PSGC, census, income, price, establishment, and regional
accounts sources usable for Metro Manila/NCR market research.

## Best Sources

| Source | Access | Metro Manila/NCR method | Notes |
|---|---|---|---|
| PSA OpenSTAT PXWeb API | `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB` | Use table-specific geolocation values such as NCR or NCR city/HUC rows | Strongest official statistics API backbone; direct PXWeb endpoints respond with JSON metadata. |
| 2020 population and households table | `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO/0011A6DPHH0.px` | `Geographic Location` includes NCR and cities/HUCs | Baseline population and household denominators. |
| 2023 FIES income/expenditure table | `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1E/IE/0011E3ANIE0.px` | Use NCR/HUC geography dimension where available | Affordability, income, expenditure, and savings proxies. |
| Retail prices table | `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/2018NEW/0042M4ARN01.px` | `Geolocation=130000000` for NCR | Consumer basket and food-cost monitoring. |
| Services establishment statistics | `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2D/2022/0012D4BAG00.px` | `Geolocation=1` for NCR in the cited table | B2B sizing by services industry. |
| PSA PSGC/Classifications | `https://psa.gov.ph/classifications-api/psgc` and `https://classification.psa.gov.ph/psgc` | NCR region code `130000000`; official API is tokenized | Canonical geography/code normalization; no polygons. |
| PSA Data Archive | `https://psada.psa.gov.ph/catalog` | Use survey geography variables after approved download | Microdata source discovery; access varies by dataset. |

## Live-Check Notes

- `curl https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB` returned HTTP 200 JSON locally.
- `curl https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1A/PO/0011A6DPHH0.px` returned HTTP 200 JSON metadata locally.
- PSA documentation pages and PSADA catalog returned Cloudflare 403 to plain curl in this environment; treat browser/API access separately.

