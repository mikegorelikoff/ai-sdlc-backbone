#!/usr/bin/env python3
"""Resolve versioned base, team, and user AI SDLC configuration safely."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


SCHEMA = "ai-sdlc-config/v1"
LAYERS = ("base", "team", "user")
PROFILE_ORDER = ("patch", "standard", "assured", "regulated")
INTERACTION_FIELDS = {
    "enabled", "preferred_name", "language", "response_style", "technical_depth", "status_updates"
}
FLOW_FIELDS = {"role_aliases", "menu_mode", "context_selectors"}
FLOW_SELECTOR_FIELDS = {"id", "roles", "actions", "include", "priority", "max_tokens", "reason"}


def packaged_defaults() -> Path:
    """Locate the single packaged defaults file in source and installed layouts."""
    script = Path(__file__).resolve()
    return script.parent.parent / "references" / "ai-sdlc.defaults.json"


def toon(value: object) -> str:
    """Escape one value for the repository TOON subset."""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def load_layer(path: Path | None, name: str, required: bool = False) -> tuple[dict[str, Any], list[str]]:
    """Load and structurally validate one configuration layer."""
    if path is None:
        return {}, []
    if not path.is_file():
        return {}, [f"{name} config does not exist: {path}"] if required else []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read {name} config: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return {}, [f"{name} config schema must be {SCHEMA}"]
    if not isinstance(value.get("values"), dict):
        return {}, [f"{name} config values must be an object"]
    unknown = sorted(set(value) - {"schema", "values", "protected"})
    if unknown:
        return {}, [f"{name} config has unknown top-level fields: {', '.join(unknown)}"]
    if "protected" in value and (not isinstance(value["protected"], list) or not all(isinstance(item, str) and item for item in value["protected"])):
        return {}, [f"{name} protected must be a string array"]
    return value, []


def flatten(value: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten nested object leaves into dotted paths deterministically."""
    result: dict[str, Any] = {}
    for key in sorted(value):
        path = f"{prefix}.{key}" if prefix else key
        child = value[key]
        if isinstance(child, dict):
            result.update(flatten(child, path))
        else:
            result[path] = child
    return result


def assign_path(root: dict[str, Any], path: str, value: Any) -> None:
    """Assign one dotted leaf into a nested dictionary."""
    parts = path.split(".")
    current = root
    for part in parts[:-1]:
        child = current.setdefault(part, {})
        if not isinstance(child, dict):
            raise ValueError(f"cannot merge {path}: {part} is already a scalar")
        current = child
    current[parts[-1]] = deepcopy(value)


def weakens(path: str, current: Any, candidate: Any) -> bool:
    """Return whether a protected candidate is less strict than current."""
    if path == "rigor.minimum_profile":
        if current not in PROFILE_ORDER or candidate not in PROFILE_ORDER:
            return True
        return PROFILE_ORDER.index(candidate) < PROFILE_ORDER.index(current)
    if path == "gates.allow_state_bypass":
        return current is False and candidate is not False
    if isinstance(current, bool):
        return current is True and candidate is not True
    if isinstance(current, (int, float)) and not isinstance(current, bool):
        return not isinstance(candidate, (int, float)) or candidate < current
    return candidate != current


def resolve(base: dict[str, Any], team: dict[str, Any], user: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str], list[str]]:
    """Merge layers in fixed order while protecting configured gates."""
    result: dict[str, Any] = {}
    provenance: dict[str, str] = {}
    errors: list[str] = []
    protected = tuple(dict.fromkeys(base.get("protected", [])))
    for layer_name, layer in zip(LAYERS, (base, team, user)):
        if layer_name != "base" and "protected" in layer:
            errors.append(f"{layer_name} config cannot redefine protected paths")
        for path, candidate in flatten(layer.get("values", {})).items():
            current_flat = flatten(result)
            if layer_name != "base" and path in protected and path in current_flat and weakens(path, current_flat[path], candidate):
                errors.append(f"{layer_name} config weakens protected gate {path}: {current_flat[path]!r} -> {candidate!r}")
                continue
            try:
                assign_path(result, path, candidate)
                provenance[path] = layer_name
            except ValueError as exc:
                errors.append(str(exc))
    missing = [path for path in protected if path not in flatten(result)]
    errors.extend(f"protected path is missing from resolved values: {path}" for path in missing)
    return result, provenance, errors


