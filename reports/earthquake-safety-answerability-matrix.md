# Earthquake Safety Answerability Matrix

Date: 2026-07-05

Verification status: verified with changes from public official sources on
2026-07-05.

This matrix defines the exact evidence rules for a citizen-facing earthquake
safety workflow. The product question is not "can we certify the building is
earthquake-proof?" The product question is:

> Can we answer whether public evidence exists for NSCP/seismic design review,
> OBO structural permit review, latest post-earthquake tag status, and latest
> clearance after a tag or damage event?

Use only `answerable` or `not_answerable`. Do not use partial/weak status labels
in the answerability field.

## 1. NSCP / Seismic Design Evidence

Question: **Is there evidence that this building was designed/reviewed for NSCP
earthquake or seismic requirements?**

| If we find this | Is this enough to answer the question? |
|---|---|
| Target-specific signed and sealed **Structural Design Analysis and Computations**, or **Structural Design, Computation and Seismic Analysis**, prepared by a licensed civil/structural engineer, that identifies NSCP, seismic/earthquake loads, lateral-force/resisting system, load combinations, or equivalent seismic design basis | `answerable` |
| Target-specific signed and sealed **Civil/Structural Documents**, **Civil/Structural Plans**, or **Civil/Structural Designs, Computations, Plans and Specifications** package that includes structural computations/design analysis or is tied to an issued permit record stating NSCP/NBC structural conformity | `answerable` |
| Official OBO/Building Official record, including an issued **Building Permit**, **Civil/Structural Permit**, **Compliance Evaluation Sheet**, technical review/evaluation sheet, or stamped approved plan record, saying the target's civil/structural plans, computations, or specifications were reviewed, approved, accepted, or found conforming for the relevant permit scope | `answerable` |

Not answerable if we only find:

- Boring/Soil Test alone.
- Civil/Structural Plans without computations or OBO approval.
- Building Permit without structural attachments, civil/structural permit
  reference, approved civil/structural documents, review/evaluation sheet, or
  NSCP/NBC conformity language.
- Operator statement that the building is earthquake-ready.
- News article or marketing page.
- Generic NSCP, PD 1096, ASEP, or OBO process page.

Allowed answer if answerable:

> Public evidence was found that the target has NSCP/seismic design-review
> evidence. Report the document name, issuer/custodian, date if available, exact
> target/subscope, and source URL. Do not say earthquake-proof.

## 2. OBO Structural Permit / Review Evidence

Question: **Is there evidence that this building went through official OBO
structural permit or plan-review processing?**

| If we find this | Is this enough to answer the question? |
|---|---|
| Target-specific official OBO-issued **Building Permit**, or official OBO issued-permit registry/certification, that identifies the exact building/subscope and the relevant construction, alteration, repair, renovation, demolition, or structural work scope | `answerable` |
| Target-specific issued, approved, or released **Civil/Structural Permit** or ancillary civil/structural permit record. Application-only forms are not enough unless the record also shows OBO approval, release, or review disposition | `answerable` |
| Target-specific **Compliance Evaluation Sheet**, OBO evaluation checklist, OBO correction/deficiency sheet, **Notice of Disapproval**, or other OBO plan-review record for the building permit or civil/structural scope. Report the stated disposition and do not imply approval unless the record says approved | `answerable` |
| Target-specific **Approved Civil/Structural Plans** or **Approved Plans and Specifications** with OBO/Building Official stamp, approval, release, or official custody evidence | `answerable` |
| Target-specific **Certificate of Occupancy** or **Partial Certificate of Occupancy** that identifies or references the issued Building Permit, issued ancillary permits, approved plans/specifications, or structural scope for the exact building/subscope | `answerable` |

Not answerable if we only find:

- Unified Application Form blank template.
- Permit application requirements page.
- Claim stub or Order of Payment without issued permit/review record.
- Target-specific permit application form, claim stub, Order of Payment, or
  receipt without issued permit, OBO approval, release record, or review
  disposition.
- Certificate of Occupancy that does not identify or reference the relevant
  building permit, ancillary permits, approved plans/specifications, or
  structural scope.
- Business permit.
- Corporate material-permits table that does not attach or quote the OBO record.

Allowed answer if answerable:

> Public evidence was found that the target went through OBO structural
> permit/review processing. Report the exact record and scope. Do not convert
> this into current earthquake safety.

## 3. Latest Post-Earthquake Tag Status

Question: **After a specific earthquake, what is the official tag or inspection
status for this building?**

| If we find this | Is this enough to answer the question? | Answer to the question |
|---|---|---|
| Official **Green Tag**, **INSPECTED / Green placard**, or official clearance/lifting notice for the exact building/subscope after the earthquake | `answerable` | Green / inspected / cleared for use only for the stated scope, date, and authority. Do not convert this into a general earthquake-safe claim |
| Official **Yellow Tag Notice**, **RESTRICTED USE / Yellow placard**, or official restricted-use disposition for the exact building/subscope after the earthquake | `answerable` | Yellow / restricted use; repairs, conditions, or further checks are required before full re-occupancy |
| Official **Red Tag Notice** or official red-tagged status for the exact building/subscope after the earthquake | `answerable` | Red / off limits / unsafe or not safe for occupancy / entry or use prohibited until required assessment, repair, and official clearance |
| Official **Rapid Visual Inspection**, rapid assessment, inspection report, or structural evaluation result that states the building disposition, tag, occupancy restriction, off-limits/no-entry status, unsafe/not-safe-for-occupancy finding, notice to vacate, or required repair/clearance condition | `answerable` | Use the exact disposition stated by the inspecting authority. If no tag/disposition is stated, the question is not answerable |

Not answerable if we only find:

