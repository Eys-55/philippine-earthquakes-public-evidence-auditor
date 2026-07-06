from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from scripts import workflow_skill_slash_surface


REPO_ROOT = Path(__file__).resolve().parents[1]


class WorkflowSkillSlashSurfaceTests(unittest.TestCase):
    def test_required_slash_commands_are_registered(self) -> None:
        commands = workflow_skill_slash_surface.command_registry()
        names = [command["slash"] for command in commands]

        self.assertEqual(
            [
                "/workflow-find",
                "/workflow-router",
                "/workflow-contract",
                "/workflow-create-skill",
                "/workflow-status",
                "/workflow-closeout",
            ],
            names,
        )
        for command in commands:
            self.assertEqual("skills/agent-workflow-project-maker/SKILL.md", command["canonical_skill"])
            self.assertTrue(command["operator_command"])
            self.assertIn(command["mode"], {"read", "draft", "write", "status", "closeout"})
            self.assertIn(command["approval_boundary"], {"none", "before-file-write", "before-external-action"})

    def test_command_lookup_emits_json_for_one_slash(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "scripts/workflow_skill_slash_surface.py",
                "--command",
                "/workflow-contract",
                "--json",
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("/workflow-contract", payload["slash"])
        self.assertEqual("draft", payload["mode"])
        self.assertIn("workflow contract", payload["purpose"].lower())

    def test_command_docs_and_skill_cross_reference_every_slash(self) -> None:
        commands = workflow_skill_slash_surface.command_registry()
        command_docs = (REPO_ROOT / "skills/agent-workflow-project-maker/commands.md").read_text(
            encoding="utf-8"
        )
        skill_docs = (REPO_ROOT / "skills/agent-workflow-project-maker/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("skills/ is canonical", command_docs)
        self.assertIn("Slash Compatibility Surface", skill_docs)
        self.assertIn("skills/agent-workflow-project-maker/commands.md", skill_docs)
        for command in commands:
            self.assertIn(command["slash"], command_docs)
            self.assertIn(command["slash"], skill_docs)


if __name__ == "__main__":
    unittest.main()
