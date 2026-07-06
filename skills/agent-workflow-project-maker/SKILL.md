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

## Workflow Intake Router

For workflow bugs, workflow problems, continuations, and new workflow requests,
do not jump directly to implementation. Start from ECC-loaded workflow intake.

Required sequence:

1. Create or lock a tracked workflow run immediately.
2. Set the first phase to `workflow_intake`.
3. Load ECC, Matt Pocock flow, tracker status, workflow-specific skill files,
   status/handoff docs, tests, validators, and relevant workflow-run logs.
4. If the report names an ECC concept such as loop, gate, lane, eval, handoff,
   source evidence, or human boundary, load the local docs for that concept.
5. Write or attach a context manifest under `ops/workflow-runs/`.
6. Show visible ECC proof before grilling:
   - ECC files loaded;
   - workflow/concept files loaded;
   - ECC concept meaning from the loaded files;
   - premise lock;
   - first context-aware grilling question.
7. Grill only after the loaded-context proof exists.

Do not ask blank questions. Do not rely on generic Codex assumptions about
agentic workflows. ECC is the operating model.

Fail-closed enforcement lives in `python3 scripts/validate_tracker.py`.
Workflow runs in `workflow_intake`, and all `workflow_specific_bug` runs, must
have a context manifest under `ops/workflow-runs/` with loaded ECC context and
a premise marker. If that proof is missing, tracker validation must fail before
the session can be treated as safe to continue, close, or upload.

New workflow creation requires explicit confirmation, such as:

- "Create a new workflow for this"
- "This is not a continuation. Start a new workflow."

After explicit confirmation, create the draft scaffold immediately:

- `skills/<workflow-slug>/SKILL.md`
- `data/<workflow-slug>/.gitkeep`
- `docs/status/YYYY-MM-DD-<workflow-slug>-status.md`
- `ops/workflow-runs/YYYY-MM-DD/<workflow-run-id>-context.md`

Draft scaffold files must include visible progress markers, current phase, next
action, and explicit "Not reached yet" markers for untouched sections.

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

## Slash Compatibility Surface

`skills/` remains canonical. The compatibility commands are documented in
`skills/agent-workflow-project-maker/commands.md` and exposed by
`scripts/workflow_skill_slash_surface.py`.

- `/workflow-find`
- `/workflow-router`
- `/workflow-contract`
- `/workflow-create-skill`
- `/workflow-status`
- `/workflow-closeout`
