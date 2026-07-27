#!/usr/bin/env python3
"""Deterministic tests for portable validation helper scripts."""

from __future__ import annotations

import errno
import importlib.util
import io
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
VALIDATION_PLAN = ROOT / "skills" / "ai-sdlc-validation" / "scripts" / "validation_plan.py"
REVIEW_READINESS = ROOT / "skills" / "ai-sdlc-code-review" / "scripts" / "review_readiness.py"
RUN_VALIDATION = ROOT / "skills" / "ai-sdlc-validation" / "scripts" / "run_validation.py"


def load_module(path: Path, name: str):
    """Load a helper script as a module for direct function assertions."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ValidationPlanTests(unittest.TestCase):
    """Behavior tests for validation command planning."""

    def test_skill_and_spec_changes_get_repo_local_commands(self) -> None:
        """Full flow should suggest skill, compile, and SDD gate commands."""
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATION_PLAN),
                "--full-flow",
                "skills/ai-sdlc-ba/SKILL.md",
                "skills/ai-sdlc-ba/scripts/ba_context_scaffold.py",
                "specs/176-ai-setup-hardening/requirements.md",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Suggested validation commands (full flow):", result.stdout)
        self.assertIn("test -f skills/ai-sdlc-ba/SKILL.md", result.stdout)
        self.assertIn("PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile skills/ai-sdlc-ba/scripts/ba_context_scaffold.py", result.stdout)
        self.assertIn("python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/176-ai-setup-hardening --full-flow", result.stdout)
        self.assertIn("python3 skills/ai-sdlc-sdd/scripts/check_clarify.py specs/176-ai-setup-hardening --full-flow", result.stdout)

    def test_quick_flow_keeps_plan_smaller(self) -> None:
        """Quick flow should keep the suggested SDD command set focused."""
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATION_PLAN),
                "--quick-flow",
                "skills/ai-sdlc-ba/scripts/ba_context_scaffold.py",
                "specs/176-ai-setup-hardening/requirements.md",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Suggested validation commands (quick flow):", result.stdout)
        self.assertIn("python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/176-ai-setup-hardening --quick-flow", result.stdout)
        self.assertNotIn("check_clarify.py", result.stdout)

    def test_canonical_runtime_uses_real_paths_and_runtime_suite(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATION_PLAN),
                "--quick-flow",
                "skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skills/ai-sdlc-shared-runtime/SKILL.md", result.stdout)
        self.assertIn("unittest discover -s skills/ai-sdlc-shared-runtime/tests", result.stdout)
        self.assertIn("skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py", result.stdout)

    def test_deleted_skill_gets_absence_check(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATION_PLAN),
                "--quick-flow",
                "skills/ai-sdlc-removed/SKILL.md",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "test ! -e skills/ai-sdlc-removed/SKILL.md", result.stdout
        )
        self.assertNotIn(
            "test -f skills/ai-sdlc-removed/SKILL.md", result.stdout
        )

    def test_validation_runner_retries_temporary_process_exhaustion(self) -> None:
        module = load_module(RUN_VALIDATION, "run_validation_retry")

        class FakeProcess:
            pid = 2_147_483_647
            stdout = io.BytesIO()
            stderr = io.BytesIO()

            @staticmethod
            def wait(timeout=None):
                return 0

            @staticmethod
            def poll():
                return 0

        attempts = 0

        def popen(*args, **kwargs):
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise OSError(errno.EAGAIN, "temporary process exhaustion")
            return FakeProcess()

        with mock.patch.object(module.subprocess, "Popen", side_effect=popen):
            result = module.execute_bounded(
                ["python3", "check.py"], ROOT, timeout=1, limit=1024
            )

        self.assertEqual(attempts, 3)
        self.assertEqual(result[0], 0)


class ReviewReadinessTests(unittest.TestCase):
    """Behavior tests for code-review helper warnings."""

    def test_skill_warning_uses_repo_local_paths(self) -> None:
        """Skill metadata warnings should reference repo-local skill paths."""
        module = load_module(REVIEW_READINESS, "review_readiness")
        warnings = module.skill_metadata_warnings(["skills/ai-sdlc-ba/SKILL.md"], full_repo=False)
        self.assertTrue(any("inspect skills/ai-sdlc-ba/SKILL.md" in warning for warning in warnings))

    def test_runtime_warning_has_no_impossible_or_wildcard_path(self) -> None:
        module = load_module(REVIEW_READINESS, "review_readiness_shared")
        warnings = module.skill_metadata_warnings(
            ["skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py"], full_repo=False
        )
        joined = "\n".join(warnings)
        self.assertNotIn("scripts/*.py", joined)
        self.assertIn("skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install_record.py", joined)
        self.assertIn("unittest discover -s skills/ai-sdlc-shared-runtime/tests", joined)

    def test_review_readiness_recognizes_skill_deletion(self) -> None:
        module = load_module(REVIEW_READINESS, "review_readiness_deletion")
        warnings = module.skill_metadata_warnings(
            ["skills/ai-sdlc-removed/SKILL.md"], full_repo=False
        )
        self.assertTrue(
            any("skill deletion detected" in warning for warning in warnings)
        )


if __name__ == "__main__":
    unittest.main()
