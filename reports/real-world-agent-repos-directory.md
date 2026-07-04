# Real-World Agent And Skill Repos Directory

Date: 2026-07-03

## Main Question

How do you identify a real-world problem that can be solved by an agent repo, an agent skill, or a skill suite?

The answer is: look for a repeated professional workflow where the expert already follows a procedure, uses sources or tools, and produces an artifact that can be checked.

Good agent-skill problems usually look like this:

```text
messy real-world input
-> expert procedure
-> tool calls / source checks / file processing
-> structured output artifact
-> human review or approval
```

Bad problems are usually vague, one-off, unverifiable, or too high-stakes to automate without a formal safety process.

## Problem Fit Rubric

Use this before building.

| Criterion | Question to ask |
|---|---|
| Repeated painful task | Does a real person repeat this workflow often enough that packaging it saves time? |
| Structured input | Can the workflow start from files, links, forms, records, APIs, tickets, docs, or inspectable data? |
| Known procedure | Is there a checklist, policy, standard, rubric, protocol, or expert sequence? |
| Toolable steps | Can the agent search, parse, query, run scripts, inspect files, or generate an artifact? |
| Verifiable output | Can success be checked with citations, tests, diffs, scores, status labels, or audit trails? |
| Human decision boundary | Can the agent stop before irreversible, clinical, legal, financial, or customer-facing commitments? |
| Reusable packaging | Can it be written as one `SKILL.md` plus optional scripts, templates, references, and examples? |

If a problem scores well on five or more of these, it is probably worth turning into an agent skill.

## The Pattern

The clean pattern is:

```text
One painful professional task
-> one SKILL.md
-> one deterministic script if needed
-> one narrow output artifact
-> optional agent wrapper
```

Examples:

- "medical research" is too broad.
- "verify manuscript references against PubMed and CrossRef" is a skill.
- "healthcare AI" is too broad.
- "check prior-auth packet completeness against payer criteria" is a skill.
- "geospatial intelligence" is too broad.
- "assess flood susceptibility for one address using official hazard layers" is a skill.

## Directory

