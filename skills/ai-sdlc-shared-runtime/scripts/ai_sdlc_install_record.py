#!/usr/bin/env python3
"""Validate a portable harness install record and its managed inventory."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parent
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402
from ai_sdlc_install import (  # noqa: E402
    INSTALLER_ID,
    LOCK_SCHEMA,
    RECORD_SCHEMA,
    INSTALL_PROFILES,
    InstallError,
    directory_digest,
)


REQUIRED = {
    "schema",
    "revision",
    "installer",
    "agent",
    "profile",
    "selection",
    "inventory",
    "lock",
    "target",
}
LOCK_REQUIRED = {"schema", "revision", "installer", "agent", "profile", "selection", "skills", "target"}
LOCK_ENTRY_REQUIRED = {"name", "path", "sha256"}
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def published_inventory() -> list[str]:
    """Read the packaged full-skill inventory in source or installed layouts."""
    script = Path(__file__).resolve()
    candidates = (
        script.parents[1] / "references" / "ai-sdlc-managed-skills.txt",
        script.parents[2] / "config" / "ai-sdlc-managed-skills.txt",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8").splitlines()
    return []


def validate(record_path: Path, skills_root: Path) -> list[str]:
    try:
        value = toon_codec.loads(record_path.read_text(encoding="utf-8-sig"))
    except (OSError, toon_codec.ToonDecodeError) as exc:
        return [f"cannot read install record: {exc}"]
    if not isinstance(value, dict) or set(value) != REQUIRED:
        return [
            "install record must contain exactly schema, revision, installer, "
            "agent, profile, selection, inventory, lock, target"
        ]
    errors: list[str] = []
    if value["schema"] != RECORD_SCHEMA:
        errors.append(f"install record schema must be {RECORD_SCHEMA}")
    if not isinstance(value["revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", value["revision"]):
        errors.append("install record revision must be a lowercase 40-character Git SHA")
    if value["installer"] != INSTALLER_ID:
        errors.append(f"install record installer must be {INSTALLER_ID}")
    profile = value["profile"]
    if profile not in INSTALL_PROFILES:
        errors.append("install record profile is unknown")
        return errors
    profile_contract = INSTALL_PROFILES[profile]
    if value["agent"] != profile_contract["agent"]:
        errors.append("install record agent must match its profile")
    if value["selection"] not in {"all-skills", "explicit-skills"}:
        errors.append("install record selection is invalid")
    if value["inventory"] != ".ai-sdlc/harness-managed-skills.txt":
        errors.append("install record inventory must be .ai-sdlc/harness-managed-skills.txt")
        return errors
    if value["lock"] != ".ai-sdlc/harness-install-lock.toon":
        errors.append("install record lock must be .ai-sdlc/harness-install-lock.toon")
        return errors
    if value["target"] != profile_contract["target"]:
        errors.append("install record target must match its profile")
        return errors
    inventory_path = record_path.resolve().parent.parent / value["inventory"]
    try:
        names = inventory_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"cannot read managed inventory: {exc}")
        return errors
    if names != sorted(set(names)) or not names:
        errors.append("managed inventory must contain unique sorted skill names")
    if any(not SKILL_NAME_RE.fullmatch(name) for name in names):
        errors.append("managed inventory contains an invalid skill name")
    published = published_inventory()
    if not published:
        errors.append("packaged full-skill inventory is missing")
    elif value["selection"] == "all-skills" and names != published:
        errors.append("all-skills inventory must exactly match the packaged full-skill inventory")
    elif value["selection"] == "explicit-skills":
        unknown = sorted(set(names) - set(published))
        if unknown:
            errors.append(f"explicit-skills inventory contains unpublished skills: {', '.join(unknown)}")
        if "ai-sdlc-shared-runtime" not in names:
            errors.append("explicit-skills inventory must include ai-sdlc-shared-runtime")
    installed = sorted(path.name for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    missing = sorted(set(names) - set(installed))
    if missing:
        errors.append(f"managed skills are not installed: {', '.join(missing)}")
        return errors

    lock_path = record_path.resolve().parent.parent / value["lock"]
    try:
        lock = toon_codec.loads(lock_path.read_text(encoding="utf-8-sig"))
    except (OSError, toon_codec.ToonDecodeError) as exc:
        errors.append(f"cannot read deterministic install lock: {exc}")
        return errors
    if not isinstance(lock, dict) or set(lock) != LOCK_REQUIRED:
        errors.append(
            "install lock must contain exactly schema, revision, installer, "
            "agent, profile, selection, skills, target"
        )
        return errors
    for field in ("revision", "installer", "agent", "profile", "selection", "target"):
        if lock[field] != value[field]:
            errors.append(f"install lock {field} must match the install record")
    if lock["schema"] != LOCK_SCHEMA:
        errors.append(f"install lock schema must be {LOCK_SCHEMA}")
    entries = lock["skills"]
    if not isinstance(entries, list):
        errors.append("install lock skills must be a list")
        return errors
    locked_names: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != LOCK_ENTRY_REQUIRED:
            errors.append("every install lock entry must contain exactly name, path, sha256")
            return errors
        name = entry["name"]
        if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
            errors.append("install lock contains an invalid skill name")
            continue
        locked_names.append(name)
        if entry["path"] != f"{value['target']}/{name}":
            errors.append(f"install lock path is invalid for {name}")
        if not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            errors.append(f"install lock digest is invalid for {name}")
            continue
        try:
            actual_digest = directory_digest(skills_root / name)
        except (InstallError, OSError) as exc:
            errors.append(f"cannot hash installed skill {name}: {exc}")
            continue
        if actual_digest != entry["sha256"]:
            errors.append(f"installed skill digest differs for {name}")
    if locked_names != names:
        errors.append("install lock skill names must exactly match the managed inventory")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, default=Path(".ai-sdlc/harness-install.toon"))
    parser.add_argument("--skills-root", type=Path)
    args = parser.parse_args()
    if args.skills_root is None:
        try:
            record = toon_codec.loads(args.record.read_text(encoding="utf-8-sig"))
            args.skills_root = args.record.resolve().parent.parent / record["target"]
        except (OSError, KeyError, TypeError, toon_codec.ToonDecodeError):
            args.skills_root = Path(".agents/skills")
    errors = validate(args.record, args.skills_root)
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print(f"Harness install record valid: {args.record}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
