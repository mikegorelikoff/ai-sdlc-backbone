#!/usr/bin/env python3
"""Deterministic lease scheduler for AI SDLC v2 run plans."""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import importlib.util
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon  # noqa: E402

_RUNTIME_PATH = Path(__file__).resolve().parents[2] / "ai-sdlc-runtime" / "scripts/runtime.py"
_RUNTIME_SPEC = importlib.util.spec_from_file_location("ai_sdlc_scheduler_runtime", _RUNTIME_PATH)
if _RUNTIME_SPEC is None or _RUNTIME_SPEC.loader is None:
    raise RuntimeError("cannot load sibling ai-sdlc-runtime")
runtime = importlib.util.module_from_spec(_RUNTIME_SPEC)
_RUNTIME_SPEC.loader.exec_module(runtime)

SCHEMA = "ai-sdlc-scheduler-state/v1"
EVENT_SCHEMA = "ai-sdlc-scheduler-event/v1"
ZERO_HASH = "0" * 64
TERMINAL = {"succeeded", "failed", "blocked"}


def digest(value: Any) -> str:
    text = value if isinstance(value, str) else toon.encode_toon(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fingerprinted(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("fingerprint", None)
    result["fingerprint"] = digest(result)
    return result


def read_toon(path: Path) -> Any:
    try:
        return toon.loads(path.read_text(encoding="utf-8"))
    except (OSError, toon.ToonDecodeError) as exc:
        raise ValueError(f"cannot read TOON {path}: {exc}") from exc


def atomic_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(toon.encode_toon(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(state_path: Path) -> Iterator[None]:
    lock_path = state_path.with_suffix(state_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def validate_plan(plan: Any) -> dict[str, Any]:
    """Delegate the immutable plan contract to the canonical runtime validator."""
    return runtime.validate_plan(plan)


def plan_task_definitions(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "id": task["id"],
        "depends_on": list(task["depends_on"]),
        "context_fingerprint": task["context"]["fingerprint"],
        "step_fingerprint": task["step_fingerprint"],
        "max_attempts": task["max_attempts"],
    } for task in plan["tasks"]]


def state_task_definitions(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "id": task["id"],
        "depends_on": list(task["depends_on"]),
        "context_fingerprint": task["context_fingerprint"],
        "step_fingerprint": task["step_fingerprint"],
        "max_attempts": task["max_attempts"],
    } for task in state["tasks"]]


def project(state: dict[str, Any]) -> dict[str, Any]:
    succeeded = {item["id"] for item in state["tasks"] if item["status"] == "succeeded"}
    state["ready"] = sorted(
        task["id"] for task in state["tasks"]
        if task["status"] == "pending" and set(task["depends_on"]) <= succeeded
    )
    if all(task["status"] == "succeeded" for task in state["tasks"]):
        state["status"] = "completed"
        state["ready"] = []
    elif any(task["status"] in {"failed", "blocked"} for task in state["tasks"]):
        state["status"] = "blocked"
    else:
        state["status"] = "running"
    return fingerprinted(state)


def append_event(state: dict[str, Any], kind: str, task_id: str, payload: dict[str, Any]) -> None:
    previous = state["event_fingerprint"]
    event = {
        "schema": EVENT_SCHEMA,
        "seq": len(state["events"]) + 1,
        "type": kind,
        "task_id": task_id,
        "payload": copy.deepcopy(payload),
        "previous": previous,
    }
    event["fingerprint"] = digest(event)
    state["events"].append(event)
    state["event_fingerprint"] = event["fingerprint"]


def initial_state(run_id: str, plan: dict[str, Any], now: int, max_parallelism: int = 1) -> dict[str, Any]:
    if max_parallelism < 1:
        raise ValueError("scheduler parallelism must be positive")
    tasks = [{
        **definition,
        "status": "pending",
        "attempts": 0,
        "lease": {},
        "terminal": {},
    } for definition in plan_task_definitions(plan)]
    state = {
        "schema": SCHEMA,
        "run_id": run_id,
        "plan_fingerprint": plan["fingerprint"],
        "max_parallelism": max_parallelism,
        "revision": 0,
        "status": "running",
        "ready": [],
        "tasks": tasks,
        "events": [],
        "event_fingerprint": ZERO_HASH,
        "fingerprint": "",
    }
    append_event(state, "scheduler-created", "", {
        "run_id": run_id,
        "plan_fingerprint": plan["fingerprint"],
        "max_parallelism": max_parallelism,
        "tasks": state_task_definitions(state),
    })
    return project(state)


def validate_state(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict) or state.get("schema") != SCHEMA:
        raise ValueError("scheduler state schema mismatch")
    claimed = state.get("fingerprint")
    semantic = copy.deepcopy(state)
    semantic.pop("fingerprint", None)
    if claimed != digest(semantic):
        raise ValueError("scheduler state fingerprint mismatch")
    previous = ZERO_HASH
    for index, event in enumerate(state.get("events", []), 1):
        claimed_event = event.get("fingerprint")
        semantic_event = copy.deepcopy(event)
        semantic_event.pop("fingerprint", None)
        if event.get("seq") != index or event.get("previous") != previous or claimed_event != digest(semantic_event):
            raise ValueError("scheduler event chain mismatch")
        previous = claimed_event
    if state.get("event_fingerprint") != previous:
        raise ValueError("scheduler event head mismatch")
    replayed = replay_state(state)
    if replayed != state:
        raise ValueError("scheduler projection differs from event replay")
    return copy.deepcopy(state)


def replay_state(state: dict[str, Any]) -> dict[str, Any]:
    if not state.get("events") or state["events"][0].get("type") != "scheduler-created":
        raise ValueError("scheduler creation event is invalid")
    created = state["events"][0].get("payload")
    if not isinstance(created, dict):
        raise ValueError("scheduler creation event is invalid")
    definitions = created.get("tasks")
    if not isinstance(definitions, list):
        raise ValueError("scheduler creation event is invalid")
    tasks = [{
        "id": task["id"],
        "depends_on": list(task["depends_on"]),
        "context_fingerprint": task["context_fingerprint"],
        "step_fingerprint": task["step_fingerprint"],
        "max_attempts": task["max_attempts"],
        "status": "pending",
        "attempts": 0,
        "lease": {},
        "terminal": {},
    } for task in definitions]
    replayed = {
        "schema": SCHEMA,
        "run_id": created.get("run_id"),
        "plan_fingerprint": created.get("plan_fingerprint"),
        "max_parallelism": created.get("max_parallelism"),
        "revision": 0,
        "status": "running",
        "ready": [],
        "tasks": tasks,
        "events": copy.deepcopy(state["events"]),
        "event_fingerprint": state["event_fingerprint"],
        "fingerprint": "",
    }
    for index, event in enumerate(replayed["events"]):
        kind = event["type"]
        payload = event["payload"]
        if index == 0:
            expected = {
                "run_id": replayed["run_id"],
                "plan_fingerprint": replayed["plan_fingerprint"],
                "max_parallelism": replayed["max_parallelism"],
                "tasks": definitions,
            }
            if kind != "scheduler-created" or payload != expected:
                raise ValueError("scheduler creation event is invalid")
            continue
        replayed["revision"] += 1
        if kind == "task-leased":
            task = task_row(replayed, event["task_id"])
            if task["status"] != "pending" or payload["attempt"] != task["attempts"] + 1:
                raise ValueError("scheduler lease event transition is invalid")
            task["status"] = "leased"
            task["attempts"] = payload["attempt"]
            task["lease"] = {
                "worker": payload["worker"], "nonce": payload["nonce"],
                "issued_at": payload["issued_at"], "expires_at": payload["expires_at"],
            }
        elif kind == "scheduler-recovered":
            expired = payload.get("expired")
            if not isinstance(expired, list) or not expired:
                raise ValueError("scheduler recovery event is invalid")
            for task_id in expired:
                task = task_row(replayed, task_id)
                if task["status"] != "leased" or task["lease"]["expires_at"] > payload["now"]:
                    raise ValueError("scheduler recovery event transition is invalid")
                task["status"] = "pending"
                task["lease"] = {}
        elif kind == "lease-heartbeat":
            task = task_row(replayed, event["task_id"])
            if (
                task["status"] != "leased"
                or task["lease"]["worker"] != payload.get("worker")
                or task["lease"]["nonce"] != payload.get("nonce")
                or task["lease"]["expires_at"] <= payload.get("now", -1)
                or payload.get("expires_at", 0) <= task["lease"]["expires_at"]
            ):
                raise ValueError("scheduler heartbeat event transition is invalid")
            task["lease"]["expires_at"] = payload["expires_at"]
        elif kind == "task-attempts-exhausted":
            task = task_row(replayed, event["task_id"])
            if task["status"] != "pending" or task["attempts"] != task["max_attempts"]:
                raise ValueError("scheduler attempt exhaustion transition is invalid")
            task["status"] = "blocked"
            task["terminal"] = {"outcome": "blocked", "result_fingerprint": ""}
        elif kind == "task-terminal":
            task = task_row(replayed, event["task_id"])
            if task["status"] != "leased":
                raise ValueError("scheduler terminal event transition is invalid")
            task["status"] = payload["outcome"]
            task["terminal"] = copy.deepcopy(payload)
            task["lease"] = {}
        else:
            raise ValueError(f"unknown scheduler event type: {kind}")
        project(replayed)
    return project(replayed)


def mutate(path: Path, expected_revision: int, now: int, action) -> dict[str, Any]:
    with locked(path):
        state = validate_state(read_toon(path))
        if state["revision"] != expected_revision:
            raise ValueError(f"scheduler revision mismatch: expected {expected_revision}; actual {state['revision']}")
        action(state)
        state["revision"] += 1
        state = project(state)
        atomic_write(path, state)
        return state


def task_row(state: dict[str, Any], task_id: str) -> dict[str, Any]:
    task = next((item for item in state["tasks"] if item["id"] == task_id), None)
    if task is None:
        raise ValueError(f"unknown scheduler task: {task_id}")
    return task


def claim_action(worker: str, lease_seconds: int, context_fingerprint: str, now: int):
    def action(state: dict[str, Any]) -> None:
        active = sum(task["status"] == "leased" for task in state["tasks"])
        if active >= state["max_parallelism"]:
            raise ValueError("scheduler parallelism limit reached")
        if not state["ready"]:
            raise ValueError("no dependency-ready task")
        task = task_row(state, state["ready"][0])
        if task["context_fingerprint"] != context_fingerprint:
            raise ValueError("stale context fingerprint")
        if task["attempts"] >= task["max_attempts"]:
            task["status"] = "blocked"
            task["terminal"] = {"outcome": "blocked", "result_fingerprint": ""}
            append_event(state, "task-attempts-exhausted", task["id"], {})
            return
        attempt = task["attempts"] + 1
        nonce = digest({"run": state["run_id"], "task": task["id"], "worker": worker, "attempt": attempt, "revision": state["revision"]})
        task["status"] = "leased"
        task["attempts"] = attempt
        task["lease"] = {"worker": worker, "nonce": nonce, "issued_at": now, "expires_at": now + lease_seconds}
        append_event(state, "task-leased", task["id"], {"attempt": attempt, "worker": worker, "nonce": nonce, "issued_at": now, "expires_at": now + lease_seconds})
    return action


def heartbeat_action(task_id: str, worker: str, nonce: str, lease_seconds: int, now: int):
    def action(state: dict[str, Any]) -> None:
        task = task_row(state, task_id)
        lease = task["lease"]
        if task["status"] != "leased" or lease.get("worker") != worker or lease.get("nonce") != nonce:
            raise ValueError("stale or foreign lease cannot heartbeat")
        if lease["expires_at"] <= now:
            raise ValueError("expired lease cannot heartbeat before recovery")
        expires_at = now + lease_seconds
        if expires_at <= lease["expires_at"]:
            raise ValueError("heartbeat must extend lease expiry")
        lease["expires_at"] = expires_at
        append_event(state, "lease-heartbeat", task_id, {
            "worker": worker, "nonce": nonce, "now": now, "expires_at": expires_at,
        })
    return action


def recovery_action(now: int):
    def action(state: dict[str, Any]) -> None:
        expired = sorted(
            task["id"] for task in state["tasks"]
            if task["status"] == "leased" and task["lease"]["expires_at"] <= now
        )
        if not expired:
            raise ValueError("no expired scheduler leases")
        for task_id in expired:
            task = task_row(state, task_id)
            task["status"] = "pending"
            task["lease"] = {}
        append_event(state, "scheduler-recovered", "", {"now": now, "expired": expired})
    return action


def terminal_action(task_id: str, worker: str, nonce: str, outcome: str, result_fingerprint: str, now: int):
    def action(state: dict[str, Any]) -> None:
        task = task_row(state, task_id)
        lease = task["lease"]
        if task["status"] != "leased" or lease.get("worker") != worker or lease.get("nonce") != nonce:
            raise ValueError("stale or foreign lease cannot commit")
        if lease["expires_at"] <= now:
            raise ValueError("expired lease cannot commit before recovery")
        if outcome not in TERMINAL:
            raise ValueError("terminal outcome is invalid")
        if outcome == "succeeded" and not re.fullmatch(r"[a-f0-9]{64}", result_fingerprint):
            raise ValueError("successful result requires a SHA-256 fingerprint")
        task["status"] = outcome
        task["terminal"] = {"outcome": outcome, "result_fingerprint": result_fingerprint}
        task["lease"] = {}
        append_event(state, "task-terminal", task_id, {"outcome": outcome, "result_fingerprint": result_fingerprint})
    return action


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--quick-flow", action="store_true")
    root.add_argument("--full-flow", action="store_true")
    root.add_argument("--state-check", action="store_true")
    root.add_argument("--begin-state", action="store_true")
    root.add_argument("--complete-state", action="store_true")
    sub = root.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--plan", type=Path, required=True)
    create.add_argument("--state", type=Path, required=True)
    create.add_argument("--run-id", required=True)
    create.add_argument("--now", type=int, required=True)
    create.add_argument("--max-parallelism", type=int, default=1)
    for name in ("status", "replay", "recover"):
        item = sub.add_parser(name)
        item.add_argument("--state", type=Path, required=True)
        if name == "recover":
            item.add_argument("--expected-revision", type=int, required=True)
            item.add_argument("--now", type=int, required=True)
    claim = sub.add_parser("claim")
    claim.add_argument("--state", type=Path, required=True)
    claim.add_argument("--expected-revision", type=int, required=True)
    claim.add_argument("--worker", required=True)
    claim.add_argument("--lease-seconds", type=int, required=True)
    claim.add_argument("--context-fingerprint", required=True)
    claim.add_argument("--now", type=int, required=True)
    heartbeat = sub.add_parser("heartbeat")
    heartbeat.add_argument("--state", type=Path, required=True)
    heartbeat.add_argument("--expected-revision", type=int, required=True)
    heartbeat.add_argument("--task", required=True)
    heartbeat.add_argument("--worker", required=True)
    heartbeat.add_argument("--nonce", required=True)
    heartbeat.add_argument("--lease-seconds", type=int, required=True)
    heartbeat.add_argument("--now", type=int, required=True)
    complete = sub.add_parser("complete")
    complete.add_argument("--state", type=Path, required=True)
    complete.add_argument("--expected-revision", type=int, required=True)
    complete.add_argument("--task", required=True)
    complete.add_argument("--worker", required=True)
    complete.add_argument("--nonce", required=True)
    complete.add_argument("--outcome", choices=sorted(TERMINAL), required=True)
    complete.add_argument("--result-fingerprint", default="")
    complete.add_argument("--now", type=int, required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: scheduler cannot mutate feature lifecycle state", file=sys.stderr)
        return 1
    try:
        if args.command == "create":
            plan = validate_plan(read_toon(args.plan))
            if args.state.exists():
                raise ValueError("scheduler state already exists")
            state = initial_state(args.run_id, plan, args.now, args.max_parallelism)
            atomic_write(args.state, state)
        elif args.command in {"status", "replay"}:
            state = validate_state(read_toon(args.state))
        elif args.command == "recover":
            state = mutate(args.state, args.expected_revision, args.now, recovery_action(args.now))
        elif args.command == "claim":
            if args.lease_seconds < 1:
                raise ValueError("lease duration must be positive")
            state = mutate(args.state, args.expected_revision, args.now, claim_action(args.worker, args.lease_seconds, args.context_fingerprint, args.now))
        elif args.command == "heartbeat":
            if args.lease_seconds < 1:
                raise ValueError("lease duration must be positive")
            state = mutate(
                args.state, args.expected_revision, args.now,
                heartbeat_action(args.task, args.worker, args.nonce, args.lease_seconds, args.now),
            )
        else:
            state = mutate(args.state, args.expected_revision, args.now, terminal_action(args.task, args.worker, args.nonce, args.outcome, args.result_fingerprint, args.now))
        sys.stdout.write(toon.encode_toon(state))
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
