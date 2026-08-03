#!/usr/bin/env python3
"""Progressive-disclosure manifest and selector contract tests."""

from __future__ import annotations

import sys
import shutil
import tempfile
import unittest
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(RUNTIME))

import ai_sdlc_steps as STEPS


BASELINE_SKILL_WORDS = 79_950
MAX_ROUTER_LINES = 120
MAX_ROUTER_WORD_RATIO = 0.40


def manifests() -> list[Path]:
    return sorted((ROOT / "skills").glob("*/steps/manifest.toon"))


def fixture(
    root: Path,
    *,
    selector: dict[str, object] | None = None,
    step_text: str | None = None,
) -> Path:
    skill = root / "skills" / "ai-sdlc-fixture"
    steps_root = skill / "steps"
    steps_root.mkdir(parents=True)
    content = step_text or (
        "# Execute\n\n## Entry\n\nUse bounded fixture evidence.\n\n"
        "## Procedure\n\nPerform the selected fixture action deterministically.\n\n"
        "## Exit\n\nReturn explicit validation evidence and stop.\n"
    )
    standard_content = (
        "# {title}\n\n## Entry\n\nUse bounded fixture evidence.\n\n"
        "## Procedure\n\nPerform this fixture checkpoint deterministically and "
        "preserve explicit evidence for the next dependency.\n\n"
        "## Exit\n\nReturn explicit validation evidence and stop.\n"
    )
    for step_id in ("preflight", "context", "validate", "handoff"):
        steps_root.joinpath(f"{step_id}.md").write_text(
            standard_content.format(title=step_id.title()),
            encoding="utf-8",
        )
    steps_root.joinpath("execute.md").write_text(content, encoding="utf-8")
    record = dict(selector or {})
    execute_path = str(record.pop("path", "steps/execute.md"))
    execute_id = str(record.pop("id", "execute"))
    execute_phases = list(record.pop("phases", ["execute"]))
    execute_roles = list(record.pop("roles", ["software-engineer"]))
    execute_actions = list(record.pop("actions", []))
    execute_max = int(record.pop("max_tokens", 256))
    execute_reason = str(
        record.pop("reason", "execute the bounded fixture procedure")
    )
    execute_load = str(record.pop("load", "on-demand"))
    skill.joinpath("SKILL.md").write_text(
        "---\nname: ai-sdlc-fixture\ndescription: Fixture.\n---\n\n"
        "# Fixture\n\n"
        "[`steps/preflight.md`](steps/preflight.md)\n"
        "[`steps/context.md`](steps/context.md)\n"
        f"[`{execute_path}`]({execute_path})\n"
        "[`steps/validate.md`](steps/validate.md)\n"
        "[`steps/handoff.md`](steps/handoff.md)\n",
        encoding="utf-8",
    )

    context = {
        "required": True,
        "budget_tokens": 512,
        "mandatory": ["step_document"],
        "selectors": ["step"],
        "critical_anchors": ["## Entry", "## Procedure", "## Exit"],
        "min_savings_percent": 0,
        "fallback": "direct_read",
    }

    def node(
        step_id: str,
        path: str,
        step_type: str,
        phases: list[str],
        depends_on: list[str],
        operation: str,
    ) -> dict[str, object]:
        return {
            "id": step_id,
            "path": path,
            "type": step_type,
            "depends_on": depends_on,
            "condition": {
                "phases": phases,
                "roles": ["software-engineer"],
                "actions": [],
            },
            "load": "required",
            "max_tokens": 256,
            "reason": f"run the deterministic {step_id} fixture checkpoint",
            "operation": operation,
            "capabilities": ["filesystem.read"],
            "side_effect": "none",
            "context": context,
            "gates": ["fixture-evidence"],
            "outputs": [f"{step_id}-evidence"],
            "max_attempts": 1,
            "commit_boundary": "none",
            "on_failure": "block",
        }

    graph = [
        node(
            "preflight",
            "steps/preflight.md",
            "analysis",
            ["prepare"],
            [],
            "inspect-fixture",
        ),
        node(
            "context",
            "steps/context.md",
            "context",
            ["clarify", "route"],
            ["preflight"],
            "compile-context",
        ),
        {
            **node(
                execute_id,
                execute_path,
                "action",
                execute_phases,
                ["context"],
                "execute-fixture",
            ),
            "condition": {
                "phases": execute_phases,
                "roles": execute_roles,
                "actions": execute_actions,
            },
            "load": execute_load,
            "max_tokens": execute_max,
            "reason": execute_reason,
            "side_effect": "workspace-write",
            **record,
        },
        node(
            "validate",
            "steps/validate.md",
            "validation",
            ["validate"],
            [execute_id],
            "validate-fixture",
        ),
        node(
            "handoff",
            "steps/handoff.md",
            "handoff",
            ["handoff", "complete"],
            ["validate"],
            "handoff-fixture",
        ),
    ]
    skill.joinpath("steps/manifest.toon").write_text(
        toon_codec.dumps(
            {
                "schema": STEPS.SCHEMA,
                "skill": "ai-sdlc-fixture",
                "version": STEPS.VERSION,
                "entrypoints": {
                    "prepare": ["preflight"],
                    "clarify": ["context"],
                    "route": ["context"],
                    "execute": [execute_id],
                    "validate": ["validate"],
                    "handoff": ["handoff"],
                    "complete": ["handoff"],
                },
                "budgets": {
                    "step_max_tokens": 512,
                    "context_max_tokens": 512,
                    "min_context_savings_percent": 0,
                },
                "steps": graph,
            }
        ),
        encoding="utf-8",
    )
    return skill


