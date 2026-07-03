# Agent 6 - Waste, Drainage, Service-Risk Proxies

## Bottom Line

Natural hazards have enough data for a strong MVP. Waste-management quality does
not. The defensible version is a `waste_or_drainage_service_signals` section
with `supported`, `weak_proxy`, or `unknown` labels.

## High-Value Sources

- MMDA Flood-Prone Areas:
  `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/Flood_Prone_Areas_WFL1/FeatureServer/0`
- MMDA River Line:
  `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MMDAOAGMP_River/FeatureServer`
- DPWH Transparency Portal:
  `https://transparency.dpwh.gov.ph/`
- BetterGov DPWH transparency mirror:
  `https://huggingface.co/datasets/bettergovph/dpwh-transparency-data`
- BetterGov flood control dataset discovery:
  `https://data.bettergov.ph/api/v1/datasets?search=flood&limit=10`
- Metro Manila Flood Management Project PDF:
  `https://documents1.worldbank.org/curated/en/099100324190511960/pdf/P1538141e9ead80fe196e812b5eed79f98a.pdf`
- PIA/MMDA pumping station update:
  `https://pia.gov.ph/news/mmda-upgrades-26-pumping-stations-to-combat-metro-manila-flooding/`
- Quezon City sanitation page:
  `https://quezoncity.gov.ph/departments/department-of-sanitation-and-cleanup-works-of-quezon-city/`
- Pasig services page:
  `https://pasigcity.gov.ph/services`
- EMB-NCR Basura Patrol:
  `https://ncr.emb.gov.ph/basurapatrol/`
- MMDA FOI request precedent:
  `https://www.foi.gov.ph/agencies/mmda/request-for-flood-incident-and-waste-management-data-2018present/`
- MMDA historical flood reports FOI:
  `https://www.foi.gov.ph/agencies/mmda/historical-flood-reports-in-metro-manila-2022-to-2025/`

## Integration Notes

Do not say an address has bad waste management unless a complaint dataset,
official performance record, or repeated official incident evidence supports
that specific area. Use flood-prone points, river proximity, DPWH flood-control
projects, and LGU schedules as proxies only.
