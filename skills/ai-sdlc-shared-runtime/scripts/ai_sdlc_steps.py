#!/usr/bin/env python3
"""Validate and select skill-owned procedural steps just in time."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SCHEMA = "ai-sdlc-skill-steps/v1"
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
SELECTOR_FIELDS = {
    "id",
    "path",
    "phases",
    "roles",
    "actions",
    "load",
    "max_tokens",
    "reason",
}


@dataclass(frozen=True)
class StepSelection:
    schema: str
    skill: str
    phase: str
    role: str
    action: str
    selected: tuple[str, ...]
    skipped: tuple[str, ...]
    selected_tokens: int
    broad_tokens: int
    savings_percent: float
    manifest_fingerprint: str
    selection_fingerprint: str


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _unique_strings(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def resolve_skill_root(root: Path, skill: str) -> Path:
    """Resolve one installed skill without accepting caller-selected paths."""
    if not re.fullmatch(r"ai-sdlc-[a-z0-9]+(?:-[a-z0-9]+)*", skill):
        raise ValueError(f"STEP_UNKNOWN_SKILL: invalid skill id {skill!r}")
    packaged = Path(__file__).resolve().parents[2]
    target_candidates = (
        root.resolve() / "skills" / skill,
        root.resolve() / ".agents" / "skills" / skill,
    )
    seen: set[Path] = set()
    for candidate in target_candidates:
        if candidate.is_symlink():
            raise ValueError(f"STEP_INVALID_MANIFEST: unsafe target skill directory for {skill}")
        if not candidate.exists():
            continue
        if not candidate.is_dir():
            raise ValueError(f"STEP_INVALID_MANIFEST: unsafe target skill directory for {skill}")
        if (candidate / "SKILL.md").is_symlink() or not (candidate / "SKILL.md").is_file():
            raise ValueError(f"STEP_INVALID_MANIFEST: target skill {skill} is missing SKILL.md")
        if not (candidate / "steps" / "manifest.json").is_file():
            raise ValueError(
                f"STEP_INVALID_MANIFEST: target skill {skill} is missing steps/manifest.json"
            )
        return candidate.resolve()
    for candidate in (packaged / skill,):
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if (
            candidate.is_dir()
            and not candidate.is_symlink()
            and not (candidate / "SKILL.md").is_symlink()
            and (candidate / "SKILL.md").is_file()
            and (candidate / "steps" / "manifest.json").is_file()
        ):
            return resolved
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
        raise ValueError(f"STEP_UNSAFE_PATH: step escapes {skill_root.name}: {relative}") from exc
    if path.is_symlink() or not resolved.is_file():
        raise ValueError(f"STEP_UNSAFE_PATH: step must be a regular non-symlink file: {relative}")
    return resolved


def load_manifest(root: Path, skill: str) -> tuple[Path, dict[str, object]]:
    """Load and fully validate one skill-owned selector manifest."""
    skill_root = resolve_skill_root(root, skill)
    path = skill_root / "steps" / "manifest.json"
    if path.is_symlink() or not path.is_file():
        raise ValueError("STEP_INVALID_MANIFEST: manifest must be a regular non-symlink file")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"STEP_INVALID_MANIFEST: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "skill", "selectors"}:
        raise ValueError("STEP_INVALID_MANIFEST: expected schema, skill, and selectors fields")
    if value["schema"] != SCHEMA:
        raise ValueError(f"STEP_INVALID_MANIFEST: schema must be {SCHEMA}")
    if value["skill"] != skill:
        raise ValueError(
            f"STEP_INVALID_MANIFEST: skill field {value['skill']!r} does not match {skill!r}"
        )
    selectors = value["selectors"]
    if not isinstance(selectors, list) or not selectors:
        raise ValueError("STEP_INVALID_MANIFEST: selectors must be a non-empty array")
    selector_ids: set[str] = set()
    paths: set[str] = set()
    validated_selectors: list[dict[str, object]] = []
    router = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    for index, selector in enumerate(selectors):
        prefix = f"STEP_INVALID_MANIFEST: selectors[{index}]"
        if not isinstance(selector, dict) or set(selector) != SELECTOR_FIELDS:
            raise ValueError(f"{prefix} has invalid fields")
        selector_id = selector["id"]
        if (
            not isinstance(selector_id, str)
            or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", selector_id)
            or selector_id in selector_ids
        ):
            raise ValueError(f"{prefix}.id must be unique kebab-case")
        selector_ids.add(selector_id)
        relative = selector["path"]
        if not isinstance(relative, str) or relative in paths:
            raise ValueError(f"{prefix}.path must be a unique string")
        paths.add(relative)
        step_path = _contained_file(skill_root, relative)
        if f"]({relative})" not in router:
            raise ValueError(f"{prefix}.path is not linked from SKILL.md: {relative}")
        for field in ("phases", "roles", "actions"):
            if not _unique_strings(selector[field], nonempty=field == "phases"):
                raise ValueError(f"{prefix}.{field} must be a unique string array")
        unknown_phases = sorted(set(selector["phases"]) - PHASE_IDS)
        unknown_roles = sorted(set(selector["roles"]) - ROLE_IDS)
        if unknown_phases:
            raise ValueError(f"{prefix}.phases has unknown values: {', '.join(unknown_phases)}")
        if unknown_roles:
            raise ValueError(f"{prefix}.roles has unknown values: {', '.join(unknown_roles)}")
        if selector["load"] not in LOAD_RULES:
            raise ValueError(f"{prefix}.load must be required, on-demand, or before-completion")
        max_tokens = selector["max_tokens"]
        if (
            not isinstance(max_tokens, int)
            or isinstance(max_tokens, bool)
            or not 64 <= max_tokens <= 5000
        ):
            raise ValueError(f"{prefix}.max_tokens must be an integer from 64 to 5000")
        reason = selector["reason"]
        if not isinstance(reason, str) or not 8 <= len(reason) <= 240:
            raise ValueError(f"{prefix}.reason must contain 8 to 240 characters")
        tokens = (len(step_path.read_text(encoding="utf-8")) + 3) // 4
        if tokens > max_tokens:
            raise ValueError(
                f"STEP_TOKEN_OVERFLOW: {relative} uses {tokens} tokens; cap is {max_tokens}"
            )
        for previous in validated_selectors:
            phases_overlap = bool(
                set(selector["phases"]) & set(previous["phases"])  # type: ignore[arg-type]
            )
            roles_overlap = (
                not selector["roles"]
                or not previous["roles"]
                or bool(
                    set(selector["roles"]) & set(previous["roles"])  # type: ignore[arg-type]
                )
            )
            actions_overlap = (
                not selector["actions"]
                or not previous["actions"]
                or bool(
                    set(selector["actions"]) & set(previous["actions"])  # type: ignore[arg-type]
                )
            )
            if phases_overlap and roles_overlap and actions_overlap:
                raise ValueError(
                    "STEP_INVALID_MANIFEST: overlapping selectors "
                    f"{previous['id']!r} and {selector_id!r}"
                )
        validated_selectors.append(selector)
    actual_paths = {
        path.relative_to(skill_root).as_posix()
        for path in (skill_root / "steps").glob("*.md")
    }
    undeclared = sorted(actual_paths - paths)
    if undeclared:
        raise ValueError(
            "STEP_INVALID_MANIFEST: undeclared step files: " + ", ".join(undeclared)
        )
    return skill_root, value


def select_steps(
    root: Path,
    skill: str,
    phase: str,
    *,
    role: str = "",
    action: str = "",
) -> StepSelection:
    """Select the smallest matching procedural step set."""
    if phase not in PHASE_IDS:
        raise ValueError(f"STEP_UNKNOWN_PHASE: {phase}")
    if role and role not in ROLE_IDS:
        raise ValueError(f"STEP_UNKNOWN_ROLE: {role}")
    skill_root, manifest = load_manifest(root, skill)
    selected: list[str] = []
    skipped: list[str] = []
    selected_tokens = 0
    broad_tokens = 0
    for selector in manifest["selectors"]:  # type: ignore[index]
        path = _contained_file(skill_root, str(selector["path"]))
        tokens = (len(path.read_text(encoding="utf-8")) + 3) // 4
        broad_tokens += tokens
        phase_match = phase in selector["phases"]
        role_match = not role or not selector["roles"] or role in selector["roles"]
        action_match = (
            not action or not selector["actions"] or action in selector["actions"]
        )
        if phase_match and role_match and action_match:
            selected_tokens += tokens
            selected.append(
                f"{skill}/{selector['path']}:{hashlib.sha256(path.read_bytes()).hexdigest()}:"
                f"{tokens}:{selector['load']}:{selector['reason']}"
            )
        else:
            reasons = []
            if not phase_match:
                reasons.append("phase")
            if not role_match:
                reasons.append("role")
            if not action_match:
                reasons.append("action")
            skipped.append(f"{selector['id']}:{'/'.join(reasons)} mismatch")
    if not selected:
        raise ValueError(
            f"STEP_NO_MATCH: {skill} has no selector for phase={phase}, "
            f"role={role or '*'}, action={action or '*'}"
        )
    savings = round(
        ((broad_tokens - selected_tokens) / broad_tokens * 100.0)
        if broad_tokens
        else 0.0,
        2,
    )
    manifest_fingerprint = _digest(manifest)
    selection_fingerprint = _digest(
        {
            "manifest": manifest_fingerprint,
            "skill": skill,
            "phase": phase,
            "role": role,
            "action": action,
            "selected": selected,
            "skipped": skipped,
        }
    )
    return StepSelection(
        schema=SCHEMA,
        skill=skill,
        phase=phase,
        role=role,
        action=action,
        selected=tuple(selected),
        skipped=tuple(skipped),
        selected_tokens=selected_tokens,
        broad_tokens=broad_tokens,
        savings_percent=savings,
        manifest_fingerprint=manifest_fingerprint,
        selection_fingerprint=selection_fingerprint,
    )


def render_toon(selection: StepSelection) -> str:
    values = asdict(selection)
    return "\n".join(
        f"{key}: "
        + (
            json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            if isinstance(value, (dict, list, tuple))
            else str(value)
        )
        for key, value in values.items()
    ) + "\n"


def validate_all(root: Path) -> tuple[str, ...]:
    """Validate every installable skill visible in the selected layout."""
    packaged = Path(__file__).resolve().parents[2]
    candidates = (
        root.resolve() / "skills",
        root.resolve() / ".agents" / "skills",
        packaged,
    )
    names: set[str] = set()
    for candidate in candidates:
        if not candidate.is_dir() or candidate.is_symlink():
            continue
        names.update(
            path.name
            for path in candidate.iterdir()
            if path.is_dir() and not path.is_symlink() and (path / "SKILL.md").is_file()
        )
    if not names:
        raise ValueError("STEP_UNKNOWN_SKILL: no installable skills found")
    for skill in sorted(names):
        load_manifest(root, skill)
    return tuple(sorted(names))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--skill")
    parser.add_argument("--phase", choices=sorted(PHASE_IDS))
    parser.add_argument("--role", default="")
    parser.add_argument("--action", default="")
    parser.add_argument(
        "--validate-all",
        action="store_true",
        help="validate every installed skill manifest without selecting a phase",
    )
    parser.add_argument("--format", choices=("json", "toon"), default="toon")
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
        if args.validate_all:
            names = validate_all(args.root.resolve())
            result = {
                "schema": "ai-sdlc-skill-step-inventory/v1",
                "skills": len(names),
                "skill_names": names,
                "result": "valid",
            }
            if args.format == "json":
                print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            else:
                print(
                    "\n".join(
                        (
                            f"schema: {result['schema']}",
                            f"skills: {result['skills']}",
                            "skill_names: "
                            + json.dumps(names, ensure_ascii=False, separators=(",", ":")),
                            "result: valid",
                        )
                    )
                )
            return 0
        if not args.skill or not args.phase:
            parser.error("--skill and --phase are required unless --validate-all is used")
        result = select_steps(
            args.root.resolve(),
            args.skill,
            args.phase,
            role=args.role,
            action=args.action,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    else:
        print(render_toon(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
