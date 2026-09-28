#!/usr/bin/env python3
"""Git storage and artifact hierarchy resolution for ai-sdlc-spec-state."""

from __future__ import annotations

import datetime
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from spec_state_config import SpecStateConfig

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
from ai_sdlc_safe_io import atomic_write_text, bounded_path, ensure_directory  # noqa: E402


BASELINE_PATTERN = re.compile(r"^baselinespec-(.+?)-(\d+\.\d+\.\d+)-(\d{8})\.md$")
DECISION_ARCHIVE_PATTERN = re.compile(r"^decision-knowledgebase-(.+?)-(\d+\.\d+\.\d+)-(\d{8})\.md$")
INDEX_PATTERN = re.compile(r"^(\d{8})-(.+?)(?:-index)?\.md$")
SPEC_PATTERN = re.compile(r"^(\d{8})-(.+?)-spec\.md$")
DECISION_LOG_PATTERN = re.compile(r"^(\d{8})-(.+?)-decisions?\.md$")
PLAN_PATTERN = re.compile(r"^(\d{8})-(.+?)-plan\.md$")
READABLE_PATTERN = re.compile(r"^(\d{8})-(.+?)-readable\.md$")


@dataclass
class SpecHierarchy:
    latest_index: Optional[Path] = None
    latest_index_date: Optional[str] = None
    latest_baseline: Optional[Path] = None
    latest_baseline_version: Optional[str] = None
    latest_baseline_date: Optional[str] = None
    latest_decision_archive: Optional[Path] = None
    latest_decision_archive_version: Optional[str] = None
    latest_decision_archive_date: Optional[str] = None
    decision_logs_since_archive: list[Path] = field(default_factory=list)
    feature_specs_since_baseline: list[Path] = field(default_factory=list)
    plans: list[Path] = field(default_factory=list)
    readable_specs: list[Path] = field(default_factory=list)
    all_artifacts: list[Path] = field(default_factory=list)
    storage_dir: Optional[Path] = None


class GitStorage:
    """Manages Git-backed specification state repository."""

    def __init__(self, config: SpecStateConfig, workspace_root: Optional[Path] = None):
        self.config = config
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self._local_storage_path: Optional[Path] = None

    def _is_local_repository(self, target: str) -> bool:
        """Determine if target repository is a local directory."""
        if target.startswith("file://") or target.startswith("/") or target.startswith("./") or target.startswith("../"):
            return True
        # Check if target exists as a local folder relative to workspace_root
        candidate = (self.workspace_root / target).resolve()
        return candidate.is_dir()

    def get_storage_path(self) -> Path:
        """Resolve the local path where the storage repo is mounted/checked out."""
        if self._local_storage_path:
            return self._local_storage_path

        target = self.config.storage.repository
        if self._is_local_repository(target):
            clean_target = target.removeprefix("file://")
            local_p = Path(clean_target)
            if not local_p.is_absolute():
                local_p = (self.workspace_root / local_p).resolve()
            self._local_storage_path = local_p
            return self._local_storage_path

        # Remote git repo: cache in .ai-sdlc/spec-state/storage_repo
        cache_dir = self.workspace_root / ".ai-sdlc" / "spec-state" / "storage_repo"
        self._local_storage_path = cache_dir
        return self._local_storage_path

    def ensure_storage_ready(self) -> Path:
        """Ensure storage directory exists, initialized as a git repo or cloned from remote."""
        storage_path = self.get_storage_path()
        storage_path.mkdir(parents=True, exist_ok=True)

        git_dir = storage_path / ".git"
        if not git_dir.exists():
            target = self.config.storage.repository
            if self._is_local_repository(target):
                # Initialize local Git repository if not initialized
                subprocess.run(["git", "init", "-b", self.config.storage.branch], cwd=storage_path, check=False, capture_output=True)
                # If git init with -b fails on older git, do git init then git checkout -B
                if not git_dir.exists():
                    subprocess.run(["git", "init"], cwd=storage_path, check=True, capture_output=True)
                    subprocess.run(["git", "checkout", "-B", self.config.storage.branch], cwd=storage_path, check=False, capture_output=True)
            else:
                # Attempt to clone remote
                res = subprocess.run(
                    ["git", "clone", "--branch", self.config.storage.branch, target, str(storage_path)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if res.returncode != 0:
                    # Clone failed (could be non-existent remote or branch, or offline test); fallback to init with origin
                    subprocess.run(["git", "init"], cwd=storage_path, check=True, capture_output=True)
                    subprocess.run(["git", "checkout", "-B", self.config.storage.branch], cwd=storage_path, check=False, capture_output=True)
                    subprocess.run(["git", "remote", "add", "origin", target], cwd=storage_path, check=False, capture_output=True)

        return storage_path

    def get_repo_specs_dir(self) -> Path:
        """Return the directory inside storage where this repo's specifications live."""
        storage_root = self.ensure_storage_ready()
        root_section = self.config.storage.root.strip("/")
        repo_id = self.config.repository.id

        if root_section:
            specs_dir = storage_root / root_section / repo_id
        else:
            specs_dir = storage_root / repo_id

        specs_dir.mkdir(parents=True, exist_ok=True)
        return specs_dir

    def sync_push(self, commit_message: str) -> dict[str, Any]:
        """Commit changes in storage and push to origin if configured."""
        storage_root = self.ensure_storage_ready()
        result = {"committed": False, "pushed": False, "status": "clean", "error": None}

        try:
            # Stage everything
            subprocess.run(["git", "add", "-A"], cwd=storage_root, check=True, capture_output=True)

            # Check if there are changes to commit
            status_res = subprocess.run(
                ["git", "status", "--porcelain"], cwd=storage_root, check=True, capture_output=True, text=True
            )
            if not status_res.stdout.strip():
                result["status"] = "clean"
                return result

            # Commit
            commit_res = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=storage_root,
                check=False,
                capture_output=True,
                text=True,
            )
            if commit_res.returncode == 0:
                result["committed"] = True
                result["status"] = "committed"
            else:
                result["error"] = commit_res.stderr.strip()
                return result

            # Try to push if remote origin exists
            remotes = subprocess.run(["git", "remote"], cwd=storage_root, capture_output=True, text=True).stdout.split()
            if "origin" in remotes and not self._is_local_repository(self.config.storage.repository):
                push_res = subprocess.run(
                    ["git", "push", "origin", self.config.storage.branch],
                    cwd=storage_root,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if push_res.returncode == 0:
                    result["pushed"] = True
                    result["status"] = "synced"
                else:
                    result["status"] = "ahead"
                    result["error"] = push_res.stderr.strip()
            else:
                result["status"] = "committed_locally"

        except Exception as exc:
            result["error"] = str(exc)
            result["status"] = "error"

        return result

    def check_sync_status(self) -> str:
        """Check sync health: clean, ahead, behind, diverged, or offline."""
        storage_root = self.ensure_storage_ready()
        try:
            status_res = subprocess.run(
                ["git", "status", "--porcelain"], cwd=storage_root, check=True, capture_output=True, text=True
            )
            if status_res.stdout.strip():
                return "dirty"

            remotes = subprocess.run(["git", "remote"], cwd=storage_root, capture_output=True, text=True).stdout.split()
            if "origin" not in remotes:
                return "clean"

            # Check upstream branch tracking
            rev_res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "@{upstream}"],
                cwd=storage_root,
                check=False,
                capture_output=True,
                text=True,
            )
            if rev_res.returncode != 0:
                return "clean"

            counts = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", f"HEAD...{rev_res.stdout.strip()}"],
                cwd=storage_root,
                check=False,
                capture_output=True,
                text=True,
            )
            if counts.returncode == 0 and counts.stdout.strip():
                ahead, behind = (int(x) for x in counts.stdout.strip().split())
                if ahead > 0 and behind > 0:
                    return "diverged"
                if ahead > 0:
                    return "ahead"
                if behind > 0:
                    return "behind"

            return "clean"
        except Exception:
            return "offline"


