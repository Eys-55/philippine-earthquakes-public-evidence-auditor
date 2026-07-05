# Real-World Workflow Catalog

This folder is the local workflow-search system for finding real-world workflow
patterns and Codex/ECC config-package references.

## Start Here

| File | Purpose |
| --- | --- |
| `workflow-search-index.json` | Main clean 171-row searchable catalog. |
| `workflow-search-index.csv` | Spreadsheet-friendly version of the catalog. |
| `workflow-search-index-by-domain.json` | Compact domain grouping for quick lookup. |
| `../../reports/workflow-search-index.md` | Human-readable summary and best rows by domain. |
| `../../scripts/query_workflow_catalog.py` | Main query command. |

## Query Examples

```bash
python3 scripts/query_workflow_catalog.py "healthcare referral packet"
python3 scripts/query_workflow_catalog.py "education workflow"
python3 scripts/query_workflow_catalog.py "real estate due diligence"
python3 scripts/query_workflow_catalog.py "document processing human review"
python3 scripts/query_workflow_catalog.py "Codex config package"
```

## Quality Model

| Tier | Meaning |
| --- | --- |
| `gold` | Source reachable or canonicalized, high confidence, ready to copy/adapt. |
| `silver` | Useful reference with medium or better confidence. |
| `bronze` | Potentially useful but source needs repair or verification. |
| `needs_verification` | Searchable, but verify before relying on it. |

## Source Runs

The clean index was built from:

- `workflow-catalog-runs/2026-07-05-priority1-cli-10x5/`
- `workflow-catalog-runs/2026-07-05-remaining-cli-25x5/`
- `workflow-catalog-runs/workflow-classifications-all.json`

Rebuild the clean index after changing source rows:

```bash
python3 scripts/build_workflow_search_index.py
```