def validate_interaction(values: dict[str, Any]) -> list[str]:
    """Validate the optional typed presentation profile after layer resolution."""
    interaction = values.get("interaction")
    if interaction is None:
        return []
    if not isinstance(interaction, dict):
        return ["interaction must be an object"]
    unknown = sorted(set(interaction) - INTERACTION_FIELDS)
    errors = [f"interaction has unknown fields: {', '.join(unknown)}"] if unknown else []
    if "enabled" in interaction and not isinstance(interaction["enabled"], bool):
        errors.append("interaction.enabled must be boolean")
    preferred_name = interaction.get("preferred_name", "")
    if (
        not isinstance(preferred_name, str)
        or len(preferred_name) > 80
        or any(ord(char) < 32 or ord(char) == 127 or char in "\u2028\u2029" for char in preferred_name)
    ):
        errors.append("interaction.preferred_name must be a control-free string of at most 80 characters")
    language = interaction.get("language", "auto")
    if (
        not isinstance(language, str)
        or language != language.strip()
        or not re.fullmatch(r"auto|[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", language)
    ):
        errors.append("interaction.language must be auto or a simple BCP-47 language tag")
    allowed = {
        "response_style": {"concise", "balanced", "detailed"},
        "technical_depth": {"adaptive", "foundational", "practitioner", "expert"},
        "status_updates": {"minimal", "milestones", "frequent"},
    }
    for field, choices in allowed.items():
        if field in interaction and interaction[field] not in choices:
            errors.append(f"interaction.{field} must be one of: {', '.join(sorted(choices))}")
    return errors


