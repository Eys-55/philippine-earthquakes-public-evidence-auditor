# Workflow Link Seed

Generated: 2026-07-05

This is the readiness artifact from the six inside-Codex discovery agents. It captures indexed workflow, skill, template, and lane links before any external CLI classification agents are launched.

- Repos inspected: 17 / 17
- Deduped seed links: 171
- CLI chunks at 10 links each: 18

## Completeness Status

| Repo | Seed links | Needs second pass | Inspection notes |
| --- | ---: | --- | --- |
| sickn33/antigravity-awesome-skills | 12 | true | Inspected README, docs workflow/bundle indexes, generated manifests, marketplace manifest, and plugin/skills surfaces. Captured indexed surfaces first for 1,898+ generated skills. |
| agentskillexchange/skills | 20 | true | Inspected README, categories, industries, root manifests, template/spec surfaces. Captured indexed surfaces first for 2,678 generated skills. |
| tinh2/skills-hub-registry | 24 | true | Inspected README, orchestrator tables, and visible tree. Captured categories, orchestrators, and combo workflow folders first. |
| danielrosehill/Useful-AI-Agent-Skills | 1 | true | Inspected README and SCOPE; captured meta-list/category surfaces. |
| msitarzewski/agency-agents | 5 | true | Inspected README, divisions, tools, and folders; captured division surfaces for 235 source agent files. |
| ashishpatel26/500-AI-Agents-Projects | 6 | true | Inspected README, agents, course/examples/notebook sections, and industry-use-case sections. |
| mergisi/awesome-openclaw-agents | 10 | true | Inspected README, agents.json, agents/README, skills/README, configs, USE-CASES; captured indexed category surfaces. |
| jim-schwoebel/awesome_ai_agents | 1 | true | Inspected README; captured category anchors and Workflows section. |
| K-Dense-AI/scientific-agent-skills | 3 | true | Inspected top-level SKILL.md folders and generated skills catalog; found 149 top-level skill folders. |
| FreedomIntelligence/OpenClaw-Medical-Skills | 3 | true | Inspected plugin manifest, skills directory, README skill overview; found hundreds of medical SKILL.md files. |
| ahacker-1/cre-agent-skills | 13 | true | Inspected docs/SKILL-INDEX and plugin packs; captured 66 skill-file index and CRE workflow categories. |
| CaseMark/skills | 15 | true | Inspected root SKILL, template/spec, audit export, and category folders across legal/medical/finance/capital/casedev. |
| indranilbanerjee/contentforge | 10 | true | Inspected README, AGENTS, manifests, skills, commands, templates, and industry packs. |
| marieai/marie-ai | 16 | true | Inspected README, docs, examples, pipeline/executor/template surfaces; captured document-intelligence workflow surfaces. |
| enescingoz/awesome-n8n-templates | 15 | true | Inspected README, docs/index.md, llms.txt, category folders. Found 313 JSON workflow templates; captured categories. |
| ritik-prog/n8n-automation-templates-5000 | 14 | true | Inspected README and tree. Large/generated repo with 6,260 JSON workflows across lanes/platform folders; captured lanes and major platform/category folders. |
| api-evangelist/use-cases | 3 | false | Inspected README, apis.yml, JSON-LD context, vocabulary; apis list empty. |

## Seed Links

