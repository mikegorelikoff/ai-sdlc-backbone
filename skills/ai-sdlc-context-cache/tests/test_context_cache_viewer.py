#!/usr/bin/env python3
"""Focused tests for the reusable offline context graph viewer."""

from __future__ import annotations

import hashlib
import importlib.util
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-context-cache/scripts/context_cache.py"
VIEWER = ROOT / "skills/ai-sdlc-context-cache/scripts/graph_viewer.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_context_cache_viewer", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CACHE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CACHE)


class ContextCacheViewerTests(unittest.TestCase):
    SOURCE = (
        "def render_value():\n"
        "    marker = 'SOURCE_BODY_SENTINEL'\n"
        "    boundary = '</script><script>EVIL_SENTINEL'\n"
        "    return marker + boundary\n"
    )

    def repository(self, directory: str) -> tuple[Path, Path]:
        root = Path(directory)
        subprocess.run(
            ["git", "init", str(root)], check=True, stdout=subprocess.DEVNULL
        )
        source = root / "src/app.py"
        source.parent.mkdir()
        source.write_text(self.SOURCE, encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        cache = CACHE.resolve_cache(root, None)
        cache.parent.mkdir(parents=True)
        connection = sqlite3.connect(cache)
        CACHE.initialize(connection)
        connection.executescript(
            """
            CREATE TABLE symbols (
                id TEXT PRIMARY KEY, path TEXT NOT NULL, language TEXT NOT NULL,
                kind TEXT NOT NULL, name TEXT NOT NULL,
                qualified_name TEXT NOT NULL, start_byte INTEGER NOT NULL,
                end_byte INTEGER NOT NULL, start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL
            );
            CREATE TABLE occurrences (
                id TEXT PRIMARY KEY, path TEXT NOT NULL, symbol_id TEXT NOT NULL,
                role TEXT NOT NULL, name TEXT NOT NULL, container TEXT NOT NULL,
                start_byte INTEGER NOT NULL, end_byte INTEGER NOT NULL,
                start_line INTEGER NOT NULL, end_line INTEGER NOT NULL
            );
            CREATE TABLE ast_calls (
                id TEXT PRIMARY KEY, path TEXT NOT NULL, language TEXT NOT NULL,
                name TEXT NOT NULL, start_byte INTEGER NOT NULL,
                end_byte INTEGER NOT NULL, start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL
            );
            CREATE TABLE graph_nodes (
                id TEXT PRIMARY KEY, kind TEXT NOT NULL, path TEXT NOT NULL,
                label TEXT NOT NULL
            );
            CREATE TABLE graph_edges (
                source_id TEXT NOT NULL, target_id TEXT NOT NULL,
                kind TEXT NOT NULL, label TEXT NOT NULL,
                evidence_path TEXT NOT NULL,
                PRIMARY KEY(source_id, target_id, kind, label, evidence_path)
            );
            """
        )
        source_hash = hashlib.sha256(self.SOURCE.encode("utf-8")).hexdigest()
        metadata = {
            "schema": CACHE.DB_SCHEMA,
            "config_fingerprint": CACHE.config_fingerprint(),
            "graph_complete": "true",
            "graph_fingerprint": "graph-fixture-v1",
            "repository_fingerprint": "repository-fixture-v1",
            "cache_fingerprint": "cache-fixture-v1",
        }
        connection.executemany(
            "INSERT INTO metadata(key, value) VALUES(?, ?)", sorted(metadata.items())
        )
        connection.execute(
            "INSERT INTO documents VALUES(?, ?, ?, ?, ?)",
            ("src/app.py", source_hash, len(self.SOURCE.encode("utf-8")), 4, "evidence_only"),
        )
        connection.execute(
            "INSERT INTO chunks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "chunk-1", "src/app.py", 0, 1, 4, "chunk-hash", source_hash,
                24, "", "", self.SOURCE,
            ),
        )
        connection.executemany(
            "INSERT INTO graph_nodes VALUES(?, ?, ?, ?)",
            [
                ("file-1", "file", "src/app.py", "src/app.py"),
                ("chunk-1", "chunk", "src/app.py", "src/app.py:1-4"),
                ("symbol-1", "symbol", "src/app.py", "render_value"),
                ("call-1", "call", "src/app.py", "render_value"),
            ],
        )
        connection.execute(
            "INSERT INTO symbols VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("symbol-1", "src/app.py", "python", "function", "render_value", "render_value", 0, 18, 1, 4),
        )
        connection.execute(
            "INSERT INTO ast_calls VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            ("call-1", "src/app.py", "python", "render_value", 0, 12, 1, 1),
        )
        connection.executemany(
            "INSERT INTO graph_edges VALUES(?, ?, ?, ?, ?)",
            [
                ("file-1", "chunk-1", "contains", "chunk", "src/app.py"),
                ("file-1", "symbol-1", "defines", "function", "src/app.py"),
                ("call-1", "symbol-1", "calls", "render_value", "src/app.py"),
            ],
        )
        connection.commit()
        connection.close()
        return root, cache

    def test_visualize_is_deterministic_complete_and_source_free_by_default(self) -> None:
        with tempfile.TemporaryDirectory(prefix="context graph #") as directory:
            root, cache = self.repository(directory)
            first = CACHE.visualize(root, cache)
            html_path = root / first["output"]
            first_bytes = html_path.read_bytes()
            second = CACHE.visualize(root, cache)
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, html_path.read_bytes())
            self.assertEqual(first["nodes"], 4)
            self.assertEqual(first["edges"], 3)
            self.assertEqual(first["source_files"], 0)
            html = first_bytes.decode("utf-8")
            self.assertNotIn("SOURCE_BODY_SENTINEL", html)
            self.assertNotIn("https://", html)
            self.assertIn("const ADJ = new Map()", html)
            self.assertIn("Direct relations", html)
            self.assertIn('role="dialog"', html)
            self.assertIn('id="modalBackdrop"', html)
            self.assertIn("function openModal()", html)
            self.assertIn("event.target===modalBackdrop", html)
            self.assertIn('aria-label="Graph filters and view settings"', html)
            self.assertIn('id="reset" class="control-button fit"', html)
            self.assertIn('id="inspectorKind"', html)
            self.assertIn('id="propertiesTitle"', html)
            self.assertIn('id="contextTitle"', html)
            self.assertIn('id="incomingTotal"', html)
            self.assertIn('id="outgoingTotal"', html)
            self.assertIn('id="sourceState"', html)
            self.assertIn("item.className='property-row'", html)
            self.assertIn("chevron.className='chevron'", html)
            self.assertIn('<header class="topbar" role="banner">', html)
            self.assertIn('id="headerGraphCount"', html)
            self.assertIn('<body class="linear-shell">', html)
            self.assertNotIn('class="status-pill"', html)
            self.assertNotIn('class="tab-count"', html)
            self.assertNotIn('class="summary-chip"', html)
            self.assertNotIn('class="filter-chip', html)
            self.assertNotIn('<aside class="panel">', html)
            modal = html.split('id="inspectorModal"', 1)[1].split('</section>\n  </div>', 1)[0]
            self.assertNotIn('id="nodeToggles"', modal)
            self.assertNotIn('id="edgeToggle"', modal)
            self.assertNotIn('Graph snapshot', modal)
            self.assertNotIn('id="nodeTotal"', modal)

    def test_source_opt_in_escapes_script_boundaries_and_labels_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, cache = self.repository(directory)
            receipt = CACHE.visualize(root, cache, include_source=True)
            html = (root / receipt["output"]).read_text(encoding="utf-8")
            self.assertEqual(receipt["source_files"], 1)
            self.assertEqual(receipt["stale_source_files"], 0)
            self.assertIn("SOURCE_BODY_SENTINEL", html)
            self.assertNotIn("</script><script>EVIL_SENTINEL", html)
            self.assertIn("\\u003c/script>\\u003cscript>EVIL_SENTINEL", html)
            self.assertIn("tok-keyword", html)
            self.assertIn("highlightLine(code", html)
            (root / "src/app.py").write_text(self.SOURCE + "# drift\n", encoding="utf-8")
            stale = CACHE.visualize(root, cache, include_source=True)
            self.assertEqual(stale["status"], "stale")
            self.assertEqual(stale["stale"], 1)
            self.assertEqual(stale["stale_source_files"], 1)

    def test_output_is_confined_and_incomplete_graph_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, cache = self.repository(directory)
            with self.assertRaisesRegex(CACHE.CacheError, "inside the cache directory"):
                CACHE.visualize(root, cache, root / "outside.html")
            connection = sqlite3.connect(cache)
            connection.execute(
                "UPDATE metadata SET value='false' WHERE key='graph_complete'"
            )
            connection.commit()
            connection.close()
            with self.assertRaisesRegex(CACHE.CacheError, "graph is incomplete"):
                CACHE.visualize(root, cache)

    def test_cli_emits_toon_receipt_and_embedded_javascript_compiles(self) -> None:
        helper_help = subprocess.run(
            [sys.executable, str(VIEWER), "--help"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(helper_help.returncode, 0, helper_help.stderr)
        self.assertIn("--state-check", helper_help.stdout)
        self.assertIn("--quick-flow", helper_help.stdout)
        with tempfile.TemporaryDirectory() as directory:
            root, _cache = self.repository(directory)
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPT), "visualize", "--root", str(root),
                    "--output", ".ai-sdlc/cache/cli-view.html", "--include-source",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = CACHE.decode_toon(result.stdout)
            self.assertEqual(receipt["schema"], CACHE.GRAPH_VIEWER.VIEW_SCHEMA)
            self.assertEqual(receipt["command"], "visualize")
            self.assertEqual(receipt["output"], ".ai-sdlc/cache/cli-view.html")
            if shutil.which("node"):
                html = (root / receipt["output"]).read_text(encoding="utf-8")
                script = html.split("<script>", 1)[1].rsplit("</script>", 1)[0]
                javascript = root / ".ai-sdlc/cache/viewer-check.js"
                javascript.write_text(script, encoding="utf-8")
                checked = subprocess.run(
                    ["node", "--check", str(javascript)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == "__main__":
    unittest.main()
