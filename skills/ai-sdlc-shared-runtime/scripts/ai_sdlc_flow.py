#!/usr/bin/env python3
"""Deterministic role-guided contracts for the AI SDLC Explore -> Apply flow."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import ai_sdlc_steps


SCHEMA = "ai-sdlc-flow/v2"
REGISTRY_SCHEMA = "ai-sdlc-flow-selectors/v1"
REFINEMENT_ROOT = "specs-refiniment"
IMPLEMENTATION_ROOT = "specs"
PACK_SAVINGS_MINIMUM = 15.0
COMPLETE_STATUSES = {"done", "skipped", "not_applicable"}
DEFAULT_BASE_BRANCHES = {"dev", "main", "master"}
ROLE_IDS = ("business-analyst", "product-manager", "software-architect", "software-engineer", "qa-engineer")
STAGE_PREDECESSORS: dict[str, tuple[str, ...]] = {
    "discovery": (),
    "prfaq": ("discovery",),
    "delivery_package_gap_review": ("prfaq",),
    "requirements_readiness": ("delivery_package_gap_review",),
    "goal_epic_mapping": ("requirements_readiness",),
    "backlog_gap_review": ("goal_epic_mapping",),
    "backlog_decomposition": ("backlog_gap_review",),
    "story_decomposition": ("backlog_decomposition",),
    "qa_plan": ("requirements_readiness",),
    "qa_gap_review": ("qa_plan",),
    "branching": (),
    "sdd": ("branching",),
    "validation": ("sdd",),
    "code_review": ("validation",),
    "security_testing": ("sdd",),
    "commit_prep": ("code_review",),
}


@dataclass(frozen=True)
class ContextEconomics:
    raw_tokens: int
    packed_tokens: int
    reread_tokens: int
    net_tokens: int
    savings_tokens: int
    savings_percent: float
    critical_total: int
    critical_retained: int
    recall_percent: float
    selected_strategy: str
    reason: str


@dataclass(frozen=True)
class DecisionCard:
    schema: str
    mode: str
    repo_id: str
    intent: str
    intent_class: str
    intent_confidence: float
    intent_reason: str
    feature: str
    workspace: str
    stage: str
    skill: str
    rigor: str
    rigor_reason: str
    roles: tuple[str, ...]
    role_evidence: tuple[str, ...]
    project_context: str
    sources: tuple[str, ...]
    context_economics: ContextEconomics
    blockers: tuple[str, ...]
    planned_writes: tuple[str, ...]
    next_checkpoint: str
    fingerprint: str
    requested_role: str
    active_role: str
    role_handoff_reason: str
    action_id: str
    action_code: str
    menu_options: tuple[str, ...]
    current_step: str
    step_reference: str
    selected_references: tuple[str, ...]
    skipped_references: tuple[str, ...]
    selector_fingerprint: str
    config_fingerprint: str
    skill_step_reference: str
    step_manifest_fingerprint: str


@dataclass(frozen=True)
class JitReferenceSelection:
    selected: tuple[str, ...]
    skipped: tuple[str, ...]
    fingerprint: str
    selected_tokens: int
    broad_tokens: int
    skill_step_reference: str
    step_manifest_fingerprint: str


INTENT_RULES: tuple[tuple[str, tuple[str, ...], str, str, str], ...] = (
    ("commit", ("commit", "stage changes"), "implementation", "commit_prep", "ai-sdlc-commit-prep"),
    ("security_review", ("security", "owasp", "authz", "abuse case"), "implementation", "security_testing", "ai-sdlc-security-testing"),
    ("new_refinement", ("feedback", "refinement", "new feature", "new request", "idea", "customer problem", "product", "discover"), "refinement", "discovery", "ai-sdlc-working-backwards-discovery"),
    ("qa_planning", ("testability", "qa coverage", "test plan"), "refinement", "qa_gap_review", "ai-sdlc-qa-requirements-gap-review"),
    ("story_decomposition", ("story", "backlog", "epic"), "refinement", "story_decomposition", "ai-sdlc-user-story-decomposition"),
    ("review", ("code review", "review diff", "review pr", "review code", "review"), "implementation", "code_review", "ai-sdlc-code-review"),
    ("validation", ("validate", "validation", "regression", "smoke test"), "implementation", "validation", "ai-sdlc-validation"),
    ("implementation", ("implement", "fix", "bug", "refactor", "api", "architecture"), "implementation", "sdd", "ai-sdlc-sdd"),
)


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _string_array(value: object) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def _validate_selector_records(
    selectors: object,
    *,
    role_ids: set[str],
    action_ids: set[str],
    source: str,
) -> None:
    """Validate selector shapes before routing can index their fields."""
    if not isinstance(selectors, list):
        raise ValueError(f"{source}: selectors must be an array")
    seen: set[str] = set()
    fields = {"id", "roles", "actions", "include", "priority", "max_tokens", "reason"}
    for index, selector in enumerate(selectors):
        prefix = f"{source}[{index}]"
        if not isinstance(selector, dict) or set(selector) != fields:
            raise ValueError(f"{prefix}: invalid selector fields")
        selector_id = selector["id"]
        if (
            not isinstance(selector_id, str)
            or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", selector_id)
            or selector_id in seen
        ):
            raise ValueError(f"{prefix}.id: expected a unique kebab-case id")
        seen.add(selector_id)
        for field in ("roles", "actions", "include"):
            if not _string_array(selector[field]):
                raise ValueError(f"{prefix}.{field}: expected a unique non-empty-string array")
        unknown_roles = sorted(set(selector["roles"]) - role_ids)
        unknown_actions = sorted(set(selector["actions"]) - action_ids)
        if unknown_roles:
            raise ValueError(f"{prefix}.roles: unknown roles: {', '.join(unknown_roles)}")
        if unknown_actions:
            raise ValueError(f"{prefix}.actions: unknown actions: {', '.join(unknown_actions)}")
        for relative in selector["include"]:
            candidate = Path(relative)
            if (
                candidate.is_absolute()
                or ".." in candidate.parts
                or not candidate.parts
                or candidate.parts[0] not in {"references", "steps"}
            ):
                raise ValueError(f"{prefix}.include: unsafe flow-package path: {relative}")
        priority = selector["priority"]
        max_tokens = selector["max_tokens"]
        if (
            not isinstance(priority, int)
            or isinstance(priority, bool)
            or not 0 <= priority <= 100
        ):
            raise ValueError(f"{prefix}.priority: expected an integer from 0 to 100")
        if (
            not isinstance(max_tokens, int)
            or isinstance(max_tokens, bool)
            or not 16 <= max_tokens <= 4000
        ):
            raise ValueError(f"{prefix}.max_tokens: expected an integer from 16 to 4000")
        reason = selector["reason"]
        if not isinstance(reason, str) or not 8 <= len(reason) <= 240:
            raise ValueError(f"{prefix}.reason: expected 8 to 240 characters")


def flow_skill_root(root: Path | None = None) -> Path:
    """Resolve the flow package in a checkout or installed skill set."""
    candidates = []
    if root is not None:
        candidates.extend((root.resolve() / "skills" / "ai-sdlc-flow", root.resolve() / ".agents" / "skills" / "ai-sdlc-flow"))
    candidates.append(Path(__file__).resolve().parents[2] / "ai-sdlc-flow")
    for candidate in candidates:
        if (candidate / "references" / "selector-registry.json").is_file():
            return candidate.resolve()
    raise ValueError("FLOW_REGISTRY_MISSING: ai-sdlc-flow selector registry was not found")


def load_registry(root: Path | None = None, path: Path | None = None) -> dict[str, object]:
    """Load and validate the trusted declarative selector registry."""
    skill_root = flow_skill_root(root)
    registry_path = (path or skill_root / "references" / "selector-registry.json").resolve()
    try:
        registry_path.relative_to(skill_root)
    except ValueError as exc:
        raise ValueError("FLOW_UNSAFE_SELECTOR: registry must remain inside ai-sdlc-flow") from exc
    if registry_path.is_symlink() or not registry_path.is_file():
        raise ValueError("FLOW_UNSAFE_SELECTOR: registry must be a regular non-symlink file")
    try:
        value = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"FLOW_INVALID_REGISTRY: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema") != REGISTRY_SCHEMA:
        raise ValueError(f"FLOW_INVALID_REGISTRY: schema must be {REGISTRY_SCHEMA}")
    roles = value.get("roles")
    actions = value.get("actions")
    selectors = value.get("selectors")
    if not all(isinstance(item, list) for item in (roles, actions, selectors)):
        raise ValueError("FLOW_INVALID_REGISTRY: roles, actions, and selectors must be arrays")
    role_fields = {"id", "label", "aliases"}
    if any(not isinstance(item, dict) or set(item) != role_fields for item in roles):
        raise ValueError("FLOW_INVALID_REGISTRY: invalid role fields")
    role_ids = [item["id"] for item in roles]
    if tuple(role_ids) != ROLE_IDS or len(set(role_ids)) != len(ROLE_IDS):
        raise ValueError("FLOW_INVALID_REGISTRY: exactly five canonical roles are required in stable order")
    for index, role in enumerate(roles):
        if (
            not isinstance(role["label"], str)
            or not role["label"]
            or not _string_array(role["aliases"])
        ):
            raise ValueError(f"FLOW_INVALID_REGISTRY: invalid role record at index {index}")
    action_fields = {"id", "code", "skill", "role", "workspace", "stage", "step"}
    action_ids: list[str] = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict) or set(action) != action_fields:
            raise ValueError(f"FLOW_INVALID_REGISTRY: invalid action fields at index {index}")
        if not all(isinstance(action[field], str) and action[field] for field in action_fields):
            raise ValueError(f"FLOW_INVALID_REGISTRY: action values must be non-empty strings at index {index}")
        if action["role"] not in ROLE_IDS:
            raise ValueError(f"FLOW_INVALID_REGISTRY: unknown action role {action['role']}")
        if action["workspace"] not in {"refinement", "implementation"}:
            raise ValueError(f"FLOW_INVALID_REGISTRY: invalid action workspace {action['workspace']}")
        step = Path(action["step"])
        if step.is_absolute() or ".." in step.parts or step.parts[:1] != ("steps",):
            raise ValueError(f"FLOW_INVALID_REGISTRY: unsafe action step {action['step']}")
        action_ids.append(action["id"])
    if len(action_ids) != len(set(action_ids)):
        raise ValueError("FLOW_INVALID_REGISTRY: action ids must be unique")
    try:
        _validate_selector_records(
            selectors,
            role_ids=set(ROLE_IDS),
            action_ids=set(action_ids),
            source="FLOW_INVALID_REGISTRY: selectors",
        )
    except ValueError as exc:
        raise ValueError(str(exc)) from exc
    return value


def classify_intent(intent: str) -> tuple[str, str, str, str, tuple[str, ...]]:
    normalized = " ".join(intent.lower().split())
    matches = [
        (name, workspace, stage, skill, keyword)
        for name, keywords, workspace, stage, skill in INTENT_RULES
        for keyword in keywords
        if keyword in normalized
    ]
    classes = {item[0] for item in matches}
    if "review" in classes and len(classes) > 1:
        matches = [item for item in matches if item[0] != "review"]
        classes = {item[0] for item in matches}
    if len(classes) > 1:
        return "ambiguous", "", "", "", ("FLOW_AMBIGUOUS_INTENT: request matches " + "/".join(sorted(classes)),)
    if matches:
        name, workspace, stage, skill, keyword = matches[0]
        return name, workspace, stage, skill, (f"intent signal: {keyword}",)
    return "ambiguous", "", "", "", ("FLOW_AMBIGUOUS_INTENT: select one action from the menu",)


def discover_skills(root: Path) -> tuple[frozenset[str], tuple[str, ...]]:
    packaged = Path(__file__).resolve().parents[2]
    candidates = (("source", root.resolve() / "skills"), ("project", root.resolve() / ".agents" / "skills"), ("packaged", packaged))
    names: set[str] = set()
    roots: list[str] = []
    seen: set[Path] = set()
    for label, candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen or not resolved.is_dir():
            continue
        seen.add(resolved)
        found = {path.name for path in resolved.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()}
        if found:
            names.update(found)
            roots.append(f"{label}={resolved.as_posix()}")
    return frozenset(names), tuple(roots)


def current_branch(root: Path) -> str:
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.stdout.strip()


def state_route(root: Path, feature: str, workspace: str, requested_skill: str) -> tuple[str, str, str, str] | None:
    base = REFINEMENT_ROOT if workspace == "refinement" else IMPLEMENTATION_ROOT
    path = root.resolve() / base / feature / "_ai_sdlc" / "state.toon"
    if not path.is_file():
        return None
    state: dict[str, object] = {"stages": []}
    in_stages = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("stages["):
            in_stages = True
            continue
        if line.startswith("skips["):
            in_stages = False
            continue
        if in_stages and line.startswith("  "):
            values = [value.strip() for value in line.strip().split(",")]
            values.extend([""] * (6 - len(values)))
            state["stages"].append(dict(zip(("id", "skill", "status", "workspace", "artifacts", "decision_ref"), values)))  # type: ignore[union-attr]
        elif not line.startswith("  ") and ":" in line:
            key, value = line.split(":", 1)
            state[key.strip()] = value.strip()
    state_workspace = str(state.get("workspace") or workspace)
    stages = [row for row in state["stages"] if isinstance(row, dict) and row.get("workspace") == state_workspace]  # type: ignore[index]
    active = str(state.get("active_skill", "")).strip()
    if active:
        row = next((item for item in stages if item.get("skill") == active), {})
        return state_workspace, str(row.get("id") or state.get("current_stage") or ""), active, f"active feature state: {active}"
    rows_by_id = {str(item.get("id", "")): item for item in stages}
    requested = next((item for item in stages if item.get("skill") == requested_skill), None)
    if not requested:
        return None

    def earliest_missing(stage_id: str) -> dict[str, str] | None:
        for predecessor in STAGE_PREDECESSORS.get(stage_id, ()):
            row = rows_by_id.get(predecessor)
            if not row or str(row.get("status", "")) in COMPLETE_STATUSES:
                continue
            return earliest_missing(predecessor) or row
        return None

    prerequisite = earliest_missing(str(requested.get("id", "")))
    if prerequisite:
        return state_workspace, str(prerequisite.get("id", "")), str(prerequisite.get("skill", "")), f"earliest incomplete prerequisite stage: {prerequisite.get('id', '')}"
    return None


def select_roles(intent: str, *, stage: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Compatibility projection: return exactly one canonical active role."""
    intent_class, _, _, _, _ = classify_intent(intent)
    role = {
        "new_refinement": "business-analyst",
        "story_decomposition": "product-manager",
        "security_review": "software-architect",
        "qa_planning": "qa-engineer",
        "validation": "qa-engineer",
    }.get(intent_class, "software-engineer")
    return (role,), (f"{role}: owns {stage or intent_class}",)


