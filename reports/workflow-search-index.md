# Workflow Search Index

Generated: 2026-07-05T11:01:13.631173+00:00

This is the clean lookup layer over all 171 classified workflow doors. Use it as the main catalog for finding reusable workflow patterns, source repos, and Codex/ECC config-package references.

## Summary

- Workflows indexed: 171
- Domains: 11
- Workflow families: 10
- Gold rows: 67
- Silver rows: 43
- Needs verification: 61

## How To Query

Codex reads `data/agentic-repos/workflow-search-index.json` and
`data/agentic-repos/workflow-search-index-by-domain.json` directly through the
agent-workflow-project-maker skill.

## Quality Tiers

| Tier | Meaning | Rows |
| --- | --- | ---: |
| gold | Source reachable or canonicalized, high confidence, ready to copy/adapt. | 67 |
| silver | Useful reference with medium or better confidence. | 43 |
| bronze | Potentially useful but source needs repair or verification. | 0 |
| needs_verification | Searchable, but verify before relying on it. | 61 |

## Domain Counts

| Domain | Rows |
| --- | ---: |
| agent_workflows | 51 |
| public_evidence | 39 |
| automation | 24 |
| document_processing | 20 |
| real_estate | 16 |
| healthcare | 9 |
| legal_casework | 4 |
| finance_crm | 4 |
| education | 2 |
| research | 1 |
| general | 1 |

## Workflow Family Counts

| Family | Rows |
| --- | ---: |
| config_package_registry | 53 |
| evidence_due_diligence | 42 |
| document_transformation | 36 |
| case_intake_review | 15 |
| healthcare_admin | 10 |
| automation_queue | 10 |
| education_support | 2 |
| compliance_human_review | 1 |
| research_knowledge | 1 |
| monitoring | 1 |

## Codex Usefulness

| Usefulness | Rows |
| --- | ---: |
| strong_reference | 62 |
| copy_or_adapt_now | 48 |
| verify_source_first | 36 |
| use_with_caution | 15 |
| translate_pattern_only | 10 |

## Source Status

| Status | Rows |
| --- | ---: |
| exact_page_reachable | 63 |
| canonicalized | 47 |
| broken | 36 |
| exact_page_sparse | 25 |

## Best Rows By Domain

### healthcare

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0021 | README Available Skills | K-Dense-AI/scientific-agent-skills | healthcare_admin | gold | copy_or_adapt_now | Skill-pack structure, domain category taxonomy, database-backed workflow prompts, source provenance expectations, and clinical documentation/treatment-plan draft boundaries. | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/README.md |
| surface-0063 | Industry Use Cases | ashishpatel26/500-AI-Agents-Projects | healthcare_admin | silver | strong_reference | Industry-use-case taxonomy and the idea of separating healthcare, health insurance, and document/claims examples. | https://github.com/ashishpatel26/500-AI-Agents-Projects/blob/main/README.md |
| surface-0113 | USE-CASES | mergisi/awesome-openclaw-agents | healthcare_admin | silver | strong_reference | Health-adjacent workflow categories, lab-result organization idea, reimbursement admin pattern, and human-in-the-loop action boundary. | https://github.com/mergisi/awesome-openclaw-agents/blob/main/USE-CASES.md |
| surface-0007 | Medical skills | CaseMark/skills | healthcare_admin | needs_verification | verify_source_first | Only copy packet assembly, checklist, summarization, and review-handoff structure after source verification. | https://github.com/CaseMark/skills/tree/main/med |
| surface-0016 | Medical document workflows | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare_admin | needs_verification | verify_source_first | Only copy document-workflow structure, packet assembly patterns, and human-review gates after source verification. | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/tree/main/skills |
| surface-0017 | Plugin manifest | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare_admin | needs_verification | verify_source_first | Only copy manifest metadata, skill indexing structure, and review-boundary conventions after source verification. | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/blob/main/openclaw.plugin.json |
| surface-0018 | README Skills Overview | FreedomIntelligence/OpenClaw-Medical-Skills | healthcare_admin | needs_verification | verify_source_first | Only copy high-level package taxonomy, workflow names, and review-gate framing after source verification. | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/blob/main/README.md |
| surface-0083 | Healthcare industry pack | indranilbanerjee/contentforge | healthcare_admin | needs_verification | use_with_caution | Quality gates, fact-checking phases, review scoring, Word output artifact pattern, and provenance thinking for regulated content workflows. | https://github.com/indranilbanerjee/contentforge |
| surface-0085 | Pharma industry pack | indranilbanerjee/contentforge | healthcare_admin | needs_verification | use_with_caution | Phase gates, source verification, review scoring, document-output pattern, and provenance support for regulated content. | https://github.com/indranilbanerjee/contentforge |

