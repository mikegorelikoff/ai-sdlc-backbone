#!/usr/bin/env python3
"""Bridge scheduler leases to isolated one-StepCard runtime runs."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_SKILL = Path(__file__).resolve().parents[1]
SCHEDULER = load_module("ai_sdlc_worker_scheduler", _SKILL / "scripts/scheduler.py")
RUNTIME = load_module("ai_sdlc_worker_runtime", _SKILL.parents[0] / "ai-sdlc-runtime/scripts/runtime.py")
TOON = RUNTIME.toon_codec
DISPATCH_SCHEMA = "ai-sdlc-scheduler-dispatch/v1"


def bounded(root: Path, path: Path) -> Path:
    root = root.resolve()
    candidate = path.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("scheduler worker path escapes repository")
    if path.is_symlink():
        raise ValueError("scheduler worker path is a symlink")
    return candidate


def subplan(parent: dict[str, Any], task_id: str) -> dict[str, Any]:
    parent = SCHEDULER.validate_plan(parent)
    task = next((item for item in parent["tasks"] if item["id"] == task_id), None)
    if task is None:
        raise ValueError(f"task is absent from immutable plan: {task_id}")
    selected = copy.deepcopy(task)
    selected["depends_on"] = []
    semantic = copy.deepcopy(parent)
    semantic["tasks"] = [selected]
    semantic["budgets"] = {
        "max_steps": 1,
        "max_failures": max(1, min(parent["budgets"]["max_failures"], 1)),
        "max_tokens": min(parent["budgets"]["max_tokens"], selected["max_tokens"]),
    }
    semantic.pop("fingerprint", None)
    value = {**semantic, "fingerprint": RUNTIME.digest(semantic)}
    return RUNTIME.validate_plan(value)


def dispatch(
    repository: Path,
    plan_path: Path,
    state_path: Path,
    expected_revision: int,
    worker: str,
    lease_seconds: int,
    now: int,
) -> dict[str, Any]:
    repository = repository.resolve()
    plan_path = bounded(repository, plan_path)
    state_path = bounded(repository, state_path)
    plan = SCHEDULER.validate_plan(SCHEDULER.read_toon(plan_path))
    before = SCHEDULER.validate_state(SCHEDULER.read_toon(state_path))
    if before["plan_fingerprint"] != plan["fingerprint"]:
        raise ValueError("scheduler and immutable plan fingerprints differ")
    if SCHEDULER.state_task_definitions(before) != SCHEDULER.plan_task_definitions(plan):
        raise ValueError("scheduler task definitions differ from immutable plan")
    if not before["ready"]:
        raise ValueError("no dependency-ready task")
    ready = before["ready"][0]
    planned = next(item for item in plan["tasks"] if item["id"] == ready)
    claimed = SCHEDULER.mutate(
        state_path,
        expected_revision,
        now,
        SCHEDULER.claim_action(worker, lease_seconds, planned["context"]["fingerprint"], now),
    )
    claimed_task = next(item for item in claimed["tasks"] if item["id"] == ready)
    if claimed_task["status"] != "leased":
        raise ValueError("scheduler task attempt budget is exhausted")
    lease = claimed_task["lease"]
    runtime_run_id = f"{claimed['run_id']}--{ready}--{claimed_task['attempts']}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", runtime_run_id):
        raise ValueError("derived runtime run id is unsafe")
    dispatch_root = bounded(repository, repository / "_ai_sdlc/scheduler" / claimed["run_id"] / "dispatches")
    dispatch_root.mkdir(parents=True, exist_ok=True)
    dispatch_path = dispatch_root / f"{lease['nonce']}.toon"
    task_plan = subplan(plan, ready)
    semantic = {
        "schema": DISPATCH_SCHEMA,
        "scheduler_run_id": claimed["run_id"],
        "scheduler_plan_fingerprint": claimed["plan_fingerprint"],
        "scheduler_state": str(state_path.resolve().relative_to(repository)),
        "scheduler_revision": claimed["revision"],
        "task_id": ready,
        "worker": worker,
        "lease_nonce": lease["nonce"],
        "lease_expires_at": lease["expires_at"],
        "context_fingerprint": planned["context"]["fingerprint"],
        "runtime_run_id": runtime_run_id,
        "runtime_plan_fingerprint": task_plan["fingerprint"],
    }
    record = {**semantic, "fingerprint": SCHEDULER.digest(semantic)}
    SCHEDULER.atomic_write(dispatch_path, record)
    descriptor, temporary = tempfile.mkstemp(prefix="runtime-plan-", suffix=".toon", dir=dispatch_root)
    os.close(descriptor)
    temporary_path = Path(temporary)
    try:
        SCHEDULER.atomic_write(temporary_path, task_plan)
        runs_root = bounded(repository, repository / "_ai_sdlc/runs")
        runtime_state = RUNTIME.start_run(repository, runs_root, runtime_run_id, temporary_path)
        run_dir = runs_root / runtime_run_id
        runtime_plan, runtime_state, _recovered = RUNTIME.load_run(run_dir, runtime_run_id)
        runtime_task = RUNTIME.task_row(runtime_state, ready)
        assert runtime_task is not None
        key = RUNTIME.task_idempotency(runtime_plan, runtime_task, 1)
        runtime_state = RUNTIME.append_event(
            run_dir, runtime_state, runtime_plan, "task-started",
            task_id=ready, idempotency_key=key,
            payload={"operation": runtime_task["operation"]},
        )
    finally:
        temporary_path.unlink(missing_ok=True)
    return {"schema": "ai-sdlc-scheduler-worker-result/v1", "action": "dispatch", "dispatch": record, "scheduler": claimed, "runtime": runtime_state}


def commit(repository: Path, dispatch_path: Path, state_path: Path, expected_revision: int, now: int) -> dict[str, Any]:
    repository = repository.resolve()
    dispatch_path = bounded(repository, dispatch_path)
    state_path = bounded(repository, state_path)
    record = SCHEDULER.read_toon(dispatch_path)
    if not isinstance(record, dict) or record.get("schema") != DISPATCH_SCHEMA:
        raise ValueError("scheduler dispatch schema mismatch")
    semantic = copy.deepcopy(record)
    claimed = semantic.pop("fingerprint", None)
    if claimed != SCHEDULER.digest(semantic):
        raise ValueError("scheduler dispatch fingerprint mismatch")
    state_before = SCHEDULER.validate_state(SCHEDULER.read_toon(state_path))
    relative_state = str(state_path.relative_to(repository))
    if (
        record.get("scheduler_state") != relative_state
        or record.get("scheduler_run_id") != state_before["run_id"]
        or record.get("scheduler_plan_fingerprint") != state_before["plan_fingerprint"]
        or record.get("scheduler_revision") != expected_revision
        or state_before["revision"] != expected_revision
    ):
        raise ValueError("dispatch is not bound to the current scheduler state")
    scheduled_task = SCHEDULER.task_row(state_before, record["task_id"])
    if scheduled_task["context_fingerprint"] != record["context_fingerprint"]:
        raise ValueError("dispatch context differs from scheduler state")
    run_dir = bounded(repository, repository / "_ai_sdlc/runs" / record["runtime_run_id"])
    runtime_plan, runtime_state, recovered = RUNTIME.load_run(run_dir, record["runtime_run_id"])
    if runtime_plan["fingerprint"] != record["runtime_plan_fingerprint"]:
        raise ValueError("dispatch runtime plan fingerprint mismatch")
    task = RUNTIME.task_row(runtime_state, record["task_id"])
    if recovered or task is None or task["status"] not in {"succeeded", "failed", "blocked"} or task["protocol_phase"] != "result":
        raise ValueError("runtime task is not durably terminal")
    scheduler_state = SCHEDULER.mutate(
        state_path, expected_revision, now,
        SCHEDULER.terminal_action(
            record["task_id"], record["worker"], record["lease_nonce"],
            task["status"], task["result_fingerprint"], now,
        ),
    )
    return {"schema": "ai-sdlc-scheduler-worker-result/v1", "action": "commit", "dispatch": record, "scheduler": scheduler_state, "runtime": runtime_state}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--dispatch", action="store_true")
    actions.add_argument("--commit", action="store_true")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--dispatch-record", type=Path)
    parser.add_argument("--expected-revision", type=int, required=True)
    parser.add_argument("--worker")
    parser.add_argument("--lease-seconds", type=int, default=300)
    parser.add_argument("--now", type=int, required=True)
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: scheduler worker cannot mutate feature lifecycle state", file=sys.stderr)
        return 1
    try:
        if args.dispatch:
            if args.plan is None or not args.worker:
                raise ValueError("dispatch requires --plan and --worker")
            result = dispatch(args.repository, args.plan, args.state, args.expected_revision, args.worker, args.lease_seconds, args.now)
        else:
            if args.dispatch_record is None:
                raise ValueError("commit requires --dispatch-record")
            result = commit(args.repository, args.dispatch_record, args.state, args.expected_revision, args.now)
        sys.stdout.write(TOON.encode_toon(result))
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
