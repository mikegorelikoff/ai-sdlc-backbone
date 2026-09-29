#!/usr/bin/env python3
"""Tests for skills/ai-sdlc-qa/scripts/qa_plan.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "ai-sdlc-qa" / "scripts" / "qa_plan.py"

_SHARED = ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import decode_toon


class QaPlanTests(unittest.TestCase):
    def test_qa_plan_emits_canonical_toon(self) -> None:
        command = [
            sys.executable,
            str(SCRIPT),
            "--feature",
            "qa-demo",
            "--summary",
            "Verify installation and verification contracts",
            "--acceptance",
            "QA-001|qa-engineer|clean workspace|run qa_plan|toon plan emitted|automated|high",
            "--regression",
            "tests/test_qa.py",
            "--validation",
            "python3 -m unittest",
            "--manual-check",
            "inspect plan structure",
            "--residual-risk",
            "cross-platform paths",
            "--status",
            "ready",
        ]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        artifact = decode_toon(result.stdout)
        self.assertEqual("ai-sdlc-qa-plan/v1", artifact["schema"])
        self.assertEqual("qa-demo", artifact["feature"])
        self.assertEqual("ready", artifact["status"])
        self.assertEqual(1, len(artifact["acceptance"]))
        self.assertEqual("QA-001", artifact["acceptance"][0]["id"])
        self.assertEqual(["tests/test_qa.py"], artifact["regression_targets"])
        self.assertEqual(["python3 -m unittest"], artifact["validation_evidence"])

    def test_qa_plan_file_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            rel_output = Path("tmp_plan.toon")
            command = [
                sys.executable,
                str(SCRIPT),
                "--feature",
                "file-demo",
                "--summary",
                "File write check",
                "--acceptance",
                "QA-002|tester|setup|act|assert|evidence|low",
                "--output",
                str(rel_output),
            ]
            result = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, check=True)
            written = tmp_path / rel_output
            self.assertTrue(written.is_file())
            artifact = decode_toon(written.read_text(encoding="utf-8"))
            self.assertEqual("ai-sdlc-qa-plan/v1", artifact["schema"])
            self.assertEqual("file-demo", artifact["feature"])


if __name__ == "__main__":
    unittest.main()
