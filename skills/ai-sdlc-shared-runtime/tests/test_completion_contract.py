"""Regression tests for dependency-consistent step completion claims."""

import tempfile
import unittest
from pathlib import Path

from test_steps import STEPS, fixture, toon_codec
from ai_sdlc_state_machine import STAGE_BY_SKILL, STAGE_BY_ID


class CompletionContractTests(unittest.TestCase):
    def test_declared_lifecycle_bindings_match_runtime_authority(self):
        root = Path(__file__).resolve().parents[3]
        for path in (root / "skills").glob("*/steps/01-prepare.md"):
            text = path.read_text()
            if "Registered stage:" not in text:
                continue
            with self.subTest(skill=path.parent.parent.name):
                stage = STAGE_BY_SKILL[path.parent.parent.name]
                self.assertIn(f"Registered stage: `{stage.stage_id}`", text)
                self.assertIn(f"Canonical output: `{stage.artifacts}`", text)
                for predecessor in stage.predecessors:
                    self.assertIn(f"`{STAGE_BY_ID[predecessor].skill}`", text)
                for consumer in STAGE_BY_ID.values():
                    if stage.stage_id in consumer.predecessors:
                        self.assertIn(f"`{consumer.skill}`", text)

    def test_handoff_cannot_bypass_output_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = fixture(root)
            path = skill / "steps/manifest.toon"
            manifest = toon_codec.decode_toon(path.read_text())
            manifest["steps"][-1]["depends_on"] = ["execute"]
            path.write_text(toon_codec.encode_toon(manifest))
            with self.assertRaisesRegex(ValueError, "unvalidated actions"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")

    def test_shared_contract_is_mandatory_and_changes_fingerprints(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = fixture(root)
            step = skill / "steps/preflight.md"
            step.write_text(step.read_text() +
                            "\n[decisions](../../ai-sdlc-shared-runtime/references/execution-contract.md)\n")
            with self.assertRaisesRegex(ValueError, "STEP_CONTEXT_INSUFFICIENT"):
                STEPS.select_steps(root, "ai-sdlc-fixture", "prepare")
            reference = root / "skills/ai-sdlc-shared-runtime/references/execution-contract.md"
            reference.parent.mkdir(parents=True)
            reference.write_text("Use source evidence.\n")
            first = STEPS.select_steps(root, "ai-sdlc-fixture", "prepare")
            self.assertTrue(any(item["path"].endswith("execution-contract.md")
                                for item in first.step_cards[0]["context"]["selected"]))
            reference.write_text("Use current source evidence.\n")
            second = STEPS.select_steps(root, "ai-sdlc-fixture", "prepare")
            self.assertNotEqual(first.graph_fingerprint, second.graph_fingerprint)
            self.assertNotEqual(first.step_cards[0]["context"]["fingerprint"],
                                second.step_cards[0]["context"]["fingerprint"])

    def test_completed_action_cannot_skip_its_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            with self.assertRaisesRegex(ValueError, "STEP_INVALID_COMPLETION"):
                STEPS.select_steps(root, "ai-sdlc-fixture", "validate",
                                   completed_steps=["execute"])

    def test_terminal_claim_cannot_skip_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            with self.assertRaisesRegex(ValueError, "STEP_INVALID_COMPLETION"):
                STEPS.select_steps(root, "ai-sdlc-fixture", "complete",
                                   completed_steps=["handoff"])

    def test_valid_prefix_resumes_at_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            result = STEPS.select_steps(root, "ai-sdlc-fixture", "complete",
                                        completed_steps=["preflight", "context", "execute"])
            self.assertEqual(result.ready_steps, ("validate",))
            self.assertFalse(result.complete)


if __name__ == "__main__":
    unittest.main()
