#!/usr/bin/env python3
"""Validate, select, and compile executable skill steps just in time."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from ai_sdlc_step_context import (
    StepContextPack,
    compile_step_context,
    validate_step_context_pack,
)
from ai_sdlc_paths import repository_root_from_skills_root
from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon


SCHEMA = "ai-sdlc-skill-steps/v2"
SELECTION_SCHEMA = "ai-sdlc-skill-step-selection/v2"
STEP_CARD_SCHEMA = "ai-sdlc-step-card/v1"
RUN_PLAN_SCHEMA = "ai-sdlc-run-plan/v2"
INVENTORY_SCHEMA = "ai-sdlc-skill-step-inventory/v2"
VERSION = "4.1.0"
ROLE_IDS = {
    "business-analyst",
    "product-manager",
    "software-architect",
    "software-engineer",
    "qa-engineer",
}
PHASE_IDS = {
    "prepare",
    "clarify",
    "route",
    "execute",
    "handoff",
    "validate",
    "complete",
}
LOAD_RULES = {"required", "on-demand", "before-completion"}
STEP_TYPES = {"analysis", "context", "action", "validation", "handoff"}
SIDE_EFFECTS = {"none", "workspace-write", "external-write", "destructive"}
COMMIT_BOUNDARIES = {"none", "after-step"}
FAILURE_POLICIES = {"block", "retry", "handoff"}
TOP_FIELDS = {"schema", "skill", "version", "entrypoints", "budgets", "steps"}
BUDGET_FIELDS = {
    "step_max_tokens",
    "context_max_tokens",
    "min_context_savings_percent",
}
STEP_FIELDS = {
    "id",
    "path",
    "type",
    "depends_on",
    "condition",
    "load",
    "max_tokens",
    "reason",
    "operation",
    "capabilities",
    "side_effect",
    "context",
    "gates",
    "outputs",
    "max_attempts",
    "commit_boundary",
    "on_failure",
}
CONDITION_FIELDS = {"phases", "roles", "actions"}
CONTEXT_FIELDS = {
    "required",
    "budget_tokens",
    "mandatory",
    "selectors",
    "critical_anchors",
    "min_savings_percent",
    "fallback",
}
CONTEXT_SELECTORS = {
    "step",
    "repository-instructions",
    "feature-traces",
    "changed-path-topology",
}
CACHE_POLICY_SCHEMA = "ai-sdlc-context-cache-runtime-policy/v1"
CACHE_POLICY_FIELDS = {"schema", "defaults", "overrides"}
CACHE_SETTING_FIELDS = {
    "enabled", "budget_tokens", "limit", "graph_depth", "graph_limit",
    "lock_timeout_ms", "process_timeout_ms", "min_savings_percent",
}


@dataclass(frozen=True)
class StepCard:
    """One executable, context-aware step contract."""

    schema: str
    skill: str
    step_id: str
    path: str
    step_type: str
    depends_on: tuple[str, ...]
    operation: str
    capabilities: tuple[str, ...]
    side_effect: str
    gates: tuple[str, ...]
    outputs: tuple[str, ...]
    max_attempts: int
    commit_boundary: str
    on_failure: str
    load: str
    reason: str
    context: dict[str, object]
    ready: bool
    graph_fingerprint: str
    step_fingerprint: str
    idempotency_scope: str


@dataclass(frozen=True)
class StepSelection:
    """Deterministic ready-set selection for one phase entrypoint."""

    schema: str
    skill: str
    phase: str
    role: str
    action: str
    target_steps: tuple[str, ...]
    ready_steps: tuple[str, ...]
    pending_steps: tuple[str, ...]
    completed_steps: tuple[str, ...]
    execution_order: tuple[str, ...]
    selected: tuple[str, ...]
    skipped: tuple[str, ...]
    step_cards: tuple[dict[str, object], ...]
    complete: bool
    selected_tokens: int
    broad_tokens: int
    savings_percent: float
    manifest_fingerprint: str
    graph_fingerprint: str
    selection_fingerprint: str


def _canonical(value: object) -> str:
    return encode_toon(_plain(value))


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _plain(value: object) -> object:
    """Normalize tuples and dataclasses to the portable TOON data model."""
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _unique_strings(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def _schema_mismatch_error(received: object) -> ValueError:
    return ValueError(
        "STEP_SCHEMA_MISMATCH: received "
        f"{received!r}; expected {SCHEMA}; regenerate the skill graph as TOON v2"
    )


def resolve_skill_root(root: Path, skill: str) -> Path:
    """Resolve one installed skill without accepting caller-selected paths."""
    if not re.fullmatch(r"ai-sdlc-[a-z0-9]+(?:-[a-z0-9]+)*", skill):
        raise ValueError(f"STEP_UNKNOWN_SKILL: invalid skill id {skill!r}")
    packaged = Path(__file__).resolve().parents[2]
    candidates = (
        root.resolve() / "skills" / skill,
        root.resolve() / ".agents" / "skills" / skill,
        root.resolve() / ".claude" / "skills" / skill,
        packaged / skill,
    )
    for index, candidate in enumerate(candidates):
        if candidate.is_symlink():
            raise ValueError(
                f"STEP_INVALID_MANIFEST: unsafe target skill directory for {skill}"
            )
        if not candidate.exists():
            continue
        if not candidate.is_dir():
            raise ValueError(
                f"STEP_INVALID_MANIFEST: unsafe target skill directory for {skill}"
            )
        router = candidate / "SKILL.md"
        manifest = candidate / "steps" / "manifest.toon"
        if router.is_symlink() or not router.is_file():
            raise ValueError(
                f"STEP_INVALID_MANIFEST: target skill {skill} is missing SKILL.md"
            )
        if not manifest.is_file():
            if index < 2:
                raise ValueError(
                    f"STEP_INVALID_MANIFEST: target skill {skill} is missing "
                    "steps/manifest.toon"
                )
            continue
        return candidate.resolve()
    raise ValueError(f"STEP_UNKNOWN_SKILL: no installable step manifest for {skill}")


def _contained_file(skill_root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if (
        candidate.is_absolute()
        or ".." in candidate.parts
        or not re.fullmatch(r"steps/[a-z0-9][a-z0-9-]*\.md", relative)
    ):
        raise ValueError(f"STEP_UNSAFE_PATH: invalid step path {relative!r}")
    path = skill_root / candidate
    resolved = path.resolve()
    try:
        resolved.relative_to(skill_root)
    except ValueError as exc:
        raise ValueError(
            f"STEP_UNSAFE_PATH: step escapes {skill_root.name}: {relative}"
        ) from exc
    if path.is_symlink() or not resolved.is_file():
        raise ValueError(
            f"STEP_UNSAFE_PATH: step must be a regular non-symlink file: {relative}"
        )
    return resolved


def _validate_condition(value: object, prefix: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != CONDITION_FIELDS:
        raise ValueError(f"{prefix}.condition has invalid fields")
    for field in ("phases", "roles", "actions"):
        if not _unique_strings(value[field], nonempty=field == "phases"):
            raise ValueError(f"{prefix}.condition.{field} must be a unique string array")
    unknown_phases = sorted(set(value["phases"]) - PHASE_IDS)
    unknown_roles = sorted(set(value["roles"]) - ROLE_IDS)
    if unknown_phases:
        raise ValueError(
            f"{prefix}.condition.phases has unknown values: {', '.join(unknown_phases)}"
        )
    if unknown_roles:
        raise ValueError(
            f"{prefix}.condition.roles has unknown values: {', '.join(unknown_roles)}"
        )
    return value


def _validate_context(
    value: object,
    *,
    prefix: str,
    context_max: int,
    minimum_savings: float,
) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != CONTEXT_FIELDS:
        raise ValueError(f"{prefix}.context has invalid fields")
    if value["required"] is not True:
        raise ValueError(f"{prefix}.context.required must be true")
    budget = value["budget_tokens"]
    if (
        not isinstance(budget, int)
        or isinstance(budget, bool)
        or not 64 <= budget <= context_max
    ):
        raise ValueError(
            f"{prefix}.context.budget_tokens must be 64..{context_max}"
        )
    if not _unique_strings(value["mandatory"], nonempty=True):
        raise ValueError(f"{prefix}.context.mandatory must be non-empty and unique")
    if value["mandatory"] != ["step_document"]:
        raise ValueError(
            f"{prefix}.context.mandatory must contain only step_document in v4"
        )
    if not _unique_strings(value["selectors"], nonempty=True):
        raise ValueError(f"{prefix}.context.selectors must be non-empty and unique")
    unknown = sorted(set(value["selectors"]) - CONTEXT_SELECTORS)
    if unknown:
        raise ValueError(
            f"{prefix}.context.selectors has unknown values: {', '.join(unknown)}"
        )
    if "step" not in value["selectors"]:
        raise ValueError(f"{prefix}.context.selectors must include step")
    if not _unique_strings(value["critical_anchors"], nonempty=True):
        raise ValueError(
            f"{prefix}.context.critical_anchors must be non-empty and unique"
        )
    savings = value["min_savings_percent"]
    if not isinstance(savings, (int, float)) or isinstance(savings, bool):
        raise ValueError(f"{prefix}.context.min_savings_percent must be numeric")
    if float(savings) != float(minimum_savings):
        raise ValueError(
            f"{prefix}.context.min_savings_percent must match budgets "
            f"({minimum_savings})"
        )
    if value["fallback"] != "direct_read":
        raise ValueError(f"{prefix}.context.fallback must be direct_read")
    return value


def _topological_order(
    steps: list[dict[str, object]],
    *,
    subset: set[str] | None = None,
) -> tuple[str, ...]:
    by_id = {str(step["id"]): step for step in steps}
    selected = set(by_id) if subset is None else set(subset)
    indexes = {str(step["id"]): index for index, step in enumerate(steps)}
    indegree = {
        step_id: sum(1 for dep in by_id[step_id]["depends_on"] if dep in selected)
        for step_id in selected
    }
    ready = sorted(
        (step_id for step_id, degree in indegree.items() if degree == 0),
        key=lambda value: (indexes[value], value),
    )
    result: list[str] = []
    while ready:
        current = ready.pop(0)
        result.append(current)
        for candidate in selected:
            if current in by_id[candidate]["depends_on"]:
                indegree[candidate] -= 1
                if indegree[candidate] == 0:
                    ready.append(candidate)
                    ready.sort(key=lambda value: (indexes[value], value))
    if len(result) != len(selected):
        cyclic = sorted(selected - set(result))
        raise ValueError(
            "STEP_INVALID_MANIFEST: dependency cycle contains " + ", ".join(cyclic)
        )
    return tuple(result)


def _closure(by_id: dict[str, dict[str, object]], targets: Iterable[str]) -> set[str]:
    result: set[str] = set()

    def visit(step_id: str) -> None:
        if step_id in result:
            return
        result.add(step_id)
        for dependency in by_id[step_id]["depends_on"]:
            visit(str(dependency))

    for target in targets:
        visit(target)
    return result


def load_manifest(root: Path, skill: str) -> tuple[Path, dict[str, object]]:
    """Load and fully validate one executable skill graph."""
    skill_root = resolve_skill_root(root, skill)
    path = skill_root / "steps" / "manifest.toon"
    if path.is_symlink() or not path.is_file():
        raise ValueError("STEP_INVALID_MANIFEST: manifest must be a regular non-symlink file")
    try:
        value = decode_toon(path.read_text(encoding="utf-8"))
    except (OSError, ToonDecodeError) as exc:
        raise ValueError(f"STEP_INVALID_MANIFEST: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("STEP_INVALID_MANIFEST: manifest must be an object")
    if value.get("schema") != SCHEMA:
        raise _schema_mismatch_error(value.get("schema"))
    if set(value) != TOP_FIELDS:
        raise ValueError(
            "STEP_INVALID_MANIFEST: expected schema, skill, version, entrypoints, "
            "budgets, and steps fields"
        )
    if value["skill"] != skill:
        raise ValueError(
            f"STEP_INVALID_MANIFEST: skill field {value['skill']!r} "
            f"does not match {skill!r}"
        )
    if value["version"] != VERSION:
        raise ValueError(f"STEP_INVALID_MANIFEST: version must be {VERSION}")

    budgets = value["budgets"]
    if not isinstance(budgets, dict) or set(budgets) != BUDGET_FIELDS:
        raise ValueError("STEP_INVALID_MANIFEST: budgets fields are invalid")
    step_max = budgets["step_max_tokens"]
    context_max = budgets["context_max_tokens"]
    minimum_savings = budgets["min_context_savings_percent"]
    if not isinstance(step_max, int) or isinstance(step_max, bool) or not 64 <= step_max <= 5000:
        raise ValueError("STEP_INVALID_MANIFEST: step_max_tokens must be 64..5000")
    if (
        not isinstance(context_max, int)
        or isinstance(context_max, bool)
        or not 64 <= context_max <= 24000
    ):
        raise ValueError("STEP_INVALID_MANIFEST: context_max_tokens must be 64..24000")
    if (
        not isinstance(minimum_savings, (int, float))
        or isinstance(minimum_savings, bool)
        or not 0 <= float(minimum_savings) <= 100
    ):
        raise ValueError(
            "STEP_INVALID_MANIFEST: min_context_savings_percent must be 0..100"
        )

    steps = value["steps"]
    if not isinstance(steps, list) or len(steps) < 5:
        raise ValueError("STEP_INVALID_MANIFEST: steps must contain at least five nodes")
    router = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    ids: set[str] = set()
    paths: set[str] = set()
    validated: list[dict[str, object]] = []
    for index, step in enumerate(steps):
        prefix = f"STEP_INVALID_MANIFEST: steps[{index}]"
        if not isinstance(step, dict) or set(step) != STEP_FIELDS:
            raise ValueError(f"{prefix} has invalid fields")
        step_id = step["id"]
        if (
            not isinstance(step_id, str)
            or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", step_id)
            or step_id in ids
        ):
            raise ValueError(f"{prefix}.id must be unique kebab-case")
        ids.add(step_id)
        relative = step["path"]
        if not isinstance(relative, str) or relative in paths:
            raise ValueError(f"{prefix}.path must be a unique string")
        paths.add(relative)
        step_path = _contained_file(skill_root, relative)
        if f"]({relative})" not in router:
            raise ValueError(f"{prefix}.path is not linked from SKILL.md: {relative}")
        text = step_path.read_text(encoding="utf-8")
        for heading in ("## Entry", "## Procedure", "## Exit"):
            if heading not in text:
                raise ValueError(f"{prefix}.path is missing required heading {heading}")
        if step["type"] not in STEP_TYPES:
            raise ValueError(f"{prefix}.type is invalid")
        if not _unique_strings(step["depends_on"]):
            raise ValueError(f"{prefix}.depends_on must be a unique string array")
        _validate_condition(step["condition"], prefix)
        if step["load"] not in LOAD_RULES:
            raise ValueError(f"{prefix}.load is invalid")
        maximum = step["max_tokens"]
        if (
            not isinstance(maximum, int)
            or isinstance(maximum, bool)
            or not 64 <= maximum <= step_max
        ):
            raise ValueError(f"{prefix}.max_tokens must be 64..{step_max}")
        tokens = (len(text) + 3) // 4
        if tokens > maximum:
            raise ValueError(
                f"STEP_TOKEN_OVERFLOW: {relative} uses {tokens} tokens; cap is {maximum}"
            )
        if not isinstance(step["reason"], str) or not 8 <= len(step["reason"]) <= 240:
            raise ValueError(f"{prefix}.reason must contain 8 to 240 characters")
        if not isinstance(step["operation"], str) or not re.fullmatch(
            r"[a-z][a-z0-9-]{1,63}", step["operation"]
        ):
            raise ValueError(f"{prefix}.operation must be kebab-case")
        if not _unique_strings(step["capabilities"], nonempty=True) or any(
            not re.fullmatch(r"[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+", capability)
            for capability in step["capabilities"]
        ):
            raise ValueError(f"{prefix}.capabilities are invalid")
        if step["side_effect"] not in SIDE_EFFECTS:
            raise ValueError(f"{prefix}.side_effect is invalid")
        _validate_context(
            step["context"],
            prefix=prefix,
            context_max=context_max,
            minimum_savings=float(minimum_savings),
        )
        if not _unique_strings(step["gates"], nonempty=True):
            raise ValueError(f"{prefix}.gates must be non-empty and unique")
        if not _unique_strings(step["outputs"], nonempty=True):
            raise ValueError(f"{prefix}.outputs must be non-empty and unique")
        attempts = step["max_attempts"]
        if (
            not isinstance(attempts, int)
            or isinstance(attempts, bool)
            or not 1 <= attempts <= 5
        ):
            raise ValueError(f"{prefix}.max_attempts must be 1..5")
        if step["commit_boundary"] not in COMMIT_BOUNDARIES:
            raise ValueError(f"{prefix}.commit_boundary is invalid")
        if step["on_failure"] not in FAILURE_POLICIES:
            raise ValueError(f"{prefix}.on_failure is invalid")
        validated.append(step)

    by_id = {str(step["id"]): step for step in validated}
    for step in validated:
        unknown = sorted(set(step["depends_on"]) - ids)
        if unknown:
            raise ValueError(
                f"STEP_INVALID_MANIFEST: {step['id']} has unknown dependencies: "
                + ", ".join(unknown)
            )
        if step["id"] in step["depends_on"]:
            raise ValueError(
                f"STEP_INVALID_MANIFEST: {step['id']} cannot depend on itself"
            )
    _topological_order(validated)

    entrypoints = value["entrypoints"]
    if not isinstance(entrypoints, dict) or set(entrypoints) != PHASE_IDS:
        raise ValueError(
            "STEP_INVALID_MANIFEST: entrypoints must define every standard phase"
        )
    all_targets: set[str] = set()
    for phase in sorted(PHASE_IDS):
        targets = entrypoints[phase]
        if not _unique_strings(targets, nonempty=True):
            raise ValueError(
                f"STEP_INVALID_MANIFEST: entrypoints.{phase} must be non-empty and unique"
            )
        unknown = sorted(set(targets) - ids)
        if unknown:
            raise ValueError(
                f"STEP_INVALID_MANIFEST: entrypoints.{phase} has unknown steps: "
                + ", ".join(unknown)
            )
        for target in targets:
            if phase not in by_id[target]["condition"]["phases"]:
                raise ValueError(
                    f"STEP_INVALID_MANIFEST: entrypoint {phase}->{target} "
                    "does not declare the phase"
                )
        all_targets.update(targets)
    reachable = _closure(by_id, all_targets)
    if reachable != ids:
        raise ValueError(
            "STEP_INVALID_MANIFEST: unreachable steps: "
            + ", ".join(sorted(ids - reachable))
        )

    actual_paths = {
        item.relative_to(skill_root).as_posix()
        for item in (skill_root / "steps").glob("*.md")
    }
    undeclared = sorted(actual_paths - paths)
    if undeclared:
        raise ValueError(
            "STEP_INVALID_MANIFEST: undeclared step files: " + ", ".join(undeclared)
        )
    return skill_root, value


def _step_document_record(skill_root: Path, skill: str, step: dict[str, object]) -> str:
    path = _contained_file(skill_root, str(step["path"]))
    text = path.read_text(encoding="utf-8")
    tokens = (len(text) + 3) // 4
    return (
        f"{skill}/{step['path']}:{hashlib.sha256(path.read_bytes()).hexdigest()}:"
        f"{tokens}:{step['load']}:{step['reason']}"
    )


def _graph_fingerprint(
    skill_root: Path,
    manifest: dict[str, object],
) -> str:
    documents = [
        {
            "step": step["id"],
            "path": step["path"],
            "sha256": hashlib.sha256(
                _contained_file(skill_root, str(step["path"])).read_bytes()
            ).hexdigest(),
        }
        for step in manifest["steps"]
    ]
    return _digest({"manifest": manifest, "documents": documents})


def _condition_matches(step: dict[str, object], role: str, action: str) -> bool:
    condition = step["condition"]
    return (
        (not role or not condition["roles"] or role in condition["roles"])
        and (not action or not condition["actions"] or action in condition["actions"])
    )


def _context_cache_root(root: Path) -> Path | None:
    # A source checkout contains every optional module for development, which is
    # not user opt-in. Automatic activation is limited to project installs.
    root = root.resolve()

    def safe_project_path(path: Path, *, directory: bool = False) -> bool:
        try:
            relative = path.relative_to(root)
        except ValueError:
            return False
        cursor = root
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                return False
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            return False
        return resolved.is_dir() if directory else resolved.is_file()

    packaged = Path(__file__).resolve().parents[2]
    candidates = [
        root / ".agents/skills/ai-sdlc-context-cache",
        root / ".claude/skills/ai-sdlc-context-cache",
    ]
    if packaged.resolve() != (root / "skills").resolve():
        candidates.append(packaged / "ai-sdlc-context-cache")
    for candidate in candidates:
        script = candidate / "scripts/context_cache.py"
        policy = candidate / "references/runtime-policy.toon"
        if (
            safe_project_path(candidate, directory=True)
            and safe_project_path(script)
            and safe_project_path(policy)
        ):
            return candidate.resolve()
    return None


def _cache_settings(
    root: Path,
    cache_root: Path,
    skill: str,
    step_id: str,
    manifest_budget: int,
    manifest_savings: float,
) -> dict[str, object]:
    paths = [cache_root / "references/runtime-policy.toon"]
    root_resolved = root.resolve()
    override = root_resolved / ".ai-sdlc/context-cache-policy.toon"
    if override.exists():
        cursor = root_resolved
        try:
            relative = override.relative_to(root_resolved)
            for part in relative.parts:
                cursor = cursor / part
                if cursor.is_symlink():
                    raise ValueError("CACHE_POLICY_INVALID: project policy is unsafe")
            override.resolve(strict=True).relative_to(root_resolved)
        except (OSError, ValueError) as exc:
            raise ValueError("CACHE_POLICY_INVALID: project policy is unsafe") from exc
        if not override.is_file():
            raise ValueError("CACHE_POLICY_INVALID: project policy is unsafe")
        paths.append(override)
    merged: dict[str, object] = {}
    for path in paths:
        value = decode_toon(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or set(value) != CACHE_POLICY_FIELDS:
            raise ValueError("CACHE_POLICY_INVALID: top-level fields are invalid")
        if value.get("schema") != CACHE_POLICY_SCHEMA:
            raise ValueError("CACHE_POLICY_INVALID: schema is invalid")
        defaults = value.get("defaults")
        overrides = value.get("overrides")
        if not isinstance(defaults, dict) or not set(defaults) <= CACHE_SETTING_FIELDS:
            raise ValueError("CACHE_POLICY_INVALID: defaults are invalid")
        if not isinstance(overrides, list):
            raise ValueError("CACHE_POLICY_INVALID: overrides must be an array")
        for key, item in defaults.items():
            if key == "enabled":
                valid = isinstance(item, bool)
            elif key == "min_savings_percent":
                valid = isinstance(item, (int, float)) and not isinstance(item, bool)
            else:
                valid = isinstance(item, int) and not isinstance(item, bool)
            if not valid:
                raise ValueError(f"CACHE_POLICY_INVALID: {key} has invalid type")
        merged.update(defaults)
        for item in overrides:
            if (
                not isinstance(item, dict)
                or not {"skill", "step_id"} <= set(item)
                or not set(item) <= CACHE_SETTING_FIELDS | {"skill", "step_id"}
            ):
                raise ValueError("CACHE_POLICY_INVALID: override fields are invalid")
            if not all(isinstance(item[key], str) and item[key] for key in ("skill", "step_id")):
                raise ValueError("CACHE_POLICY_INVALID: override identity is invalid")
            for key, field_value in item.items():
                if key in {"skill", "step_id"}:
                    continue
                if key == "enabled":
                    valid = isinstance(field_value, bool)
                elif key == "min_savings_percent":
                    valid = isinstance(field_value, (int, float)) and not isinstance(field_value, bool)
                else:
                    valid = isinstance(field_value, int) and not isinstance(field_value, bool)
                if not valid:
                    raise ValueError(f"CACHE_POLICY_INVALID: {key} has invalid type")
            if item["skill"] == skill and item["step_id"] == step_id:
                merged.update({k: v for k, v in item.items() if k not in {"skill", "step_id"}})
    settings = {
        "enabled": bool(merged.get("enabled", True)),
        "budget_tokens": min(manifest_budget, int(merged.get("budget_tokens", manifest_budget))),
        "limit": int(merged.get("limit", 12)),
        "graph_depth": int(merged.get("graph_depth", 1)),
        "graph_limit": int(merged.get("graph_limit", 64)),
        "lock_timeout_ms": int(merged.get("lock_timeout_ms", 1500)),
        "process_timeout_ms": int(merged.get("process_timeout_ms", 8000)),
        "min_savings_percent": max(manifest_savings, float(merged.get("min_savings_percent", manifest_savings))),
    }
    if not 64 <= settings["budget_tokens"] <= manifest_budget:
        raise ValueError("CACHE_POLICY_INVALID: budget is outside manifest bounds")
    if not 1 <= settings["limit"] <= 100 or not 0 <= settings["graph_depth"] <= 4:
        raise ValueError("CACHE_POLICY_INVALID: retrieval bounds are invalid")
    if not 1 <= settings["graph_limit"] <= 500:
        raise ValueError("CACHE_POLICY_INVALID: graph limit is invalid")
    if not 50 <= settings["lock_timeout_ms"] <= 30_000:
        raise ValueError("CACHE_POLICY_INVALID: lock timeout is invalid")
    if not 250 <= settings["process_timeout_ms"] <= 60_000:
        raise ValueError("CACHE_POLICY_INVALID: process timeout is invalid")
    if not 0 <= settings["min_savings_percent"] <= 100:
        raise ValueError("CACHE_POLICY_INVALID: savings threshold is invalid")
    return settings


def _cached_context(
    *,
    root: Path,
    cache_root: Path,
    skill: str,
    step: dict[str, object],
    explicit_paths: Iterable[str],
    goal: str,
    trace_ids: Iterable[str],
) -> StepContextPack | None:
    contract = step["context"]
    settings = _cache_settings(
        root, cache_root, skill, str(step["id"]),
        int(contract["budget_tokens"]), float(contract["min_savings_percent"]),
    )
    if not settings["enabled"]:
        return None
    script = cache_root / "scripts/context_cache.py"
    timeout = settings["process_timeout_ms"] / 1000.0
    warm_command = [
        sys.executable, str(script), "warm", "--root", str(root),
        "--lock-timeout-ms", str(settings["lock_timeout_ms"]), "--retries", "1",
    ]
    warmed = subprocess.run(
        warm_command, check=False, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, timeout=timeout,
    )
    if warmed.returncode != 0:
        return None
    query = " ".join(
        value for value in (
            goal, skill, str(step["id"]), str(step["reason"]),
            " ".join(sorted({str(value) for value in trace_ids if str(value)})),
            " ".join(sorted({str(value) for value in explicit_paths if str(value)})),
        ) if value
    )
    packed = subprocess.run(
        [
            sys.executable, str(script), "pack", "--root", str(root),
            "--query", query, "--skill", skill, "--step-id", str(step["id"]),
            "--budget-tokens", str(settings["budget_tokens"]),
            "--limit", str(settings["limit"]),
            "--graph-depth", str(settings["graph_depth"]),
            "--graph-limit", str(settings["graph_limit"]),
            "--min-savings-percent", str(settings["min_savings_percent"]),
        ],
        check=False, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, timeout=timeout,
    )
    if packed.returncode != 0:
        return None
    value = decode_toon(packed.stdout)
    validated = validate_step_context_pack(
        value, expected_skill=skill, expected_step_id=str(step["id"]),
        require_sufficient=True,
    )
    if validated["strategy"] != "packed":
        return None
    selected_paths = {str(item["path"]) for item in validated["selected"]}
    if any(str(path) not in selected_paths for path in explicit_paths):
        return None
    return StepContextPack(**validated)


def _build_card(
    *,
    root: Path,
    skill_root: Path,
    skill: str,
    step: dict[str, object],
    graph_fingerprint: str,
    explicit_paths: Iterable[str],
    goal: str,
    trace_ids: Iterable[str],
) -> StepCard:
    context: StepContextPack | None = None
    cache_root = _context_cache_root(root)
    if cache_root is not None:
        try:
            context = _cached_context(
                root=root, cache_root=cache_root, skill=skill, step=step,
                explicit_paths=explicit_paths, goal=goal, trace_ids=trace_ids,
            )
        except (OSError, subprocess.SubprocessError, ToonDecodeError, ValueError):
            context = None
    if context is None:
        context = compile_step_context(
            root=root,
            skill_root=skill_root,
            skill=skill,
            step=step,
            explicit_paths=explicit_paths,
            goal=goal,
            trace_ids=trace_ids,
        )
    path = _contained_file(skill_root, str(step["path"]))
    step_fingerprint = _digest(
        {
            "step": step,
            "document_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    )
    return StepCard(
        schema=STEP_CARD_SCHEMA,
        skill=skill,
        step_id=str(step["id"]),
        path=str(step["path"]),
        step_type=str(step["type"]),
        depends_on=tuple(str(value) for value in step["depends_on"]),
        operation=str(step["operation"]),
        capabilities=tuple(str(value) for value in step["capabilities"]),
        side_effect=str(step["side_effect"]),
        gates=tuple(str(value) for value in step["gates"]),
        outputs=tuple(str(value) for value in step["outputs"]),
        max_attempts=int(step["max_attempts"]),
        commit_boundary=str(step["commit_boundary"]),
        on_failure=str(step["on_failure"]),
        load=str(step["load"]),
        reason=str(step["reason"]),
        context=asdict(context),
        ready=context.sufficient,
        graph_fingerprint=graph_fingerprint,
        step_fingerprint=step_fingerprint,
        idempotency_scope=f"{skill}:{step['id']}:{graph_fingerprint}",
    )


def select_steps(
    root: Path,
    skill: str,
    phase: str,
    *,
    role: str = "",
    action: str = "",
    completed_steps: Iterable[str] = (),
    context_paths: Iterable[str] = (),
    goal: str = "",
    trace_ids: Iterable[str] = (),
) -> StepSelection:
    """Resolve the ready set for one executable phase entrypoint."""
    if phase not in PHASE_IDS:
        raise ValueError(f"STEP_UNKNOWN_PHASE: {phase}")
    if role and role not in ROLE_IDS:
        raise ValueError(f"STEP_UNKNOWN_ROLE: {role}")
    root = root.resolve()
    completed_steps = tuple(str(value) for value in completed_steps)
    context_paths = tuple(str(value) for value in context_paths)
    trace_ids = tuple(str(value) for value in trace_ids)
    skill_root, manifest = load_manifest(root, skill)
    steps = manifest["steps"]
    by_id = {str(step["id"]): step for step in steps}
    targets = [
        str(step_id)
        for step_id in manifest["entrypoints"][phase]
        if _condition_matches(by_id[str(step_id)], role, action)
    ]
    if not targets:
        raise ValueError(
            f"STEP_NO_MATCH: {skill} has no entrypoint for phase={phase}, "
            f"role={role or '*'}, action={action or '*'}"
        )
    closure = _closure(by_id, targets)
    incompatible = sorted(
        step_id
        for step_id in closure
        if not _condition_matches(by_id[step_id], role, action)
    )
    if incompatible:
        raise ValueError(
            "STEP_CONDITION_BLOCKED: dependency conditions do not match: "
            + ", ".join(incompatible)
        )
    completed = set(completed_steps)
    unknown_completed = sorted(completed - set(by_id))
    if unknown_completed:
        raise ValueError(
            "STEP_UNKNOWN_COMPLETION: " + ", ".join(unknown_completed)
        )
    order = _topological_order(steps, subset=closure)
    pending = tuple(step_id for step_id in order if step_id not in completed)
    ready = tuple(
        step_id
        for step_id in pending
        if set(by_id[step_id]["depends_on"]) <= completed
    )
    if pending and not ready:
        raise ValueError(
            "STEP_NO_READY_NODE: pending graph has no dependency-satisfied step"
        )

    graph_fingerprint = _graph_fingerprint(skill_root, manifest)
    selected = tuple(
        _step_document_record(skill_root, skill, by_id[step_id])
        for step_id in ready
    )
    cards = tuple(
        asdict(
            _build_card(
                root=root,
                skill_root=skill_root,
                skill=skill,
                step=by_id[step_id],
                graph_fingerprint=graph_fingerprint,
                explicit_paths=context_paths,
                goal=goal,
                trace_ids=trace_ids,
            )
        )
        for step_id in ready
    )
    skipped: list[str] = []
    for step in steps:
        step_id = str(step["id"])
        if step_id not in closure:
            skipped.append(f"{step_id}:outside-entrypoint-closure")
        elif step_id in completed:
            skipped.append(f"{step_id}:completed")
        elif step_id not in ready:
            missing = sorted(set(step["depends_on"]) - completed)
            skipped.append(f"{step_id}:waiting-for:{'/'.join(missing)}")
    broad_tokens = sum(
        (len(_contained_file(skill_root, str(step["path"])).read_text(encoding="utf-8")) + 3)
        // 4
        for step in steps
    )
    selected_tokens = sum(
        (len(_contained_file(skill_root, str(by_id[step_id]["path"])).read_text(encoding="utf-8")) + 3)
        // 4
        for step_id in ready
    )
    savings = round(
        ((broad_tokens - selected_tokens) / broad_tokens * 100.0)
        if broad_tokens
        else 0.0,
        2,
    )
    manifest_fingerprint = _digest(manifest)
    semantic = {
        "schema": SELECTION_SCHEMA,
        "manifest": manifest_fingerprint,
        "graph": graph_fingerprint,
        "skill": skill,
        "phase": phase,
        "role": role,
        "action": action,
        "targets": targets,
        "ready": ready,
        "pending": pending,
        "completed": sorted(completed),
        "selected": selected,
        "skipped": skipped,
        "step_cards": cards,
    }
    return StepSelection(
        schema=SELECTION_SCHEMA,
        skill=skill,
        phase=phase,
        role=role,
        action=action,
        target_steps=tuple(targets),
        ready_steps=ready,
        pending_steps=pending,
        completed_steps=tuple(sorted(completed)),
        execution_order=order,
        selected=selected,
        skipped=tuple(skipped),
        step_cards=cards,
        complete=not pending,
        selected_tokens=selected_tokens,
        broad_tokens=broad_tokens,
        savings_percent=savings,
        manifest_fingerprint=manifest_fingerprint,
        graph_fingerprint=graph_fingerprint,
        selection_fingerprint=_digest(semantic),
    )


def compile_run_plan(
    root: Path,
    skill: str,
    phase: str,
    *,
    role: str = "",
    action: str = "",
    completed_steps: Iterable[str] = (),
    context_paths: Iterable[str] = (),
    goal: str = "",
    trace_ids: Iterable[str] = (),
) -> dict[str, object]:
    """Compile a context-complete v2 task plan from the selected skill graph."""
    completed_steps = tuple(str(value) for value in completed_steps)
    context_paths = tuple(str(value) for value in context_paths)
    trace_ids = tuple(str(value) for value in trace_ids)
    selection = select_steps(
        root,
        skill,
        phase,
        role=role,
        action=action,
        completed_steps=completed_steps,
        context_paths=context_paths,
        goal=goal,
        trace_ids=trace_ids,
    )
    skill_root, manifest = load_manifest(root, skill)
    by_id = {str(step["id"]): step for step in manifest["steps"]}
    closure = set(selection.execution_order)
    tasks: list[dict[str, object]] = []
    insufficient: list[str] = []
    for step_id in selection.execution_order:
        step = by_id[step_id]
        card = asdict(
            _build_card(
                root=root.resolve(),
                skill_root=skill_root,
                skill=skill,
                step=step,
                graph_fingerprint=selection.graph_fingerprint,
                explicit_paths=context_paths,
                goal=goal,
                trace_ids=trace_ids,
            )
        )
        validate_step_context_pack(
            card["context"],
            expected_skill=skill,
            expected_step_id=step_id,
        )
        if card["ready"] is not True:
            insufficient.append(
                f"{step_id} ({card['context']['reason']})"
            )
        tasks.append(
            {
                "id": f"{skill}:{step_id}",
                "schema": card["schema"],
                "skill": card["skill"],
                "step_id": card["step_id"],
                "path": card["path"],
                "step_type": card["step_type"],
                "status": "pending",
                "depends_on": [
                    f"{skill}:{dependency}"
                    for dependency in card["depends_on"]
                    if dependency in closure
                ],
                "operation": card["operation"],
                "capabilities": card["capabilities"],
                "side_effect": card["side_effect"],
                "context": card["context"],
                "gates": card["gates"],
                "outputs": card["outputs"],
                "max_attempts": card["max_attempts"],
                "max_tokens": step["max_tokens"],
                "commit_boundary": card["commit_boundary"],
                "on_failure": card["on_failure"],
                "load": card["load"],
                "reason": card["reason"],
                "ready": card["ready"],
                "graph_fingerprint": card["graph_fingerprint"],
                "step_fingerprint": card["step_fingerprint"],
                "idempotency_scope": card["idempotency_scope"],
            }
        )
    if insufficient:
        raise ValueError(
            "STEP_CONTEXT_INSUFFICIENT: "
            + "; ".join(insufficient)
        )
    plan: dict[str, object] = {
        "schema": RUN_PLAN_SCHEMA,
        "skill": skill,
        "entrypoint": phase,
        "role": role,
        "action": action,
        "manifest_fingerprint": selection.manifest_fingerprint,
        "graph_fingerprint": selection.graph_fingerprint,
        "selection_fingerprint": selection.selection_fingerprint,
        "targets": list(selection.target_steps),
        "budgets": {
            "max_steps": sum(int(task["max_attempts"]) for task in tasks),
            "max_failures": max(
                1,
                sum(int(task["max_attempts"]) - 1 for task in tasks),
            ),
            "max_tokens": sum(int(task["max_tokens"]) for task in tasks),
        },
        "tasks": tasks,
    }
    plan["fingerprint"] = _digest(plan)
    return plan


def render_toon(value: object) -> str:
    values = _plain(value)
    if not isinstance(values, dict):
        raise ValueError("STEP_RENDER_ERROR: TOON root must be an object")
    return encode_toon(values)


def _candidate_names(root: Path) -> set[str]:
    packaged = Path(__file__).resolve().parents[2]
    candidates = (
        root.resolve() / "skills",
        root.resolve() / ".agents" / "skills",
        root.resolve() / ".claude" / "skills",
        packaged,
    )
    names: set[str] = set()
    for candidate in candidates:
        if not candidate.is_dir() or candidate.is_symlink():
            continue
        names.update(
            path.name
            for path in candidate.iterdir()
            if path.is_dir()
            and not path.is_symlink()
            and (path / "SKILL.md").is_file()
            and path.name.startswith("ai-sdlc-")
        )
    return names


def validate_all(root: Path) -> tuple[tuple[str, ...], int]:
    """Validate every installable skill visible in the selected layout."""
    names = _candidate_names(root)
    if not names:
        raise ValueError("STEP_UNKNOWN_SKILL: no installable skills found")
    nodes = 0
    for skill in sorted(names):
        _skill_root, manifest = load_manifest(root, skill)
        nodes += len(manifest["steps"])
    return tuple(sorted(names)), nodes


def _root_from_skills_root(path: Path) -> Path:
    try:
        return repository_root_from_skills_root(path)
    except ValueError as exc:
        raise ValueError(f"STEP_INVALID_ROOT: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--skills-root", type=Path)
    parser.add_argument("--skill")
    parser.add_argument("--phase", choices=sorted(PHASE_IDS))
    parser.add_argument("--role", default="")
    parser.add_argument("--action", default="")
    parser.add_argument("--completed-step", action="append", default=[])
    parser.add_argument("--context-path", action="append", default=[])
    parser.add_argument("--goal", default="")
    parser.add_argument("--trace-id", action="append", default=[])
    parser.add_argument(
        "--emit-plan",
        action="store_true",
        help="compile the selected graph to ai-sdlc-run-plan/v2",
    )
    parser.add_argument(
        "--validate-all",
        action="store_true",
        help="validate every installed skill graph without selecting a phase",
    )
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
        parser.error("step selection is read-only and cannot mutate lifecycle state")
    try:
        root = (
            _root_from_skills_root(args.skills_root)
            if args.skills_root
            else args.root.resolve()
        )
        if args.validate_all:
            names, nodes = validate_all(root)
            result = {
                "schema": INVENTORY_SCHEMA,
                "skills": len(names),
                "nodes": nodes,
                "minimum_nodes_per_skill": 5,
                "skill_names": names,
                "result": "valid",
            }
        else:
            if not args.skill or not args.phase:
                parser.error(
                    "--skill and --phase are required unless --validate-all is used"
                )
            if args.emit_plan:
                result = compile_run_plan(
                    root,
                    args.skill,
                    args.phase,
                    role=args.role,
                    action=args.action,
                    completed_steps=args.completed_step,
                    context_paths=args.context_path,
                    goal=args.goal,
                    trace_ids=args.trace_id,
                )
            else:
                result = asdict(
                    select_steps(
                        root,
                        args.skill,
                        args.phase,
                        role=args.role,
                        action=args.action,
                        completed_steps=args.completed_step,
                        context_paths=args.context_path,
                        goal=args.goal,
                        trace_ids=args.trace_id,
                    )
                )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(render_toon(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
