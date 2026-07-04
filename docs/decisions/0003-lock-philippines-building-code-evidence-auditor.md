# 0003 - Lock Philippines Building Code Evidence Auditor Direction

Date: 2026-07-04

## Status

Accepted

## Context

The user identified a stronger ECC-aligned agentic workflow than a single hazard
API lookup: investigate a Philippine building, mall, hotel, or establishment and
produce a public evidence packet about building-code-related compliance signals.

This direction was motivated by recent earthquake damage in the user's city and
the need for a workflow that can gather, compare, and qualify public evidence
without pretending to perform an engineering inspection.

This does not invalidate the disaster-risk assessor work. It extends the same
public-safety and source-attributed evidence pattern into built-environment due
diligence.

## Decision

The next agentic workflow target is:

**Philippines Building Code Evidence Auditor**

Input:

- building, establishment, mall, hotel, school, hospital, office, or public
  facility name;
- city or province;
- optional address, coordinates, owner, operator, developer, or known incident.

Output:

- source-attributed evidence packet;
- normalized building identity and location confidence;
- public evidence of building permit, occupancy permit, inspection, closure,
  retrofit, repair, or compliance-related records when available;
- public evidence about owner, operator, developer, contractor, architect,
  engineer, or other responsible parties when available;
- relevant standards context, including PD 1096, its IRR, National Structural
  Code context, accessibility/fire/occupancy references, and local OBO/LGU
  process notes where sourceable;
- earthquake damage, closure, repair, retrofit, or public safety incident
  history;
- confidence labels and manual follow-up questions;
- caveats and source URLs.

## ECC Shape

The workflow must be designed as an audit-only ECC skill first:

- workflow surface: `skills/philippines-building-code-evidence-auditor/SKILL.md`;
- raw evidence: `data/building-code-auditor/agent-findings/`;
- schemas and evals: `data/building-code-auditor/`;
- sample packet: `reports/building-code-evidence-packet-*.md`;
- design plan: `docs/plans/2026-07-04-building-code-evidence-auditor-design.md`.

Recommended agent lanes:

- standards lane;
- building identity lane;
- permit and occupancy evidence lane;
- contractor and professional evidence lane;
- incident, damage, retrofit, and inspection lane;
- reviewer and citation-audit lane.

## Safety Boundary

The workflow must not claim that a building is legally compliant, structurally
safe, earthquake-safe, or fit for occupancy unless that exact claim is supported
by authoritative public evidence.

Absence of public evidence is not evidence of noncompliance.

Allowed labels:

- `confirmed_public_evidence`;
- `partial_public_evidence`;
- `not_found`;
- `conflicting`;
- `manual_request_needed`;
- `not_assessable_from_public_web`.

The agent prepares evidence for human review. It does not replace an engineer,
architect, building official, lawyer, inspector, insurer, or local government
authority.

## Consequences

Future work should focus first on robustness artifacts before broad web
scouring:

1. evidence packet schema;
2. test cases and regression set;
3. skill instructions;
4. validation script;
5. one sample building packet;
6. only then broader city-scale scanning.

The previous disaster-risk documents remain valid and reusable, especially for
hazard context, but the current agent-building exercise should prioritize the
building-code evidence auditor unless the user changes direction again.