def select_rigor(intent: str, *, requested: str | None = None, policy_requires_full: bool = False) -> tuple[str, str, tuple[str, ...]]:
    high_risk = any(word in intent.lower() for word in ("architecture", "migration", "security", "authorization", "cross-cutting", "ambiguous"))
    automatic = "full" if high_risk else "quick"
    effective = requested or automatic
    reason = f"automatic {automatic}: " + ("cross-cutting or risk signal" if high_risk else "bounded low-risk intent")
    if requested:
        reason += f"; explicit {requested} override"
    if policy_requires_full and effective == "quick":
        effective, reason = "full", reason + "; upgraded because policy requires full"
    if effective not in {"quick", "full"}:
        return "full", reason, (f"FLOW_UNSAFE_RIGOR: unsupported rigor {effective}",)
    return effective, reason, ()


def choose_context(*, raw_tokens: int, packed_tokens: int, reread_tokens: int, critical_total: int, critical_retained: int) -> ContextEconomics:
    values = (raw_tokens, packed_tokens, reread_tokens, critical_total, critical_retained)
    if any(value < 0 for value in values) or critical_retained > critical_total:
        raise ValueError("FLOW_INVALID_CONTEXT: invalid token or critical-anchor counts")
    net = packed_tokens + reread_tokens
    savings = raw_tokens - net
    percent = round((savings / raw_tokens * 100.0) if raw_tokens else 0.0, 2)
    recall = round((critical_retained / critical_total * 100.0) if critical_total else 100.0, 2)
    accepted = recall == 100.0 and percent >= PACK_SAVINGS_MINIMUM
    reason = "100% critical-anchor recall and net savings meet the 15% threshold" if accepted else "; ".join(filter(None, ("critical-anchor recall is below 100%" if recall < 100 else "", "net savings including rereads are below 15%" if percent < 15 else "")))
    return ContextEconomics(raw_tokens, packed_tokens, reread_tokens, net, savings, percent, critical_total, critical_retained, recall, "packed" if accepted else "direct", reason)


