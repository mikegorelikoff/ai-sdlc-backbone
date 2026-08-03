#!/usr/bin/env python3
"""Run deterministic production gates for the whole-codebase AST graph."""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / "skills/ai-sdlc-shared-runtime/scripts"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))
from ai_sdlc_toon import encode_toon  # noqa: E402

SCRIPT = ROOT / "skills/ai-sdlc-context-cache/scripts/context_cache.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_context_cache_release", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CACHE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CACHE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--runs", type=int, choices=(2, 3), default=2)
    parser.add_argument(
        "--fault",
        choices=("parser", "determinism", "bounds", "freshness", "economics", "suite"),
    )
    parser.add_argument("--format", choices=("toon",), default="toon")
    args = parser.parse_args()
    root = CACHE.resolve_root(args.root)
    cache = CACHE.resolve_cache(root, None)
    gates: list[list[object]] = []
    preflight = CACHE.graph_preflight(root)
    parser_ok = bool(preflight.get("complete")) and args.fault != "parser"
    gates.append(["parser_preflight", "passed" if parser_ok else "failed"])

    receipts = []
    for index in range(args.runs):
        receipts.append(CACHE.build(
            root, cache, rebuild=index == 0, require_graph=True
        ))
    fingerprints = [str(row["cache_fingerprint"]) for row in receipts]
    deterministic = len(set(fingerprints)) == 1 and args.fault != "determinism"
    gates.append(["determinism", "passed" if deterministic else "failed"])

    stats = CACHE.graph_stats(root, cache)
    complete = bool(stats.get("graph_complete")) and args.fault != "freshness"
    bounds = (
        int(stats["counts"]["edges"]) <= int(stats["bounds"]["max_total_edges"])
        and int(stats["max_fanout"]) <= int(stats["bounds"]["max_edges_per_kind"])
        and args.fault != "bounds"
    )
    gates.append(["fresh_complete_graph", "passed" if complete else "failed"])
    gates.append(["relation_bounds", "passed" if bounds else "failed"])

    packed = CACHE.pack(
        root, cache, "Tree-sitter Kotlin Swift graph completeness",
        "ai-sdlc-context-cache", "retrieve", 4000, 24, 2, 128,
        min_savings_percent=25.0, require_graph=True,
    )
    economic = (
        packed["strategy"] == "packed"
        and float(packed["savings_percent"]) >= 25.0
        and float(packed["critical_recall_percent"]) == 100.0
        and args.fault != "economics"
    )
    gates.append(["token_economics", "passed" if economic else "failed"])

    environment = dict(os.environ)
    environment["PYTHONPYCACHEPREFIX"] = "/tmp/ai-sdlc-release-pyc"
    suite = subprocess.run(
        [
            sys.executable, "-m", "unittest",
            "skills/ai-sdlc-context-cache/tests/test_context_cache.py",
            "skills/ai-sdlc-context-cache/tests/test_context_cache_languages.py",
            "skills/ai-sdlc-context-cache/tests/test_context_cache_graph.py",
            "skills/ai-sdlc-context-cache/tests/test_context_cache_retrieval.py",
        ],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        env=environment,
    )
    suite_ok = suite.returncode == 0 and args.fault != "suite"
    gates.append(["focused_regression", "passed" if suite_ok else "failed"])
    production_ready = all(row[1] == "passed" for row in gates)
    output = {
        "schema": "ai-sdlc-code-graph-release-audit/v1",
        "status": "passed" if production_ready else "failed",
        "production_ready": production_ready,
        "runs": args.runs,
        "fault": args.fault or "none",
        "gates": gates,
        "cache_fingerprints": fingerprints,
        "repository_fingerprint": str(stats.get("repository_fingerprint", "")),
        "graph_fingerprint": str(stats.get("graph_fingerprint", "")),
        "graph_counts": stats.get("counts", {}),
        "coverage": stats.get("coverage", []),
        "max_fanout": stats.get("max_fanout", 0),
        "packed_tokens": int(packed["packed_tokens"]),
        "raw_tokens": int(packed["raw_tokens"]),
        "savings_percent": float(packed["savings_percent"]),
        "critical_recall_percent": float(packed["critical_recall_percent"]),
    }
    print(encode_toon(output), end="")
    return 0 if production_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