| Repo | Domain | Real-world problem | What to study |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Agent skill packaging | Agents need reusable instructions and bundled assets for tasks beyond one prompt | Official examples, folder structure, progressive disclosure |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Skill specification | Agent skills need a portable format across agent systems | Spec, metadata, scripts/assets pattern |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | Directory | Builders need to discover real-world agent skills by category | How repos are categorized and filtered |
| [block/agent-skills](https://github.com/block/agent-skills) | Business/team skills | Teams need portable reusable skills for work | Marketplace/package framing |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Software engineering | Engineering workflows need production-grade agent skills | Verification discipline and process-over-knowledge framing |
| [Aperivue/verify-refs](https://github.com/Aperivue/verify-refs) | Medical manuscript review | Catch fabricated or mismatched citations before peer review | Single-purpose audit-only skill |
| [Aperivue/check-reporting](https://github.com/Aperivue/check-reporting) | Medical manuscript reporting | Check manuscript compliance against reporting guidelines | Checklist status labels and guideline review |
| [Aperivue/medsci-skills](https://github.com/Aperivue/medsci-skills) | Medical research | Literature search, reporting checks, citation checks, stats, publication support | Skill-suite organization with standalone hero skills |
| [NVIDIA/digital-health-skills](https://github.com/NVIDIA/digital-health-skills) | Digital health AI | Evaluate, adapt, and guide healthcare AI workflows including clinical ASR | Metric-driven evaluation workflows |
| [ajhcs/healthcare-agents](https://github.com/ajhcs/healthcare-agents) | Healthcare administration | Package healthcare admin roles and workflows into specialist agents | Admin workflow decomposition |
| [awslabs/hcls-agent-skills](https://github.com/awslabs/hcls-agent-skills) | Healthcare and life sciences | Claims, genomics, imaging, drug discovery, and HCLS workflows need portable skills | Multi-domain regulated-workflow packaging |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | Medical research | Protocol design, data analysis, evidence insights, academic writing | How broad research work is split into modules |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Science and research | Scientific agents need repeatable workflows for databases, computation, and analysis | API/database-backed skill design |
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | Medical AI | Medical AI skills need a large reusable library | Large-scope library structure; verify quality before reuse |
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | Templates and domain skills | Claude Code users need installable templates and domain skill examples | The pydicom skill: a narrow DICOM file-processing workflow |
| [mapbox/mapbox-agent-skills](https://github.com/mapbox/mapbox-agent-skills) | Geospatial product development | Mapbox workflows need product-specific SDK, map, token, and performance guidance | Domain-specific SDK/product constraints |
| [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) | Product management | PM workflows need repeatable templates, phases, and artifacts | How non-coding business workflows become skills |

## What These Repos Teach

### 1. Real-World Agents Start From Work, Not From Models

The best examples do not start with "build an AI agent." They start with a job:

- verify references;
- audit reporting guidelines;
- evaluate clinical ASR;
- process DICOM files;
- run a claims or prior-auth workflow;
- inspect a geospatial source;
- produce a product-management artifact.

Then the repo packages the workflow so an agent can repeat it.

### 2. A Good Skill Has A Clear Done State

Good:

- "A table of references marked verified, mismatch, missing, or uncertain."
- "A reporting checklist with present / partial / missing."
- "A DICOM metadata extract with anonymization status."
- "A flood-risk packet with source citations and caveats."

Weak:

- "Help with healthcare."
- "Analyze the market."
- "Make me productive."

### 3. The Agent Should Not Be The Final Authority

The better repos use an audit, review, or assistive stance. That matters in healthcare, finance, legal, geospatial risk, and any high-consequence domain.

The agent should gather, check, draft, and route. A human should approve sensitive final decisions.

### 4. Scripts Matter

If the same parsing, API lookup, validation, or formatting step happens repeatedly, it should become a script inside the skill. The agent should not improvise every time.

Examples:

- citation lookup script;
- DICOM anonymization or metadata script;
- JSON schema validator;
- map-layer query script;
- checklist scoring script.

### 5. The First Product Is Often A Directory Or Packet

Many useful agentic products are not apps at first. They are:

- directories;
- evidence packets;
- audit reports;
- checklists;
- validated JSON;
- generated docs;
- review queues.

That is why these repos are useful to study: they show how to build an agentic workflow before building a full app.

## Problem Discovery Method

Use this loop to find good agent-skill ideas:

1. Watch someone do real work.
2. Write down every repeated decision, source lookup, file conversion, checklist, and artifact.
3. Ask what part is tedious but still rule-governed.
4. Ask what the output should look like if done correctly.
5. Ask what can be verified automatically.
6. Draw the human approval boundary.
7. Package only that narrow workflow first.

## Quick Test

A problem is probably good for an agent skill if you can complete this sentence:

```text
When I receive [input], I need to check [sources/rules],
perform [steps/tools], and produce [artifact],
but stop before [human decision boundary].
```

Examples:

```text
When I receive a manuscript reference list, I need to check PubMed and CrossRef,
match titles/authors/DOIs, and produce a verification table,
but stop before telling the author the paper is ready to submit.
```

```text
When I receive a referral packet, I need to check payer criteria,
missing documents, diagnosis/procedure evidence, and produce a readiness packet,
but stop before submitting the authorization.
```

```text
When I receive an address, I need to check official hazard layers,
waterway proximity, and local incident points, and produce a cited risk packet,
but stop before claiming engineering safety or official certification.
```

## Recommended Study Order

1. [Aperivue/verify-refs](https://github.com/Aperivue/verify-refs) - cleanest single-purpose example.
2. [Aperivue/check-reporting](https://github.com/Aperivue/check-reporting) - best checklist/audit example.
3. [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) - best engineering craft framing.
4. [NVIDIA/digital-health-skills](https://github.com/NVIDIA/digital-health-skills) - healthcare AI evaluation framing.
5. [ajhcs/healthcare-agents](https://github.com/ajhcs/healthcare-agents) - healthcare admin decomposition.
6. [mapbox/mapbox-agent-skills](https://github.com/mapbox/mapbox-agent-skills) - domain-product workflow framing.
7. [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills) - non-coding workflow packaging.

## Sources

Repo metadata was verified through the GitHub API on 2026-07-03. The machine-readable snapshot is stored in:

- `data/agentic-repos/real-world-agent-repos-directory.json`

Primary source links are the GitHub repositories listed in the directory table above.
