#!/usr/bin/env python3
"""Pure contracts for the guided AI SDLC Explore -> Apply flow."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SCHEMA = "ai-sdlc-flow/v1"
REFINEMENT_ROOT = "specs-refiniment"
IMPLEMENTATION_ROOT = "specs"
PACK_SAVINGS_MINIMUM = 15.0


@dataclass(frozen=True)
class ContextEconomics:
    """Measured context choice, including targeted reread cost."""

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
    """Stable semantic route accepted by Apply."""

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


INTENT_RULES: tuple[tuple[str, tuple[str, ...], str, str, str], ...] = (
    (
        "new_refinement",
        ("feedback", "refinement", "new feature", "new request", "idea", "customer problem"),
        "refinement",
        "discovery",
        "ai-sdlc-working-backwards-discovery",
    ),
    (
        "review",
        ("code review", "review diff", "review pr", "spec-first review"),
        "implementation",
        "code_review",
        "ai-sdlc-code-review",
    ),
    (
        "validation",
        ("validate", "regression", "smoke test", "qa"),
        "implementation",
        "validation",
        "ai-sdlc-validation",
    ),
    (
        "implementation",
        ("implement", "fix", "bug", "refactor", "api", "architecture"),
        "implementation",
        "sdd",
        "ai-sdlc-sdd",
    ),
)


def classify_intent(intent: str) -> tuple[str, str, str, str, tuple[str, ...]]:
    """Classify intent before any feature state is considered."""
    normalized = " ".join(intent.lower().split())
    matches = [
        (name, workspace, stage, skill, keyword)
        for name, keywords, workspace, stage, skill in INTENT_RULES
        for keyword in keywords
        if keyword in normalized
    ]
    classes = {match[0] for match in matches}
    if len(classes) > 1:
        return (
            "ambiguous",
            "",
            "",
            "",
            ("FLOW_AMBIGUOUS_INTENT: request matches " + "/".join(sorted(classes)),),
        )
    if matches:
        name, workspace, stage, skill, keyword = matches[0]
        return name, workspace, stage, skill, (f"intent signal: {keyword}",)
    return (
        "ambiguous",
        "",
        "",
        "",
        ("FLOW_AMBIGUOUS_INTENT: provide refinement, implementation, review, or validation intent",),
    )


def select_roles(intent: str, *, stage: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Select the minimum roles and evidence-backed additions."""
    normalized = intent.lower()
    roles = ["Contributor", "Repository Maintainer"]
    evidence = [f"Contributor: request owner", f"Repository Maintainer: {stage or 'routing'} stage"]
    signals = (
        ("Security", ("authorization", "auth", "security", "secret", "owasp")),
        ("Data", ("migration", "schema", "database", "retention")),
        ("Operations", ("release", "rollout", "deploy", "support")),
        ("Product", ("pricing", "policy", "customer outcome", "market")),
    )
    for role, keywords in signals:
        keyword = next((item for item in keywords if item in normalized), None)
        if keyword:
            roles.append(role)
            evidence.append(f"{role}: intent signal `{keyword}`")
    if stage in {"code_review", "validation"}:
        roles.append("Reviewer and QA")
        evidence.append(f"Reviewer and QA: {stage} stage")
    return tuple(roles), tuple(evidence)


def select_rigor(
    intent: str,
    *,
    requested: str | None = None,
    policy_requires_full: bool = False,
) -> tuple[str, str, tuple[str, ...]]:
    """Select quick/full rigor and enforce the protected minimum."""
    normalized = intent.lower()
    high_risk = any(
        word in normalized
        for word in ("architecture", "migration", "security", "authorization", "cross-cutting", "ambiguous")
    )
    automatic = "full" if high_risk else "quick"
    blockers: list[str] = []
    effective = requested or automatic
    reason = f"automatic {automatic}: " + ("cross-cutting or risk signal" if high_risk else "bounded low-risk intent")
    if requested:
        reason += f"; explicit {requested} override"
    if policy_requires_full and effective == "quick":
        effective = "full"
        reason += "; upgraded because policy requires full"
    if effective not in {"quick", "full"}:
        blockers.append(f"FLOW_UNSAFE_RIGOR: unsupported rigor {effective}")
        effective = "full"
    return effective, reason, tuple(blockers)


