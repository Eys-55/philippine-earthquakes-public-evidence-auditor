# Workflow Catalog CLI Readiness

Generated: 2026-07-05

Status: superseded by skills-first catalog lookup. The Python CLI preparation
tooling was removed on 2026-07-06 because workflow catalog operation now lives
through Codex chat, skills, and committed JSON indexes.

## Current Seed

- Internal discovery agents completed: 6 / 6
- Repos represented: 17 / 17
- Raw discovered rows before dedupe: 203
- Deduped seed links: 171
- CLI prompt chunks prepared: 18
- Max links per CLI prompt: 10
- External CLI agents launched: 0

The seed is intentionally index-first for very large or generated repos. Large
catalogs are represented by manifests, category folders, and major workflow
lanes, with `needs_second_pass: true` where full leaf expansion is not yet
verified.

## Prepared Artifacts

- `data/agentic-repos/workflow-catalog-internal/agent-001.json`
- `data/agentic-repos/workflow-catalog-internal/agent-002.json`
- `data/agentic-repos/workflow-catalog-internal/agent-003.json`
- `data/agentic-repos/workflow-catalog-internal/agent-004.json`
- `data/agentic-repos/workflow-catalog-internal/agent-005.json`
- `data/agentic-repos/workflow-catalog-internal/agent-006.json`
- `data/agentic-repos/workflow-link-seed.raw.json`
- `data/agentic-repos/workflow-link-seed.json`
- `data/agentic-repos/workflow-catalog-cli/prompts/agent-001.json` through `agent-018.json`
- `reports/workflow-link-seed.md`

## Superseded Launch Shape

Historical shape only; do not use this as the current workflow surface.

```bash
codex exec \
  -m gpt-5.5 \
  -c model_reasoning_effort='"low"' \
  --search \
  -s read-only \
  -a never \
  -C /Users/acecanacan/Documents/market-research-agent \
  --output-last-message data/agentic-repos/workflow-catalog-cli/agent-001.json \
  "$(cat data/agentic-repos/workflow-catalog-cli/prompts/agent-001.json)"
```

Each prompt file owns at most 10 seed links. The current seed requires 18 CLI
classification agents, not 30, because the deduped seed is 171 links.

## Historical Readiness Checks

- `python3 -m json.tool data/agentic-repos/workflow-link-seed.raw.json`
- `python3 -m json.tool data/agentic-repos/workflow-link-seed.json`
