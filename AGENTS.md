# Market Research Agent Workspace - ECC Instructions

This repo is an ECC-aligned multi-project workspace. Multiple agentic workflows
may live here at the same time, but each workflow must stay in its own project
lane so evidence, schemas, status notes, and safety boundaries do not mix.

## Core Rules

- Agent-first: split broad research into independent source categories before
  integration.
- Security-first: no credentials, no auth bypass, no signup flows, no paid
  actions, and no third-party writes without explicit user approval.
- Plan before execute: define source categories, validation checks, and output
  schemas before collecting or merging data.
- Source attribution: every important claim in reports must cite a source URL.
- Immutability: preserve raw agent findings and validation logs; integration
  outputs should be new files or new rows, not destructive rewrites.
- Workflow surface: put reusable workflows under `skills/` first. Avoid
  `commands/` unless a compatibility shim is explicitly needed.

## ECC Agentic Workflow Contract

Before designing or implementing any new agentic workflow in this repo, route the
work through ECC rather than starting from a topic idea alone.

Define the workflow contract first:

- repeated real-world job: what task will a person run more than once;
- trigger and scope: when the skill should activate and when it should refuse;
- input contract: files, links, addresses, APIs, records, prompts, or other
  inspectable inputs;
- agent lanes: independent source, validation, integration, and review roles;
- tool and action space: narrow read/search/parse/query actions with explicit
  third-party write boundaries;
- raw evidence surface: preserved findings, logs, source responses, and caveats;
- integrated output: report, JSON packet, brief, atlas, dataset, or visual card;
- validation loop: freshness, reachability, source URL, schema checks, and
  expected failure cases;
- safety contract: secrets, auth, paid actions, publishing, and irreversible
  operations are blocked unless explicitly approved;
- reusable skill surface: document the workflow under `skills/<name>/SKILL.md`
  before adding scripts, app surfaces, scheduled runs, or compatibility shims.

Start with input and output only after naming the repeated job. If the repeated
job is vague, clarify that first. If the job is clear, lock the input contract,
then the output artifact, then the agent lanes and validation loop.

## Project Lane Policy

Codex should treat a project lane as the working boundary for a repeated
workflow. Before changing files, running searches, or continuing a previous
thread, identify the active lane from the user's words, the file path, or the
latest status artifact. If the lane is ambiguous, ask one short lane-selection
question before editing.

For new lanes, use one stable slug per workflow across the repo:

- `skills/<project-slug>/SKILL.md` - canonical workflow instructions.
- `data/<project-slug>/` - schemas, fixtures, raw evidence, samples, and evals.
- `reports/<project-slug>-*.md` - integrated human-readable outputs.
- `docs/plans/YYYY-MM-DD-<project-slug>-*.md` - design and execution plans.
- `docs/decisions/000X-*.md` - durable scope and architecture decisions.
- `docs/status/YYYY-MM-DD-<project-slug>-*.md` - handoff and resume state.
- `scripts/validate_<project_slug>*.py` - validation gates when useful.

Existing lanes with documented historical data surfaces, such as
`data/building-code-auditor/`, may keep those paths. The lane table and README
must make the mapping explicit.

Do not store second-project ideas inside another lane's `skills/`, `data/`,
`reports/`, or status files. Shared source inventories may remain at the repo
level only when they are explicitly reusable by multiple lanes.

Lane lifecycle:

- `exploring` - the repeated job is not locked yet; keep work in a placeholder
  lane such as `untitled-project`.
- `active` - the repeated job, input contract, and output artifact are locked.
- `paused` - preserve the status file and resume prompt, but do not blend the
  lane into active work.
- `reference` - reusable source atlas, schema, or research substrate used by
  more than one active lane.

Codex memory can remember the lane convention and current lane list, but the
repo is authoritative. Update repo docs first for team/project knowledge; use
memory only as a reminder for future Codex sessions.

## Control Repo Tracker Authority

Use `skills/control-repo-manager/SKILL.md` before answering project status or
ending a session in this repo. Project, repo, workstream, session, handoff,
daily rollup, and sync status comes from `ops/registry/*.json` and
`ops/events/*.jsonl`.

Folder scans, lane tables, README sections, AGENTS.md sections, and project
surface inventories are audit evidence only. Deleted or stale surfaces must not
be reported as active projects. Run `python3 scripts/tracker_status.py` before
answering what projects are active.

## Agent skills

### Issue tracker

Issues, PRDs, and implementation slices for this repo live in GitHub Issues.
External PRs are not a request surface because this is a solo-developed control
repo. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default Matt Pocock triage label vocabulary: `needs-triage`,
`needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See
`docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo. Use root `CONTEXT.md` for domain language and
root `docs/adr/` for architecture decisions. See `docs/agents/domain.md`.

## Visualization Default

Draw.io / diagrams.net is sidelined indefinitely for this repo. Do not use the
installed `drawio-skill`, create `.drawio` files, create draw.io exports, or
suggest draw.io as the default visualization path unless the user explicitly
asks to reopen draw.io.

When the user asks to "visualize this", "make a chart", "make a diagram", or
otherwise asks for a visual workflow representation, use the installed
`mermaid-skill` and keep the source as Mermaid in Markdown or `.mmd`.

