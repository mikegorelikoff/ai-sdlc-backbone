#!/usr/bin/env python3
"""Run every skill-owned Python test file without silent discovery gaps."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from ai_sdlc_toon import encode_toon


SCHEMA = "ai-sdlc-test-suite-receipt/v1"


def digest(value: object) -> str:
    return hashlib.sha256(encode_toon(value).encode("utf-8")).hexdigest()


def discover(root: Path) -> tuple[Path, ...]:
    """Return the complete, stable skill test-file inventory."""
    root = root.resolve()
    skills = root / "skills"
    if skills.is_symlink() or not skills.is_dir():
        raise ValueError("TEST_SUITE_INVALID_ROOT: skills directory is unavailable")
    paths = tuple(
        path
        for path in sorted(skills.glob("*/tests/test_*.py"))
        if path.name != "test_each_skill_tests.py"
    )
    if not paths:
        raise ValueError("TEST_SUITE_EMPTY: no skill test files were discovered")
    for path in paths:
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(
                f"TEST_SUITE_UNSAFE_PATH: {path.relative_to(root)}"
            ) from exc
        if path.is_symlink() or not resolved.is_file():
            raise ValueError(
                f"TEST_SUITE_UNSAFE_PATH: {path.relative_to(root)}"
            )
    return paths


def run_suite(root: Path, paths: tuple[Path, ...], timeout: int) -> dict[str, Any]:
    """Execute each test file in path order and return a stable receipt."""
    root = root.resolve()
    items: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="ai-sdlc-test-pycache-") as cache:
        environment = os.environ.copy()
        environment["PYTHONPYCACHEPREFIX"] = cache
        for path in paths:
            relative = path.relative_to(root).as_posix()
            diagnostic = ""
            try:
                completed = subprocess.run(
                    [sys.executable, relative, "-v"],
                    cwd=root,
                    env=environment,
                    check=False,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=timeout,
                )
                exit_code = completed.returncode
                if exit_code:
                    diagnostic = (completed.stdout + completed.stderr)[-8_000:]
            except subprocess.TimeoutExpired as exc:
                exit_code = 124
                stdout = exc.stdout or b""
                stderr = exc.stderr or b""
                if isinstance(stdout, str):
                    stdout = stdout.encode("utf-8", errors="replace")
                if isinstance(stderr, str):
                    stderr = stderr.encode("utf-8", errors="replace")
                diagnostic = (stdout + stderr).decode(
                    "utf-8",
                    errors="replace",
                )[-8_000:]
            item: dict[str, object] = {
                "path": relative,
                "status": "passed" if exit_code == 0 else "failed",
                "exit_code": exit_code,
            }
            if diagnostic:
                item["diagnostic"] = diagnostic
            items.append(item)
    failed = sum(item["status"] == "failed" for item in items)
    semantic: dict[str, Any] = {
        "schema": SCHEMA,
        "test_files": len(items),
        "passed": len(items) - failed,
        "failed": failed,
        "result": "passed" if failed == 0 else "failed",
        "items": items,
    }
    return {**semantic, "fingerprint": digest(semantic)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--format", choices=("toon",), default="toon")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument(
        "--state-workspace",
        choices=("refinement", "implementation"),
    )
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        parser.error("test-suite execution cannot mutate feature lifecycle state")
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    try:
        root = args.root.resolve()
        paths = discover(root)
        if args.list:
            semantic: dict[str, Any] = {
                "schema": "ai-sdlc-test-suite-inventory/v1",
                "test_files": len(paths),
                "paths": [path.relative_to(root).as_posix() for path in paths],
            }
            result = {**semantic, "fingerprint": digest(semantic)}
            exit_code = 0
        else:
            result = run_suite(root, paths, args.timeout)
            exit_code = 0 if result["failed"] == 0 else 1
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(encode_toon(result), end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
