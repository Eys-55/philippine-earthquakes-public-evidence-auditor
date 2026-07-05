# Workflow Agent Comparison

Generated: 2026-07-05

This was a small apples-to-apples test of one internal Codex agent and one
Codex CLI run over the same five workflow doors.

## Test Doors

| ID | Door | Repo | Category |
| --- | --- | --- | --- |
| surface-0007 | Medical skills | CaseMark/skills | Healthcare / Medical Workflow |
| surface-0038 | Security Operations & GRC Workflows | agentskillexchange/skills | Evidence / Due Diligence |
| surface-0008 | OCR | CaseMark/skills | Document Transformation |
| surface-0082 | Education industry pack | indranilbanerjee/contentforge | Education Workflow |
| surface-0003 | Case development skills | CaseMark/skills | Case Intake / Legal Review |

## Result

Both outputs were good enough for a batch cataloging pass.

| Runner | Result quality | Main strength | Main issue |
| --- | --- | --- | --- |
| Internal Codex agent | Good | Concise classifications and good warning on sparse or mispathed links | No persisted output file unless the parent saves it |
| Codex CLI | Better for batch use | Included stronger source evidence and canonicalized broken/sparse GitHub paths | Produced noisy unrelated MCP auth warnings in terminal output |

## Decision

Use Codex CLI agents for the larger catalog enrichment run, because they can
write one output file per chunk and are easier to audit afterward.

Use internal Codex agents for spot checks, prompt calibration, and review of
the CLI output.

## Prompt Change Before Scaling

Add these fields to the classification schema before running a larger batch:

| Field | Purpose |
| --- | --- |
| `source_url_status` | Record `exact_page_reachable`, `exact_page_sparse`, `broken`, or `canonicalized`. |
| `canonical_source_url` | Preserve the original URL while recording the better source if the original door is broken or shallow. |
| `evidence_basis` | Short note on whether the row came from the exact page, README fallback, raw skill file, or repo index. |

This matters because several seed doors point to shallow paths such as
`/med` or `/casedev`, while the actual repo content may live under a nested
path like `skills/med` or `skills/casedev`.

## Next Recommended Batch

Run the Priority 1 doors through CLI chunks of 5-10 doors each. Keep the
first full batch small enough to inspect manually before expanding to the
remaining doors.