For Codex-visible progress charts, use the conservative Mermaid profile that
renders reliably in the Codex rich viewer:

- use `graph TD` or `graph LR`;
- keep the chart file as one ` ```mermaid ` block and nothing else;
- do not use `stateDiagram-v2`, `flowchart`, `classDef`, Mermaid init
  directives, image embeds, or generated PNG/SVG replacements in the canonical
  chart Markdown;
- use explicit `<br/>` line breaks inside longer labels so Mermaid does not
  split words automatically;
- keep each manual label line short enough to avoid word wrapping in the Codex
  viewer;
- write chart nodes as short natural phrases, not terse status fragments;
- for workflow charts, show the human or operator decision flow, not artifact
  status; use objective action labels such as "Ask one missing detail", "Show
  best match", and "User confirms exact place?";
- keep implementation progress, test status, and artifact status in the paired
  Markdown table, not in the graph;
- put detailed notes in the paired Markdown table, not inside complex node
  labels.

For viewing, render Mermaid charts to SVG and open them through a dark HTML
viewer. The HTML viewer should be chart-only: no headings, no explanatory copy,
no progress table, and no discussion text unless the user explicitly asks for
those elements.

Use plain Markdown tables only in the paired table file, not in the HTML chart
viewer.

Do not create custom HTML workflow charts unless the user explicitly asks for an
HTML page.

## Historical Project Surface Notes

Do not use this section to determine current project status. It is historical
background for old workspace surfaces. Run `python3 scripts/tracker_status.py`
before reporting which projects are current.

- `philippines-building-code-evidence-auditor-v2` - tracker-listed current
  project; verify live status with `tracker_status.py`.
- `philippines-building-code-evidence-auditor` - predecessor surface; do not
  report as current while V2 is the tracker-listed auditor.
- `address-disaster-risk-assessor` - obsolete historical surface; do not report
  as current unless explicitly reopened and tracker-listed.
- `metro-manila-source-atlas` - stale source-atlas surface; do not report as
  current.
- `untitled-project` - placeholder surface; do not report as current.

2026-07-04 update: the user explicitly reopened the project direction for a
new ECC agent-building target: the **Philippines Building Code Evidence
Auditor**. This is historical context only; the tracker now decides current
project status. Disaster-risk work remains background context, not a current
project unless the tracker says so.

Priority sources:

- HazardHunterPH / GeoRiskPH for official multi-hazard assessment context.
- Project NOAH / BetterGov hazard layers for flood, landslide, and storm-surge
  zones.
- PHIVOLCS FaultFinder and public hazard services for active fault and
  liquefaction exposure.
- MMDA ArcGIS for Metro Manila boundaries, flood-prone points, rivers, and local
  risk overlays.
- HDX geohazards and administrative boundaries for downloadable geospatial
  fallback data.
- OpenStreetMap / Geofabrik for waterways, roads, access, facilities, and weak
  service-risk proxies.

## Validation Standard

For each high-priority source, record:

- reachability and HTTP status;
- access method and format;
- freshness signal;
- Metro Manila relevance method;
- address or coordinate assessment method;
- license or terms;
- auth/gating status;
- sample query or download command;
- risks and caveats.

Statuses should use: `active`, `reachable but stale`, `manual-only`,
`auth-gated`, `commercial`, or `dead`.

## Repo Map

- `README.md` - project index and artifact map.
- `reports/` - human-readable integrated reports.
- `data/metro-manila-source-atlas.json` - ranked inventory.
- `data/disaster-risk/` - canonical disaster-risk source priorities and future
  assessor outputs.
- `data/agent-findings/` - raw six-agent findings.
- `data/deep-dive/` - structured validation and qualification outputs.
- `data/building-code-auditor/` - schemas, source landscape, test cases, and
  samples for the building-code evidence auditor lane.
- `data/untitled-project/` - placeholder evidence and contract notes for the
  next workflow before it is renamed.
- `docs/decisions/` - durable project decisions.
- `docs/plans/` - product and workflow design documents.
- `docs/status/` - lane status, handoff, and resume notes.
- `skills/address-disaster-risk-assessor/` - historical ECC workflow surface
  for address-based disaster assessment.
- `skills/metro-manila-source-atlas/` - reusable ECC workflow for refreshing or
  extending the source atlas.
- `skills/philippines-building-code-evidence-auditor/` - predecessor ECC
  workflow surface for Philippine building identity and public evidence audit
  gates.
- `skills/untitled-project/` - placeholder lane for the next project until it is
  named and promoted.

## Verification

Before committing, run:

```bash
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
python3 scripts/tracker_upload_gate.py
python3 scripts/tracker_repo_audit.py
python3 -m json.tool data/metro-manila-source-atlas.json >/tmp/metro-manila-source-atlas.json
python3 -m json.tool data/deep-dive/local-validation-summary.json >/tmp/local-validation-summary.json
python3 -m json.tool data/deep-dive/source-qualification-matrix.json >/tmp/source-qualification-matrix.json
python3 -m json.tool data/disaster-risk/source-priorities.json >/tmp/disaster-risk-source-priorities.json
python3 scripts/validate_progress_docs.py
git diff --check
```

For docs-only changes, JSON parsing and whitespace checks are the required gate.
For future code, add tests before implementation and keep ECC's 80% coverage
target.