| ID | Repo | Candidate | Name | Domain hint | Confidence | Needs second pass | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| wfseed-0001 | CaseMark/skills | manifest | All skills audit export | machine-readable catalog | high | true | https://github.com/CaseMark/skills/blob/main/audit/export/all-skills.json |
| wfseed-0002 | CaseMark/skills | category | Capital skills | capital markets workflows | high | true | https://github.com/CaseMark/skills/tree/main/capital |
| wfseed-0003 | CaseMark/skills | category | Case development skills | case intake/review workflows | high | true | https://github.com/CaseMark/skills/tree/main/casedev |
| wfseed-0004 | CaseMark/skills | workflow | Case setup | case intake | high | false | https://github.com/CaseMark/skills/tree/main/casedev/setup |
| wfseed-0005 | CaseMark/skills | category | Finance skills | finance workflows | high | true | https://github.com/CaseMark/skills/tree/main/finance |
| wfseed-0006 | CaseMark/skills | category | Legal skills | legal workflows | high | true | https://github.com/CaseMark/skills/tree/main/legal |
| wfseed-0007 | CaseMark/skills | category | Medical skills | medical/PHI-aware workflows | high | true | https://github.com/CaseMark/skills/tree/main/med |
| wfseed-0008 | CaseMark/skills | workflow | OCR | document extraction | high | false | https://github.com/CaseMark/skills/tree/main/casedev/ocr |
| wfseed-0009 | CaseMark/skills | workflow | Redline | human review/document redline | high | false | https://github.com/CaseMark/skills/tree/main/casedev/redline |
| wfseed-0010 | CaseMark/skills | manifest | Root skill | skill router | high | false | https://github.com/CaseMark/skills/blob/main/SKILL.md |
| wfseed-0011 | CaseMark/skills | workflow | Search | case search | high | false | https://github.com/CaseMark/skills/tree/main/casedev/search |
| wfseed-0012 | CaseMark/skills | manifest | Skill spec | skill format | high | false | https://github.com/CaseMark/skills/blob/main/spec/SKILL_SPEC.md |
| wfseed-0013 | CaseMark/skills | template | Skill template | skill authoring | high | false | https://github.com/CaseMark/skills/blob/main/template/SKILL.md |
| wfseed-0014 | CaseMark/skills | workflow | Transcription | audio to document | high | false | https://github.com/CaseMark/skills/tree/main/casedev/transcription |
| wfseed-0015 | CaseMark/skills | workflow | Vaults | document vaults | high | false | https://github.com/CaseMark/skills/tree/main/casedev/vaults |
| wfseed-0016 | FreedomIntelligence/OpenClaw-Medical-Skills | category | Medical document workflows | medical document processing | high | true | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/tree/main/skills |
| wfseed-0017 | FreedomIntelligence/OpenClaw-Medical-Skills | manifest | Plugin manifest | medical skill package | high | true | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/blob/main/openclaw.plugin.json |
| wfseed-0018 | FreedomIntelligence/OpenClaw-Medical-Skills | category | README Skills Overview | medical overview categories | high | true | https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills/blob/main/README.md |
| wfseed-0019 | K-Dense-AI/scientific-agent-skills | category | Generated skills catalog | research skills catalog | high | true | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/docs/skills.md |
| wfseed-0020 | K-Dense-AI/scientific-agent-skills | category | Literature and paper workflows | scientific literature review | high | true | https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills |
| wfseed-0021 | K-Dense-AI/scientific-agent-skills | category | README Available Skills | science and medical skill index | high | true | https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/README.md |
| wfseed-0022 | agentskillexchange/skills | lane | AI Agency Operations & FDE Workflows | agency/FDE workflows | high | true | https://github.com/agentskillexchange/skills/blob/main/industries/ai-agency-operations.md |
| wfseed-0023 | agentskillexchange/skills | category | Browser Automation | 118 skills | high | true | https://github.com/agentskillexchange/skills/tree/main/categories/browser-automation |
| wfseed-0024 | agentskillexchange/skills | category | Categories index | 17 categories | high | true | https://github.com/agentskillexchange/skills/blob/main/categories/README.md |
| wfseed-0025 | agentskillexchange/skills | manifest | Codex manifest | Codex skill catalog | high | true | https://github.com/agentskillexchange/skills/blob/main/codex.json |
| wfseed-0026 | agentskillexchange/skills | skill | Coordinate multi-agent workflows with Ruflo | multi-agent coding workflows | high | false | https://github.com/agentskillexchange/skills/tree/main/skills/coordinate-multi-agent-claude-code-and-codex-workflows-with-ruflo |
| wfseed-0027 | agentskillexchange/skills | lane | Data Platform & Analytics Engineering | data platform workflows | high | true | https://github.com/agentskillexchange/skills/blob/main/industries/data-platform-analytics-engineering.md |
| wfseed-0028 | agentskillexchange/skills | category | Developer Tools | 354 skills | high | true | https://github.com/agentskillexchange/skills/tree/main/categories/developer-tools |
| wfseed-0029 | agentskillexchange/skills | manifest | Full Catalog | 2,678 skills | high | true | https://github.com/agentskillexchange/skills/blob/main/CATALOG.md |
| wfseed-0030 | agentskillexchange/skills | category | Industry collections index | 15 industry overlays | high | true | https://github.com/agentskillexchange/skills/blob/main/industries/README.md |
| wfseed-0031 | agentskillexchange/skills | lane | Infrastructure, SRE & Incident Operations | SRE/incident operations | high | true | https://github.com/agentskillexchange/skills/blob/main/industries/infrastructure-sre-incident-operations.md |
| wfseed-0032 | agentskillexchange/skills | manifest | JSON Index | machine-readable catalog | high | true | https://github.com/agentskillexchange/skills/blob/main/skills.json |
| wfseed-0033 | agentskillexchange/skills | manifest | OpenClaw manifest | OpenClaw skill catalog | high | true | https://github.com/agentskillexchange/skills/blob/main/openclaw.json |
| wfseed-0034 | agentskillexchange/skills | skill | Orchestrate review-first multi-agent development work with Kandev | multi-agent development | high | false | https://github.com/agentskillexchange/skills/tree/main/skills/orchestrate-review-first-multi-agent-development-work-with-kandev |
| wfseed-0035 | agentskillexchange/skills | category | Research & Scraping | 116 skills | high | true | https://github.com/agentskillexchange/skills/tree/main/categories/research-scraping |
| wfseed-0036 | agentskillexchange/skills | skill | Run academic literature review and paper-output workflows with Aut Sci Write | research workflow | high | false | https://github.com/agentskillexchange/skills/tree/main/skills/run-academic-literature-review-and-paper-output-workflows-with-aut-sci-write |
| wfseed-0037 | agentskillexchange/skills | category | Security & Verification | 236 skills | high | true | https://github.com/agentskillexchange/skills/tree/main/categories/security-verification |
| wfseed-0038 | agentskillexchange/skills | lane | Security Operations & GRC Workflows | security/GRC workflows | high | true | https://github.com/agentskillexchange/skills/blob/main/industries/security-operations-grc-workflows.md |
| wfseed-0039 | agentskillexchange/skills | manifest | Skill spec | skill format | high | false | https://github.com/agentskillexchange/skills/blob/main/spec/SKILL_SPEC.md |
| wfseed-0040 | agentskillexchange/skills | template | Skill template | skill authoring | high | false | https://github.com/agentskillexchange/skills/blob/main/template/SKILL.md |
| wfseed-0041 | agentskillexchange/skills | category | Templates & Workflows | 191 skills | high | true | https://github.com/agentskillexchange/skills/tree/main/categories/templates-workflows |
| wfseed-0042 | ahacker-1/cre-agent-skills | category | Asset Management | commercial real estate asset management | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/asset-management |
| wfseed-0043 | ahacker-1/cre-agent-skills | category | Brokerage | brokerage workflows | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/brokerage |
| wfseed-0044 | ahacker-1/cre-agent-skills | category | CRE Due Diligence plugin pack | real estate due diligence package | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/plugins/cre-due-diligence |
| wfseed-0045 | ahacker-1/cre-agent-skills | category | Capital Markets | capital markets | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/capital-markets |
| wfseed-0046 | ahacker-1/cre-agent-skills | category | Closing | closing workflows | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/closing |
| wfseed-0047 | ahacker-1/cre-agent-skills | category | Document Ingestion | document processing | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/document-ingestion |
| wfseed-0048 | ahacker-1/cre-agent-skills | category | Due Diligence | real estate due diligence | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/due-diligence |
| wfseed-0049 | ahacker-1/cre-agent-skills | category | Financing | financing workflows | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/financing |
| wfseed-0050 | ahacker-1/cre-agent-skills | category | Industrial | industrial CRE | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/industrial |
| wfseed-0051 | ahacker-1/cre-agent-skills | category | Legal | legal review | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/legal |
| wfseed-0052 | ahacker-1/cre-agent-skills | category | Office | office CRE | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/office |
| wfseed-0053 | ahacker-1/cre-agent-skills | category | Skill Index | 66 CRE skills | high | true | https://github.com/ahacker-1/cre-agent-skills/blob/main/docs/SKILL-INDEX.md |
| wfseed-0054 | ahacker-1/cre-agent-skills | category | Underwriting | underwriting | high | true | https://github.com/ahacker-1/cre-agent-skills/tree/main/skills/underwriting |
| wfseed-0055 | api-evangelist/use-cases | category | Evidence and compliance vocabulary | public evidence, compliance support, earthquake-adjacent due diligence | high | false | https://github.com/api-evangelist/use-cases/blob/main/README.md |
| wfseed-0056 | api-evangelist/use-cases | manifest | JSON-LD context | structured vocabulary | high | false | https://github.com/api-evangelist/use-cases/tree/main/use-cases.jsonld |
| wfseed-0057 | api-evangelist/use-cases | manifest | apis.yml manifest | API/use-case manifest | high | false | https://github.com/api-evangelist/use-cases/blob/main/apis.yml |
| wfseed-0058 | ashishpatel26/500-AI-Agents-Projects | category | Agents directory | working agent implementations | high | true | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents |
| wfseed-0059 | ashishpatel26/500-AI-Agents-Projects | category | Agno Examples | agent examples | high | true | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agno-examples |
| wfseed-0060 | ashishpatel26/500-AI-Agents-Projects | category | AutoGen Notebooks | multi-agent notebooks | high | true | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/AutoGen-Examples |
| wfseed-0061 | ashishpatel26/500-AI-Agents-Projects | category | CrewAI Examples | agent examples | high | true | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/crewAI-examples |
| wfseed-0062 | ashishpatel26/500-AI-Agents-Projects | category | CrewAI MCP Course | agent course examples | high | true | https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/crewAI-MCP-Course |
| wfseed-0063 | ashishpatel26/500-AI-Agents-Projects | category | Industry Use Cases | healthcare, finance, education, real estate, retail, legal | high | true | https://github.com/ashishpatel26/500-AI-Agents-Projects/blob/main/README.md |
| wfseed-0064 | danielrosehill/Useful-AI-Agent-Skills | category | Scope and Curation Rules | catalog governance | high | true | https://github.com/danielrosehill/Useful-AI-Agent-Skills/blob/main/README.md |
| wfseed-0065 | enescingoz/awesome-n8n-templates | category | AI Research/RAG/Data Analysis | AI research/RAG/data analysis | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/AI Research & RAG & Data Analysis |
| wfseed-0066 | enescingoz/awesome-n8n-templates | category | Gmail/Email | email processing | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Gmail & Email |
| wfseed-0067 | enescingoz/awesome-n8n-templates | category | Google Drive/Sheets | document/spreadsheet automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Google Drive & Sheets |
| wfseed-0068 | enescingoz/awesome-n8n-templates | category | HR/Recruitment | HR workflows | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/HR & Recruitment |
| wfseed-0069 | enescingoz/awesome-n8n-templates | category | Notion | knowledge/workspace automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Notion |
| wfseed-0070 | enescingoz/awesome-n8n-templates | category | OpenAI and LLMs | LLM automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/OpenAI & LLMs |
| wfseed-0071 | enescingoz/awesome-n8n-templates | category | PDF Document Processing | document processing | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/PDF & Document Processing |
| wfseed-0072 | enescingoz/awesome-n8n-templates | category | README Catalog | 313 automation templates | high | true | https://github.com/enescingoz/awesome-n8n-templates/blob/main/README.md |
| wfseed-0073 | enescingoz/awesome-n8n-templates | category | Slack | team workflow automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Slack |
| wfseed-0074 | enescingoz/awesome-n8n-templates | category | Social Media | social workflows | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Social Media |
| wfseed-0075 | enescingoz/awesome-n8n-templates | category | Telegram | messaging automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/Telegram |
| wfseed-0076 | enescingoz/awesome-n8n-templates | category | WhatsApp | messaging automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/WhatsApp |
| wfseed-0077 | enescingoz/awesome-n8n-templates | category | WordPress | publishing automation | high | true | https://github.com/enescingoz/awesome-n8n-templates/tree/main/WordPress |
| wfseed-0078 | enescingoz/awesome-n8n-templates | category | docs/index.md | template index | high | true | https://github.com/enescingoz/awesome-n8n-templates/blob/main/docs/index.md |
| wfseed-0079 | enescingoz/awesome-n8n-templates | category | llms.txt | LLM-readable index | high | true | https://github.com/enescingoz/awesome-n8n-templates/blob/main/llms.txt |
| wfseed-0080 | indranilbanerjee/contentforge | category | AGENTS instructions | workflow operating rules | high | true | https://github.com/indranilbanerjee/contentforge/blob/main/AGENTS.md |
| wfseed-0081 | indranilbanerjee/contentforge | category | Commands directory | 9 command workflows | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/commands |
| wfseed-0082 | indranilbanerjee/contentforge | category | Education industry pack | education | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/skills/education |
| wfseed-0083 | indranilbanerjee/contentforge | category | Healthcare industry pack | healthcare | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/skills/healthcare |
| wfseed-0084 | indranilbanerjee/contentforge | category | Legal industry pack | legal | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/skills/legal |
| wfseed-0085 | indranilbanerjee/contentforge | category | Pharma industry pack | pharma | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/skills/pharma |
| wfseed-0086 | indranilbanerjee/contentforge | category | README skill catalog | industry content workflows | high | true | https://github.com/indranilbanerjee/contentforge/blob/main/README.md |
| wfseed-0087 | indranilbanerjee/contentforge | category | Real estate industry pack | real estate | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/skills/real-estate |
| wfseed-0088 | indranilbanerjee/contentforge | category | Skills directory | 21 skill packs | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/skills |
| wfseed-0089 | indranilbanerjee/contentforge | category | Templates | document templates | high | true | https://github.com/indranilbanerjee/contentforge/tree/main/templates |
| wfseed-0090 | jim-schwoebel/awesome_ai_agents | category | Real Estate Agents | real estate | high | true | https://github.com/jim-schwoebel/awesome_ai_agents/blob/main/README.md |
| wfseed-0091 | marieai/marie-ai | category | Agentic document intelligence docs | document intelligence | high | true | https://github.com/marieai/marie-ai/blob/main/README.md |
| wfseed-0092 | marieai/marie-ai | category | Core query pipeline | query pipeline | high | true | https://github.com/marieai/marie-ai/tree/main/marie/core |
| wfseed-0093 | marieai/marie-ai | category | DAG workflows | DAG workflows | high | true | https://github.com/marieai/marie-ai/tree/main/marie/workflows |
| wfseed-0094 | marieai/marie-ai | category | Document pipelines guide | document processing | high | true | https://github.com/marieai/marie-ai/blob/main/docs/document-pipelines.md |
| wfseed-0095 | marieai/marie-ai | category | Executor pipeline | execution pipeline | high | true | https://github.com/marieai/marie-ai/tree/main/marie/executor |
| wfseed-0096 | marieai/marie-ai | category | Executor template | runtime template | high | true | https://github.com/marieai/marie-ai/tree/main/executor/template |
| wfseed-0097 | marieai/marie-ai | category | Extract Engine | document extraction | high | true | https://github.com/marieai/marie-ai/tree/main/marie/extract |
| wfseed-0098 | marieai/marie-ai | category | Flows guide | workflow orchestration | high | true | https://github.com/marieai/marie-ai/blob/main/docs/flows.md |
| wfseed-0099 | marieai/marie-ai | category | Form extraction | forms | high | true | https://github.com/marieai/marie-ai/tree/main/examples/form-extraction |
| wfseed-0100 | marieai/marie-ai | category | Invoice processing | invoices | high | true | https://github.com/marieai/marie-ai/tree/main/examples/invoice-processing |
| wfseed-0101 | marieai/marie-ai | category | Marie MCP | MCP/runtime integration | high | true | https://github.com/marieai/marie-ai/tree/main/mcp |
| wfseed-0102 | marieai/marie-ai | category | Orchestrate flow | orchestration | high | true | https://github.com/marieai/marie-ai/tree/main/marie/orchestrate |
| wfseed-0103 | marieai/marie-ai | category | Project template | project template | high | true | https://github.com/marieai/marie-ai/tree/main/template |
| wfseed-0104 | marieai/marie-ai | category | Query planners | retrieval/query planning | high | true | https://github.com/marieai/marie-ai/tree/main/marie/query_planner |
| wfseed-0105 | marieai/marie-ai | category | Template matching | document extraction | high | true | https://github.com/marieai/marie-ai/tree/main/marie/template_matching |
| wfseed-0106 | marieai/marie-ai | category | Workspaces | workspace processing | high | true | https://github.com/marieai/marie-ai/blob/main/docs/workspaces.md |
| wfseed-0107 | mergisi/awesome-openclaw-agents | category | Claude skills | model skill pack | high | true | https://github.com/mergisi/awesome-openclaw-agents/tree/main/skills/claude |
| wfseed-0108 | mergisi/awesome-openclaw-agents | category | Configs | configuration templates | high | true | https://github.com/mergisi/awesome-openclaw-agents/tree/main/configs |
| wfseed-0109 | mergisi/awesome-openclaw-agents | category | Gemma skills | model skill pack | high | true | https://github.com/mergisi/awesome-openclaw-agents/tree/main/skills/gemma |
| wfseed-0110 | mergisi/awesome-openclaw-agents | category | Memory wiki templates | knowledge workflows | high | true | https://github.com/mergisi/awesome-openclaw-agents/tree/main/memory-wiki |
| wfseed-0111 | mergisi/awesome-openclaw-agents | category | Quickstart | setup workflow | high | true | https://github.com/mergisi/awesome-openclaw-agents/blob/main/QUICKSTART.md |
| wfseed-0112 | mergisi/awesome-openclaw-agents | category | README Catalog | multi-industry OpenClaw templates | high | true | https://github.com/mergisi/awesome-openclaw-agents/blob/main/README.md |
| wfseed-0113 | mergisi/awesome-openclaw-agents | category | USE-CASES | education, healthcare, legal, real estate, compliance, automation | high | true | https://github.com/mergisi/awesome-openclaw-agents/blob/main/USE-CASES.md |
| wfseed-0114 | mergisi/awesome-openclaw-agents | category | agents category index | category index | high | true | https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/README.md |
| wfseed-0115 | mergisi/awesome-openclaw-agents | category | agents.json | machine-readable agent templates | high | true | https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents.json |
| wfseed-0116 | mergisi/awesome-openclaw-agents | category | skills README | skill packs | high | true | https://github.com/mergisi/awesome-openclaw-agents/blob/main/skills/README.md |
| wfseed-0117 | msitarzewski/agency-agents | manifest | Divisions manifest | agent taxonomy | high | true | https://github.com/msitarzewski/agency-agents/blob/main/divisions.json |
| wfseed-0118 | msitarzewski/agency-agents | category | Engineering division | engineering agents | high | true | https://github.com/msitarzewski/agency-agents/tree/main/agents/engineering |
| wfseed-0119 | msitarzewski/agency-agents | category | Specialized division | domain agents | high | true | https://github.com/msitarzewski/agency-agents/tree/main/agents/specialized |
| wfseed-0120 | msitarzewski/agency-agents | category | Strategy playbooks | business strategy workflows | high | true | https://github.com/msitarzewski/agency-agents/tree/main/strategy |
| wfseed-0121 | msitarzewski/agency-agents | manifest | Tools manifest | tool taxonomy | high | true | https://github.com/msitarzewski/agency-agents/blob/main/tools.json |
| wfseed-0122 | ritik-prog/n8n-automation-templates-5000 | category | CRM | sales/CRM automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/CRM |
| wfseed-0123 | ritik-prog/n8n-automation-templates-5000 | category | Google | Google workspace automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Google |
| wfseed-0124 | ritik-prog/n8n-automation-templates-5000 | category | HubSpot | CRM automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/HubSpot |
| wfseed-0125 | ritik-prog/n8n-automation-templates-5000 | category | Moodle | education automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Moodle |
| wfseed-0126 | ritik-prog/n8n-automation-templates-5000 | category | Notion | knowledge automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Notion |
| wfseed-0127 | ritik-prog/n8n-automation-templates-5000 | category | OpenAI | LLM automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/OpenAI |
| wfseed-0128 | ritik-prog/n8n-automation-templates-5000 | category | Salesforce | CRM automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Salesforce |
| wfseed-0129 | ritik-prog/n8n-automation-templates-5000 | category | Security Monitoring | monitoring workflows | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/blob/main/README.md |
| wfseed-0130 | ritik-prog/n8n-automation-templates-5000 | category | Slack | team workflow automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Slack |
| wfseed-0131 | ritik-prog/n8n-automation-templates-5000 | category | Templates based on platforms lane | 2,000 workflows | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms |
| wfseed-0132 | ritik-prog/n8n-automation-templates-5000 | category | Zillow | real estate automation | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/Templates based on paltforms/Zillow |
| wfseed-0133 | ritik-prog/n8n-automation-templates-5000 | category | n8n advance lane | 204 workflows | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/n8n advance |
| wfseed-0134 | ritik-prog/n8n-automation-templates-5000 | category | n8n_2000_workflows lane | 2,001 workflows | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/n8n_2000_workflows |
| wfseed-0135 | ritik-prog/n8n-automation-templates-5000 | category | workflows by Zie619 lane | 2,055 workflows | high | true | https://github.com/ritik-prog/n8n-automation-templates-5000/tree/main/workflows by Zie619 |
| wfseed-0136 | sickn33/antigravity-awesome-skills | template | AAS Agent & MCP Builder | agent/MCP/eval builder | high | false | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins/antigravity-bundle-aas-agent-mcp-builder |
| wfseed-0137 | sickn33/antigravity-awesome-skills | template | AAS Security Engineer | security audit | high | false | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins/antigravity-bundle-aas-security-engineer |
| wfseed-0138 | sickn33/antigravity-awesome-skills | template | AAS Web App Builder | web app building | high | false | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins/antigravity-bundle-aas-web-app-builder |
| wfseed-0139 | sickn33/antigravity-awesome-skills | category | Bundles index | role bundles | high | false | https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md |
| wfseed-0140 | sickn33/antigravity-awesome-skills | workflow | Design a DDD Core Domain | architecture | high | false | https://github.com/sickn33/antigravity-awesome-skills/blob/main/data/workflows.json |
| wfseed-0141 | sickn33/antigravity-awesome-skills | manifest | Full skill catalog | 1,898+ skills | high | true | https://github.com/sickn33/antigravity-awesome-skills/blob/main/CATALOG.md |
| wfseed-0142 | sickn33/antigravity-awesome-skills | manifest | Machine-readable bundles | bundle metadata | high | false | https://github.com/sickn33/antigravity-awesome-skills/blob/main/data/bundles.json |
| wfseed-0143 | sickn33/antigravity-awesome-skills | manifest | Plugin marketplace manifest | Codex config package bundles | high | false | https://github.com/sickn33/antigravity-awesome-skills/blob/main/.agents/plugins/marketplace.json |
| wfseed-0144 | sickn33/antigravity-awesome-skills | manifest | Skills index | machine-readable skills | high | true | https://github.com/sickn33/antigravity-awesome-skills/blob/main/skills_index.json |
| wfseed-0145 | sickn33/antigravity-awesome-skills | workflow | Workflows index | ordered execution playbooks | high | false | https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md |
| wfseed-0146 | sickn33/antigravity-awesome-skills | template | plugins/ | generated plugin bundles | high | true | https://github.com/sickn33/antigravity-awesome-skills/tree/main/plugins |
| wfseed-0147 | sickn33/antigravity-awesome-skills | category | skills/ | installable skill folders | high | true | https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills |
| wfseed-0148 | tinh2/skills-hub-registry | workflow | /analyze | cross-layer analysis | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/analysis/analyze |
| wfseed-0149 | tinh2/skills-hub-registry | workflow | /arch-review | architecture review | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/review/arch-review |
| wfseed-0150 | tinh2/skills-hub-registry | workflow | /build | full app build pipeline | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/build/build |
| wfseed-0151 | tinh2/skills-hub-registry | workflow | /devops | deployment orchestrator | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/deploy/devops |
| wfseed-0152 | tinh2/skills-hub-registry | workflow | /document | documentation/document transformation orchestrator | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/docs/document |
| wfseed-0153 | tinh2/skills-hub-registry | workflow | /dx | developer experience orchestrator | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/productivity/dx |
| wfseed-0154 | tinh2/skills-hub-registry | workflow | /integrate | integration orchestrator | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/integration/integrate |
| wfseed-0155 | tinh2/skills-hub-registry | workflow | /qa | automated QA pipeline | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/qa/qa |
| wfseed-0156 | tinh2/skills-hub-registry | workflow | /secure | security orchestrator | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/security/secure |
| wfseed-0157 | tinh2/skills-hub-registry | workflow | /test-suite | testing orchestrator | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/test/test-suite |
| wfseed-0158 | tinh2/skills-hub-registry | workflow | /ux | UX audit/design validation | high | false | https://github.com/tinh2/skills-hub-registry/tree/main/ux/ux |
| wfseed-0159 | tinh2/skills-hub-registry | manifest | README Skill Catalog | 430 skills | high | true | https://github.com/tinh2/skills-hub-registry/blob/main/README.md |
| wfseed-0160 | tinh2/skills-hub-registry | category | analysis | domain analysis/research/industry verticals | high | true | https://github.com/tinh2/skills-hub-registry/tree/main/analysis |
| wfseed-0161 | tinh2/skills-hub-registry | category | build | project scaffolding/build pipelines | high | true | https://github.com/tinh2/skills-hub-registry/tree/main/build |
| wfseed-0162 | tinh2/skills-hub-registry | category | combo | multi-skill chains | high | true | https://github.com/tinh2/skills-hub-registry/tree/main/combo |
| wfseed-0163 | tinh2/skills-hub-registry | workflow | compliance-suite | compliance-support chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/compliance-suite |
| wfseed-0164 | tinh2/skills-hub-registry | workflow | design-to-code | multi-skill chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/design-to-code |
| wfseed-0165 | tinh2/skills-hub-registry | workflow | fix-and-ship | multi-skill chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/fix-and-ship |
| wfseed-0166 | tinh2/skills-hub-registry | workflow | mvp-spec | multi-skill chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/mvp-spec |
| wfseed-0167 | tinh2/skills-hub-registry | category | qa | quality assurance | high | true | https://github.com/tinh2/skills-hub-registry/tree/main/qa |
| wfseed-0168 | tinh2/skills-hub-registry | workflow | review-implement | multi-skill chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/review-implement |
| wfseed-0169 | tinh2/skills-hub-registry | workflow | secure-ship | multi-skill chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/secure-ship |
| wfseed-0170 | tinh2/skills-hub-registry | workflow | ship-pipeline | multi-skill chain | medium | false | https://github.com/tinh2/skills-hub-registry/tree/main/combo/ship-pipeline |
| wfseed-0171 | tinh2/skills-hub-registry | category | test | automated testing | high | true | https://github.com/tinh2/skills-hub-registry/tree/main/test |
