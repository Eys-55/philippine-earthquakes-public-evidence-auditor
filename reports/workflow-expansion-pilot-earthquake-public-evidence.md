# Workflow Expansion Pilot: Earthquake / Public Evidence

Generated: 2026-07-05

Query source: `data/agentic-repos/workflow-router.json`, read through the
agent-workflow-project-maker skill.

## Result

The pilot worked. The router narrowed 171 doors down to 8, and the agents found
copy/adapt candidates without crawling the full catalog.

## Door Quality

| Door | Result | Role |
| --- | --- | --- |
| `ahacker-1/cre-agent-skills` CRE Due Diligence plugin pack | strong | direct workflow source |
| `ahacker-1/cre-agent-skills` Due Diligence | strong | direct workflow source |
| `ahacker-1/cre-agent-skills` Document Ingestion | strong | direct workflow source |
| `ahacker-1/cre-agent-skills` Legal | strong | direct workflow source |
| `tinh2/skills-hub-registry` compliance-suite | useful | compliance and permit pattern source |
| `api-evangelist/use-cases` Evidence and compliance vocabulary | useful | taxonomy source |
| `mergisi/awesome-openclaw-agents` USE-CASES | broad | inspiration only |
| `ashishpatel26/500-AI-Agents-Projects` Industry Use Cases | broad | inspiration only |

## Best Candidates

| Rank | Candidate | Source | Fit | Why it matters |
| ---: | --- | --- | --- | --- |
| 1 | Legal & Title Review | `ahacker-1/cre-agent-skills` | copy | Public records, ownership, liens, litigation, zoning, code violations, permits, occupancy certificates, sources, and uncertainty flags. |
| 2 | permit-compliance | `tinh2/skills-hub-registry` | copy | Directly names construction permits, building code, inspections, occupancy, environmental compliance, and jurisdiction caveats. |
| 3 | Document Classifier | `ahacker-1/cre-agent-skills` | copy | Best evidence packet intake pattern: classify documents, find missing pieces, surface conflicts, and force human confirmation. |
| 4 | Environmental Review | `ahacker-1/cre-agent-skills` | copy | Good source taxonomy, public database matrix, hazard context, missing-data protocol, and uncertainty flags. |
| 5 | Physical Inspection Analyst | `ahacker-1/cre-agent-skills` | adapt | Building systems checklist and explicit boundary for structural, seismic, fire/life-safety, and engineering conclusions. |
| 6 | Title & Survey Reviewer | `ahacker-1/cre-agent-skills` | adapt | Exception classification, cross-source validation, survey/title inconsistencies, risk flags, and human review. |
| 7 | Compliance vocabulary | `api-evangelist/use-cases` | copy | Router vocabulary for Search, Aggregation, Transformation, Compliance, Data, Storage, Geolocation, Government, and Real Estate. |
| 8 | Risk Scoring | `ahacker-1/cre-agent-skills` | adapt | Severity labels, risk bands, escalation triggers, mitigation fields, and human materiality review. |

## What This Teaches

The right final catalog should separate:

- `copy`: directly reusable workflow pattern for Codex/ECC.
- `adapt`: useful structure, but needs domain/localization changes.
- `taxonomy`: vocabulary/source classification support.
- `inspiration`: useful idea, not a source of truth.
- `ignore`: unrelated or unsafe for this workflow.

For the earthquake/building evidence workflow, the best path is not a giant
30-agent crawl. It is:

1. Use the router to select the best doors.
2. Expand only those doors.
3. Extract exact workflow patterns.
4. Convert the top copy/adapt candidates into a local ECC workflow contract.

## Recommended Next Step

Build a curated `earthquake-public-evidence-pattern-pack` from the top candidates:

- public-records search and source taxonomy from Legal & Title Review;
- permit/building-code/occupancy taxonomy from permit-compliance;
- evidence packet intake from Document Classifier;
- hazard/source-matrix and uncertainty protocol from Environmental Review;
- human review and professional-boundary language from Physical Inspection and Title & Survey Review.
