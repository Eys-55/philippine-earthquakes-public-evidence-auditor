#!/usr/bin/env python3
"""Print a read-only audit of registered repos and project surfaces."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPOS_PATH = ROOT / "ops" / "registry" / "repos.json"
PROJECTS_PATH = ROOT / "ops" / "registry" / "projects.json"
SURFACE_INVENTORY_PATH = ROOT / "data" / "project-surface-inventory.json"
REQUIRED_REPO_FIELDS = (
    "id",
    "path",
    "github_remote",
    "default_branch",
    "role",
    "owning_project",
    "upload_policy",
    "last_clean_check",
)
STRING_REPO_FIELDS = (
    "id",
    "path",
    "github_remote",
    "default_branch",
    "role",
    "owning_project",
    "upload_policy",
)
ROLE_VALUES = {"control", "generated", "reference", "external"}
UPLOAD_POLICY_VALUES = {"required", "manual", "never"}
JsonObject = dict[str, Any]


class AuditError(RuntimeError):
    """Raised when the audit cannot read required tracker inputs."""


@dataclass(frozen=True)
class GitCommandResult:
    stdout: str
    stderr: str
    returncode: int

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    @property
    def error(self) -> str:
        return self.stderr.strip() or f"git exited {self.returncode}"


@dataclass(frozen=True)
class RepoRecord:
    repo_id: str
    path_label: str
    resolved_path: Path
    github_remote: str
    default_branch: str
    role: str
    owning_project: str
    upload_policy: str


@dataclass(frozen=True)
class RepoAudit:
    repo: RepoRecord
    branch: str
    local_head: str
    remote_url: str
    remote_head: str
    dirty_files: list[str]
    untracked_files: list[str]
    errors: list[str]


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> JsonObject:
    if not path.exists():
        raise AuditError(f"missing required file: {display_path(path)}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AuditError(
            f"{display_path(path)}: invalid JSON at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuditError(f"{display_path(path)}: top-level JSON must be an object")
    return payload


def records_for(payload: JsonObject, key: str, source_path: Path) -> list[JsonObject]:
    records = payload.get(key)
    if not isinstance(records, list):
        raise AuditError(f"{display_path(source_path)}: missing required {key} array")

    normalized: list[JsonObject] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise AuditError(
                f"{display_path(source_path)}: {key}[{index}] must be an object"
            )
        normalized.append(record)
    return normalized


def require_string(record: JsonObject, field: str, repo_label: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value:
        raise AuditError(f"{repo_label}: {field} must be a non-empty string")
    return value


def repo_path(path_label: str) -> Path:
    candidate = Path(path_label).expanduser()
    if candidate.is_absolute():
        return candidate.resolve(strict=False)
    return (ROOT / candidate).resolve(strict=False)


def load_repo_records() -> list[RepoRecord]:
    payload = read_json(REPOS_PATH)
    repos = records_for(payload, "repos", REPOS_PATH)
    repo_records: list[RepoRecord] = []
    seen_ids: set[str] = set()

    for index, repo in enumerate(repos, start=1):
        repo_label = f"{display_path(REPOS_PATH)}: repos[{index}]"
        missing_fields = [field for field in REQUIRED_REPO_FIELDS if field not in repo]
        if missing_fields:
            raise AuditError(
                f"{repo_label}: missing required field(s): {', '.join(missing_fields)}"
            )

        for field in STRING_REPO_FIELDS:
            require_string(repo, field, repo_label)

        repo_id = require_string(repo, "id", repo_label)
        if repo_id in seen_ids:
            raise AuditError(f"{repo_label}: duplicate repo id {repo_id}")
        seen_ids.add(repo_id)

        role = require_string(repo, "role", repo_id)
        if role not in ROLE_VALUES:
            raise AuditError(
                f"{repo_id}: role must be one of {', '.join(sorted(ROLE_VALUES))}"
            )

        upload_policy = require_string(repo, "upload_policy", repo_id)
        if upload_policy not in UPLOAD_POLICY_VALUES:
            raise AuditError(
                f"{repo_id}: upload_policy must be one of "
                f"{', '.join(sorted(UPLOAD_POLICY_VALUES))}"
            )

        path_label = require_string(repo, "path", repo_id)
        repo_records.append(
            RepoRecord(
                repo_id=repo_id,
                path_label=path_label,
                resolved_path=repo_path(path_label),
                github_remote=require_string(repo, "github_remote", repo_id),
                default_branch=require_string(repo, "default_branch", repo_id),
                role=role,
                owning_project=require_string(repo, "owning_project", repo_id),
                upload_policy=upload_policy,
            )
        )

    return repo_records


def run_git(repo_path_value: Path, args: list[str]) -> GitCommandResult:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_path_value,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        return GitCommandResult(stdout="", stderr=str(exc), returncode=1)
    return GitCommandResult(
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
        returncode=result.returncode,
    )


def value_or_error(result: GitCommandResult) -> tuple[str, str | None]:
    if result.ok:
        return result.stdout, None
    return "unknown", result.error


def parse_status(status_output: str) -> tuple[list[str], list[str]]:
    dirty_files: list[str] = []
    untracked_files: list[str] = []
    for line in status_output.splitlines():
        if not line:
            continue
        if line.startswith("?? "):
            untracked_files.append(line[3:])
            continue
        dirty_files.append(line[3:] if len(line) > 3 else line)
    return dirty_files, untracked_files


def parse_remote_head(ls_remote_output: str) -> str:
    first_line = ls_remote_output.splitlines()[0] if ls_remote_output else ""
    parts = first_line.split()
    return parts[0] if parts else "missing"


def audit_repo(repo: RepoRecord) -> RepoAudit:
    errors: list[str] = []
    if not repo.resolved_path.exists():
        return RepoAudit(
            repo=repo,
            branch="missing path",
            local_head="missing path",
            remote_url="missing path",
            remote_head="missing path",
            dirty_files=[],
            untracked_files=[],
            errors=[f"path does not exist: {repo.resolved_path}"],
        )

    branch, branch_error = value_or_error(
        run_git(repo.resolved_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    )
    local_head, local_head_error = value_or_error(
        run_git(repo.resolved_path, ["rev-parse", "HEAD"])
    )
    remote_url, remote_url_error = value_or_error(
        run_git(repo.resolved_path, ["remote", "get-url", "origin"])
    )
    status_result = run_git(
        repo.resolved_path,
        ["status", "--porcelain=v1", "--untracked-files=all"],
    )
    if status_result.ok:
        dirty_files, untracked_files = parse_status(status_result.stdout)
    else:
        dirty_files = []
        untracked_files = []
        errors.append(f"status: {status_result.error}")

    for label, error in (
        ("branch", branch_error),
        ("local HEAD", local_head_error),
        ("remote URL", remote_url_error),
    ):
        if error:
            errors.append(f"{label}: {error}")

    remote_ref = (
        branch if branch and branch != "unknown" and branch != "HEAD" else repo.default_branch
    )
    remote_result = run_git(
        repo.resolved_path,
        ["ls-remote", "origin", f"refs/heads/{remote_ref}"],
    )
    if remote_result.ok:
        remote_head = parse_remote_head(remote_result.stdout)
    else:
        remote_head = "unknown"
        errors.append(f"remote HEAD ({remote_ref}): {remote_result.error}")

    return RepoAudit(
        repo=repo,
        branch=branch,
        local_head=local_head,
        remote_url=remote_url,
        remote_head=remote_head,
        dirty_files=dirty_files,
        untracked_files=untracked_files,
        errors=errors,
    )


def active_project_ids(
    projects_payload: JsonObject,
    inventory_payload: JsonObject,
) -> dict[str, set[str]]:
    sources: dict[str, set[str]] = {}
    for index, project in enumerate(
        records_for(projects_payload, "projects", PROJECTS_PATH),
        start=1,
    ):
        project_label = f"{display_path(PROJECTS_PATH)}: projects[{index}]"
        project_id = require_string(project, "id", project_label)
        status = require_string(project, "status", project_label)
        if status == "active":
            sources.setdefault(project_id, set()).add("registry active project")

    for index, project in enumerate(
        records_for(
            inventory_payload,
            "active_current_projects",
            SURFACE_INVENTORY_PATH,
        ),
        start=1,
    ):
        project_label = (
            f"{display_path(SURFACE_INVENTORY_PATH)}: "
            f"active_current_projects[{index}]"
        )
        slug = require_string(project, "slug", project_label)
        sources.setdefault(slug, set()).add("inventory active_current_projects")

    return sources


def non_project_records(projects_payload: JsonObject) -> dict[str, JsonObject]:
    records: dict[str, JsonObject] = {}
    for index, record in enumerate(
        records_for(projects_payload, "non_projects", PROJECTS_PATH),
        start=1,
    ):
        record_label = f"{display_path(PROJECTS_PATH)}: non_projects[{index}]"
        record_id = require_string(record, "id", record_label)
        require_string(record, "reason", record_label)
        records[record_id] = record
    return records


def inventory_stale_records(inventory_payload: JsonObject) -> dict[str, JsonObject]:
    records: dict[str, JsonObject] = {}
    for index, record in enumerate(
        records_for(
            inventory_payload,
            "non_current_surfaces",
            SURFACE_INVENTORY_PATH,
        ),
        start=1,
    ):
        record_label = (
            f"{display_path(SURFACE_INVENTORY_PATH)}: "
            f"non_current_surfaces[{index}]"
        )
        slug = require_string(record, "slug", record_label)
        records[slug] = record
    return records


def existing_inventory_paths(record: JsonObject | None) -> list[str]:
    if record is None:
        return []
    paths = record.get("paths", [])
    if not isinstance(paths, list):
        return []

    existing_paths: list[str] = []
    for raw_path in paths:
        if not isinstance(raw_path, str) or not raw_path:
            continue
        path = ROOT / raw_path
        if path.exists():
            existing_paths.append(raw_path)
    return existing_paths


def print_wrapped_list(values: list[str], empty_message: str) -> None:
    if not values:
        print(f"  - {empty_message}")
        return
    for value in values:
        print(f"  - {value}")


def print_registered_repos(audits: list[RepoAudit]) -> None:
    print("## Registered Repos")
    print()
    for audit in audits:
        repo = audit.repo
        print(f"- `{repo.repo_id}`")
        print(f"  - Path: `{repo.path_label}`")
        print(f"  - Resolved Path: `{repo.resolved_path}`")
        print(f"  - Role: `{repo.role}`")
        print(f"  - Owning Project: `{repo.owning_project}`")
        print(f"  - Upload Policy: `{repo.upload_policy}`")
        print(f"  - Expected GitHub Remote: `{repo.github_remote}`")
        print(f"  - Current Branch: `{audit.branch}`")
        print(f"  - Local HEAD: `{audit.local_head}`")
        print(f"  - Remote URL: `{audit.remote_url}`")
        print(f"  - Remote HEAD ({audit.branch}): `{audit.remote_head}`")
        print(f"  - Dirty Files: {len(audit.dirty_files)}")
        print(f"  - Untracked Files: {len(audit.untracked_files)}")
        if audit.errors:
            print("  - Git Inspection Warnings:")
            for error in audit.errors:
                print(f"    - {error}")
    print()


def print_active_projects(
    project_sources: dict[str, set[str]],
    stale_ids: set[str],
) -> None:
    print("## Active Projects From Registry/Inventory")
    print()
    active_ids = sorted(
        project_id for project_id in project_sources if project_id not in stale_ids
    )
    if not active_ids:
        print("- No active projects found after excluding registered stale/non-project ids.")
        print()
        return

    for project_id in active_ids:
        print(f"- `{project_id}`")
        print(f"  - Source: {', '.join(sorted(project_sources[project_id]))}")
    print()


def print_stale_surfaces(
    *,
    registry_stale: dict[str, JsonObject],
    inventory_stale: dict[str, JsonObject],
    project_sources: dict[str, set[str]],
) -> None:
    print("## Stale Or Orphaned Surfaces")
    print()
    stale_ids = sorted(set(registry_stale) | set(inventory_stale))
    if not stale_ids:
        print("- No registered stale or orphaned surfaces found.")
        print()
        return

    for stale_id in stale_ids:
        registry_record = registry_stale.get(stale_id)
        inventory_record = inventory_stale.get(stale_id)
        source_labels: list[str] = []
        if registry_record is not None:
            source_labels.append("registry non_projects")
        if inventory_record is not None:
            source_labels.append("inventory non_current_surfaces")
        if registry_record is None:
            source_labels.append("orphaned from registry")
        if inventory_record is None:
            source_labels.append("missing inventory path record")

        print(f"- `{stale_id}`")
        print(f"  - Source: {', '.join(source_labels)}")
        classification = inventory_record.get("classification") if inventory_record else None
        if isinstance(classification, str) and classification:
            print(f"  - Classification: `{classification}`")
        reason = None
        if registry_record is not None and isinstance(registry_record.get("reason"), str):
            reason = registry_record["reason"]
        elif inventory_record is not None and isinstance(inventory_record.get("reason"), str):
            reason = inventory_record["reason"]
        if reason:
            print(f"  - Reason: {reason}")
        if stale_id in project_sources:
            print("  - Active Conflict: suppressed from active project section")
        print("  - Existing Inventory Paths:")
        print_wrapped_list(
            existing_inventory_paths(inventory_record),
            "No listed inventory paths currently exist.",
        )
    print()


def print_dirty_files(audits: list[RepoAudit]) -> None:
    print("## Dirty Or Untracked Files")
    print()
    any_changes = False
    for audit in audits:
        if not audit.dirty_files and not audit.untracked_files:
            continue
        any_changes = True
        print(f"- `{audit.repo.repo_id}`")
        print("  - Dirty Files:")
        print_wrapped_list(audit.dirty_files, "None")
        print("  - Untracked Files:")
        print_wrapped_list(audit.untracked_files, "None")
    if not any_changes:
        print("- No dirty or untracked files in registered local repos.")
    print()


def main() -> int:
    try:
        repo_records = load_repo_records()
        projects_payload = read_json(PROJECTS_PATH)
        inventory_payload = read_json(SURFACE_INVENTORY_PATH)
        registry_stale = non_project_records(projects_payload)
        inventory_stale = inventory_stale_records(inventory_payload)
        stale_ids = set(registry_stale) | set(inventory_stale)
        project_sources = active_project_ids(projects_payload, inventory_payload)
    except AuditError as exc:
        print(f"tracker repo audit failed: {exc}", file=sys.stderr)
        return 1

    audits = [audit_repo(repo) for repo in repo_records]

    print("# Repo Audit")
    print()
    print_registered_repos(audits)
    print_active_projects(project_sources, stale_ids)
    print_stale_surfaces(
        registry_stale=registry_stale,
        inventory_stale=inventory_stale,
        project_sources=project_sources,
    )
    print_dirty_files(audits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
