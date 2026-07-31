#!/usr/bin/env python3
"""Install the harness deterministically without non-TOON machine artifacts."""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from contextlib import contextmanager
import fcntl
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parent
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


INSTALLER_ID = "ai-sdlc-harness/4.0.1"
LOCK_SCHEMA = "ai-sdlc-install-lock/v1"
RECORD_SCHEMA = "ai-sdlc-install-record/v2"
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REVISION_RE = re.compile(r"[0-9a-f]{40}")
LEGACY_MACHINE_SUFFIX = "." + "".join(chr(value) for value in (106, 115, 111, 110))


class InstallError(RuntimeError):
    """Raised when a deterministic installation precondition fails."""


def _run_git(source: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(source), *arguments],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def verify_source_identity(source: Path, revision: str) -> None:
    """Bind a Git-backed source checkout to the requested immutable revision."""
    result = _run_git(source, "rev-parse", "--verify", "HEAD")
    if result.returncode:
        raise InstallError("source must be a Git checkout with a committed HEAD")
    actual = result.stdout.strip()
    if actual != revision:
        raise InstallError(f"source revision mismatch: expected {revision}, found {actual}")
    status = _run_git(source, "status", "--porcelain", "--untracked-files=all")
    if status.returncode:
        raise InstallError(f"cannot inspect source status: {status.stderr.strip()}")
    if status.stdout.strip():
        raise InstallError("source checkout is dirty; use an immutable clean checkout")


def read_inventory(source: Path) -> list[str]:
    """Read and validate the canonical published skill inventory."""
    path = source / "config" / "ai-sdlc-managed-skills.txt"
    if path.is_symlink():
        raise InstallError("published inventory must not be a symbolic link")
    try:
        names = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise InstallError(f"cannot read published inventory: {exc}") from exc
    if not names or names != sorted(set(names)):
        raise InstallError("published inventory must contain unique sorted skill names")
    if any(not SKILL_NAME_RE.fullmatch(name) for name in names):
        raise InstallError("published inventory contains an invalid skill name")
    linked = [name for name in names if (source / "skills" / name).is_symlink()]
    if linked:
        raise InstallError("published skill roots must not be symbolic links: " + ", ".join(linked))
    missing = [name for name in names if not (source / "skills" / name / "SKILL.md").is_file()]
    if missing:
        raise InstallError("published skills are missing: " + ", ".join(missing))
    return names


def selected_inventory(published: list[str], requested: list[str]) -> tuple[list[str], str]:
    """Resolve an all-skills or explicit deterministic selection."""
    if not requested:
        return published, "all-skills"
    names = sorted(set(requested))
    unknown = sorted(set(names) - set(published))
    if unknown:
        raise InstallError("requested unpublished skills: " + ", ".join(unknown))
    if "ai-sdlc-shared-runtime" not in names:
        raise InstallError("explicit selection must include ai-sdlc-shared-runtime")
    return names, "explicit-skills"


