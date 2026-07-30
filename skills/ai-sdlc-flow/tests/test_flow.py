#!/usr/bin/env python3
"""Behavior tests for guided Explore and Apply contracts."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
CORE_PATH = ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts" / "ai_sdlc_flow.py"
SCRIPT = ROOT / "skills" / "ai-sdlc-flow" / "scripts" / "flow.py"
sys.path.insert(0, str(CORE_PATH.parent))
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

    def test_former_navigator_routes_are_preserved(self) -> None:
        fixtures = {
            "Prepare a commit": "ai-sdlc-commit-prep",
            "Run an OWASP security review": "ai-sdlc-security-testing",
            "Review QA coverage and testability": "ai-sdlc-qa-requirements-gap-review",
            "Decompose this backlog into stories": "ai-sdlc-user-story-decomposition",
            "Discover a new product idea": "ai-sdlc-working-backwards-discovery",
            "Review PR": "ai-sdlc-code-review",
            "Run regression validation": "ai-sdlc-validation",
            "Implement GET /health behavior while preserving existing route behavior.": "ai-sdlc-sdd",
        }
        for intent, expected in fixtures.items():
            with self.subTest(intent=intent):
                self.assertEqual(FLOW.classify_intent(intent)[3], expected)

    def test_guided_entrypoint_is_unique_in_active_inventories(self) -> None:
        navigator = "ai-sdlc-navigator"
        self.assertFalse((ROOT / "skills" / navigator / "SKILL.md").exists())
        inventories = (
            ROOT / "compatibility" / "baseline-v1.toon",
            ROOT / "config" / "ai-sdlc-managed-skills.txt",
            ROOT / "modules" / "core" / "module.toon",
            ROOT / "skills" / "ai-sdlc-shared-runtime"
            / "references" / "ai-sdlc-managed-skills.txt",
        )
        for inventory in inventories:
            with self.subTest(inventory=inventory):
                self.assertNotIn(
                    navigator, inventory.read_text(encoding="utf-8")
                )

    def test_active_feature_state_has_priority_over_new_intent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = (
                root
                / "specs"
                / "011-guided-explore-apply-flow"
                / "_ai_sdlc"
                / "state.toon"
            )
            state.parent.mkdir(parents=True)
            state.write_text(
                "feature: 011-guided-explore-apply-flow\n"
                "workspace: implementation\n"
                "current_stage: sdd\n"
                "active_skill: ai-sdlc-sdd\n\n"
                "stages[1]{id,skill,status,workspace,artifacts,decision_ref}:\n"
                "  sdd,ai-sdlc-sdd,in_progress,implementation,specs/011-guided-explore-apply-flow,DEC-001\n\n"
                "skips[0]{stage,reason,decision_ref,flow_mode}:\n",
                encoding="utf-8",
            )

            card = FLOW.build_card(
                root=root,
                intent="Prepare a commit",
                feature="011-guided-explore-apply-flow",
            )

            self.assertEqual(card.skill, "ai-sdlc-sdd")
            self.assertIn("active feature state", card.intent_reason)

    def test_earliest_incomplete_state_stage_guides_apply_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = (
                root
                / "specs"
                / "011-guided-explore-apply-flow"
                / "_ai_sdlc"
                / "state.toon"
            )
            state.parent.mkdir(parents=True)
            state.write_text(
                "feature: 011-guided-explore-apply-flow\n"
                "workspace: implementation\n"
                "current_stage: branching\n"
                "active_skill:\n\n"
                "stages[2]{id,skill,status,workspace,artifacts,decision_ref}:\n"
                "  branching,ai-sdlc-branching,not_started,implementation,branch-plan.md,\n"
                "  sdd,ai-sdlc-sdd,not_started,implementation,specs/011-guided-explore-apply-flow,\n\n"
                "skips[0]{stage,reason,decision_ref,flow_mode}:\n",
                encoding="utf-8",
            )

            card = FLOW.build_card(
                root=root,
                intent="Implement API",
                feature="011-guided-explore-apply-flow",
            )

            self.assertEqual(card.skill, "ai-sdlc-branching")
            self.assertIn("earliest incomplete", card.intent_reason)

    def test_unrelated_optional_stage_does_not_hijack_commit_route(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            state = (
                root
                / "specs"
                / "011-guided-explore-apply-flow"
                / "_ai_sdlc"
                / "state.toon"
            )
            state.parent.mkdir(parents=True)
            state.write_text(
                "feature: 011-guided-explore-apply-flow\n"
                "workspace: implementation\n"
                "current_stage: commit_prep\n"
                "active_skill:\n\n"
                "stages[6]{id,skill,status,workspace,artifacts,decision_ref}:\n"
                "  branching,ai-sdlc-branching,done,implementation,branch-plan.md,\n"
                "  sdd,ai-sdlc-sdd,done,implementation,specs/011-guided-explore-apply-flow,\n"
                "  validation,ai-sdlc-validation,done,implementation,validation.md,\n"
                "  code_review,ai-sdlc-code-review,done,implementation,code-review.md,\n"
                "  security_testing,ai-sdlc-security-testing,not_started,implementation,security-review.md,\n"
                "  commit_prep,ai-sdlc-commit-prep,not_started,implementation,commit-readiness.md,\n\n"
                "skips[0]{stage,reason,decision_ref,flow_mode}:\n",
                encoding="utf-8",
            )

            card = FLOW.build_card(
                root=root,
                intent="Prepare a commit",
                feature="011-guided-explore-apply-flow",
            )

            self.assertEqual(card.skill, "ai-sdlc-commit-prep")

    def test_shared_base_branch_routes_implementation_to_branching(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(
                ["git", "init", "-b", "main"],
                cwd=root,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "-c",
                    "commit.gpgsign=false",
                    "commit",
                    "--allow-empty",
                    "-m",
                    "fixture",
                ],
                cwd=root,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            card = FLOW.build_card(
                root=root,
                intent="Implement API",
                feature="011-guided-explore-apply-flow",
            )

            self.assertEqual(card.skill, "ai-sdlc-branching")
            self.assertIn("shared base branch", card.intent_reason)

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

    def test_exactly_one_role_is_selected_from_evidence(self) -> None:
        roles, evidence = FLOW.select_roles("Implement a local parser", stage="sdd")
        self.assertEqual(roles, ("software-engineer",))
        security_roles, security_evidence = FLOW.select_roles("Implement authorization checks", stage="sdd")
        self.assertEqual(security_roles, ("software-engineer",))
        self.assertEqual(len(security_evidence), 1)
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

    def test_explore_toon_is_read_only_and_apply_verifies_one_action(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "specs").mkdir()
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            explored = subprocess.run(
                [
                    "python3", str(SCRIPT), "explore", "--root", str(root),
                    "--intent", "Implement API", "--feature", "011-guided-explore-apply-flow",
                    "--format", "toon",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(explored.returncode, 0, explored.stderr)
            self.assertEqual(before, after)
            card = toon_codec.loads(explored.stdout)
            verified = subprocess.run(
                ["python3", str(SCRIPT), "apply", "--root", str(root), "--card", "-"],
                input=explored.stdout, check=False, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            action = toon_codec.loads(verified.stdout)
            self.assertEqual(action["status"], "verified")
            self.assertEqual(action["schema"], "ai-sdlc-flow-apply/v3")
            self.assertGreater(action["planned_tasks"], 0)
            self.assertFalse((root / "_ai_sdlc/runs").exists())
            started = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "apply",
                    "--root",
                    str(root),
                    "--card",
                    "-",
                    "--execute",
                    "--run-id",
                    "flow-run",
                ],
                input=explored.stdout,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(started.returncode, 0, started.stderr)
            receipt = toon_codec.loads(started.stdout)
            self.assertEqual(receipt["status"], "started")
            self.assertTrue(
                (root / "_ai_sdlc/runs/flow-run/journal/000001.toon").is_file()
            )

    def test_explicit_source_cannot_remove_mandatory_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config" / "ai-sdlc.defaults.toon").write_text(
                toon_codec.dumps({}) + "\n",
                encoding="utf-8",
            )
            extra = root / "extra.md"
            extra.write_text("extra\n", encoding="utf-8")
            records = FLOW.discover_sources(root, "011-guided-explore-apply-flow", (extra,))
            self.assertTrue(any(item.startswith("config/ai-sdlc.defaults.toon:") for item in records))
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
                    "--source", "evidence.md", "--format", "toon",
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

    def test_v3_card_exposes_step_card_and_run_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            card = FLOW.build_card(
                root=Path(temp),
                intent="Implement the API",
                feature="013-role-guided-installable-flow",
                requested_action="implementation",
            )
            self.assertEqual(card.schema, "ai-sdlc-flow/v3")
            self.assertEqual(card.active_role, "software-engineer")
            self.assertEqual(card.roles, ("software-engineer",))
            self.assertEqual(card.action_code, "BUILD")
            self.assertEqual(card.current_step, "execute")
            self.assertTrue(any("roles/software-engineer.md" in item for item in card.selected_references))
            self.assertTrue(any("steps/execute.md" in item for item in card.selected_references))
            self.assertEqual(
                card.skill_step_reference,
                "ai-sdlc-sdd/steps/01-prepare.md",
            )
            self.assertTrue(card.step_manifest_fingerprint)
            self.assertEqual(card.step_card["schema"], "ai-sdlc-step-card/v1")
            self.assertEqual(card.run_plan["schema"], "ai-sdlc-run-plan/v2")
            self.assertEqual(
                card.run_plan_fingerprint,
                card.run_plan["fingerprint"],
            )
            self.assertEqual(card.context_economics.recall_percent, 100.0)
            self.assertGreaterEqual(card.context_economics.savings_percent, 15.0)

    def test_role_override_records_explicit_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            card = FLOW.build_card(
                root=Path(temp),
                intent="Implement the API",
                feature="013-role-guided-installable-flow",
                requested_role="business-analyst",
                requested_action="implementation",
            )
            self.assertEqual(card.requested_role, "business-analyst")
            self.assertEqual(card.active_role, "software-engineer")
            self.assertIn("owns implementation", card.role_handoff_reason)

    def test_every_flow_action_resolves_an_owning_skill_step(self) -> None:
        registry = FLOW.load_registry(ROOT)
        with tempfile.TemporaryDirectory() as temp:
            for action in registry["actions"]:
                with self.subTest(action=action["id"]):
                    card = FLOW.build_card(
                        root=Path(temp),
                        intent="Run the selected lifecycle action",
                        feature="013-role-guided-installable-flow",
                        requested_action=action["id"],
                    )
                    self.assertTrue(card.skill_step_reference)
                    self.assertFalse(
                        any(blocker.startswith("STEP_") for blocker in card.blockers),
                        card.blockers,
                    )

    def test_ambiguous_intent_emits_deterministic_menu(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            card = FLOW.build_card(
                root=Path(temp),
                intent="Help with this work",
                feature="013-role-guided-installable-flow",
            )
            self.assertEqual(card.intent_class, "ambiguous")
            self.assertEqual(card.menu_options, tuple(sorted(card.menu_options)))
            self.assertGreater(len(card.menu_options), 5)

    def test_legacy_card_is_rejected_with_migration_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            payload = toon_codec.dumps({"schema": "ai-sdlc-flow/v1"})
            result = subprocess.run(
                ["python3", str(SCRIPT), "apply", "--root", temp, "--card", "-"],
                input=payload, check=False, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("regenerate ai-sdlc-flow/v3", result.stderr)

    def test_apply_revalidates_the_same_bounded_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "specs").mkdir()
            team = root / "team.toon"
            team.write_text(toon_codec.dumps({
                "schema": "ai-sdlc-config/v1",
                "values": {"flow": {
                    "role_aliases": {"builder": "software-engineer"},
                    "menu_mode": "ambiguous",
                    "context_selectors": [],
                }},
            }), encoding="utf-8")
            explored = subprocess.run(
                [
                    "python3", str(SCRIPT), "explore", "--root", str(root),
                    "--intent", "Implement API", "--feature", "013-role-guided-installable-flow",
                    "--role", "builder", "--team", str(team), "--format", "toon",
                ],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(explored.returncode, 0, explored.stderr)
            verified = subprocess.run(
                [
                    "python3", str(SCRIPT), "apply", "--root", str(root),
                    "--team", str(team), "--card", "-",
                ],
                input=explored.stdout, check=False, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)

    def test_selector_rejects_registry_outside_flow_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            external = Path(temp) / "registry.toon"
            external.write_text(toon_codec.dumps({}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "FLOW_UNSAFE_SELECTOR"):
                FLOW.load_registry(ROOT, external)

    def test_direct_api_rejects_malformed_configured_selector(self) -> None:
        malformed = {
            "context_selectors": [
                {
                    "id": "unsafe",
                    "roles": ["unknown-role"],
                    "actions": ["implementation"],
                    "include": ["../outside.md"],
                    "priority": 50,
                    "max_tokens": 200,
                    "reason": "must remain contained",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "FLOW_INVALID_CONFIG"):
                FLOW.build_card(
                    root=Path(temp),
                    intent="Implement API",
                    feature="013-role-guided-installable-flow",
                    flow_config=malformed,
                )

    def test_direct_api_rejects_unknown_flow_config_field(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "unknown fields"):
                FLOW.build_card(
                    root=Path(temp),
                    intent="Implement API",
                    feature="013-role-guided-installable-flow",
                    flow_config={"unbounded_context": True},
                )


if __name__ == "__main__":
    unittest.main()
