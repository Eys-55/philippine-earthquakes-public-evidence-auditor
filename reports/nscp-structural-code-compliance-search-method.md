# NSCP Structural-Code Compliance Search Method

Date: 2026-07-05

This is the working method for learning how to search National Structural Code
of the Philippines (NSCP) and structural-code compliance evidence in the
Philippines Building Code Evidence Auditor.

The main lesson is strict: public web search usually cannot prove that a named
building complies with NSCP. It can find context, target identity, incident
history, permit-process routes, and sometimes indirect permit fields. A
target-specific NSCP or structural-code claim needs official or professional
documents tied to the exact building, subscope, and timeframe.

This method is not a structural assessment, engineering inspection, legal
opinion, safety certification, or final compliance audit.

## What Counts

Strongest evidence is target-tied and document-based:

- OBO-issued building permit or certified true copy.
- Civil/structural ancillary permit.
- Certificate of occupancy.
- OBO evaluation sheet or plan-review record.
- Signed and sealed structural plans.
- Signed and sealed structural design analysis or computations.
- Structural stability certificate.
- Official post-earthquake structural assessment, rapid visual assessment,
  red/yellow tag, closure order, reoccupancy clearance, repair permit, retrofit
  permit, or demolition permit.
- Court, procurement, or regulatory filing that attaches or quotes
  target-specific engineering or permit records.

Strong indirect evidence can support a partial packet but not final NSCP
compliance:

- SEC, bond, or annual-report filings listing target-specific permit,
  occupancy, completion, ECC, or business-permit fields.
- Official LGU, BFP, CDRRMO, City Engineer, DPWH, court, PIA, or PNA text
  referencing target-specific inspection, clearance, repair, or closure.
- Operator or developer statements naming structural inspection, closure, repair,
  reopening condition, or professional review for the exact target.

Generic context is useful, but it is not building-specific proof:

- PD 1096 / National Building Code context.
- NSCP / ASEP / PRC professional-standard context.
- Fire Code, accessibility, green-building, and OBO/BFP process pages.
- LGU permit requirements and citizen charters.

Weak leads stay weak unless corroborated:

- Social posts, snippets, photos, videos, store locators, mall hours, reopening
  posts, booking availability, and tenant pages.
- Contractor, architect, engineer, developer, or portfolio pages that do not tie
  the professional or firm to the exact building and regulated document set.

## Source Basis

