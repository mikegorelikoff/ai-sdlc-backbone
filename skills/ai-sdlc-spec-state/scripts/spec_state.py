#!/usr/bin/env python3
"""Main CLI and Python library interface for ai-sdlc-spec-state."""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Optional

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402

from spec_state_config import CONFIG_FILENAME, SpecStateConfig, find_config_file, init_config, load_config, run_wizard
from spec_state_rotation import (
    ImpactScorer,
    apply_retention,
    check_index_freshness,
    check_rotation_triggers,
    generate_repository_index,
    rotate_baseline_and_decisions,
)
from spec_state_storage import GitStorage, SpecHierarchy, publish_feature_artifacts, resolve_spec_hierarchy


def ensure_config_or_wizard(
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    interactive: bool = True,
    auto_create: bool = True,
) -> SpecStateConfig:
    """Deterministically verify whether .sdlc.toon exists; if missing, launch the setup wizard."""
    found = find_config_file(config_path, root)
    if found and found.is_file():
        return load_config(found)

    if not auto_create:
        return load_config(config_path, root)

    ws = (root or Path.cwd()).resolve()
    target = config_path or (ws / CONFIG_FILENAME)
    sys.stderr.write(f"\n[ai-sdlc-spec-state] Deterministic check: '{CONFIG_FILENAME}' not found in {ws}.\n")
    sys.stderr.write("[ai-sdlc-spec-state] Launching setup wizard to establish specification state...\n\n")
    return run_wizard(workspace_root=ws, target_file=target, interactive=interactive)


def fetch_spec_state(
    feature: Optional[str] = None,
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    stage_dir: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Any]:
    """Retrieve and stage specification state hierarchy."""
    config = ensure_config_or_wizard(config_path, root, interactive=interactive)
    workspace = root or (config.config_path.parent if config.config_path else Path.cwd())
    storage = GitStorage(config, workspace_root=workspace)
    hierarchy = resolve_spec_hierarchy(storage)
    freshness = check_index_freshness(hierarchy.latest_index, config.lifecycle.refresh_index_after_days)
    triggers = check_rotation_triggers(config, hierarchy)

    # Local staging folder: .ai-sdlc/spec-state/context/
    context_stage = stage_dir or (workspace / ".ai-sdlc" / "spec-state" / "context")
    context_stage.mkdir(parents=True, exist_ok=True)

    staged_files: dict[str, str] = {}
    if hierarchy.latest_index and hierarchy.latest_index.is_file():
        dest = context_stage / "repository-index.md"
        shutil.copy2(hierarchy.latest_index, dest)
        staged_files["index"] = str(dest)

    if hierarchy.latest_baseline and hierarchy.latest_baseline.is_file():
        dest = context_stage / "latest-baseline.md"
        shutil.copy2(hierarchy.latest_baseline, dest)
        staged_files["baseline"] = str(dest)

    if hierarchy.latest_decision_archive and hierarchy.latest_decision_archive.is_file():
        dest = context_stage / "decision-knowledgebase.md"
        shutil.copy2(hierarchy.latest_decision_archive, dest)
        staged_files["decision_archive"] = str(dest)

    # Incremental specs staging
    inc_specs_staged: list[str] = []
    inc_specs_dir = context_stage / "feature-specs"
    inc_specs_dir.mkdir(parents=True, exist_ok=True)
    for sp in hierarchy.feature_specs_since_baseline:
        dest = inc_specs_dir / sp.name
        shutil.copy2(sp, dest)
        inc_specs_staged.append(str(dest))
    staged_files["incremental_specs"] = inc_specs_staged  # type: ignore

    # Incremental decision logs staging
    inc_dec_staged: list[str] = []
    inc_dec_dir = context_stage / "decision-logs"
    inc_dec_dir.mkdir(parents=True, exist_ok=True)
    for dl in hierarchy.decision_logs_since_archive:
        dest = inc_dec_dir / dl.name
        shutil.copy2(dl, dest)
        inc_dec_staged.append(str(dest))
    staged_files["incremental_decisions"] = inc_dec_staged  # type: ignore

    return {
        "status": "success",
        "repository_id": config.repository.id,
        "version": config.repository.version,
        "storage": f"{config.storage.repository}:{config.storage.branch}",
        "sync_state": storage.check_sync_status(),
        "index": {
            "path": str(hierarchy.latest_index) if hierarchy.latest_index else None,
            "date": hierarchy.latest_index_date,
            "status": freshness["status"],
            "age_days": freshness["age_days"],
            "needs_refresh": freshness["needs_refresh"],
        },
        "baseline": {
            "path": str(hierarchy.latest_baseline) if hierarchy.latest_baseline else None,
            "version": hierarchy.latest_baseline_version,
            "date": hierarchy.latest_baseline_date,
        },
        "decision_archive": {
            "path": str(hierarchy.latest_decision_archive) if hierarchy.latest_decision_archive else None,
            "date": hierarchy.latest_decision_archive_date,
        },
        "counts": {
            "feature_specs_since_baseline": len(hierarchy.feature_specs_since_baseline),
            "decision_logs_since_archive": len(hierarchy.decision_logs_since_archive),
            "plans": len(hierarchy.plans),
            "readable_specs": len(hierarchy.readable_specs),
            "total_artifacts": len(hierarchy.all_artifacts),
        },
        "rotation": triggers,
        "staged_context": str(context_stage),
        "staged_files": staged_files,
    }


