#!/usr/bin/env python3
"""Run a bounded, journaled, resumable v2 skill-step state machine."""

from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402
from ai_sdlc_safe_io import bounded_path, ensure_directory  # noqa: E402
from ai_sdlc_step_context import validate_step_context_pack  # noqa: E402


PLAN_SCHEMA = "ai-sdlc-run-plan/v2"
STEP_CARD_SCHEMA = "ai-sdlc-step-card/v1"
EVENT_SCHEMA = "ai-sdlc-run-event/v2"
STATE_SCHEMA = "ai-sdlc-run-state/v2"
RESULT_SCHEMA = "ai-sdlc-run-result/v2"
PLAN_FIELDS = {
    "schema",
    "skill",
    "entrypoint",
    "role",
    "action",
    "manifest_fingerprint",
    "graph_fingerprint",
    "selection_fingerprint",
    "targets",
    "budgets",
    "tasks",
    "fingerprint",
}
BUDGET_FIELDS = {"max_steps", "max_failures", "max_tokens"}
TASK_FIELDS = {
    "id",
    "schema",
    "skill",
    "step_id",
    "path",
    "step_type",
    "status",
    "depends_on",
    "operation",
    "capabilities",
    "side_effect",
    "context",
    "gates",
    "outputs",
    "max_attempts",
    "max_tokens",
    "commit_boundary",
    "on_failure",
    "load",
    "reason",
    "ready",
    "graph_fingerprint",
    "step_fingerprint",
    "idempotency_scope",
}
EVENT_FIELDS = {
    "schema",
    "seq",
    "type",
    "run_id",
    "task_id",
    "attempt",
    "idempotency_key",
    "payload",
    "previous",
    "fingerprint",
}
EVENT_TYPES = {
    "run-started",
    "task-planned",
    "task-started",
    "task-terminal",
    "task-evidence",
    "task-result",
    "task-retry-requested",
    "run-stopped",
}
RESULT_RECORD_FIELDS = {
    "outcome",
    "result_fingerprint",
    "tokens",
    "commit",
    "reason",
}
SIDE_EFFECTS = {"none", "workspace-write", "external-write", "destructive"}
FAILURE_POLICIES = {"block", "retry", "handoff"}
STEP_TYPES = {"analysis", "context", "action", "validation", "handoff"}
LOAD_RULES = {"required", "on-demand", "before-completion"}
ZERO_HASH = "0" * 64


def canonical(value: Any) -> str:
    """Return canonical newline-terminated TOON."""
    return toon_codec.encode_toon(value)


def digest(value: Any) -> str:
    """Return one stable SHA-256 identity."""
    text = value if isinstance(value, str) else canonical(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def valid_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-f0-9]{64}", value))


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def validate_task_record(task: dict[str, Any], record: Any) -> dict[str, Any]:
    """Validate one task result without coercing replayed journal values."""
    if not isinstance(record, dict) or set(record) != RESULT_RECORD_FIELDS:
        raise ValueError("task result record fields are invalid")
    if record["outcome"] not in {"succeeded", "failed", "blocked"}:
        raise ValueError("task result outcome is invalid")
    if (
        not isinstance(record["result_fingerprint"], str)
        or not isinstance(record["commit"], str)
        or not isinstance(record["reason"], str)
        or not isinstance(record["tokens"], int)
        or isinstance(record["tokens"], bool)
    ):
        raise ValueError("task result record types are invalid")
    if record["result_fingerprint"] and not valid_hash(
        record["result_fingerprint"]
    ):
        raise ValueError("task result fingerprint must be empty or a SHA-256 value")
    if record["outcome"] == "succeeded":
        if not valid_hash(record["result_fingerprint"]):
            raise ValueError("successful task requires a result fingerprint")
        if task["commit_boundary"] == "after-step" and not re.fullmatch(
            r"[a-f0-9]{7,64}",
            record["commit"],
        ):
            raise ValueError(
                "successful task requires 7-to-64-character hexadecimal "
                "commit evidence"
            )
    if record["tokens"] < 0 or record["tokens"] > task["max_tokens"]:
        raise ValueError(f"task tokens must be 0..{task['max_tokens']}")
    return copy.deepcopy(record)


def completion_fingerprint(
    record: dict[str, Any],
    evidence: list[str],
    effect_receipt: str,
) -> str:
    """Bind every replay-sensitive completion field to one stable identity."""
    return digest(
        {
            "schema": "ai-sdlc-task-completion/v1",
            "record": record,
            "evidence": evidence,
            "effect_receipt": effect_receipt,
        }
    )


