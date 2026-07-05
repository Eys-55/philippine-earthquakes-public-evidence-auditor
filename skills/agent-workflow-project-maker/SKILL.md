---
name: agent-workflow-project-maker
description: Use the repo's real-world workflow catalog to turn a repeated job into a Codex/ECC project skill with input contracts, output artifacts, schemas, validators, and tracking. Use when the user asks for an agent workflow project maker, workflow catalog, workflow finder, real-world agent workflow examples, reusable project creation, or converting a vague project idea into a tracked skill.
---

# Agent Workflow Project Maker

This skill owns the workflow-catalog/project-maker surface in this repo. It
should be treated as a real project surface, not as loose research output.

## Owned Surfaces

- Catalog data: `data/agentic-repos/`
- Main index: `data/agentic-repos/workflow-search-index.json`
- Domain index: `data/agentic-repos/workflow-search-index-by-domain.json`
- Human reports: `reports/workflow-*.md`
- Query tools: `scripts/query_workflow_catalog.py`,
  `scripts/query_workflow_router.py`
- Build tools: `scripts/build_workflow_*.py`,
  `scripts/workflow_catalog_*.py`

The current catalog says it is a lookup layer for real-world workflow patterns
and Codex/ECC config-package references. Use that as the starting point.

## Workflow

1. Name the repeated real-world job.
2. Query the catalog for comparable workflows:

   ```bash
   python3 scripts/query_workflow_catalog.py "<job or domain phrase>"
   python3 scripts/query_workflow_router.py "<job or domain phrase>"
   ```

3. Inspect only the relevant catalog rows and source references.
4. Draft the project contract:
   - trigger and refusal scope;
   - input contract;
   - output artifact;
   - source/tool lanes;
   - raw evidence surface;
   - validation loop;
   - safety boundary.
5. Create or update a project skill under `skills/<project-slug>/SKILL.md`.
6. Add schemas, fixtures, examples, and validators only after the contract is
   clear.
7. Update `data/project-surface-inventory.json` so the new project is tracked.

## Rules

- Do not create placeholder projects. If the repeated job is vague, ask for the
  missing job before writing project files.
- Do not treat generated catalog rows as verified truth. Inspect source URLs or
  mark the row as needing verification.
- Keep runtime/platform examples as references unless the user explicitly
  chooses that runtime.
- Keep Codex/ECC as the operating surface. External repos are references or
  adapters, not the project brain.
- Never add a project to README or AGENTS.md unless it has a skill, owned paths,
  and inventory entry.

## Output Contract

For a new project, produce:

- `skills/<project-slug>/SKILL.md`;
- `data/<project-slug>/` for schemas, fixtures, examples, and raw evidence;
- optional `scripts/validate_<project_slug>*.py`;
- `docs/status/YYYY-MM-DD-<project-slug>-status.md`;
- inventory entry in `data/project-surface-inventory.json`.

When the user only wants ideation, stop at a project contract draft and do not
create files.
