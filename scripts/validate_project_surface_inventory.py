#!/usr/bin/env python3
"""Validate the repo project surface inventory."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data" / "project-surface-inventory.json"


def as_path(path_text: str) -> Path:
    return ROOT / path_text.rstrip("/")


def path_exists(path_text: str) -> bool:
    return as_path(path_text).exists()


def main() -> int:
    if not INVENTORY_PATH.exists():
        print(f"missing inventory: {INVENTORY_PATH.relative_to(ROOT)}", file=sys.stderr)
        return 1

    with INVENTORY_PATH.open("r", encoding="utf-8") as handle:
        inventory = json.load(handle)

    errors: list[str] = []
    warnings: list[str] = []

    expected_count = inventory.get("user_stated_expected_current_project_count")
    active_projects = inventory.get("active_current_projects", [])
    if not isinstance(active_projects, list):
        errors.append("active_current_projects must be a list")
        active_projects = []

    if expected_count is not None and len(active_projects) != expected_count:
        errors.append(
            "active project count mismatch: "
            f"expected {expected_count}, inventory has {len(active_projects)}"
        )

    seen_slugs: set[str] = set()
    for project in active_projects:
        slug = project.get("slug")
        if not slug:
            errors.append("active project missing slug")
            continue
        if slug in seen_slugs:
            errors.append(f"duplicate active project slug: {slug}")
        seen_slugs.add(slug)

        skill = project.get("skill")
        if not skill:
            errors.append(f"{slug}: missing skill path")
        elif not path_exists(skill):
            errors.append(f"{slug}: skill path does not exist: {skill}")

        for owned_path in project.get("owned_paths", []):
            if not path_exists(owned_path):
                errors.append(f"{slug}: owned path does not exist: {owned_path}")

    active_slugs = {project.get("slug") for project in active_projects}
    forbidden_active = {"address-disaster-risk-assessor", "metro-manila-source-atlas", "untitled-project"}
    for slug in sorted(active_slugs & forbidden_active):
        errors.append(f"{slug}: forbidden as active project by current audit")

    for surface in inventory.get("non_current_surfaces", []):
        slug = surface.get("slug", "<unknown>")
        existing_paths = [path for path in surface.get("paths", []) if path_exists(path)]
        if existing_paths:
            classification = surface.get("classification", "non_current")
            warnings.append(
                f"{slug}: {classification} still present with {len(existing_paths)} path(s)"
            )

    print(f"validated inventory: {INVENTORY_PATH.relative_to(ROOT)}")
    print(f"active projects: {len(active_projects)}")
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
