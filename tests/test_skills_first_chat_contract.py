from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

AUTHORITATIVE_FILES = [
    "AGENTS.md",
    "CONTEXT.md",
    "docs/adr/0001-track-workflow-runs-as-session-scoped-operations.md",
    "skills/agent-workflow-project-maker/SKILL.md",
    "skills/control-repo-manager/SKILL.md",
]

ADAPTER_DOCS = [
    "skills/agent-workflow-project-maker/commands.md",
    "skills/control-repo-manager/commands.md",
]


class SkillsFirstChatContractTests(unittest.TestCase):
    def test_authoritative_docs_declare_chat_and_skills_as_operator_interface(self) -> None:
        required_phrases = [
            "Skills are the operator interface",
            "Codex chat is the operator surface",
            "The user never runs tracker scripts",
            "scripts are internal adapters",
        ]

        for relative_path in AUTHORITATIVE_FILES:
            with self.subTest(path=relative_path):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                for phrase in required_phrases:
                    self.assertIn(phrase, text)

    def test_command_docs_are_marked_internal_adapter_docs(self) -> None:
        for relative_path in ADAPTER_DOCS:
            with self.subTest(path=relative_path):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("Internal Adapter Reference", text)
                self.assertIn("not operator instructions", text)
                self.assertIn("Do not tell the user to run", text)

    def test_agent_workflow_skill_triggers_on_plain_chat_workflow_intent(self) -> None:
        text = (REPO_ROOT / "skills/agent-workflow-project-maker/SKILL.md").read_text(
            encoding="utf-8"
        )

        triggers = [
            "I am building a workflow",
            "I found a bug in my workflow",
            "create a workflow",
            "continue this workflow",
        ]
        for trigger in triggers:
            self.assertIn(trigger, text)


if __name__ == "__main__":
    unittest.main()
