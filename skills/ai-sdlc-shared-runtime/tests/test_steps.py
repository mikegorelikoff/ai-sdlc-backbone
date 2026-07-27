#!/usr/bin/env python3
"""Progressive-disclosure manifest and selector contract tests."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(RUNTIME))

import ai_sdlc_steps as STEPS


BASELINE_SKILL_WORDS = 79_950
MAX_ROUTER_LINES = 120
MAX_ROUTER_WORD_RATIO = 0.40


def manifests() -> list[Path]:
    return sorted((ROOT / "skills").glob("*/steps/manifest.json"))


def fixture(
    root: Path,
    *,
    selector: dict[str, object] | None = None,
    step_text: str | None = None,
) -> Path:
    skill = root / "skills" / "ai-sdlc-fixture"
    step = skill / "steps" / "execute.md"
    step.parent.mkdir(parents=True)
    content = step_text or (
        "# Execute\n\n## Entry\n\nUse bounded fixture evidence.\n\n"
        "## Procedure\n\nPerform the selected fixture action deterministically.\n\n"
        "## Exit\n\nReturn explicit validation evidence and stop.\n"
    )
    step.write_text(content, encoding="utf-8")
    skill.joinpath("SKILL.md").write_text(
        "---\nname: ai-sdlc-fixture\ndescription: Fixture.\n---\n\n"
        "# Fixture\n\n[`steps/execute.md`](steps/execute.md)\n",
        encoding="utf-8",
    )
    record = selector or {
        "id": "execute",
        "path": "steps/execute.md",
        "phases": ["execute"],
        "roles": ["software-engineer"],
        "actions": [],
        "load": "on-demand",
        "max_tokens": 256,
        "reason": "execute the bounded fixture procedure",
    }
    skill.joinpath("steps/manifest.json").write_text(
        json.dumps(
            {
                "schema": STEPS.SCHEMA,
                "skill": "ai-sdlc-fixture",
                "selectors": [record],
            }
        ),
        encoding="utf-8",
    )
    return skill


class StepManifestTests(unittest.TestCase):
    def test_every_installable_skill_has_a_valid_linked_manifest(self) -> None:
        skill_docs = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skill_docs), 44)
        self.assertEqual(len(manifests()), 44)
        for skill_doc in skill_docs:
            with self.subTest(skill=skill_doc.parent.name):
                skill_root, manifest = STEPS.load_manifest(
                    ROOT, skill_doc.parent.name
                )
                declared = {
                    selector["path"] for selector in manifest["selectors"]
                }
                actual = {
                    path.relative_to(skill_root).as_posix()
                    for path in (skill_root / "steps").glob("*.md")
                }
                self.assertEqual(declared, actual)
                router = skill_doc.read_text(encoding="utf-8")
                for relative in declared:
                    self.assertIn(relative, router)

    def test_routers_meet_line_and_aggregate_word_budgets(self) -> None:
        skill_docs = sorted((ROOT / "skills").glob("*/SKILL.md"))
        total_words = 0
        for skill_doc in skill_docs:
            text = skill_doc.read_text(encoding="utf-8")
            lines = text.count("\n") + 1
            total_words += len(text.split())
            with self.subTest(skill=skill_doc.parent.name):
                self.assertLess(lines, MAX_ROUTER_LINES)
                self.assertIn("## Step Selector", text)
                self.assertIn("## Progressive Disclosure Contract", text)
        self.assertLessEqual(
            total_words,
            int(BASELINE_SKILL_WORDS * MAX_ROUTER_WORD_RATIO),
        )

    def test_step_files_are_complete_procedures(self) -> None:
        for path in sorted((ROOT / "skills").glob("*/steps/*.md")):
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("## Entry", text)
                self.assertIn("## Procedure", text)
                self.assertIn("## Exit", text)
                self.assertGreaterEqual(len(text.split()), 80)

    def test_required_contract_survives_router_split(self) -> None:
        tokens = (
            "--quick-flow",
            "--full-flow",
            "_ai_sdlc/state.toon",
            "artifact_metadata",
            "metatags",
            "specs-index.toon",
            "index.md",
            "Do not create `summary.txt`",
            "directly in the active agent response",
            ".agents/skills/",
            "ai-sdlc-shared-runtime",
        )
        for skill_doc in sorted((ROOT / "skills").glob("*/SKILL.md")):
            manifest = json.loads(
                (skill_doc.parent / "steps/manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            aggregate = skill_doc.read_text(encoding="utf-8")
            aggregate += "\n".join(
                (skill_doc.parent / selector["path"]).read_text(encoding="utf-8")
                for selector in manifest["selectors"]
            )
            for token in tokens:
                with self.subTest(skill=skill_doc.parent.name, token=token):
                    self.assertIn(token, aggregate)

    def test_representative_role_phase_selection_is_deterministic(self) -> None:
        cases = (
            ("ai-sdlc-ba", "execute", "business-analyst"),
            ("ai-sdlc-prfaq-package-synthesis", "execute", "product-manager"),
            ("ai-sdlc-architecture", "execute", "software-architect"),
            ("ai-sdlc-sdd", "execute", "software-engineer"),
            ("ai-sdlc-qa", "validate", "qa-engineer"),
        )
        for skill, phase, role in cases:
            with self.subTest(skill=skill, phase=phase, role=role):
                first = STEPS.select_steps(ROOT, skill, phase, role=role)
                second = STEPS.select_steps(ROOT, skill, phase, role=role)
                self.assertEqual(first, second)
                self.assertEqual(len(first.selected), 1)
                self.assertGreater(first.broad_tokens, first.selected_tokens)
                self.assertGreater(first.savings_percent, 0)

    def test_role_and_action_filters_are_optional_constraints(self) -> None:
        selection = STEPS.select_steps(ROOT, "ai-sdlc-sdd", "execute")
        self.assertEqual(len(selection.selected), 1)

    def test_unknown_phase_role_and_skill_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "STEP_UNKNOWN_PHASE"):
            STEPS.select_steps(ROOT, "ai-sdlc-sdd", "invent")
        with self.assertRaisesRegex(ValueError, "STEP_UNKNOWN_ROLE"):
            STEPS.select_steps(ROOT, "ai-sdlc-sdd", "execute", role="manager")
        with self.assertRaisesRegex(ValueError, "STEP_UNKNOWN_SKILL"):
            STEPS.select_steps(ROOT, "ai-sdlc-missing", "execute")

    def test_incomplete_target_skill_cannot_fall_back_to_packaged_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shadow = root / "skills" / "ai-sdlc-sdd"
            shadow.mkdir(parents=True)
            shadow.joinpath("SKILL.md").write_text(
                "---\nname: ai-sdlc-sdd\ndescription: Incomplete shadow.\n---\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing steps/manifest.json"):
                STEPS.load_manifest(root, "ai-sdlc-sdd")

    def test_broken_target_symlink_cannot_fall_back_to_packaged_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skills = root / "skills"
            skills.mkdir()
            (skills / "ai-sdlc-sdd").symlink_to(root / "missing-skill")
            with self.assertRaisesRegex(ValueError, "unsafe target skill directory"):
                STEPS.load_manifest(root, "ai-sdlc-sdd")

    def test_role_mismatch_returns_no_match(self) -> None:
        with self.assertRaisesRegex(ValueError, "STEP_NO_MATCH"):
            STEPS.select_steps(
                ROOT,
                "ai-sdlc-sdd",
                "execute",
                role="qa-engineer",
            )

    def test_traversal_and_token_overflow_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bad_path = {
                "id": "execute",
                "path": "steps/../secret.md",
                "phases": ["execute"],
                "roles": [],
                "actions": [],
                "load": "on-demand",
                "max_tokens": 256,
                "reason": "escaping path must fail closed",
            }
            fixture(root, selector=bad_path)
            with self.assertRaisesRegex(ValueError, "STEP_UNSAFE_PATH"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            too_large = "# Execute\n\n" + ("bounded evidence " * 500)
            fixture(root, step_text=too_large)
            with self.assertRaisesRegex(ValueError, "STEP_TOKEN_OVERFLOW"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")

    def test_symlink_step_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = fixture(root)
            step = skill / "steps" / "execute.md"
            target = skill / "target.md"
            target.write_text("# Target\n", encoding="utf-8")
            step.unlink()
            step.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "STEP_UNSAFE_PATH"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")

    def test_undeclared_step_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = fixture(root)
            skill.joinpath("steps/hidden.md").write_text(
                "# Hidden\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "undeclared step files"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")

    def test_overlapping_selectors_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = fixture(root)
            second = skill / "steps" / "also-execute.md"
            second.write_text(
                "# Also Execute\n\n## Entry\n\nEnter safely.\n\n"
                "## Procedure\n\nPerform the second bounded action.\n\n"
                "## Exit\n\nReturn evidence and stop.\n",
                encoding="utf-8",
            )
            router = skill / "SKILL.md"
            router.write_text(
                router.read_text(encoding="utf-8")
                + "\n[`steps/also-execute.md`](steps/also-execute.md)\n",
                encoding="utf-8",
            )
            manifest_path = skill / "steps" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["selectors"].append(
                {
                    "id": "also-execute",
                    "path": "steps/also-execute.md",
                    "phases": ["execute"],
                    "roles": ["software-engineer"],
                    "actions": [],
                    "load": "on-demand",
                    "max_tokens": 256,
                    "reason": "overlapping selector must fail closed",
                }
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "overlapping selectors"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")


if __name__ == "__main__":
    unittest.main()