### education

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0125 | Moodle | ritik-prog/n8n-automation-templates-5000 | education_support | silver | strong_reference | Copy the source taxonomy idea: Moodle as an education workflow door with trigger/integration examples. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Moodle |
| surface-0082 | Education industry pack | indranilbanerjee/contentforge | education_support | needs_verification | use_with_caution | Copy the idea of domain-specific configuration that informs drafting and validation. | https://github.com/indranilbanerjee/contentforge |

### real_estate

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0048 | Due Diligence | ahacker-1/cre-agent-skills | evidence_due_diligence | gold | copy_or_adapt_now | Copy multi-lane evidence review, issue logs, source attribution, exception handling, and mandatory review boundary. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/due-diligence |
| surface-0053 | Skill Index | ahacker-1/cre-agent-skills | evidence_due_diligence | gold | copy_or_adapt_now | Copy the index structure: skill name, use-when statement, key inputs, and paired knowledge base columns. | https://github.com/ahacker-1/cre-agent-skills/blob/main/docs/SKILL-INDEX.md |
| surface-0042 | Asset Management | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the folder-level taxonomy and repeated-job labels for CRE asset operations. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/asset-management |
| surface-0043 | Brokerage | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the transaction-stage taxonomy and artifact-oriented workflow names. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/brokerage |
| surface-0044 | CRE Due Diligence plugin pack | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the package grouping and due-diligence lane list as catalog metadata. | https://github.com/ahacker-1/cre-agent-skills/tree/main/claude-code-plugins/cre-due-diligence |
| surface-0045 | Capital Markets | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the packetized comparison pattern, source traceability, caveat discipline, and reviewer-style output framing. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/capital-markets |
| surface-0046 | Closing | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy closing-readiness checklist structure, exception tracking, evidence status labels, and human escalation boundary. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/closing |
| surface-0047 | Document Ingestion | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy document inventory, source-file preservation, field extraction with confidence/caveats, and parse validation gates. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/document-ingestion |
| surface-0049 | Financing | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy term comparison tables, assumption tracking, source-linked financing evidence, and review-before-external-action gates. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/financing |
| surface-0050 | Industrial | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the category taxonomy and artifact names for industrial CRE diligence lanes. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/industrial |
| surface-0051 | Legal | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the legal diligence lane taxonomy and explicit review-gate posture. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/legal |
| surface-0052 | Office | ahacker-1/cre-agent-skills | evidence_due_diligence | silver | strong_reference | Copy the office-specific diligence lane names and expected artifact categories. | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/office |

