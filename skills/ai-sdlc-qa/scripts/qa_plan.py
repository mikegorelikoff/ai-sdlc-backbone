#!/usr/bin/env python3
"""Create a canonical TOON QA plan for AI SDLC."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if _SHARED.is_dir() and str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
try:
    from ai_sdlc_state_machine import add_state_arguments, run_state_action
except ImportError:
    add_state_arguments = None
    run_state_action = None

try:
    import usage_journal
except ImportError:
    usage_journal = None

try:
    from toon import encode_toon
except ImportError:
    from ai_sdlc_toon import encode_toon


FEATURE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
STATUSES = ("planned", "partial", "ready", "blocked")


def scenario(value: str) -> dict[str, str]:
    fields = ("id", "actor", "setup", "action", "expected", "evidence", "risk")
    parts = [part.strip() for part in value.split("|", 6)]
    if len(parts) != len(fields) or any(not part for part in parts):
        raise argparse.ArgumentTypeError(
            "acceptance must be ID|actor|setup|action|expected|evidence|risk"
        )
    if not re.fullmatch(r"QA-[0-9]{3}", parts[0]):
        raise argparse.ArgumentTypeError("acceptance ID must match QA-NNN")
    if parts[-1] not in {"low", "medium", "high"}:
        raise argparse.ArgumentTypeError("acceptance risk must be low, medium, or high")
    return dict(zip(fields, parts))


def output_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.suffix != ".toon":
        raise argparse.ArgumentTypeError("output must be a safe project-relative .toon path")
    return path


def atomic_write(path: Path, content: str) -> None:
    root = Path.cwd().resolve()
    target = (root / path).resolve(strict=False)
    if target == root or root not in target.parents:
        raise ValueError("output escapes the project root")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("output path contains a symlink")
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--feature", required=True)
    result.add_argument("--summary", required=True)
    result.add_argument("--acceptance", action="append", required=True, type=scenario)
    result.add_argument("--regression", action="append", default=[])
    result.add_argument("--validation", action="append", default=[])
    result.add_argument("--manual-check", action="append", default=[])
    result.add_argument("--residual-risk", action="append", default=[])
    result.add_argument("--status", choices=STATUSES, default="planned")
    result.add_argument("--schema", default="ai-sdlc-qa-plan/v1")
    result.add_argument("--output", type=output_path)
    result.add_argument("--quick-flow", action="store_true", help="Run in quick flow mode")
    result.add_argument("--full-flow", action="store_true", help="Run in full flow mode")
    if add_state_arguments:
        add_state_arguments(result)
    return result


def main() -> int:
    args = parser().parse_args()
    if run_state_action:
        state_rc = run_state_action(args, "ai-sdlc-qa", "refinement")
        if state_rc:
            return state_rc
    if not FEATURE.fullmatch(args.feature):
        raise SystemExit("feature must be a lowercase hyphenated slug")
    artifact = {
        "schema": args.schema,
        "feature": args.feature,
        "summary": args.summary.strip(),
        "status": args.status,
        "acceptance": args.acceptance,
        "regression_targets": [value.strip() for value in args.regression if value.strip()],
        "validation_evidence": [value.strip() for value in args.validation if value.strip()],
        "manual_checks": [value.strip() for value in args.manual_check if value.strip()],
        "residual_risks": [value.strip() for value in args.residual_risk if value.strip()],
    }
    content = encode_toon(artifact)
    if args.output:
        try:
            atomic_write(args.output, content)
        except ValueError as error:
            raise SystemExit(str(error)) from error
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    if usage_journal:
        with usage_journal.track_skill("ai-sdlc-qa", trigger="user"):
            raise SystemExit(main())
    else:
        raise SystemExit(main())
