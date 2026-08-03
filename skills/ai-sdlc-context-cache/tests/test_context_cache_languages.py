#!/usr/bin/env python3
"""Twelve-language Tree-sitter completeness tests for the code graph."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-context-cache/scripts/context_cache.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_context_cache_graph", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CACHE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CACHE)
GRAPH = CACHE.CODE_GRAPH

SOURCES = {
    "src/typescript.ts": 'import {x} from "./x"; class Greeter { hello(): number { return helper(); } } function helper(): number { return 1; }',
    "src/python.py": "import os\nclass Greeter:\n def hello(self):\n  return helper()\ndef helper(): return 1\n",
    "src/javascript.js": 'import x from "./x.js"; class Greeter { hello() { return helper(); } } function helper() { return 1; }',
    "src/java.java": "import java.util.List; class Greeter { int hello() { return helper(); } int helper(){ return 1; } }",
    "src/csharp.cs": "using System; class Greeter { int Hello() { return Helper(); } int Helper(){ return 1; } }",
    "src/php.php": "<?php use Foo\\Bar; class Greeter { function hello() { return helper(); } } function helper(){ return 1; }",
    "src/shell.sh": "source ./lib.sh\nhello() { helper; }\nhelper() { echo hi; }\n",
    "src/cpp.cpp": '#include "x.h"\nclass Greeter { public: int hello(){ return helper(); } int helper(){ return 1; } };',
    "src/go.go": 'package demo\nimport "fmt"\ntype Greeter struct{}\nfunc (g Greeter) Hello() int { return helper() }\nfunc helper() int { fmt.Println("x"); return 1 }',
    "src/rust.rs": "use std::fmt; struct Greeter; impl Greeter { fn hello(&self) -> i32 { helper() } } fn helper() -> i32 { 1 }",
    "src/kotlin.kt": 'package demo\nimport kotlin.io.println\nclass Greeter { fun hello(): Int = helper() }\nfun helper(): Int { println("x"); return 1 }',
    "src/swift.swift": "import Foundation\nclass Greeter { func hello() -> Int { return helper() } }\nfunc helper() -> Int { return 1 }",
}


@unittest.skipIf(GRAPH is None, "graph runtime requires Python 3.10+")
class ContextCacheLanguageTests(unittest.TestCase):
    def repository(self, directory: str) -> Path:
        root = Path(directory)
        subprocess.run(["git", "init", str(root)], check=True, stdout=subprocess.DEVNULL)
        for relative, content in SOURCES.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        return root

    def test_tc_001_preflight_verifies_all_twelve_pinned_grammars(self) -> None:
        output = GRAPH.preflight()
        self.assertTrue(output["complete"], output)
        self.assertEqual(len(output["languages"]), 12)
        self.assertEqual({row["status"] for row in output["languages"]}, {"ready"})
        self.assertEqual(output["runtime_network"], "denied")

    def test_tc_001_parser_lock_requires_the_complete_runtime(self) -> None:
        lock_path = ROOT / "skills/ai-sdlc-context-cache/references/parser-lock.toon"
        lock = CACHE.decode_toon(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(GRAPH.parser_lock_errors(lock), [])
        partial = dict(lock)
        partial["wheels"] = list(lock["wheels"])[:-1]
        self.assertIn(
            "incomplete-or-duplicate-wheel-lock",
            GRAPH.parser_lock_errors(partial),
        )

    def test_tc_002_native_parser_crash_is_contained(self) -> None:
        original = GRAPH.subprocess.run
        try:
            GRAPH.subprocess.run = lambda *_args, **_kwargs: subprocess.CompletedProcess(
                args=[], returncode=-11, stdout="", stderr=""
            )
            with self.assertRaisesRegex(GRAPH.GraphError, "parser-process-failed"):
                GRAPH.extract_isolated(
                    "src/crash.py", "def safe(): return 1\n", "0" * 64
                )
        finally:
            GRAPH.subprocess.run = original

    def test_tc_002_parser_environment_excludes_parent_secrets(self) -> None:
        marker = "AI_SDLC_TEST_SECRET"
        original = os.environ.get(marker)
        try:
            os.environ[marker] = "must-not-reach-parser"
            environment = GRAPH._parser_environment()
            self.assertNotIn(marker, environment)
            self.assertEqual(environment["AI_SDLC_RUNTIME_NETWORK"], "denied")
            self.assertEqual(environment["PYTHONNOUSERSITE"], "1")
        finally:
            if original is None:
                os.environ.pop(marker, None)
            else:
                os.environ[marker] = original

    def test_tc_005_each_language_emits_ast_symbols_and_occurrences(self) -> None:
        languages = set()
        for relative, content in sorted(SOURCES.items()):
            facts = GRAPH.extract(
                relative, content, hashlib.sha256(content.encode()).hexdigest()
            )
            languages.add(facts.language)
            self.assertGreater(len(facts.symbols), 0, relative)
            self.assertGreater(len(facts.occurrences), 0, relative)
            self.assertGreater(facts.node_count, 0, relative)
        self.assertEqual(languages, set(GRAPH.LANGUAGE_SUFFIXES))

    def test_tc_006_real_parse_error_never_claims_completeness(self) -> None:
        with self.assertRaisesRegex(GRAPH.GraphError, "parse-error:kotlin"):
            content = "class Broken { fun nope( }"
            GRAPH.extract(
                "src/broken.kt", content,
                hashlib.sha256(content.encode()).hexdigest(),
            )

    def test_tc_007_kotlin_and_swift_share_completeness_gate(self) -> None:
        for language, relative in (
            ("kotlin", "src/kotlin.kt"), ("swift", "src/swift.swift")
        ):
            content = SOURCES[relative]
            facts = GRAPH.extract(
                relative, content, hashlib.sha256(content.encode()).hexdigest()
            )
            self.assertEqual(facts.language, language)
            self.assertTrue(any(row[4] == "Greeter" for row in facts.symbols))
            self.assertTrue(any(row[3] == "definition" for row in facts.occurrences))

    def test_tc_008_each_missing_grammar_blocks_graph_complete(self) -> None:
        original = GRAPH._get_parser
        try:
            for missing in GRAPH.LANGUAGE_SUFFIXES:
                def loader(language: str, path: str = "", missing_language: str = missing):
                    if language == missing_language:
                        raise RuntimeError("missing test grammar")
                    return original(language, path)
                GRAPH._get_parser = loader
                output = GRAPH.preflight()
                self.assertFalse(output["complete"], missing)
                row = next(item for item in output["languages"] if item["language"] == missing)
                self.assertEqual(row["status"], "missing")
        finally:
            GRAPH._get_parser = original

    def test_tc_009_clean_graph_builds_are_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.repository(directory)
            cache = CACHE.resolve_cache(root, None)
            first = CACHE.build(root, cache, rebuild=True, require_graph=True)
            first_stats = CACHE.graph_stats(root, cache)
            second = CACHE.build(root, cache, rebuild=True, require_graph=True)
            second_stats = CACHE.graph_stats(root, cache)
            self.assertEqual(first["cache_fingerprint"], second["cache_fingerprint"])
            self.assertEqual(CACHE.canonical(first_stats), CACHE.canonical(second_stats))
            self.assertTrue(second_stats["graph_complete"])
            self.assertEqual(second_stats["counts"]["files"], 12)
            connection = sqlite3.connect(cache)
            try:
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM language_coverage WHERE files=1 AND parsed=1 AND errors=0"
                    ).fetchone()[0],
                    12,
                )
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