### public_evidence

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0019 | Generated skills catalog | K-Dense-AI/scientific-agent-skills | evidence_due_diligence | gold | copy_or_adapt_now | Copy the skill taxonomy, research use cases, provenance emphasis, and routing hints. | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/docs/skills.md |
| surface-0036 | Run academic literature review and paper-output workflows with Aut Sci Write | agentskillexchange/skills | evidence_due_diligence | gold | copy_or_adapt_now | Skill metadata shape, prerequisites, source-linked upstream reference, research stages, evidence extraction and citation artifact boundaries. | https://github.com/agentskillexchange/skills/tree/main/skills/run-academic-literature-review-and-paper-output-workflows-with-aut-sci-write |
| surface-0037 | Security & Verification | agentskillexchange/skills | case_intake_review | gold | copy_or_adapt_now | Category taxonomy, security-verification grouping, list-style registry shape, and evidence fields such as stars/downloads when independently verified. | https://github.com/agentskillexchange/skills/tree/main/categories/security-verification |
| surface-0038 | Security Operations & GRC Workflows | agentskillexchange/skills | evidence_due_diligence | gold | copy_or_adapt_now | Copy the audit packet pattern, approval-gate framing, artifact checklist, and evidence-first language. | https://github.com/agentskillexchange/skills/blob/main/industries/security-operations-grc-workflows.md |
| surface-0064 | Scope and Curation Rules | danielrosehill/Useful-AI-Agent-Skills | evidence_due_diligence | gold | copy_or_adapt_now | Scope taxonomy, inclusion/exclusion criteria, category structure, and curation language around installable skill artifacts. | https://github.com/danielrosehill/Useful-AI-Agent-Skills/blob/main/README.md |
| surface-0088 | Skills directory | indranilbanerjee/contentforge | config_package_registry | gold | copy_or_adapt_now | Directory-as-registry shape, one folder per skill, portable SKILL.md convention, manifest wrappers, and explicit support matrix language. | https://github.com/indranilbanerjee/contentforge/tree/master/skills |
| surface-0148 | /analyze | tinh2/skills-hub-registry | config_package_registry | gold | copy_or_adapt_now | Skill metadata shape, trigger wording, stack-detection matrix idea, and phased audit structure. | https://raw.githubusercontent.com/tinh2/skills-hub-registry/main/analysis/analyze/SKILL.md |
| surface-0152 | /document | tinh2/skills-hub-registry | document_transformation | gold | copy_or_adapt_now | Copy the audit structure: detect stack and maturity, inventory docs, score gaps, recommend next actions, validate report completeness. | https://github.com/tinh2/skills-hub-registry/tree/main/docs/document |
| surface-0153 | /dx | tinh2/skills-hub-registry | config_package_registry | gold | copy_or_adapt_now | Phase structure: input parsing, stack detection, six-area scoring rubric, recommendation priority, self-healing validation, report format. | https://raw.githubusercontent.com/tinh2/skills-hub-registry/main/productivity/dx/SKILL.md |
| surface-0155 | /qa | tinh2/skills-hub-registry | case_intake_review | gold | copy_or_adapt_now | Phased QA structure: input/scope, project detection, API verification, screen audit, domain consistency, integration verification, report and cleanup. | https://raw.githubusercontent.com/tinh2/skills-hub-registry/main/qa/qa/SKILL.md |
| surface-0157 | /test-suite | tinh2/skills-hub-registry | config_package_registry | gold | copy_or_adapt_now | Copy the stack-detection inventory, testing-category taxonomy, weighted scoring model, prioritized remediation routing, and explicit no-edit boundary. | https://raw.githubusercontent.com/tinh2/skills-hub-registry/main/test/test-suite/SKILL.md |
| surface-0158 | /ux | tinh2/skills-hub-registry | config_package_registry | gold | strong_reference | Copy the dual-mode audit/validation contract, screen inventory, theme-token inventory, WCAG checklist, motion review, and severity model. | https://raw.githubusercontent.com/tinh2/skills-hub-registry/main/ux/ux/SKILL.md |

