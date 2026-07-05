# Workflow Router Table Revamp Sample

Generated: 2026-07-05

This is a sample revamped table over all 171 seed links. It treats each row as a router surface or door, not as a fully read leaf workflow. The point is fast querying first, then lazy expansion of only the best matching doors.

## What Changes

Old seed table answers: what link did we find?

New router table answers: when the user asks for a workflow, which door should we open first?

## Proposed Columns

| Column | Why it exists |
| --- | --- |
| `surface_id` | Stable row id for the router surface. |
| `surface_level` | Distinguishes manifest, category, lane, template, skill package, or workflow surface. |
| `domain_tags` | Fast domain matching: healthcare, real estate, education, public evidence, document processing, etc. |
| `workflow_pattern_tags` | Pattern matching: EvidenceAudit, DocumentTransformation, CaseIntake, HumanReview, Monitoring, QueueProcessing, ConfigPackage. |
| `input_contract_hint` | What the eventual workflow expects as input. |
| `output_artifact_hint` | What the workflow likely produces. |
| `codex_fit` | Whether this is Codex-adjacent, skill/package reference, inspiration, runtime/platform, or source taxonomy. |
| `expand_priority` | 1 means open first for common target queries; 3 means lower priority. |
| `expand_when` | Tells us when to spend agents on deep expansion. |

## Coverage Summary

- Router surfaces: 171
- Repos: 17
- Priority 1 surfaces: 52
- Priority 2 surfaces: 106
- Priority 3 surfaces: 13

### Domain Tags

| Domain | Count |
| --- | ---: |
| agent_workflows | 46 |
| general | 41 |
| automation | 21 |
| real_estate | 20 |
| document_processing | 16 |
| legal | 10 |
| healthcare | 9 |
| finance_or_crm | 8 |
| research | 7 |
| public_evidence | 6 |
| education | 4 |

### Workflow Pattern Tags

| Pattern | Count |
| --- | ---: |
| SkillRegistry | 91 |
| ConfigPackage | 63 |
| QueueProcessing | 35 |
| AutomationTemplate | 35 |
| PatternRouter | 28 |
| HumanReview | 24 |
| EvidenceAudit | 23 |
| DueDiligence | 20 |
| DocumentTransformation | 16 |
| ComplianceSupport | 14 |
| CaseIntake | 10 |
| HealthcareAdmin | 9 |
| ResearchOps | 7 |
| WorkflowSurface | 4 |
| EducationSupport | 4 |
| Monitoring | 2 |

### Earthquake / Public Evidence Audit

| Surface | Repo | Patterns | Why open it |
| --- | --- | --- | --- |
| Security Operations & GRC Workflows | agentskillexchange/skills | EvidenceAudit, ComplianceSupport | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Asset Management | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Brokerage | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, ComplianceSupport, ConfigPackage, SkillRegistry | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Capital Markets | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Closing | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Document Ingestion | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, DocumentTransformation | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Due Diligence | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, ComplianceSupport | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Financing | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Industrial | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Legal | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, CaseIntake, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Office | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

### Healthcare / Patient Documents

| Surface | Repo | Patterns | Why open it |
| --- | --- | --- | --- |
| Medical skills | CaseMark/skills | HealthcareAdmin, ComplianceSupport, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | HealthcareAdmin, ComplianceSupport, HumanReview, DocumentTransformation | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | HealthcareAdmin, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | HealthcareAdmin, ComplianceSupport, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| README Available Skills | K-Dense-AI/scientific-agent-skills | HealthcareAdmin, ComplianceSupport, HumanReview, ResearchOps, ConfigPackage, SkillRegistry | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Healthcare industry pack | indranilbanerjee/contentforge | HealthcareAdmin, ComplianceSupport, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Pharma industry pack | indranilbanerjee/contentforge | HealthcareAdmin, ComplianceSupport, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| USE-CASES | mergisi/awesome-openclaw-agents | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