def publish_spec_state(
    feature: str,
    artifacts: dict[str, Path | str],
    ticket_id: Optional[str] = None,
    logical_spec_id: Optional[str] = None,
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Any]:
    """Publish feature artifacts into persistent specification storage."""
    config = ensure_config_or_wizard(config_path, root, interactive=interactive)
    workspace = root or (config.config_path.parent if config.config_path else Path.cwd())
    storage = GitStorage(config, workspace_root=workspace)
    return publish_feature_artifacts(
        config=config,
        storage=storage,
        feature=feature,
        artifact_files=artifacts,
        ticket_id=ticket_id,
        logical_spec_id=logical_spec_id,
        commit=True,
    )


def status_spec_state(
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Any]:
    """Inspect current specification state and health metrics."""
    config = ensure_config_or_wizard(config_path, root, interactive=interactive)
    workspace = root or (config.config_path.parent if config.config_path else Path.cwd())
    storage = GitStorage(config, workspace_root=workspace)
    hierarchy = resolve_spec_hierarchy(storage)
    freshness = check_index_freshness(hierarchy.latest_index, config.lifecycle.refresh_index_after_days)
    triggers = check_rotation_triggers(config, hierarchy)

    return {
        "status": "success",
        "repository": {
            "id": config.repository.id,
            "version": config.repository.version,
            "source": config.repository.source,
        },
        "storage": {
            "provider": config.storage.provider,
            "repository": config.storage.repository,
            "branch": config.storage.branch,
            "root": config.storage.root,
            "sync_state": storage.check_sync_status(),
        },
        "index": {
            "path": str(hierarchy.latest_index) if hierarchy.latest_index else None,
            "date": hierarchy.latest_index_date,
            "status": freshness["status"],
            "age_days": freshness["age_days"],
            "threshold_days": freshness["threshold_days"],
            "needs_refresh": freshness["needs_refresh"],
            "message": freshness["message"],
        },
        "baseline": {
            "path": str(hierarchy.latest_baseline) if hierarchy.latest_baseline else None,
            "version": hierarchy.latest_baseline_version,
            "date": hierarchy.latest_baseline_date,
        },
        "decision_archive": {
            "path": str(hierarchy.latest_decision_archive) if hierarchy.latest_decision_archive else None,
            "date": hierarchy.latest_decision_archive_date,
        },
        "metrics": {
            "specs_since_baseline": len(hierarchy.feature_specs_since_baseline),
            "spec_threshold": config.lifecycle.rotation_spec_threshold,
            "decisions_since_archive": len(hierarchy.decision_logs_since_archive),
            "decision_threshold": config.lifecycle.decision_archive_after_specs,
            "total_artifacts": len(hierarchy.all_artifacts),
        },
        "rotation": triggers,
    }


def refresh_index(
    force: bool = False,
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Any]:
    """Generate or update the repository structural index."""
    config = ensure_config_or_wizard(config_path, root, interactive=interactive)
    workspace = root or (config.config_path.parent if config.config_path else Path.cwd())
    storage = GitStorage(config, workspace_root=workspace)
    hierarchy = resolve_spec_hierarchy(storage)
    freshness = check_index_freshness(hierarchy.latest_index, config.lifecycle.refresh_index_after_days)

    if not freshness["needs_refresh"] and not force:
        return {
            "status": "fresh",
            "message": f"Repository index is fresh ({freshness['age_days']} days old). Use --force to regenerate.",
            "path": freshness["path"],
        }

    date_str = datetime.date.today().strftime("%Y%m%d")
    repo_id = config.repository.id
    version = config.repository.version

    specs_dir = storage.get_repo_specs_dir()
    index_path = specs_dir / f"{date_str}-{repo_id}.md"

    doc = generate_repository_index(workspace, repo_id, version)
    index_path.write_text(doc, encoding="utf-8")

    sync_res = storage.sync_push(f"index(spec-state): refresh structural repository index for {repo_id}")

    return {
        "status": "refreshed",
        "path": str(index_path),
        "date": date_str,
        "sync": sync_res,
    }


