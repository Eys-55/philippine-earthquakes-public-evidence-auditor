# Gate 2 Six-Establishment Menu Search

Date: 2026-07-04

This is a Gate 2 learning run for the Philippines Building Code Evidence
Auditor. Six read-only research agents searched all five Gate 2 menu scopes for
six General Santos targets. The purpose is to learn which scopes produce public
evidence, which require manual requests, and where the workflow must block
safety or compliance conclusions.

This is not a compliance audit, structural assessment, engineering inspection,
or safety certification.

## Executive Summary

The menu works, but Gate 2 needs more structure before Gate 3.

- Incident, damage, closure, repair, or retrofit history is the best first live
  scope for five of six targets: KCC/Veranza, SM City General Santos,
  Fitmart/RD Plaza, Gaisano/GMall, and Robinsons GenSan.
- Grand Summit Hotel General Santos is better as a broad public-evidence packet
  first, with incident/damage searched as the first lane inside that packet.
- Robinsons GenSan is the only target with confirmed public permit/occupancy
  evidence from a corporate filing. Other targets mostly expose OBO process
  routes and require manual records requests.
- No target had public web evidence sufficient to say it fulfills the National
  Structural Code of the Philippines or any building-specific structural-code
  compliance standard.
- Generic PD 1096, NSCP, Fire Code, accessibility, and OBO process sources are
  useful context only. They do not prove a named building is compliant, safe, or
  fit for occupancy.

## Consolidated Matrix

Statuses:

- `confirmed_public_evidence`: source-backed public evidence exists for that
  menu scope.
- `partial_public_evidence`: some useful public evidence exists, but it is not
  complete or official enough for the target-specific question.
- `manual_request_needed`: public route exists, but target-specific records must
  be requested from LGU/OBO/BFP/operator or similar custodians.
- `not_assessable_from_public_web`: public web context exists, but the
  target-specific claim cannot be assessed without official or professional
  documents.

