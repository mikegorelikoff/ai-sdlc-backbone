#!/usr/bin/env python3
"""Evaluate every executable skill graph with deterministic TOON receipts."""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Callable


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ai_sdlc_steps as steps_runtime  # noqa: E402
from ai_sdlc_paths import repository_root_from_skills_root  # noqa: E402
from ai_sdlc_safe_io import atomic_write_text, bounded_path  # noqa: E402
from ai_sdlc_step_context import validate_step_context_pack  # noqa: E402
from ai_sdlc_toon import encode_toon  # noqa: E402


RECEIPT_SCHEMA = "ai-sdlc-eval-receipt/v1"
LIVE_PROTOCOL_SCHEMA = "ai-sdlc-live-eval-protocol/v1"
LIVE_RECEIPT_SCHEMA = "ai-sdlc-live-eval-receipt/v1"
SCENARIOS = ("happy", "blocked", "invalid", "resume", "context")
LIVE_SCENARIOS = (
    {
        "id": "routing",
        "criterion": "routing",
        "skill": "ai-sdlc-flow",
        "phase": "execute",
        "required_types": ("analysis", "action"),
    },
    {
        "id": "step-compliance",
        "criterion": "step_compliance",
        "skill": "ai-sdlc-sdd",
        "phase": "validate",
        "required_types": ("analysis", "context", "action", "validation"),
    },
    {
        "id": "evidence",
        "criterion": "evidence",
        "skill": "ai-sdlc-qa",
        "phase": "handoff",
        "required_types": (
            "analysis",
            "context",
            "action",
            "validation",
            "handoff",
        ),
    },
    {
        "id": "recovery",
        "criterion": "recovery",
        "skill": "ai-sdlc-scheduler",
        "phase": "execute",
        "required_types": ("analysis", "context", "action"),
    },
    {
        "id": "context",
        "criterion": "context",
        "skill": "ai-sdlc-project-context",
        "phase": "execute",
        "required_types": ("analysis", "context", "action"),
    },
    {
        "id": "authorization",
        "criterion": "authorization",
        "skill": "ai-sdlc-approvals-sandbox",
        "phase": "execute",
        "required_types": ("analysis", "context", "action"),
    },
)
LIVE_THRESHOLDS = {
    "routing": 90,
    "step_compliance": 100,
    "evidence": 90,
    "recovery": 90,
    "context": 90,
    "authorization": 100,
}


def digest(value: object) -> str:
    """Hash one canonical portable value."""
    return hashlib.sha256(encode_toon(value).encode("utf-8")).hexdigest()


def root_from_skills_root(skills_root: Path) -> Path:
    """Resolve a source or project-scoped skills directory."""
    try:
        return repository_root_from_skills_root(skills_root)
    except ValueError as exc:
        raise ValueError(f"EVAL_INVALID_ROOT: {exc}") from exc


def skill_names(skills_root: Path, selected: set[str]) -> tuple[str, ...]:
    """Return the stable installable skill inventory."""
    if skills_root.is_symlink() or not skills_root.is_dir():
        raise ValueError(f"EVAL_INVALID_ROOT: {skills_root}")
    names = tuple(
        path.name
        for path in sorted(skills_root.iterdir())
        if path.is_dir()
        and not path.is_symlink()
        and path.name.startswith("ai-sdlc-")
        and (path / "SKILL.md").is_file()
    )
    if selected:
        missing = sorted(selected - set(names))
        if missing:
            raise ValueError("EVAL_UNKNOWN_SKILL: " + ", ".join(missing))
        return tuple(name for name in names if name in selected)
    if not names:
        raise ValueError("EVAL_EMPTY_CATALOG: no installable skills found")
    return names


def _case(
    scenario: str,
    callback: Callable[[], str],
) -> dict[str, str]:
    """Execute one isolated scenario without hiding its failure reason."""
    try:
        evidence = callback()
    except (OSError, RuntimeError, ValueError) as exc:
        return {
            "scenario": scenario,
            "status": "failed",
            "evidence": f"{type(exc).__name__}: {exc}",
        }
    return {"scenario": scenario, "status": "passed", "evidence": evidence}


