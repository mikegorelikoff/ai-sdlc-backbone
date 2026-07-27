"""Forward tests for the installable AI SDLC shared runtime."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"
RUNTIME = SKILLS / "ai-sdlc-shared-runtime" / "scripts"
INSTALL_SMOKE = SKILLS / "ai-sdlc-shared-runtime" / "tests" / "install_smoke.py"


class InstalledRuntimeTests(unittest.TestCase):
    """Prove scripts work after skill-only installation, without source shared."""

    def test_runtime_is_canonical_and_self_contained(self) -> None:
        helpers = sorted(RUNTIME.glob("*.py"))
        self.assertGreaterEqual(len(helpers), 21)
        self.assertTrue((RUNTIME / "ai_sdlc_flow.py").is_file())
        self.assertFalse((SKILLS / "_shared").exists())

    def test_sdd_scaffold_runs_from_skill_only_installation(self) -> None:
        result = subprocess.run(
            [sys.executable, str(INSTALL_SMOKE), "--mode", "emulated"],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("installed runtime, complete SDD gates, and commit readiness passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