def choose_context(
    *,
    raw_tokens: int,
    packed_tokens: int,
    reread_tokens: int,
    critical_total: int,
    critical_retained: int,
) -> ContextEconomics:
    """Choose packed context only when recall and net economics pass."""
    values = (raw_tokens, packed_tokens, reread_tokens, critical_total, critical_retained)
    if any(value < 0 for value in values):
        raise ValueError("FLOW_INVALID_CONTEXT: token and anchor counts must be non-negative")
    if critical_retained > critical_total:
        raise ValueError("FLOW_INVALID_CONTEXT: retained anchors cannot exceed total anchors")
    net = packed_tokens + reread_tokens
    savings = raw_tokens - net
    savings_percent = round((savings / raw_tokens * 100.0) if raw_tokens else 0.0, 2)
    recall = round((critical_retained / critical_total * 100.0) if critical_total else 100.0, 2)
    accepted = recall == 100.0 and savings_percent >= PACK_SAVINGS_MINIMUM
    if accepted:
        strategy = "packed"
        reason = "100% critical-anchor recall and net savings meet the 15% threshold"
    else:
        strategy = "direct"
        reasons = []
        if recall < 100.0:
            reasons.append("critical-anchor recall is below 100%")
        if savings_percent < PACK_SAVINGS_MINIMUM:
            reasons.append("net savings including rereads are below 15%")
        reason = "; ".join(reasons)
    return ContextEconomics(
        raw_tokens=raw_tokens,
        packed_tokens=packed_tokens,
        reread_tokens=reread_tokens,
        net_tokens=net,
        savings_tokens=savings,
        savings_percent=savings_percent,
        critical_total=critical_total,
        critical_retained=critical_retained,
        recall_percent=recall,
        selected_strategy=strategy,
        reason=reason,
    )


def validate_workspace(root: Path, feature: str, workspace: str) -> tuple[Path | None, tuple[str, ...]]:
    """Resolve one tool-owned feature root and reject unsafe topology."""
    if not re.fullmatch(r"\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", feature):
        return None, ("FLOW_UNSAFE_ROOT: feature must match NNN-kebab-case",)
    base_name = REFINEMENT_ROOT if workspace == "refinement" else IMPLEMENTATION_ROOT
    base_path = root / base_name
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
    other = root / (IMPLEMENTATION_ROOT if workspace == "refinement" else REFINEMENT_ROOT) / feature
    if candidate.exists() and other.exists() and (candidate.is_symlink() or other.is_symlink()):
        blockers.append("FLOW_UNSAFE_ROOT: linked or divergent workspace roots are unsupported")
    return (None, tuple(blockers)) if blockers else (candidate, ())


def source_hashes(root: Path, paths: Iterable[Path]) -> tuple[str, ...]:
    """Return sorted repository-relative SHA-256 evidence records."""
    records: list[str] = []
    root = root.resolve()
    for path in paths:
        resolved = path.resolve()
        resolved.relative_to(root)
        digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
        records.append(f"{resolved.relative_to(root).as_posix()}:{digest}")
    return tuple(sorted(records))


def discover_sources(root: Path, feature: str, explicit: Iterable[Path] = ()) -> tuple[str, ...]:
    """Hash mandatory repository controls plus caller-selected evidence."""
    root = root.resolve()
    mandatory = (
        root / "modules" / "core" / "module.json",
        root / "config" / "ai-sdlc.defaults.json",
        root / "config" / "ai-sdlc-managed-skills.txt",
        root / "project-context.md",
        root / REFINEMENT_ROOT / "_ai_sdlc" / "specs-index.toon",
        root / REFINEMENT_ROOT / feature / "_ai_sdlc" / "state.toon",
        root / IMPLEMENTATION_ROOT / "_ai_sdlc" / "specs-index.toon",
        root / IMPLEMENTATION_ROOT / feature / "_ai_sdlc" / "state.toon",
    )
    candidates = tuple(dict.fromkeys((*filter(Path.is_file, mandatory), *explicit)))
    return source_hashes(root, candidates)


