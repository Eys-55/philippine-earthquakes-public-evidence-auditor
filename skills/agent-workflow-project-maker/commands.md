# Agent Workflow Project Maker Commands

skills/ is canonical. These slash names are a compatibility surface for
operators, not a second workflow source of truth.

| Slash | Mode | Purpose |
| --- | --- | --- |
| `/workflow-find` | read | Find existing workflow surfaces before creating anything new. |
| `/workflow-router` | read | Route a raw workflow problem through ECC-loaded workflow intake. |
| `/workflow-contract` | draft | Draft or inspect an ECC workflow contract for a workflow idea. |
| `/workflow-create-skill` | write | Create draft workflow scaffold files after explicit confirmation. |
| `/workflow-status` | status | Show tracker-backed workflow status and current next actions. |
| `/workflow-closeout` | closeout | Check validation, GitHub upload safety, and continuation readiness. |

Use `scripts/workflow_skill_slash_surface.py --command <slash> --json` to
inspect one command definition.

## Router Contract

Workflow-router work must start from ECC-loaded intake. A reported workflow bug
or workflow problem creates or locks a tracked workflow run, loads ECC and
workflow-specific context, writes a context manifest, shows visible ECC proof,
then asks the first context-aware grilling question.

Do not use these commands to skip into implementation.
