#!/usr/bin/env python3
"""Configuration parser and validator for ai-sdlc-spec-state."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402


SCHEMA_NAME = "ai-sdlc-spec-state-schema/v1"
CONFIG_FILENAME = ".sdlc.toon"
REPO_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")


@dataclass
class StorageConfig:
    provider: str = "git"
    repository: str = "shared/agent-planning-docs"
    branch: str = "main"
    root: str = "specs"


@dataclass
class RepoConfig:
    id: str = "my-service"
    version: str = "1.0.0"
    source: str = "."


@dataclass
class ArtifactsConfig:
    baseline_spec: bool = True
    decision_logs: bool = True
    feature_specs: bool = True
    index: bool = True
    plans: bool = True
    readable_specs: bool = True


@dataclass
class LifecycleConfig:
    decision_archive_after_specs: int = 50
    fetch_before_feature: bool = True
    publish_before_pr: bool = True
    refresh_index_after_days: int = 14
    rotation_spec_threshold: int = 50


@dataclass
class RetentionConfig:
    cleanup_archived_artifacts: bool = False
    keep_current_baseline: int = 1
    keep_previous_baselines: int = 2


@dataclass
class ConfluenceIntegrationConfig:
    enabled: bool = False
    space: str = ""


@dataclass
class IntegrationsConfig:
    confluence: ConfluenceIntegrationConfig = field(default_factory=ConfluenceIntegrationConfig)


@dataclass
class MultiRepoConfig:
    logical_spec_id_field: str = "spec_id"
    strategy: str = "duplicate"  # "duplicate" or "canonical"


@dataclass
class ImpactConfig:
    enabled: bool = False
    refresh_index_threshold: int = 10


@dataclass
class SpecStateConfig:
    schema: str = SCHEMA_NAME
    enabled: bool = True
    storage: StorageConfig = field(default_factory=StorageConfig)
    repository: RepoConfig = field(default_factory=RepoConfig)
    artifacts: ArtifactsConfig = field(default_factory=ArtifactsConfig)
    lifecycle: LifecycleConfig = field(default_factory=LifecycleConfig)
    retention: RetentionConfig = field(default_factory=RetentionConfig)
    integrations: IntegrationsConfig = field(default_factory=IntegrationsConfig)
    multi_repo: MultiRepoConfig = field(default_factory=MultiRepoConfig)
    impact: ImpactConfig = field(default_factory=ImpactConfig)
    config_path: Optional[Path] = None


def validate_config(data: dict[str, Any]) -> list[str]:
    """Validate dictionary structure against specification state schema rules."""
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["Configuration root must be a dictionary / object."]

    schema = data.get("schema")
    if not schema or not str(schema).startswith("ai-sdlc-spec-state-schema/"):
        errors.append(f"schema must be 'ai-sdlc-spec-state-schema/v1', got: {schema!r}")

    if "enabled" in data and not isinstance(data["enabled"], bool):
        errors.append("enabled must be a boolean.")

    # Storage validation
    storage = data.get("storage")
    if not isinstance(storage, dict):
        errors.append("storage section is required and must be an object.")
    else:
        provider = storage.get("provider")
        if provider != "git":
            errors.append(f"storage.provider must be 'git', got: {provider!r}")
        if not storage.get("repository") or not str(storage.get("repository")).strip():
            errors.append("storage.repository must be a non-empty string.")
        if not storage.get("branch") or not str(storage.get("branch")).strip():
            errors.append("storage.branch must be a non-empty string.")
        if not storage.get("root") or not str(storage.get("root")).strip():
            errors.append("storage.root must be a non-empty string.")

    # Repository validation
    repo = data.get("repository")
    if not isinstance(repo, dict):
        errors.append("repository section is required and must be an object.")
    else:
        repo_id = repo.get("id")
        if not repo_id or not isinstance(repo_id, str) or not REPO_ID_PATTERN.match(repo_id):
            errors.append(
                f"repository.id must be a non-empty alphanumeric identifier (allows '-', '_', '.'), got: {repo_id!r}"
            )
        if not repo.get("version") or not isinstance(repo.get("version"), str):
            errors.append("repository.version must be a non-empty version string.")

    # Lifecycle validation
    lifecycle = data.get("lifecycle", {})
    if isinstance(lifecycle, dict):
        refresh_days = lifecycle.get("refresh_index_after_days", 14)
        if not isinstance(refresh_days, int) or refresh_days < 1:
            errors.append(f"lifecycle.refresh_index_after_days must be an integer >= 1, got: {refresh_days!r}")
        rot_threshold = lifecycle.get("rotation_spec_threshold", 50)
        if not isinstance(rot_threshold, int) or rot_threshold < 1:
            errors.append(f"lifecycle.rotation_spec_threshold must be an integer >= 1, got: {rot_threshold!r}")
        dec_specs = lifecycle.get("decision_archive_after_specs", 50)
        if not isinstance(dec_specs, int) or dec_specs < 1:
            errors.append(f"lifecycle.decision_archive_after_specs must be an integer >= 1, got: {dec_specs!r}")

    # Retention validation
    retention = data.get("retention", {})
    if isinstance(retention, dict):
        keep_curr = retention.get("keep_current_baseline", 1)
        if not isinstance(keep_curr, int) or keep_curr < 1:
            errors.append(f"retention.keep_current_baseline must be an integer >= 1, got: {keep_curr!r}")
        keep_prev = retention.get("keep_previous_baselines", 2)
        if not isinstance(keep_prev, int) or keep_prev < 0:
            errors.append(f"retention.keep_previous_baselines must be an integer >= 0, got: {keep_prev!r}")

    # Multi-repo validation
    multi_repo = data.get("multi_repo", {})
    if isinstance(multi_repo, dict):
        strat = multi_repo.get("strategy", "duplicate")
        if strat not in ("duplicate", "canonical"):
            errors.append(f"multi_repo.strategy must be 'duplicate' or 'canonical', got: {strat!r}")

    return errors


def find_config_file(explicit_path: Optional[Path] = None, root: Optional[Path] = None) -> Optional[Path]:
    """Search for .sdlc.toon from given explicit path, root, or walking upwards from CWD."""
    if explicit_path:
        p = explicit_path.resolve()
        if p.is_file():
            return p
        if p.is_dir() and (p / CONFIG_FILENAME).is_file():
            return p / CONFIG_FILENAME
        return None

    search_dir = (root or Path.cwd()).resolve()
    for current in [search_dir, *search_dir.parents]:
        candidate = current / CONFIG_FILENAME
        if candidate.is_file():
            return candidate
        # Stop at Git root boundary
        if (current / ".git").exists():
            break

    return None


def load_config(path: Optional[Path] = None, root: Optional[Path] = None) -> SpecStateConfig:
    """Discover, load, and validate .sdlc.toon configuration."""
    config_file = find_config_file(path, root)
    if not config_file or not config_file.is_file():
        searched = str(path or root or Path.cwd())
        raise FileNotFoundError(
            f"Specification state configuration file '{CONFIG_FILENAME}' not found (searched from {searched}). "
            "Run 'python3 skills/ai-sdlc-spec-state/scripts/spec_state.py init' or 'spec-state init' to create one."
        )

    content = config_file.read_text(encoding="utf-8")
    raw_data = toon_codec.loads(content)

    if not isinstance(raw_data, dict):
        raise ValueError(f"Corrupted or invalid TOON configuration in {config_file}: expected key-value mapping.")

    errors = validate_config(raw_data)
    if errors:
        raise ValueError(f"Invalid specification state configuration in {config_file}:\n" + "\n".join(f"  - {e}" for e in errors))

    # Parse Storage
    st_dict = raw_data.get("storage", {})
    storage = StorageConfig(
        provider=st_dict.get("provider", "git"),
        repository=str(st_dict.get("repository", "shared/agent-planning-docs")),
        branch=str(st_dict.get("branch", "main")),
        root=str(st_dict.get("root", "specs")),
    )

    # Parse Repository
    rp_dict = raw_data.get("repository", {})
    repository = RepoConfig(
        id=str(rp_dict.get("id", "my-service")),
        version=str(rp_dict.get("version", "1.0.0")),
        source=str(rp_dict.get("source", ".")),
    )

    # Parse Artifacts
    art_dict = raw_data.get("artifacts", {})
    artifacts = ArtifactsConfig(
        baseline_spec=bool(art_dict.get("baseline_spec", True)),
        decision_logs=bool(art_dict.get("decision_logs", True)),
        feature_specs=bool(art_dict.get("feature_specs", True)),
        index=bool(art_dict.get("index", True)),
        plans=bool(art_dict.get("plans", True)),
        readable_specs=bool(art_dict.get("readable_specs", True)),
    )

    # Parse Lifecycle
    lc_dict = raw_data.get("lifecycle", {})
    lifecycle = LifecycleConfig(
        decision_archive_after_specs=int(lc_dict.get("decision_archive_after_specs", 50)),
        fetch_before_feature=bool(lc_dict.get("fetch_before_feature", True)),
        publish_before_pr=bool(lc_dict.get("publish_before_pr", True)),
        refresh_index_after_days=int(lc_dict.get("refresh_index_after_days", 14)),
        rotation_spec_threshold=int(lc_dict.get("rotation_spec_threshold", 50)),
    )

    # Parse Retention
    rt_dict = raw_data.get("retention", {})
    retention = RetentionConfig(
        cleanup_archived_artifacts=bool(rt_dict.get("cleanup_archived_artifacts", False)),
        keep_current_baseline=int(rt_dict.get("keep_current_baseline", 1)),
        keep_previous_baselines=int(rt_dict.get("keep_previous_baselines", 2)),
    )

    # Parse Integrations
    it_dict = raw_data.get("integrations", {})
    conf_dict = it_dict.get("confluence", {}) if isinstance(it_dict, dict) else {}
    integrations = IntegrationsConfig(
        confluence=ConfluenceIntegrationConfig(
            enabled=bool(conf_dict.get("enabled", False)),
            space=str(conf_dict.get("space", "")),
        )
    )

    # Parse MultiRepo
    mr_dict = raw_data.get("multi_repo", {})
    multi_repo = MultiRepoConfig(
        logical_spec_id_field=str(mr_dict.get("logical_spec_id_field", "spec_id")),
        strategy=str(mr_dict.get("strategy", "duplicate")),
    )

    # Parse Impact
    im_dict = raw_data.get("impact", {})
    impact = ImpactConfig(
        enabled=bool(im_dict.get("enabled", False)),
        refresh_index_threshold=int(im_dict.get("refresh_index_threshold", 10)),
    )

    return SpecStateConfig(
        schema=str(raw_data.get("schema", SCHEMA_NAME)),
        enabled=bool(raw_data.get("enabled", True)),
        storage=storage,
        repository=repository,
        artifacts=artifacts,
        lifecycle=lifecycle,
        retention=retention,
        integrations=integrations,
        multi_repo=multi_repo,
        impact=impact,
        config_path=config_file,
    )


def init_config(
    target_path: Path,
    repo_id: str = "my-service",
    version: str = "1.0.0",
    storage_repo: str = "shared/agent-planning-docs",
    branch: str = "main",
    root: str = "specs",
    force: bool = False,
) -> SpecStateConfig:
    """Create a new .sdlc.toon configuration file with standard defaults."""
    target_file = target_path / CONFIG_FILENAME if target_path.is_dir() else target_path

    if target_file.exists() and not force:
        raise FileExistsError(
            f"Configuration file already exists at {target_file}. Use force=True to overwrite."
        )

    config_dict = {
        "schema": SCHEMA_NAME,
        "enabled": True,
        "storage": {
            "branch": branch,
            "provider": "git",
            "repository": storage_repo,
            "root": root,
        },
        "repository": {
            "id": repo_id,
            "source": ".",
            "version": version,
        },
        "artifacts": {
            "baseline_spec": True,
            "decision_logs": True,
            "feature_specs": True,
            "index": True,
            "plans": True,
            "readable_specs": True,
        },
        "lifecycle": {
            "decision_archive_after_specs": 50,
            "fetch_before_feature": True,
            "publish_before_pr": True,
            "refresh_index_after_days": 14,
            "rotation_spec_threshold": 50,
        },
        "retention": {
            "cleanup_archived_artifacts": False,
            "keep_current_baseline": 1,
            "keep_previous_baselines": 2,
        },
        "integrations": {
            "confluence": {
                "enabled": False,
                "space": "",
            }
        },
        "multi_repo": {
            "logical_spec_id_field": "spec_id",
            "strategy": "duplicate",
        },
        "impact": {
            "enabled": False,
            "refresh_index_threshold": 10,
        },
    }

    target_file.parent.mkdir(parents=True, exist_ok=True)
    rendered = toon_codec.dumps(config_dict)
    target_file.write_text(rendered, encoding="utf-8")

    return load_config(target_file)


def detect_repo_id(workspace_root: Path) -> str:
    """Auto-detect sensible repository identifier from manifests, git origin, or directory name."""
    # 1. Check pyproject.toml
    pyproject = workspace_root / "pyproject.toml"
    if pyproject.is_file():
        try:
            m = re.search(r'^\s*name\s*=\s*["\']([^"\']+)["\']', pyproject.read_text(encoding="utf-8"), re.MULTILINE)
            if m:
                return re.sub(r"[^a-zA-Z0-9_\-\.]", "-", m.group(1)).strip("-")
        except Exception:
            pass

    # 2. Check package.json
    pkg_json = workspace_root / "package.json"
    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            if "name" in data and isinstance(data["name"], str):
                clean_name = data["name"].split("/")[-1].replace("@", "")
                return re.sub(r"[^a-zA-Z0-9_\-\.]", "-", clean_name).strip("-")
        except Exception:
            pass

    # 3. Check git origin URL
    try:
        res = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            url = res.stdout.strip()
            slug = url.rstrip("/").split("/")[-1].removesuffix(".git")
            if slug:
                return re.sub(r"[^a-zA-Z0-9_\-\.]", "-", slug).strip("-")
    except Exception:
        pass

    # 4. Fallback to folder name
    return re.sub(r"[^a-zA-Z0-9_\-\.]", "-", workspace_root.name).strip("-") or "my-service"


def detect_repo_version(workspace_root: Path) -> str:
    """Auto-detect initial repository semver version."""
    pyproject = workspace_root / "pyproject.toml"
    if pyproject.is_file():
        try:
            m = re.search(r'^\s*version\s*=\s*["\']([^"\']+)["\']', pyproject.read_text(encoding="utf-8"), re.MULTILINE)
            if m:
                return m.group(1).strip()
        except Exception:
            pass

    pkg_json = workspace_root / "package.json"
    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            if "version" in data and isinstance(data["version"], str):
                return data["version"].strip()
        except Exception:
            pass

    try:
        res = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            ver = res.stdout.strip().lstrip("v")
            if ver:
                return ver
    except Exception:
        pass

    return "1.0.0"


def run_wizard(
    workspace_root: Optional[Path] = None,
    target_file: Optional[Path] = None,
    interactive: bool = True,
    defaults_override: Optional[dict[str, Any]] = None,
    force: bool = False,
) -> SpecStateConfig:
    """Run an interactive or automated setup wizard to configure .sdlc.toon."""
    ws = (workspace_root or Path.cwd()).resolve()
    target = target_file or (ws / CONFIG_FILENAME)
    overrides = defaults_override or {}

    detected_id = detect_repo_id(ws)
    detected_ver = detect_repo_version(ws)

    def _ask(prompt_text: str, default_val: Any) -> str:
        if (
            not interactive
            or not sys.stdin
            or not hasattr(sys.stdin, "isatty")
            or not sys.stdin.isatty()
            or os.environ.get("AI_SDLC_NON_INTERACTIVE") == "1"
        ):
            return str(default_val)
        try:
            sys.stdout.write(f"{prompt_text} [{default_val}]: ")
            sys.stdout.flush()
            val = sys.stdin.readline().strip()
            return val if val else str(default_val)
        except (EOFError, KeyboardInterrupt):
            return str(default_val)

    if interactive and sys.stdin.isatty():
        sys.stdout.write("\n" + "=" * 72 + "\n")
        sys.stdout.write("  AI SDLC Specification State Setup Wizard (.sdlc.toon)\n")
        sys.stdout.write("=" * 72 + "\n")
        sys.stdout.write("Configures persistent specification state and synchronization rules.\n\n")

    # Step 1: Repository Identity
    repo_id = overrides.get("repo_id") or _ask("Step 1/4: Enter Repository ID", detected_id)
    version = overrides.get("version") or _ask("Step 1/4: Enter Initial Version", detected_ver)

    # Step 2: Storage Location
    default_storage = overrides.get("storage_repo") or "shared/agent-planning-docs"
    storage_repo = _ask("Step 2/4: Shared planning storage repository (Git remote or path)", default_storage)
    branch = overrides.get("branch") or _ask("Step 2/4: Storage branch name", "main")
    root_folder = overrides.get("root") or _ask("Step 2/4: Storage specs root folder", "specs")

    # Step 3: Freshness & Rotation
    refresh_days_str = overrides.get("refresh_days") or _ask("Step 3/4: Repository index refresh threshold (days)", 14)
    rotation_specs_str = overrides.get("rotation_specs") or _ask("Step 3/4: Automatic baseline rotation threshold (specs)", 50)

    try:
        refresh_days = int(refresh_days_str)
    except ValueError:
        refresh_days = 14

    try:
        rotation_specs = int(rotation_specs_str)
    except ValueError:
        rotation_specs = 50

    # Step 4: Multi-repo & Retention
    prev_baselines_str = overrides.get("keep_previous_baselines") or _ask("Step 4/4: Previous baselines to retain", 2)
    multi_repo_strat = overrides.get("multi_repo_strategy") or _ask("Step 4/4: Multi-repository strategy (duplicate/canonical)", "duplicate")
    if multi_repo_strat not in ("duplicate", "canonical"):
        multi_repo_strat = "duplicate"

    try:
        prev_baselines = int(prev_baselines_str)
    except ValueError:
        prev_baselines = 2

    # Scaffold the configuration
    cfg = init_config(
        target_path=target,
        repo_id=repo_id,
        version=version,
        storage_repo=storage_repo,
        branch=branch,
        root=root_folder,
        force=force,
    )

    # Apply wizard customization thresholds
    config_dict = toon_codec.loads(target.read_text(encoding="utf-8"))
    config_dict["lifecycle"]["refresh_index_after_days"] = refresh_days
    config_dict["lifecycle"]["rotation_spec_threshold"] = rotation_specs
    config_dict["retention"]["keep_previous_baselines"] = prev_baselines
    config_dict["multi_repo"]["strategy"] = multi_repo_strat
    target.write_text(toon_codec.dumps(config_dict), encoding="utf-8")

    if interactive and sys.stdin.isatty():
        sys.stdout.write("\n" + "=" * 72 + "\n")
        sys.stdout.write(f"  Configuration successfully initialized at: {target}\n")
        sys.stdout.write(f"  Repository: {repo_id} (v{version})\n")
        sys.stdout.write(f"  Storage: {storage_repo}:{branch} (root: {root_folder})\n")
        sys.stdout.write("=" * 72 + "\n\n")

    return load_config(target)

