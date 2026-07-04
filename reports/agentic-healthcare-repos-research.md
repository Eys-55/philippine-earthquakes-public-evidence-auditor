# Agentic Healthcare Repos Research

Date: 2026-07-03

## What This Is

This is the repo-focused version of the earlier agentic healthcare research. The useful pattern is not "healthcare AI apps" in general. The pattern is narrow professional skill repos: one real healthcare or medical-research job, one repeatable workflow, one output artifact.

## Repos We Found

| Repo | What it is | Narrow workflow pattern | Why it mattered for our project |
|---|---|---|---|
| `Aperivue/verify-refs` | Standalone reference-verification skill for medical manuscripts | Verify manuscript references against PubMed and CrossRef; catch fabricated or mismatched citations before peer review | Shows a single-purpose "hero skill" with a clear professional job and audit-only output |
| `Aperivue/check-reporting` | Reporting-guideline audit skill for medical manuscripts | Check STROBE, CONSORT, STARD, PRISMA, TRIPOD+AI, CLAIM, and risk-of-bias items as `PRESENT / PARTIAL / MISSING` | Good model for checklist-based expert review with evidence labels |
| `Aperivue/medsci-skills` | Broader medical-science skills suite | Literature search, reporting-guideline checks, citation checks, statistics, publication figures, and submission support | Useful suite pattern: broad umbrella, but individual skills can stand alone |
| `NVIDIA/digital-health-skills` | Digital-health skills repo for agent-guided healthcare AI workflows | Evaluation, data generation, model adaptation, deployment guidance, and clinical ASR workflows | Shows a specialized healthcare AI skill pack around model improvement and evaluation |
| `FreedomIntelligence/OpenClaw-Medical-Skills` | Large open-source medical AI skills library | Medical/scientific research tasks packaged as reusable skills | Shows scale: many medical skills under one library, but should be filtered for quality before reuse |
| `ajhcs/healthcare-agents` | Portable prompt and `SKILL.md` pack for US healthcare administration | 51 specialist agents for healthcare administration workflows | Closest to healthcare operations: admin agents rather than clinical diagnosis |
| `davila7/claude-code-templates` pydicom skill | A pydicom skill inside a larger Claude Code templates repo | Read, write, anonymize, inspect, and convert DICOM medical imaging files | Shows the "process DICOM files" example: a narrow medical-file workflow, not a broad app |

## The Pattern To Copy

The repeatable structure is:

```text
One painful professional task
-> one SKILL.md
-> one deterministic script if needed
-> one narrow output artifact
-> optional agent wrapper
```

For our own work, the equivalent is not a generic "healthcare agent" or "market research agent." It should be a narrow skill with a concrete job:

- verify references;
- audit reporting guidelines;
- improve clinical ASR;
- process DICOM files;
- generate a referral evidence packet;
- check prior-auth readiness;
- audit a payer-policy packet;
- assess disaster risk for a place.

## What To Borrow

From `Aperivue/verify-refs`:

- audit-only stance;
- clear external databases;
- source-mismatch detection;
- narrow artifact: citation verification report.

From `Aperivue/check-reporting`:

- checklist taxonomy;
- item-level status labels;
- guideline-based review;
- present / partial / missing output structure.

From `Aperivue/medsci-skills`:

- suite-level organization;
- separate hero skills;
- medical research workflow coverage;
- reusable skills across Claude Code, Codex, Cursor, and GitHub Copilot.

From `NVIDIA/digital-health-skills`:

- evaluation-first healthcare AI workflow;
- clinical ASR setup, build, evaluation, and model adaptation;
- model quality metrics rather than vague productivity claims.

From `ajhcs/healthcare-agents`:

- healthcare administration as a safer agentic wedge;
- many specialist roles;
- portable prompt and `SKILL.md` packaging.

From the pydicom skill:

- file-specific medical workflow;
- anonymization and metadata extraction as first-class concerns;
- deterministic tooling around a domain library.

## Cautions

- These repos are examples and patterns, not automatically production-ready healthcare systems.
- Healthcare workflows can touch PHI, clinical safety, payer rules, and regulatory obligations.
- For any PEDGA-related use, prefer no-PHI workflows first.
- Do not copy broad medical-agent behavior into clinical advice.
- Use the "one painful professional task" pattern before building a big app.

## Best Fit For PEDGA

The closest repo pattern for PEDGA is not clinical diagnosis. It is:

```text
Referral / payer / pathway evidence packet skill
```

That would look like:

- input: referral question, source docs, payer or clinic criteria;
- workflow: gather evidence, check completeness, cite gaps, prepare packet;
- output: human-reviewable evidence packet;
- safety: no unsupervised clinical recommendation, no silent PHI expansion.

## Sources Verified

- `Aperivue/verify-refs`: https://github.com/Aperivue/verify-refs
- `Aperivue/check-reporting`: https://github.com/Aperivue/check-reporting
- `Aperivue/medsci-skills`: https://github.com/Aperivue/medsci-skills
- `NVIDIA/digital-health-skills`: https://github.com/NVIDIA/digital-health-skills
- `FreedomIntelligence/OpenClaw-Medical-Skills`: https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills
- `ajhcs/healthcare-agents`: https://github.com/ajhcs/healthcare-agents
- `davila7/claude-code-templates` pydicom skill: https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/scientific/pydicom/SKILL.md
