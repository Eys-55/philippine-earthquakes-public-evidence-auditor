# Workflow Router

Generated: 2026-07-05

This is the durable router over the 171 seed links. Each row is a workflow surface, or door, used for fast query matching before deeper agent expansion.

## Summary

- Router surfaces: 171
- Repos: 17
- Priority 1 surfaces: 52
- Priority 2 surfaces: 106
- Priority 3 surfaces: 13

## Domain Tags

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

## Workflow Pattern Tags

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

## Earthquake / Public Evidence Audit

| Surface | Repo | Domains | Patterns | Priority | Why open it |
| --- | --- | --- | --- | ---: | --- |
| Security Operations & GRC Workflows | agentskillexchange/skills | public_evidence | EvidenceAudit, ComplianceSupport | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Asset Management | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Brokerage | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport, ConfigPackage, SkillRegistry | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Capital Markets | ahacker-1/cre-agent-skills | real_estate, finance_or_crm | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Closing | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Document Ingestion | ahacker-1/cre-agent-skills | real_estate, document_processing | DueDiligence, EvidenceAudit, DocumentTransformation | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Due Diligence | ahacker-1/cre-agent-skills | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Financing | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Industrial | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Legal | ahacker-1/cre-agent-skills | real_estate, legal | DueDiligence, EvidenceAudit, CaseIntake, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Office | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

## Healthcare / Patient Documents

| Surface | Repo | Domains | Patterns | Priority | Why open it |
| --- | --- | --- | --- | ---: | --- |
| Medical skills | CaseMark/skills | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare, document_processing | HealthcareAdmin, ComplianceSupport, HumanReview, DocumentTransformation | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| README Available Skills | K-Dense-AI/scientific-agent-skills | healthcare, research | HealthcareAdmin, ComplianceSupport, HumanReview, ResearchOps, ConfigPackage, SkillRegistry | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | healthcare, real_estate, education, legal, finance_or_crm | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Healthcare industry pack | indranilbanerjee/contentforge | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Pharma industry pack | indranilbanerjee/contentforge | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| USE-CASES | mergisi/awesome-openclaw-agents | healthcare, real_estate, education, public_evidence, legal | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

## Real Estate Due Diligence

| Surface | Repo | Domains | Patterns | Priority | Why open it |
| --- | --- | --- | --- | ---: | --- |
| Asset Management | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Brokerage | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport, ConfigPackage, SkillRegistry | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Capital Markets | ahacker-1/cre-agent-skills | real_estate, finance_or_crm | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Closing | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Document Ingestion | ahacker-1/cre-agent-skills | real_estate, document_processing | DueDiligence, EvidenceAudit, DocumentTransformation | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Due Diligence | ahacker-1/cre-agent-skills | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Financing | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Industrial | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Legal | ahacker-1/cre-agent-skills | real_estate, legal | DueDiligence, EvidenceAudit, CaseIntake, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Office | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Skill Index | ahacker-1/cre-agent-skills | real_estate | DueDiligence, EvidenceAudit, ConfigPackage, SkillRegistry | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

## Education

| Surface | Repo | Domains | Patterns | Priority | Why open it |
| --- | --- | --- | --- | ---: | --- |
| Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | healthcare, real_estate, education, legal, finance_or_crm | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Education industry pack | indranilbanerjee/contentforge | education | EducationSupport | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| USE-CASES | mergisi/awesome-openclaw-agents | healthcare, real_estate, education, public_evidence, legal | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Moodle | ritik-prog/n8n-automation-templates-5000 | education | EducationSupport, QueueProcessing, AutomationTemplate | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

## Document Processing / Human Review

