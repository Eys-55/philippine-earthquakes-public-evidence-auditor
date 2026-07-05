# Control Repo Tracker Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a repo-local control tracker that records projects, repos, workstreams, sessions, daily progress, handoffs, and GitHub upload state so status answers come from durable tracked files.

**Architecture:** Use Python standard-library scripts plus JSON/JSONL files under `ops/`. The tracker is file-backed, append-only for event/session logs, and validated by a single `scripts/validate_tracker.py` gate that is safe to run before every commit.

**Tech Stack:** Python 3 standard library, JSON, JSONL, Markdown, git CLI, existing ECC skills surface.

---

## Implementation Rules

- Do not rename the tracker into a mascot or product name.
- Do not report stale folders as active projects.
- Do not delete stale project files in this plan.
- Use `apply_patch` for manual edits.
- Keep all scripts runnable from the repo root.
- Run validation after every task.
- Commit frequently and upload to GitHub after each meaningful checkpoint.

## Task 1: Add Tracker Test Harness

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_validate_tracker.py`

**Step 1: Write the failing tests**

Create `tests/__init__.py` as an empty package marker.

Create `tests/test_validate_tracker.py`:

```python
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_tracker import validate_tracker_root


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class ValidateTrackerTests(unittest.TestCase):
    def test_valid_tracker_seed_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            write_json(root / "ops/registry/projects.json", {
                "projects": [
                    {
                        "id": "agent-workflow-project-maker",
                        "title": "Agent Workflow Project Maker",
                        "status": "active",
                        "owner_intent": "Create reusable ECC workflow project packs.",
                        "current_goal": "Track workflow creation work.",
                        "repos": ["control-repo"],
                        "workstreams": ["tracker-build"],
                        "not_projects": [],
                        "last_event_id": None,
                        "last_uploaded_commit": None
                    }
                ],
                "non_projects": [
                    {
                        "id": "metro-manila-source-atlas",
                        "reason": "Stale foundation surface; do not report as active."
                    }
                ]
            })
            write_json(root / "ops/registry/repos.json", {
                "repos": [
                    {
                        "id": "control-repo",
                        "path": ".",
                        "github_remote": "https://github.com/example/repo.git",
                        "default_branch": "main",
                        "role": "control",
                        "owning_project": "shared",
                        "upload_policy": "required",
                        "last_clean_check": None
                    }
                ]
            })
            write_json(root / "ops/registry/workstreams.json", {
                "workstreams": [
                    {
                        "id": "tracker-build",
                        "project_id": "agent-workflow-project-maker",
                        "repo_id": "control-repo",
                        "status": "active",
                        "objective": "Build the control repo tracker.",
                        "session_ids": [],
                        "handoff": "ops/handoffs/latest.md",
                        "open_decisions": [],
                        "next_action": "Implement tracker scripts."
                    }
                ]
            })
            write_json(root / "ops/sync/github-upload-state.json", {
                "repos": {
                    "control-repo": {
                        "local_branch": "main",
                        "local_head": "abc123",
                        "remote_branch": "main",
                        "remote_head": "abc123",
                        "status": "clean",
                        "untracked_file_count": 0,
                        "last_successful_upload": "2026-07-06T00:00:00Z",
                        "last_verification_command": "git ls-remote origin refs/heads/main"
                    }
                }
            })
            (root / "ops/events").mkdir(parents=True)
            (root / "ops/sessions").mkdir(parents=True)
            result = validate_tracker_root(root)
            self.assertEqual([], result.errors)

    def test_workstream_missing_project_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw_tmp:
            root = Path(raw_tmp)
            write_json(root / "ops/registry/projects.json", {"projects": [], "non_projects": []})
            write_json(root / "ops/registry/repos.json", {
                "repos": [
                    {
                        "id": "control-repo",
                        "path": ".",
                        "github_remote": "https://github.com/example/repo.git",
                        "default_branch": "main",
                        "role": "control",
                        "owning_project": "shared",
                        "upload_policy": "required",
                        "last_clean_check": None
                    }
                ]
            })
            write_json(root / "ops/registry/workstreams.json", {
                "workstreams": [
                    {
                        "id": "bad-workstream",
                        "project_id": "missing-project",
                        "repo_id": "control-repo",
                        "status": "active",
                        "objective": "Broken reference.",
                        "session_ids": [],
                        "handoff": "ops/handoffs/latest.md",
                        "open_decisions": [],
                        "next_action": "Fix registry."
                    }
                ]
            })
            write_json(root / "ops/sync/github-upload-state.json", {"repos": {}})
            result = validate_tracker_root(root)
            self.assertIn("bad-workstream: unknown project_id missing-project", result.errors)


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_validate_tracker -v
```

Expected: FAIL with `ModuleNotFoundError` for `scripts.validate_tracker`.

**Step 3: Commit**

Do not commit yet. The tests intentionally fail until Task 2 adds the validator.

## Task 2: Implement Tracker Validator

**Files:**
- Create: `scripts/validate_tracker.py`

**Step 1: Write minimal implementation**

Create `scripts/validate_tracker.py`:

```python
#!/usr/bin/env python3
"""Validate the control repo tracker registries and logs."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"missing {path}")
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{path}: top-level JSON must be an object")
        return {}
    return payload


def ids_for(records: object, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(records, list):
        errors.append(f"{label} must be a list")
        return set()
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            errors.append(f"{label} entry must be an object")
            continue
        record_id = record.get(key)
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{label} entry missing {key}")
            continue
        if record_id in seen:
            errors.append(f"duplicate {label} id {record_id}")
        seen.add(record_id)
    return seen


def validate_jsonl_file(path: Path, errors: list[str]) -> None:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{line_number}: invalid JSONL: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{path}:{line_number}: JSONL event must be an object")


def validate_tracker_root(root: Path = ROOT) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    projects_payload = read_json(root / "ops/registry/projects.json", errors)
    repos_payload = read_json(root / "ops/registry/repos.json", errors)
    workstreams_payload = read_json(root / "ops/registry/workstreams.json", errors)
    upload_payload = read_json(root / "ops/sync/github-upload-state.json", errors)

    project_ids = ids_for(projects_payload.get("projects", []), "id", "project", errors)
    repo_ids = ids_for(repos_payload.get("repos", []), "id", "repo", errors)
    workstream_ids = ids_for(workstreams_payload.get("workstreams", []), "id", "workstream", errors)

    non_projects = projects_payload.get("non_projects", [])
    if isinstance(non_projects, list):
        non_project_ids = {
            item.get("id")
            for item in non_projects
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        for overlap in sorted(project_ids & non_project_ids):
            errors.append(f"{overlap}: listed as both project and non_project")

    for project in projects_payload.get("projects", []):
        if not isinstance(project, dict):
            continue
        project_id = project.get("id", "<unknown>")
        for repo_id in project.get("repos", []):
            if repo_id not in repo_ids:
                errors.append(f"{project_id}: unknown repo {repo_id}")
        for workstream_id in project.get("workstreams", []):
            if workstream_id not in workstream_ids:
                errors.append(f"{project_id}: unknown workstream {workstream_id}")

    for workstream in workstreams_payload.get("workstreams", []):
        if not isinstance(workstream, dict):
            continue
        workstream_id = workstream.get("id", "<unknown>")
        project_id = workstream.get("project_id")
        repo_id = workstream.get("repo_id")
        if project_id not in project_ids:
            errors.append(f"{workstream_id}: unknown project_id {project_id}")
        if repo_id not in repo_ids:
            errors.append(f"{workstream_id}: unknown repo_id {repo_id}")

    upload_repos = upload_payload.get("repos", {})
    if not isinstance(upload_repos, dict):
        errors.append("github-upload-state repos must be an object")
        upload_repos = {}

    for repo in repos_payload.get("repos", []):
        if not isinstance(repo, dict):
            continue
        repo_id = repo.get("id")
        if repo.get("upload_policy") == "required" and repo_id not in upload_repos:
            errors.append(f"{repo_id}: required repo missing upload state")
        state = upload_repos.get(repo_id)
        if isinstance(state, dict) and state.get("local_head") != state.get("remote_head"):
            errors.append(f"{repo_id}: local_head differs from remote_head")

    for folder_name in ("events", "sessions"):
        folder = root / "ops" / folder_name
        if not folder.exists():
            warnings.append(f"missing optional log folder ops/{folder_name}")
            continue
        for path in sorted(folder.rglob("*.jsonl")):
            validate_jsonl_file(path, errors)

    return ValidationResult(errors=errors, warnings=warnings)


def main() -> int:
    result = validate_tracker_root(ROOT)
    for warning in result.warnings:
        print(f"warning: {warning}")
    if result.errors:
        print("tracker validation failed:", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("tracker validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 2: Run tests**

Run:

```bash
python3 -m unittest tests.test_validate_tracker -v
```

Expected: PASS.

**Step 3: Run syntax check**

Run:

```bash
python3 -m py_compile scripts/validate_tracker.py tests/test_validate_tracker.py
find . -type d -name __pycache__ -prune -exec rm -rf {} +
```

Expected: no output.

**Step 4: Commit**

```bash
git add scripts/validate_tracker.py tests/__init__.py tests/test_validate_tracker.py
git commit -m "test: add tracker validation harness"
git push origin main
```

## Task 3: Seed Tracker Registry

**Files:**
- Create: `ops/registry/projects.json`
- Create: `ops/registry/repos.json`
- Create: `ops/registry/workstreams.json`
- Create: `ops/events/.gitkeep`
- Create: `ops/sessions/.gitkeep`
- Create: `ops/daily/.gitkeep`
- Create: `ops/handoffs/latest.md`
- Create: `ops/public/linkedin-posts.jsonl`
- Create: `ops/sync/github-upload-state.json`

**Step 1: Create seed registries**

Create `ops/registry/projects.json` with only the two current active projects:

```json
{
  "schema_version": 1,
  "projects": [
    {
      "id": "philippines-building-code-evidence-auditor",
      "title": "Philippines Building Code Evidence Auditor",
      "status": "active",
      "owner_intent": "Audit public evidence for Philippine buildings without overclaiming safety or compliance.",
      "current_goal": "Keep the evidence-auditor workflow testable and source-bounded.",
      "repos": ["market-research-agent-control"],
      "workstreams": ["building-code-evidence-auditor"],
      "not_projects": [
        "address-disaster-risk-assessor",
        "metro-manila-source-atlas",
        "untitled-project",
        "multi-lane-foundation-model"
      ],
      "last_event_id": null,
      "last_uploaded_commit": null
    },
    {
      "id": "agent-workflow-project-maker",
      "title": "Agent Workflow Project Maker",
      "status": "active",
      "owner_intent": "Create reusable ECC workflow project packs and manage generated repo work.",
      "current_goal": "Build the control repo tracker and project creation workflow.",
      "repos": ["market-research-agent-control"],
      "workstreams": ["control-repo-tracker"],
      "not_projects": [],
      "last_event_id": null,
      "last_uploaded_commit": null
    }
  ],
  "non_projects": [
    {
      "id": "address-disaster-risk-assessor",
      "reason": "Deleted or obsolete surface; do not report as active unless explicitly reopened."
    },
    {
      "id": "metro-manila-source-atlas",
      "reason": "Stale foundation surface; do not report as active."
    },
    {
      "id": "untitled-project",
      "reason": "Placeholder surface; do not report as active."
    },
    {
      "id": "multi-lane-foundation-model",
      "reason": "Stale policy model; do not report as active."
    }
  ]
}
```

Create `ops/registry/repos.json`:

```json
{
  "schema_version": 1,
  "repos": [
    {
      "id": "market-research-agent-control",
      "path": ".",
      "github_remote": "https://github.com/Eys-55/philippine-earthquakes-public-evidence-auditor.git",
      "default_branch": "main",
      "role": "control",
      "owning_project": "shared",
      "upload_policy": "required",
      "last_clean_check": null
    }
  ]
}
```

Create `ops/registry/workstreams.json`:

```json
{
  "schema_version": 1,
  "workstreams": [
    {
      "id": "building-code-evidence-auditor",
      "project_id": "philippines-building-code-evidence-auditor",
      "repo_id": "market-research-agent-control",
      "status": "active",
      "objective": "Maintain the Philippine building evidence audit workflow.",
      "session_ids": [],
      "handoff": "docs/status/2026-07-06-project-surface-audit.md",
      "open_decisions": [],
      "next_action": "Use tracker status before changing project lists."
    },
    {
      "id": "control-repo-tracker",
      "project_id": "agent-workflow-project-maker",
      "repo_id": "market-research-agent-control",
      "status": "active",
      "objective": "Build a tracker for projects, repos, sessions, and GitHub upload state.",
      "session_ids": [],
      "handoff": "ops/handoffs/latest.md",
      "open_decisions": [
        "Decide whether command shims should live under commands/."
      ],
      "next_action": "Implement tracker status and event logging scripts."
    }
  ]
}
```

Create `ops/sync/github-upload-state.json` after reading the current local and
remote HEAD with:

```bash
LOCAL_HEAD="$(git rev-parse HEAD)"
REMOTE_HEAD="$(git ls-remote origin refs/heads/main | awk '{print $1}')"
```

Expected JSON shape:

```json
{
  "schema_version": 1,
  "repos": {
    "market-research-agent-control": {
      "local_branch": "main",
      "local_head": "<LOCAL_HEAD>",
      "remote_branch": "main",
      "remote_head": "<REMOTE_HEAD>",
      "status": "clean",
      "untracked_file_count": 0,
      "last_successful_upload": "2026-07-06T00:00:00Z",
      "last_verification_command": "git ls-remote origin refs/heads/main"
    }
  }
}
```

Create `ops/handoffs/latest.md`:

```markdown
# Latest Control Repo Handoff

Status: tracker seed pending first live session event.

Next action: run `python3 scripts/tracker_status.py` after Task 4.
```

Create `ops/public/linkedin-posts.jsonl` as an empty file.

**Step 2: Validate seed**

Run:

```bash
python3 scripts/validate_tracker.py
python3 -m json.tool ops/registry/projects.json >/tmp/tracker-projects.json
python3 -m json.tool ops/registry/repos.json >/tmp/tracker-repos.json
python3 -m json.tool ops/registry/workstreams.json >/tmp/tracker-workstreams.json
python3 -m json.tool ops/sync/github-upload-state.json >/tmp/tracker-upload-state.json
```

Expected: validator passes.

**Step 3: Commit and upload**

```bash
git add ops
git commit -m "feat: seed control repo tracker registry"
git push origin main
```

## Task 4: Add Project Status Script

**Files:**
- Create: `scripts/tracker_status.py`

**Step 1: Write failing behavior check**

Run before creating the script:

```bash
python3 scripts/tracker_status.py
```

Expected: FAIL because the file does not exist.

**Step 2: Implement status script**

Create `scripts/tracker_status.py`:

```python
#!/usr/bin/env python3
"""Print control repo project status from tracker registries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    projects = read_json(ROOT / "ops/registry/projects.json")
    workstreams = read_json(ROOT / "ops/registry/workstreams.json")
    upload_state = read_json(ROOT / "ops/sync/github-upload-state.json")

    workstreams_by_project: dict[str, list[dict]] = {}
    for workstream in workstreams.get("workstreams", []):
        workstreams_by_project.setdefault(workstream["project_id"], []).append(workstream)

    print("# Project Status")
    print()
    for project in projects.get("projects", []):
        if project.get("status") != "active":
            continue
        print(f"## {project['title']} (`{project['id']}`)")
        print(f"- Status: {project['status']}")
        print(f"- Current goal: {project['current_goal']}")
        for workstream in workstreams_by_project.get(project["id"], []):
            print(f"- Workstream `{workstream['id']}`: {workstream['status']} - {workstream['next_action']}")
        print()

    non_projects = projects.get("non_projects", [])
    if non_projects:
        print("## Not Active Projects")
        for item in non_projects:
            print(f"- `{item['id']}`: {item['reason']}")
        print()

    print("## GitHub Upload State")
    for repo_id, state in upload_state.get("repos", {}).items():
        same_head = state.get("local_head") == state.get("remote_head")
        marker = "uploaded" if same_head else "not uploaded"
        print(f"- `{repo_id}`: {marker} ({state.get('local_branch')} -> {state.get('remote_branch')})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 3: Verify output**

Run:

```bash
python3 scripts/tracker_status.py
```

Expected: output lists exactly two active projects and separates not-active
surfaces.

**Step 4: Commit and upload**

```bash
git add scripts/tracker_status.py
git commit -m "feat: add tracker project status"
git push origin main
```

## Task 5: Add Event Logging Script

**Files:**
- Create: `scripts/tracker_log_event.py`

**Step 1: Write failing behavior check**

Run:

```bash
python3 scripts/tracker_log_event.py --help
```

Expected: FAIL because the script does not exist.

**Step 2: Implement event logger**

Create `scripts/tracker_log_event.py` with `argparse` fields:

```python
--project-id
--repo-id
--workstream-id
--session-id
--actor
--summary
--next-action
```

The script should:

1. load `ops/registry/projects.json`, `repos.json`, and `workstreams.json`;
2. reject unknown ids;
3. generate an event id like `evt-YYYYMMDD-HHMMSS`;
4. append one JSON object to `ops/events/YYYY-MM-DD.jsonl`;
5. update the touched project's `last_event_id`;
6. print the event id.

Use this core append logic:

```python
def append_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
```

**Step 3: Verify logging**

Run:

```bash
python3 scripts/tracker_log_event.py \
  --project-id agent-workflow-project-maker \
  --repo-id market-research-agent-control \
  --workstream-id control-repo-tracker \
  --session-id manual-2026-07-06 \
  --actor codex \
  --summary "Added control repo tracker implementation plan." \
  --next-action "Implement tracker scripts task by task."
python3 scripts/validate_tracker.py
```

Expected: event id prints and validation passes.

**Step 4: Commit and upload**

```bash
git add ops/registry/projects.json ops/events scripts/tracker_log_event.py
git commit -m "feat: add tracker event logging"
git push origin main
```

## Task 6: Add Session Start And Handoff Scripts

**Files:**
- Create: `scripts/tracker_session_start.py`
- Create: `scripts/tracker_session_handoff.py`

**Step 1: Implement session start**

`scripts/tracker_session_start.py` should accept:

```python
--project-id
--repo-id
--workstream-id
--objective
```

It should create `ops/sessions/YYYY-MM-DD/session-<timestamp>.jsonl`, append a
`session_started` event, update `workstreams.json` with the session id, and
print the session path.

**Step 2: Implement handoff generation**

`scripts/tracker_session_handoff.py` should accept:

```python
--session-id
--next-action
```

It should read the matching session log and current workstream state, then
write `ops/handoffs/latest.md` with:

```markdown
# Latest Control Repo Handoff

Session: <session-id>
Project: <project-id>
Workstream: <workstream-id>

## What Changed

- <event summaries>

## Current State

- <workstream objective and status>

## Next Action

<next-action>
```

**Step 3: Verify**

Run:

```bash
SESSION_PATH="$(python3 scripts/tracker_session_start.py \
  --project-id agent-workflow-project-maker \
  --repo-id market-research-agent-control \
  --workstream-id control-repo-tracker \
  --objective "Test session logging")"
python3 scripts/validate_tracker.py
python3 scripts/tracker_session_handoff.py \
  --session-id "$(basename "$SESSION_PATH" .jsonl | sed 's/^session-//')" \
  --next-action "Continue tracker implementation."
```

Expected: validation passes and `ops/handoffs/latest.md` is updated.

**Step 4: Commit and upload**

```bash
git add ops/sessions ops/registry/workstreams.json ops/handoffs/latest.md scripts/tracker_session_start.py scripts/tracker_session_handoff.py
git commit -m "feat: add tracker session handoffs"
git push origin main
```

## Task 7: Add Upload Gate

**Files:**
- Create: `scripts/tracker_upload_gate.py`

**Step 1: Implement upload gate**

The script should:

1. run `git status --short`;
2. count untracked files;
3. read `git rev-parse --abbrev-ref HEAD`;
4. read `git rev-parse HEAD`;
5. read `git ls-remote origin refs/heads/<branch>`;
6. update `ops/sync/github-upload-state.json`;
7. fail if local HEAD differs from remote HEAD;
8. print a direct message: `uploaded to GitHub` or `local changes still need upload`.

Do not auto-commit in this script for V1. Keep commit/upload as explicit agent
actions so diffs can be reviewed.

**Step 2: Verify before upload**

Run:

```bash
python3 scripts/tracker_upload_gate.py
```

Expected during an uncommitted edit: FAIL with a clear message.

**Step 3: Commit and upload the gate**

```bash
git add scripts/tracker_upload_gate.py ops/sync/github-upload-state.json
git commit -m "feat: add github upload gate"
git push origin main
```

**Step 4: Verify after upload**

Run:

```bash
python3 scripts/tracker_upload_gate.py
python3 scripts/validate_tracker.py
```

Expected: PASS and upload state shows matching local/remote HEAD.

## Task 8: Add Daily Rollup

**Files:**
- Create: `scripts/tracker_daily_rollup.py`

**Step 1: Implement rollup**

The script should accept `--date YYYY-MM-DD`, read `ops/events/<date>.jsonl`,
and write `ops/daily/<date>.md`.

Markdown format:

```markdown
# Daily Control Repo Rollup - YYYY-MM-DD

## Projects Moved

- <project id>: <summary>

## GitHub Uploads

- <repo id>: <uploaded/not uploaded>

## Blocked

- <blocked item or "None">

## Public Progress Candidates

- <candidate or "None">

## Next Actions

- <workstream id>: <next action>
```

**Step 2: Verify**

Run:

```bash
python3 scripts/tracker_daily_rollup.py --date 2026-07-06
python3 scripts/validate_tracker.py
```

Expected: rollup file is created and validation passes.

**Step 3: Commit and upload**

```bash
git add scripts/tracker_daily_rollup.py ops/daily
git commit -m "feat: add tracker daily rollups"
git push origin main
```

## Task 9: Add Repo Audit Script

**Files:**
- Create: `scripts/tracker_repo_audit.py`

**Step 1: Implement audit**

The script should:

1. read `ops/registry/repos.json`;
2. inspect each local repo path;
3. report current branch, local HEAD, remote URL, remote HEAD, dirty files, and
   untracked files;
4. compare registered non-project ids against actual paths from
   `data/project-surface-inventory.json`;
5. print stale surfaces under a separate `Stale Or Orphaned Surfaces` section.

**Step 2: Verify**

Run:

```bash
python3 scripts/tracker_repo_audit.py
python3 scripts/validate_tracker.py
```

Expected: audit prints the existing stale surfaces as stale, not as active
projects.

**Step 3: Commit and upload**

```bash
git add scripts/tracker_repo_audit.py
git commit -m "feat: add tracker repo audit"
git push origin main
```

## Task 10: Document Control Repo Manager Skill And Slash Surface

**Files:**
- Create: `skills/control-repo-manager/SKILL.md`
- Create: `skills/control-repo-manager/agents/openai.yaml`
- Create: `skills/control-repo-manager/commands.md`

**Step 1: Write skill**

The skill must say:

- Use before answering project status.
- Use before ending any session in this repo.
- Status comes from `ops/registry/*.json` and `ops/events/*.jsonl`.
- Folder scans are audit evidence only.
- Deleted/stale surfaces must not be reported as active projects.
- A session is not complete until tracker, commit, GitHub upload, and upload
  verification are done.

**Step 2: Write command map**

Document these command equivalents in `commands.md`:

```markdown
# Control Repo Manager Commands

## /project-status

Run `python3 scripts/tracker_status.py`.

## /session-start

Run `python3 scripts/tracker_session_start.py ...`.

## /sync-now

Run validation, commit intended changes, upload to GitHub, then run
`python3 scripts/tracker_upload_gate.py`.

## /session-handoff

Run `python3 scripts/tracker_session_handoff.py ...`, then `/sync-now`.

## /repo-register

Add a repo to `ops/registry/repos.json`, then run
`python3 scripts/validate_tracker.py`.

## /repo-audit

Run `python3 scripts/tracker_repo_audit.py`.
```

**Step 3: Verify**

Run:

```bash
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
python3 scripts/tracker_repo_audit.py
```

Expected: scripts pass and command docs match available scripts.

**Step 4: Commit and upload**

```bash
git add skills/control-repo-manager
git commit -m "docs: add control repo manager skill"
git push origin main
```

## Task 11: Wire Final Verification Gate

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`

**Step 1: Update verification docs**

Add these commands to the repo verification section:

```bash
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
python3 scripts/tracker_upload_gate.py
```

Add a short README section:

```markdown
## Control Repo Tracker

This repo uses `ops/` as the authoritative tracker for projects, repos,
workstreams, sessions, handoffs, daily rollups, and GitHub upload state. Use
`python3 scripts/tracker_status.py` before answering what projects are active.
Folder names are not project authority.
```

**Step 2: Verify all gates**

Run:

```bash
python3 scripts/validate_project_surface_inventory.py
python3 scripts/validate_progress_docs.py
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
python3 scripts/tracker_upload_gate.py
git diff --check
```

Expected: all pass. The existing project-surface inventory warnings may remain
until a separate deletion/archive cleanup is approved.

**Step 3: Commit and upload**

```bash
git add AGENTS.md README.md ops/sync/github-upload-state.json
git commit -m "docs: require control repo tracker gate"
git push origin main
```

## Final Acceptance

Run:

```bash
python3 -m unittest tests.test_validate_tracker -v
python3 scripts/validate_project_surface_inventory.py
python3 scripts/validate_progress_docs.py
python3 scripts/validate_tracker.py
python3 scripts/tracker_status.py
python3 scripts/tracker_repo_audit.py
python3 scripts/tracker_upload_gate.py
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Acceptance criteria:

- `tracker_status.py` lists exactly two active projects.
- Stale/deleted surfaces are shown as not active.
- Workstreams reference valid projects and repos.
- Required repo upload state exists.
- Local HEAD and GitHub remote HEAD match.
- No untracked tracker files remain.
- Latest commit is uploaded to GitHub.