def _happy(root: Path, skill: str, cache: dict[str, object]) -> str:
    first = steps_runtime.select_steps(root, skill, "prepare")
    second = steps_runtime.select_steps(root, skill, "prepare")
    if encode_toon(asdict(first)) != encode_toon(asdict(second)):
        raise ValueError("selection bytes changed for identical inputs")
    if first.schema != steps_runtime.SELECTION_SCHEMA or not first.ready_steps:
        raise ValueError("prepare did not produce a ready v2 selection")
    if any(card["schema"] != steps_runtime.STEP_CARD_SCHEMA for card in first.step_cards):
        raise ValueError("prepare emitted a non-StepCard result")
    plan_a = steps_runtime.compile_run_plan(root, skill, "execute")
    plan_b = steps_runtime.compile_run_plan(root, skill, "execute")
    if encode_toon(plan_a) != encode_toon(plan_b):
        raise ValueError("run-plan bytes changed for identical inputs")
    cache["prepare"] = first
    cache["plan"] = plan_a
    cache["graph_fingerprint"] = first.graph_fingerprint
    return (
        f"selection={first.selection_fingerprint};"
        f"plan={plan_a['fingerprint']};ready={len(first.ready_steps)}"
    )


def _blocked(root: Path, skill: str, cache: dict[str, object]) -> str:
    selection = steps_runtime.select_steps(root, skill, "execute")
    waiting = tuple(
        item for item in selection.skipped if ":waiting-for:" in item
    )
    if not selection.ready_steps or not waiting:
        raise ValueError("dependency gate did not leave downstream work waiting")
    if len(selection.pending_steps) <= len(selection.ready_steps):
        raise ValueError("execute closure was not dependency-gated")
    cache["execute"] = selection
    return (
        f"ready={','.join(selection.ready_steps)};"
        f"waiting={len(waiting)}"
    )


def _invalid(root: Path, skill: str, _cache: dict[str, object]) -> str:
    try:
        steps_runtime.select_steps(root, skill, "outside-contract")
    except ValueError as exc:
        if str(exc) == "STEP_UNKNOWN_PHASE: outside-contract":
            return "STEP_UNKNOWN_PHASE rejected before graph execution"
        raise
    raise ValueError("unknown phase was accepted")


def _resume(root: Path, skill: str, cache: dict[str, object]) -> str:
    selection = cache.get("execute")
    if not isinstance(selection, steps_runtime.StepSelection):
        selection = steps_runtime.select_steps(root, skill, "execute")
    completed: set[str] = set()
    waves: list[str] = []
    previous_pending = len(selection.pending_steps) + 1
    for _ in range(16):
        if len(selection.pending_steps) >= previous_pending:
            raise ValueError("resume did not reduce the pending set")
        previous_pending = len(selection.pending_steps)
        if selection.complete:
            break
        if not selection.ready_steps:
            raise ValueError("resume reached a nonterminal graph with no ready node")
        waves.append("+".join(selection.ready_steps))
        completed.update(selection.ready_steps)
        selection = steps_runtime.select_steps(
            root,
            skill,
            "execute",
            completed_steps=sorted(completed),
        )
    else:
        raise ValueError("resume exceeded the bounded wave count")
    if not selection.complete or tuple(sorted(completed)) != tuple(
        sorted(selection.execution_order)
    ):
        raise ValueError("resume did not reach the exact terminal closure")
    return f"waves={'>'.join(waves)};completed={len(completed)}"


