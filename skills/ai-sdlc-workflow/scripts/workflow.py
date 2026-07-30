#!/usr/bin/env python3
"""Validate and compile v2 workflows from canonical skill-step graphs."""

from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_steps as step_runtime  # noqa: E402
import ai_sdlc_toon as toon_codec  # noqa: E402
from ai_sdlc_okf import migrate_concept_text, write_bundle_indexes  # noqa: E402


WORKFLOW_SCHEMA = "ai-sdlc-workflow/v2"
PLAN_SCHEMA = "ai-sdlc-workflow-plan/v2"
WORKFLOW_FIELDS = {"schema", "id", "version", "nodes"}
NODE_FIELDS = {
    "id",
    "depends_on",
    "skill",
    "entrypoint",
    "role",
    "action",
    "condition",
    "approval_owner",
}
CONDITION_FIELDS = {"field", "operator", "value"}
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def canonical(value: Any) -> str:
    return toon_codec.encode_toon(value)


def digest(value: Any) -> str:
    text = value if isinstance(value, str) else canonical(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_write(path: Path, content: str) -> None:
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f"output path contains a symlink component: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def validate_condition(value: Any, prefix: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict) or set(value) != CONDITION_FIELDS:
        return [f"{prefix}.condition fields are invalid"]
    errors: list[str] = []
    if not isinstance(value["field"], str) or not re.fullmatch(
        r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*",
        value["field"],
    ):
        errors.append(f"{prefix}.condition.field is invalid")
    if value["operator"] not in {"eq", "in", "exists"}:
        errors.append(f"{prefix}.condition.operator is invalid")
    if value["operator"] == "in" and not isinstance(value["value"], list):
        errors.append(f"{prefix}.condition.value must be an array for in")
    if value["operator"] == "exists" and not isinstance(value["value"], bool):
        errors.append(f"{prefix}.condition.value must be boolean for exists")
    return errors


def topological_order(nodes: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    by_id = {node["id"]: node for node in nodes}
    order = {node["id"]: index for index, node in enumerate(nodes)}
    pending = {node["id"]: set(node["depends_on"]) for node in nodes}
    completed: set[str] = set()
    result: list[str] = []
    while pending:
        ready = sorted(
            (
                node_id
                for node_id, dependencies in pending.items()
                if dependencies <= completed
            ),
            key=lambda node_id: (order[node_id], node_id),
        )
        if not ready:
            return [], sorted(pending)
        for node_id in ready:
            result.append(node_id)
            completed.add(node_id)
            pending.pop(node_id)
    return result, []


def validate_workflow(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["workflow must be a TOON mapping"]
    received = value.get("schema")
    if received != WORKFLOW_SCHEMA:
        return [
            f"WORKFLOW_SCHEMA_MISMATCH: received {received!r}; "
            f"expected {WORKFLOW_SCHEMA}; rewrite the workflow as skill graph nodes"
        ]
    if set(value) != WORKFLOW_FIELDS:
        return ["workflow fields do not match the v2 contract"]
    errors: list[str] = []
    if not isinstance(value["id"], str) or not ID.fullmatch(value["id"]):
        errors.append("workflow id is invalid")
    if not isinstance(value["version"], str) or not re.fullmatch(
        r"\d+\.\d+\.\d+",
        value["version"],
    ):
        errors.append("workflow version must use x.y.z")
    nodes = value["nodes"]
    if not isinstance(nodes, list) or not nodes:
        return errors + ["workflow nodes must be a non-empty array"]
    ids: list[str] = []
    valid: list[dict[str, Any]] = []
    for index, node in enumerate(nodes):
        prefix = f"nodes[{index}]"
        if not isinstance(node, dict) or set(node) != NODE_FIELDS:
            errors.append(f"{prefix} fields are invalid")
            continue
        valid.append(node)
        node_id = node["id"]
        ids.append(node_id if isinstance(node_id, str) else "")
        if not isinstance(node_id, str) or not ID.fullmatch(node_id):
            errors.append(f"{prefix}.id is invalid")
        if not unique_strings(node["depends_on"]):
            errors.append(f"{prefix}.depends_on must be unique strings")
        if not isinstance(node["skill"], str) or not re.fullmatch(
            r"ai-sdlc-[a-z0-9]+(?:-[a-z0-9]+)*",
            node["skill"],
        ):
            errors.append(f"{prefix}.skill is invalid")
        if node["entrypoint"] not in step_runtime.PHASE_IDS:
            errors.append(f"{prefix}.entrypoint is invalid")
        if node["role"] and node["role"] not in step_runtime.ROLE_IDS:
            errors.append(f"{prefix}.role is invalid")
        if not isinstance(node["action"], str):
            errors.append(f"{prefix}.action must be text")
        errors.extend(validate_condition(node["condition"], prefix))
        if not isinstance(node["approval_owner"], str):
            errors.append(f"{prefix}.approval_owner must be text")
    if len(ids) != len(set(ids)):
        errors.append("workflow node ids must be unique")
    known = set(ids)
    for node in valid:
        unknown = sorted(set(node["depends_on"]) - known)
        if unknown:
            errors.append(
                f"node {node['id']} has unknown dependencies: "
                + ", ".join(unknown)
            )
        if node["id"] in node["depends_on"]:
            errors.append(f"node {node['id']} depends on itself")
    if not errors:
        _order, cyclic = topological_order(valid)
        if cyclic:
            errors.append("workflow dependency cycle contains " + ", ".join(cyclic))
    return errors


def get_field(context: dict[str, Any], field: str) -> tuple[Any, bool]:
    current: Any = context
    for part in field.split("."):
        if not isinstance(current, dict) or part not in current:
            return None, False
        current = current[part]
    return current, True


def condition_status(
    condition: dict[str, Any] | None,
    context: dict[str, Any] | None,
) -> tuple[str, str]:
    if condition is None:
        return "eligible", "unconditional"
    if context is None:
        return "deferred", "condition-context-missing"
    actual, exists = get_field(context, condition["field"])
    operator = condition["operator"]
    expected = condition["value"]
    if operator == "exists":
        matched = exists is expected
    elif operator == "eq":
        matched = exists and actual == expected
    else:
        matched = exists and actual in expected
    return (
        ("eligible", "condition-matched")
        if matched
        else ("skipped", "condition-not-matched")
    )


def workflow_waves(
    nodes: list[dict[str, Any]],
    statuses: dict[str, str],
    concurrency: int,
) -> list[dict[str, Any]]:
    by_id = {node["id"]: node for node in nodes}
    index = {node["id"]: position for position, node in enumerate(nodes)}
    pending = {
        node["id"] for node in nodes if statuses[node["id"]] == "eligible"
    }
    completed = {
        node["id"] for node in nodes if statuses[node["id"]] == "skipped"
    }
    waves: list[dict[str, Any]] = []
    while pending:
        ready = sorted(
            (
                node_id
                for node_id in pending
                if set(by_id[node_id]["depends_on"]) <= completed
            ),
            key=lambda node_id: (index[node_id], node_id),
        )
        if not ready:
            break
        for offset in range(0, len(ready), concurrency):
            batch = ready[offset : offset + concurrency]
            waves.append(
                {
                    "index": len(waves) + 1,
                    "mode": "parallel" if len(batch) > 1 else "sequential",
                    "nodes": batch,
                }
            )
        pending -= set(ready)
        completed |= set(ready)
    return waves


def terminal_tasks(tasks: list[dict[str, Any]]) -> list[str]:
    dependencies = {
        dependency for task in tasks for dependency in task["depends_on"]
    }
    return sorted(task["id"] for task in tasks if task["id"] not in dependencies)


def compile_workflow(
    repository: Path,
    workflow: dict[str, Any],
    context: dict[str, Any] | None,
    concurrency: int,
    approved_nodes: set[str],
) -> dict[str, Any]:
    """Compile eligible workflow nodes into one runtime-compatible v2 plan."""
    decisions: list[dict[str, str]] = []
    statuses: dict[str, str] = {}
    for node in workflow["nodes"]:
        status, reason = condition_status(node["condition"], context)
        if (
            status == "eligible"
            and node["approval_owner"]
            and node["id"] not in approved_nodes
        ):
            status, reason = "blocked", "approval-required"
        statuses[node["id"]] = status
        decisions.append(
            {
                "id": node["id"],
                "skill": node["skill"],
                "entrypoint": node["entrypoint"],
                "status": status,
                "reason": reason,
            }
        )

    by_id = {node["id"]: node for node in workflow["nodes"]}
    order, _cyclic = topological_order(workflow["nodes"])
    compiled: dict[str, dict[str, Any]] = {}
    all_tasks: list[dict[str, Any]] = []
    graph_parts: list[str] = []
    selection_parts: list[str] = []
    manifest_parts: list[str] = []
    for node_id in order:
        if statuses[node_id] != "eligible":
            continue
        node = by_id[node_id]
        subplan = step_runtime.compile_run_plan(
            repository,
            node["skill"],
            node["entrypoint"],
            role=node["role"],
            action=node["action"],
            goal=(
                node["action"]
                or f"workflow {workflow['id']} node {node['id']}"
            ),
            trace_ids=(workflow["id"], node["id"]),
        )
        internal_ids = {task["id"] for task in subplan["tasks"]}
        prefix = f"{node_id}/"
        tasks: list[dict[str, Any]] = []
        dependency_terminals = [
            terminal
            for dependency in node["depends_on"]
            if dependency in compiled
            for terminal in terminal_tasks(compiled[dependency]["tasks"])
        ]
        for task in subplan["tasks"]:
            updated = copy.deepcopy(task)
            updated["id"] = prefix + task["id"]
            updated["depends_on"] = [
                prefix + dependency
                for dependency in task["depends_on"]
                if dependency in internal_ids
            ]
            if not updated["depends_on"]:
                updated["depends_on"] = sorted(dependency_terminals)
            tasks.append(updated)
        compiled[node_id] = {"plan": subplan, "tasks": tasks}
        all_tasks.extend(tasks)
        graph_parts.append(subplan["graph_fingerprint"])
        selection_parts.append(subplan["selection_fingerprint"])
        manifest_parts.append(subplan["manifest_fingerprint"])

    run_semantic = {
        "schema": step_runtime.RUN_PLAN_SCHEMA,
        "skill": f"workflow:{workflow['id']}",
        "entrypoint": "workflow",
        "role": "",
        "action": workflow["id"],
        "manifest_fingerprint": digest(sorted(manifest_parts)),
        "graph_fingerprint": digest(sorted(graph_parts)),
        "selection_fingerprint": digest(sorted(selection_parts)),
        "targets": terminal_tasks(all_tasks) if all_tasks else ["blocked"],
        "budgets": {
            "max_steps": max(
                1,
                sum(int(task["max_attempts"]) for task in all_tasks),
            ),
            "max_failures": max(
                1,
                sum(int(task["max_attempts"]) - 1 for task in all_tasks),
            ),
            "max_tokens": max(
                1,
                sum(int(task["max_tokens"]) for task in all_tasks),
            ),
        },
        "tasks": all_tasks,
    }
    run_plan = {
        **run_semantic,
        "fingerprint": digest(run_semantic),
    }
    executable = bool(all_tasks) and all(
        status in {"eligible", "skipped"} for status in statuses.values()
    )
    semantic = {
        "schema": PLAN_SCHEMA,
        "workflow": {
            "id": workflow["id"],
            "version": workflow["version"],
            "fingerprint": digest(workflow),
        },
        "node_decisions": decisions,
        "waves": workflow_waves(workflow["nodes"], statuses, concurrency),
        "approvals": [
            {
                "node": node["id"],
                "owner": node["approval_owner"],
                "status": (
                    "approved"
                    if node["id"] in approved_nodes
                    else "required"
                ),
            }
            for node in workflow["nodes"]
            if node["approval_owner"]
        ],
        "capabilities": sorted(
            {
                capability
                for task in all_tasks
                for capability in task["capabilities"]
            }
        ),
        "side_effects": sorted({task["side_effect"] for task in all_tasks}),
        "run_plan": run_plan,
        "executable": executable,
    }
    return {**semantic, "fingerprint": digest(semantic)}


def markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Workflow Plan",
        "",
        f"Workflow: `{plan['workflow']['id']}@{plan['workflow']['version']}`",
        f"Fingerprint: `{plan['fingerprint']}`",
        f"Executable: `{str(plan['executable']).lower()}`",
        "",
        "## Waves",
        "",
    ]
    lines.extend(
        f"- {wave['index']}. **{wave['mode']}**: "
        + ", ".join(f"`{node}`" for node in wave["nodes"])
        for wave in plan["waves"]
    )
    lines.extend(["", "## Decisions", ""])
    lines.extend(
        f"- `{item['id']}`: {item['status']} — {item['reason']}"
        for item in plan["node_decisions"]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--workflow", type=Path, required=True)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--validate", action="store_true")
    actions.add_argument("--plan", action="store_true")
    parser.add_argument("--context", type=Path)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--approved-node", action="append", default=[])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--format", choices=("toon", "markdown"), default="toon")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    parser.add_argument("--generated-by")
    args = parser.parse_args()

    if args.begin_state or args.complete_state:
        print("ERROR: workflow planning cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir() or not 1 <= args.concurrency <= 64:
        print("ERROR: repository must exist and concurrency must be 1..64")
        return 1
    try:
        workflow = toon_codec.loads(
            args.workflow.resolve().read_text(encoding="utf-8")
        )
    except (OSError, toon_codec.ToonDecodeError) as exc:
        print(f"ERROR: cannot read workflow: {exc}")
        return 1
    errors = validate_workflow(workflow)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    context: dict[str, Any] | None = None
    if args.context:
        try:
            context = toon_codec.loads(
                args.context.resolve().read_text(encoding="utf-8")
            )
        except (OSError, toon_codec.ToonDecodeError) as exc:
            print(f"ERROR: cannot read context: {exc}")
            return 1
        if not isinstance(context, dict):
            print("ERROR: context must be a TOON mapping")
            return 1
    try:
        plan = compile_workflow(
            repository,
            workflow,
            context,
            args.concurrency,
            set(args.approved_node),
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    plan_markdown = migrate_concept_text(
        markdown(plan),
        profile_key="workflow-plan.md",
        generated_by_override=args.generated_by,
    )
    if args.write:
        if not plan["executable"]:
            print("ERROR: non-executable workflow plan cannot be persisted")
            return 1
        output_root = repository / f"_ai_sdlc/workflows/{workflow['id']}"
        try:
            atomic_write(
                output_root / "workflow-plan.toon",
                toon_codec.encode_toon(plan),
            )
            atomic_write(
                output_root / "run-plan.toon",
                toon_codec.encode_toon(plan["run_plan"]),
            )
            atomic_write(output_root / "plan.md", plan_markdown)
            write_bundle_indexes(repository / "_ai_sdlc")
        except (OSError, ValueError) as exc:
            print(f"ERROR: {exc}")
            return 1
    if args.format == "toon":
        print(toon_codec.encode_toon(plan), end="")
    else:
        print(plan_markdown, end="")
    return 0 if args.validate or plan["executable"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