### Real Estate Due Diligence

| Surface | Repo | Patterns | Why open it |
| --- | --- | --- | --- |
| Asset Management | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Brokerage | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, ComplianceSupport, ConfigPackage, SkillRegistry | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Capital Markets | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Closing | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Document Ingestion | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, DocumentTransformation | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Due Diligence | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, ComplianceSupport | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Financing | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Industrial | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Legal | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, CaseIntake, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Office | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Skill Index | ahacker-1/cre-agent-skills | DueDiligence, EvidenceAudit, ConfigPackage, SkillRegistry | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

### Education

| Surface | Repo | Patterns | Why open it |
| --- | --- | --- | --- |
| Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Education industry pack | indranilbanerjee/contentforge | EducationSupport | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| USE-CASES | mergisi/awesome-openclaw-agents | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Moodle | ritik-prog/n8n-automation-templates-5000 | EducationSupport, QueueProcessing, AutomationTemplate | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

### Document Processing / Human Review

| Surface | Repo | Patterns | Why open it |
| --- | --- | --- | --- |
| Case development skills | CaseMark/skills | CaseIntake, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Case setup | CaseMark/skills | CaseIntake, HumanReview | can classify directly from this link when query matches |
| Legal skills | CaseMark/skills | CaseIntake, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Medical skills | CaseMark/skills | HealthcareAdmin, ComplianceSupport, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| OCR | CaseMark/skills | DocumentTransformation | can classify directly from this link when query matches |
| Redline | CaseMark/skills | DocumentTransformation, CaseIntake, HumanReview | can classify directly from this link when query matches |
| Search | CaseMark/skills | CaseIntake, HumanReview | can classify directly from this link when query matches |
| Transcription | CaseMark/skills | DocumentTransformation | can classify directly from this link when query matches |
| Vaults | CaseMark/skills | DocumentTransformation | can classify directly from this link when query matches |
| Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | HealthcareAdmin, ComplianceSupport, HumanReview, DocumentTransformation | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | HealthcareAdmin, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | HealthcareAdmin, ComplianceSupport, HumanReview | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

## Full Router Surface Sample

