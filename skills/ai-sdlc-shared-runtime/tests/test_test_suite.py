#!/usr/bin/env python3
"""Tests for complete skill test-file discovery and execution."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ai_sdlc_test_suite as suite  # noqa: E402
from ai_sdlc_toon import encode_toon  # noqa: E402


def write_test(root: Path, skill: str, name: str, exit_code: int) -> Path:
    path = root / f"skills/{skill}/tests/test_{name}.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"raise SystemExit({exit_code})\n", encoding="utf-8")
    return path


class TestSuiteTests(unittest.TestCase):
    def test_discovery_and_success_receipt_are_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_test(root, "ai-sdlc-a", "second", 0)
            write_test(root, "ai-sdlc-a", "first", 0)
            paths = suite.discover(root)
            self.assertEqual(
                [path.name for path in paths],
                ["test_first.py", "test_second.py"],
            )
            first = suite.run_suite(root, paths, 10)
            second = suite.run_suite(root, paths, 10)
            self.assertEqual(encode_toon(first), encode_toon(second))
            self.assertEqual(first["test_files"], 2)
            self.assertEqual(first["failed"], 0)
            self.assertEqual(first["result"], "passed")

    def test_failure_is_explicit_and_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_test(root, "ai-sdlc-a", "failed", 7)
            result = suite.run_suite(root, suite.discover(root), 10)
            self.assertEqual(result["failed"], 1)
            self.assertEqual(result["result"], "failed")
            self.assertEqual(result["items"][0]["exit_code"], 7)

    def test_empty_and_symlinked_inventories_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "skills").mkdir()
            with self.assertRaisesRegex(ValueError, "TEST_SUITE_EMPTY"):
                suite.discover(root)
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            (root / "skills").mkdir()
            external = Path(outside) / "test_external.py"
            external.write_text("raise SystemExit(0)\n", encoding="utf-8")
            linked = root / "skills/ai-sdlc-a/tests/test_linked.py"
            linked.parent.mkdir(parents=True)
            linked.symlink_to(external)
            with self.assertRaisesRegex(ValueError, "TEST_SUITE_UNSAFE_PATH"):
                suite.discover(root)


if __name__ == "__main__":
    unittest.main()
