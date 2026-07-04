# Six-Agent Real-World Agent Repos Directory

Date: 2026-07-03

## Purpose

Six research lanes were run to find real-world agent, skill, workflow, and repository examples across domains. The point is not just to collect repos. The point is to learn how to recognize problems that are good candidates for agentic systems.

## Core Question

How do I identify a problem that can be solved by an agent, skill, or skill suite?

Use this sentence:

```text
When I receive [input], I need to check [sources/rules],
perform [steps/tools], and produce [artifact],
but stop before [human decision boundary].
```

If you can fill that in clearly, the problem is probably a good candidate.

## Six Research Agents

| Agent lane | Domain cluster | What it searched for |
|---|---|---|
| Agent 1 | Education and learning | Tutor systems, grading, course generation, learning analytics, education skills |
| Agent 2 | Healthcare and life sciences | Medical research, healthcare admin, clinical ASR, DICOM, prior auth, pharma |
| Agent 3 | Real estate, construction, geospatial | Property analysis, CRE, zoning, BIM, construction docs, site analysis |
| Agent 4 | Finance, legal, compliance, insurance, government | Due diligence, contract review, claims, underwriting, AML, filings, policy ops |
| Agent 5 | Business operations and engineering ops | Support, GTM, recruiting, product management, marketing, SRE, security ops |
| Agent 6 | Cross-domain platforms and directories | Skill specs, official examples, vendor skill repos, marketplaces, MCP/tool layers |

## How To Study These Repos

For each repo, ask:

1. What is the repeated professional job?
2. What is the input?
3. What sources, tools, APIs, files, or standards does it use?
4. What artifact does it produce?
5. What is the human review boundary?
6. Is it a single skill, a suite of skills, a team of agents, an MCP/tool layer, or a full app?

The best repos have a clear artifact: verification table, risk report, underwriting packet, incident report, course package, support routing decision, zoning result, DICOM output, audit packet, or generated PRD.

## Agent 1 - Education And Learning

