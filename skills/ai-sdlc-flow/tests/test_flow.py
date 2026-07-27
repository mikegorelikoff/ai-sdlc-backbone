#!/usr/bin/env python3
"""Behavior tests for guided Explore and Apply contracts."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE_PATH = ROOT / "skills" / "_shared" / "ai_sdlc_flow.py"
SCRIPT = ROOT / "skills" / "ai-sdlc-flow" / "scripts" / "flow.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_flow", CORE_PATH)
assert SPEC and SPEC.loader
FLOW = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FLOW
SPEC.loader.exec_module(FLOW)


class FlowTests(unittest.TestCase):
    """Pure and CLI contract tests."""

    def test_feedback_is_classified_before_feature_state(self) -> None:
        result = FLOW.classify_intent("Refinement based on user feedback")
        self.assertEqual(result[:4], ("new_refinement", "refinement", "discovery", "ai-sdlc-working-backwards-discovery"))

    def test_mixed_material_intent_blocks(self) -> None:
        result = FLOW.classify_intent("Use customer feedback and implement the API")
        self.assertEqual(result[0], "ambiguous")
        self.assertIn("FLOW_AMBIGUOUS_INTENT", result[4][0])

    def test_context_pack_requires_recall_and_net_savings(self) -> None:
        accepted = FLOW.choose_context(
            raw_tokens=1000, packed_tokens=700, reread_tokens=100,
            critical_total=4, critical_retained=4,
        )
        boundary = FLOW.choose_context(
            raw_tokens=10000, packed_tokens=8501, reread_tokens=0,
            critical_total=4, critical_retained=4,
        )
        anchor_loss = FLOW.choose_context(
            raw_tokens=1000, packed_tokens=500, reread_tokens=0,
            critical_total=4, critical_retained=3,
        )
        self.assertEqual(accepted.selected_strategy, "packed")
        self.assertEqual(boundary.savings_percent, 14.99)
        self.assertEqual(boundary.selected_strategy, "direct")
        self.assertEqual(anchor_loss.selected_strategy, "direct")
        with self.assertRaisesRegex(ValueError, "FLOW_INVALID_CONTEXT"):
            FLOW.choose_context(
                raw_tokens=100, packed_tokens=-1, reread_tokens=0,
                critical_total=1, critical_retained=1,
            )
        with self.assertRaisesRegex(ValueError, "FLOW_INVALID_CONTEXT"):
            FLOW.choose_context(
                raw_tokens=100, packed_tokens=50, reread_tokens=0,
                critical_total=1, critical_retained=2,
            )

    def test_roles_expand_only_from_evidence(self) -> None:
        roles, evidence = FLOW.select_roles("Implement a local parser", stage="sdd")
        self.assertEqual(roles, ("Contributor", "Repository Maintainer"))
        security_roles, security_evidence = FLOW.select_roles("Implement authorization checks", stage="sdd")
        self.assertIn("Security", security_roles)
        self.assertTrue(any("authorization" in item for item in security_evidence))
        self.assertFalse(any("customer" in item.lower() for item in evidence))

    def test_rigor_override_cannot_bypass_policy(self) -> None:
        rigor, reason, blockers = FLOW.select_rigor(
            "Fix local label", requested="quick", policy_requires_full=True
        )
        self.assertEqual(rigor, "full")
        self.assertIn("policy requires full", reason)
        self.assertEqual(blockers, ())

    def test_card_fingerprint_is_stable_and_semantic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            card1 = FLOW.build_card(
                root=root, intent="Implement API", feature="011-guided-explore-apply-flow"
            )
            card2 = FLOW.build_card(
                root=root, intent="  Implement   API ", feature="011-guided-explore-apply-flow"
            )
            changed = FLOW.build_card(
                root=root, intent="Implement API security", feature="011-guided-explore-apply-flow"
            )
            self.assertEqual(card1.fingerprint, card2.fingerprint)
            self.assertNotEqual(card1.fingerprint, changed.fingerprint)

    def test_symlink_feature_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "specs").mkdir()
            target = root / "real"
            target.mkdir()
            (root / "specs" / "011-guided-explore-apply-flow").symlink_to(target, target_is_directory=True)
            resolved, blockers = FLOW.validate_workspace(
                root, "011-guided-explore-apply-flow", "implementation"
            )
            self.assertIsNone(resolved)
            self.assertTrue(any("symlink" in blocker for blocker in blockers))

    def test_symlink_workspace_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "real-specs"
            target.mkdir()
            (root / "specs").symlink_to(target, target_is_directory=True)
            resolved, blockers = FLOW.validate_workspace(
                root, "011-guided-explore-apply-flow", "implementation"
            )
            self.assertIsNone(resolved)
            self.assertTrue(any("workspace root" in blocker for blocker in blockers))

    def test_explore_json_is_read_only_and_apply_verifies_one_action(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "specs").mkdir()
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            explored = subprocess.run(
                [
                    "python3", str(SCRIPT), "explore", "--root", str(root),
                    "--intent", "Implement API", "--feature", "011-guided-explore-apply-flow",
                    "--format", "json",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(explored.returncode, 0, explored.stderr)
            self.assertEqual(before, after)
            card = json.loads(explored.stdout)
            verified = subprocess.run(
                ["python3", str(SCRIPT), "apply", "--root", str(root), "--card", "-"],
                input=explored.stdout, check=False, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            action = json.loads(verified.stdout)
            self.assertEqual(action["status"], "verified")
            self.assertEqual(action["action"].count("begin"), 1)

    def test_explicit_source_cannot_remove_mandatory_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config" / "ai-sdlc.defaults.json").write_text("{}\n", encoding="utf-8")
            extra = root / "extra.md"
            extra.write_text("extra\n", encoding="utf-8")
            records = FLOW.discover_sources(root, "011-guided-explore-apply-flow", (extra,))
            self.assertTrue(any(item.startswith("config/ai-sdlc.defaults.json:") for item in records))
            self.assertTrue(any(item.startswith("extra.md:") for item in records))

    def test_apply_rejects_source_drift_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "specs").mkdir()
            evidence = root / "evidence.md"
            evidence.write_text("accepted\n", encoding="utf-8")
            explored = subprocess.run(
                [
                    "python3", str(SCRIPT), "explore", "--root", str(root),
                    "--intent", "Implement API", "--feature", "011-guided-explore-apply-flow",
                    "--source", "evidence.md", "--format", "json",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            evidence.write_text("changed\n", encoding="utf-8")
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            applied = subprocess.run(
                ["python3", str(SCRIPT), "apply", "--root", str(root), "--card", "-"],
                input=explored.stdout, check=False, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(applied.returncode, 2)
            self.assertIn("FLOW_ROUTE_DRIFT", applied.stderr)
            self.assertEqual(before, after)

    def test_spec_first_review_hides_rationale_until_findings(self) -> None:
        seeded_diff = "BUG[P1]: bypass state guard\nREADABILITY: opaque branch names"
        packet = FLOW.build_independent_review_packet(
            requirements="state guard is mandatory",
            tests="accepted state must reject mutation",
            diff=seeded_diff,
        )
        self.assertIn("BUG[P1]", packet["diff"])
        self.assertIn("READABILITY", packet["diff"])
        self.assertNotIn("ai_rationale", packet)
        self.assertNotIn("prior_verdict", packet)
        with self.assertRaisesRegex(ValueError, "FLOW_REVIEW_ORDER"):
            FLOW.reveal_review_context(
                independent_findings=[],
                ai_rationale="looks correct",
                prior_verdict="approved",
            )
        comparison = FLOW.reveal_review_context(
            independent_findings=("P1 state-guard bypass", "readability violation"),
            ai_rationale="looks correct",
            prior_verdict="approved",
        )
        self.assertEqual(comparison["phase"], "comparison")

    def test_clean_review_can_record_explicit_no_findings(self) -> None:
        comparison = FLOW.reveal_review_context(
            independent_findings=("No findings.",),
            ai_rationale="clean implementation",
            prior_verdict="not reviewed",
        )
        self.assertEqual(comparison["independent_findings"], ("No findings.",))

    def test_markdown_and_toon_share_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            card = FLOW.build_card(
                root=Path(temp), intent="Review diff", feature="011-guided-explore-apply-flow",
                sources=("requirements.md:abc",),
            )
            self.assertIn(card.fingerprint, FLOW.render_markdown(card))
            self.assertIn(card.fingerprint, FLOW.render_toon(card))
            self.assertIn("requirements.md:abc", FLOW.render_markdown(card))
            self.assertIn("requirements.md:abc", FLOW.render_toon(card))
            self.assertIn("confidence 1.00", FLOW.render_markdown(card))


if __name__ == "__main__":
    unittest.main()
