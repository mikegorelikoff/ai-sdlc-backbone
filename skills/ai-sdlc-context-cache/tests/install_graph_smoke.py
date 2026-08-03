#!/usr/bin/env python3
"""Verify the pinned offline AST runtime and all twelve grammars."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import socket
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / "skills/ai-sdlc-shared-runtime/scripts"
SCRIPTS = ROOT / "skills/ai-sdlc-context-cache/scripts"
for candidate in (SHARED, SCRIPTS):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from ai_sdlc_toon import decode_toon, encode_toon  # noqa: E402
import code_graph as graph  # noqa: E402


def deny_network() -> None:
    def denied(*_args: object, **_kwargs: object) -> object:
        raise OSError("offline smoke denied network")
    socket.create_connection = denied  # type: ignore[assignment]
    socket.socket.connect = denied  # type: ignore[assignment]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--wheelhouse", type=Path)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--format", choices=("toon",), default="toon")
    args = parser.parse_args()
    if args.offline:
        deny_network()
    lock = decode_toon(args.lock.read_text(encoding="utf-8"))
    failures: list[str] = []
    lock_errors = graph.parser_lock_errors(lock)
    if lock_errors:
        failures.extend(lock_errors)
        lock = {}
    preflight = graph.preflight()
    if not preflight["complete"]:
        failures.append("parser-preflight-incomplete")
    wheel_rows: list[list[object]] = []
    if args.wheelhouse:
        for row in lock.get("wheels", []):
            if not isinstance(row, dict):
                continue
            filename = str(row.get("filename", ""))
            expected = str(row.get("sha256", ""))
            path = args.wheelhouse / filename
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
            status = "verified" if actual == expected and expected else "failed"
            wheel_rows.append([str(row.get("name", "")), filename, status])
            if status != "verified":
                failures.append(f"wheel-hash:{filename}")
    output = {
        "schema": "ai-sdlc-code-graph-install-smoke/v1",
        "status": "passed" if not failures else "failed",
        "offline": args.offline,
        "lock": args.lock.as_posix(),
        "preflight": preflight,
        "wheels": wheel_rows,
        "failures": sorted(failures),
    }
    print(encode_toon(output), end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