def resolve_spec_hierarchy(storage: GitStorage) -> SpecHierarchy:
    """Scan the repository storage folder and build the deterministic SpecHierarchy."""
    specs_dir = storage.get_repo_specs_dir()
    hierarchy = SpecHierarchy(storage_dir=specs_dir)

    if not specs_dir.exists():
        return hierarchy

    all_files = sorted([f for f in specs_dir.iterdir() if f.is_file()], key=lambda p: p.name)
    hierarchy.all_artifacts = all_files

    baselines: list[tuple[str, str, str, Path]] = []  # (date, version, repo_id, path)
    decision_archives: list[tuple[str, str, str, Path]] = []
    indexes: list[tuple[str, Path]] = []
    feature_specs: list[tuple[str, Path]] = []
    decision_logs: list[tuple[str, Path]] = []
    plans: list[Path] = []
    readable_specs: list[Path] = []

    repo_id = storage.config.repository.id

    for file_path in all_files:
        name = file_path.name

        # 1. Baseline spec check: baselinespec-<repo>-<version>-<date>.md
        b_match = BASELINE_PATTERN.match(name)
        if b_match:
            b_repo, b_ver, b_date = b_match.groups()
            baselines.append((b_date, b_ver, b_repo, file_path))
            continue

        # 2. Decision archive check: decision-knowledgebase-<repo>-<version>-<date>.md
        da_match = DECISION_ARCHIVE_PATTERN.match(name)
        if da_match:
            da_repo, da_ver, da_date = da_match.groups()
            decision_archives.append((da_date, da_ver, da_repo, file_path))
            continue

        # 3. Plan check
        if PLAN_PATTERN.match(name):
            plans.append(file_path)

        # 4. Readable spec check
        if READABLE_PATTERN.match(name):
            readable_specs.append(file_path)

        # 5. Incremental feature spec check
        s_match = SPEC_PATTERN.match(name)
        if s_match:
            s_date, _ = s_match.groups()
            feature_specs.append((s_date, file_path))
            continue

        # 6. Incremental decision log check
        d_match = DECISION_LOG_PATTERN.match(name)
        if d_match:
            d_date, _ = d_match.groups()
            decision_logs.append((d_date, file_path))
            continue

        # 7. Index check: YYYYMMDD-<repo_id>.md or YYYYMMDD-<repo_id>-index.md
        i_match = INDEX_PATTERN.match(name)
        if i_match:
            i_date, i_slug = i_match.groups()
            if repo_id in i_slug:
                indexes.append((i_date, file_path))

    # Sort baselines by date descending
    baselines.sort(key=lambda item: item[0], reverse=True)
    if baselines:
        latest_b_date, latest_b_ver, _, latest_b_path = baselines[0]
        hierarchy.latest_baseline = latest_b_path
        hierarchy.latest_baseline_version = latest_b_ver
        hierarchy.latest_baseline_date = latest_b_date

    # Sort decision archives by date descending
    decision_archives.sort(key=lambda item: item[0], reverse=True)
    if decision_archives:
        latest_da_date, latest_da_ver, _, latest_da_path = decision_archives[0]
        hierarchy.latest_decision_archive = latest_da_path
        hierarchy.latest_decision_archive_version = latest_da_ver
        hierarchy.latest_decision_archive_date = latest_da_date

    # Sort indexes by date descending
    indexes.sort(key=lambda item: item[0], reverse=True)
    if indexes:
        hierarchy.latest_index_date, hierarchy.latest_index = indexes[0]

    # Filter incremental feature specs after latest baseline date
    # (If no baseline exists, all feature specs are incremental)
    if hierarchy.latest_baseline_date:
        hierarchy.feature_specs_since_baseline = [
            path for (s_date, path) in feature_specs if s_date >= hierarchy.latest_baseline_date and path != hierarchy.latest_baseline
        ]
    else:
        hierarchy.feature_specs_since_baseline = [path for (_, path) in feature_specs]

    # Filter incremental decision logs after latest decision archive date
    if hierarchy.latest_decision_archive_date:
        hierarchy.decision_logs_since_archive = [
            path for (d_date, path) in decision_logs if d_date >= hierarchy.latest_decision_archive_date and path != hierarchy.latest_decision_archive
        ]
    else:
        hierarchy.decision_logs_since_archive = [path for (_, path) in decision_logs]

    hierarchy.plans = plans
    hierarchy.readable_specs = readable_specs

    return hierarchy