def regular_files(directory: Path) -> list[Path]:
    """Return bounded regular files and reject links or alternate machine formats."""
    files: list[Path] = []
    for path in sorted(directory.rglob("*"), key=lambda item: item.relative_to(directory).as_posix()):
        relative = path.relative_to(directory)
        if "__pycache__" in relative.parts or path.suffix.lower() in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise InstallError(f"skill source contains a symbolic link: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise InstallError(f"skill source contains a non-regular file: {path}")
        if path.suffix.lower() == LEGACY_MACHINE_SUFFIX:
            raise InstallError(f"skill source contains a non-TOON machine artifact: {path}")
        files.append(path)
    return files


def directory_digest(directory: Path) -> str:
    """Hash relative paths, sizes, and bytes in stable lexical order."""
    if directory.is_symlink():
        raise InstallError(f"managed skill root must not be a symbolic link: {directory}")
    if not directory.is_dir():
        raise InstallError(f"managed skill root is not a directory: {directory}")
    digest = hashlib.sha256()
    for path in regular_files(directory):
        relative = path.relative_to(directory).as_posix().encode("utf-8")
        payload = path.read_bytes()
        mode = path.stat().st_mode & 0o777
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(mode.to_bytes(4, "big"))
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def _write_stage(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _restore_path(destination: Path, backup: Path | None) -> None:
    if destination.is_dir():
        shutil.rmtree(destination)
    elif destination.exists() or destination.is_symlink():
        destination.unlink()
    if backup is not None and backup.exists():
        os.replace(backup, destination)


def validate_managed_directory(root: Path, path: Path) -> None:
    """Validate one repository-contained directory without following a link."""
    if path.is_symlink():
        raise InstallError(f"managed directory must not be a symbolic link: {path}")
    if path.exists() and not path.is_dir():
        raise InstallError(f"managed path is not a directory: {path}")
    if path.exists():
        try:
            path.resolve().relative_to(root)
        except ValueError as exc:
            raise InstallError(f"managed directory escapes the consumer repository: {path}") from exc


def ensure_managed_directory(root: Path, path: Path) -> None:
    """Create a validated managed directory."""
    validate_managed_directory(root, path)
    path.mkdir(parents=True, exist_ok=True)


@contextmanager
def consumer_mutation_lock(root: Path) -> Iterator[None]:
    """Serialize installer mutations through repository-owned Git metadata."""
    top_level = _run_git(root, "rev-parse", "--show-toplevel")
    if top_level.returncode:
        raise InstallError("consumer root must be a Git repository")
    if Path(top_level.stdout.strip()).resolve() != root.resolve():
        raise InstallError("run the installer from the consumer repository root")
    lock_result = _run_git(root, "rev-parse", "--git-path", "ai-sdlc-install.lock")
    if lock_result.returncode:
        raise InstallError(f"cannot resolve consumer mutation lock: {lock_result.stderr.strip()}")
    lock_path = Path(lock_result.stdout.strip())
    if not lock_path.is_absolute():
        lock_path = root / lock_path
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+b")
    try:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise InstallError("another Harness installation is already mutating this repository") from exc
        yield
    finally:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()


def _install_locked(
    *,
    source: Path,
    root: Path,
    revision: str,
    agent: str,
    requested: list[str],
    replace_reviewed: bool,
) -> tuple[int, Path, Path]:
    """Stage, verify, and transactionally apply one project-scoped installation."""
    source = source.resolve()
    root = root.resolve()
    if not source.is_dir():
        raise InstallError(f"source directory does not exist: {source}")
    if not root.is_dir():
        raise InstallError(f"consumer repository directory does not exist: {root}")
    if not REVISION_RE.fullmatch(revision):
        raise InstallError("revision must be an exact lowercase 40-character Git SHA")
    if agent != "codex":
        raise InstallError("the v4 native installer currently validates project scope only for agent codex")
    legacy_lock = root / ("skills-lock" + LEGACY_MACHINE_SUFFIX)
    if legacy_lock.exists() or legacy_lock.is_symlink():
        raise InstallError(
            "legacy installer lock exists at the repository root; review and remove "
            "that installer-owned file before the TOON-only install"
        )
    verify_source_identity(source, revision)
    published = read_inventory(source)
    names, selection = selected_inventory(published, requested)

    source_digests: dict[str, str] = {}
    for name in names:
        source_digests[name] = directory_digest(source / "skills" / name)

    agents_root = root / ".agents"
    skills_root = agents_root / "skills"
    metadata_root = root / ".ai-sdlc"
    validate_managed_directory(root, agents_root)
    validate_managed_directory(root, skills_root)
    validate_managed_directory(root, metadata_root)
    for metadata_name in (
        "harness-managed-skills.txt",
        "harness-install.toon",
        "harness-install-lock.toon",
    ):
        metadata_path = metadata_root / metadata_name
        if metadata_path.is_symlink():
            raise InstallError(f"managed metadata must not be a symbolic link: {metadata_path}")

    changed: list[str] = []
    for name in names:
        destination = skills_root / name
        if destination.is_symlink():
            raise InstallError(f"managed destination must not be a symbolic link: {destination}")
        if not destination.exists():
            changed.append(name)
            continue
        if not destination.is_dir() or destination.is_symlink():
            raise InstallError(f"managed destination is not a regular directory: {destination}")
        if directory_digest(destination) != source_digests[name]:
            if not replace_reviewed:
                raise InstallError(
                    f"managed destination differs: {destination}; review it before --replace-reviewed"
                )
            changed.append(name)

    ensure_managed_directory(root, agents_root)
    ensure_managed_directory(root, skills_root)
    ensure_managed_directory(root, metadata_root)
    stage_root = Path(tempfile.mkdtemp(prefix=".ai-sdlc-install-", dir=agents_root))
    staged_skills = stage_root / "skills"
    backup_skills = stage_root / "backup-skills"
    staged_metadata = stage_root / "metadata"
    backup_metadata = stage_root / "backup-metadata"
    applied_skills: list[tuple[Path, Path | None]] = []
    applied_metadata: list[tuple[Path, Path | None]] = []
    try:
        for name in changed:
            staged = staged_skills / name
            shutil.copytree(source / "skills" / name, staged)
            if directory_digest(staged) != source_digests[name]:
                raise InstallError(f"staged skill digest mismatch: {name}")

        inventory_path = metadata_root / "harness-managed-skills.txt"
        record_path = metadata_root / "harness-install.toon"
        lock_path = metadata_root / "harness-install-lock.toon"
        lock = {
            "agent": agent,
            "installer": INSTALLER_ID,
            "revision": revision,
            "schema": LOCK_SCHEMA,
            "selection": selection,
            "skills": [
                {
                    "name": name,
                    "path": f".agents/skills/{name}",
                    "sha256": source_digests[name],
                }
                for name in names
            ],
            "target": ".agents/skills",
        }
        record = {
            "agent": agent,
            "installer": INSTALLER_ID,
            "inventory": ".ai-sdlc/harness-managed-skills.txt",
            "lock": ".ai-sdlc/harness-install-lock.toon",
            "revision": revision,
            "schema": RECORD_SCHEMA,
            "selection": selection,
            "target": ".agents/skills",
        }
        _write_stage(staged_metadata / inventory_path.name, "".join(f"{name}\n" for name in names))
        _write_stage(staged_metadata / record_path.name, toon_codec.dumps(record))
        _write_stage(staged_metadata / lock_path.name, toon_codec.dumps(lock))

        for name in changed:
            destination = skills_root / name
            backup: Path | None = None
            if destination.exists():
                backup = backup_skills / name
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, backup)
            applied_skills.append((destination, backup))
            os.replace(staged_skills / name, destination)

        for destination in (inventory_path, record_path, lock_path):
            backup = None
            if destination.exists():
                backup = backup_metadata / destination.name
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, backup)
            applied_metadata.append((destination, backup))
            os.replace(staged_metadata / destination.name, destination)
    except Exception:
        for destination, backup in reversed(applied_metadata):
            _restore_path(destination, backup)
        for destination, backup in reversed(applied_skills):
            _restore_path(destination, backup)
        raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)

    return len(names), record_path, lock_path


def install(
    *,
    source: Path,
    root: Path,
    revision: str,
    agent: str,
    requested: list[str],
    replace_reviewed: bool,
) -> tuple[int, Path, Path]:
    """Serialize, stage, verify, and apply one project-scoped installation."""
    resolved_root = root.resolve()
    with consumer_mutation_lock(resolved_root):
        return _install_locked(
            source=source,
            root=resolved_root,
            revision=revision,
            agent=agent,
            requested=requested,
            replace_reviewed=replace_reviewed,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--revision", required=True)
    parser.add_argument("--agent", default="codex")
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--replace-reviewed", action="store_true")
    args = parser.parse_args()
    try:
        count, record, lock = install(
            source=args.source,
            root=args.root,
            revision=args.revision,
            agent=args.agent,
            requested=args.skill,
            replace_reviewed=args.replace_reviewed,
        )
    except (InstallError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Installed {count} AI SDLC Harness skills into .agents/skills")
    print(f"Install record: {record.relative_to(args.root.resolve())}")
    print(f"Deterministic lock: {lock.relative_to(args.root.resolve())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