class StepManifestTests(unittest.TestCase):
    def test_every_installable_skill_has_a_valid_linked_manifest(self) -> None:
        skill_docs = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skill_docs), 46)
        self.assertEqual(len(manifests()), 46)
        for skill_doc in skill_docs:
            with self.subTest(skill=skill_doc.parent.name):
                skill_root, manifest = STEPS.load_manifest(
                    ROOT, skill_doc.parent.name
                )
                declared = {
                    selector["path"] for selector in manifest["steps"]
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
            manifest = toon_codec.loads(
                (skill_doc.parent / "steps/manifest.toon").read_text(
                    encoding="utf-8"
                )
            )
            aggregate = skill_doc.read_text(encoding="utf-8")
            aggregate += "\n".join(
                (skill_doc.parent / selector["path"]).read_text(encoding="utf-8")
                for selector in manifest["steps"]
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

    def test_context_cache_policy_is_exact_and_clamped_to_manifest(self) -> None:
        cache_root = ROOT / "skills/ai-sdlc-context-cache"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".ai-sdlc").mkdir()
            policy = {
                "schema": STEPS.CACHE_POLICY_SCHEMA,
                "defaults": {"budget_tokens": 9000, "limit": 8},
                "overrides": [
                    {
                        "skill": "ai-sdlc-ba",
                        "step_id": "execute",
                        "budget_tokens": 7000,
                        "graph_depth": 2,
                    }
                ],
            }
            path = root / ".ai-sdlc/context-cache-policy.toon"
            path.write_text(toon_codec.dumps(policy), encoding="utf-8")
            settings = STEPS._cache_settings(
                root, cache_root, "ai-sdlc-ba", "execute", 1200, 15.0
            )
            self.assertEqual(settings["budget_tokens"], 1200)
            self.assertEqual(settings["limit"], 8)
            self.assertEqual(settings["graph_depth"], 2)

            policy["defaults"]["unknown"] = True
            path.write_text(toon_codec.dumps(policy), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "CACHE_POLICY_INVALID"):
                STEPS._cache_settings(
                    root, cache_root, "ai-sdlc-ba", "execute", 1200, 15.0
                )

    def test_project_installed_cache_is_used_by_normal_stepcard_compilation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            installed = root / ".agents/skills"
            installed.mkdir(parents=True)
            for name in ("ai-sdlc-context-cache", "ai-sdlc-shared-runtime"):
                shutil.copytree(ROOT / "skills" / name, installed / name)
            evidence = root / "docs"
            evidence.mkdir()
            for index in range(6):
                evidence.joinpath(f"evidence-{index}.md").write_text(
                    ("fixture deterministic execution evidence\n" * 80),
                    encoding="utf-8",
                )
            selection = STEPS.select_steps(
                root,
                "ai-sdlc-fixture",
                "execute",
                role="software-engineer",
                goal="fixture deterministic execution evidence",
            )
            self.assertEqual(selection.step_cards[0]["context"]["strategy"], "packed")
            self.assertTrue((root / ".ai-sdlc/cache/context-cache.sqlite3").is_file())

    def test_context_cache_install_below_symlinked_parent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            external = Path(outside) / ".agents"
            installed = external / "skills/ai-sdlc-context-cache"
            installed.parent.mkdir(parents=True)
            shutil.copytree(ROOT / "skills/ai-sdlc-context-cache", installed)
            (root / ".agents").symlink_to(external, target_is_directory=True)
            self.assertIsNone(STEPS._context_cache_root(root))

    def test_run_plan_tasks_are_context_complete_step_card_projections(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            first = STEPS.compile_run_plan(
                root,
                "ai-sdlc-fixture",
                "execute",
                role="software-engineer",
                goal="execute deterministic fixture",
                trace_ids=("FR-007",),
            )
            second = STEPS.compile_run_plan(
                root,
                "ai-sdlc-fixture",
                "execute",
                role="software-engineer",
                goal="execute deterministic fixture",
                trace_ids=("FR-007",),
            )
            self.assertEqual(STEPS.render_toon(first), STEPS.render_toon(second))
            self.assertTrue(first["tasks"])
            for task in first["tasks"]:
                with self.subTest(step=task["step_id"]):
                    self.assertEqual(task["schema"], STEPS.STEP_CARD_SCHEMA)
                    self.assertEqual(
                        task["context"]["schema"],
                        "ai-sdlc-context-pack/v4",
                    )
                    self.assertTrue(task["ready"])
                    self.assertTrue(task["context"]["sufficient"])
                    self.assertEqual(
                        task["graph_fingerprint"],
                        first["graph_fingerprint"],
                    )
                    self.assertEqual(
                        task["idempotency_scope"],
                        (
                            f"{task['skill']}:{task['step_id']}:"
                            f"{first['graph_fingerprint']}"
                        ),
                    )

    def test_run_plan_fails_closed_when_any_step_context_is_insufficient(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = fixture(root)
            manifest_path = skill / "steps/manifest.toon"
            manifest = toon_codec.loads(
                manifest_path.read_text(encoding="utf-8")
            )
            execute = next(
                step for step in manifest["steps"] if step["id"] == "execute"
            )
            execute["context"]["critical_anchors"].append(
                "MUST-PRESERVE-THIS-ANCHOR"
            )
            manifest_path.write_text(
                toon_codec.dumps(manifest),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "STEP_CONTEXT_INSUFFICIENT"):
                STEPS.compile_run_plan(
                    root,
                    "ai-sdlc-fixture",
                    "execute",
                    role="software-engineer",
                )

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
            with self.assertRaisesRegex(ValueError, "missing steps/manifest.toon"):
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
            too_large = (
                "# Execute\n\n## Entry\n\nEnter safely.\n\n## Procedure\n\n"
                + ("bounded evidence " * 500)
                + "\n\n## Exit\n\nReturn evidence.\n"
            )
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

    def test_dependency_cycle_fails_closed(self) -> None:
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
            manifest_path = skill / "steps" / "manifest.toon"
            manifest = toon_codec.loads(manifest_path.read_text(encoding="utf-8"))
            execute = next(
                step for step in manifest["steps"] if step["id"] == "execute"
            )
            execute["depends_on"] = ["also-execute"]
            also_execute = dict(execute)
            also_execute.update(
                {
                    "id": "also-execute",
                    "path": "steps/also-execute.md",
                    "depends_on": ["execute"],
                    "reason": "dependency cycle must fail closed",
                    "outputs": ["also-execute-evidence"],
                }
            )
            manifest["steps"].append(also_execute)
            manifest_path.write_text(toon_codec.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "dependency cycle"):
                STEPS.load_manifest(root, "ai-sdlc-fixture")


if __name__ == "__main__":
    unittest.main()