### document_processing

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0008 | OCR | CaseMark/skills | document_transformation | gold | copy_or_adapt_now | Copy the explicit input limits, asynchronous job lifecycle, JSON-first commands, timeout handling, and word-level confidence output pattern. | https://raw.githubusercontent.com/CaseMark/skills/main/skills/casedev/ocr/SKILL.md |
| surface-0009 | Redline | CaseMark/skills | document_transformation | gold | copy_or_adapt_now | Copy the two-input comparison contract, structured output schema, detail levels, focus filters, and explicit scanned-document fallback to OCR. | https://raw.githubusercontent.com/CaseMark/skills/main/skills/casedev/redline/SKILL.md |
| surface-0014 | Transcription | CaseMark/skills | document_transformation | gold | copy_or_adapt_now | Copy the vault-backed media input requirement, speaker diarization controls, job watch pattern, and explicit file type and size limits. | https://raw.githubusercontent.com/CaseMark/skills/main/skills/casedev/transcription/SKILL.md |
| surface-0015 | Vaults | CaseMark/skills | document_transformation | gold | copy_or_adapt_now | Copy the isolated collection model, upload-list-download-search action set, ingestion readiness check, and explicit search fallback behavior. | https://raw.githubusercontent.com/CaseMark/skills/main/skills/casedev/vaults/SKILL.md |
| surface-0023 | Browser Automation | agentskillexchange/skills | document_transformation | gold | copy_or_adapt_now | Copy the category organization and separation among scraping, UI testing, screenshots/PDF, accessibility, visual regression, and session tooling. | https://github.com/agentskillexchange/skills/tree/main/categories/browser-automation |
| surface-0035 | Research & Scraping | agentskillexchange/skills | document_transformation | gold | copy_or_adapt_now | Copy category labels, package routing ideas, source-collection patterns, and validation prompts for scraping/research workflows. | https://github.com/agentskillexchange/skills/tree/main/categories/research-scraping |
| surface-0065 | AI Research/RAG/Data Analysis | enescingoz/awesome-n8n-templates | document_transformation | gold | strong_reference | Trigger shapes, document/RAG pipeline ideas, source routing, queue-like handoff, and structured output examples. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/AI_Research_RAG_and_Data_Analysis |
| surface-0071 | PDF Document Processing | enescingoz/awesome-n8n-templates | document_transformation | gold | strong_reference | Copy workflow ideas, input/output contract shapes, extraction stages, and review gates. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/PDF_and_Document_Processing |
| surface-0075 | Telegram | enescingoz/awesome-n8n-templates | document_transformation | gold | strong_reference | Copy abstract trigger-input-output shapes, credential separation, review-before-send boundaries, and queue/notification patterns. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Telegram |
| surface-0091 | Agentic document intelligence docs | marieai/marie-ai | healthcare_admin | gold | strong_reference | Copy the pipeline shape: ingestion, OCR, classification, extraction, validation, transformation, monitoring, and explicit document-domain examples. | https://github.com/marieai/marie-ai/blob/main/README.md |
| surface-0133 | n8n advance lane | ritik-prog/n8n-automation-templates-5000 | document_transformation | gold | strong_reference | Operational job names, routing/escalation patterns, report-generation boundaries, and queue/review concepts. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/n8n advance |
| surface-0067 | Google Drive/Sheets | enescingoz/awesome-n8n-templates | document_transformation | silver | strong_reference | Copy high-level trigger-transform-write patterns, document summarization flow shape, and concrete input/output contracts after selecting a specific template. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Google_Drive_and_Google_Sheets |

### legal_casework

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0022 | AI Agency Operations & FDE Workflows | agentskillexchange/skills | config_package_registry | gold | copy_or_adapt_now | High-level workflow category labels, reusable surface framing, and source-backed terminology. | https://github.com/agentskillexchange/skills/blob/main/industries/ai-agency-operations.md |
| surface-0025 | Codex manifest | agentskillexchange/skills | config_package_registry | gold | copy_or_adapt_now | Manifest field model, category and verification metadata, and slug-based discovery pattern. | https://github.com/agentskillexchange/skills/blob/main/codex.json |
| surface-0057 | apis.yml manifest | api-evangelist/use-cases | case_intake_review | needs_verification | verify_source_first | Manifest/index pattern, category labels, and routing vocabulary if confirmed from the canonical file. | https://github.com/api-evangelist/use-cases/blob/main/apis.yml |
| surface-0141 | Full skill catalog | sickn33/antigravity-awesome-skills | config_package_registry | needs_verification | use_with_caution | Catalog organization, entry fields, category groupings, and link conventions if source verification confirms them. | https://github.com/sickn33/antigravity-awesome-skills/blob/main/CATALOG.md |

### finance_crm

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0128 | Salesforce | ritik-prog/n8n-automation-templates-5000 | automation_queue | gold | strong_reference | Trigger taxonomy, CRM source/destination naming, queue-like sync and notification patterns, and explicit credential/input assumptions. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Salesforce |
| surface-0131 | Templates based on platforms lane | ritik-prog/n8n-automation-templates-5000 | document_transformation | gold | strong_reference | Platform taxonomy, integration grouping, and the idea of separating source doors from workflow contracts. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms |
| surface-0122 | CRM | ritik-prog/n8n-automation-templates-5000 | document_transformation | needs_verification | translate_pattern_only | Copy high-level trigger, queue, transformation, and approval patterns when they are clearly evidenced. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/CRM |
| surface-0124 | HubSpot | ritik-prog/n8n-automation-templates-5000 | document_transformation | needs_verification | translate_pattern_only | Copy high-level CRM trigger, queue, enrichment, transformation, and approval patterns when clearly evidenced. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/HubSpot |

