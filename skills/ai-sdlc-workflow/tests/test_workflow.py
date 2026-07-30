#!/usr/bin/env python3
"""Tests for v2 workflow-to-runtime compilation."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-workflow/scripts/workflow.py"
RUNTIME = ROOT / "skills/ai-sdlc-runtime/scripts/runtime.py"


class WorkflowTests(unittest.TestCase):
    def node(
        self,
        node_id: str,
        dependencies: list[str],
        skill: str,
        entrypoint: str,
        *,
        condition: object = None,
        approval_owner: str = "",
    ) -> dict[str, object]:
        return {
            "id": node_id,
            "depends_on": dependencies,
            "skill": skill,
            "entrypoint": entrypoint,
            "role": "",
            "action": "",
            "condition": condition,
            "approval_owner": approval_owner,
        }

    def value(self) -> dict[str, object]:
        return {
            "schema": "ai-sdlc-workflow/v2",
            "id": "assure-feature",
            "version": "2.0.0",
            "nodes": [
                self.node("sdd", [], "ai-sdlc-sdd", "execute"),
                self.node(
                    "qa",
                    ["sdd"],
                    "ai-sdlc-qa",
                    "validate",
                    approval_owner="QA Lead",
                ),
            ],
        }

    def cli(
        self,
        repository: Path,
        value: dict[str, object],
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        path = repository / "workflow.toon"
        path.write_text(toon_codec.encode_toon(value), encoding="utf-8")
        return subprocess.run(
            [
                "python3",
                str(SCRIPT),
                str(repository),
                "--workflow",
                str(path),
                *args,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_compiles_skill_graphs_to_runtime_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            result = self.cli(
                Path(temp),
                self.value(),
                "--plan",
                "--approved-node",
                "qa",
                "--write",
                "--format",
                "toon",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            plan = toon_codec.loads(result.stdout)
            self.assertEqual(plan["schema"], "ai-sdlc-workflow-plan/v2")
            self.assertEqual(
                plan["run_plan"]["schema"],
                "ai-sdlc-run-plan/v2",
            )
            task_ids = [task["id"] for task in plan["run_plan"]["tasks"]]
            self.assertTrue(all(task_id.startswith(("sdd/", "qa/")) for task_id in task_ids))
            qa_roots = [
                task
                for task in plan["run_plan"]["tasks"]
                if task["id"].startswith("qa/")
                and all(not dependency.startswith("qa/") for dependency in task["depends_on"])
            ]
            self.assertTrue(qa_roots)
            self.assertTrue(
                all(
                    any(dependency.startswith("sdd/") for dependency in task["depends_on"])
                    for task in qa_roots
                )
            )
            output_root = Path(temp) / "_ai_sdlc/workflows/assure-feature"
            self.assertTrue((output_root / "workflow-plan.toon").is_file())
            self.assertTrue((output_root / "run-plan.toon").is_file())
            started = subprocess.run(
                [
                    "python3",
                    str(RUNTIME),
                    str(Path(temp)),
                    "--start",
                    "--run-id",
                    "workflow-run",
                    "--plan",
                    str(output_root / "run-plan.toon"),
                    "--format",
                    "toon",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(
                started.returncode,
                0,
                started.stdout + started.stderr,
            )

    def test_missing_approval_blocks_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            result = self.cli(repository, self.value(), "--plan", "--write")
            self.assertEqual(result.returncode, 1)
            self.assertIn("non-executable", result.stdout)
            self.assertFalse((repository / "_ai_sdlc").exists())

    def test_conditions_defer_and_skip_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            value = self.value()
            value["nodes"][0]["condition"] = {
                "field": "release.enabled",
                "operator": "eq",
                "value": True,
            }
            deferred = self.cli(repository, value, "--plan")
            self.assertEqual(deferred.returncode, 2)
            self.assertFalse(toon_codec.loads(deferred.stdout)["executable"])
            context = repository / "context.toon"
            context.write_text(
                toon_codec.encode_toon({"release": {"enabled": False}}),
                encoding="utf-8",
            )
            skipped = self.cli(
                repository,
                value,
                "--plan",
                "--context",
                str(context),
                "--approved-node",
                "qa",
            )
            self.assertEqual(skipped.returncode, 0)
            decision = toon_codec.loads(skipped.stdout)["node_decisions"][0]
            self.assertEqual(decision["status"], "skipped")

    def test_cycle_and_legacy_schema_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            cyclic = self.value()
            cyclic["nodes"][0]["depends_on"] = ["qa"]
            result = self.cli(repository, cyclic, "--validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("dependency cycle", result.stdout)
            legacy = self.value()
            legacy["schema"] = "ai-sdlc-workflow/legacy"
            result = self.cli(repository, legacy, "--validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("WORKFLOW_SCHEMA_MISMATCH", result.stdout)


if __name__ == "__main__":
    unittest.main()
