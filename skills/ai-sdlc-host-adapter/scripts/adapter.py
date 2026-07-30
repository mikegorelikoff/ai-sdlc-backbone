#!/usr/bin/env python3
"""Validate v2 host adapters and negotiate one canonical StepCard."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402
from ai_sdlc_okf import migrate_concept_text, write_bundle_indexes  # noqa: E402
from ai_sdlc_step_context import validate_step_context_pack  # noqa: E402


ADAPTER_SCHEMA = "ai-sdlc-host-adapter/v2"
REQUEST_SCHEMA = "ai-sdlc-capability-request/v2"
RESULT_SCHEMA = "ai-sdlc-capability-negotiation/v2"
STEP_CARD_SCHEMA = "ai-sdlc-step-card/v1"
ADAPTER_FIELDS = {
    "schema",
    "id",
    "version",
    "host",
    "harness_api",
    "capabilities",
    "operations",
    "limits",
}
REQUEST_FIELDS = {"schema", "step_card", "concurrency", "isolation_required"}
OPERATION_FIELDS = {"portable", "host_operation", "semantics"}
STEP_CARD_FIELDS = {
    "schema",
    "skill",
    "step_id",
    "path",
    "step_type",
    "depends_on",
    "operation",
    "capabilities",
    "side_effect",
    "gates",
    "outputs",
    "max_attempts",
    "commit_boundary",
    "on_failure",
    "load",
    "reason",
    "context",
    "ready",
    "graph_fingerprint",
    "step_fingerprint",
    "idempotency_scope",
}
NAME = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)*$")


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


def semver(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        return None
    return tuple(int(item) for item in value.split("."))


def names(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    if (
        not isinstance(value, list)
        or (nonempty and not value)
        or not all(isinstance(item, str) and NAME.fullmatch(item) for item in value)
    ):
        return [f"{field} must be a valid identifier array"]
    return [f"{field} must be unique"] if len(value) != len(set(value)) else []


def validate_adapter(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["adapter must be a TOON mapping"]
    received = value.get("schema")
    if received != ADAPTER_SCHEMA:
        return [
            f"ADAPTER_SCHEMA_MISMATCH: received {received!r}; "
            f"expected {ADAPTER_SCHEMA}; regenerate the adapter contract"
        ]
    if set(value) != ADAPTER_FIELDS:
        return ["adapter fields do not match the v2 contract"]
    errors: list[str] = []
    if not isinstance(value["id"], str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*",
        value["id"],
    ):
        errors.append("adapter id is invalid")
    if semver(value["version"]) is None:
        errors.append("adapter version must use x.y.z")
    if not isinstance(value["host"], str) or not value["host"].strip():
        errors.append("adapter host is required")
    api = value["harness_api"]
    if (
        not isinstance(api, dict)
        or set(api) != {"min", "max_exclusive"}
        or semver(api.get("min")) is None
        or semver(api.get("max_exclusive")) is None
    ):
        errors.append("adapter harness_api range is invalid")
    elif semver(api["min"]) >= semver(api["max_exclusive"]):
        errors.append("adapter harness_api range is empty")
    errors.extend(names(value["capabilities"], "adapter capabilities"))
    operations = value["operations"]
    portable: list[str] = []
    if not isinstance(operations, list) or not operations:
        errors.append("adapter operations must be non-empty")
    else:
        for index, operation in enumerate(operations):
            if not isinstance(operation, dict) or set(operation) != OPERATION_FIELDS:
                errors.append(f"operations[{index}] fields are invalid")
                continue
            portable.append(str(operation["portable"]))
            if not all(
                isinstance(operation[field], str)
                and NAME.fullmatch(operation[field])
                for field in ("portable", "host_operation")
            ):
                errors.append(f"operations[{index}] identifiers are invalid")
            if operation["semantics"] != "equivalent":
                errors.append(f"operations[{index}].semantics must be equivalent")
    if len(portable) != len(set(portable)):
        errors.append("portable operation mappings must be unique")
    limits = value["limits"]
    if (
        not isinstance(limits, dict)
        or set(limits) != {"max_concurrency", "isolation"}
        or not isinstance(limits.get("max_concurrency"), int)
        or isinstance(limits.get("max_concurrency"), bool)
        or not 1 <= limits.get("max_concurrency", 0) <= 64
        or not isinstance(limits.get("isolation"), bool)
    ):
        errors.append("adapter limits are invalid")
    return errors


def validate_step_card(value: Any) -> list[str]:
    if not isinstance(value, dict) or set(value) != STEP_CARD_FIELDS:
        return ["request step_card fields are invalid"]
    errors: list[str] = []
    if value["schema"] != STEP_CARD_SCHEMA:
        errors.append(f"step_card schema must be {STEP_CARD_SCHEMA}")
    if not isinstance(value["skill"], str) or not re.fullmatch(
        r"ai-sdlc-[a-z0-9]+(?:-[a-z0-9]+)*",
        value["skill"],
    ):
        errors.append("step_card skill is invalid")
    if (
        not isinstance(value["step_id"], str)
        or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value["step_id"])
    ):
        errors.append("step_card step_id is invalid")
    if (
        not isinstance(value["path"], str)
        or not re.fullmatch(r"steps/[a-z0-9][a-z0-9-]*\.md", value["path"])
    ):
        errors.append("step_card path is invalid")
    if value["step_type"] not in {
        "analysis",
        "context",
        "action",
        "validation",
        "handoff",
    }:
        errors.append("step_card step_type is invalid")
    errors.extend(names(value["depends_on"], "step_card depends_on"))
    errors.extend(names(value["capabilities"], "step_card capabilities", nonempty=True))
    if value["side_effect"] not in {
        "none",
        "workspace-write",
        "external-write",
        "destructive",
    }:
        errors.append("step_card side_effect is invalid")
    errors.extend(names(value["gates"], "step_card gates", nonempty=True))
    errors.extend(names(value["outputs"], "step_card outputs", nonempty=True))
    if (
        not isinstance(value["max_attempts"], int)
        or isinstance(value["max_attempts"], bool)
        or not 1 <= value["max_attempts"] <= 5
    ):
        errors.append("step_card max_attempts must be 1..5")
    if value["commit_boundary"] not in {"none", "after-step"}:
        errors.append("step_card commit_boundary is invalid")
    if value["on_failure"] not in {"block", "retry", "handoff"}:
        errors.append("step_card on_failure is invalid")
    if value["load"] not in {"required", "on-demand", "before-completion"}:
        errors.append("step_card load is invalid")
    if not isinstance(value["reason"], str) or not value["reason"]:
        errors.append("step_card reason is required")
    if value["ready"] is not True:
        errors.append("step_card must be context-ready before negotiation")
    for field in ("graph_fingerprint", "step_fingerprint"):
        if not isinstance(value[field], str) or not re.fullmatch(
            r"[a-f0-9]{64}",
            value[field],
        ):
            errors.append(f"step_card {field} is invalid")
    if not isinstance(value["idempotency_scope"], str) or not value[
        "idempotency_scope"
    ]:
        errors.append("step_card idempotency_scope is required")
    elif (
        isinstance(value["skill"], str)
        and isinstance(value["step_id"], str)
        and isinstance(value["graph_fingerprint"], str)
        and value["idempotency_scope"]
        != (
            f"{value['skill']}:{value['step_id']}:"
            f"{value['graph_fingerprint']}"
        )
    ):
        errors.append("step_card idempotency_scope is inconsistent")
    try:
        validate_step_context_pack(
            value["context"],
            expected_skill=(
                value["skill"] if isinstance(value["skill"], str) else ""
            ),
            expected_step_id=(
                value["step_id"]
                if isinstance(value["step_id"], str)
                else ""
            ),
            require_sufficient=True,
        )
    except ValueError as exc:
        errors.append(f"step_card context is invalid: {exc}")
    return errors


def validate_request(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["request must be a TOON mapping"]
    received = value.get("schema")
    if received != REQUEST_SCHEMA:
        return [
            f"ADAPTER_SCHEMA_MISMATCH: received {received!r}; "
            f"expected {REQUEST_SCHEMA}; rebuild the request from a StepCard"
        ]
    if set(value) != REQUEST_FIELDS:
        return ["request fields do not match the v2 contract"]
    errors = validate_step_card(value["step_card"])
    if (
        not isinstance(value["concurrency"], int)
        or isinstance(value["concurrency"], bool)
        or not 1 <= value["concurrency"] <= 64
    ):
        errors.append("request concurrency must be 1..64")
    if not isinstance(value["isolation_required"], bool):
        errors.append("request isolation_required must be boolean")
    return errors


def required_capabilities(card: dict[str, Any]) -> list[str]:
    capabilities = set(card["capabilities"])
    side_effect_capability = {
        "workspace-write": "filesystem.write",
        "external-write": "external.write",
        "destructive": "destructive.execute",
    }.get(card["side_effect"])
    if side_effect_capability:
        capabilities.add(side_effect_capability)
    return sorted(capabilities)


def negotiate(adapter: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    card = request["step_card"]
    operation = f"step.{card['step_type']}"
    native = {
        item["portable"]: item["host_operation"]
        for item in adapter["operations"]
    }
    mapping = (
        {
            "portable": operation,
            "host_operation": native[operation],
            "semantics": "equivalent",
        }
        if operation in native
        else {}
    )
    required = required_capabilities(card)
    missing = sorted(set(required) - set(adapter["capabilities"]))
    unsupported = [] if mapping else [operation]
    effective_concurrency = min(
        request["concurrency"],
        adapter["limits"]["max_concurrency"],
    )
    fallbacks: list[dict[str, str]] = []
    if effective_concurrency < request["concurrency"]:
        fallbacks.append(
            {"subject": "concurrency", "reason": "host-concurrency-clamped"}
        )
    if request["isolation_required"] and not adapter["limits"]["isolation"]:
        effective_concurrency = 1
        fallbacks.append(
            {"subject": "isolation", "reason": "sequential-isolation-fallback"}
        )
    semantic = {
        "schema": RESULT_SCHEMA,
        "adapter": {
            "id": adapter["id"],
            "version": adapter["version"],
            "host": adapter["host"],
            "fingerprint": digest(adapter),
        },
        "request_fingerprint": digest(request),
        "step": {
            "skill": card["skill"],
            "step_id": card["step_id"],
            "step_fingerprint": card["step_fingerprint"],
            "graph_fingerprint": card["graph_fingerprint"],
        },
        "compatible": not unsupported and not missing,
        "mapping": mapping,
        "required_capabilities": required,
        "missing_capabilities": missing,
        "unsupported_operations": unsupported,
        "side_effect": card["side_effect"],
        "idempotency_scope": card["idempotency_scope"],
        "gates": card["gates"],
        "outputs": card["outputs"],
        "evidence_required": True,
        "limits": {
            "requested_concurrency": request["concurrency"],
            "effective_concurrency": effective_concurrency,
            "isolation_requested": request["isolation_required"],
            "isolation_native": adapter["limits"]["isolation"],
        },
        "fallbacks": fallbacks,
        "reason_codes": (
            [f"unsupported-operation:{item}" for item in unsupported]
            + [f"missing-capability:{item}" for item in missing]
            or ["compatible"]
        ),
    }
    return {**semantic, "fingerprint": digest(semantic)}


def markdown(value: dict[str, Any]) -> str:
    mapping = value["mapping"]
    mapped = (
        f"`{mapping['portable']}` -> `{mapping['host_operation']}`"
        if mapping
        else "none"
    )
    return (
        "# Host Capability Negotiation\n\n"
        f"- Adapter: `{value['adapter']['id']}@{value['adapter']['version']}`\n"
        f"- Step: `{value['step']['skill']}:{value['step']['step_id']}`\n"
        f"- Compatible: **{str(value['compatible']).lower()}**\n"
        f"- Mapping: {mapped}\n"
        f"- Side effect: `{value['side_effect']}`\n"
        f"- Fingerprint: `{value['fingerprint']}`\n"
    )


def load(path: Path, label: str) -> tuple[Any, str | None]:
    try:
        return toon_codec.loads(path.resolve().read_text(encoding="utf-8")), None
    except (OSError, toon_codec.ToonDecodeError) as exc:
        return {}, f"cannot read {label}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--adapter", type=Path, required=True)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--validate", action="store_true")
    actions.add_argument("--negotiate", action="store_true")
    parser.add_argument("--request", type=Path)
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
        print("ERROR: adapter negotiation cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print("ERROR: repository does not exist")
        return 1
    adapter, error = load(args.adapter, "adapter")
    errors = [error] if error else validate_adapter(adapter)
    if args.negotiate and args.request is None:
        errors.append("--request is required for negotiation")
    request: Any = {}
    if args.request:
        request, error = load(args.request, "request")
        errors.extend([error] if error else validate_request(request))
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    if args.validate:
        semantic = {
            "schema": RESULT_SCHEMA,
            "adapter": {
                "id": adapter["id"],
                "version": adapter["version"],
                "host": adapter["host"],
                "fingerprint": digest(adapter),
            },
            "valid": True,
        }
        value = {**semantic, "fingerprint": digest(semantic)}
    else:
        value = negotiate(adapter, request)
    negotiation_markdown = (
        migrate_concept_text(
            markdown(value),
            profile_key="negotiation.md",
            generated_by_override=args.generated_by,
        )
        if args.negotiate
        else ""
    )
    if args.write and args.negotiate:
        output = (
            repository
            / f"_ai_sdlc/adapters/{adapter['id']}/negotiation.toon"
        )
        try:
            atomic_write(output, toon_codec.encode_toon(value))
            atomic_write(output.with_suffix(".md"), negotiation_markdown)
            write_bundle_indexes(repository / "_ai_sdlc")
        except (OSError, ValueError) as exc:
            print(f"ERROR: {exc}")
            return 1
    if args.format == "toon":
        print(toon_codec.encode_toon(value), end="")
    elif args.negotiate:
        print(negotiation_markdown, end="")
    else:
        print("# Host Adapter\n\n- Valid: `true`\n", end="")
    return 0 if args.validate or value["compatible"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
