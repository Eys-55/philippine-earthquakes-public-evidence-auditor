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

    def test_workflow_bug_intake_requires_visible_ecc_proof_before_grilling(self) -> None:
        intake = workflow_skill_slash_surface.build_intake_result(
            raw_report="I found a bug in the earthquake workflow intake.",
            workflow_run_id="wfr-test",
            session_id="session-test",
            project_id="agent-workflow-project-maker",
            affected_workflow="philippines-building-code-evidence-auditor-v2",
            run_date="2026-07-06",
        )

        self.assertEqual("workflow_intake", intake["current_skill"])
        self.assertEqual("workflow_specific_bug", intake["flow_id"])
        self.assertEqual(
            "ops/workflow-runs/2026-07-06/wfr-test-context.md",
            intake["context_manifest_path"],
        )
        proof = intake["visible_ecc_proof"]
        self.assertIn("AGENTS.md", proof["ecc_files_loaded"])
        self.assertIn(
            "skills/agent-workflow-project-maker/SKILL.md",
            proof["workflow_context_files_loaded"],
        )
        self.assertIn("philippines-building-code-evidence-auditor-v2", proof["premise"])
        self.assertIn("workflow", proof["first_context_aware_question"].lower())

    def test_loop_reports_load_loop_specific_ecc_docs(self) -> None:
        intake = workflow_skill_slash_surface.build_intake_result(
            raw_report="The loop keeps going and does not stop.",
            workflow_run_id="wfr-loop",
            session_id="session-test",
            project_id="agent-workflow-project-maker",
            affected_workflow="philippines-building-code-evidence-auditor-v2",
            run_date="2026-07-06",
        )

        proof = intake["visible_ecc_proof"]
        concept_ids = [concept["id"] for concept in proof["ecc_concepts_loaded"]]
        self.assertIn("loop", concept_ids)
        self.assertIn(
            "docs/plans/2026-07-05-building-code-agent-loop.md",
            proof["workflow_context_files_loaded"],
        )
        loop = next(concept for concept in proof["ecc_concepts_loaded"] if concept["id"] == "loop")
        self.assertIn("locked objective", loop["meaning"])

    def test_new_workflow_confirmation_creates_scaffold_plan_with_progress_markers(self) -> None:
        self.assertTrue(
            workflow_skill_slash_surface.is_new_workflow_confirmation(
                "Create a new workflow for this"
            )
        )
        self.assertTrue(
            workflow_skill_slash_surface.is_new_workflow_confirmation(
                "This is not a continuation. Start a new workflow."
            )
        )

        plan = workflow_skill_slash_surface.scaffold_plan(
            workflow_slug="Client Intake Loop",
            workflow_run_id="wfr-scaffold",
            run_date="2026-07-06",
        )
        paths = [file["path"] for file in plan["files"]]

        self.assertEqual("client-intake-loop", plan["workflow_slug"])
        self.assertIn("skills/client-intake-loop/SKILL.md", paths)
        self.assertIn("data/client-intake-loop/.gitkeep", paths)
        self.assertIn("docs/status/2026-07-06-client-intake-loop-status.md", paths)
        self.assertIn("ops/workflow-runs/2026-07-06/wfr-scaffold-context.md", paths)
        for file in plan["files"]:
            self.assertEqual("draft", file["status"])
            self.assertEqual("0%", file["progress"])
            self.assertEqual("not reached", file["current_phase"])
            self.assertIn("Not reached yet", file["not_yet_reached_marker"])

    def test_closeout_is_not_continue_safe_until_uploaded(self) -> None:
        pending = workflow_skill_slash_surface.closeout_summary(upload_status="pending")
        uploaded = workflow_skill_slash_surface.closeout_summary(upload_status="uploaded")

        self.assertFalse(pending["continue_safe"])
        self.assertIn("push", pending["next_action"])
        self.assertTrue(uploaded["continue_safe"])


if __name__ == "__main__":
    unittest.main()