def validate_workspace(root: Path, feature: str, workspace: str) -> tuple[Path | None, tuple[str, ...]]:
    if not re.fullmatch(r"\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", feature):
        return None, ("FLOW_UNSAFE_ROOT: feature must match NNN-kebab-case",)
    base_path = root / (REFINEMENT_ROOT if workspace == "refinement" else IMPLEMENTATION_ROOT)
    base = base_path.resolve()
    candidate = base / feature
    blockers: list[str] = []
    if base_path.is_symlink():
        blockers.append("FLOW_UNSAFE_ROOT: canonical workspace root must not be a symlink")
    if candidate.exists() and candidate.is_symlink():
        blockers.append("FLOW_UNSAFE_ROOT: feature root must not be a symlink")
    try:
        candidate.resolve(strict=False).relative_to(base)
    except ValueError:
        blockers.append("FLOW_UNSAFE_ROOT: feature root escapes its canonical workspace")
    return (None, tuple(blockers)) if blockers else (candidate, ())


def source_hashes(root: Path, paths: Iterable[Path]) -> tuple[str, ...]:
    records: list[str] = []
    root = root.resolve()
    for path in paths:
        resolved = path.resolve()
        resolved.relative_to(root)
        records.append(f"{resolved.relative_to(root).as_posix()}:{hashlib.sha256(resolved.read_bytes()).hexdigest()}")
    return tuple(sorted(records))