| ID | Surface | Repo | Level | Domains | Patterns | Codex fit | Priority | Expand when |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| surface-0001 | All skills audit export | CaseMark/skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0002 | Capital skills | CaseMark/skills | category_surface | finance_or_crm | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0003 | Case development skills | CaseMark/skills | category_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0004 | Case setup | CaseMark/skills | workflow_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0005 | Finance skills | CaseMark/skills | category_surface | finance_or_crm | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0006 | Legal skills | CaseMark/skills | category_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0007 | Medical skills | CaseMark/skills | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0008 | OCR | CaseMark/skills | workflow_surface | document_processing | DocumentTransformation | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0009 | Redline | CaseMark/skills | workflow_surface | document_processing, legal | DocumentTransformation, CaseIntake, HumanReview | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0010 | Root skill | CaseMark/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0011 | Search | CaseMark/skills | workflow_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0012 | Skill spec | CaseMark/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0013 | Skill template | CaseMark/skills | template_or_package | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0014 | Transcription | CaseMark/skills | workflow_surface | document_processing | DocumentTransformation | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0015 | Vaults | CaseMark/skills | workflow_surface | document_processing | DocumentTransformation | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0016 | Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | category_surface | healthcare, document_processing | HealthcareAdmin, ComplianceSupport, HumanReview, DocumentTransformation | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0017 | Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | catalog_manifest | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0018 | README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0019 | Generated skills catalog | K-Dense-AI/scientific-agent-skills | category_surface | research | ResearchOps, ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0020 | Literature and paper workflows | K-Dense-AI/scientific-agent-skills | category_surface | research | ResearchOps, HumanReview | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0021 | README Available Skills | K-Dense-AI/scientific-agent-skills | category_surface | healthcare, research | HealthcareAdmin, ComplianceSupport, HumanReview, ResearchOps, ConfigPackage, SkillRegistry | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0022 | AI Agency Operations & FDE Workflows | agentskillexchange/skills | industry_lane | general | WorkflowSurface | skill/package reference | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0023 | Browser Automation | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0024 | Categories index | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0025 | Codex manifest | agentskillexchange/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | Codex-native or Codex-adjacent | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0026 | Coordinate multi-agent workflows with Ruflo | agentskillexchange/skills | skill_package | agent_workflows | ConfigPackage, SkillRegistry | Codex-native or Codex-adjacent | 3 | can classify directly from this link when query matches |
| surface-0027 | Data Platform & Analytics Engineering | agentskillexchange/skills | industry_lane | general | WorkflowSurface | skill/package reference | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0028 | Developer Tools | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0029 | Full Catalog | agentskillexchange/skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0030 | Industry collections index | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0031 | Infrastructure, SRE & Incident Operations | agentskillexchange/skills | industry_lane | general | Monitoring | skill/package reference | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0032 | JSON Index | agentskillexchange/skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0033 | OpenClaw manifest | agentskillexchange/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0034 | Orchestrate review-first multi-agent development work with Kandev | agentskillexchange/skills | skill_package | agent_workflows | HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0035 | Research & Scraping | agentskillexchange/skills | category_surface | research | ResearchOps | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0036 | Run academic literature review and paper-output workflows with Aut Sci Write | agentskillexchange/skills | skill_package | research | ResearchOps, HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0037 | Security & Verification | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0038 | Security Operations & GRC Workflows | agentskillexchange/skills | industry_lane | public_evidence | EvidenceAudit, ComplianceSupport | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0039 | Skill spec | agentskillexchange/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0040 | Skill template | agentskillexchange/skills | template_or_package | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0041 | Templates & Workflows | agentskillexchange/skills | category_surface | general | QueueProcessing, AutomationTemplate | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0042 | Asset Management | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0043 | Brokerage | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0044 | CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | category_surface | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport, ConfigPackage, SkillRegistry | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0045 | Capital Markets | ahacker-1/cre-agent-skills | category_surface | real_estate, finance_or_crm | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0046 | Closing | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0047 | Document Ingestion | ahacker-1/cre-agent-skills | category_surface | real_estate, document_processing | DueDiligence, EvidenceAudit, DocumentTransformation | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0048 | Due Diligence | ahacker-1/cre-agent-skills | category_surface | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0049 | Financing | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0050 | Industrial | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0051 | Legal | ahacker-1/cre-agent-skills | category_surface | real_estate, legal | DueDiligence, EvidenceAudit, CaseIntake, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0052 | Office | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0053 | Skill Index | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit, ConfigPackage, SkillRegistry | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0054 | Underwriting | ahacker-1/cre-agent-skills | category_surface | real_estate, finance_or_crm | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0055 | Evidence and compliance vocabulary | api-evangelist/use-cases | category_surface | public_evidence | EvidenceAudit, ComplianceSupport, HumanReview | source taxonomy | 1 | can classify directly from this link when query matches |
| surface-0056 | JSON-LD context | api-evangelist/use-cases | catalog_manifest | general | ConfigPackage, SkillRegistry | source taxonomy | 2 | can classify directly from this link when query matches |
| surface-0057 | apis.yml manifest | api-evangelist/use-cases | catalog_manifest | legal | CaseIntake, HumanReview, ConfigPackage, SkillRegistry | source taxonomy | 1 | can classify directly from this link when query matches |
| surface-0058 | Agents directory | ashishpatel26/500-AI-Agents-Projects | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0059 | Agno Examples | ashishpatel26/500-AI-Agents-Projects | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0060 | AutoGen Notebooks | ashishpatel26/500-AI-Agents-Projects | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0061 | CrewAI Examples | ashishpatel26/500-AI-Agents-Projects | category_surface | real_estate | DueDiligence, EvidenceAudit | inspiration catalog | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0062 | CrewAI MCP Course | ashishpatel26/500-AI-Agents-Projects | category_surface | real_estate | DueDiligence, EvidenceAudit | inspiration catalog | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0063 | Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | category_surface | healthcare, real_estate, education, legal, finance_or_crm | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | inspiration catalog | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0064 | Scope and Curation Rules | danielrosehill/Useful-AI-Agent-Skills | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0065 | AI Research/RAG/Data Analysis | enescingoz/awesome-n8n-templates | category_surface | research | ResearchOps, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0066 | Gmail/Email | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0067 | Google Drive/Sheets | enescingoz/awesome-n8n-templates | category_surface | document_processing | DocumentTransformation, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0068 | HR/Recruitment | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0069 | Notion | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0070 | OpenAI and LLMs | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0071 | PDF Document Processing | enescingoz/awesome-n8n-templates | category_surface | document_processing | DocumentTransformation, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0072 | README Catalog | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate, ConfigPackage, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0073 | Slack | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0074 | Social Media | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0075 | Telegram | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0076 | WhatsApp | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0077 | WordPress | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0078 | docs/index.md | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0079 | llms.txt | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0080 | AGENTS instructions | indranilbanerjee/contentforge | category_surface | agent_workflows | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0081 | Commands directory | indranilbanerjee/contentforge | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0082 | Education industry pack | indranilbanerjee/contentforge | category_surface | education | EducationSupport | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0083 | Healthcare industry pack | indranilbanerjee/contentforge | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0084 | Legal industry pack | indranilbanerjee/contentforge | category_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0085 | Pharma industry pack | indranilbanerjee/contentforge | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0086 | README skill catalog | indranilbanerjee/contentforge | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0087 | Real estate industry pack | indranilbanerjee/contentforge | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0088 | Skills directory | indranilbanerjee/contentforge | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0089 | Templates | indranilbanerjee/contentforge | category_surface | document_processing | DocumentTransformation, QueueProcessing, AutomationTemplate | skill/package reference | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0090 | Real Estate Agents | jim-schwoebel/awesome_ai_agents | category_surface | real_estate | DueDiligence, EvidenceAudit | inspiration catalog | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0091 | Agentic document intelligence docs | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0092 | Core query pipeline | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0093 | DAG workflows | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0094 | Document pipelines guide | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0095 | Executor pipeline | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0096 | Executor template | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0097 | Extract Engine | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0098 | Flows guide | marieai/marie-ai | category_surface | agent_workflows | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0099 | Form extraction | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0100 | Invoice processing | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0101 | Marie MCP | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0102 | Orchestrate flow | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0103 | Project template | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0104 | Query planners | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0105 | Template matching | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0106 | Workspaces | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0107 | Claude skills | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0108 | Configs | mergisi/awesome-openclaw-agents | category_surface | general | QueueProcessing, AutomationTemplate | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0109 | Gemma skills | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0110 | Memory wiki templates | mergisi/awesome-openclaw-agents | category_surface | general | QueueProcessing, AutomationTemplate | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0111 | Quickstart | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0112 | README Catalog | mergisi/awesome-openclaw-agents | category_surface | general | QueueProcessing, AutomationTemplate, ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0113 | USE-CASES | mergisi/awesome-openclaw-agents | category_surface | healthcare, real_estate, education, public_evidence, legal | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | inspiration catalog | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0114 | agents category index | mergisi/awesome-openclaw-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0115 | agents.json | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | QueueProcessing, AutomationTemplate | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0116 | skills README | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0117 | Divisions manifest | msitarzewski/agency-agents | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0118 | Engineering division | msitarzewski/agency-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0119 | Specialized division | msitarzewski/agency-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0120 | Strategy playbooks | msitarzewski/agency-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0121 | Tools manifest | msitarzewski/agency-agents | catalog_manifest | general | ConfigPackage, SkillRegistry | inspiration catalog | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0122 | CRM | ritik-prog/n8n-automation-templates-5000 | category_surface | finance_or_crm | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0123 | Google | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0124 | HubSpot | ritik-prog/n8n-automation-templates-5000 | category_surface | finance_or_crm | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0125 | Moodle | ritik-prog/n8n-automation-templates-5000 | category_surface | education | EducationSupport, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0126 | Notion | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0127 | OpenAI | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0128 | Salesforce | ritik-prog/n8n-automation-templates-5000 | category_surface | finance_or_crm | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0129 | Security Monitoring | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | Monitoring, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0130 | Slack | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0131 | Templates based on platforms lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0132 | Zillow | ritik-prog/n8n-automation-templates-5000 | category_surface | real_estate | DueDiligence, EvidenceAudit, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0133 | n8n advance lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0134 | n8n_2000_workflows lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0135 | workflows by Zie619 lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0136 | AAS Agent & MCP Builder | sickn33/antigravity-awesome-skills | template_or_package | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0137 | AAS Security Engineer | sickn33/antigravity-awesome-skills | template_or_package | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0138 | AAS Web App Builder | sickn33/antigravity-awesome-skills | template_or_package | general | ConfigPackage, SkillRegistry | skill/package reference | 3 | can classify directly from this link when query matches |
| surface-0139 | Bundles index | sickn33/antigravity-awesome-skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0140 | Design a DDD Core Domain | sickn33/antigravity-awesome-skills | workflow_surface | agent_workflows | WorkflowSurface | skill/package reference | 3 | can classify directly from this link when query matches |
| surface-0141 | Full skill catalog | sickn33/antigravity-awesome-skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0142 | Machine-readable bundles | sickn33/antigravity-awesome-skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0143 | Plugin marketplace manifest | sickn33/antigravity-awesome-skills | catalog_manifest | general | ConfigPackage, SkillRegistry | Codex-native or Codex-adjacent | 2 | can classify directly from this link when query matches |
| surface-0144 | Skills index | sickn33/antigravity-awesome-skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0145 | Workflows index | sickn33/antigravity-awesome-skills | workflow_surface | agent_workflows | WorkflowSurface | skill/package reference | 3 | can classify directly from this link when query matches |
| surface-0146 | plugins/ | sickn33/antigravity-awesome-skills | template_or_package | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0147 | skills/ | sickn33/antigravity-awesome-skills | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0148 | /analyze | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0149 | /arch-review | tinh2/skills-hub-registry | workflow_surface | agent_workflows | HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0150 | /build | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0151 | /devops | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0152 | /document | tinh2/skills-hub-registry | workflow_surface | document_processing | DocumentTransformation, ConfigPackage, SkillRegistry | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0153 | /dx | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 3 | can classify directly from this link when query matches |
| surface-0154 | /integrate | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0155 | /qa | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 3 | can classify directly from this link when query matches |
| surface-0156 | /secure | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0157 | /test-suite | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0158 | /ux | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0159 | README Skill Catalog | tinh2/skills-hub-registry | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0160 | analysis | tinh2/skills-hub-registry | category_surface | research | ResearchOps, ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0161 | build | tinh2/skills-hub-registry | category_surface | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0162 | combo | tinh2/skills-hub-registry | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0163 | compliance-suite | tinh2/skills-hub-registry | workflow_surface | public_evidence | EvidenceAudit, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 1 | can classify directly from this link when query matches |
| surface-0164 | design-to-code | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0165 | fix-and-ship | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0166 | mvp-spec | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0167 | qa | tinh2/skills-hub-registry | category_surface | general | ConfigPackage, SkillRegistry | skill/package reference | 3 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| surface-0168 | review-implement | tinh2/skills-hub-registry | workflow_surface | agent_workflows | HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0169 | secure-ship | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0170 | ship-pipeline | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | can classify directly from this link when query matches |
| surface-0171 | test | tinh2/skills-hub-registry | category_surface | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