| Repo | Real-world problem | Workflow pattern | Study note |
|---|---|---|---|
| [GarethManning/education-agent-skills](https://github.com/GarethManning/education-agent-skills) | Reusable education-specific agent behavior for teachers, designers, and learners | `SKILL.md` library across pedagogical domains | Strongest pure education skills reference |
| [DaRL-GenAI/instructional_agents](https://github.com/DaRL-GenAI/instructional_agents) | Reduce faculty workload for course design and material production | Multi-agent ADDIE workflow with copilot checkpoints | Serious course-generation pipeline |
| [ai-shifu/skills](https://github.com/ai-shifu/skills) | Turn raw materials into live 1:1 AI-Shifu courses | Course creator and course direction advisor skills | Good production workflow contract |
| [ahmedEid1/lumen](https://github.com/ahmedEid1/lumen) | Generate private courses and scoped tutor experiences | Multi-agent authoring orchestrator, tutor agents, RAG, evals | Production-like education platform |
| [cepdnaclk/e20-4yp-ai-driven-automated-feedback-and-tutoring-system-for-higher-education](https://github.com/cepdnaclk/e20-4yp-ai-driven-automated-feedback-and-tutoring-system-for-higher-education) | Automate assignment ingestion, grading, and feedback | Moodle REST, multi-agent grading engine | Practical education-ops automation |
| [mvallet91/JELAI](https://github.com/mvallet91/JELAI) | Add tutor support and telemetry to JupyterHub learning | Tutor agent, expert agent, prompt files, telemetry pipeline | Classroom coding environment pattern |
| [Schlaflied/Plot-Ark](https://github.com/Schlaflied/Plot-Ark) | Detect at-risk learners and generate reports | A2A multi-agent pipeline, xAPI, knowledge graph/RAG | Education analytics beyond tutoring |
| [A-R007/Multi-Agent-Study-Assistant](https://github.com/A-R007/Multi-Agent-Study-Assistant) | Adaptive study roadmaps, quizzes, tutoring, document Q&A | Six specialized agents with RAG | Compact learner-facing multi-agent app |
| [Man0dya/Tutor-AI](https://github.com/Man0dya/Tutor-AI) | Generate study content, question sets, and feedback | FastAPI agents, React UI, vector search | Separates agent backend from learner UI |
| [jtangen/classbuild](https://github.com/jtangen/classbuild) | Turn one topic into editable course materials | Prompt builders for syllabus, chapters, quizzes, slides | Strong generated-artifact workflow |
| [rebornstar1/InstructAI](https://github.com/rebornstar1/InstructAI) | Generate courses, track progress, personalize content | Full-stack course builder and analytics | Useful full-stack education app structure |
| [EdFife/HTML-as-JSON](https://github.com/EdFife/HTML-as-JSON) | Avoid broken LMS imports from direct LLM course generation | HTML as structured intermediate layer | Reliability-through-data-structure pattern |
| [Imsharad/building-agents](https://github.com/Imsharad/building-agents) | Review complex technical student submissions at scale | Multi-agent assessment framework | Grading technical projects at scale |
| [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) | Help academics build practical AI workflows | Downloadable skills, agents, templates, starter plugin | Academic operations reference |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | Literature review, research design, writing, Zotero workflows | Portable `SKILL.md` catalog | Academic/research education operations |

## Agent 2 - Healthcare, Life Sciences, And Medical Research

| Repo | Real-world problem | Workflow pattern | Study note |
|---|---|---|---|
| [ajhcs/healthcare-agents](https://github.com/ajhcs/healthcare-agents) | US healthcare admin across revenue cycle, payer, compliance, quality | 51 specialist Markdown agents and `SKILL.md` installs | Strong healthcare admin packaging |
| [Aperivue/medsci-skills](https://github.com/Aperivue/medsci-skills) | Clinical research lifecycle and manuscript support | 52 skills, orchestrator, reporting-guideline gates | Best medical research integrity pattern |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | Evidence discovery, protocol design, data analysis, academic writing | 550+ medical research skills | Broad medical skill taxonomy |
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | Biomedical and clinical research assistance | 869 `SKILL.md` modules | Large medical skill atlas |
| [K-Dense-AI/scientific-agent-skills](https://github.com/k-dense-ai/scientific-agent-skills) | Scientific workflows across biology, chemistry, medicine, imaging | 148 agent skills, database/tool connectors | Cross-domain scientific architecture |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | Bioinformatics and life-science coding workflows | 199 `SKILL.md` files with examples | Strong computational biology packaging |
| [RConsortium/pharma-skills](https://github.com/RConsortium/pharma-skills) | Biopharma R&D, clinical trials, submissions, statistics | Skill folders with benchmark lifecycle | Regulated pharma workflow discipline |
| [aws-samples/amazon-bedrock-agents-healthcare-lifesciences](https://github.com/aws-samples/amazon-bedrock-agents-healthcare-lifesciences) | Drug research, trials, genomics, terminology, HCLS workflows | Reference agents, skills, MCP servers | Enterprise HCLS toolkit pattern |
| [snap-stanford/biomni](https://github.com/snap-stanford/biomni) | Biomedical research agent for hypothesis and data analysis | Retrieval planning, code execution, biomedical tools | Agent as research operator |
| [microsoft/Prior-Authorization-Multi-Agent-Solution-Accelerator](https://github.com/microsoft/Prior-Authorization-Multi-Agent-Solution-Accelerator) | Payer-side prior authorization review | Compliance, clinical reviewer, coverage, synthesis agents | Strong full-stack healthcare ops example |
| [pablosalvador10/gbb-ai-hls-factory-prior-auth](https://github.com/pablosalvador10/gbb-ai-hls-factory-prior-auth) | Prior-auth packet processing and decision support | OCR, retrieval, policy reasoning pipeline | Modular PA processing workflow |
| [NVIDIA/digital-health-skills](https://github.com/NVIDIA/digital-health-skills) | Clinical ASR evaluation and adaptation | Four staged skills with WER/CER/KER/SER evaluation | Best clinical ASR skill packaging |
| [NVIDIA-AI-Blueprints/ambient-healthcare-agents](https://github.com/NVIDIA-AI-Blueprints/ambient-healthcare-agents) | Ambient clinical voice documentation and patient voice agent | ASR/TTS, diarization, SOAP note generation | Voice agent architecture |
| [Google-Health/medasr](https://github.com/google-health/medasr) | Healthcare-domain ASR usage and fine-tuning | Model repo with notebooks and docs | Model grounding for ASR workflows |
| [CCI-Bonn/OHIF-AI](https://github.com/CCI-Bonn/OHIF-AI) | DICOM imaging segmentation and reporting | OHIF viewer plus AI segmentation/reporting | DICOM UI and workflow reference |
| [Google-Health/medgemma](https://github.com/google-health/medgemma) | Medical text/image comprehension and EHR navigation | Model notebooks, EHR navigator example | Medical multimodal workflow reference |
| [elisaterumi-ai/clinical-agent-skills](https://github.com/elisaterumi-ai/clinical-agent-skills) | Clinical NLP: anonymization, NER, summaries, coding, timelines | Modular `/skills` directory | Privacy-first clinical skill decomposition |

## Agent 3 - Real Estate, Construction, Architecture, Geospatial

| Repo | Real-world problem | Workflow pattern | Study note |
|---|---|---|---|
| [zubair-trabzada/ai-realestate-claude](https://github.com/zubair-trabzada/ai-realestate-claude) | Property analysis, comps, rental income, investment signal, PDF reports | 15 skills, 5 parallel analysis agents | Vertical skill-orchestrator pattern |
| [ahacker-1/cre-agent-skills](https://github.com/ahacker-1/cre-agent-skills) | CRE underwriting, diligence, financing, brokerage, legal, closing | Standalone prompt/skill library | CRE workflow decomposition |
| [ahacker-1/cre-acquisition-orchestrator](https://github.com/ahacker-1/cre-acquisition-orchestrator) | Multifamily/CRE acquisition diligence and closing | 31 named AI roles, schemas, dashboard, simulation | Agentic CRE operating-system pattern |
| [hoangtng/real-estate-agents](https://github.com/hoangtng/real-estate-agents) | CMA, offers, underwriting, marketing, compliance | Agent personas plus `SKILL.md` deliverables | Very studyable agent + skill pairing |
| [brightdata/real-estate-ai-agent](https://github.com/brightdata/real-estate-ai-agent) | Structured extraction from real-estate listing sites | CrewAI, Bright Data MCP, schema JSON extraction | Property data-ingestion pattern |
| [Josephrp/EasyRealEstate](https://github.com/Josephrp/EasyRealEstate) | Real estate investment planning in Italy | Multi-agent group chat with planner and finance agent | Lightweight investment analysis split |
| [datadrivenconstruction/DDC_Skills_for_AI_Agents_in_Construction](https://github.com/datadrivenconstruction/DDC_Skills_for_AI_Agents_in_Construction) | Construction automation: BIM, cost, scheduling, docs | 221 `SKILL.md` files | Construction skill-library scale |
| [datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR) | Construction cost estimation and cost DB search | Qdrant plus n8n AI workflows | RAG + estimating workflow |
| [datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN](https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN) | Convert CAD/BIM formats into machine-readable data | Agent workflow around local converters | AEC file-to-data bridge |
| [hamzaabduljabbar/construction-drawing-analyzer](https://github.com/hamzaabduljabbar/construction-drawing-analyzer) | Read and classify construction drawing sets | Claude skill plus Python scripts | Narrow construction-doc automation |
| [dcy0577/Text2BIM](https://github.com/dcy0577/Text2BIM) | Generate editable BIM models from natural language | Multi-agent framework writes BIM API code | BIM agent collaboration |
| [hzlbbfrog/Generative-BIM](https://github.com/hzlbbfrog/Generative-BIM) | Structural design pipeline with BIM and generative AI | Four-stage BIM/design/evaluation pipeline | BIM pipeline decomposition |
| [opengeos/GeoAgent](https://github.com/opengeos/GeoAgent) | Geospatial analysis and visualization via LLM tools | Geospatial Python/QGIS/STAC/NASA tools exposed to agent | Best GIS agent framework in lane |
| [aws-samples/sample-geospatial-code-agent](https://github.com/aws-samples/sample-geospatial-code-agent) | Natural-language satellite imagery analysis over map polygons | Agent writes/runs Python and returns overlays/statistics | Site-selection/hazard analysis pattern |
| [melbamorph/zoner](https://github.com/melbamorph/zoner) | Public zoning assistant | ChatKit app plus Agent Builder workflow | Zoning assistant UI pattern |
| [melbamorph/zonerMCP](https://github.com/melbamorph/zonerMCP) | GIS/zoning lookup tool layer | Hardened MCP server over ArcGIS zoning data | Permitting/zoning MCP pattern |
| [tmoody1973/mkedev](https://github.com/tmoody1973/mkedev) | Milwaukee zoning, parcels, development sites | Voice/vision platform with zoning interpreter and 22 tools | Local-government property development example |
| [AlpacaLabsLLC/skills-for-architects](https://github.com/AlpacaLabsLLC/skills-for-architects) | Architecture, real estate, workplace strategy skills | Built-environment `SKILL.md` repo | Domain-specific skill distribution |

## Agent 4 - Finance, Legal, Compliance, Insurance, Government

| Repo | Real-world problem | Workflow pattern | Study note |
|---|---|---|---|
| [zoharbabin/due-diligence-agents](https://github.com/zoharbabin/due-diligence-agents) | M&A due diligence across 9 domains | Parallel workstreams, cross-reference graph, reports/Excel/JSON | Strongest diligence artifact chain |
| [aws-samples/sample-ma-due-diligence-agentcore](https://github.com/aws-samples/sample-ma-due-diligence-agentcore) | M&A due diligence in transportation/logistics | Supervisor agent routes to specialist agents | Production-adjacent AWS architecture |
| [anthropics/claude-for-legal](https://github.com/anthropics/claude-for-legal) | Legal workflows with attorney-review guardrails | Plugin/skill suite with citations and human gates | Professional-boundary design |
| [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill) | Contract review, risk detection, redlines, negotiation prep | CUAD categories, benchmark caveats, redline handoff | Compact legal skill example |
| [alisoliman/insurance-multi-agent](https://github.com/alisoliman/insurance-multi-agent) | Insurance claims processing | Claim assessor, policy checker, risk analyst, communication agent | Claims-workbench role split |
| [AstitvaAdrosonic/InsureIQ](https://github.com/AstitvaAdrosonic/InsureIQ) | Insurance underwriting submissions | Email intake, audit agent, risk agents, underwriter review | Strong intake-to-review chain |
| [vijayyarabolu/insurance-underwriting-agent](https://github.com/vijayyarabolu/insurance-underwriting-agent) | Underwriting decision support | Deterministic hard stops plus LLM rationale | Regulated fail-closed pattern |
| [mongodb-industry-solutions/fsi-aml-fraud-detection](https://github.com/mongodb-industry-solutions/fsi-aml-fraud-detection) | AML/KYC fraud detection and SAR investigations | Six-agent SAR pipeline plus tools | Compliance investigation workflow |
| [microsoft/azure-trust-agents](https://github.com/microsoft/azure-trust-agents) | Financial compliance monitoring and fraud alerts | Data agent, risk analyzer, compliance report, fraud alert | Enterprise risk/report split |
| [Snowflake-Labs/sfguide-agentic-ai-for-asset-management](https://github.com/Snowflake-Labs/sfguide-agentic-ai-for-asset-management) | Asset-management risk and compliance reporting | Agent orchestrates holdings, policies, regulations, PDF report | Audit-ready report model |
| [DEFRA/ai-agents-policy-writeup](https://github.com/DEFRA/ai-agents-policy-writeup) | Government policy operations | LangGraph parliamentary question and letters workflows | Public-sector synthesis under constraints |
| [cmdrvl/cmdrvl-xew](https://github.com/cmdrvl/cmdrvl-xew) | SEC/XBRL filing early-warning checks | Deterministic CLI, schemas, Evidence Packs | Artifact discipline reference |
| [cyanheads/secedgar-mcp-server](https://github.com/cyanheads/secedgar-mcp-server) | SEC EDGAR filings and XBRL financial data for agents | MCP server with SEC tools/resources/prompts | Finance tool layer |
| [jagmarques/asqav-compliance](https://github.com/jagmarques/asqav-compliance) | AI-agent governance checks in CI/CD | GitHub Action scans PRs for oversight/audit gaps | Compliance-as-code pattern |
| [verifywise-ai/verifywise](https://github.com/verifywise-ai/verifywise) | AI governance, GRC, evidence, incidents | Risk/control mappings and evidence center | Governance artifact taxonomy |
| [rfrod/compliance_mcp](https://github.com/rfrod/compliance_mcp) | Fraud and AML counterparty screening | MCP tools for transaction lookup and screening | Small compliance tool surface |
| [marc-shade/fraud-detection-mcp](https://github.com/marc-shade/fraud-detection-mcp) | Fraud/anomaly detection and transaction protection | MCP server with fraud tools and ML ensemble | Tool-surface design for fraud |

## Agent 5 - Business Operations, GTM, Support, Product, DevOps

| Repo | Real-world problem | Workflow pattern | Study note |
|---|---|---|---|
| [dandye/ai-runbooks](https://github.com/dandye/ai-runbooks) | Security alert triage, IOC enrichment, threat hunting, IR | Runbooks, personas, reports, IRPs | Strong ops artifact repo |
| [J-Staff/mistral-workflow-support-triage](https://github.com/J-Staff/mistral-workflow-support-triage) | Customer support email triage | Durable workflow package with sample JSONs | Typed workflow packaging |
| [nick-railsback/fulfillment-triage-agents](https://github.com/nick-railsback/fulfillment-triage-agents) | E-commerce fulfillment support triage | Multi-agent intake, scoring, routing, verification | Human-in-loop support routing |
| [agentlifylabs/agents](https://github.com/agentlifylabs/agents/blob/main/multi-step/support-triage-agent.md) | Support ticket classification and routing | Multi-step prompt workflow | Clean prompt-only triage decomposition |
| [Prospeda/gtm-skills](https://github.com/Prospeda/gtm-skills) | B2B sales, GTM research, outreach, HubSpot workflows | `SKILL.md`, GTM folders, SDR agents | Sales workflow packaging |
| [kaymen99/sales-outreach-automation-langgraph](https://github.com/kaymen99/sales-outreach-automation-langgraph) | Sales lead research and personalized outreach | LangGraph pipeline with report outputs | Outreach artifacts and pipeline |
| [kevins981/recruiting-admin-prompts](https://github.com/kevins981/recruiting-admin-prompts) | Recruiter prep, intake notes, sourcing, candidate research | Prompt library | Bounded HR/recruiting automation |
| [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills) | Product docs, discovery, prioritization, PRDs, strategy | Many `skills/*/SKILL.md`, examples, templates | Strong PM skill library |
| [Digidai/product-manager-skills](https://github.com/Digidai/product-manager-skills) | PM coaching, PRDs, roadmap, discovery, SaaS diagnostics | Single installable skill plus templates/examples | Compact PM skill example |
| [AICMO/AiCMO-Marketing-Prompt-Collection](https://github.com/AICMO/AiCMO-Marketing-Prompt-Collection) | Marketing strategy, reporting, product marketing, content ops | Department-organized prompt catalog and skills | Marketing-ops taxonomy |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Copilot instructions, skills, agents, code/security workflows | `.github/agents`, `skills/*/SKILL.md`, docs | Official packaging reference |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Engineering quality, code review, security, testing, CI/CD | Agents plus skills | Excellent developer-ops structure |
| [wshobson/agents](https://github.com/wshobson/agents) | Engineering, DevOps, incident response, code review | Plugin folders with agents, skills, commands | Broad technical ops library |
| [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) | Incident command, code review, security audit, growth agents | Agents and skills across `.claude` and `.codex` | Incident commander/postmortem template |
| [jbrahy/meta-agent-teams](https://github.com/jbrahy/meta-agent-teams) | Operational teams for marketing, DevOps, customer success, AE, PM | Team/agent system prompts and evals | Whole-team packaging pattern |
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | Cross-functional agency roles for engineering, marketing, reporting | Agent markdown, playbooks, examples | Deliverable-focused personas |
| [freddy-schuetz/n8n-claw-agents](https://github.com/freddy-schuetz/n8n-claw-agents) | n8n automation expert agents | Manifest and persona files | Automation agent manifest pattern |

## Agent 6 - Cross-Domain Platforms, Specs, Directories, Tool Layers

| Repo | Real-world problem | Workflow pattern | Study note |
|---|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Core Agent Skills specification | `SKILL.md`, scripts, references, assets | Baseline schema |
| [anthropics/skills](https://github.com/anthropics/skills) | Official agent skill examples | Self-contained skill folders | Canonical skill structure |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | GitHub Copilot skill directory | Skill folders with scripts/templates/reference data | Copilot-style packaging |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | Cross-platform skill directory | Awesome-list catalog | Discovery index, not trusted dependency |
| [NVIDIA/skills](https://github.com/NVIDIA/skills) | NVIDIA skill catalog | Product skills mirrored into catalog | Enterprise-scale distribution |
| [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills) | Gemini API/SDK/model interaction skills | Provider-authored API skills | Solves fast-moving docs problem |
| [vercel/ai](https://github.com/vercel/ai/tree/main/skills) | Vercel AI SDK repo-local skills | Skill forces agents to verify bundled docs/source | Repo-local SDK skill pattern |
| [cloudflare/skills](https://github.com/cloudflare/skills) | Cloudflare platform skills | Cross-agent install paths | Developer-platform skill layer |
| [stripe/ai](https://github.com/stripe/ai) | Payments/business integration skills | Official skills and plugins | High-risk integration guidance |
| [Shopify/agent-skills](https://github.com/Shopify/agent-skills) | Shopify API ecosystem skills | Generated skills plus validation scripts | Validation tools bundled with skills |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | Supabase backend/database skills | Installable Agent Skills format | Database/backend platform pattern |
| [aws-samples/sample-agent-skills](https://github.com/aws-samples/sample-agent-skills) | Office/PDF document handling in agentic IDEs | Skills plus Python/`uv` executable support | Non-code workplace automation |
| [aws-samples/sample-code-for-devops-agent-skills](https://github.com/aws-samples/sample-code-for-devops-agent-skills) | DevOps/SRE incident response and RCA | Runbooks, decision trees, MCP tool guidance, evals | SRE playbook skills |
| [cloudflare/agent-skills-discovery-rfc](https://github.com/cloudflare/agent-skills-discovery-rfc) | Remote skill discovery via `.well-known` | Skill index and progressive disclosure | Marketplace/discovery architecture |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | MCP reference servers and community pointers | Tool/server examples | Adjacent tool layer |
| [openai/openai-agents-js](https://github.com/openai/openai-agents-js) | OpenAI Agents SDK examples | Agents, tools, guardrails, handoffs, tracing | Executable agent workflow layer |
| [microsoft/Agent-Framework-Samples](https://github.com/microsoft/Agent-Framework-Samples) | Microsoft Agent Framework samples | Python/.NET tutorials and examples | Enterprise agent patterns outside SKILL.md |
| [openai/openai-apps-sdk-examples](https://github.com/openai/openai-apps-sdk-examples) | ChatGPT Apps SDK examples | MCP server plus UI widget examples | Agent skill to tool to UI bridge |

## Cross-Domain Patterns

### Pattern 1 - Audit Skill

The agent checks something against rules and returns a status table.

Examples:

- references against PubMed/CrossRef;
- manuscript against reporting guidelines;
- contract against playbook;
- PR against security checks;
- AI agent repo against governance controls.

### Pattern 2 - Evidence Packet

The agent gathers sources, extracts evidence, and produces a human-reviewable packet.

Examples:

- referral packet;
- prior-auth packet;
- M&A due diligence packet;
- underwriting packet;
- property investment packet;
- disaster-risk packet.

### Pattern 3 - Triage And Routing

The agent classifies incoming work, scores urgency/risk, and routes it.

Examples:

- support ticket triage;
- fulfillment issue routing;
- security alert triage;
- claims triage;
- student assignment feedback routing.

### Pattern 4 - File-To-Artifact Conversion

The agent turns messy source files into structured output.

Examples:

- DICOM to metadata/report;
- CAD/BIM to data;
- PDF data room to risk findings;
- course material to syllabus/slides/quizzes;
- support emails to classified tickets.

### Pattern 5 - Specialist Team

Multiple agents represent specialist roles and then synthesize.

Examples:

- legal, finance, tech, cyber, HR due diligence;
- property value, rental income, neighborhood, market, investment agents;
- claim assessor, policy checker, risk analyst, communication agent;
- course designer, assessment designer, evaluator, reviewer.

### Pattern 6 - Tool Layer / MCP Layer

The agent needs structured tools to do real work.

Examples:

- SEC EDGAR MCP;
- zoning ArcGIS MCP;
- compliance screening MCP;
- fraud detection MCP;
- platform API skills from Stripe, Shopify, Supabase, Cloudflare.

## Best Repos To Study First

Start here if the goal is to learn how to build this stuff:

1. [Aperivue/verify-refs](https://github.com/Aperivue/verify-refs) - clean single-purpose audit skill.
2. [Aperivue/check-reporting](https://github.com/Aperivue/check-reporting) - checklist and status-label design.
3. [GarethManning/education-agent-skills](https://github.com/GarethManning/education-agent-skills) - education skill taxonomy.
4. [microsoft/Prior-Authorization-Multi-Agent-Solution-Accelerator](https://github.com/microsoft/Prior-Authorization-Multi-Agent-Solution-Accelerator) - healthcare multi-agent workflow with human review.
5. [zoharbabin/due-diligence-agents](https://github.com/zoharbabin/due-diligence-agents) - due diligence artifact chain.
6. [hoangtng/real-estate-agents](https://github.com/hoangtng/real-estate-agents) - clean agent persona plus skill pairing.
7. [hamzaabduljabbar/construction-drawing-analyzer](https://github.com/hamzaabduljabbar/construction-drawing-analyzer) - narrow domain file-processing skill with scripts.
8. [dandye/ai-runbooks](https://github.com/dandye/ai-runbooks) - runbook and incident-response artifact pattern.
9. [Shopify/agent-skills](https://github.com/Shopify/agent-skills) - skills with bundled validation tools.
10. [cloudflare/agent-skills-discovery-rfc](https://github.com/cloudflare/agent-skills-discovery-rfc) - how a skill directory might be discoverable.

## What To Build As Practice

A good first exercise is not a big app. Build one narrow workflow:

```text
repo-study-card
Input: one GitHub repo URL.
Process: inspect README, folder structure, skills/agents/scripts, outputs, safety boundaries.
Output: a one-page study card with problem, workflow, artifact, and build lesson.
Human boundary: no install, no execution, no trust claim.
```

This would teach the exact muscle needed to identify agentic opportunities.