- Reputable news, including reports quoting OCBO, OBO, PICE, LGU, DPWH, or City
  Engineer officials, unless the run can also cite an official source URL,
  document, public post, inspection list, or notice for the exact
  building/subscope.
- News may be used as a lead or corroborating context only; if the official
  tag/status source cannot be retrieved, mark Q3 not answerable from official
  sources and recommend manual OCBO/OBO/LGU/DPWH request.
- Operator says open or business as usual.
- Social media post without official OCBO/LGU/PICE/DPWH attribution.
- Old inspection before the earthquake in question.
- Rapid visual inspection was conducted but no result/tag/status is stated.

Required context when answerable:

- Earthquake date or event.
- Inspection/tag date.
- Issuing authority.
- Exact building or affected portion.
- Tag/status language.
- Restriction or allowed-use language.

## 4. Latest Clearance After Damage Or Tag

Question: **If the building was yellow-tagged, red-tagged, damaged, closed, or
restricted, has it later been officially cleared?**

| If we find this | Is this enough to answer the question? | Answer to the question |
|---|---|---|
| Official **Re-occupancy Clearance** for the exact building/subscope after the damage, restriction, red tag, or yellow tag | `answerable` | Cleared for re-occupancy for the stated scope and date |
| Official updated **Green Tag** after a previous Yellow Tag or Red Tag | `answerable` | Previously restricted/no-entry status was lifted for the stated scope and date |
| Official OCBO/OBO, City Engineer, LGU, DPWH, or OCBO/LGU-adopted PICE-assisted clearance, lifting notice, green-tag update, fit-for-occupancy / fit-for-reoccupancy declaration, or equivalent official notice stating that required repairs, retrofit works, conditions, or safety requirements have been accepted and that entry, use, occupancy, or re-occupancy may resume for the exact building/subscope | `answerable` | Cleared or allowed to resume use according to the authority's stated conditions |
| Official final inspection, certificate of completion, completion report, repair/retrofit acceptance, or compliance certificate for the earthquake repair/retrofit scope, only if issued or accepted by OCBO/OBO/Building Official/DPWH/LGU and it states or is paired with official language allowing occupancy, use, or re-occupancy | `answerable` | Repair or retrofit scope was accepted and occupancy/use/re-occupancy may resume only for the stated scope, date, conditions, and issuing authority |
| Signed and sealed **Structural Stability and Safety Certificate**, **Certificate of Structural Stability**, **Certificate of Structural Soundness and Stability**, or signed/sealed structural stability assessment issued after the earthquake or after repairs, tied to the exact building/subscope | `answerable` | Engineering stability certificate found for the stated date and scope. If no authority clearance accompanies it, say certificate found but official re-occupancy clearance not found |

Not answerable if we only find:

- Repair permit without completion or clearance.
- Retrofit permit without completion or clearance.
- Repair or retrofit permit, approved repair methodology, or construction start
  notice without final inspection, completion acceptance, green tag, clearance,
  or re-occupancy language.
- Notice to Comply, Notice of Non-Compliance, Letter/Notice of Instruction,
  Compliance Report, or generic statement that safety requirements must be
  complied with, unless the authority accepts the compliance and allows use or
  re-occupancy.
- Operator statement that repairs were done.
- Owner/operator/contractor declaration that repairs are complete or the
  building is fit for re-occupancy, unless backed by official OCBO/OBO/LGU/DPWH
  clearance or a signed/sealed engineer certificate with the caveat above.
- Reopening, booking availability, mall hours, or business activity.
- Old green tag before the relevant earthquake or before the latest damage/tag
  event.

Required context when answerable:

- Previous damage/tag/closure event.
- Clearance or certificate date.
- Issuing authority or signing professional.
- Exact building or affected portion.
- Conditions or remaining restrictions.

## Agent Output Shape

Every earthquake-only run should output:

| Field | Meaning |
|---|---|
| `question_id` | One of the four matrix question IDs |
| `evidence_found` | Exact document/status found, or `none` |
| `is_this_enough_to_answer_the_question` | `answerable` or `not_answerable` only |
| `answer_to_the_question` | Required for questions 3 and 4; allowed for 1 and 2 as a short evidence statement |
| `source_url` | Official source URL when available |
| `issuer_or_custodian` | OCBO, OBO, City Engineer, LGU, PICE, DPWH, owner/operator, or engineer of record |
| `document_date` | Inspection, tag, permit, clearance, or certificate date |
| `target_subscope` | Whole building, tower, podium, facade, tenant, wing, parking building, etc. |
| `missing_context` | What prevents the answer from being complete |
| `manual_request_needed` | Exact office or party to request records from |

This makes the agent deterministic: it searches for exact official documents,
then answers only if the found evidence matches the matrix.

## Verification Sources

- [DILG-DPWH-DICT-DTI JMC No. 2018-01](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/89926)
- [Pasay City Building Permit Application PDF](https://pasay.gov.ph/wp-content/uploads/2026/02/pasay-city-external-service-building-permit-application.pdf)
- [Muntinlupa Civil/Structural Permit PDF](https://muntinlupacity.gov.ph/wp-content/uploads/2024/09/Civil-Structural-Permit.pdf)
- [Davao City red/yellow tag announcement](https://davaocity.gov.ph/local-government/davao-city-issues-red-yellow-tags-on-earthquake-affected-buildings/)
- [Davao City tagged buildings compliance notice](https://davaocity.gov.ph/infrastructure-development/ocbo-tagged-buildings-must-comply-with-safety-requirements/)
- [DPWH Department Order No. 027 s. 2023](https://www.dpwh.gov.ph/dpwh/sites/default/files/issuances/do_027_s2023.pdf)