def _context(root: Path, skill: str, cache: dict[str, object]) -> str:
    selection = cache.get("prepare")
    if not isinstance(selection, steps_runtime.StepSelection):
        selection = steps_runtime.select_steps(root, skill, "prepare")
    if not selection.step_cards:
        raise ValueError("selection contains no context-bearing StepCard")
    strategies: set[str] = set()
    fingerprints: list[str] = []
    for card in selection.step_cards:
        context = card["context"]
        if context["schema"] != "ai-sdlc-context-pack/v4":
            raise ValueError("StepCard context schema is not v4")
        if context["critical_recall_percent"] != 100.0:
            raise ValueError("critical-anchor recall is below 100 percent")
        if not context["sufficient"]:
            raise ValueError("mandatory context is insufficient")
        strategy = str(context["strategy"])
        if strategy == "packed":
            if context["savings_percent"] < 15:
                raise ValueError("packed context misses the economics gate")
        elif strategy == "direct_read":
            if not context["direct_read_paths"] or not context["reason"]:
                raise ValueError("direct reading lacks paths or reason")
        else:
            raise ValueError(f"unknown context strategy: {strategy}")
        strategies.add(strategy)
        fingerprints.append(str(context["fingerprint"]))
    return (
        f"strategy={'+'.join(sorted(strategies))};"
        f"context={digest(fingerprints)}"
    )


def evaluate_skill(root: Path, skill: str) -> dict[str, object]:
    """Run the fixed five-scenario matrix for one skill."""
    _skill_root, manifest = steps_runtime.load_manifest(root, skill)
    cache: dict[str, object] = {}
    callbacks = (
        ("happy", _happy),
        ("blocked", _blocked),
        ("invalid", _invalid),
        ("resume", _resume),
        ("context", _context),
    )
    results = [
        _case(name, lambda callback=callback: callback(root, skill, cache))
        for name, callback in callbacks
    ]
    graph_fingerprint = str(cache.get("graph_fingerprint", digest(manifest)))
    return {
        "skill": skill,
        "manifest_schema": manifest["schema"],
        "nodes": len(manifest["steps"]),
        "graph_fingerprint": graph_fingerprint,
        "passed": sum(item["status"] == "passed" for item in results),
        "failed": sum(item["status"] == "failed" for item in results),
        "scenarios": results,
    }


def deterministic_receipt(
    skills_root: Path,
    selected: set[str] | None = None,
) -> dict[str, object]:
    """Run the all-skill deterministic matrix and return a stable receipt."""
    selected = selected or set()
    root = root_from_skills_root(skills_root)
    names = skill_names(skills_root.resolve(), selected)
    items = [evaluate_skill(root, skill) for skill in names]
    passed = sum(int(item["passed"]) for item in items)
    failed = sum(int(item["failed"]) for item in items)
    receipt: dict[str, object] = {
        "schema": RECEIPT_SCHEMA,
        "mode": "deterministic",
        "harness_version": steps_runtime.VERSION,
        "skills": len(items),
        "scenario_kinds": list(SCENARIOS),
        "scenarios": len(items) * len(SCENARIOS),
        "passed": passed,
        "failed": failed,
        "result": "passed" if failed == 0 else "failed",
        "catalog_fingerprint": digest(
            [
                {
                    "skill": item["skill"],
                    "graph_fingerprint": item["graph_fingerprint"],
                }
                for item in items
            ]
        ),
        "items": items,
    }
    receipt["receipt_fingerprint"] = digest(receipt)
    return receipt