def rotate_spec_state(
    force: bool = False,
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Any]:
    """Execute baseline and decision archive rotation."""
    config = ensure_config_or_wizard(config_path, root, interactive=interactive)
    workspace = root or (config.config_path.parent if config.config_path else Path.cwd())
    storage = GitStorage(config, workspace_root=workspace)
    hierarchy = resolve_spec_hierarchy(storage)
    return rotate_baseline_and_decisions(config, storage, hierarchy, force=force)


def cleanup_spec_state(
    dry_run: bool = False,
    force: bool = False,
    config_path: Optional[Path] = None,
    root: Optional[Path] = None,
    interactive: bool = True,
) -> dict[str, Any]:
    """Apply retention cleanup to archived historical artifacts."""
    config = ensure_config_or_wizard(config_path, root, interactive=interactive)
    workspace = root or (config.config_path.parent if config.config_path else Path.cwd())
    storage = GitStorage(config, workspace_root=workspace)
    hierarchy = resolve_spec_hierarchy(storage)
    return apply_retention(config, storage, hierarchy, dry_run=dry_run, force=force)


def format_output(data: dict[str, Any], fmt: str) -> str:
    """Format dictionary output as text table, toon, or json."""
    if fmt == "json":
        return json.dumps(data, indent=2)
    elif fmt == "toon":
        return toon_codec.dumps(data)

    # Human-readable text format
    lines = []
    if "status" in data:
        lines.append(f"Status: {data['status']}")
    for k, v in data.items():
        if k == "status":
            continue
        if isinstance(v, dict):
            lines.append(f"\n{k.upper()}:")
            for sub_k, sub_v in v.items():
                lines.append(f"  - {sub_k}: {sub_v}")
        elif isinstance(v, list):
            lines.append(f"\n{k.upper()}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="spec_state",
        description="ai-sdlc-spec-state: persistent specification state and lifecycle management",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Spec-state subcommand")

    # init
    init_p = subparsers.add_parser("init", help="Scaffold a new .sdlc.toon configuration file")
    init_p.add_argument("--repo-id", default="my-service", help="Current repository ID")
    init_p.add_argument("--version", default="1.0.0", help="Current repository version")
    init_p.add_argument("--storage-repo", default="shared/agent-planning-docs", help="Storage Git repository")
    init_p.add_argument("--branch", default="main", help="Storage Git branch")
    init_p.add_argument("--root", default="specs", help="Storage root folder")
    init_p.add_argument("--target", type=Path, default=Path.cwd(), help="Target directory or file path")
    init_p.add_argument("--force", action="store_true", help="Overwrite existing configuration file")
    init_p.add_argument("--wizard", action="store_true", help="Launch interactive step-by-step setup wizard")
    init_p.add_argument("--non-interactive", action="store_true", help="Use auto-detected defaults without prompting")

    # wizard
    wiz_p = subparsers.add_parser("wizard", help="Interactive step-by-step setup wizard for .sdlc.toon")
    wiz_p.add_argument("--target", type=Path, default=Path.cwd(), help="Target directory or file path")
    wiz_p.add_argument("--force", action="store_true", help="Overwrite existing configuration file")
    wiz_p.add_argument("--non-interactive", action="store_true", help="Use auto-detected defaults without prompting")

    # fetch
    fetch_p = subparsers.add_parser("fetch", help="Fetch and stage specification hierarchy")
    fetch_p.add_argument("--feature", help="Current feature context")
    fetch_p.add_argument("--stage-dir", type=Path, help="Override local staging directory")
    fetch_p.add_argument("--config", type=Path, help="Path to .sdlc.toon")
    fetch_p.add_argument("--format", choices=["text", "toon", "json"], default="text", help="Output format")

    # publish
    pub_p = subparsers.add_parser("publish", help="Publish feature artifacts to storage")
    pub_p.add_argument("--feature", required=True, help="Feature identifier slug")
    pub_p.add_argument("--spec", help="Path to feature specification markdown")
    pub_p.add_argument("--plan", help="Path to implementation plan markdown")
    pub_p.add_argument("--decisions", help="Path to decision log markdown")
    pub_p.add_argument("--readable", help="Path to human-readable specification")
    pub_p.add_argument("--ticket", help="Associated ticket ID (e.g. PROJ-123)")
    pub_p.add_argument("--logical-spec-id", help="Logical multi-repo spec ID")
    pub_p.add_argument("--config", type=Path, help="Path to .sdlc.toon")
    pub_p.add_argument("--format", choices=["text", "toon", "json"], default="text", help="Output format")

    # status
    status_p = subparsers.add_parser("status", help="Inspect specification state and sync health")
    status_p.add_argument("--config", type=Path, help="Path to .sdlc.toon")
    status_p.add_argument("--format", choices=["text", "toon", "json"], default="text", help="Output format")

    # refresh-index
    ref_p = subparsers.add_parser("refresh-index", help="Refresh repository structural index")
    ref_p.add_argument("--force", action="store_true", help="Force refresh even if index is fresh")
    ref_p.add_argument("--config", type=Path, help="Path to .sdlc.toon")
    ref_p.add_argument("--format", choices=["text", "toon", "json"], default="text", help="Output format")

    # rotate
    rot_p = subparsers.add_parser("rotate", help="Execute baseline & decision knowledgebase rotation")
    rot_p.add_argument("--force", action="store_true", help="Force rotation even if thresholds are not met")
    rot_p.add_argument("--config", type=Path, help="Path to .sdlc.toon")
    rot_p.add_argument("--format", choices=["text", "toon", "json"], default="text", help="Output format")

    # cleanup
    clean_p = subparsers.add_parser("cleanup", help="Apply retention cleanup")
    clean_p.add_argument("--dry-run", action="store_true", help="Preview artifacts to be cleaned without deleting")
    clean_p.add_argument("--force", action="store_true", help="Force cleanup even if disabled by config")
    clean_p.add_argument("--config", type=Path, help="Path to .sdlc.toon")
    clean_p.add_argument("--format", choices=["text", "toon", "json"], default="text", help="Output format")

    args = parser.parse_args()

    try:
        if args.command == "wizard" or (args.command == "init" and args.wizard):
            interactive = sys.stdin.isatty() and not getattr(args, "non_interactive", False)
            cfg = run_wizard(workspace_root=args.target, interactive=interactive, force=args.force)
            return 0

        elif args.command == "init":
            cfg = init_config(
                target_path=args.target,
                repo_id=args.repo_id,
                version=args.version,
                storage_repo=args.storage_repo,
                branch=args.branch,
                root=args.root,
                force=args.force,
            )
            print(f"Initialized specification state configuration at {cfg.config_path}")
            return 0

        elif args.command == "fetch":
            res = fetch_spec_state(
                feature=args.feature,
                config_path=args.config,
                stage_dir=args.stage_dir,
            )
            print(format_output(res, args.format))
            return 0

        elif args.command == "publish":
            artifacts: dict[str, str] = {}
            if args.spec:
                artifacts["spec"] = args.spec
            if args.plan:
                artifacts["plan"] = args.plan
            if args.decisions:
                artifacts["decisions"] = args.decisions
            if args.readable:
                artifacts["readable"] = args.readable

            if not artifacts:
                sys.stderr.write("Error: publish requires at least one artifact (--spec, --plan, --decisions, --readable)\n")
                return 1

            res = publish_spec_state(
                feature=args.feature,
                artifacts=artifacts,  # type: ignore
                ticket_id=args.ticket,
                logical_spec_id=args.logical_spec_id,
                config_path=args.config,
            )
            print(format_output(res, args.format))
            return 0

        elif args.command == "status":
            res = status_spec_state(config_path=args.config)
            print(format_output(res, args.format))
            return 0

        elif args.command == "refresh-index":
            res = refresh_index(force=args.force, config_path=args.config)
            print(format_output(res, args.format))
            return 0

        elif args.command == "rotate":
            res = rotate_spec_state(force=args.force, config_path=args.config)
            print(format_output(res, args.format))
            return 0

        elif args.command == "cleanup":
            res = cleanup_spec_state(dry_run=args.dry_run, force=args.force, config_path=args.config)
            print(format_output(res, args.format))
            return 0

    except Exception as exc:
        sys.stderr.write(f"Error ({args.command}): {exc}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
