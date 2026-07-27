#!/usr/bin/env python3
"""Portable OKF v0.2 rendering, indexing, validation, and migration.

The module deliberately uses only the Python standard library.  AI SDLC
artifact metadata remains a producer extension; OKF fields are the portable
knowledge contract shared by feature, change, and runtime bundles.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from ai_sdlc_safe_io import atomic_write_text


OKF_VERSION = "0.2"
DEFAULT_GENERATED_BY = "process:ai-sdlc"
RESERVED_MARKDOWN = frozenset({"index.md", "log.md"})
OKF_STATUS = frozenset({"draft", "stable", "deprecated"})
GENERATED_ACTOR = re.compile(
    r"^(?:human|process):[A-Za-z0-9][A-Za-z0-9._-]*$|^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._+-]*$"
)


@dataclass(frozen=True)
class ConceptProfile:
    """Stable portable identity for one generated Markdown concept."""

    key: str
    type: str
    title: str
    description: str
    tags: tuple[str, ...]


def _profile(
    key: str,
    concept_type: str,
    title: str,
    description: str,
    *tags: str,
) -> ConceptProfile:
    return ConceptProfile(key, concept_type, title, description, ("ai-sdlc", *tags))


_PROFILES: tuple[ConceptProfile, ...] = (
    _profile("discovery.md", "ai-sdlc.discovery", "Working Backwards Discovery", "Customer problem, audience, value, scope, and discovery evidence.", "discovery"),
    _profile("prfaq.md", "ai-sdlc.prfaq", "PRFAQ Package", "Working-backwards press release, FAQ, and business requirements.", "discovery", "requirements"),
    _profile("delivery-gap-review.md", "ai-sdlc.delivery-gap-review", "Delivery Package Gap Review", "Delivery gaps, contradictions, blockers, and readiness findings.", "review"),
    _profile("requirements-readiness.md", "ai-sdlc.requirements-readiness", "Requirements Readiness Review", "Requirements quality assessment and readiness verdict.", "review", "requirements"),
    _profile("goal-capability-map.md", "ai-sdlc.goal-capability-map", "Goal, Capability, and Epic Map", "Business goals mapped to roles, capabilities, and outcome-oriented epics.", "planning"),
    _profile("backlog-gap-review.md", "ai-sdlc.backlog-gap-review", "Backlog Requirements Gap Review", "Planning gaps and backlog-blocking ambiguity.", "review", "backlog"),
    _profile("backlog.md", "ai-sdlc.backlog", "Delivery Backlog", "Epics, stories, acceptance summaries, dependencies, and delivery tasks.", "planning", "backlog"),
    _profile("user-stories.md", "ai-sdlc.user-stories", "User Story Decomposition", "User stories, acceptance criteria, scenarios, priority, and value.", "planning", "requirements"),
    _profile("release-slicing.md", "ai-sdlc.release-slicing", "Release Slicing and Readiness", "MVP and release slices, sequencing, and backlog readiness.", "planning", "release"),
    _profile("business-context.md", "ai-sdlc.business-context", "Business Context", "Actors, workflows, rules, exceptions, and acceptance context.", "analysis", "requirements"),
    _profile("delivery-spec.md", "ai-sdlc.delivery-spec", "Delivery Specification", "Structured implementation and cross-functional delivery contract.", "requirements", "delivery"),
    _profile("qa-gap-review.md", "ai-sdlc.qa-gap-review", "QA Requirements Gap Review", "Testability gaps, missing rules, and QA blockers.", "review", "qa"),
    _profile("qa-strategy.md", "ai-sdlc.qa-strategy", "QA Scope and Strategy", "Risk-based QA scope, layers, data, environments, and suite intent.", "qa", "testing"),
    _profile("test-suite.md", "ai-sdlc.test-suite", "Test Suite", "Executable smoke, regression, and acceptance suite definitions.", "qa", "testing"),
    _profile("qa-readiness.md", "ai-sdlc.qa-readiness", "QA Traceability and Readiness", "Requirements-to-test traceability and execution readiness.", "qa", "review"),
    _profile("delivery-handoff-review.md", "ai-sdlc.delivery-handoff-review", "Delivery Handoff Review", "Strict delivery readiness and ownership handoff review.", "review", "delivery"),
    _profile("requirements.md", "ai-sdlc.requirements", "Requirements", "Implementation requirements, constraints, and acceptance criteria.", "sdd", "requirements"),
    _profile("design.md", "ai-sdlc.design", "Design", "Technical design, interfaces, architecture, and migration decisions.", "sdd", "design"),
    _profile("plan.md", "ai-sdlc.implementation-plan", "Implementation Plan", "Ordered implementation and validation plan.", "sdd", "planning"),
    _profile("tasks.md", "ai-sdlc.tasks", "Implementation Tasks", "Traceable implementation task breakdown and status.", "sdd", "tasks"),
    _profile("test-cases.md", "ai-sdlc.test-cases", "Test Cases", "Test scenarios, expected outcomes, and coverage mapping.", "qa", "testing"),
    _profile("qa.md", "ai-sdlc.qa-plan", "QA Plan", "Acceptance, regression, risk, and manual validation plan.", "qa", "testing"),
    _profile("decision-log.md", "ai-sdlc.decision-log", "Decision Log", "Auditable decisions, evidence, alternatives, and traceability.", "decision"),
    _profile("branch-plan.md", "ai-sdlc.branch-plan", "Branch Plan", "Branch alignment, delivery boundary, and handoff plan.", "git", "planning"),
    _profile("validation.md", "ai-sdlc.validation-report", "Validation Report", "Deterministic validation commands, results, and residual risk.", "validation"),
    _profile("code-review.md", "ai-sdlc.code-review", "Code Review", "Review findings, requirement alignment, and residual risk.", "review", "code"),
    _profile("security-review.md", "ai-sdlc.security-review", "Security Review", "Security threats, controls, findings, and validation evidence.", "security", "review"),
    _profile("commit-readiness.md", "ai-sdlc.commit-readiness", "Commit Readiness", "Commit scope, validation, traceability, and readiness evidence.", "git", "review"),
    _profile("commit-message.md", "ai-sdlc.commit-message", "Commit Message", "Conventional commit message and change traceability.", "git"),
    _profile("approval-plan.md", "ai-sdlc.approval-plan", "Approval and Sandbox Plan", "Approval boundaries, sandbox decisions, and safe command rules.", "safety", "planning"),
    _profile("architecture.md", "ai-sdlc.architecture", "Architecture", "Architecture constraints, decisions, and component relationships.", "architecture"),
    _profile("research.md", "ai-sdlc.research", "Research", "Evidence-backed technical or product research.", "research"),
    _profile("ux.md", "ai-sdlc.ux", "UX Specification", "User experience flows, states, and interaction requirements.", "ux"),
    _profile("ux-spec.md", "ai-sdlc.ux", "UX Specification", "User experience flows, states, and interaction requirements.", "ux"),
    _profile("change-impact.md", "ai-sdlc.change-impact", "Change Impact", "Change scope, dependencies, affected surfaces, and risks.", "analysis", "change"),
    _profile("evidence-council.md", "ai-sdlc.evidence-council", "Evidence Council", "Multi-source evidence assessment and decision support.", "evidence", "review"),
    _profile("quality-lens-report.md", "ai-sdlc.quality-lens-report", "Quality Lens Report", "Cross-functional quality findings and recommendations.", "quality", "review"),
    _profile("retrospective.md", "ai-sdlc.retrospective", "Retrospective", "Delivery outcomes, lessons, and improvement actions.", "retrospective"),
    _profile("project-context.md", "ai-sdlc.project-context", "Project Context", "Repository purpose, architecture, commands, conventions, and constraints.", "context"),
    _profile("topology.md", "ai-sdlc.context-topology", "Context Topology", "Progressive context sources, relationships, and retrieval routes.", "context"),
    _profile("task-pack.md", "ai-sdlc.context-task-pack", "Task Context Pack", "Bounded task-specific context and source evidence.", "context"),
    _profile("delivery-graph.md", "ai-sdlc.delivery-graph", "Delivery Graph", "Artifact dependencies, lifecycle state, and delivery routes.", "delivery", "graph"),
    _profile("evidence-ledger.md", "ai-sdlc.evidence-ledger", "Evidence Ledger", "Validation and review evidence with source traceability.", "evidence"),
    _profile("workflow-plan.md", "ai-sdlc.workflow-plan", "Workflow Plan", "Durable workflow steps, state, and execution guidance.", "workflow", "planning"),
    _profile("doctor-report.md", "ai-sdlc.doctor-report", "AI SDLC Doctor Report", "Installation and repository health findings.", "diagnostics"),
    _profile("upgrade-plan.md", "ai-sdlc.upgrade-plan", "AI SDLC Upgrade Plan", "Version migration actions, risks, and validation.", "migration"),
    _profile("negotiation.md", "ai-sdlc.host-negotiation", "Host Adapter Negotiation", "Host capability negotiation and adapter decisions.", "host", "integration"),
    _profile("package-trust-decision.md", "ai-sdlc.package-trust-decision", "Package Trust Decision", "Package provenance, integrity, policy, and trust decision.", "trust", "security"),
    _profile("trust-metrics.md", "ai-sdlc.trust-metrics", "Package Trust Metrics", "Local package trust observations and metrics.", "trust", "metrics"),
    _profile("proposal.md", "ai-sdlc.change-proposal", "Change Proposal", "Proposed change outcome, scope, and rationale.", "change"),
    _profile("apply-preview.md", "ai-sdlc.change-apply-preview", "Change Apply Preview", "Preview of planned change-set mutations and conflicts.", "change", "preview"),
    _profile("modules.md", "ai-sdlc.module-catalog", "Module Catalog", "Project modules, responsibilities, and relationships.", "context", "architecture"),
    _profile("external-spec-snapshot.md", "ai-sdlc.external-spec-snapshot", "External Specification Snapshot", "Traceable snapshot of an external specification source.", "external", "requirements"),
)

PROFILE_BY_KEY = {profile.key: profile for profile in _PROFILES}


def concept_profile(key_or_path: str | Path) -> ConceptProfile:
    """Return an explicit concept profile or fail closed."""
    key = Path(key_or_path).name
    profile = PROFILE_BY_KEY.get(str(key_or_path)) or PROFILE_BY_KEY.get(key)
    if profile is None and key.startswith("external-") and key.endswith(".md"):
        profile = PROFILE_BY_KEY["external-spec-snapshot.md"]
    if profile is None:
        raise ValueError(f"no OKF concept profile for {key_or_path!s}")
    return profile


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp suitable for generated.at."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def yaml_quote(value: object) -> str:
    text = str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """Split Markdown into frontmatter lines and visible body."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")
    body_start = end + len("\n---")
    while body_start < len(text) and text[body_start] in "\r\n":
        body_start += 1
    return text[4:end].splitlines(), text[body_start:]


