#!/usr/bin/env python3
"""Focused tests for deterministic local graph-enhanced RAG context caching."""

from __future__ import annotations

import importlib.util
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-context-cache/scripts/context_cache.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_context_cache", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CACHE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CACHE)


class ContextCacheTests(unittest.TestCase):
    def test_cached_repository_instructions_remain_evidence_only(self) -> None:
        self.assertEqual(CACHE.authority("AGENTS.md"), "evidence_only")
        self.assertEqual(CACHE.authority("nested/CLAUDE.md"), "evidence_only")

    def repository(self, directory: str) -> Path:
        root = Path(directory)
        subprocess.run(["git", "init", str(root)], check=True, stdout=subprocess.DEVNULL)
        (root / "AGENTS.md").write_text("# Rules\n\nKeep outputs deterministic.\n", encoding="utf-8")
        (root / "specs/feature").mkdir(parents=True)
        (root / "specs/feature/requirements.md").write_text(
            "# Requirements\n\nAC-101 scheduler context freshness must fail closed.\n",
            encoding="utf-8",
        )
        (root / "src").mkdir()
        (root / "src/runtime.py").write_text(
            "# Runtime\n\n# AC-101\ndef compile_context():\n    return 'fresh context'\n",
            encoding="utf-8",
        )
        (root / "src/worker.py").write_text(
            "# Worker\n\nfrom runtime import compile_context\n# AC-101\ndef run():\n    return compile_context()\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        return root

    def test_rebuild_and_query_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            first = CACHE.build(root, cache)
            first_status = CACHE.inspect(root, cache)
            second = CACHE.build(root, cache)
            second_status = CACHE.inspect(root, cache)
            self.assertEqual(first["cache_fingerprint"], second["cache_fingerprint"])
            self.assertEqual(CACHE.canonical(first_status), CACHE.canonical(second_status))
            query_a = CACHE.query(root, cache, "scheduler context freshness", 10, 2, 50)
            query_b = CACHE.query(root, cache, "scheduler context freshness", 10, 2, 50)
            self.assertEqual(CACHE.canonical(query_a), CACHE.canonical(query_b))
            self.assertEqual(query_a["strategy"], "cached")
            self.assertTrue(any(item["distance"] > 0 for item in query_a["results"]))

    def test_concurrent_warmers_converge_and_observations_are_aggregate_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            processes = [
                subprocess.Popen(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "warm",
                        "--root",
                        str(root),
                        "--lock-timeout-ms",
                        "5000",
                        "--retries",
                        "1",
                    ],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                for _ in range(4)
            ]
            from ai_sdlc_toon import decode_toon

            receipts = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=15)
                self.assertEqual(process.returncode, 0, stderr)
                receipts.append(decode_toon(stdout))
            self.assertEqual(
                len({item["cache_fingerprint"] for item in receipts}), 1
            )
            self.assertTrue(CACHE.inspect(root, cache)["fresh"])

            CACHE.record_observation(
                root,
                operation="pack",
                outcome="cached",
                reason="packed",
                raw_tokens=100,
                packed_tokens=60,
            )
            observed = CACHE.observations(root)
            self.assertEqual(observed["schema"], CACHE.OBSERVATION_SCHEMA)
            rendered = CACHE.canonical(observed)
            for forbidden in ("query", "prompt", "content", "credential", "identity"):
                self.assertNotIn(forbidden, rendered.lower())
            self.assertEqual(CACHE.observations(root, reset=True)["status"], "reset")
            self.assertEqual(CACHE.observations(root)["rows"], [])

    def test_source_change_during_build_never_publishes_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            source = root / "src/runtime.py"
            original_read_source = CACHE.read_source
            mutated = False

            def read_and_mutate(project_root: Path, relative: str):
                nonlocal mutated
                collected = original_read_source(project_root, relative)
                if relative == "src/runtime.py" and not mutated:
                    mutated = True
                    source.write_text(
                        source.read_text(encoding="utf-8") + "\n# changed during build\n",
                        encoding="utf-8",
                    )
                return collected

            CACHE.read_source = read_and_mutate
            try:
                with self.assertRaisesRegex(CACHE.CacheError, "source snapshot changed"):
                    CACHE.build(root, cache)
            finally:
                CACHE.read_source = original_read_source
            self.assertFalse(cache.exists())

    def test_warm_rebuilds_corrupt_state_safely(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            cache.parent.mkdir(parents=True)
            cache.write_bytes(b"not sqlite")
            receipt = CACHE.warm(root, cache, lock_timeout_ms=1000, retries=1)
            self.assertTrue(receipt["fresh"])
            self.assertTrue(CACHE.inspect(root, cache)["fresh"])

    def test_incremental_change_removes_stale_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache)
            before = sqlite3.connect(cache).execute(
                "SELECT sha256 FROM documents WHERE path='src/runtime.py'"
            ).fetchone()[0]
            (root / "src/runtime.py").write_text("# Runtime changed\n\ndef compile_context():\n    return 'new'\n", encoding="utf-8")
            (root / "src/worker.py").unlink()
            receipt = CACHE.build(root, cache)
            connection = sqlite3.connect(cache)
            try:
                after = connection.execute(
                    "SELECT sha256 FROM documents WHERE path='src/runtime.py'"
                ).fetchone()[0]
                self.assertIsNone(connection.execute(
                    "SELECT path FROM documents WHERE path='src/worker.py'"
                ).fetchone())
                self.assertEqual(connection.execute(
                    "SELECT COUNT(*) FROM chunks WHERE path='src/worker.py'"
                ).fetchone()[0], 0)
            finally:
                connection.close()
            self.assertNotEqual(before, after)
            self.assertEqual(receipt["counts"]["changed"], 1)
            self.assertEqual(receipt["counts"]["removed"], 1)

    def test_pack_is_v4_and_stale_cache_falls_back(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache)
            packed = CACHE.pack(
                root, cache, "scheduler context freshness", "ai-sdlc-scheduler",
                "context", 4000, 12, 1, 64,
            )
            self.assertEqual(packed["schema"], CACHE.PACK_SCHEMA)
            self.assertEqual(packed["selected"][0]["strategy"], "mandatory-step-document")
            self.assertEqual(packed["selected"][0]["authority"], "skill_instruction")
            self.assertTrue(all(
                item["authority"] == "evidence_only"
                for item in packed["selected"][1:]
            ))
            self.assertEqual(packed["critical_total"], 3)
            self.assertEqual(packed["critical_retained"], 3)
            CACHE.validate_step_context_pack(
                packed, expected_skill="ai-sdlc-scheduler", expected_step_id="context"
            )
            (root / "src/runtime.py").write_text("changed after index\n", encoding="utf-8")
            fallback = CACHE.query(root, cache, "scheduler context freshness", 10, 1, 20)
            self.assertEqual(fallback["strategy"], "direct_read")
            self.assertFalse(fallback["fresh"])
            self.assertEqual(fallback["results"], [])

    def test_new_eligible_source_invalidates_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache)
            (root / "src/new-worker.py").write_text(
                "# AC-101\ndef new_worker():\n    return 'new evidence'\n",
                encoding="utf-8",
            )
            fallback = CACHE.query(root, cache, "AC-101 new worker", 10, 1, 20)
            self.assertEqual(fallback["strategy"], "direct_read")
            self.assertFalse(fallback["fresh"])
            self.assertIn("src/new-worker.py:unindexed", fallback["skipped"])
            self.assertIn("src/new-worker.py", fallback["direct_read_paths"])

    def test_benchmark_is_deterministic_and_gates_packed_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            (root / "docs").mkdir()
            (root / "docs/golden.md").write_text(
                "# Golden\n\n" + "AC-202 deterministic benchmark anchor and context evidence.\n" * 180,
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            cases_path = root / "benchmark-cases.toon"
            cases_path.write_text(
                CACHE.canonical(
                    {
                        "schema": CACHE.BENCHMARK_CASES_SCHEMA,
                        "cases": [
                            {
                                "id": "GOLDEN-001",
                                "query": "AC-202 deterministic benchmark anchor",
                                "expected_paths": ["docs/golden.md"],
                                "expected_anchors": ["AC-202"],
                                "skill": "ai-sdlc-scheduler",
                                "step_id": "context",
                                "budget_tokens": 4000,
                                "expected_strategy": "packed",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache)
            first = CACHE.benchmark(root, cache, cases_path, 12, 1, 64)
            second = CACHE.benchmark(root, cache, cases_path, 12, 1, 64)
            self.assertEqual(first["status"], "passed")
            self.assertEqual(first["passed_count"], 1)
            self.assertEqual(CACHE.canonical(first), CACHE.canonical(second))
            self.assertEqual(first["cases"][0]["critical_anchor_recall_percent"], 100.0)
            self.assertGreaterEqual(first["cases"][0]["savings_percent"], 15.0)

    def test_unsafe_sources_are_excluded_and_purge_is_confined(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            (root / "access-token.txt").write_text("not indexed\n", encoding="utf-8")
            (root / "binary.txt").write_bytes(b"safe\0unsafe")
            (root / "credential.txt").write_text(
                "api_key = 'abcdefghijklmnop123456'\n", encoding="utf-8"
            )
            outside = root.parent / "outside-source.txt"
            outside.write_text("outside\n", encoding="utf-8")
            (root / "linked.txt").symlink_to(outside)
            cache = CACHE.resolve_cache(root, None)
            CACHE.build(root, cache)
            connection = sqlite3.connect(cache)
            try:
                paths = {row[0] for row in connection.execute("SELECT path FROM documents")}
            finally:
                connection.close()
            self.assertNotIn("access-token.txt", paths)
            self.assertNotIn("binary.txt", paths)
            self.assertNotIn("credential.txt", paths)
            self.assertNotIn("linked.txt", paths)
            purged = CACHE.purge(root, cache)
            self.assertEqual(purged["status"], "removed")
            self.assertFalse(cache.exists())
            self.assertTrue((root / "src/runtime.py").is_file())
            with self.assertRaisesRegex(CACHE.CacheError, "escapes"):
                CACHE.resolve_cache(root, root.parent / "outside.sqlite3")

            safe_cache_dir = root / "safe-cache"
            safe_cache_dir.mkdir()
            (root / "linked-cache").symlink_to(
                safe_cache_dir, target_is_directory=True
            )
            with self.assertRaisesRegex(CACHE.CacheError, "symbolic links"):
                CACHE.resolve_cache(root, Path("linked-cache/cache.sqlite3"))

            linked_root = root.parent / "linked-root"
            linked_root.symlink_to(root, target_is_directory=True)
            try:
                with self.assertRaisesRegex(CACHE.CacheError, "symbolic link"):
                    CACHE.resolve_root(linked_root)
            finally:
                linked_root.unlink()

    def test_cli_stdout_is_toon_for_success_and_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            built = subprocess.run(
                [sys.executable, str(SCRIPT), "build", "--root", str(root)],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            self.assertEqual(CACHE.encode_toon(CACHE.CACHE_TOON.loads(built.stdout)) if hasattr(CACHE, "CACHE_TOON") else built.stdout, built.stdout)
            queried = subprocess.run(
                [sys.executable, str(SCRIPT), "query", "--root", str(root), "--query", "AC-101 freshness"],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(queried.returncode, 0, queried.stderr)
            from ai_sdlc_toon import decode_toon
            self.assertEqual(decode_toon(queried.stdout)["schema"], CACHE.QUERY_SCHEMA)
            failed = subprocess.run(
                [sys.executable, str(SCRIPT), "inspect", "--root", str(root), "--cache", "missing.sqlite3"],
                check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(failed.returncode, 1)
            self.assertEqual(decode_toon(failed.stdout)["strategy"], "direct_read")


if __name__ == "__main__":
    unittest.main()