def project_context_status(root: Path, requested: str) -> str:
    """Resolve the default project-context freshness label without mutation."""
    if requested != "auto":
        return requested
    path = root.resolve() / "project-context.md"
    if not path.is_file():
        return "not-found"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return f"present:sha256:{digest[:12]}"


def build_independent_review_packet(
    *,
    requirements: str,
    tests: str,
    diff: str,
) -> dict[str, object]:
    """Build phase-one review evidence without anchoring rationale or verdicts."""
    return {
        "schema": "ai-sdlc-spec-first-review/v1",
        "phase": "independent_findings",
        "requirements": requirements,
        "tests": tests,
        "diff": diff,
        "excluded_until_findings": ("ai_rationale", "prior_verdict"),
    }


def reveal_review_context(
    *,
    independent_findings: Iterable[str],
    ai_rationale: str,
    prior_verdict: str,
) -> dict[str, object]:
    """Open phase two only after at least one explicit independent review result."""
    findings = tuple(item.strip() for item in independent_findings if item.strip())
    if not findings:
        raise ValueError("FLOW_REVIEW_ORDER: record independent findings or an explicit no-findings result")
    return {
        "schema": "ai-sdlc-spec-first-review/v1",
        "phase": "comparison",
        "independent_findings": findings,
        "ai_rationale": ai_rationale,
        "prior_verdict": prior_verdict,
    }


