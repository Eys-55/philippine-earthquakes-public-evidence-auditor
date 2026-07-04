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

## ECC Building Blocks

Build in this order:

1. repeated job statement;
2. evidence packet schema;
3. regression test cases;
4. skill instructions under `skills/`;
5. source and agent-lane plan;
6. validation script;
7. sample evidence packet;
8. broader scanning workflow.

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

If work resumes from this note, start by designing the evidence packet schema and
the regression test cases. Do not start with broad web scraping.