### research

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0160 | analysis | tinh2/skills-hub-registry | research_knowledge | silver | strong_reference | Category naming, routing breadth, and subfolder taxonomy for catalog expansion. | https://github.com/tinh2/skills-hub-registry/tree/main/analysis |

### automation

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0031 | Infrastructure, SRE & Incident Operations | agentskillexchange/skills | automation_queue | gold | copy_or_adapt_now | Workflow naming, source category framing, and high-level operational surface labels that are explicitly present. | https://github.com/agentskillexchange/skills/blob/main/industries/infrastructure-sre-incident-operations.md |
| surface-0040 | Skill template | agentskillexchange/skills | automation_queue | gold | copy_or_adapt_now | Minimal frontmatter pattern, source attribution placeholder, concise body structure, and install/manual-copy section pattern. | https://github.com/agentskillexchange/skills/blob/main/template/SKILL.md |
| surface-0066 | Gmail/Email | enescingoz/awesome-n8n-templates | case_intake_review | gold | strong_reference | Email trigger taxonomy, classify-label-draft-review flow, human-in-the-loop response pattern, and audit logging ideas. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Gmail_and_Email_Automation |
| surface-0068 | HR/Recruitment | enescingoz/awesome-n8n-templates | case_intake_review | gold | strong_reference | Applicant intake shape, review queue boundary, policy-doc grounding, structured screening output, and approval checkpoints. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/HR_and_Recruitment |
| surface-0076 | WhatsApp | enescingoz/awesome-n8n-templates | automation_queue | gold | strong_reference | Copy abstract WhatsApp trigger patterns, customer-message input contracts, review-before-send gates, and notification/follow-up output shapes. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/WhatsApp |
| surface-0077 | WordPress | enescingoz/awesome-n8n-templates | case_intake_review | gold | strong_reference | Copy input/output contracts for draft content, metadata enrichment, review gates, and CMS-write safety boundaries. | https://github.com/enescingoz/awesome-n8n-templates/tree/main/WordPress |
| surface-0078 | docs/index.md | enescingoz/awesome-n8n-templates | automation_queue | gold | strong_reference | Copy category taxonomy, import-time credential awareness, platform trigger/output framing, and review boundaries for external actions. | https://github.com/enescingoz/awesome-n8n-templates/blob/main/docs/index.md |
| surface-0079 | llms.txt | enescingoz/awesome-n8n-templates | case_intake_review | gold | strong_reference | Copy concise category labels, canonical folder pointers, platform coverage, and metadata-level source descriptions. | https://github.com/enescingoz/awesome-n8n-templates/blob/main/llms.txt |
| surface-0114 | Agents category index | mergisi/awesome-openclaw-agents | automation_queue | gold | copy_or_adapt_now | Category table, template-count index, browse links, and category router pattern for multi-domain workflow lookup. | https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/README.md |
| surface-0112 | README Catalog | mergisi/awesome-openclaw-agents | document_transformation | gold | copy_or_adapt_now | Copy category framing, trigger ideas, output shapes, and recurring job names. | https://github.com/mergisi/awesome-openclaw-agents/blob/main/README.md |
| surface-0130 | Slack | ritik-prog/n8n-automation-templates-5000 | automation_queue | gold | strong_reference | Slack as review/alert surface, trigger variety, queue notification patterns, and cross-system message routing concepts. | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Slack |
| surface-0013 | Skill template | CaseMark/skills | automation_queue | silver | strong_reference | Basic frontmatter shape and section headings for instructions, quick start, details, and troubleshooting. | https://github.com/CaseMark/skills/blob/main/template/SKILL.md |