def atomic_toon(path: Path, value: Any) -> None:
    """Atomically replace one canonical TOON projection."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(toon_codec.encode_toon(value))
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_toon(path: Path, label: str) -> Any:
    try:
        return toon_codec.loads(path.read_text(encoding="utf-8"))
    except (OSError, toon_codec.ToonDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc


def fingerprinted(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("fingerprint", None)
    result["fingerprint"] = digest(result)
    return result


def validate_plan(value: Any) -> dict[str, Any]:
    """Validate one immutable run v2 plan without coercion."""
    if not isinstance(value, dict):
        raise ValueError("run plan must be a TOON mapping")
    received = value.get("schema")
    if received != PLAN_SCHEMA:
        raise ValueError(
            f"RUN_SCHEMA_MISMATCH: received {received!r}; expected {PLAN_SCHEMA}; "
            "recompile with ai_sdlc_steps.py --emit-plan"
        )
    if set(value) != PLAN_FIELDS:
        raise ValueError("run plan fields do not match the v2 contract")
    for field in (
        "manifest_fingerprint",
        "graph_fingerprint",
        "selection_fingerprint",
        "fingerprint",
    ):
        if not valid_hash(value[field]):
            raise ValueError(f"run plan {field} must be a SHA-256 value")
    semantic = dict(value)
    claimed = semantic.pop("fingerprint")
    if digest(semantic) != claimed:
        raise ValueError("run plan fingerprint mismatch")
    if not isinstance(value["skill"], str) or not value["skill"]:
        raise ValueError("run plan skill is required")
    if not isinstance(value["entrypoint"], str) or not value["entrypoint"]:
        raise ValueError("run plan entrypoint is required")
    for field in ("role", "action"):
        if not isinstance(value[field], str):
            raise ValueError(f"run plan {field} must be a string")
    if not unique_strings(value["targets"], nonempty=True):
        raise ValueError("run plan targets must be unique and non-empty")
    budgets = value["budgets"]
    if not isinstance(budgets, dict) or set(budgets) != BUDGET_FIELDS:
        raise ValueError("run plan budgets fields are invalid")
    for field in BUDGET_FIELDS:
        amount = budgets[field]
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 1:
            raise ValueError(f"run plan budgets.{field} must be a positive integer")

    tasks = value["tasks"]
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("run plan tasks must be non-empty")
    ids: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, task in enumerate(tasks):
        prefix = f"run plan tasks[{index}]"
        if not isinstance(task, dict) or set(task) != TASK_FIELDS:
            raise ValueError(f"{prefix} fields are invalid")
        task_id = task["id"]
        if not isinstance(task_id, str) or not task_id or task_id in ids:
            raise ValueError(f"{prefix}.id must be a unique string")
        ids.add(task_id)
        if task["schema"] != STEP_CARD_SCHEMA:
            raise ValueError(f"{prefix}.schema must be {STEP_CARD_SCHEMA}")
        if (
            not isinstance(task["skill"], str)
            or not re.fullmatch(
                r"ai-sdlc-[a-z0-9]+(?:-[a-z0-9]+)*",
                task["skill"],
            )
            or (
                not str(value["skill"]).startswith("workflow:")
                and task["skill"] != value["skill"]
            )
        ):
            raise ValueError(f"{prefix}.skill is incompatible with plan skill")
        if (
            not isinstance(task["step_id"], str)
            or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", task["step_id"])
        ):
            raise ValueError(f"{prefix}.step_id is invalid")
        if (
            not isinstance(task["path"], str)
            or not re.fullmatch(
                r"steps/[a-z0-9][a-z0-9-]*\.md",
                task["path"],
            )
        ):
            raise ValueError(f"{prefix}.path is invalid")
        if task["step_type"] not in STEP_TYPES:
            raise ValueError(f"{prefix}.step_type is invalid")
        if task["status"] != "pending":
            raise ValueError(f"{prefix}.status must be pending in a new run")
        if not unique_strings(task["depends_on"]):
            raise ValueError(f"{prefix}.depends_on must be a unique string array")
        for field in ("capabilities", "gates", "outputs"):
            if not unique_strings(task[field], nonempty=True):
                raise ValueError(f"{prefix}.{field} must be unique and non-empty")
        if not isinstance(task["operation"], str) or not task["operation"]:
            raise ValueError(f"{prefix}.operation must be a non-empty string")
        if task["side_effect"] not in SIDE_EFFECTS:
            raise ValueError(f"{prefix}.side_effect is invalid")
        if task["on_failure"] not in FAILURE_POLICIES:
            raise ValueError(f"{prefix}.on_failure is invalid")
        if task["commit_boundary"] not in {"none", "after-step"}:
            raise ValueError(f"{prefix}.commit_boundary is invalid")
        if task["load"] not in LOAD_RULES:
            raise ValueError(f"{prefix}.load is invalid")
        if not isinstance(task["reason"], str) or not task["reason"]:
            raise ValueError(f"{prefix}.reason is required")
        if task["ready"] is not True:
            raise ValueError(f"{prefix}.ready must be true")
        if (
            not valid_hash(task["graph_fingerprint"])
            or (
                not str(value["skill"]).startswith("workflow:")
                and task["graph_fingerprint"] != value["graph_fingerprint"]
            )
        ):
            raise ValueError(f"{prefix}.graph_fingerprint differs from the plan")
        for field in ("max_attempts", "max_tokens"):
            amount = task[field]
            if not isinstance(amount, int) or isinstance(amount, bool) or amount < 1:
                raise ValueError(f"{prefix}.{field} must be a positive integer")
        if not valid_hash(task["step_fingerprint"]):
            raise ValueError(f"{prefix}.step_fingerprint must be a SHA-256 value")
        expected_scope = (
            f"{task['skill']}:{task['step_id']}:{task['graph_fingerprint']}"
        )
        if task["idempotency_scope"] != expected_scope:
            raise ValueError(f"{prefix}.idempotency_scope is invalid")
        try:
            validate_step_context_pack(
                task["context"],
                expected_skill=task["skill"],
                expected_step_id=task["step_id"],
                require_sufficient=True,
            )
        except ValueError as exc:
            raise ValueError(f"{prefix}.context failed validation: {exc}") from exc
        normalized.append(copy.deepcopy(task))

    for task in normalized:
        unknown = sorted(set(task["depends_on"]) - ids)
        if unknown:
            raise ValueError(
                f"run plan task {task['id']} has unknown dependencies: "
                + ", ".join(unknown)
            )
        if task["id"] in task["depends_on"]:
            raise ValueError(f"run plan task {task['id']} depends on itself")
    pending = {task["id"]: set(task["depends_on"]) for task in normalized}
    resolved: set[str] = set()
    while pending:
        ready = sorted(
            task_id
            for task_id, dependencies in pending.items()
            if dependencies <= resolved
        )
        if not ready:
            raise ValueError(
                "run plan dependency cycle contains " + ", ".join(sorted(pending))
            )
        for task_id in ready:
            resolved.add(task_id)
            pending.pop(task_id)
    return copy.deepcopy(value)


def task_idempotency(plan: dict[str, Any], task: dict[str, Any], attempt: int) -> str:
    return digest(
        {
            "schema": "ai-sdlc-idempotency-key/v1",
            "plan": plan["fingerprint"],
            "task": task["id"],
            "step": task["step_fingerprint"],
            "context": task["context"]["fingerprint"],
            "scope": task["idempotency_scope"],
            "attempt": attempt,
        }
    )


def initial_state(run_id: str, plan: dict[str, Any]) -> dict[str, Any]:
    tasks = []
    for task in plan["tasks"]:
        tasks.append(
            {
                **copy.deepcopy(task),
                "attempts": 0,
                "idempotency_key": "",
                "evidence": [],
                "effect_receipt": "",
                "result_fingerprint": "",
                "protocol_phase": "unplanned",
                "terminal_outcome": "",
                "completion_fingerprint": "",
                "last_record": {},
                "reason": "",
            }
        )
    state = {
        "schema": STATE_SCHEMA,
        "run_id": run_id,
        "plan_fingerprint": plan["fingerprint"],
        "graph_fingerprint": plan["graph_fingerprint"],
        "sequence": 0,
        "event_fingerprint": ZERO_HASH,
        "status": "running",
        "stop_reason": "",
        "running_task": "",
        "ready_tasks": [],
        "budgets": {
            **copy.deepcopy(plan["budgets"]),
            "used_steps": 0,
            "used_failures": 0,
            "used_tokens": 0,
        },
        "tasks": tasks,
        "fingerprint": "",
    }
    return refresh_state(state)


def task_row(state: dict[str, Any], task_id: str) -> dict[str, Any] | None:
    return next((task for task in state["tasks"] if task["id"] == task_id), None)


def refresh_state(state: dict[str, Any]) -> dict[str, Any]:
    """Recompute ready tasks, terminal status, and state fingerprint."""
    succeeded = {
        task["id"] for task in state["tasks"] if task["status"] == "succeeded"
    }
    if all(task["status"] == "succeeded" for task in state["tasks"]):
        state["status"] = "completed"
        state["stop_reason"] = ""
        state["running_task"] = ""
        state["ready_tasks"] = []
    elif state["running_task"]:
        state["ready_tasks"] = []
    elif state["status"] == "running":
        state["ready_tasks"] = sorted(
            task["id"]
            for task in state["tasks"]
            if task["status"] == "pending"
            and set(task["depends_on"]) <= succeeded
        )
        if not state["ready_tasks"]:
            state["status"] = "paused"
            state["stop_reason"] = "dependency-blocked"
    else:
        state["ready_tasks"] = []
    return fingerprinted(state)


def apply_event(
    state: dict[str, Any],
    event: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    """Apply one already-validated event to a replay projection."""
    state = copy.deepcopy(state)
    event_type = event["type"]
    task = task_row(state, event["task_id"]) if event["task_id"] else None
    payload = event["payload"]
    if event_type == "run-started":
        if (
            event["task_id"]
            or event["attempt"] != 0
            or event["idempotency_key"]
            or set(payload) != {"plan_fingerprint", "graph_fingerprint"}
            or payload.get("plan_fingerprint") != plan["fingerprint"]
            or payload.get("graph_fingerprint") != plan["graph_fingerprint"]
        ):
            raise ValueError("run-started identity does not match the immutable plan")
    elif event_type == "task-planned":
        planned = next(
            (item for item in plan["tasks"] if item["id"] == event["task_id"]),
            None,
        )
        if (
            task is None
            or planned is None
            or task["protocol_phase"] != "unplanned"
            or event["attempt"] != 0
            or event["idempotency_key"]
            or set(payload)
            != {
                "step_id",
                "step_fingerprint",
                "context_fingerprint",
                "idempotency_scope",
                "side_effect",
            }
            or payload.get("step_id") != planned["step_id"]
            or payload.get("step_fingerprint") != planned["step_fingerprint"]
            or payload.get("context_fingerprint")
            != planned["context"]["fingerprint"]
            or payload.get("idempotency_scope")
            != planned["idempotency_scope"]
            or payload.get("side_effect") != planned["side_effect"]
        ):
            raise ValueError(f"illegal task-planned event for {event['task_id']}")
        task["protocol_phase"] = "planned"
    elif event_type == "task-started":
        if (
            task is None
            or task["status"] != "pending"
            or task["protocol_phase"] != "planned"
            or state["running_task"]
            or set(payload) != {"operation"}
            or payload.get("operation") != task["operation"]
            or event["attempt"] != int(task["attempts"]) + 1
            or event["idempotency_key"]
            != task_idempotency(plan, task, int(task["attempts"]) + 1)
        ):
            raise ValueError(f"illegal task-started transition for {event['task_id']}")
        task["status"] = "running"
        task["attempts"] += 1
        task["idempotency_key"] = event["idempotency_key"]
        task["protocol_phase"] = "running"
        state["running_task"] = task["id"]
    elif event_type == "task-terminal":
        outcome = payload.get("outcome")
        completion = payload.get("completion_fingerprint")
        if (
            task is None
            or task["status"] != "running"
            or task["protocol_phase"] != "running"
            or state["running_task"] != event["task_id"]
            or event["idempotency_key"] != task["idempotency_key"]
            or event["attempt"] != task["attempts"]
            or set(payload) != {"outcome", "completion_fingerprint"}
            or outcome not in {"succeeded", "failed", "blocked"}
            or not valid_hash(completion)
        ):
            raise ValueError(f"illegal task-terminal transition for {event['task_id']}")
        task["protocol_phase"] = "terminal"
        task["terminal_outcome"] = outcome
        task["completion_fingerprint"] = completion
    elif event_type == "task-evidence":
        if (
            task is None
            or task["status"] != "running"
            or task["protocol_phase"] != "terminal"
            or event["idempotency_key"] != task["idempotency_key"]
            or event["attempt"] != task["attempts"]
            or set(payload) != {"evidence", "effect_receipt"}
            or not unique_strings(payload.get("evidence", []))
            or not isinstance(payload.get("effect_receipt"), str)
        ):
            raise ValueError(f"illegal task-evidence transition for {event['task_id']}")
        task["evidence"] = list(payload["evidence"])
        task["effect_receipt"] = payload["effect_receipt"]
        task["protocol_phase"] = "evidence"
    elif event_type == "task-result":
        if (
            task is None
            or task["status"] != "running"
            or task["protocol_phase"] != "evidence"
            or event["idempotency_key"] != task["idempotency_key"]
            or event["attempt"] != task["attempts"]
            or set(payload) != {"record"}
        ):
            raise ValueError(f"illegal task-result transition for {event['task_id']}")
        record = validate_task_record(task, payload.get("record"))
        outcome = record["outcome"]
        if outcome != task["terminal_outcome"]:
            raise ValueError("task-result outcome differs from task-terminal")
        if (
            completion_fingerprint(
                record,
                task["evidence"],
                task["effect_receipt"],
            )
            != task["completion_fingerprint"]
        ):
            raise ValueError("task completion payload fingerprint mismatch")
        if (
            outcome == "succeeded"
            and task["side_effect"] != "none"
            and not task["effect_receipt"]
        ):
            raise ValueError(
                "successful side-effecting task requires an effect receipt"
            )
        task["status"] = outcome
        task["protocol_phase"] = "result"
        task["last_record"] = copy.deepcopy(record)
        task["result_fingerprint"] = str(record.get("result_fingerprint", ""))
        task["reason"] = str(record.get("reason", ""))
        state["running_task"] = ""
        state["budgets"]["used_steps"] += 1
        state["budgets"]["used_tokens"] += int(record.get("tokens", 0))
        if outcome == "failed":
            state["budgets"]["used_failures"] += 1
        if outcome == "blocked":
            state["status"] = "paused"
            state["stop_reason"] = "task-blocked"
        elif outcome == "failed":
            state["status"] = "paused"
            state["stop_reason"] = "task-failed"
        if state["budgets"]["used_tokens"] >= state["budgets"]["max_tokens"]:
            state["status"] = "stopped"
            state["stop_reason"] = "token-budget-exhausted"
        elif state["budgets"]["used_failures"] >= state["budgets"]["max_failures"]:
            state["status"] = "stopped"
            state["stop_reason"] = "failure-budget-exhausted"
        elif (
            state["budgets"]["used_steps"] >= state["budgets"]["max_steps"]
            and outcome != "succeeded"
        ):
            state["status"] = "stopped"
            state["stop_reason"] = "step-budget-exhausted"
    elif event_type == "task-retry-requested":
        if (
            task is None
            or task["status"] not in {"failed", "blocked"}
            or task["protocol_phase"] != "result"
            or state["status"] != "paused"
            or event["attempt"] != task["attempts"]
            or event["idempotency_key"] != task["idempotency_key"]
            or set(payload) != {"reason"}
            or not isinstance(payload.get("reason"), str)
            or not payload["reason"].strip()
        ):
            raise ValueError(f"illegal retry transition for {event['task_id']}")
        if task["on_failure"] != "retry":
            raise ValueError(f"task {task['id']} does not allow retry")
        if task["attempts"] >= task["max_attempts"]:
            raise ValueError(f"task {task['id']} exhausted max attempts")
        task["status"] = "pending"
        task["reason"] = ""
        task["evidence"] = []
        task["effect_receipt"] = ""
        task["result_fingerprint"] = ""
        task["protocol_phase"] = "planned"
        task["terminal_outcome"] = ""
        task["completion_fingerprint"] = ""
        state["status"] = "running"
        state["stop_reason"] = ""
    elif event_type == "run-stopped":
        if (
            event["task_id"]
            or event["attempt"] != 0
            or event["idempotency_key"]
            or set(payload) != {"reason"}
            or not isinstance(payload.get("reason"), str)
            or not payload["reason"].strip()
            or state["status"] in {"completed", "stopped"}
        ):
            raise ValueError("illegal run-stopped transition")
        state["status"] = "stopped"
        state["stop_reason"] = payload["reason"]
        state["running_task"] = ""
    else:
        raise ValueError(f"unsupported event type: {event_type}")
    state["sequence"] = event["seq"]
    state["event_fingerprint"] = event["fingerprint"]
    return refresh_state(state)


def event_path(journal: Path, sequence: int) -> Path:
    return journal / f"{sequence:06d}.toon"


def validate_event(
    value: Any,
    *,
    expected_sequence: int,
    expected_previous: str,
    run_id: str,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != EVENT_FIELDS:
        raise ValueError(f"journal event {expected_sequence} fields are invalid")
    if value["schema"] != EVENT_SCHEMA:
        raise ValueError(
            f"RUN_SCHEMA_MISMATCH: received {value['schema']!r}; expected {EVENT_SCHEMA}"
        )
    if (
        not isinstance(value["seq"], int)
        or isinstance(value["seq"], bool)
        or value["seq"] != expected_sequence
    ):
        raise ValueError(f"journal sequence mismatch at {expected_sequence}")
    if not isinstance(value["run_id"], str) or value["run_id"] != run_id:
        raise ValueError(f"journal run identity mismatch at {expected_sequence}")
    if (
        not isinstance(value["previous"], str)
        or value["previous"] != expected_previous
    ):
        raise ValueError(f"journal chain mismatch at {expected_sequence}")
    if not isinstance(value["type"], str) or value["type"] not in EVENT_TYPES:
        raise ValueError(f"journal event type is invalid at {expected_sequence}")
    if not isinstance(value["task_id"], str):
        raise ValueError(f"journal task identity is invalid at {expected_sequence}")
    task_event = value["type"].startswith("task-")
    if task_event != bool(value["task_id"]):
        raise ValueError(f"journal task identity is invalid at {expected_sequence}")
    if (
        not isinstance(value["attempt"], int)
        or isinstance(value["attempt"], bool)
        or value["attempt"] < 0
        or not isinstance(value["idempotency_key"], str)
    ):
        raise ValueError(f"journal attempt identity is invalid at {expected_sequence}")
    if not isinstance(value["payload"], dict):
        raise ValueError(f"journal payload is invalid at {expected_sequence}")
    semantic = dict(value)
    claimed = semantic.pop("fingerprint")
    if not valid_hash(claimed) or digest(semantic) != claimed:
        raise ValueError(f"journal fingerprint mismatch at {expected_sequence}")
    return copy.deepcopy(value)


def read_journal(journal: Path, run_id: str) -> list[dict[str, Any]]:
    if journal.is_symlink() or not journal.is_dir():
        raise ValueError("journal directory is missing or unsafe")
    files = sorted(journal.iterdir())
    expected_names = [f"{index:06d}.toon" for index in range(1, len(files) + 1)]
    if [path.name for path in files] != expected_names:
        raise ValueError("journal files are not a continuous ordered sequence")
    events: list[dict[str, Any]] = []
    previous = ZERO_HASH
    for sequence, path in enumerate(files, start=1):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"journal event {sequence} is unsafe")
        value = read_toon(path, f"journal event {sequence}")
        event = validate_event(
            value,
            expected_sequence=sequence,
            expected_previous=previous,
            run_id=run_id,
        )
        events.append(event)
        previous = event["fingerprint"]
    return events


def replay(
    run_id: str,
    plan: dict[str, Any],
    events: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    state = initial_state(run_id, plan)
    seen_start = False
    planned: set[str] = set()
    for event in events:
        if event["type"] == "run-started":
            if seen_start or event["seq"] != 1:
                raise ValueError("run-started must be the first unique event")
            if event["payload"].get("plan_fingerprint") != plan["fingerprint"]:
                raise ValueError("journal plan fingerprint mismatch")
            seen_start = True
        elif not seen_start:
            raise ValueError("journal starts before run-started")
        if event["type"] == "task-planned":
            planned.add(event["task_id"])
        state = apply_event(state, event, plan)
    expected = {task["id"] for task in plan["tasks"]}
    if seen_start and planned != expected:
        raise ValueError("journal task-planned coverage differs from run plan")
    return state


def persist_state(run_dir: Path, state: dict[str, Any]) -> None:
    atomic_toon(run_dir / "state.toon", state)


def append_event(
    run_dir: Path,
    state: dict[str, Any],
    plan: dict[str, Any],
    event_type: str,
    *,
    task_id: str = "",
    payload: dict[str, Any] | None = None,
    idempotency_key: str = "",
) -> dict[str, Any]:
    task = task_row(state, task_id) if task_id else None
    attempt = int(task["attempts"]) if task else 0
    if event_type == "task-started" and task is not None:
        attempt += 1
    semantic = {
        "schema": EVENT_SCHEMA,
        "seq": int(state["sequence"]) + 1,
        "type": event_type,
        "run_id": state["run_id"],
        "task_id": task_id,
        "attempt": attempt,
        "idempotency_key": idempotency_key,
        "payload": payload or {},
        "previous": state["event_fingerprint"],
    }
    event = {**semantic, "fingerprint": digest(semantic)}
    journal = run_dir / "journal"
    if journal.is_symlink() or not journal.is_dir():
        raise ValueError("journal directory is missing or unsafe")
    destination = event_path(journal, event["seq"])
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"journal event already exists: {destination.name}")
    atomic_toon(destination, event)
    updated = apply_event(state, event, plan)
    persist_state(run_dir, updated)
    return updated


def load_run(run_dir: Path, run_id: str) -> tuple[dict[str, Any], dict[str, Any], bool]:
    plan = validate_plan(read_toon(run_dir / "plan.toon", "run plan"))
    events = read_journal(run_dir / "journal", run_id)
    state = replay(run_id, plan, events)
    recovered = False
    try:
        saved = read_toon(run_dir / "state.toon", "state projection")
        recovered = saved != state
    except ValueError:
        recovered = True
    return plan, state, recovered


class RunLock:
    """Fail fast when another process is mutating the same run."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.descriptor: int | None = None

    def __enter__(self) -> "RunLock":
        try:
            self.descriptor = os.open(
                self.path,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0),
                0o600,
            )
        except FileExistsError as exc:
            raise ValueError("run is locked by another process") from exc
        return self

    def __exit__(self, *_args: object) -> None:
        if self.descriptor is not None:
            os.close(self.descriptor)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def output(
    action: str,
    state: dict[str, Any],
    *,
    recovered: bool = False,
    idempotent: bool = False,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "action": action,
        "idempotent": idempotent,
        "recovered": recovered,
        "state": state,
    }