def validate_flow(values: dict[str, Any]) -> list[str]:
    """Validate the deliberately bounded role and JIT selector configuration."""
    flow = values.get("flow")
    if flow is None:
        return []
    if not isinstance(flow, dict):
        return ["flow must be an object"]
    unknown = sorted(set(flow) - FLOW_FIELDS)
    errors = [f"flow has unknown fields: {', '.join(unknown)}"] if unknown else []
    aliases = flow.get("role_aliases", {})
    canonical = {
        "business-analyst",
        "product-manager",
        "software-architect",
        "software-engineer",
        "qa-engineer",
    }
    actions = {
        "branching",
        "commit",
        "implementation",
        "new_refinement",
        "qa_planning",
        "review",
        "security_review",
        "story_decomposition",
        "validation",
    }
    if not isinstance(aliases, dict):
        errors.append("flow.role_aliases must be an object")
    else:
        for alias, role in aliases.items():
            if (
                not isinstance(alias, str)
                or not re.fullmatch(r"[a-z][a-z0-9-]{0,39}", alias)
                or role not in canonical
            ):
                errors.append(f"flow.role_aliases has invalid mapping: {alias!r} -> {role!r}")
    if flow.get("menu_mode", "ambiguous") not in {"ambiguous", "always"}:
        errors.append("flow.menu_mode must be one of: always, ambiguous")
    selectors = flow.get("context_selectors", [])
    if not isinstance(selectors, list):
        return errors + ["flow.context_selectors must be an array"]
    seen: set[str] = set()
    for index, selector in enumerate(selectors):
        prefix = f"flow.context_selectors[{index}]"
        if not isinstance(selector, dict):
            errors.append(f"{prefix} must be an object")
            continue
        extra = sorted(set(selector) - FLOW_SELECTOR_FIELDS)
        missing = sorted(FLOW_SELECTOR_FIELDS - set(selector))
        if extra:
            errors.append(f"{prefix} has unknown fields: {', '.join(extra)}")
        if missing:
            errors.append(f"{prefix} is missing fields: {', '.join(missing)}")
            continue
        selector_id = selector["id"]
        if not isinstance(selector_id, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", selector_id):
            errors.append(f"{prefix}.id must be kebab-case")
        elif selector_id in seen:
            errors.append(f"{prefix}.id must be unique")
        seen.add(str(selector_id))
        for field in ("roles", "actions", "include"):
            if (
                not isinstance(selector[field], list)
                or not all(isinstance(item, str) and item for item in selector[field])
                or len(selector[field]) != len(set(selector[field]))
            ):
                errors.append(f"{prefix}.{field} must be a non-empty-string array")
        if isinstance(selector["roles"], list):
            unknown_roles = sorted(
                item for item in selector["roles"] if item not in canonical
            )
            if unknown_roles:
                errors.append(
                    f"{prefix}.roles has unknown roles: {', '.join(unknown_roles)}"
                )
        if isinstance(selector["actions"], list):
            unknown_actions = sorted(
                item for item in selector["actions"] if item not in actions
            )
            if unknown_actions:
                errors.append(
                    f"{prefix}.actions has unknown actions: {', '.join(unknown_actions)}"
                )
        if isinstance(selector["include"], list):
            for relative in selector["include"]:
                if not isinstance(relative, str):
                    continue
                candidate = Path(relative)
                if (
                    candidate.is_absolute()
                    or ".." in candidate.parts
                    or not candidate.parts
                    or candidate.parts[0] not in {"references", "steps"}
                ):
                    errors.append(
                        f"{prefix}.include has unsafe flow-package path: {relative}"
                    )
        if not isinstance(selector["priority"], int) or isinstance(selector["priority"], bool) or not 0 <= selector["priority"] <= 100:
            errors.append(f"{prefix}.priority must be an integer from 0 to 100")
        if not isinstance(selector["max_tokens"], int) or isinstance(selector["max_tokens"], bool) or not 16 <= selector["max_tokens"] <= 4000:
            errors.append(f"{prefix}.max_tokens must be an integer from 16 to 4000")
        if not isinstance(selector["reason"], str) or not 8 <= len(selector["reason"]) <= 240:
            errors.append(f"{prefix}.reason must contain 8 to 240 characters")
    return errors


def render_toon(values: dict[str, Any], provenance: dict[str, str], protected: list[str]) -> str:
    """Render bounded machine output with leaf provenance."""
    flat = flatten(values)
    lines = ["schema: ai-sdlc-config-resolution/v1", f"config_schema: {SCHEMA}", "precedence: base/team/user", "", f"values[{len(flat)}]{{path,value,source,protected}}:"]
    lines.extend("  " + ",".join((path, toon(flat[path]), provenance[path], "yes" if path in protected else "no")) for path in sorted(flat))
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(values: dict[str, Any], provenance: dict[str, str], protected: list[str]) -> str:
    """Render human-readable resolved configuration."""
    flat = flatten(values)
    lines = ["# AI SDLC Resolved Configuration", "", f"- Schema: `{SCHEMA}`", "- Precedence: `base < team < user`", "", "| Path | Value | Source | Protected |", "| --- | --- | --- | --- |"]
    lines.extend(f"| `{path}` | `{json.dumps(flat[path], sort_keys=True)}` | `{provenance[path]}` | `{'yes' if path in protected else 'no'}` |" for path in sorted(flat))
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one resolved projection atomically."""
    if any(component.is_symlink() for component in (path, *list(path.parents)[:4])):
        raise SystemExit(f"ERROR: output path contains symlink component: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    """Resolve configuration and emit values with provenance."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=packaged_defaults())
    parser.add_argument("--team", type=Path)
    parser.add_argument("--user", type=Path)
    parser.add_argument("--format", choices=("markdown", "toon", "json"), default="markdown")
    parser.add_argument("--write-root", type=Path)
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
        print("ERROR: configuration resolution is read-only; it cannot change lifecycle state")
        return 1
    layers: list[dict[str, Any]] = []
    errors: list[str] = []
    for path, name in ((args.base, "base"), (args.team, "team"), (args.user, "user")):
        layer, layer_errors = load_layer(path, name, path is not None)
        layers.append(layer)
        errors.extend(layer_errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    values, provenance, resolve_errors = resolve(*layers)
    resolve_errors.extend(validate_interaction(values))
    resolve_errors.extend(validate_flow(values))
    if resolve_errors:
        for error in resolve_errors:
            print(f"ERROR: {error}")
        return 1
    protected = list(layers[0].get("protected", []))
    machine = render_toon(values, provenance, protected)
    human = render_markdown(values, provenance, protected)
    payload = json.dumps({"schema": "ai-sdlc-config-resolution/v1", "config_schema": SCHEMA, "values": values, "provenance": provenance, "protected": protected}, indent=2, sort_keys=True) + "\n"
    if args.write_root:
        atomic_write(args.write_root / "config.resolved.json", payload)
        atomic_write(args.write_root / "_ai_sdlc/config-provenance.toon", machine)
    print(payload if args.format == "json" else machine if args.format == "toon" else human, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
