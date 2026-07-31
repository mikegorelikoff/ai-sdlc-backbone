#!/usr/bin/env python3
"""Tests for release compatibility and roadmap commit auditing."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
import sys
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"))
SCRIPT = ROOT / "skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py"
BASELINE = ROOT / "compatibility/baseline-v1.toon"


class CompatibilityTests(unittest.TestCase):
    """Baseline, breaking fixture, and Git audit tests."""

    def run_check(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run compatibility validation with captured output."""
        return subprocess.run(["python3", str(SCRIPT), "--root", str(ROOT), *args], cwd=ROOT, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def git_executable_args(self) -> tuple[str, str]:
        """Return the reviewed absolute Git path required by history audits."""
        path = shutil.which("git")
        self.assertIsNotNone(path)
        return "--git-executable", str(Path(path or "").resolve())

    def test_current_release_matches_baseline(self) -> None:
        """The default complete TOON result should expose protected contracts."""
        result = self.run_check("--skip-git-audit")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("result: compatible", result.stdout)
        self.assertIn("protected_skill_names", result.stdout)
        self.assertIn("protected_cli_flags", result.stdout)
        self.assertIn("protected_routes", result.stdout)
        self.assertIn("machine_extension: .toon", result.stdout)
        self.assertIn("skill_graph_schema: ai-sdlc-skill-steps/v2", result.stdout)
        self.assertIn("contracts: 12", result.stdout)
        expected = len(list((ROOT / "skills").glob("*/SKILL.md")))
        self.assertIn(f"skills: {expected}", result.stdout)

    def test_changed_protected_contract_identity_breaks_baseline(self) -> None:
        """A protected machine contract cannot drift behind the baseline."""
        with tempfile.TemporaryDirectory() as temp:
            baseline = toon_codec.loads(BASELINE.read_text(encoding="utf-8"))
            baseline["contracts"][0]["id"] = "ai-sdlc-skill-steps/v999"
            path = Path(temp) / "baseline.toon"
            path.write_text(toon_codec.dumps(baseline), encoding="utf-8")
            result = self.run_check(
                "--baseline",
                str(path),
                "--skip-git-audit",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("protected contract identity changed", result.stdout)

    def test_semantic_node_floor_is_enforced(self) -> None:
        """Compatibility rejects shallow skill graphs even when names remain."""
        with tempfile.TemporaryDirectory() as temp:
            baseline = toon_codec.loads(BASELINE.read_text(encoding="utf-8"))
            baseline["skill_graph"]["min_nodes"] = 7
            path = Path(temp) / "baseline.toon"
            path.write_text(toon_codec.dumps(baseline), encoding="utf-8")
            result = self.run_check(
                "--baseline",
                str(path),
                "--skip-git-audit",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("has fewer than 7 semantic nodes", result.stdout)

    def test_missing_skill_breaks_baseline(self) -> None:
        """A required skill rename or removal must fail mechanically."""
        with tempfile.TemporaryDirectory() as temp:
            baseline = toon_codec.loads(BASELINE.read_text(encoding="utf-8"))
            baseline["required_skill_names"].append("ai-sdlc-removed")
            baseline["required_skill_names"].sort()
            path = Path(temp) / "baseline.toon"
            path.write_text(toon_codec.dumps(baseline), encoding="utf-8")
            result = self.run_check("--baseline", str(path), "--skip-git-audit")
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing required skills: ai-sdlc-removed", result.stdout)

    def test_new_required_flag_breaks_baseline(self) -> None:
        """A declared CLI contract must exist on every skill CLI."""
        with tempfile.TemporaryDirectory() as temp:
            baseline = toon_codec.loads(BASELINE.read_text(encoding="utf-8"))
            baseline["required_cli_flags"].append("--future-required-flag")
            path = Path(temp) / "baseline.toon"
            path.write_text(toon_codec.dumps(baseline), encoding="utf-8")
            result = self.run_check("--baseline", str(path), "--skip-git-audit")
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing stable flag --future-required-flag", result.stdout)

    def test_target_python_is_inspected_but_never_executed(self) -> None:
        """An attacker-controlled target script cannot run during compatibility."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "skills" / "ai-sdlc-probe"
            shared = root / "skills" / "ai-sdlc-shared-runtime"
            mirror = root / "skills" / "ai-sdlc-shared-runtime" / "scripts"
            for path in (skill / "scripts", shared, mirror, root / "modules"):
                path.mkdir(parents=True, exist_ok=True)
            (skill / "steps").mkdir(parents=True)
            node_specs = (
                (
                    "preflight",
                    "analysis",
                    [],
                    ["prepare"],
                    "inspect-and-route",
                    ["filesystem.read"],
                    "none",
                    ["authority"],
                    ["routing-evidence"],
                    "none",
                    "block",
                ),
                (
                    "context",
                    "context",
                    ["preflight"],
                    ["clarify", "route"],
                    "compile-context",
                    ["filesystem.read"],
                    "none",
                    ["context-sufficiency"],
                    ["context-pack"],
                    "none",
                    "block",
                ),
                (
                    "execute",
                    "action",
                    ["context"],
                    ["execute"],
                    "execute-procedure",
                    ["filesystem.read", "filesystem.write"],
                    "workspace-write",
                    ["authorization"],
                    ["procedure-result"],
                    "after-step",
                    "block",
                ),
                (
                    "validate",
                    "validation",
                    ["execute"],
                    ["validate"],
                    "validate-evidence",
                    ["filesystem.read"],
                    "none",
                    ["acceptance"],
                    ["validation-result"],
                    "none",
                    "block",
                ),
                (
                    "handoff",
                    "handoff",
                    ["validate"],
                    ["handoff", "complete"],
                    "handoff-result",
                    ["filesystem.read"],
                    "none",
                    ["terminal-evidence"],
                    ["handoff"],
                    "none",
                    "handoff",
                ),
            )
            links: list[str] = []
            nodes: list[dict[str, object]] = []
            context_contract = {
                "required": True,
                "budget_tokens": 12000,
                "mandatory": ["step_document"],
                "selectors": [
                    "step",
                    "repository-instructions",
                    "feature-traces",
                    "changed-path-topology",
                ],
                "critical_anchors": ["## Entry", "## Procedure", "## Exit"],
                "min_savings_percent": 15,
                "fallback": "direct_read",
            }
            for (
                node_id,
                node_type,
                dependencies,
                phases,
                operation,
                capabilities,
                side_effect,
                gates,
                outputs,
                commit_boundary,
                on_failure,
            ) in node_specs:
                relative = f"steps/{node_id}.md"
                links.append(f"[`{relative}`]({relative})")
                (skill / relative).write_text(
                    f"# {node_id.title()}\n\n## Entry\n\nEnter.\n\n"
                    "## Procedure\n\nProbe.\n\n## Exit\n\nStop.\n",
                    encoding="utf-8",
                )
                nodes.append(
                    {
                        "id": node_id,
                        "path": relative,
                        "type": node_type,
                        "depends_on": dependencies,
                        "condition": {
                            "phases": phases,
                            "roles": [],
                            "actions": [],
                        },
                        "load": (
                            "required"
                            if node_id in {"preflight", "context"}
                            else "before-completion"
                            if node_id in {"validate", "handoff"}
                            else "on-demand"
                        ),
                        "max_tokens": 256,
                        "reason": f"execute deterministic {node_id} compatibility probe",
                        "operation": operation,
                        "capabilities": capabilities,
                        "side_effect": side_effect,
                        "context": context_contract,
                        "gates": gates,
                        "outputs": outputs,
                        "max_attempts": 1,
                        "commit_boundary": commit_boundary,
                        "on_failure": on_failure,
                    }
                )
            (skill / "SKILL.md").write_text(
                "---\nname: ai-sdlc-probe\ndescription: Probe.\n---\n\n"
                + "\n".join(links)
                + "\n",
                encoding="utf-8",
            )
            (skill / "steps" / "manifest.toon").write_text(
                toon_codec.dumps(
                    {
                        "schema": "ai-sdlc-skill-steps/v2",
                        "skill": "ai-sdlc-probe",
                        "version": "4.0.0",
                        "entrypoints": {
                            "prepare": ["preflight"],
                            "clarify": ["context"],
                            "route": ["context"],
                            "execute": ["execute"],
                            "validate": ["validate"],
                            "handoff": ["handoff"],
                            "complete": ["handoff"],
                        },
                        "budgets": {
                            "step_max_tokens": 5000,
                            "context_max_tokens": 12000,
                            "min_context_savings_percent": 15,
                        },
                        "steps": nodes,
                    }
                ),
                encoding="utf-8",
            )
            marker = root / "EXECUTED"
            (skill / "scripts" / "probe.py").write_text(
                "from pathlib import Path\n"
                f"Path({str(marker)!r}).write_text('unsafe')\n"
                "from argparse import ArgumentParser\n"
                "p = ArgumentParser()\n"
                "p.add_argument('--quick-flow')\n"
                "p.add_argument('--full-flow')\n"
                "p.add_argument('--state-check')\n"
                "p.add_argument('--begin-state')\n"
                "p.add_argument('--complete-state')\n",
                encoding="utf-8",
            )
            config = root / "config.toon"
            config.write_text(
                toon_codec.dumps({"schema": "fixture/v1"}),
                encoding="utf-8",
            )
            for path in (
                root / "README.md",
                root / "docs/reference/artifact-routing.md",
                root / "docs/how-to/install.md",
                root / "docs/how-to/update.md",
                root / "guide.md",
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "install.sh harness-install-lock.toon compatibility update rollback\n",
                    encoding="utf-8",
                )
            baseline = {
                "schema": "ai-sdlc-compatibility-baseline/v1",
                "release": "fixture",
                "harness_api_version": "1.0.0",
                "required_skill_names": ["ai-sdlc-probe"],
                "required_cli_flags": ["--quick-flow", "--full-flow", "--state-check", "--begin-state", "--complete-state"],
                "skill_doc_contract": [],
                "routes": {},
                "config": {"schema": "fixture/v1", "defaults": "config.toon"},
                "modules": {"schema": "ai-sdlc-module/v1", "ids": []},
                "install_update_guide": "guide.md",
            }
            baseline_path = root / "baseline.toon"
            baseline_path.write_text(toon_codec.dumps(baseline), encoding="utf-8")
            result = subprocess.run(
                ["python3", str(SCRIPT), "--root", str(root), "--baseline", str(baseline_path), "--skip-git-audit"],
                cwd=ROOT,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONPYCACHEPREFIX": "/tmp/ai-sdlc-pyc"},
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(marker.exists(), "compatibility validator executed target-root Python")

    def test_git_audit_requires_an_explicit_executable(self) -> None:
        """History validation cannot silently select Git through PATH."""
        result = self.run_check("--format", "toon")
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires --git-executable", result.stdout)

    def test_git_audit_rejects_an_executable_inside_target_root(self) -> None:
        """The inspected repository cannot supply the Git binary used on it."""
        result = self.run_check("--git-executable", str(SCRIPT), "--format", "toon")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not be inside the inspected target root", result.stdout)

    def test_roadmap_audit_allows_completed_roadmap_and_maintenance(self) -> None:
        """The roadmap sequence may omit only its not-yet-created release commit."""
        result = self.run_check("--allow-pending-last", "--format", "toon", *self.git_executable_args())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_roadmap_audit_allows_post_release_maintenance_only_after_sequence(self) -> None:
        """Later maintenance is valid but cannot replace or interrupt the sequence."""
        import importlib.util

        spec = importlib.util.spec_from_file_location("compatibility_audit", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        self.assertTrue(module.audit_subjects(["one", "two"], ["one", "two"]))
        self.assertTrue(module.audit_subjects(["one", "two", "maintenance"], ["one", "two"]))
        self.assertFalse(module.audit_subjects(["one", "maintenance", "two"], ["one", "two"]))
        self.assertFalse(module.audit_subjects(["one", "one", "two"], ["one", "two"]))
        self.assertTrue(module.audit_subjects(["one"], ["one", "two"], allow_pending_last=True))
        self.assertFalse(module.audit_subjects(["prefix", "one"], ["one"], allow_pending_last=True))


if __name__ == "__main__":
    unittest.main()