def discover_sources(root: Path, feature: str, explicit: Iterable[Path] = ()) -> tuple[str, ...]:
    root = root.resolve()
    mandatory = (
        root / "modules/core/module.json", root / "config/ai-sdlc.defaults.json",
        root / "config/ai-sdlc-managed-skills.txt", root / "_ai_sdlc/context/project-context.md",
        root / REFINEMENT_ROOT / "_ai_sdlc/specs-index.toon",
        root / REFINEMENT_ROOT / feature / "_ai_sdlc/state.toon",
        root / IMPLEMENTATION_ROOT / "_ai_sdlc/specs-index.toon",
        root / IMPLEMENTATION_ROOT / feature / "_ai_sdlc/state.toon",
    )
    return source_hashes(root, tuple(dict.fromkeys((*filter(Path.is_file, mandatory), *explicit))))


def project_context_status(root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    path = root.resolve() / "_ai_sdlc/context/project-context.md"
    return f"present:sha256:{hashlib.sha256(path.read_bytes()).hexdigest()[:12]}" if path.is_file() else "not-found"


def _action_maps(registry: dict[str, object]) -> tuple[dict[str, dict[str, object]], dict[str, dict[str, object]]]:
    actions = [item for item in registry["actions"] if isinstance(item, dict)]  # type: ignore[index]
    return ({str(item["id"]): item for item in actions}, {str(item["skill"]): item for item in actions})


def _validated_flow_config(
    value: dict[str, object] | None,
    *,
    registry: dict[str, object],
) -> dict[str, object]:
    """Validate direct API configuration as strictly as the CLI boundary."""
    config = value or {}
    if not isinstance(config, dict):
        raise ValueError("FLOW_INVALID_CONFIG: flow must be an object")
    unknown = sorted(set(config) - {"role_aliases", "menu_mode", "context_selectors"})
    if unknown:
        raise ValueError(f"FLOW_INVALID_CONFIG: unknown fields: {', '.join(unknown)}")
    aliases = config.get("role_aliases", {})
    if not isinstance(aliases, dict):
        raise ValueError("FLOW_INVALID_CONFIG: role_aliases must be an object")
    for alias, role in aliases.items():
        if (
            not isinstance(alias, str)
            or not re.fullmatch(r"[a-z][a-z0-9-]{0,39}", alias)
            or role not in ROLE_IDS
        ):
            raise ValueError(f"FLOW_INVALID_CONFIG: invalid role alias {alias!r} -> {role!r}")
    if config.get("menu_mode", "ambiguous") not in {"ambiguous", "always"}:
        raise ValueError("FLOW_INVALID_CONFIG: menu_mode must be always or ambiguous")
    actions, _skills = _action_maps(registry)
    _validate_selector_records(
        config.get("context_selectors", []),
        role_ids=set(ROLE_IDS),
        action_ids=set(actions),
        source="FLOW_INVALID_CONFIG: context_selectors",
    )
    return config


def _resolve_requested_role(value: str | None, registry: dict[str, object], config: dict[str, object]) -> str:
    if not value:
        return ""
    normalized = value.strip().lower()
    aliases = config.get("role_aliases", {})
    if isinstance(aliases, dict):
        normalized = str(aliases.get(normalized, normalized))
    roles = [item for item in registry["roles"] if isinstance(item, dict)]  # type: ignore[index]
    matches = [str(item["id"]) for item in roles if normalized == item["id"] or normalized in item.get("aliases", [])]
    if len(matches) != 1:
        raise ValueError(f"FLOW_UNKNOWN_ROLE: {value}")
    return matches[0]


def select_references(
    root: Path,
    registry: dict[str, object],
    role: str,
    action: str,
    step: str,
    skill: str,
) -> JitReferenceSelection:
    """Select trusted flow references plus one owning-skill procedure."""
    skill_root = flow_skill_root(root)
    selectors = sorted((item for item in registry["selectors"] if isinstance(item, dict)), key=lambda item: (-int(item["priority"]), str(item["id"])))  # type: ignore[index]
    selected_specs: list[tuple[str, int, str]] = [(f"references/roles/{role}.md", 1200, "active role contract"), (step, 800, "current workflow step")]
    skipped: list[str] = []
    for selector in selectors:
        matches = (not selector["roles"] or role in selector["roles"]) and (not selector["actions"] or action in selector["actions"])
        if not matches:
            skipped.append(f"{selector['id']}:role/action mismatch")
            continue
        selected_specs.extend((str(path), int(selector["max_tokens"]), str(selector["reason"])) for path in selector["include"])
    selected: list[str] = []
    token_total = 0
    seen: set[str] = set()
    for relative, cap, reason in selected_specs:
        if relative in seen:
            continue
        seen.add(relative)
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError(f"FLOW_UNSAFE_SELECTOR: unsafe relative path {relative}")
        path = skill_root / relative
        resolved = path.resolve()
        try:
            resolved.relative_to(skill_root)
        except ValueError as exc:
            raise ValueError(f"FLOW_UNSAFE_SELECTOR: path escapes flow package: {relative}") from exc
        if path.is_symlink() or not resolved.is_file():
            raise ValueError(f"FLOW_UNSAFE_SELECTOR: selected reference is not a regular file: {relative}")
        tokens = (len(resolved.read_text(encoding="utf-8")) + 3) // 4
        if tokens > cap:
            raise ValueError(f"FLOW_SELECTOR_OVERSIZE: {relative} uses {tokens} tokens; cap is {cap}")
        token_total += tokens
        selected.append(f"{relative}:{hashlib.sha256(resolved.read_bytes()).hexdigest()}:{tokens}:{reason}")
    skill_steps = ai_sdlc_steps.select_steps(
        root,
        skill,
        Path(step).stem,
        role=role,
        action=action,
    )
    selected.extend(skill_steps.selected)
    skipped.extend(f"skill-step:{record}" for record in skill_steps.skipped)
    token_total += skill_steps.selected_tokens
    fingerprint = _digest(
        {
            "role": role,
            "action": action,
            "step": step,
            "skill": skill,
            "selected": selected,
            "skipped": skipped,
            "step_selection": skill_steps.selection_fingerprint,
        }
    )
    selected_step = skill_steps.selected[0].split(":", 1)[0]
    return JitReferenceSelection(
        selected=tuple(selected),
        skipped=tuple(skipped),
        fingerprint=fingerprint,
        selected_tokens=token_total,
        broad_tokens=broad_reference_tokens(root) + skill_steps.broad_tokens,
        skill_step_reference=selected_step,
        step_manifest_fingerprint=skill_steps.manifest_fingerprint,
    )


def broad_reference_tokens(root: Path) -> int:
    """Measure the legacy broad-load baseline across all flow references and steps."""
    skill_root = flow_skill_root(root)
    total = 0
    for folder in ("references", "steps"):
        for path in sorted((skill_root / folder).rglob("*")):
            if path.is_file() and not path.is_symlink() and path.suffix in {".md", ".json"}:
                total += (len(path.read_text(encoding="utf-8")) + 3) // 4
    return total


def build_independent_review_packet(*, requirements: str, tests: str, diff: str) -> dict[str, object]:
    return {"schema": "ai-sdlc-spec-first-review/v1", "phase": "independent_findings", "requirements": requirements, "tests": tests, "diff": diff, "excluded_until_findings": ("ai_rationale", "prior_verdict")}


def reveal_review_context(*, independent_findings: Iterable[str], ai_rationale: str, prior_verdict: str) -> dict[str, object]:
    findings = tuple(item.strip() for item in independent_findings if item.strip())
    if not findings:
        raise ValueError("FLOW_REVIEW_ORDER: record independent findings or an explicit no-findings result")
    return {"schema": "ai-sdlc-spec-first-review/v1", "phase": "comparison", "independent_findings": findings, "ai_rationale": ai_rationale, "prior_verdict": prior_verdict}


def build_card(
    *, root: Path, intent: str, feature: str, requested_rigor: str | None = None,
    policy_requires_full: bool = False, sources: tuple[str, ...] = (),
    project_context: str = "not-provided", economics: ContextEconomics | None = None,
    requested_role: str | None = None, requested_action: str | None = None,
    flow_config: dict[str, object] | None = None, registry_path: Path | None = None,
) -> DecisionCard:
    registry = load_registry(root, registry_path)
    config = _validated_flow_config(flow_config, registry=registry)
    configured_selectors = config.get("context_selectors", [])
    if configured_selectors:
        registry = dict(registry)
        registry["selectors"] = [*registry["selectors"], *configured_selectors]  # type: ignore[index]
    by_id, by_skill = _action_maps(registry)
    intent_class, workspace, stage, skill, intent_evidence = classify_intent(intent)
    action = by_id.get(requested_action or "") if requested_action else by_id.get(intent_class)
    blockers: list[str] = []
    if requested_action and action is None:
        blockers.append(f"FLOW_UNKNOWN_ACTION: {requested_action}")
    if action:
        intent_class = str(action["id"])
        workspace, stage, skill = str(action["workspace"]), str(action["stage"]), str(action["skill"])
        intent_evidence = (f"explicit action: {requested_action}",) if requested_action else intent_evidence
    menu_options = (
        tuple(sorted(by_id))
        if intent_class == "ambiguous" or str(config.get("menu_mode", "ambiguous")) == "always"
        else ()
    )
    existing = state_route(root, feature, workspace, skill) if workspace and skill else None
    route_evidence = list(intent_evidence)
    if existing:
        workspace, stage, skill, reason = existing
        route_evidence.append(reason)
    elif workspace == "implementation" and current_branch(root) in DEFAULT_BASE_BRANCHES:
        workspace, stage, skill = "implementation", "branching", "ai-sdlc-branching"
        route_evidence.append("shared base branch requires task branching before SDD writes")
    actual_action = by_skill.get(skill, action or {})
    action_id = str(actual_action.get("id", intent_class if intent_class != "ambiguous" else ""))
    action_code = str(actual_action.get("code", ""))
    active_role = str(actual_action.get("role", ""))
    requested_role_id = ""
    try:
        requested_role_id = _resolve_requested_role(requested_role, registry, config)
    except ValueError as exc:
        blockers.append(str(exc))
    handoff_reason = ""
    if requested_role_id and active_role and requested_role_id != active_role:
        handoff_reason = f"{requested_role_id} requested; {active_role} owns {action_id or skill}"
    roles = (active_role,) if active_role else ()
    role_evidence = (f"{active_role}: owns {action_id or stage}",) if active_role else ()
    rigor, rigor_reason, rigor_blockers = select_rigor(intent, requested=requested_rigor, policy_requires_full=policy_requires_full)
    blockers.extend(rigor_blockers)
    target, path_blockers = validate_workspace(root, feature, workspace) if workspace else (None, ())
    blockers.extend(path_blockers)
    installed, roots = discover_skills(root)
    if skill and skill not in installed:
        blockers.append(f"FLOW_MISSING_SKILL: {skill} is unavailable in " + (";".join(roots) or "all searched roots"))
    if intent_class == "ambiguous" and str(config.get("menu_mode", "ambiguous")) in {"ambiguous", "always"}:
        blockers.append("FLOW_AMBIGUOUS_INTENT: select one action from menu_options")
    step = str(actual_action.get("step", "steps/clarify.md" if menu_options else ""))
    selected: tuple[str, ...] = ()
    skipped: tuple[str, ...] = ()
    selector_fingerprint = _digest({})
    selected_tokens = 0
    broad_tokens = broad_reference_tokens(root)
    skill_step_reference = ""
    step_manifest_fingerprint = _digest({})
    if active_role and step:
        try:
            jit = select_references(
                root,
                registry,
                active_role,
                action_id,
                step,
                skill,
            )
            selected = jit.selected
            skipped = jit.skipped
            selector_fingerprint = jit.fingerprint
            selected_tokens = jit.selected_tokens
            broad_tokens = jit.broad_tokens
            skill_step_reference = jit.skill_step_reference
            step_manifest_fingerprint = jit.step_manifest_fingerprint
        except ValueError as exc:
            blockers.append(str(exc))
    context = economics or choose_context(
        raw_tokens=max(broad_tokens, selected_tokens),
        packed_tokens=selected_tokens,
        reread_tokens=0,
        critical_total=len(selected),
        critical_retained=len(selected),
    )
    config_fingerprint = _digest(config)
    planned = () if blockers or target is None else (target.relative_to(root.resolve()).as_posix(),)
    semantic = {
        "schema": SCHEMA, "repo_id": root.resolve().as_posix(), "intent": " ".join(intent.split()),
        "intent_class": intent_class, "feature": feature, "workspace": workspace, "stage": stage,
        "skill": skill, "rigor": rigor, "active_role": active_role, "requested_role": requested_role_id,
        "handoff": handoff_reason, "action_id": action_id, "action_code": action_code,
        "menu_options": menu_options, "step": step, "selected": selected, "skipped": skipped,
        "selector_fingerprint": selector_fingerprint, "config_fingerprint": config_fingerprint,
        "skill_step_reference": skill_step_reference,
        "step_manifest_fingerprint": step_manifest_fingerprint,
        "context_economics": asdict(context), "sources": sources, "project_context": project_context,
        "blockers": tuple(blockers), "planned_writes": planned,
    }
    fingerprint = _digest(semantic)
    return DecisionCard(
        schema=SCHEMA,
        mode="explore",
        repo_id=root.resolve().as_posix(),
        intent=" ".join(intent.split()),
        intent_class=intent_class,
        intent_confidence=0.0 if intent_class == "ambiguous" else 1.0,
        intent_reason="; ".join(route_evidence),
        feature=feature,
        workspace=workspace,
        stage=stage,
        skill=skill,
        rigor=rigor,
        rigor_reason=rigor_reason,
        roles=roles,
        role_evidence=role_evidence,
        project_context=project_context,
        sources=sources,
        context_economics=context,
        blockers=tuple(blockers),
        planned_writes=planned,
        next_checkpoint=(
            "Apply this fingerprint"
            if not blockers
            else "Resolve blockers and Explore again"
        ),
        fingerprint=fingerprint,
        requested_role=requested_role_id,
        active_role=active_role,
        role_handoff_reason=handoff_reason,
        action_id=action_id,
        action_code=action_code,
        menu_options=menu_options,
        current_step=Path(step).stem if step else "",
        step_reference=step,
        selected_references=selected,
        skipped_references=skipped,
        selector_fingerprint=selector_fingerprint,
        config_fingerprint=config_fingerprint,
        skill_step_reference=skill_step_reference,
        step_manifest_fingerprint=step_manifest_fingerprint,
    )


def semantic_dict(card: DecisionCard) -> dict[str, object]:
    return asdict(card)


def render_markdown(card: DecisionCard) -> str:
    e = card.context_economics
    lines = [
        "# AI SDLC Explore", "", f"- Contract: `{card.schema}`",
        f"- Intent: `{card.intent_class}` (confidence {card.intent_confidence:.2f}) — {card.intent_reason}",
        f"- Requested/active role: `{card.requested_role or 'auto'}` / `{card.active_role or 'unselected'}`",
        f"- Handoff: {card.role_handoff_reason or 'none'}",
        f"- Action: `{card.action_id or 'unselected'}` (`{card.action_code or '-'}`) → `{card.skill or 'unselected'}`",
        f"- Menu: {', '.join(card.menu_options) if card.menu_options else 'none'}",
        f"- Current step: `{card.current_step or 'unselected'}` — `{card.step_reference or '-'}`",
        f"- Owning-skill step: `{card.skill_step_reference or '-'}`",
        f"- Selected references: {', '.join(card.selected_references) if card.selected_references else 'none'}",
        f"- Skipped references: {', '.join(card.skipped_references) if card.skipped_references else 'none'}",
        f"- Feature/workspace: `{card.feature}` / `{card.workspace or 'unselected'}`",
        f"- Stage/rigor: `{card.stage or 'unselected'}` / `{card.rigor}`",
        f"- Context: `{e.selected_strategy}`; net={e.net_tokens}, savings={e.savings_percent}%, recall={e.recall_percent}%",
        f"- Selector/manifest/config fingerprints: `{card.selector_fingerprint}` / `{card.step_manifest_fingerprint}` / `{card.config_fingerprint}`",
        f"- Evidence hashes: {', '.join(card.sources) if card.sources else 'none'}",
        f"- Planned writes: {', '.join(card.planned_writes) if card.planned_writes else 'none'}",
        f"- Blockers: {'; '.join(card.blockers) if card.blockers else 'none'}",
        f"- Next checkpoint: {card.next_checkpoint}", f"- Fingerprint: `{card.fingerprint}`", "",
    ]
    return "\n".join(lines)


def render_toon(card: DecisionCard) -> str:
    value = semantic_dict(card)
    lines = [f"{key}: {_canonical(item) if isinstance(item, (dict, list, tuple)) else item}" for key, item in value.items()]
    return "\n".join(lines) + "\n"