def live_protocol_receipt(skills_root: Path) -> dict[str, object]:
    """Validate the portable live-evaluation protocol without provider calls."""
    root = root_from_skills_root(skills_root)
    installed = set(skill_names(skills_root.resolve(), set()))
    items: list[dict[str, object]] = []
    for scenario in LIVE_SCENARIOS:
        skill = str(scenario["skill"])
        status = "passed"
        evidence = ""
        plan_fingerprint = ""
        try:
            if skill not in installed:
                raise ValueError(f"representative skill is not installed: {skill}")
            _skill_root, manifest = steps_runtime.load_manifest(root, skill)
            by_id = {str(step["id"]): step for step in manifest["steps"]}
            plan = steps_runtime.compile_run_plan(
                root, skill, str(scenario["phase"])
            )
            types = {str(by_id[str(task["step_id"])]["type"]) for task in plan["tasks"]}
            missing = sorted(set(scenario["required_types"]) - types)
            if missing:
                raise ValueError("missing step types: " + ", ".join(missing))
            if any(not task["gates"] or not task["outputs"] for task in plan["tasks"]):
                raise ValueError("task lacks gates or evidence outputs")
            for task in plan["tasks"]:
                if (
                    task["schema"] != steps_runtime.STEP_CARD_SCHEMA
                    or task["ready"] is not True
                ):
                    raise ValueError("task is not a context-ready StepCard")
                validate_step_context_pack(
                    task["context"],
                    expected_skill=str(task["skill"]),
                    expected_step_id=str(task["step_id"]),
                    require_sufficient=True,
                )
            plan_fingerprint = str(plan["fingerprint"])
            evidence = (
                f"tasks={len(plan['tasks'])};types={'+'.join(sorted(types))}"
            )
        except (OSError, ValueError) as exc:
            status = "failed"
            evidence = f"{type(exc).__name__}: {exc}"
        items.append(
            {
                "id": scenario["id"],
                "criterion": scenario["criterion"],
                "skill": skill,
                "phase": scenario["phase"],
                "status": status,
                "plan_fingerprint": plan_fingerprint,
                "evidence": evidence,
            }
        )

    failed = sum(item["status"] == "failed" for item in items)
    protocol = {
        "schema": LIVE_PROTOCOL_SCHEMA,
        "scenario_version": "tc-012/v1",
        "provider_neutral": True,
        "scenarios": items,
        "thresholds": LIVE_THRESHOLDS,
        "required_evidence": [
            "provider",
            "host",
            "model",
            "execution_id",
            "scenario_results",
            "scores",
            "effect_receipts",
            "recovery_evidence",
        ],
    }
    template = {
        "schema": LIVE_RECEIPT_SCHEMA,
        "protocol_fingerprint": digest(protocol),
        "provider": "",
        "host": "",
        "model": "",
        "execution_id": "",
        "status": "pending",
        "scenario_results": [],
        "scores": {criterion: None for criterion in sorted(LIVE_THRESHOLDS)},
        "effect_receipts": [],
        "recovery_evidence": [],
    }
    receipt: dict[str, object] = {
        "schema": RECEIPT_SCHEMA,
        "mode": "live-protocol",
        "harness_version": steps_runtime.VERSION,
        "offline_scenarios": len(items),
        "passed": len(items) - failed,
        "failed": failed,
        "result": "passed" if failed == 0 else "failed",
        "protocol": protocol,
        "portable_receipt_template": template,
    }
    receipt["receipt_fingerprint"] = digest(receipt)
    return receipt


def atomic_output(root: Path, path: Path, content: str) -> None:
    """Write an explicitly requested, repository-bounded receipt atomically."""
    path = bounded_path(root, path)
    if path.suffix != ".toon":
        raise ValueError("EVAL_OUTPUT_FORMAT: output must end in .toon")
    atomic_write_text(root, path, content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("deterministic", "live-protocol"),
        required=True,
    )
    parser.add_argument("--skills-root", type=Path, required=True)
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--output", type=Path)
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
        parser.error("skill evaluation cannot mutate lifecycle state")

    try:
        root = root_from_skills_root(args.skills_root)
        if args.mode == "deterministic":
            receipt = deterministic_receipt(
                args.skills_root, selected=set(args.skill)
            )
        else:
            if args.skill:
                parser.error("--skill is available only in deterministic mode")
            receipt = live_protocol_receipt(args.skills_root)
        content = encode_toon(receipt)
        if args.output:
            output = args.output if args.output.is_absolute() else root / args.output
            atomic_output(root, output, content)
        else:
            print(content, end="")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0 if receipt["result"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