The Association of Structural Engineers of the Philippines describes ASEP as a
recognized structural-engineering organization and identifies the National
Structural Code volumes as ASEP publications and approved referral codes of the
National Building Code. Source: [ASEP About](https://aseponline.org/about/).

The PRC Board of Civil Engineering Resolution No. 17, available through the
Supreme Court E-Library, adopted NSCP provisions as part of rules and
regulations governing civil engineering practice and states that civil
engineering plans, design analysis, specifications, reports, studies,
investigations, and related documents should bear the civil engineer's signature,
license number, dry seal, and current-registration expiration date. Source:
[PRC Board Resolution No. 17](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/11/42784).

DILG-DPWH-DICT-DTI Joint Memorandum Circular No. 2018-01 sets national process
context for building permits and certificates of occupancy. It defines building
permits as documents issued by the Building Official after plans,
specifications, and other pertinent documents are found satisfactory and
substantially conforming with the National Building Code and IRR. It also lists
certificate-of-occupancy requirements including completion documents, approved
plans/specifications, issued building and ancillary permits, FSEC-related
documents, professional licenses, and inspection processes. Source:
[JMC 2018-01](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/89926).

General Santos OBO requirements expose the local process route for the current
six-establishment learning set. The requirements mention civil/structural permit
forms, structural design analysis and computation, approved structural plans,
structural stability certificates for buildings 15 years or older, and repair or
renovation attachments. Source:
[General Santos OBO building requirements](https://www.filipizen.com/partners/gensan_gensan/obo/requirement/building).

These sources explain what documents matter. They do not prove a named mall,
hotel, or other establishment is NSCP-compliant.

## Search Workflow

1. Lock identity and subscope.

   Confirm the exact building, complex, wing, tower, tenant, carpark, entrance,
   or hotel structure. Capture aliases, city, barangay, address, operator, and
   timeframe. If the user says a whole mall or complex, store that explicitly.

2. Search OBO and permit routes first.

   Look for LGU/OBO pages, citizen charters, permit portals, certified-copy
   routes, and building-permit requirements. Search for building permit,
   civil/structural permit, certificate of occupancy, structural stability
   certificate, approved plans, design computation, repair permit, renovation
   permit, and occupancy inspection report.

3. Search filings and operator documents.

   Search SEC filings, annual reports, offer supplements, official developer
   PDFs, and operator documents. Extract only target-tied fields. Treat filings
   as partial public evidence unless they attach certified records.

4. Search official incident and inspection context.

   Search OBO, BFP, CDRRMO, City Engineer, DPWH, PIA, PNA, courts, and
   reputable news for earthquake damage, fire, collapse, closure, repair,
   retrofit, red/yellow tags, inspection, and reoccupancy. Separate incident
   evidence from current structural-code compliance.

5. Search professional and contractor leads only after a lead exists.

   PCAB, PRC, contractor, architect, engineer, and portfolio sources can verify
   identities or project leads. They do not prove target compliance unless they
   connect to signed/sealed target records or official permit/inspection
   documents.

6. Classify and write the overclaim boundary.

   If only standards or process context is found, use
   `not_assessable_from_public_web` or `manual_request_needed`. Do not infer
   compliance or noncompliance.

## Query Templates

Use these with the exact target name, aliases, city, and subscope:

- `"{target}" "NSCP"`
- `"{target}" "National Structural Code"`
- `"{target}" "structural code"`
- `"{target}" "structural stability certificate"`
- `"{target}" "signed and sealed" structural`
- `"{target}" "structural design analysis"`
- `"{target}" "design computation"`
- `"{target}" "building permit"`
- `"{target}" "civil/structural permit"`
- `"{target}" "occupancy permit"`
- `"{target}" "certificate of occupancy"`
- `"{target}" "certificate of completion"`
- `"{target}" "FSEC"`
- `"{target}" "FSIC"`
- `"{target}" "structural assessment"`
- `"{target}" "earthquake" "inspection"`
- `"{target}" "red tag"`
- `"{target}" "yellow tag"`
- `"{target}" "repair permit"`
- `"{target}" "retrofit"`
- `site:gensantos.gov.ph "{target}" "OBO"`
- `site:gensantos.gov.ph "{target}" "building permit"`
- `site:robinsonsland.com "{target}" "occupancy permit"`
- `site:smprime.com "{target}" "building permit"`
- `site:elibrary.judiciary.gov.ph "National Structural Code"`
- `site:dpwh.gov.ph "National Structural Code" "building permit"`

## Classification Rubric

`confirmed_public_evidence`

Use only when a target-tied official or professional document is public and
directly supports the record type being reported. Minimum fields are target
identity, issuer or professional of record, document type, date or validity
signal, and subscope match.

`partial_public_evidence`

Use when public target-tied evidence exists, but it is indirect, incomplete,
dated, uncertified, or insufficient for a target-specific NSCP compliance claim.
Example: a corporate filing lists permit fields, or a news report quotes an
official closure without publishing the inspection record.

`manual_request_needed`

Use when a public process or record custodian is identifiable but the
target-specific document is not public. Typical custodians are OBO, BFP,
CDRRMO, City Engineer, owner, operator, developer, contractor, architect, or
civil/structural engineer of record.

`not_assessable_from_public_web`

Use when only generic standards/process context or weak leads exist for a
target-specific NSCP or structural-code claim.

`not_found`

Use only when reasonable search found no target-tied evidence and no useful
manual process route. Prefer `manual_request_needed` when a plausible OBO, BFP,
operator, developer, or professional custodian exists.

## Manual Request Checklist

For any target-specific NSCP or structural-code question, ask the relevant
custodian for:

- Building permit.
- Civil/structural permit form.
- Approved structural plans.
- Structural design analysis and computations.
- Technical specifications.
- Certificate of completion.
- Certificate of occupancy.
- FSEC and FSIC.
- Occupancy or annual inspection report.
- Structural stability certificate.
- Post-earthquake inspection or structural assessment.
- Red tag, yellow tag, reoccupancy clearance, or closure order.
- Repair, renovation, retrofit, demolition, or amendatory permit.
- OBO evaluation sheet or plan-review record.
- Names and license details of involved professionals of record.

## Gate Changes

Gate 2 and Gate 3 packets should include these fields before the auditor tries a
target-specific NSCP conclusion:

- `target_subscope`
- `timeframe`
- `source_reality_status`
- `nscp_evidence_status`
- `evidence_grade`
- `manual_request_targets`
- `manual_documents_needed`
- `overclaim_boundary`

For the six General Santos establishments, the working conclusion remains:

`not_assessable_from_public_web`

No target had public web evidence sufficient to confirm NSCP or structural-code
compliance. The right next step is a manual OBO/BFP/operator/professional record
request or a professional engineering review, depending on the exact claim.
