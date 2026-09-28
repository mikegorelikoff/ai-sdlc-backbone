#!/usr/bin/env python3
"""Rotation engine, freshness evaluation, repository indexing, and retention for ai-sdlc-spec-state."""

from __future__ import annotations

import datetime
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Optional

from spec_state_config import SpecStateConfig
from spec_state_storage import GitStorage, SpecHierarchy, resolve_spec_hierarchy, BASELINE_PATTERN, DECISION_ARCHIVE_PATTERN, INDEX_PATTERN


class ImpactScorer:
    """Calculates repository change impact to trigger proactive index refresh."""

    CRITICAL_PATTERNS = [
        re.compile(r".*\.(?:schema|toon|proto|graphql)$"),
        re.compile(r".*(?:architecture|infrastructure|gateway|models?|contracts?)/.*"),
        re.compile(r".*(?:pyproject\.toml|package\.json|go\.mod|Cargo\.toml)$"),
    ]

    CODE_PATTERNS = [
        re.compile(r".*\.(?:py|ts|tsx|js|jsx|go|rs|java|kt|cpp|c|h)$"),
    ]

    @classmethod
    def calculate_impact(cls, changed_files: list[str]) -> int:
        """Score impact points based on file type and structural significance."""
        score = 0
        for f in changed_files:
            f_norm = f.strip().replace("\\", "/")
            if "/test" in f_norm or f_norm.startswith("test") or "/docs/" in f_norm or f_norm.startswith("docs/"):
                continue
            if any(p.match(f_norm) for p in cls.CRITICAL_PATTERNS):
                score += 3
            elif any(p.match(f_norm) for p in cls.CODE_PATTERNS):
                score += 1
        return score

    @classmethod
    def should_refresh_index(cls, cumulative_impact: int, threshold: int = 10) -> bool:
        """Determine if cumulative impact meets or exceeds threshold."""
        return cumulative_impact >= threshold


def check_index_freshness(index_path: Optional[Path], threshold_days: int = 14) -> dict[str, Any]:
    """Evaluate repository index freshness against configured threshold."""
    if not index_path or not index_path.is_file():
        return {
            "status": "missing",
            "age_days": None,
            "last_updated": None,
            "threshold_days": threshold_days,
            "needs_refresh": True,
            "message": "Repository structural index is missing. Index generation is required before starting feature work.",
            "path": None,
        }

    # Extract date from filename (YYYYMMDD-*)
    m = re.match(r"^(\d{8})-", index_path.name)
    if m:
        date_str = m.group(1)
        try:
            index_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
        except ValueError:
            index_date = datetime.date.fromtimestamp(index_path.stat().st_mtime)
    else:
        index_date = datetime.date.fromtimestamp(index_path.stat().st_mtime)

    today = datetime.date.today()
    age_days = (today - index_date).days
    if age_days < 0:
        age_days = 0

    needs_refresh = age_days > threshold_days
    status = "needs-refresh" if needs_refresh else "fresh"
    msg = (
        f"Repository index is {age_days} days old (threshold: {threshold_days} days). Refresh recommended."
        if needs_refresh
        else f"Repository index is fresh ({age_days} days old, threshold: {threshold_days} days)."
    )

    return {
        "status": status,
        "age_days": age_days,
        "last_updated": index_date.strftime("%Y-%m-%d"),
        "threshold_days": threshold_days,
        "needs_refresh": needs_refresh,
        "message": msg,
        "path": str(index_path),
    }


def check_rotation_triggers(config: SpecStateConfig, hierarchy: SpecHierarchy) -> dict[str, Any]:
    """Check whether baseline rotation or decision archive compaction should be triggered."""
    specs_count = len(hierarchy.feature_specs_since_baseline)
    spec_threshold = config.lifecycle.rotation_spec_threshold
    threshold_exceeded = specs_count >= spec_threshold

    version_changed = False
    current_version = config.repository.version
    baseline_version = hierarchy.latest_baseline_version

    if baseline_version and baseline_version != current_version:
        version_changed = True

    baseline_rotation_recommended = threshold_exceeded or version_changed

    reasons: list[str] = []
    if threshold_exceeded:
        reasons.append(f"Feature spec count ({specs_count}) reached threshold ({spec_threshold})")
    if version_changed:
        reasons.append(f"Repository version bumped from {baseline_version} to {current_version}")

    decisions_count = len(hierarchy.decision_logs_since_archive)
    dec_threshold = config.lifecycle.decision_archive_after_specs
    decision_archive_recommended = decisions_count >= dec_threshold
    if decision_archive_recommended:
        reasons.append(f"Decision logs count ({decisions_count}) reached archive threshold ({dec_threshold})")

    return {
        "baseline_rotation_recommended": baseline_rotation_recommended,
        "decision_archive_recommended": decision_archive_recommended,
        "reason": "; ".join(reasons) if reasons else "No rotation required.",
        "specs_since_baseline": specs_count,
        "spec_threshold": spec_threshold,
        "version_changed": version_changed,
        "current_version": current_version,
        "baseline_version": baseline_version,
        "decisions_since_archive": decisions_count,
        "decision_threshold": dec_threshold,
    }


