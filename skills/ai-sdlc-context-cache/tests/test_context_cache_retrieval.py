#!/usr/bin/env python3
"""Symbol retrieval, disambiguation, and token-economics tests."""

from __future__ import annotations

import importlib.util
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-context-cache/scripts/context_cache.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_context_cache_retrieval", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CACHE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CACHE)
GRAPH = CACHE.CODE_GRAPH


@unittest.skipIf(GRAPH is None, "graph runtime requires Python 3.10+")
class ContextCacheRetrievalTests(unittest.TestCase):
    def repository(self, directory: str, with_skill: bool = False) -> Path:
        root = Path(directory)
        subprocess.run(["git", "init", str(root)], check=True, stdout=subprocess.DEVNULL)
        (root / "src/alpha").mkdir(parents=True)
        (root / "src/beta").mkdir(parents=True)
        (root / "src/alpha/service.py").write_text(
            "def deterministic_target():\n    return 'alpha'\n\ndef caller():\n    return deterministic_target()\n",
            encoding="utf-8",
        )
        (root / "src/beta/service.py").write_text(
            "class Worker:\n    def deterministic_target(self):\n        return 'beta'\n",
            encoding="utf-8",
        )
        (root / "src/large.py").write_text(
            "def economy_anchor():\n    return 1\n\n" +
            "# economy anchor bounded graph evidence\n" * 900,
            encoding="utf-8",
        )
        if with_skill:
            destination = root / "skills/ai-sdlc-scheduler"
            destination.mkdir(parents=True)
            shutil.copy2(
                ROOT / "skills/ai-sdlc-scheduler/SKILL.md",
                destination / "SKILL.md",
            )
            shutil.copytree(
                ROOT / "skills/ai-sdlc-scheduler/steps",
                destination / "steps",
            )
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        return root

    def test_tc_015_golden_recall_and_rank(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            first = CACHE.query(
                root, cache, "deterministic target", 10, 2, 64,
                require_graph=True,
            )
            second = CACHE.query(
                root, cache, "deterministic target", 10, 2, 64,
                require_graph=True,
            )
            paths = {row["path"] for row in first["results"]}
            self.assertEqual(
                paths & {"src/alpha/service.py", "src/beta/service.py"},
                {"src/alpha/service.py", "src/beta/service.py"},
            )
            self.assertEqual(CACHE.canonical(first), CACHE.canonical(second))

    def test_tc_016_qualified_symbols_disambiguate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            connection = sqlite3.connect(cache)
            try:
                rows = connection.execute(
                    "SELECT id, qualified_name, path FROM symbols "
                    "WHERE name='deterministic_target' ORDER BY path, qualified_name"
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(len(rows), 2)
            self.assertEqual(len({row[0] for row in rows}), 2)
            self.assertEqual(
                {(row[1], row[2]) for row in rows},
                {
                    ("deterministic_target", "src/alpha/service.py"),
                    ("Worker.deterministic_target", "src/beta/service.py"),
                },
            )

    def test_tc_017_accepts_only_economical_complete_pack(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory, with_skill=True)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            packed = CACHE.pack(
                root, cache, "economy anchor bounded graph evidence",
                "ai-sdlc-scheduler", "context", 4000, 24, 2, 128,
                min_savings_percent=25.0, require_graph=True,
            )
            self.assertEqual(packed["strategy"], "packed", packed["reason"])
            self.assertEqual(packed["critical_recall_percent"], 100.0)
            self.assertGreaterEqual(packed["savings_percent"], 25.0)

    def test_tc_018_rejects_incomplete_or_uneconomical_pack(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory, with_skill=True)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            rejected = CACHE.pack(
                root, cache, "deterministic target", "ai-sdlc-scheduler",
                "context", 4000, 4, 1, 32,
                min_savings_percent=100.0, require_graph=True,
            )
            self.assertEqual(rejected["strategy"], "direct_read")
            self.assertIn("below 100.00%", rejected["reason"])


if __name__ == "__main__":
    unittest.main()