def publish_feature_artifacts(
    config: SpecStateConfig,
    storage: GitStorage,
    feature: str,
    artifact_files: dict[str, Path | str],
    ticket_id: Optional[str] = None,
    logical_spec_id: Optional[str] = None,
    commit: bool = True,
) -> dict[str, Any]:
    """Publish feature artifacts into the repository specification storage directory."""
    specs_dir = storage.get_repo_specs_dir()
    date_str = datetime.date.today().strftime("%Y%m%d")

    clean_feature = re.sub(r"^\d{8}-", "", feature).strip().lower()
    clean_feature = re.sub(r"[^a-z0-9_-]+", "-", clean_feature).strip("-")

    published: dict[str, str] = {}

    type_to_suffix = {
        "spec": "spec.md",
        "plan": "plan.md",
        "decisions": "decisions.md",
        "readable": "readable.md",
    }

    frontmatter_extra = []
    if logical_spec_id:
        frontmatter_extra.append(f"{config.multi_repo.logical_spec_id_field}: {logical_spec_id}")
    if ticket_id:
        frontmatter_extra.append(f"ticket_id: {ticket_id}")
    frontmatter_extra.append(f"repository_id: {config.repository.id}")
    frontmatter_extra.append(f"version: {config.repository.version}")
    frontmatter_extra.append(f"date: {date_str}")

    for art_type, source in artifact_files.items():
        if art_type not in type_to_suffix:
            continue

        filename = f"{date_str}-{clean_feature}-{type_to_suffix[art_type]}"
        target_path = specs_dir / filename

        content = ""
        if isinstance(source, Path) and source.is_file():
            content = source.read_text(encoding="utf-8")
        elif isinstance(source, str):
            if os.path.isfile(source):
                content = Path(source).read_text(encoding="utf-8")
            else:
                content = source

        # Ensure frontmatter with spec_id and repo metadata
        if content.startswith("---"):
            # Update existing frontmatter
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm_body = parts[1].strip()
                for line in frontmatter_extra:
                    k = line.split(":", 1)[0].strip()
                    if f"{k}:" not in fm_body:
                        fm_body += f"\n{line}"
                content = f"---\n{fm_body}\n---{parts[2]}"
        else:
            fm_text = "\n".join(frontmatter_extra)
            content = f"---\n{fm_text}\n---\n\n{content}"

        target_path.write_text(content, encoding="utf-8")
        published[art_type] = str(target_path)

    sync_result = {}
    if commit and published:
        commit_msg = f"publish(spec-state): synchronize artifacts for feature '{clean_feature}'"
        sync_result = storage.sync_push(commit_msg)

    return {
        "feature": clean_feature,
        "date": date_str,
        "published": published,
        "sync": sync_result,
        "storage_dir": str(specs_dir),
    }