| Target | Permit / Occupancy | Incident / Damage / Closure / Repair / Retrofit | Contractor / Professional / Developer / Operator | Standards / Process Context | Broad Packet Readiness | Recommended First Live Scope |
|---|---|---|---|---|---|---|
| KCC Mall of GenSan / Veranza complex | `manual_request_needed` | `confirmed_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | Incident/damage history |
| SM City General Santos | `manual_request_needed` | `confirmed_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | Incident/damage history |
| Fitmart / Fit Mart Gensan / RD Plaza | `manual_request_needed` | `confirmed_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | Incident/damage history |
| Gaisano Mall of GenSan / GMall | `manual_request_needed` | `confirmed_public_evidence` | `partial_public_evidence` | `confirmed_public_evidence` | `partial_public_evidence` | Incident/damage history |
| Robinsons GenSan / Robinsons Place GenSan | `confirmed_public_evidence` | `confirmed_public_evidence` | `partial_public_evidence` | `partial_public_evidence` | `confirmed_public_evidence` | Incident/damage history |
| Grand Summit Hotel General Santos | `manual_request_needed` | `partial_public_evidence` | `partial_public_evidence` | `not_assessable_from_public_web` | `partial_public_evidence` | Broad packet, incident lane first |

## Target Notes

### KCC Mall of GenSan / Veranza Complex

Treat KCC Mall of GenSan and Veranza as one combined test target, but preserve
sublocation ambiguity. Public sources may refer to KCC Mall, Veranza, KCC
Supermarket, the KCC/Veranza entrance, parking, or corporate areas.

Strongest public incident sources:

- [MindaNews June 2026 GenSan quake report](https://mindanews.com/top-stories/2026/06/at-least-11-dead-4-missing-142-injured-in-quake-stricken-gensan/)
- [PNA 2019 KCC corner wall collapse](https://www.pna.gov.ph/articles/1071654)
- [MindaNews 2019 KCC quake damage](https://mindanews.com/top-stories/2019/06/series-of-quakes-damage-gensan-mall/)

Gate 2 lesson: incident history is strong, but target_subscope is mandatory.
Public standards sources did not show target-specific NSCP compliance.

### SM City General Santos

Identity is strong through [SM Supermalls](https://www.smsupermalls.com/mall-directory/sm-city-general-santos/information)
and [SM Prime](https://www.smprime.com/company_releases/sm-prime-to-open-sm-city-general-santos-in-south-cotabato/).
Sublocations include main mall, tenants, supermarket, store, trade hall, cinemas,
and carpark.

Strongest public incident sources:

- [MindaNews 2011 partial work suspension](https://mindanews.com/top-stories/2011/09/after-accident-lgu-partially-suspends-work-at-sm-gensan/)
- [Inquirer 2011 platform-collapse report](https://newsinfo.inquirer.net/119151/7-construction-workers-hurt-as-platform-collapses-in-sm-gensan)
- [GMA 2026 closure report](https://www.gmanetwork.com/news/money/companies/990752/sm-gensan-to-remain-closed-following-mindanao-earthquake/story/)
- [Inquirer 2026 mall suspension report](https://newsinfo.inquirer.net/2242621/mindanao-earthquake-gensan-malls-suspend-operations)

Gate 2 lesson: incident history must separate carpark/construction incidents
from mall-wide earthquake closures.

### Fitmart / Fit Mart Gensan / RD Plaza

Identity is the messiest target. Public sources conflate Fitmart, RD Plaza,
Jollibee Fitmart/RD Plaza, and radio-station floors.

Strongest public incident sources:

- [MindaNews June 2026 quake report](https://mindanews.com/top-stories/2026/06/7-8-magnitude-quake-jolts-general-santos-quake-felt-in-other-parts-of-mindanao/)
- [MindaNews casualty/damage report](https://mindanews.com/top-stories/2026/06/at-least-11-dead-4-missing-142-injured-in-quake-stricken-gensan/)
- [Radyo Natin/DZRH radio-station report](https://www.radyonatin.com.ph/post/commercial-building-housing-dzrh-and-love-radio-collapses-after-magnitude-78-earthquake-in-general-santos-city)
- [PHIVOLCS June 2026 primer](https://www.phivolcs.dost.gov.ph/primer-on-the-08-june-2026-magnitude-mw-7-8-offshore-sarangani-earthquake/)

Gate 2 lesson: this target proves Gate 2 needs a required sublocation lock before
Gate 3. The user or evidence search must distinguish the whole Fitmart/RD Plaza
complex from the Jollibee tenant and the radio-station floor/building.

### Gaisano Mall of GenSan / GMall

Identity is supported by [Gaisano Malls](https://gaisanomalls.com/mall-directory/)
and [Gaisano About Us](https://gaisanomalls.com/about-us/). Sublocations include
entrances, reopened portions, tenants, supermarket/store areas, cinemas, and
reconstruction areas.

Strongest public incident sources:

- [Inquirer 2019 fire report](https://newsinfo.inquirer.net/1178501/firemen-still-battling-gaisano-mall-fire-in-general-santos)
- [Inquirer fire reignition report](https://newsinfo.inquirer.net/1178903/gensan-mall-fire-restarts-6-hours-after-fire-out-declared)
- [PNA fire responders item](https://www.pna.gov.ph/articles/1084102)

Gate 2 lesson: incident history is strong, but current structural status,
rebuilt-area scope, and post-2026 inspection claims remain manual-request items.

### Robinsons GenSan / Robinsons Place GenSan

Identity is strong through [Robinsons Malls](https://robinsonsmalls.com/mall-info/robinsons-place-gensan)
and [Robinsons virtual mall directory](https://vmd.robinsonsmalls.com/list-of-malls/mindanao/robinsons-gen-san).
Do not merge this target with Grand Summit Hotel General Santos or the newer
Palengke Heneral PPP project.

Robinsons is the strongest public permit/occupancy case. A [Robinsons Land 2023
offer supplement](https://robinsonsland.com/sites/default/files/2023-06/RLC%20-%20Final%20Offer%20Supplement%20%28dated%2013%20June%202023%29%20vF.pdf)
lists occupancy permit, certificate of completion, ECC, building permit, and
business permit fields for Robinsons Place Gen San. This is still a company
filing, not a certified LGU record.

Strongest incident sources:

- [Inquirer June 2026 mall suspension report](https://newsinfo.inquirer.net/2242621/mindanao-earthquake-gensan-malls-suspend-operations)
- [Bilyonaryo RLC statement report](https://bilyonaryo.com/2026/06/08/robinsons-land-all-safe-at-general-santos-property-after-7-8-magnitude-quake-mall-closed-for-structural-inspection/property/)
- [AP November 2023 quake report](https://apnews.com/article/philippines-earthquake-mindanao-688f1e3b08854f31e92eaf1fd12e0bcb)

Gate 2 lesson: even when permit-like data exists publicly, certified copies,
approved plans, current inspections, repair/retrofit status, and NSCP compliance
still require manual verification.

### Grand Summit Hotel General Santos

Identity is strong through [Robinsons Hotels](https://robinsonshotels.com/brand/grand-summit-hotels/),
[Grand Summit Hotels](https://grandsummithotels.ph/), and [JG Summit](https://www.jgsummit.com.ph/news/robinsons-hotels-resorts-grand-summit-hotel-opens-in-general-santos-city-20211021).
The strongest address form is Honorio Arriola corner Arradaza Street, Barangay
Lagao, General Santos City. Arrazada appears as a spelling variant.

Strongest sources:

- [Robinsons Hotels brand page](https://robinsonshotels.com/brand/grand-summit-hotels/)
- [RLC 2025 SEC 17-A](https://robinsonsland.com/sites/default/files/2026-04/RLC_SEC%2017-A_December%2031%202025.pdf)
- [GenSan building permit process PDF](https://hrmdo.gensantos.gov.ph/uploads/services/585_2e78b91ca0ad9bc403965dcbb896d2a9.pdf)
- [GenSan occupancy/use process PDF](https://hrmdo.gensantos.gov.ph/uploads/services/591_638e6e72c175bb6feaf0d3d2c99d7091.pdf)

Gate 2 lesson: broad packet first is better here. Identity and
operator/developer evidence are strong, but target-specific permit, occupancy,
inspection, FSIC/FSEC, and post-quake clearance documents were not found
publicly.

## Cross-Target Lessons

### What Actually Produces Public Evidence

- Incident/damage history is the most productive scope for the mall targets.
- Identity and operator/developer context are usually findable.
- General OBO permit/occupancy process routes are findable.
- Robinsons GenSan is the only target where target-specific permit/occupancy
  fields surfaced publicly through a corporate filing.

### What Usually Requires Manual Requests

- Certified building permits.
- Certificates of occupancy.
- Annual inspection records.
- FSIC/FSEC records.
- Post-earthquake OBO or City Engineer inspection reports.
- Red/yellow tag records.
- Repair, retrofit, demolition, or reoccupancy clearances.
- Signed/sealed structural plans, design computations, and professional-of-record
  details.

### NSCP / Structural-Code Lesson

For all six targets, public standards/process sources can be cited as context.
None of the six targets had public web evidence sufficient to conclude that the
target fulfills NSCP or is structurally compliant.

The correct label for target-specific NSCP questions is usually:

`not_assessable_from_public_web`

unless an actual official, permit, inspection, engineering, or signed/sealed
document tied to the target is found.

## Gate 2 Design Changes Recommended

Gate 2 should not only store `locked_scope`. It should also store:

- `target_subscope`: whole mall, hotel building, entrance, tenant, carpark,
  supermarket, RD Plaza building, radio-station floor, etc.
- `timeframe`: 2011 construction, 2019 fire, 2023 quake, June 2026 quake, all
  public history, or user-specified.
- `source_reality_status`: public-searchable, public-process-only,
  manual-request-needed, name-required, or not-publicly-assessable.
- `manual_request_targets`: OBO, BFP, CDRRMO, City Engineer, operator, developer,
  hotel/mall administration, or professional/contractor registry.
- `overclaim_boundary`: what this scope cannot conclude.

This is the main output of the six-agent run: the Gate 2 menu is valid, but the
live locked-scope packet must capture sublocation and source-reality details
before Gate 3 evidence packets are designed.