### agent_workflows

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0010 | Root skill | CaseMark/skills | config_package_registry | gold | copy_or_adapt_now | Frontmatter plus concise description, explicit prerequisites, output sections, verification rule, and caveat pattern. | https://github.com/CaseMark/skills/blob/main/SKILL.md |
| surface-0024 | Categories index | agentskillexchange/skills | config_package_registry | gold | copy_or_adapt_now | Category taxonomy, counts, broad descriptions, and category-link routing pattern. | https://github.com/agentskillexchange/skills/blob/main/categories/README.md |
| surface-0027 | Data Platform & Analytics Engineering | agentskillexchange/skills | case_intake_review | gold | strong_reference | Copy the surface taxonomy, workflow stack framing, persona targeting, validation-before-rollout posture, and separation between data operations, analytics changes, performance, tab | https://github.com/agentskillexchange/skills/blob/main/industries/data-platform-analytics-engineering.md |
| surface-0028 | Developer Tools | agentskillexchange/skills | config_package_registry | gold | copy_or_adapt_now | Copy the category-level grouping, tool-discovery shape, and registry pattern for mapping developer-tool requests to specific skill/package references. | https://github.com/agentskillexchange/skills/tree/main/categories/developer-tools |
| surface-0039 | Skill spec | agentskillexchange/skills | document_transformation | gold | copy_or_adapt_now | Directory shape, required frontmatter concepts, slug discipline, source attribution field, and verification metadata concept. | https://github.com/agentskillexchange/skills/blob/main/spec/SKILL_SPEC.md |
| surface-0058 | Agents directory | ashishpatel26/500-AI-Agents-Projects | config_package_registry | gold | copy_or_adapt_now | Task taxonomy, folder-per-agent organization, quick-start expectations, metadata-file idea, and candidate real-world job names. | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents |
| surface-0080 | AGENTS instructions | indranilbanerjee/contentforge | config_package_registry | gold | strong_reference | AGENTS.md structure, canonical entry-point table, repo path map, skill-discovery wording, and clear connector opt-in boundary. | https://github.com/indranilbanerjee/contentforge/blob/master/AGENTS.md |
| surface-0081 | Commands directory | indranilbanerjee/contentforge | config_package_registry | gold | copy_or_adapt_now | Command directory layout, concise command naming, and mapping pattern from user-facing entry points to skills. | https://github.com/indranilbanerjee/contentforge/tree/master/commands |
| surface-0086 | README skill catalog | indranilbanerjee/contentforge | config_package_registry | gold | copy_or_adapt_now | README package anatomy, supported-surface matrix, skill catalog table, command-to-skill relationship, manifest path documentation, and validation/release consistency checks. | https://github.com/indranilbanerjee/contentforge/blob/master/README.md |
| surface-0109 | On-device skills folder | mergisi/awesome-openclaw-agents | config_package_registry | gold | copy_or_adapt_now | Folder shape with SKILL.md plus script entry point, install URL pattern, sample prompts, and optional UI asset convention. | https://github.com/mergisi/awesome-openclaw-agents/tree/main/skills/gemma |
| surface-0107 | Platform skills folder | mergisi/awesome-openclaw-agents | config_package_registry | gold | copy_or_adapt_now | Skill folder table, concise SKILL.md frontmatter convention, trigger-heavy descriptions, and short skill-size guidance. | https://github.com/mergisi/awesome-openclaw-agents/tree/main/skills/claude |
| surface-0116 | skills README | mergisi/awesome-openclaw-agents | case_intake_review | gold | strong_reference | Registry README shape, platform/category grouping, short compatibility table, and pointer from index to folder-level install instructions. | https://github.com/mergisi/awesome-openclaw-agents/blob/main/skills/README.md |

### general

| ID | Workflow | Repo | Family | Tier | Usefulness | What to copy | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| surface-0092 | Core query pipeline | marieai/marie-ai | config_package_registry | needs_verification | verify_source_first | High-level separation of core query routing concepts if confirmed in source. | https://github.com/marieai/marie-ai/tree/main/marie/core |

## Machine Files

- JSON: `data/agentic-repos/workflow-search-index.json`
- CSV: `data/agentic-repos/workflow-search-index.csv`
- By-domain JSON: `data/agentic-repos/workflow-search-index-by-domain.json`
