from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class WorkflowSkillSlashSurfaceTests(unittest.TestCase):
    def test_slash_names_are_documented_only_as_internal_compatibility_text(self) -> None:
        command_docs = (REPO_ROOT / "skills/agent-workflow-project-maker/commands.md").read_text(
            encoding="utf-8"
        )
        skill_docs = (REPO_ROOT / "skills/agent-workflow-project-maker/SKILL.md").read_text(
            encoding="utf-8"
        )
        names = [
            "/tracker workflow",
            "/tracker status",
            "/tracker closeout",
            "/workflow-find",
            "/workflow-router",
            "/workflow-contract",
            "/workflow-create-skill",
            "/workflow-status",
            "/workflow-closeout",
        ]

        self.assertIn("skills/ is canonical", command_docs)
        self.assertIn("Internal Adapter Reference", command_docs)
        self.assertIn("not operator instructions", command_docs)
        self.assertIn("Slash Compatibility Surface", skill_docs)
        self.assertIn("skills/agent-workflow-project-maker/commands.md", skill_docs)
        for name in names:
            self.assertIn(name, command_docs)
            self.assertIn(name, skill_docs)

    def test_workflow_intake_contract_lives_in_skill_not_python_surface(self) -> None:
        skill_docs = (REPO_ROOT / "skills/agent-workflow-project-maker/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertFalse((REPO_ROOT / "scripts/workflow_skill_slash_surface.py").exists())
        self.assertFalse((REPO_ROOT / "scripts/tracker_workflow_intake_start.py").exists())
        self.assertIn("Show visible ECC proof before grilling", skill_docs)
        self.assertIn("ECC concepts", skill_docs)
        self.assertIn("Draft scaffold files", skill_docs)


if __name__ == "__main__":
    unittest.main()
