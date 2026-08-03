#!/usr/bin/env python3
"""Verify and install the offline hash-locked AST graph runtime."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime/scripts"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))
from ai_sdlc_toon import decode_toon, encode_toon  # noqa: E402
from ai_sdlc_state_machine import add_state_arguments, run_state_action  # noqa: E402
import code_graph as graph  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    add_state_arguments(parser)
    args = parser.parse_args()
    state_rc = run_state_action(args, "ai-sdlc-context-cache", "implementation")
    if state_rc:
        return state_rc
    value = decode_toon(args.lock.read_text(encoding="utf-8"))
    failures: list[str] = []
    wheels: list[tuple[str, bytes]] = []
    rows: list[list[str]] = []
    lock_errors = graph.parser_lock_errors(value)
    if lock_errors:
        failures.extend(lock_errors)
    else:
        for item in value.get("wheels", []):
            if not isinstance(item, dict):
                failures.append("invalid-wheel-row")
                continue
            path = (args.wheelhouse / str(item.get("filename", ""))).resolve()
            try:
                path.relative_to(args.wheelhouse.resolve())
            except ValueError:
                failures.append("wheel-path-escape")
                continue
            data = path.read_bytes() if path.is_file() else b""
            actual = hashlib.sha256(data).hexdigest() if data else ""
            expected = str(item.get("sha256", ""))
            status = "verified" if actual == expected and expected else "failed"
            rows.append([str(item.get("name", "")), path.name, status])
            if status == "verified":
                wheels.append((path.name, data))
            else:
                failures.append(f"wheel-hash:{path.name}")
    installed = False
    if not failures and not args.verify_only:
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-verified-wheels-") as directory:
            verified_paths: list[Path] = []
            for filename, data in wheels:
                verified = Path(directory) / filename
                verified.write_bytes(data)
                verified.chmod(0o444)
                verified_paths.append(verified)
            result = subprocess.run(
                [
                    str(args.python), "-m", "pip", "install", "--no-index",
                    "--no-deps", *[str(path) for path in verified_paths],
                ],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            installed = result.returncode == 0
            if not installed:
                failures.append(f"pip-install-exit-{result.returncode}")
    output = {
        "schema": "ai-sdlc-code-graph-runtime-install/v1",
        "status": "passed" if not failures else "failed",
        "mode": "verify" if args.verify_only else "install",
        "network": "denied-by-no-index",
        "python": str(args.python),
        "wheelhouse": str(args.wheelhouse),
        "wheels": rows,
        "installed": installed,
        "failures": sorted(failures),
    }
    print(encode_toon(output), end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
