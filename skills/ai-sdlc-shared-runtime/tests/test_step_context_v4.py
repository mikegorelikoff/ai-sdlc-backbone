#!/usr/bin/env python3
"""Deterministic context-engineering tests for executable StepCards."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path


RUNTIME = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(RUNTIME))

from ai_sdlc_step_context import (  # noqa: E402
    compile_step_context,
    validate_step_context_pack,
)
from ai_sdlc_steps import _build_card  # noqa: E402
from ai_sdlc_toon import encode_toon  # noqa: E402


STEP_TEXT = (
    "# Execute\n\n"
    "## Entry\n\n"
    "Use bounded evidence and preserve critical instructions.\n\n"
    "## Procedure\n\n"
    "Compile the minimum sufficient context deterministically.\n\n"
    "## Exit\n\n"
    "Return explicit evidence and the context fingerprint.\n"
)


def fixture(
    root: Path,
    *,
    step_text: str = STEP_TEXT,
    budget: int = 2_000,
    minimum_savings: float = 15.0,
    critical: tuple[str, ...] = ("## Entry", "## Procedure", "## Exit"),
) -> tuple[Path, dict[str, object]]:
    skill_root = root / "skills/ai-sdlc-fixture"
    steps_root = skill_root / "steps"
    steps_root.mkdir(parents=True)
    (steps_root / "execute.md").write_text(step_text, encoding="utf-8")
    step = {
        "id": "execute",
        "path": "steps/execute.md",
        "type": "action",
        "depends_on": [],
        "condition": {
            "phases": ["execute"],
            "roles": ["software-engineer"],
            "actions": [],
        },
        "load": "on-demand",
        "max_tokens": 512,
        "reason": "compile minimum sufficient context for deterministic execution",
        "operation": "execute-fixture",
        "capabilities": ["filesystem.read"],
        "side_effect": "none",
        "context": {
            "required": True,
            "budget_tokens": budget,
            "mandatory": ["step_document"],
            "selectors": [
                "step",
                "repository-instructions",
                "feature-traces",
                "changed-path-topology",
            ],
            "critical_anchors": list(critical),
            "min_savings_percent": minimum_savings,
            "fallback": "direct_read",
        },
        "gates": ["context-sufficient"],
        "outputs": ["context-evidence"],
        "max_attempts": 1,
        "commit_boundary": "none",
        "on_failure": "block",
    }
    return skill_root, step


class StepContextV4Tests(unittest.TestCase):
    """Exercise selection, authority, economics, safety, and identity."""

    def compile(
        self,
        root: Path,
        skill_root: Path,
        step: dict[str, object],
        *,
        explicit_paths: tuple[str, ...] = (),
        goal: str = "deterministic context execution",
        trace_ids: tuple[str, ...] = ("FR-007", "TC-011"),
    ):
        return compile_step_context(
            root=root,
            skill_root=skill_root,
            skill="ai-sdlc-fixture",
            step=step,
            explicit_paths=explicit_paths,
            goal=goal,
            trace_ids=trace_ids,
        )

    def test_packed_context_is_byte_stable_and_preserves_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_root, step = fixture(root)
            (root / "AGENTS.md").write_text(
                "# Repository Instructions\n\nKeep execution bounded and auditable.\n",
                encoding="utf-8",
            )
            source = root / "src/context_engine.py"
            source.parent.mkdir()
            source.write_text(
                "\n".join(
                    f"context_trace_{index} = 'deterministic context evidence'"
                    for index in range(1_200)
                )
                + "\n",
                encoding="utf-8",
            )

            first = self.compile(
                root,
                skill_root,
                step,
                explicit_paths=("src/context_engine.py", "AGENTS.md"),
            )
            second = self.compile(
                root,
                skill_root,
                step,
                explicit_paths=("AGENTS.md", "src/context_engine.py"),
            )

            self.assertEqual(first, second)
            self.assertEqual(
                encode_toon(asdict(first)),
                encode_toon(asdict(second)),
            )
            self.assertEqual(first.strategy, "packed")
            self.assertTrue(first.sufficient)
            self.assertEqual(first.critical_recall_percent, 100.0)
            self.assertGreaterEqual(first.savings_percent, 15.0)
            self.assertEqual(first.direct_read_paths, ())
            authority = {item.path: item.authority for item in first.selected}
            self.assertEqual(
                authority["ai-sdlc-fixture/steps/execute.md"],
                "skill_instruction",
            )
            self.assertEqual(
                authority["AGENTS.md"],
                "repository_instruction",
            )
            self.assertEqual(
                authority["src/context_engine.py"],
                "evidence_only",
            )
            validate_step_context_pack(
                asdict(first),
                expected_skill="ai-sdlc-fixture",
                expected_step_id="execute",
                require_sufficient=True,
            )

    def test_low_savings_uses_explicit_direct_read_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_root, step = fixture(root)
            result = self.compile(root, skill_root, step)
            self.assertTrue(result.sufficient)
            self.assertEqual(result.strategy, "direct_read")
            self.assertEqual(result.savings_percent, 0.0)
            self.assertEqual(
                result.direct_read_paths,
                ("ai-sdlc-fixture/steps/execute.md",),
            )

    def test_missing_critical_anchor_makes_step_card_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_root, step = fixture(
                root,
                critical=("## Entry", "MUST-PRESERVE-THIS-ANCHOR"),
            )
            result = self.compile(root, skill_root, step)
            self.assertFalse(result.sufficient)
            self.assertEqual(result.critical_recall_percent, 50.0)
            self.assertIn("missing critical anchors", result.reason)
            card = _build_card(
                root=root,
                skill_root=skill_root.resolve(),
                skill="ai-sdlc-fixture",
                step=step,
                graph_fingerprint="a" * 64,
                explicit_paths=(),
                goal="",
                trace_ids=(),
            )
            self.assertFalse(card.ready)

    def test_unsafe_secret_symlink_and_missing_paths_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_root, step = fixture(root)
            (root / "safe.md").write_text("safe evidence\n", encoding="utf-8")
            (root / "linked.md").symlink_to(root / "safe.md")
            result = self.compile(
                root,
                skill_root,
                step,
                explicit_paths=(
                    "../outside.md",
                    "config/api-token.txt",
                    "linked.md",
                    "missing.md",
                ),
            )
            selected_paths = {item.path for item in result.selected}
            self.assertNotIn("../outside.md", selected_paths)
            self.assertNotIn("config/api-token.txt", selected_paths)
            self.assertNotIn("linked.md", selected_paths)
            self.assertNotIn("missing.md", selected_paths)
            self.assertIn("../outside.md:unsafe-or-secret-path", result.skipped)
            self.assertIn(
                "config/api-token.txt:unsafe-or-secret-path",
                result.skipped,
            )
            self.assertIn("linked.md:symlink", result.skipped)
            self.assertIn("missing.md:missing", result.skipped)

    def test_pack_fingerprint_detects_semantic_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_root, step = fixture(root)
            value = asdict(self.compile(root, skill_root, step))
            tampered = copy.deepcopy(value)
            tampered["reason"] = "changed after compilation"
            with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
                validate_step_context_pack(tampered)


if __name__ == "__main__":
    unittest.main()