def _fingerprint_payload(values: dict[str, object]) -> str:
    return json.dumps(values, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_card(
    *,
    root: Path,
    intent: str,
    feature: str,
    requested_rigor: str | None = None,
    policy_requires_full: bool = False,
    sources: tuple[str, ...] = (),
    project_context: str = "not-provided",
    economics: ContextEconomics | None = None,
) -> DecisionCard:
    """Build a read-only decision card from explicit evidence."""
    intent_class, workspace, stage, skill, intent_evidence = classify_intent(intent)
    roles, role_evidence = select_roles(intent, stage=stage)
    rigor, rigor_reason, rigor_blockers = select_rigor(
        intent, requested=requested_rigor, policy_requires_full=policy_requires_full
    )
    target, path_blockers = validate_workspace(root, feature, workspace) if workspace else (None, ())
    context = economics or choose_context(
        raw_tokens=0, packed_tokens=0, reread_tokens=0, critical_total=0, critical_retained=0
    )
    blockers = tuple(intent_evidence if intent_class == "ambiguous" else ()) + rigor_blockers + path_blockers
    planned_writes = () if blockers or target is None else (target.relative_to(root.resolve()).as_posix(),)
    semantic = {
        "schema": SCHEMA,
        "repo_id": root.resolve().as_posix(),
        "intent": " ".join(intent.split()),
        "intent_class": intent_class,
        "intent_confidence": 0.0 if intent_class == "ambiguous" else 1.0,
        "feature": feature,
        "workspace": workspace,
        "stage": stage,
        "skill": skill,
        "rigor": rigor,
        "roles": roles,
        "role_evidence": role_evidence,
        "project_context": project_context,
        "sources": sources,
        "context_economics": asdict(context),
        "blockers": blockers,
        "planned_writes": planned_writes,
    }
    fingerprint = hashlib.sha256(_fingerprint_payload(semantic).encode("utf-8")).hexdigest()
    return DecisionCard(
        schema=SCHEMA,
        mode="explore",
        repo_id=root.resolve().as_posix(),
        intent=" ".join(intent.split()),
        intent_class=intent_class,
        intent_confidence=0.0 if intent_class == "ambiguous" else 1.0,
        intent_reason="; ".join(intent_evidence),
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
        blockers=blockers,
        planned_writes=planned_writes,
        next_checkpoint="Apply this fingerprint" if not blockers else "Resolve blockers and Explore again",
        fingerprint=fingerprint,
    )


def semantic_dict(card: DecisionCard) -> dict[str, object]:
    """Return a JSON-safe card projection."""
    return asdict(card)


def render_markdown(card: DecisionCard) -> str:
    """Render a readable decision card."""
    e = card.context_economics
    lines = [
        "# AI SDLC Explore",
        "",
        f"- Intent: `{card.intent_class}` (confidence {card.intent_confidence:.2f}) — {card.intent_reason}",
        f"- Feature/workspace: `{card.feature}` / `{card.workspace or 'unselected'}`",
        f"- Stage/skill: `{card.stage or 'unselected'}` / `{card.skill or 'unselected'}`",
        f"- Rigor: `{card.rigor}` — {card.rigor_reason}",
        f"- Roles: {', '.join(card.roles)}",
        f"- Project context: {card.project_context}",
        f"- Evidence hashes: {', '.join(card.sources) if card.sources else 'none'}",
        f"- Context: `{e.selected_strategy}`; raw={e.raw_tokens}, packed={e.packed_tokens}, "
        f"reread={e.reread_tokens}, net={e.net_tokens}, savings={e.savings_percent}%, "
        f"critical recall={e.recall_percent}%",
        f"- Planned writes: {', '.join(card.planned_writes) if card.planned_writes else 'none'}",
        f"- Blockers: {'; '.join(card.blockers) if card.blockers else 'none'}",
        f"- Next checkpoint: {card.next_checkpoint}",
        f"- Route fingerprint: `{card.fingerprint}`",
    ]
    return "\n".join(lines) + "\n"


def render_toon(card: DecisionCard) -> str:
    """Render a compact, deterministic TOON-compatible projection."""
    e = card.context_economics
    lines = [
        f"schema: {card.schema}",
        f"mode: {card.mode}",
        f"repo_id: {card.repo_id}",
        f"intent: {card.intent.replace(',', ';')}",
        f"intent_class: {card.intent_class}",
        f"intent_confidence: {card.intent_confidence}",
        f"intent_reason: {card.intent_reason.replace(',', ';')}",
        f"feature: {card.feature}",
        f"workspace: {card.workspace}",
        f"stage: {card.stage}",
        f"skill: {card.skill}",
        f"rigor: {card.rigor}",
        f"rigor_reason: {card.rigor_reason.replace(',', ';')}",
        f"project_context: {card.project_context.replace(',', ';')}",
        f"fingerprint: {card.fingerprint}",
        "",
        f"sources[{len(card.sources)}]{{evidence}}:",
    ]
    lines.extend(f"  {value.replace(',', ';')}" for value in card.sources)
    lines.extend([
        "",
        f"roles[{len(card.roles)}]{{role,evidence}}:",
    ])
    lines.extend(f"  {role},{evidence.replace(',', ';')}" for role, evidence in zip(card.roles, card.role_evidence))
    lines.extend(
        [
            "",
            "context_economics{raw_tokens,packed_tokens,reread_tokens,net_tokens,savings_percent,critical_total,critical_retained,recall_percent,selected_strategy}:",
            f"  {e.raw_tokens},{e.packed_tokens},{e.reread_tokens},{e.net_tokens},{e.savings_percent},{e.critical_total},{e.critical_retained},{e.recall_percent},{e.selected_strategy}",
            "",
            f"blockers[{len(card.blockers)}]{{message}}:",
        ]
    )
    lines.extend(f"  {value.replace(',', ';')}" for value in card.blockers)
    lines.extend(["", f"planned_writes[{len(card.planned_writes)}]{{path}}:"])
    lines.extend(f"  {value}" for value in card.planned_writes)
    return "\n".join(lines).rstrip() + "\n"