| Surface | Repo | Domains | Patterns | Priority | Why open it |
| --- | --- | --- | --- | ---: | --- |
| Case development skills | CaseMark/skills | legal | CaseIntake, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Case setup | CaseMark/skills | legal | CaseIntake, HumanReview | 1 | can classify directly from this link when query matches |
| Legal skills | CaseMark/skills | legal | CaseIntake, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Medical skills | CaseMark/skills | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| OCR | CaseMark/skills | document_processing | DocumentTransformation | 1 | can classify directly from this link when query matches |
| Redline | CaseMark/skills | document_processing, legal | DocumentTransformation, CaseIntake, HumanReview | 1 | can classify directly from this link when query matches |
| Search | CaseMark/skills | legal | CaseIntake, HumanReview | 1 | can classify directly from this link when query matches |
| Transcription | CaseMark/skills | document_processing | DocumentTransformation | 1 | can classify directly from this link when query matches |
| Vaults | CaseMark/skills | document_processing | DocumentTransformation | 1 | can classify directly from this link when query matches |
| Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare, document_processing | HealthcareAdmin, ComplianceSupport, HumanReview, DocumentTransformation | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |
| README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | 1 | expand only when query hits this domain or repo; inspect index/manifest then top leaf folders |

## Full Router Table

| ID | Surface | Repo | Level | Domains | Patterns | Codex fit | Priority | Source |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| surface-0001 | All skills audit export | CaseMark/skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/CaseMark/skills/blob/main/audit/export/all-skills.json |
| surface-0002 | Capital skills | CaseMark/skills | category_surface | finance_or_crm | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/CaseMark/skills/tree/main/capital |
| surface-0003 | Case development skills | CaseMark/skills | category_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev |
| surface-0004 | Case setup | CaseMark/skills | workflow_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev/setup |
| surface-0005 | Finance skills | CaseMark/skills | category_surface | finance_or_crm | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/CaseMark/skills/tree/main/finance |
| surface-0006 | Legal skills | CaseMark/skills | category_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/legal |
| surface-0007 | Medical skills | CaseMark/skills | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/med |
| surface-0008 | OCR | CaseMark/skills | workflow_surface | document_processing | DocumentTransformation | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev/ocr |
| surface-0009 | Redline | CaseMark/skills | workflow_surface | document_processing, legal | DocumentTransformation, CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev/redline |
| surface-0010 | Root skill | CaseMark/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/CaseMark/skills/blob/main/SKILL.md |
| surface-0011 | Search | CaseMark/skills | workflow_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev/search |
| surface-0012 | Skill spec | CaseMark/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/CaseMark/skills/blob/main/spec/SKILL_SPEC.md |
| surface-0013 | Skill template | CaseMark/skills | template_or_package | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/CaseMark/skills/blob/main/template/SKILL.md |
| surface-0014 | Transcription | CaseMark/skills | workflow_surface | document_processing | DocumentTransformation | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev/transcription |
| surface-0015 | Vaults | CaseMark/skills | workflow_surface | document_processing | DocumentTransformation | skill/package reference | 1 | https://github.com/CaseMark/skills/tree/main/casedev/vaults |
| surface-0016 | Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | category_surface | healthcare, document_processing | HealthcareAdmin, ComplianceSupport, HumanReview, DocumentTransformation | skill/package reference | 1 | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/tree/main/skills |
| surface-0017 | Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | catalog_manifest | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 1 | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/blob/main/openclaw.plugin.json |
| surface-0018 | README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/blob/main/README.md |
| surface-0019 | Generated skills catalog | K-Dense-AI/scientific-agent-skills | category_surface | research | ResearchOps, ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/docs/skills.md |
| surface-0020 | Literature and paper workflows | K-Dense-AI/scientific-agent-skills | category_surface | research | ResearchOps, HumanReview | skill/package reference | 2 | https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills |
| surface-0021 | README Available Skills | K-Dense-AI/scientific-agent-skills | category_surface | healthcare, research | HealthcareAdmin, ComplianceSupport, HumanReview, ResearchOps, ConfigPackage, SkillRegistry | skill/package reference | 1 | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/README.md |
| surface-0022 | AI Agency Operations & FDE Workflows | agentskillexchange/skills | industry_lane | general | WorkflowSurface | skill/package reference | 3 | https://github.com/agentskillexchange/skills/blob/main/industries/ai-agency-operations.md |
| surface-0023 | Browser Automation | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 3 | https://github.com/agentskillexchange/skills/tree/main/categories/browser-automation |
| surface-0024 | Categories index | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/categories/README.md |
| surface-0025 | Codex manifest | agentskillexchange/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | Codex-native or Codex-adjacent | 2 | https://github.com/agentskillexchange/skills/blob/main/codex.json |
| surface-0026 | Coordinate multi-agent workflows with Ruflo | agentskillexchange/skills | skill_package | agent_workflows | ConfigPackage, SkillRegistry | Codex-native or Codex-adjacent | 3 | https://github.com/agentskillexchange/skills/tree/main/skills/coordinate-multi-agent-claude-code-and-codex-workflows-with-ruflo |
| surface-0027 | Data Platform & Analytics Engineering | agentskillexchange/skills | industry_lane | general | WorkflowSurface | skill/package reference | 3 | https://github.com/agentskillexchange/skills/blob/main/industries/data-platform-analytics-engineering.md |
| surface-0028 | Developer Tools | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 3 | https://github.com/agentskillexchange/skills/tree/main/categories/developer-tools |
| surface-0029 | Full Catalog | agentskillexchange/skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/CATALOG.md |
| surface-0030 | Industry collections index | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/industries/README.md |
| surface-0031 | Infrastructure, SRE & Incident Operations | agentskillexchange/skills | industry_lane | general | Monitoring | skill/package reference | 3 | https://github.com/agentskillexchange/skills/blob/main/industries/infrastructure-sre-incident-operations.md |
| surface-0032 | JSON Index | agentskillexchange/skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/skills.json |
| surface-0033 | OpenClaw manifest | agentskillexchange/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/openclaw.json |
| surface-0034 | Orchestrate review-first multi-agent development work with Kandev | agentskillexchange/skills | skill_package | agent_workflows | HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/tree/main/skills/orchestrate-review-first-multi-agent-development-work-with-kandev |
| surface-0035 | Research & Scraping | agentskillexchange/skills | category_surface | research | ResearchOps | skill/package reference | 2 | https://github.com/agentskillexchange/skills/tree/main/categories/research-scraping |
| surface-0036 | Run academic literature review and paper-output workflows with Aut Sci Write | agentskillexchange/skills | skill_package | research | ResearchOps, HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/tree/main/skills/run-academic-literature-review-and-paper-output-workflows-with-aut-sci-write |
| surface-0037 | Security & Verification | agentskillexchange/skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/tree/main/categories/security-verification |
| surface-0038 | Security Operations & GRC Workflows | agentskillexchange/skills | industry_lane | public_evidence | EvidenceAudit, ComplianceSupport | skill/package reference | 1 | https://github.com/agentskillexchange/skills/blob/main/industries/security-operations-grc-workflows.md |
| surface-0039 | Skill spec | agentskillexchange/skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/spec/SKILL_SPEC.md |
| surface-0040 | Skill template | agentskillexchange/skills | template_or_package | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/agentskillexchange/skills/blob/main/template/SKILL.md |
| surface-0041 | Templates & Workflows | agentskillexchange/skills | category_surface | general | QueueProcessing, AutomationTemplate | skill/package reference | 2 | https://github.com/agentskillexchange/skills/tree/main/categories/templates-workflows |
| surface-0042 | Asset Management | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/asset-management |
| surface-0043 | Brokerage | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/brokerage |
| surface-0044 | CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | category_surface | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport, ConfigPackage, SkillRegistry | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/plugins/cre-due-diligence |
| surface-0045 | Capital Markets | ahacker-1/cre-agent-skills | category_surface | real_estate, finance_or_crm | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/capital-markets |
| surface-0046 | Closing | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/closing |
| surface-0047 | Document Ingestion | ahacker-1/cre-agent-skills | category_surface | real_estate, document_processing | DueDiligence, EvidenceAudit, DocumentTransformation | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/document-ingestion |
| surface-0048 | Due Diligence | ahacker-1/cre-agent-skills | category_surface | real_estate, public_evidence | DueDiligence, EvidenceAudit, ComplianceSupport | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/due-diligence |
| surface-0049 | Financing | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/financing |
| surface-0050 | Industrial | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/industrial |
| surface-0051 | Legal | ahacker-1/cre-agent-skills | category_surface | real_estate, legal | DueDiligence, EvidenceAudit, CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/legal |
| surface-0052 | Office | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/office |
| surface-0053 | Skill Index | ahacker-1/cre-agent-skills | category_surface | real_estate | DueDiligence, EvidenceAudit, ConfigPackage, SkillRegistry | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/blob/main/docs/SKILL-INDEX.md |
| surface-0054 | Underwriting | ahacker-1/cre-agent-skills | category_surface | real_estate, finance_or_crm | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/underwriting |
| surface-0055 | Evidence and compliance vocabulary | api-evangelist/use-cases | category_surface | public_evidence | EvidenceAudit, ComplianceSupport, HumanReview | source taxonomy | 1 | https://github.com/api-evangelist/use-cases/blob/main/README.md |
| surface-0056 | JSON-LD context | api-evangelist/use-cases | catalog_manifest | general | ConfigPackage, SkillRegistry | source taxonomy | 2 | https://github.com/api-evangelist/use-cases/tree/main/use-cases.jsonld |
| surface-0057 | apis.yml manifest | api-evangelist/use-cases | catalog_manifest | legal | CaseIntake, HumanReview, ConfigPackage, SkillRegistry | source taxonomy | 1 | https://github.com/api-evangelist/use-cases/blob/main/apis.yml |
| surface-0058 | Agents directory | ashishpatel26/500-AI-Agents-Projects | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents |
| surface-0059 | Agno Examples | ashishpatel26/500-AI-Agents-Projects | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agno-examples |
| surface-0060 | AutoGen Notebooks | ashishpatel26/500-AI-Agents-Projects | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/AutoGen-Examples |
| surface-0061 | CrewAI Examples | ashishpatel26/500-AI-Agents-Projects | category_surface | real_estate | DueDiligence, EvidenceAudit | inspiration catalog | 1 | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/crewAI-examples |
| surface-0062 | CrewAI MCP Course | ashishpatel26/500-AI-Agents-Projects | category_surface | real_estate | DueDiligence, EvidenceAudit | inspiration catalog | 1 | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/crewAI-MCP-Course |
| surface-0063 | Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | category_surface | healthcare, real_estate, education, legal, finance_or_crm | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | inspiration catalog | 1 | https://github.com/ashishpatel26/500-AI-Agents-Projects/blob/main/README.md |
| surface-0064 | Scope and Curation Rules | danielrosehill/Useful-AI-Agent-Skills | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/danielrosehill/Useful-AI-Agent-Skills/blob/main/README.md |
| surface-0065 | AI Research/RAG/Data Analysis | enescingoz/awesome-n8n-templates | category_surface | research | ResearchOps, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/AI Research & RAG & Data Analysis |
| surface-0066 | Gmail/Email | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Gmail & Email |
| surface-0067 | Google Drive/Sheets | enescingoz/awesome-n8n-templates | category_surface | document_processing | DocumentTransformation, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Google Drive & Sheets |
| surface-0068 | HR/Recruitment | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/HR & Recruitment |
| surface-0069 | Notion | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Notion |
| surface-0070 | OpenAI and LLMs | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/OpenAI & LLMs |
| surface-0071 | PDF Document Processing | enescingoz/awesome-n8n-templates | category_surface | document_processing | DocumentTransformation, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/PDF & Document Processing |
| surface-0072 | README Catalog | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate, ConfigPackage, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/blob/main/README.md |
| surface-0073 | Slack | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Slack |
| surface-0074 | Social Media | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Social Media |
| surface-0075 | Telegram | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Telegram |
| surface-0076 | WhatsApp | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/WhatsApp |
| surface-0077 | WordPress | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/tree/main/WordPress |
| surface-0078 | docs/index.md | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/blob/main/docs/index.md |
| surface-0079 | llms.txt | enescingoz/awesome-n8n-templates | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/enescingoz/awesome-n8n-templates/blob/main/llms.txt |
| surface-0080 | AGENTS instructions | indranilbanerjee/contentforge | category_surface | agent_workflows | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/indranilbanerjee/contentforge/blob/main/AGENTS.md |
| surface-0081 | Commands directory | indranilbanerjee/contentforge | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/indranilbanerjee/contentforge/tree/main/commands |
| surface-0082 | Education industry pack | indranilbanerjee/contentforge | category_surface | education | EducationSupport | skill/package reference | 1 | https://github.com/indranilbanerjee/contentforge/tree/main/skills/education |
| surface-0083 | Healthcare industry pack | indranilbanerjee/contentforge | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | https://github.com/indranilbanerjee/contentforge/tree/main/skills/healthcare |
| surface-0084 | Legal industry pack | indranilbanerjee/contentforge | category_surface | legal | CaseIntake, HumanReview | skill/package reference | 1 | https://github.com/indranilbanerjee/contentforge/tree/main/skills/legal |
| surface-0085 | Pharma industry pack | indranilbanerjee/contentforge | category_surface | healthcare | HealthcareAdmin, ComplianceSupport, HumanReview | skill/package reference | 1 | https://github.com/indranilbanerjee/contentforge/tree/main/skills/pharma |
| surface-0086 | README skill catalog | indranilbanerjee/contentforge | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/indranilbanerjee/contentforge/blob/main/README.md |
| surface-0087 | Real estate industry pack | indranilbanerjee/contentforge | category_surface | real_estate | DueDiligence, EvidenceAudit | skill/package reference | 1 | https://github.com/indranilbanerjee/contentforge/tree/main/skills/real-estate |
| surface-0088 | Skills directory | indranilbanerjee/contentforge | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/indranilbanerjee/contentforge/tree/main/skills |
| surface-0089 | Templates | indranilbanerjee/contentforge | category_surface | document_processing | DocumentTransformation, QueueProcessing, AutomationTemplate | skill/package reference | 1 | https://github.com/indranilbanerjee/contentforge/tree/main/templates |
| surface-0090 | Real Estate Agents | jim-schwoebel/awesome_ai_agents | category_surface | real_estate | DueDiligence, EvidenceAudit | inspiration catalog | 1 | https://github.com/jim-schwoebel/awesome_ai_agents/blob/main/README.md |
| surface-0091 | Agentic document intelligence docs | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | https://github.com/marieai/marie-ai/blob/main/README.md |
| surface-0092 | Core query pipeline | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/marie/core |
| surface-0093 | DAG workflows | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/marie/workflows |
| surface-0094 | Document pipelines guide | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | https://github.com/marieai/marie-ai/blob/main/docs/document-pipelines.md |
| surface-0095 | Executor pipeline | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/marie/executor |
| surface-0096 | Executor template | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/executor/template |
| surface-0097 | Extract Engine | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | https://github.com/marieai/marie-ai/tree/main/marie/extract |
| surface-0098 | Flows guide | marieai/marie-ai | category_surface | agent_workflows | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/blob/main/docs/flows.md |
| surface-0099 | Form extraction | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | https://github.com/marieai/marie-ai/tree/main/examples/form-extraction |
| surface-0100 | Invoice processing | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | https://github.com/marieai/marie-ai/tree/main/examples/invoice-processing |
| surface-0101 | Marie MCP | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/mcp |
| surface-0102 | Orchestrate flow | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/marie/orchestrate |
| surface-0103 | Project template | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/template |
| surface-0104 | Query planners | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/tree/main/marie/query_planner |
| surface-0105 | Template matching | marieai/marie-ai | category_surface | document_processing | DocumentTransformation | runtime/platform inspiration | 1 | https://github.com/marieai/marie-ai/tree/main/marie/template_matching |
| surface-0106 | Workspaces | marieai/marie-ai | category_surface | general | PatternRouter, SkillRegistry | runtime/platform inspiration | 2 | https://github.com/marieai/marie-ai/blob/main/docs/workspaces.md |
| surface-0107 | Claude skills | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/tree/main/skills/claude |
| surface-0108 | Configs | mergisi/awesome-openclaw-agents | category_surface | general | QueueProcessing, AutomationTemplate | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/tree/main/configs |
| surface-0109 | Gemma skills | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/tree/main/skills/gemma |
| surface-0110 | Memory wiki templates | mergisi/awesome-openclaw-agents | category_surface | general | QueueProcessing, AutomationTemplate | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/tree/main/memory-wiki |
| surface-0111 | Quickstart | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/blob/main/QUICKSTART.md |
| surface-0112 | README Catalog | mergisi/awesome-openclaw-agents | category_surface | general | QueueProcessing, AutomationTemplate, ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/blob/main/README.md |
| surface-0113 | USE-CASES | mergisi/awesome-openclaw-agents | category_surface | healthcare, real_estate, education, public_evidence, legal | HealthcareAdmin, ComplianceSupport, HumanReview, DueDiligence, EvidenceAudit, EducationSupport, CaseIntake | inspiration catalog | 1 | https://github.com/mergisi/awesome-openclaw-agents/blob/main/USE-CASES.md |
| surface-0114 | agents category index | mergisi/awesome-openclaw-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/README.md |
| surface-0115 | agents.json | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | QueueProcessing, AutomationTemplate | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents.json |
| surface-0116 | skills README | mergisi/awesome-openclaw-agents | category_surface | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/mergisi/awesome-openclaw-agents/blob/main/skills/README.md |
| surface-0117 | Divisions manifest | msitarzewski/agency-agents | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/msitarzewski/agency-agents/blob/main/divisions.json |
| surface-0118 | Engineering division | msitarzewski/agency-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 3 | https://github.com/msitarzewski/agency-agents/tree/main/agents/engineering |
| surface-0119 | Specialized division | msitarzewski/agency-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/msitarzewski/agency-agents/tree/main/agents/specialized |
| surface-0120 | Strategy playbooks | msitarzewski/agency-agents | category_surface | general | PatternRouter, SkillRegistry | inspiration catalog | 2 | https://github.com/msitarzewski/agency-agents/tree/main/strategy |
| surface-0121 | Tools manifest | msitarzewski/agency-agents | catalog_manifest | general | ConfigPackage, SkillRegistry | inspiration catalog | 2 | https://github.com/msitarzewski/agency-agents/blob/main/tools.json |
| surface-0122 | CRM | ritik-prog/n8n-automation-templates-5000 | category_surface | finance_or_crm | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/CRM |
| surface-0123 | Google | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Google |
| surface-0124 | HubSpot | ritik-prog/n8n-automation-templates-5000 | category_surface | finance_or_crm | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/HubSpot |
| surface-0125 | Moodle | ritik-prog/n8n-automation-templates-5000 | category_surface | education | EducationSupport, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Moodle |
| surface-0126 | Notion | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Notion |
| surface-0127 | OpenAI | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/OpenAI |
| surface-0128 | Salesforce | ritik-prog/n8n-automation-templates-5000 | category_surface | finance_or_crm | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Salesforce |
| surface-0129 | Security Monitoring | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | Monitoring, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/blob/main/README.md |
| surface-0130 | Slack | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Slack |
| surface-0131 | Templates based on platforms lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms |
| surface-0132 | Zillow | ritik-prog/n8n-automation-templates-5000 | category_surface | real_estate | DueDiligence, EvidenceAudit, QueueProcessing, AutomationTemplate | runtime/platform inspiration | 1 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Zillow |
| surface-0133 | n8n advance lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/n8n advance |
| surface-0134 | n8n_2000_workflows lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/n8n_2000_workflows |
| surface-0135 | workflows by Zie619 lane | ritik-prog/n8n-automation-templates-5000 | category_surface | automation | QueueProcessing, AutomationTemplate | runtime/platform inspiration | 2 | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/workflows by Zie619 |
| surface-0136 | AAS Agent & MCP Builder | sickn33/antigravity-awesome-skills | template_or_package | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins/antigravity-bundle-aas-agent-mcp-builder |
| surface-0137 | AAS Security Engineer | sickn33/antigravity-awesome-skills | template_or_package | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins/antigravity-bundle-aas-security-engineer |
| surface-0138 | AAS Web App Builder | sickn33/antigravity-awesome-skills | template_or_package | general | ConfigPackage, SkillRegistry | skill/package reference | 3 | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins/antigravity-bundle-aas-web-app-builder |
| surface-0139 | Bundles index | sickn33/antigravity-awesome-skills | category_surface | general | PatternRouter, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md |
| surface-0140 | Design a DDD Core Domain | sickn33/antigravity-awesome-skills | workflow_surface | agent_workflows | WorkflowSurface | skill/package reference | 3 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/data/workflows.json |
| surface-0141 | Full skill catalog | sickn33/antigravity-awesome-skills | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/CATALOG.md |
| surface-0142 | Machine-readable bundles | sickn33/antigravity-awesome-skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/data/bundles.json |
| surface-0143 | Plugin marketplace manifest | sickn33/antigravity-awesome-skills | catalog_manifest | general | ConfigPackage, SkillRegistry | Codex-native or Codex-adjacent | 2 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/.agents/plugins/marketplace.json |
| surface-0144 | Skills index | sickn33/antigravity-awesome-skills | catalog_manifest | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/skills_index.json |
| surface-0145 | Workflows index | sickn33/antigravity-awesome-skills | workflow_surface | agent_workflows | WorkflowSurface | skill/package reference | 3 | https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md |
| surface-0146 | plugins/ | sickn33/antigravity-awesome-skills | template_or_package | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins |
| surface-0147 | skills/ | sickn33/antigravity-awesome-skills | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills |
| surface-0148 | /analyze | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/analysis/analyze |
| surface-0149 | /arch-review | tinh2/skills-hub-registry | workflow_surface | agent_workflows | HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/review/arch-review |
| surface-0150 | /build | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/build/build |
| surface-0151 | /devops | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/deploy/devops |
| surface-0152 | /document | tinh2/skills-hub-registry | workflow_surface | document_processing | DocumentTransformation, ConfigPackage, SkillRegistry | skill/package reference | 1 | https://github.com/tinh2/skills-hub-registry/tree/main/docs/document |
| surface-0153 | /dx | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 3 | https://github.com/tinh2/skills-hub-registry/tree/main/productivity/dx |
| surface-0154 | /integrate | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/integration/integrate |
| surface-0155 | /qa | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 3 | https://github.com/tinh2/skills-hub-registry/tree/main/qa/qa |
| surface-0156 | /secure | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/security/secure |
| surface-0157 | /test-suite | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/test/test-suite |
| surface-0158 | /ux | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/ux/ux |
| surface-0159 | README Skill Catalog | tinh2/skills-hub-registry | catalog_manifest | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/blob/main/README.md |
| surface-0160 | analysis | tinh2/skills-hub-registry | category_surface | research | ResearchOps, ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/analysis |
| surface-0161 | build | tinh2/skills-hub-registry | category_surface | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/build |
| surface-0162 | combo | tinh2/skills-hub-registry | category_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo |
| surface-0163 | compliance-suite | tinh2/skills-hub-registry | workflow_surface | public_evidence | EvidenceAudit, ComplianceSupport, HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 1 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/compliance-suite |
| surface-0164 | design-to-code | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/design-to-code |
| surface-0165 | fix-and-ship | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/fix-and-ship |
| surface-0166 | mvp-spec | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/mvp-spec |
| surface-0167 | qa | tinh2/skills-hub-registry | category_surface | general | ConfigPackage, SkillRegistry | skill/package reference | 3 | https://github.com/tinh2/skills-hub-registry/tree/main/qa |
| surface-0168 | review-implement | tinh2/skills-hub-registry | workflow_surface | agent_workflows | HumanReview, ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/review-implement |
| surface-0169 | secure-ship | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/secure-ship |
| surface-0170 | ship-pipeline | tinh2/skills-hub-registry | workflow_surface | agent_workflows | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/combo/ship-pipeline |
| surface-0171 | test | tinh2/skills-hub-registry | category_surface | general | ConfigPackage, SkillRegistry | skill/package reference | 2 | https://github.com/tinh2/skills-hub-registry/tree/main/test |