def start_run(
    repository: Path,
    runs_root: Path,
    run_id: str,
    plan_path: Path,
) -> dict[str, Any]:
    plan = validate_plan(read_toon(plan_path.resolve(), "run plan"))
    ensure_directory(repository, runs_root)
    final = bounded_path(repository, runs_root / run_id)
    if final.exists():
        raise ValueError("run already exists")
    temporary = Path(tempfile.mkdtemp(prefix=".run-", dir=runs_root))
    try:
        (temporary / "journal").mkdir()
        atomic_toon(temporary / "plan.toon", plan)
        state = initial_state(run_id, plan)
        state = append_event(
            temporary,
            state,
            plan,
            "run-started",
            payload={
                "plan_fingerprint": plan["fingerprint"],
                "graph_fingerprint": plan["graph_fingerprint"],
            },
        )
        for task in plan["tasks"]:
            state = append_event(
                temporary,
                state,
                plan,
                "task-planned",
                task_id=task["id"],
                payload={
                    "step_id": task["step_id"],
                    "step_fingerprint": task["step_fingerprint"],
                    "context_fingerprint": task["context"]["fingerprint"],
                    "idempotency_scope": task["idempotency_scope"],
                    "side_effect": task["side_effect"],
                },
            )
        os.replace(temporary, final)
        return state
    except Exception:
        for child in sorted(temporary.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        if temporary.exists():
            temporary.rmdir()
        raise


def record_task(
    run_dir: Path,
    state: dict[str, Any],
    plan: dict[str, Any],
    task_id: str,
    record: dict[str, Any],
    evidence: list[str],
    effect_receipt: str,
    supplied_key: str,
) -> tuple[dict[str, Any], bool]:
    task = task_row(state, task_id)
    if task is None:
        raise ValueError(f"unknown task: {task_id}")
    record = validate_task_record(task, record)
    if not isinstance(effect_receipt, str) or not isinstance(supplied_key, str):
        raise ValueError("task completion receipt fields must be strings")
    normalized_evidence = sorted(set(evidence))
    if not unique_strings(normalized_evidence):
        raise ValueError("task evidence must contain unique non-empty strings")
    if not normalized_evidence and record["result_fingerprint"]:
        normalized_evidence = [f"result:{record['result_fingerprint']}"]
    expected_key = task["idempotency_key"]
    if supplied_key and supplied_key != expected_key:
        raise ValueError("idempotency key does not match the started task")
    completion = completion_fingerprint(
        record,
        normalized_evidence,
        effect_receipt,
    )
    if task["status"] in {"succeeded", "failed", "blocked"}:
        if (
            task["protocol_phase"] == "result"
            and task["last_record"] == record
            and task["evidence"] == normalized_evidence
            and task["effect_receipt"] == effect_receipt
            and task["completion_fingerprint"] == completion
        ):
            return state, True
        raise ValueError(
            "idempotency replay payload does not match the completed task"
        )
    if task["status"] != "running" or state["running_task"] != task_id:
        raise ValueError(f"task {task_id} is not running")
    if record["outcome"] == "succeeded":
        if task["side_effect"] != "none" and not effect_receipt:
            raise ValueError("successful side-effecting task requires an effect receipt")
    if task["protocol_phase"] == "running":
        state = append_event(
            run_dir,
            state,
            plan,
            "task-terminal",
            task_id=task_id,
            idempotency_key=expected_key,
            payload={
                "outcome": record["outcome"],
                "completion_fingerprint": completion,
            },
        )
        task = task_row(state, task_id)
        assert task is not None
    if task["protocol_phase"] == "terminal":
        if (
            task["terminal_outcome"] != record["outcome"]
            or task["completion_fingerprint"] != completion
        ):
            raise ValueError(
                "idempotency replay payload does not match task-terminal"
            )
        state = append_event(
            run_dir,
            state,
            plan,
            "task-evidence",
            task_id=task_id,
            idempotency_key=expected_key,
            payload={
                "evidence": normalized_evidence,
                "effect_receipt": effect_receipt,
            },
        )
        task = task_row(state, task_id)
        assert task is not None
    if task["protocol_phase"] == "evidence":
        if (
            task["terminal_outcome"] != record["outcome"]
            or task["completion_fingerprint"] != completion
            or task["evidence"] != normalized_evidence
            or task["effect_receipt"] != effect_receipt
        ):
            raise ValueError(
                "idempotency replay payload does not match task-evidence"
            )
        state = append_event(
            run_dir,
            state,
            plan,
            "task-result",
            task_id=task_id,
            idempotency_key=expected_key,
            payload={"record": record},
        )
    elif task["protocol_phase"] not in {"terminal", "result"}:
        raise ValueError(f"task {task_id} completion protocol is invalid")
    return state, False


def render_markdown(result: dict[str, Any]) -> str:
    state = result["state"]
    return (
        "# Runtime State\n\n"
        f"- Run: `{state['run_id']}`\n"
        f"- Status: `{state['status']}`\n"
        f"- Sequence: {state['sequence']}\n"
        f"- Running task: `{state['running_task'] or 'none'}`\n"
        f"- Ready: `{', '.join(state['ready_tasks']) or 'none'}`\n"
        f"- Stop reason: `{state['stop_reason'] or 'none'}`\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--start", action="store_true")
    actions.add_argument("--next", action="store_true")
    actions.add_argument("--record", action="store_true")
    actions.add_argument("--resume", action="store_true")
    actions.add_argument("--status", action="store_true")
    actions.add_argument("--retry")
    actions.add_argument("--stop", action="store_true")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--task")
    parser.add_argument("--outcome", choices=("succeeded", "failed", "blocked"))
    parser.add_argument("--result-fingerprint", default="")
    parser.add_argument("--tokens", type=int, default=0)
    parser.add_argument("--commit", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--effect-receipt", default="")
    parser.add_argument("--idempotency-key", default="")
    parser.add_argument("--format", choices=("markdown", "toon"), default="toon")
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
        print("ERROR: runtime cannot mutate feature lifecycle state")
        return 1
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.run_id):
        print("ERROR: run id is unsafe")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    try:
        runs_root = bounded_path(repository, repository / "_ai_sdlc/runs")
        run_dir = bounded_path(repository, runs_root / args.run_id)
        recovered = False
        idempotent = False
        if args.start:
            if args.plan is None:
                raise ValueError("--plan is required for --start")
            state = start_run(repository, runs_root, args.run_id, args.plan)
            result = output("start", state)
        else:
            if not run_dir.is_dir() or run_dir.is_symlink():
                raise ValueError("run does not exist or is unsafe")
            if args.status:
                _plan, state, recovered = load_run(run_dir, args.run_id)
                result = output("status", state, recovered=recovered)
            else:
                with RunLock(run_dir / ".lock"):
                    plan, state, recovered = load_run(run_dir, args.run_id)
                    if recovered:
                        persist_state(run_dir, state)
                    if args.resume:
                        result = output("resume", state, recovered=recovered)
                    elif args.next:
                        if state["status"] != "running":
                            raise ValueError(
                                f"run is not running: {state['status']} "
                                f"({state['stop_reason']})"
                            )
                        if state["running_task"]:
                            idempotent = True
                        elif not state["ready_tasks"]:
                            raise ValueError("run has no ready task")
                        else:
                            task = task_row(state, state["ready_tasks"][0])
                            assert task is not None
                            key = task_idempotency(
                                plan,
                                task,
                                int(task["attempts"]) + 1,
                            )
                            state = append_event(
                                run_dir,
                                state,
                                plan,
                                "task-started",
                                task_id=task["id"],
                                idempotency_key=key,
                                payload={"operation": task["operation"]},
                            )
                        result = output("next", state, idempotent=idempotent)
                    elif args.record:
                        if not args.task or not args.outcome:
                            raise ValueError("--task and --outcome are required for --record")
                        record = {
                            "outcome": args.outcome,
                            "result_fingerprint": args.result_fingerprint,
                            "tokens": args.tokens,
                            "commit": args.commit,
                            "reason": args.reason,
                        }
                        state, idempotent = record_task(
                            run_dir,
                            state,
                            plan,
                            args.task,
                            record,
                            list(args.evidence),
                            args.effect_receipt,
                            args.idempotency_key,
                        )
                        result = output("record", state, idempotent=idempotent)
                    elif args.retry:
                        if not args.reason.strip():
                            raise ValueError("--retry requires --reason")
                        task = task_row(state, args.retry)
                        if task is None:
                            raise ValueError(f"unknown task: {args.retry}")
                        state = append_event(
                            run_dir,
                            state,
                            plan,
                            "task-retry-requested",
                            task_id=args.retry,
                            idempotency_key=task["idempotency_key"],
                            payload={"reason": args.reason},
                        )
                        result = output("retry", state)
                    elif args.stop:
                        if not args.reason.strip():
                            raise ValueError("--stop requires --reason")
                        state = append_event(
                            run_dir,
                            state,
                            plan,
                            "run-stopped",
                            payload={"reason": args.reason},
                        )
                        result = output("stop", state)
                    else:
                        raise ValueError("unsupported runtime action")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.format == "toon":
        print(toon_codec.encode_toon(result), end="")
    else:
        print(render_markdown(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
