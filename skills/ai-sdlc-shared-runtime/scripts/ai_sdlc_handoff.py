#!/usr/bin/env python3
"""Render a journal-backed AI SDLC run handoff v2."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import ai_sdlc_toon as toon_codec  # noqa: E402


SCHEMA = "ai-sdlc-handoff/v2"


@dataclass(frozen=True)
class NextAction:
    """A required or optional downstream action."""

    skill: str
    reason: str
    command: str
    expected_artifact: str


def parse_action(value: str) -> NextAction:
    parts = [part.strip() for part in value.split("|", 3)]
    if len(parts) != 4 or not all(parts):
        raise argparse.ArgumentTypeError(
            "action must be skill|reason|command|expected_artifact"
        )
    if not re.fullmatch(r"ai-sdlc-[a-z0-9]+(?:-[a-z0-9]+)*", parts[0]):
        raise argparse.ArgumentTypeError("action skill is invalid")
    return NextAction(*parts)


def digest(value: Any) -> str:
    return hashlib.sha256(toon_codec.encode_toon(value).encode("utf-8")).hexdigest()


def load_replayed_run(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load the owning runtime and require an exact current replay projection."""
    runtime_scripts = (
        Path(__file__).resolve().parents[2]
        / "ai-sdlc-runtime"
        / "scripts"
    )
    if not runtime_scripts.is_dir() or runtime_scripts.is_symlink():
        raise ValueError("handoff requires the sibling ai-sdlc-runtime skill")
    sys.path.insert(0, str(runtime_scripts))
    import runtime as runtime_engine

    resolved = run_dir.resolve()
    if run_dir.is_symlink() or not resolved.is_dir():
        raise ValueError("run directory is missing or unsafe")
    run_id = resolved.name
    plan, state, recovered = runtime_engine.load_run(resolved, run_id)
    if recovered:
        raise ValueError(
            "run projection differs from journal replay; resume the run first"
        )
    return plan, state


def build_handoff(
    plan: dict[str, Any],
    state: dict[str, Any],
    *,
    current_owner: str,
    required: NextAction,
    optional: list[NextAction],
    residual_risks: list[str],
) -> dict[str, Any]:
    status = state["status"]
    result = (
        "complete"
        if status == "completed"
        else "blocked"
        if status in {"paused", "stopped"}
        else "partial"
    )
    blockers: list[str] = []
    if state["stop_reason"]:
        blockers.append(state["stop_reason"])
    blockers.extend(
        f"{task['id']}: {task['reason']}"
        for task in state["tasks"]
        if task["status"] in {"failed", "blocked"} and task["reason"]
    )
    steps = [
        {
            "id": task["id"],
            "skill": task["skill"],
            "step_id": task["step_id"],
            "status": task["status"],
            "attempts": task["attempts"],
            "idempotency_key": task["idempotency_key"],
            "evidence": task["evidence"],
            "effect_receipt": task["effect_receipt"],
            "result_fingerprint": task["result_fingerprint"],
        }
        for task in state["tasks"]
    ]
    semantic = {
        "schema": SCHEMA,
        "result": result,
        "run_id": state["run_id"],
        "run_status": status,
        "sequence": state["sequence"],
        "plan_fingerprint": plan["fingerprint"],
        "graph_fingerprint": state["graph_fingerprint"],
        "event_fingerprint": state["event_fingerprint"],
        "steps": steps,
        "blockers": sorted(set(blockers)),
        "residual_risks": sorted(set(residual_risks)),
        "current_owner": current_owner,
        "next_required": asdict(required),
        "next_optional": [asdict(item) for item in optional],
    }
    return {**semantic, "fingerprint": digest(semantic)}


def render_markdown(value: dict[str, Any]) -> str:
    required = value["next_required"]
    lines = [
        "# AI SDLC Run Handoff",
        "",
        f"- Result: `{value['result']}`",
        f"- Run: `{value['run_id']}` at sequence {value['sequence']}",
        f"- Owner: `{value['current_owner']}`",
        f"- Fingerprint: `{value['fingerprint']}`",
        "",
        "## Steps",
        "",
    ]
    lines.extend(
        f"- `{step['id']}`: {step['status']}; attempts={step['attempts']}; "
        f"evidence={len(step['evidence'])}"
        for step in value["steps"]
    )
    lines.extend(["", "## Blockers", ""])
    lines.extend(f"- {item}" for item in value["blockers"])
    if not value["blockers"]:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Next Required",
            "",
            f"- Skill: `{required['skill']}`",
            f"- Reason: {required['reason']}",
            f"- Command: `{required['command']}`",
            f"- Expected artifact: `{required['expected_artifact']}`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--current-owner", required=True)
    parser.add_argument("--next-required", type=parse_action, required=True)
    parser.add_argument("--next-optional", type=parse_action, action="append", default=[])
    parser.add_argument("--residual-risk", action="append", default=[])
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print(
            "ERROR: handoff emission is read-only; runtime owns transitions"
        )
        return 1
    try:
        plan, state = load_replayed_run(args.run_dir)
        value = build_handoff(
            plan,
            state,
            current_owner=args.current_owner,
            required=args.next_required,
            optional=args.next_optional,
            residual_risks=args.residual_risk,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.format == "toon":
        print(toon_codec.encode_toon(value), end="")
    else:
        print(render_markdown(value), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
