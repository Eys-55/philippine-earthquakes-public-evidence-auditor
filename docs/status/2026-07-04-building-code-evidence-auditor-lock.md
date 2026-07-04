# Building Code Evidence Auditor Progress Lock

Date: 2026-07-04

## Locked Direction

Build an ECC-aligned agentic workflow for Philippine building-code evidence
auditing.

Working name:

**Philippines Building Code Evidence Auditor**

## Current Understanding

The user wants to provide a building, mall, hotel, or establishment in the
Philippines and have an agent scour public sources for evidence related to:

- building-code and structural-code context;
- building permits and occupancy permits;
- owner, operator, developer, contractor, architect, and engineer traces;
- inspection, closure, repair, retrofit, or earthquake-damage history;
- source reliability, freshness, caveats, and missing records.

The workflow must be robust enough to teach and demonstrate agentic workflow
building, not just produce one report.

## Non-Negotiable Boundary

The product is an evidence auditor, not a compliance certifier.

It must not claim:

- the building is legally compliant;
- the building is structurally safe;
- the building is earthquake-safe;
- the building is fit for occupancy;
- a missing public record proves noncompliance.

It may say:

- public evidence was found;
- public evidence was partial;
- no public evidence was found;
- public sources conflict;
- manual OBO/LGU/engineer follow-up is needed;
- the issue is not assessable from public web evidence.

## Current Build Focus

Focus only on Step 1 first: building identity confirmation.

The target user may know very little about the building. They might only have a
hotel name, mall name, booking link, Google Maps link, photo, receipt, nearby
landmark, or rough city. The workflow must first help the user and agent agree
on the exact building before searching permits, contractors, incidents, or code
evidence.

Step 1 output:

- the user's raw clue;
- the best likely building candidate, plus up to two alternates only when there
  is real ambiguity;
- address and jurisdiction confidence;
- whether the target is a whole building, a tenant, a hotel, a mall, or a
  complex;
- a plain-language confirmation prompt;
- a stop gate that blocks the audit until the user confirms.

Confirmation style:

- If the target is obvious, show the best guess and ask for confirmation.
- If there are similar branches, nearby complexes, or tenant/building confusion,
  show at most three options.
- Keep the clarification light and human, for example: "I think you mean this
  one. Just checking, not this other similarly named place, right?"
- Do a small search before asking whenever the clue is searchable, because
  Philippine place names, branches, malls, hotels, and mixed-use buildings can be
  messy.

Current artifact:

- `data/building-code-auditor/building-identity-schema.json`

## ECC Building Blocks

Build in this order:

1. building identity confirmation;
2. repeated job statement;
3. evidence packet schema;
4. regression test cases;
5. skill instructions under `skills/`;
6. source and agent-lane plan;
7. validation script;
8. sample evidence packet;
9. broader scanning workflow.

## Agent Lanes

Recommended first lanes:

- standards lane: PD 1096, IRR, NSCP/ASEP context, accessibility, fire, and
  occupancy context;
- identity lane: exact building identity, address, use type, owner/operator;
- permit lane: building permit, occupancy permit, LGU/OBO and official public
  records;
- contractor lane: developer, contractor, architect, engineer, PCAB/PRC/SEC or
  public traces where sourceable;
- incident lane: earthquake damage, closure orders, retrofits, repair works,
  inspection reports, and news;
- reviewer lane: citation audit, confidence labels, and overclaim prevention.

## Next Concrete Artifacts

- `docs/plans/2026-07-04-building-code-evidence-auditor-design.md`
- `skills/philippines-building-code-evidence-auditor/SKILL.md`
- `data/building-code-auditor/evidence-schema.json`
- `data/building-code-auditor/test-cases.json`
- `scripts/validate_building_code_packet.py`
- `reports/sample-building-code-evidence-packet.md`

## Resume Prompt

If work resumes from this note, start with building identity confirmation. Do not
search permits, contractors, incidents, or code evidence until the user confirms
the exact building.