def _top_level_blocks(lines: Sequence[str]) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {}
    active: str | None = None
    for line in lines:
        if line and not line[0].isspace() and ":" in line:
            active = line.split(":", 1)[0].strip()
            blocks[active] = [line]
        elif active is not None:
            blocks[active].append(line)
    return blocks


def _scalar(blocks: dict[str, list[str]], key: str) -> str:
    lines = blocks.get(key, ())
    if not lines:
        return ""
    value = lines[0].split(":", 1)[1].strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def _nested_scalar(blocks: dict[str, list[str]], parent: str, key: str) -> str:
    for line in blocks.get(parent, ())[1:]:
        if line.startswith("  " + key + ":"):
            value = line.split(":", 1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            return value
    return ""


def _nested_list(
    blocks: dict[str, list[str]], parent: str, key: str
) -> tuple[str, ...]:
    values: list[str] = []
    active = False
    for line in blocks.get(parent, ())[1:]:
        if line.startswith("  ") and not line.startswith("    "):
            active = line.startswith("  " + key + ":")
            continue
        if active and line.startswith("    - "):
            value = line[6:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            values.append(value)
    return tuple(values)


def okf_status(lifecycle_status: str | None) -> str:
    """Map internal lifecycle states without implying verification."""
    normalized = (lifecycle_status or "draft").strip().lower()
    if normalized in {"approved", "validated", "done", "complete", "completed", "stable"}:
        return "stable"
    if normalized in {"superseded", "deprecated"}:
        return "deprecated"
    return "draft"


def generated_actor(existing_text: str, override: str | None = None) -> str:
    """Resolve generated.by from override, preserved metadata, or safe default."""
    existing_lines, _ = split_frontmatter(existing_text) if existing_text else ([], "")
    existing = _nested_scalar(_top_level_blocks(existing_lines), "generated", "by")
    actor = override or existing or DEFAULT_GENERATED_BY
    if not GENERATED_ACTOR.fullmatch(actor):
        raise ValueError(
            "generated.by must be human:<id>, process:<id>, or <producer>/<version>"
        )
    return actor


def render_frontmatter(
    *,
    profile: ConceptProfile,
    status: str,
    generated_by: str,
    generated_at: str,
    sources: Sequence[str] = (),
    verified_by: str | None = None,
    verified_at: str | None = None,
    verification_evidence: Sequence[str] = (),
    extension_lines: Sequence[str] = (),
) -> list[str]:
    """Render portable OKF fields followed by producer extension blocks."""
    if status not in OKF_STATUS:
        raise ValueError(f"unsupported OKF status: {status}")
    if not GENERATED_ACTOR.fullmatch(generated_by):
        raise ValueError(f"invalid generated.by actor: {generated_by}")
    if verified_by or verified_at or verification_evidence:
        if not (verified_by and verified_at and verification_evidence):
            raise ValueError("verified requires by, at, and non-empty evidence")
        if not GENERATED_ACTOR.fullmatch(verified_by):
            raise ValueError(f"invalid verified.by actor: {verified_by}")
    lines = [
        "---",
        f"type: {yaml_quote(profile.type)}",
        f"title: {yaml_quote(profile.title)}",
        f"description: {yaml_quote(profile.description)}",
        "tags:",
        *(f"  - {yaml_quote(tag)}" for tag in profile.tags),
        f"status: {yaml_quote(status)}",
        "generated:",
        f"  by: {yaml_quote(generated_by)}",
        f"  at: {yaml_quote(generated_at)}",
    ]
    if sources:
        lines.append("  sources:")
        lines.extend(f"    - {yaml_quote(source)}" for source in sources)
    if verified_by:
        lines.extend(
            [
                "verified:",
                f"  by: {yaml_quote(verified_by)}",
                f"  at: {yaml_quote(verified_at)}",
                "  evidence:",
                *(f"    - {yaml_quote(item)}" for item in verification_evidence),
            ]
        )
    if extension_lines:
        lines.extend(extension_lines)
    lines.extend(["---", ""])
    return lines


def render_concept(
    body: str,
    *,
    profile_key: str | Path,
    lifecycle_status: str = "draft",
    generated_by_override: str | None = None,
    existing_text: str = "",
    sources: Sequence[str] = (),
    extension_lines: Sequence[str] = (),
    meaningful_change: bool = True,
) -> str:
    """Render one concept while preserving actor/time on metadata-only refresh."""
    profile = concept_profile(profile_key)
    actor = generated_actor(existing_text, generated_by_override)
    existing_lines, _ = split_frontmatter(existing_text) if existing_text else ([], "")
    blocks = _top_level_blocks(existing_lines)
    prior_at = _nested_scalar(blocks, "generated", "at")
    generated_at = utc_now() if meaningful_change or not prior_at else prior_at
    verified_by = None if meaningful_change else _nested_scalar(blocks, "verified", "by") or None
    verified_at = None if meaningful_change else _nested_scalar(blocks, "verified", "at") or None
    verification_evidence = (
        () if meaningful_change else _nested_list(blocks, "verified", "evidence")
    )
    known = {"type", "title", "description", "tags", "status", "generated", "verified"}
    explicit_extension_keys = {
        line.split(":", 1)[0]
        for line in extension_lines
        if line and not line[0].isspace() and ":" in line
    }
    preserved_extensions: list[str] = []
    for key, block in blocks.items():
        if key not in known and key not in explicit_extension_keys:
            preserved_extensions.extend(block)
    metadata = render_frontmatter(
        profile=profile,
        status=okf_status(lifecycle_status),
        generated_by=actor,
        generated_at=generated_at,
        sources=sources,
        verified_by=verified_by,
        verified_at=verified_at,
        verification_evidence=verification_evidence,
        extension_lines=(*preserved_extensions, *extension_lines),
    )
    return "\n".join(metadata).rstrip() + "\n\n" + body.lstrip()


def migrate_concept_text(
    text: str,
    *,
    profile_key: str | Path,
    generated_by_override: str | None = None,
) -> str:
    """Add or normalize OKF fields while preserving producer extensions/body."""
    profile = concept_profile(profile_key)
    frontmatter, body = split_frontmatter(text)
    blocks = _top_level_blocks(frontmatter)
    existing_type = _scalar(blocks, "type")
    if existing_type and existing_type != profile.type:
        raise ValueError(
            f"existing type {existing_type!r} conflicts with profile {profile.type!r}"
        )
    lifecycle_status = _nested_scalar(blocks, "artifact_metadata", "status") or _scalar(blocks, "status")
    actor = generated_actor(text, generated_by_override)
    generated_at = _nested_scalar(blocks, "generated", "at") or utc_now()
    verified_by = _nested_scalar(blocks, "verified", "by") or None
    verified_at = _nested_scalar(blocks, "verified", "at") or None
    verification_evidence = _nested_list(blocks, "verified", "evidence")
    known = {
        "type",
        "title",
        "description",
        "tags",
        "status",
        "generated",
        "verified",
    }
    extension_lines: list[str] = []
    for key, block in blocks.items():
        if key not in known:
            extension_lines.extend(block)
    metadata = render_frontmatter(
        profile=profile,
        status=okf_status(lifecycle_status),
        generated_by=actor,
        generated_at=generated_at,
        verified_by=verified_by,
        verified_at=verified_at,
        verification_evidence=verification_evidence,
        extension_lines=extension_lines,
    )
    return "\n".join(metadata).rstrip() + "\n\n" + body.lstrip()


def concept_metadata(text: str) -> dict[str, str]:
    """Read the bounded portable fields used by indexes and validators."""
    frontmatter, _ = split_frontmatter(text)
    blocks = _top_level_blocks(frontmatter)
    return {
        "type": _scalar(blocks, "type"),
        "title": _scalar(blocks, "title"),
        "description": _scalar(blocks, "description"),
        "status": _scalar(blocks, "status"),
        "generated_by": _nested_scalar(blocks, "generated", "by"),
        "generated_at": _nested_scalar(blocks, "generated", "at"),
    }


def _relative_link(path: Path, directory: Path) -> str:
    return path.relative_to(directory).as_posix()


def render_bundle_index(bundle_root: Path, directory: Path) -> str:
    """Render a reserved progressive index for one bundle directory."""
    is_root = directory.resolve() == bundle_root.resolve()
    title = bundle_root.name if is_root else directory.name
    lines: list[str] = []
    if is_root:
        lines.extend(["---", f"okf_version: {yaml_quote(OKF_VERSION)}", "---", ""])
    lines.extend([f"# {title}", "", "Progressive index for this OKF knowledge bundle.", ""])
    concepts = sorted(
        path
        for path in directory.glob("*.md")
        if path.name not in RESERVED_MARKDOWN
    )
    groups = sorted(
        child
        for child in directory.iterdir()
        if child.is_dir()
        and (
            any(path.name not in RESERVED_MARKDOWN for path in child.rglob("*.md"))
            or any(path.name == "index.md" for path in child.rglob("index.md"))
        )
    )
    if concepts:
        lines.extend(["## Concepts", ""])
        for path in concepts:
            metadata = concept_metadata(path.read_text(encoding="utf-8"))
            label = metadata["title"] or path.stem.replace("-", " ").title()
            detail = " · ".join(
                value for value in (metadata["type"], metadata["status"]) if value
            )
            suffix = f" — {detail}" if detail else ""
            lines.append(f"- [{label}]({_relative_link(path, directory)}){suffix}")
        lines.append("")
    if groups:
        lines.extend(["## Groups", ""])
        for group in groups:
            lines.append(f"- [{group.name}]({group.name}/index.md)")
        lines.append("")
    if not concepts and not groups:
        lines.extend(["## Contents", "", "- No Markdown concepts yet.", ""])
    return "\n".join(lines).rstrip() + "\n"


def bundle_index_outputs(bundle_root: Path) -> dict[Path, str]:
    """Return every root/nested index write without mutating the bundle."""
    directories = {bundle_root}
    for concept in bundle_root.rglob("*.md"):
        if concept.name not in RESERVED_MARKDOWN:
            directories.add(concept.parent)
            parent = concept.parent
            while parent != bundle_root and bundle_root in parent.parents:
                directories.add(parent)
                parent = parent.parent
    return {
        directory / "index.md": render_bundle_index(bundle_root, directory)
        for directory in sorted(directories, key=lambda path: path.as_posix())
    }


def write_bundle_indexes(bundle_root: Path) -> list[Path]:
    """Write deterministic progressive indexes for an OKF bundle."""
    outputs = bundle_index_outputs(bundle_root)
    for path, text in outputs.items():
        atomic_write_text(bundle_root, path, text)
    return sorted(outputs)


def validate_bundle(bundle_root: Path) -> list[str]:
    """Return OKF v0.2 conformance issues for one recursive bundle."""
    issues: list[str] = []
    root_index = bundle_root / "index.md"
    if not root_index.is_file():
        issues.append("missing root index.md")
    else:
        try:
            frontmatter, _ = split_frontmatter(root_index.read_text(encoding="utf-8"))
            blocks = _top_level_blocks(frontmatter)
            if set(blocks) != {"okf_version"} or _scalar(blocks, "okf_version") != OKF_VERSION:
                issues.append("root index.md frontmatter must contain only okf_version: \"0.2\"")
        except ValueError as exc:
            issues.append(f"index.md: {exc}")
    for path in sorted(bundle_root.rglob("*.md")):
        relative = path.relative_to(bundle_root).as_posix()
        if path.name == "index.md":
            if path != root_index:
                try:
                    frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"))
                    if frontmatter:
                        issues.append(f"{relative}: nested index.md must not have frontmatter")
                except ValueError as exc:
                    issues.append(f"{relative}: {exc}")
            continue
        if path.name == "log.md":
            continue
        try:
            metadata = concept_metadata(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            issues.append(f"{relative}: {exc}")
            continue
        if not metadata["type"]:
            issues.append(f"{relative}: missing non-empty top-level type")
        if metadata["status"] not in OKF_STATUS:
            issues.append(f"{relative}: invalid status {metadata['status']!r}")
        actor = metadata["generated_by"]
        if not actor or not GENERATED_ACTOR.fullmatch(actor):
            issues.append(f"{relative}: invalid or missing generated.by")
        if not metadata["generated_at"]:
            issues.append(f"{relative}: missing generated.at")
    return issues


def migrate_bundle(
    bundle_root: Path,
    *,
    generated_by_override: str | None = None,
    apply: bool = False,
) -> list[Path]:
    """Preflight a complete bundle, then optionally write all concepts/indexes."""
    outputs: dict[Path, str] = {}
    for path in sorted(bundle_root.rglob("*.md")):
        if path.name in RESERVED_MARKDOWN:
            continue
        outputs[path] = migrate_concept_text(
            path.read_text(encoding="utf-8"),
            profile_key=path.name,
            generated_by_override=generated_by_override,
        )
    # Render indexes against migrated concept metadata without partial writes.
    if apply:
        for path, text in outputs.items():
            atomic_write_text(bundle_root, path, text)
        write_bundle_indexes(bundle_root)
    return sorted(outputs)


def _selected_bundles(paths: Iterable[Path]) -> list[Path]:
    bundles = [path.resolve() for path in paths]
    if not bundles:
        raise ValueError("at least one bundle path is required")
    return bundles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundles", nargs="+", type=Path)
    parser.add_argument("--generated-by")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write-index", action="store_true")
    action.add_argument("--migrate", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Apply migration; default is preflight only")
    args = parser.parse_args()
    try:
        for bundle in _selected_bundles(args.bundles):
            if args.check:
                issues = validate_bundle(bundle)
                if issues:
                    for issue in issues:
                        print(f"ERROR: {bundle}: {issue}")
                    return 2
                print(f"OK: {bundle}")
            elif args.write_index:
                for path in write_bundle_indexes(bundle):
                    print(f"Wrote {path}")
            else:
                paths = migrate_bundle(
                    bundle,
                    generated_by_override=args.generated_by,
                    apply=args.apply,
                )
                verb = "Migrated" if args.apply else "Would migrate"
                print(f"{verb} {len(paths)} concepts in {bundle}")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
