# Agent 4 - Metro Manila Local / MMDA / LGU

## Bottom Line

The best automatable local data comes from MMDA ArcGIS FeatureServer layers and
PAGASA's Pasig-Marikina-Tullahan operational flood-warning page. Most LGU DRRMO
or CDRA materials are PDFs, service pages, or request workflows.

## High-Value Sources

- MMDA GIS Hub:
  `https://metro-manila-geographic-information-system-hub-mmda.hub.arcgis.com/`
- MMDA ArcGIS Feature Service search:
  `https://www.arcgis.com/sharing/rest/search?f=json&q=orgid:Jlef2HFcOgOf9c7u%20AND%20type:%22Feature%20Service%22&num=30`
- MMDA Flood-Prone Areas:
  `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/Flood_Prone_Areas_WFL1/FeatureServer/0`
- MMDA River Line:
  `https://services1.arcgis.com/Jlef2HFcOgOf9c7u/arcgis/rest/services/MMDAOAGMP_River/FeatureServer`
- PAGASA Pasig-Marikina-Tullahan FFWS:
  `https://pasig-marikina-tullahanffws.pagasa.dost.gov.ph/water/map.do`
- Quezon City CDRA report:
  `https://quezoncity.gov.ph/wp-content/uploads/2023/08/Quezon-City-CDRA-Report.pdf`
- Taguig Peace and Order / DRRMO page:
  `https://www.taguig.gov.ph/peace-and-order/`
- Valenzuela citizen charter:
  `https://valenzuela.gov.ph/files/citizens_charter.pdf`

## Integration Notes

Use MMDA flood-prone points and river lines as first-class local evidence. LGU
pages should be supporting context or request paths, not primary scoring data.
