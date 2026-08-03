#!/usr/bin/env python3
"""Storage, bounds, incremental, and safety tests for the AST graph."""

from __future__ import annotations

import importlib.util
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-context-cache/scripts/context_cache.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_context_cache_graph_cases", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CACHE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CACHE)
GRAPH = CACHE.CODE_GRAPH


@unittest.skipIf(GRAPH is None, "graph runtime requires Python 3.10+")
class ContextCacheGraphTests(unittest.TestCase):
    def repository(self, directory: str) -> Path:
        root = Path(directory)
        subprocess.run(["git", "init", str(root)], check=True, stdout=subprocess.DEVNULL)
        (root / "src").mkdir()
        (root / "src/a.py").write_text(
            "# AC-101\ndef stable_symbol():\n    return helper()\ndef helper():\n    return 1\n",
            encoding="utf-8",
        )
        (root / "src/b.py").write_text(
            "# AC-101\nfrom a import stable_symbol\ndef consumer():\n    return stable_symbol()\n",
            encoding="utf-8",
        )
        (root / "notes.md").write_text("AC-101 graph evidence\n" * 10, encoding="utf-8")
        (root / "private-token.txt").write_text("DO_NOT_INDEX_SENTINEL", encoding="utf-8")
        (root / "image.bin").write_bytes(b"\x00DO_NOT_INDEX_SENTINEL")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        return root

    def test_tc_003_and_004_corpus_accounting_reconciles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            receipt = CACHE.build(root, cache, rebuild=True, require_graph=True)
            connection = sqlite3.connect(cache)
            try:
                documents = int(connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0])
                exclusions = int(connection.execute("SELECT COUNT(*) FROM graph_exclusions").fetchone()[0])
                candidates = receipt["counts"]["total_candidates"]
                self.assertEqual(documents + exclusions, candidates)
                self.assertEqual(
                    connection.execute("SELECT COUNT(DISTINCT path) FROM documents").fetchone()[0],
                    documents,
                )
            finally:
                connection.close()

    def test_tc_010_v1_state_is_never_mutated_in_place(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            cache.parent.mkdir(parents=True)
            connection = sqlite3.connect(cache)
            connection.execute("CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            connection.execute("INSERT INTO metadata VALUES('schema', 'ai-sdlc-context-cache/v1')")
            connection.commit()
            connection.close()
            before = cache.read_bytes()
            with self.assertRaisesRegex(CACHE.CacheError, "incompatible"):
                CACHE.build(root, cache)
            self.assertEqual(cache.read_bytes(), before)
            rebuilt = CACHE.build(root, cache, rebuild=True, require_graph=True)
            self.assertTrue(rebuilt["fresh"])

    def test_tc_011_trace_hubs_replace_pairwise_cliques(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            connection = sqlite3.connect(cache)
            try:
                members = int(connection.execute(
                    "SELECT COUNT(*) FROM graph_edges WHERE kind='spec-trace' AND label='AC-101'"
                ).fetchone()[0])
                hubs = int(connection.execute(
                    "SELECT COUNT(*) FROM graph_nodes WHERE kind='trace-hub' AND label='AC-101'"
                ).fetchone()[0])
                legacy = int(connection.execute(
                    "SELECT COUNT(*) FROM edges WHERE kind='trace-id' AND label='AC-101'"
                ).fetchone()[0])
                self.assertEqual(hubs, 1)
                self.assertGreater(members, 1)
                self.assertLessEqual(legacy, members * 2)
                self.assertLess(legacy, members * (members - 1))
            finally:
                connection.close()

    def test_tc_012_bound_breach_rejects_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            previous = GRAPH.MAX_TOTAL_EDGES
            GRAPH.MAX_TOTAL_EDGES = 1
            try:
                with self.assertRaisesRegex(GRAPH.GraphError, "graph-edge-bound-exceeded"):
                    CACHE.build(root, cache, rebuild=True, require_graph=True)
            finally:
                GRAPH.MAX_TOTAL_EDGES = previous
            self.assertFalse(cache.exists())

    def test_tc_013_incremental_refresh_removes_stale_facts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            connection = sqlite3.connect(cache)
            before = connection.execute(
                "SELECT id FROM symbols WHERE path='src/a.py' AND name='stable_symbol'"
            ).fetchone()[0]
            untouched = connection.execute(
                "SELECT id FROM symbols WHERE path='src/b.py' AND name='consumer'"
            ).fetchone()[0]
            connection.close()
            (root / "src/a.py").write_text(
                "def stable_symbol():\n    return 2\ndef replacement():\n    return 3\n",
                encoding="utf-8",
            )
            CACHE.build(root, cache, require_graph=True)
            connection = sqlite3.connect(cache)
            try:
                self.assertEqual(connection.execute(
                    "SELECT id FROM symbols WHERE path='src/a.py' AND name='stable_symbol'"
                ).fetchone()[0], before)
                self.assertEqual(connection.execute(
                    "SELECT id FROM symbols WHERE path='src/b.py' AND name='consumer'"
                ).fetchone()[0], untouched)
                self.assertEqual(connection.execute(
                    "SELECT COUNT(*) FROM symbols WHERE path='src/a.py' AND name='helper'"
                ).fetchone()[0], 0)
            finally:
                connection.close()

    def test_tc_019_and_020_graph_stats_are_stable_and_strict_query_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            first = CACHE.graph_stats(root, cache)
            second = CACHE.graph_stats(root, cache)
            self.assertEqual(CACHE.canonical(first), CACHE.canonical(second))
            self.assertTrue(first["graph_complete"])
            connection = sqlite3.connect(cache)
            connection.execute("UPDATE metadata SET value='false' WHERE key='graph_complete'")
            connection.commit()
            connection.close()
            fallback = CACHE.query(root, cache, "stable symbol", 10, 2, 64, require_graph=True)
            self.assertEqual(fallback["strategy"], "direct_read")
            self.assertEqual(fallback["reason"], "graph-incomplete")

    def test_tc_024_unsafe_inputs_are_excluded_without_content_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache, rebuild=True, require_graph=True)
            rendered = CACHE.canonical(CACHE.graph_stats(root, cache))
            connection = sqlite3.connect(cache)
            try:
                reasons = dict(connection.execute(
                    "SELECT path, reason FROM graph_exclusions ORDER BY path"
                ))
                self.assertEqual(reasons["private-token.txt"], "secret-like-path")
                dump = " ".join(
                    str(value)
                    for table in ("documents", "chunks", "graph_exclusions")
                    for row in connection.execute(f"SELECT * FROM {table}")
                    for value in row
                )
            finally:
                connection.close()
            self.assertNotIn("DO_NOT_INDEX_SENTINEL", rendered)
            self.assertNotIn("DO_NOT_INDEX_SENTINEL", dump)


if __name__ == "__main__":
    unittest.main()