def generate_repository_index(project_root: Path, repo_id: str, version: str) -> str:
    """Generate a compact structural model of the repository for AI-assisted development."""
    date_str = datetime.date.today().strftime("%Y%m%d")

    # Discover top-level dirs
    top_dirs: list[str] = []
    manifests: list[str] = []
    for item in sorted(project_root.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            top_dirs.append(item.name)
        elif item.is_file():
            if item.name in ("pyproject.toml", "package.json", "setup.py", "Cargo.toml", "go.mod", "Makefile", "mkdocs.yml"):
                manifests.append(item.name)

    # Detect high-level architecture
    arch_type = "Modular Python / Multi-package workspace"
    if "skills" in top_dirs and "docs" in top_dirs:
        arch_type = "Agentic Skill Architecture & Control Plane"
    elif "src" in top_dirs or "lib" in top_dirs:
        arch_type = "Standard Layered Application"

    modules_desc: list[str] = []
    for d in top_dirs:
        sub_count = len(list((project_root / d).glob("*")))
        modules_desc.append(f"- **`{d}/`**: primary functional subsystem (~{sub_count} root entries)")

    manifests_desc = ", ".join(f"`{m}`" for m in manifests) if manifests else "standard project structure"

    return f"""# Repository Index: {repo_id}

- **Repository ID:** `{repo_id}`
- **Version:** `{version}`
- **Index Date:** `{date_str}`
- **Architecture Model:** {arch_type}

## 1. System Architecture & Boundaries

The `{repo_id}` system provides structured services and components adhering to deterministic specification and contracts.
Primary manifests and package anchors: {manifests_desc}.

## 2. Core Modules & Subsystems

{chr(10).join(modules_desc)}

## 3. Integration Boundaries & Dependencies

- Inter-module communication is decoupled via contract schemas, immutable data models, and deterministic APIs.
- Downstream tooling depends on stable manifest definitions and verified schemas.
- External systems connect via explicit adapters with validation boundaries.

## 4. High-Risk Areas & Constraints

- **Deterministic Contracts:** Schema definitions must remain backwards-compatible.
- **Fail-Open Resilience:** Subsystem failures must report structured error states rather than crashing downstream callers.
- **State Integrity:** Persistent specification artifacts are immutable once published; rotation compacts history deterministically.
"""


def rotate_baseline_and_decisions(
    config: SpecStateConfig,
    storage: GitStorage,
    hierarchy: SpecHierarchy,
    force: bool = False,
) -> dict[str, Any]:
    """Execute atomic baseline and decision knowledgebase rotation."""
    triggers = check_rotation_triggers(config, hierarchy)
    if not triggers["baseline_rotation_recommended"] and not force:
        return {
            "status": "skipped",
            "message": "Rotation triggers not met. Use force=True to force rotation.",
            "triggers": triggers,
        }

    specs_dir = storage.get_repo_specs_dir()
    repo_id = config.repository.id
    version = config.repository.version
    date_str = datetime.date.today().strftime("%Y%m%d")

    # 1. Synthesize New Baseline Specification
    baseline_filename = f"baselinespec-{repo_id}-{version}-{date_str}.md"
    baseline_path = specs_dir / baseline_filename

    feature_specs_content: list[str] = []
    for spec_file in hierarchy.feature_specs_since_baseline:
        text = spec_file.read_text(encoding="utf-8")
        clean_text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
        feature_specs_content.append(f"### Feature: {spec_file.stem}\n\n{clean_text.strip()}\n")

    prior_baseline_note = ""
    if hierarchy.latest_baseline:
        prior_baseline_note = f"\n*Supersedes baseline: `{hierarchy.latest_baseline.name}` ({hierarchy.latest_baseline_version})*\n"

    baseline_doc = f"""# Baseline Specification: {repo_id}

- **Repository:** `{repo_id}`
- **Version:** `{version}`
- **Baseline Date:** `{date_str}`
- **Compacted Feature Specs:** {len(hierarchy.feature_specs_since_baseline)}
{prior_baseline_note}

## 1. System Scope & Accepted Capabilities

This baseline establishes the accepted specification state for `{repo_id}` version `{version}`.

## 2. Integrated Feature Specifications

{chr(10).join(feature_specs_content) if feature_specs_content else "_No incremental feature specs compacted in this cycle._"}

## 3. Invariants & Acceptance Contracts

- All integrated feature capabilities have passed verification and security requirements.
- Any subsequent feature development must treat this baseline as canonical context.
"""
    baseline_path.write_text(baseline_doc, encoding="utf-8")

    # 2. Synthesize New Decision Knowledgebase Archive
    archive_filename = f"decision-knowledgebase-{repo_id}-{version}-{date_str}.md"
    archive_path = specs_dir / archive_filename

    decisions_content: list[str] = []
    for dec_file in hierarchy.decision_logs_since_archive:
        text = dec_file.read_text(encoding="utf-8")
        clean_text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
        decisions_content.append(f"### Decisions from `{dec_file.stem}`\n\n{clean_text.strip()}\n")

    prior_archive_note = ""
    if hierarchy.latest_decision_archive:
        prior_archive_note = f"\n*Supersedes decision knowledgebase: `{hierarchy.latest_decision_archive.name}`*\n"

    archive_doc = f"""# Decision Knowledgebase: {repo_id}

- **Repository:** `{repo_id}`
- **Version:** `{version}`
- **Archive Date:** `{date_str}`
- **Compacted Decision Logs:** {len(hierarchy.decision_logs_since_archive)}
{prior_archive_note}

## 1. Historical Architecture & Design Decisions

This document summarizes accepted decisions, rejected alternatives, rationale, and constraints compacted during rotation.

## 2. Consolidated Decision Records

{chr(10).join(decisions_content) if decisions_content else "_No incremental decision logs compacted in this cycle._"}

## 3. Active Architectural Invariants

- Decisions recorded here remain in force unless explicitly superseded by a future decision log.
"""
    archive_path.write_text(archive_doc, encoding="utf-8")

    # 3. Refresh Repository Index
    index_filename = f"{date_str}-{repo_id}.md"
    index_path = specs_dir / index_filename
    index_doc = generate_repository_index(storage.workspace_root, repo_id, version)
    index_path.write_text(index_doc, encoding="utf-8")

    # 4. Commit and Synchronize
    commit_msg = f"rotate(spec-state): rotate baseline, decisions, and index for {repo_id} v{version}"
    sync_res = storage.sync_push(commit_msg)

    return {
        "status": "rotated",
        "baseline": str(baseline_path),
        "decision_archive": str(archive_path),
        "index": str(index_path),
        "specs_compacted": len(hierarchy.feature_specs_since_baseline),
        "decisions_compacted": len(hierarchy.decision_logs_since_archive),
        "sync": sync_res,
    }


def apply_retention(
    config: SpecStateConfig,
    storage: GitStorage,
    hierarchy: SpecHierarchy,
    dry_run: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    """Archive historical artifacts exceeding retention limits."""
    specs_dir = storage.get_repo_specs_dir()

    if not config.retention.cleanup_archived_artifacts and not force:
        return {
            "status": "skipped_by_policy",
            "message": "Retention cleanup is disabled by policy (retention.cleanup_archived_artifacts: false).",
            "cleaned": [],
            "retained": [f.name for f in hierarchy.all_artifacts],
        }

    # Discover all historical baselines
    baselines: list[tuple[str, Path]] = []
    for f in specs_dir.iterdir():
        if f.is_file() and BASELINE_PATTERN.match(f.name):
            m = BASELINE_PATTERN.match(f.name)
            if m:
                baselines.append((m.group(3), f))

    baselines.sort(key=lambda x: x[0], reverse=True)

    keep_count = config.retention.keep_current_baseline + config.retention.keep_previous_baselines
    retained_baselines = baselines[:keep_count]
    excess_baselines = baselines[keep_count:]

    cleaned: list[str] = []
    archive_dir = specs_dir / "archive"

    if excess_baselines:
        cutoff_date = retained_baselines[-1][0] if retained_baselines else "99999999"

        # Candidates to archive: excess baselines and artifacts strictly older than cutoff_date
        candidates: list[Path] = [p for (_, p) in excess_baselines]

        for f in specs_dir.iterdir():
            if f.is_file() and f not in [p for (_, p) in retained_baselines]:
                # Extract date
                m_date = re.match(r"^(\d{8})-", f.name)
                if m_date and m_date.group(1) < cutoff_date:
                    candidates.append(f)

        for item in candidates:
            cleaned.append(item.name)
            if not dry_run:
                archive_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(archive_dir / item.name))

    sync_res = {}
    if not dry_run and cleaned:
        sync_res = storage.sync_push(f"cleanup(spec-state): archive {len(cleaned)} historical artifacts")

    return {
        "status": "cleaned" if not dry_run else "dry_run",
        "cleaned": cleaned,
        "archive_dir": str(archive_dir) if cleaned else None,
        "retained_baselines": [p.name for (_, p) in retained_baselines],
        "sync": sync_res,
    }
