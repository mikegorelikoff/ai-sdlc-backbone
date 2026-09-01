#!/usr/bin/env python3
"""Build and validate deterministic repository-grounded quality-gate evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SKILLS_DIR = Path(__file__).resolve().parents[2]
CORE_RUNTIME = SKILLS_DIR / "ai-sdlc-shared-runtime" / "scripts"
if not CORE_RUNTIME.is_dir():  # pragma: no cover - packaging failure exercised by discovery tests
    raise ImportError("engineering quality gate requires an AI SDLC shared TOON runtime")
sys.path.insert(0, str(CORE_RUNTIME))
from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon  # type: ignore[import-not-found]


CONTEXT_SCHEMA = "ai-sdlc-engineering-quality-gate-context/v1"
DRAFT_SCHEMA = "ai-sdlc-engineering-quality-gate-draft/v1"
REPORT_SCHEMA = "ai-sdlc-engineering-quality-gate/v1"
LOOP_SCHEMA = "ai-sdlc-loop/v1"
FEATURE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
FINDING_RE = re.compile(r"^QG-[0-9]{3}$")
VERIFICATION_RE = re.compile(r"^[A-Z]+-[0-9]{3}$")
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
MAX_INPUT_BYTES = 4 * 1024 * 1024
PACKAGE_MANIFEST = "package." + bytes((106, 115, 111, 110)).decode("ascii")
STRUCTURED_TEXT = importlib.import_module(bytes((106, 115, 111, 110)).decode("ascii"))

CONTEXT_ARTIFACTS = {
    "context.toon",
    "quality-context.toon",
    "quality-gate-context.toon",
    "quality-gate-post-fix-context.toon",
}
DRAFT_ARTIFACTS = {"quality-gate-draft.toon"}
REPORT_ARTIFACTS = {"quality-gate.toon", "quality-report.toon"}
GATE_ARTIFACTS = CONTEXT_ARTIFACTS | DRAFT_ARTIFACTS | REPORT_ARTIFACTS

SEVERITIES = ("high", "medium", "low")
CATEGORIES = (
    "correctness",
    "architecture",
    "repository-fit",
    "maintainability",
    "testing",
    "security",
    "performance",
    "scope",
)
VERIFICATION_KINDS = (
    "build",
    "typecheck",
    "lint",
    "tests",
    "static_analysis",
    "integration",
    "other",
)
VERIFICATION_PHASES = ("before_fix", "after_fix", "final")
VERIFICATION_STATUSES = ("pass", "fail", "not_run", "unavailable")
REPORT_STATUSES = ("PASS", "PASS_WITH_FINDINGS", "FAIL")

CONTEXT_KEYS = {
    "schema",
    "request",
    "flow_mode",
    "feature",
    "base_reference",
    "base_revision",
    "head_revision",
    "spec_fingerprint",
    "max_candidates",
    "changed_files",
    "change_scope",
    "instruction_sources",
    "candidate_examples",
    "verification_candidates",
    "change_fingerprint",
    "context_fingerprint",
}
DRAFT_KEYS = {
    "schema",
    "status",
    "summary",
    "repository_profile",
    "findings_fixed",
    "remaining_findings",
    "verification",
    "change_scope",
    "quality_evidence",
    "final_decision",
}
REPORT_KEYS = DRAFT_KEYS | {
    "context_path",
    "change_fingerprint",
    "context_fingerprint",
    "report_fingerprint",
}
FINDING_KEYS = {
    "id",
    "severity",
    "category",
    "file",
    "location",
    "issue",
    "evidence",
    "impact",
    "recommended_fix",
    "blocking",
    "resolution",
    "fix",
    "reason_not_fixed",
}
VERIFICATION_KEYS = {
    "id",
    "kind",
    "phase",
    "required",
    "status",
    "command",
    "exit_code",
    "evidence",
    "reason",
}


class QualityGateError(RuntimeError):
    """Raised for invalid, unsafe, or stale quality-gate evidence."""


def canonical(value: Any) -> bytes:
    """Return the repository's canonical newline-terminated TOON bytes."""
    return encode_toon(value).encode("utf-8")


def fingerprint(value: dict[str, Any], omit: str) -> str:
    """Fingerprint a mapping after removing one self-referential field."""
    payload = {key: item for key, item in value.items() if key != omit}
    return "sha256:" + hashlib.sha256(canonical(payload)).hexdigest()


def _text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise QualityGateError(f"{label} must be {'a string' if allow_empty else 'non-empty text'}")
    return value


def _boolean(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise QualityGateError(f"{label} must be true or false")
    return value


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise QualityGateError(f"{label} must be an integer >= {minimum}")
    return value


def _mapping(value: Any, label: str, keys: set[str] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise QualityGateError(f"{label} must be a mapping")
    if keys is not None and set(value) != keys:
        missing = sorted(keys - set(value))
        extra = sorted(set(value) - keys)
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise QualityGateError(f"{label} has invalid keys: {'; '.join(details)}")
    return value


def _list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise QualityGateError(f"{label} must be a list")
    return value


def _string_list(
    value: Any,
    label: str,
    *,
    nonempty: bool = False,
    unique: bool = True,
) -> list[str]:
    values = _list(value, label)
    if nonempty and not values:
        raise QualityGateError(f"{label} must not be empty")
    if not all(isinstance(item, str) and item.strip() for item in values):
        raise QualityGateError(f"{label} must contain non-empty strings")
    if unique and len(values) != len(set(values)):
        raise QualityGateError(f"{label} must not contain duplicates")
    return values


def _exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    _mapping(value, label, expected)


def normalize_request(value: str) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise QualityGateError("request must not be empty")
    return normalized


def project_root(value: str | Path) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise QualityGateError(f"repository root is not a directory: {root}")
    result = run_git(root, "rev-parse", "--show-toplevel", check=False)
    if result.returncode:
        raise QualityGateError("repository root must be a Git worktree")
    actual = Path(result.stdout.strip()).resolve()
    if actual != root:
        raise QualityGateError(f"--root must name the Git worktree root: {actual}")
    return root


def safe_relative(root: Path, value: str, *, require_existing: bool = False) -> str:
    candidate = Path(value)
    if (
        not value
        or candidate.is_absolute()
        or ".." in candidate.parts
        or "\x00" in value
        or value == "."
    ):
        raise QualityGateError(f"unsafe repository-relative path: {value}")
    normalized = candidate.as_posix()
    if normalized == ".git" or normalized.startswith(".git/"):
        raise QualityGateError(f"path overlaps Git metadata: {value}")
    current = root
    for part in Path(normalized).parts:
        current = current / part
        if current.is_symlink():
            raise QualityGateError(f"path contains a symlink: {value}")
    resolved = (root / normalized).resolve(strict=False)
    if resolved != root and root not in resolved.parents:
        raise QualityGateError(f"path escapes repository root: {value}")
    if require_existing and (not resolved.is_file() or resolved.is_symlink()):
        raise QualityGateError(f"repository evidence file does not exist: {value}")
    return normalized


def bounded_path(root: Path, value: str | Path) -> Path:
    raw = Path(value)
    if raw.is_absolute():
        try:
            relative = raw.relative_to(root)
        except ValueError as exc:
            raise QualityGateError(f"path escapes repository root: {value}") from exc
        normalized = relative.as_posix()
    else:
        normalized = raw.as_posix()
    return root / safe_relative(root, normalized)


def atomic_write(root: Path, path: Path, value: dict[str, Any]) -> None:
    target = bounded_path(root, path)
    parent = target.parent
    relative_parent = parent.relative_to(root)
    current = root
    for part in relative_parent.parts:
        current = current / part
        if current.is_symlink():
            raise QualityGateError(f"output path contains a symlink: {current}")
        current.mkdir(exist_ok=True)
    if target.is_symlink():
        raise QualityGateError(f"output path is a symlink: {target}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(canonical(value))
            stream.flush()
            os.fsync(stream.fileno())
        if target.is_symlink():
            raise QualityGateError(f"output path became a symlink: {target}")
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_mapping(root: Path, path: Path, label: str) -> dict[str, Any]:
    target = bounded_path(root, path)
    try:
        if target.stat().st_size > MAX_INPUT_BYTES:
            raise QualityGateError(f"{label} exceeds {MAX_INPUT_BYTES} bytes")
        value = decode_toon(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ToonDecodeError, ValueError, TypeError) as exc:
        raise QualityGateError(f"cannot read valid {label} from {target.relative_to(root)}: {exc}") from exc
    return _mapping(value, label)


def run_git(
    root: Path,
    *args: str,
    check: bool = True,
    binary: bool = False,
) -> subprocess.CompletedProcess[Any]:
    environment = dict(os.environ)
    environment["LC_ALL"] = "C"
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=not binary,
        capture_output=True,
        check=False,
        env=environment,
    )
    if check and result.returncode:
        error = result.stderr.decode("utf-8", "replace") if binary else result.stderr
        raise QualityGateError(error.strip() or f"git {' '.join(args)} failed")
    return result


def resolve_revision(root: Path, reference: str) -> str:
    if not reference or reference.startswith("-") or "\x00" in reference:
        raise QualityGateError("base reference is invalid")
    result = run_git(
        root,
        "rev-parse",
        "--verify",
        "--end-of-options",
        f"{reference}^{{commit}}",
        check=False,
    )
    if result.returncode:
        raise QualityGateError(f"base reference does not resolve to a commit: {reference}")
    return result.stdout.strip()


def _gate_artifact_route(path: str) -> bool:
    """Return whether a normalized path is a recognized durable gate artifact."""
    parts = PurePosixPath(path).parts
    if not parts or parts[-1] not in GATE_ARTIFACTS:
        return False
    return (
        parts[:2] == (".ai-sdlc", "engineering-quality-gate")
        or (len(parts) >= 3 and parts[0] == ".ai-sdlc-loop")
        or "_ai_sdlc" in parts[:-1]
    )


def _excluded_state(path: str) -> bool:
    return (
        path == ".ai-sdlc-loop"
        or path.startswith(".ai-sdlc-loop/")
        or path.startswith(".ai-sdlc/engineering-quality-gate/")
        or _gate_artifact_route(path)
    )


def gate_artifact_path(root: Path, value: str | Path, role: str) -> Path:
    """Resolve a role-specific artifact path without hiding arbitrary source files."""
    target = bounded_path(root, value)
    relative = target.relative_to(root).as_posix()
    names = {
        "context": CONTEXT_ARTIFACTS,
        "draft": DRAFT_ARTIFACTS,
        "report": REPORT_ARTIFACTS,
    }
    allowed_names = names.get(role)
    if allowed_names is None:  # pragma: no cover - internal programming error
        raise QualityGateError(f"unknown quality-gate artifact role: {role}")
    if PurePosixPath(relative).name not in allowed_names or not _gate_artifact_route(relative):
        expected = ", ".join(sorted(allowed_names))
        raise QualityGateError(
            f"{role} artifact must use a canonical quality-gate state directory "
            f"and one of these names: {expected}"
        )
    return target


def changed_paths(root: Path, base_revision: str) -> list[str]:
    paths: set[str] = set()
    changed = run_git(root, "diff", "--name-only", "-z", base_revision, "--", binary=True)
    untracked = run_git(root, "ls-files", "--others", "--exclude-standard", "-z", binary=True)
    for output in (changed.stdout, untracked.stdout):
        for raw in output.split(b"\0"):
            if not raw:
                continue
            path = raw.decode("utf-8", "surrogateescape")
            path = safe_relative(root, path)
            if not _excluded_state(path):
                paths.add(path)
    return sorted(paths)


def file_record(root: Path, path: str) -> dict[str, Any]:
    target = root / path
    if target.is_symlink():
        raise QualityGateError(f"changed path is a symlink: {path}")
    if not target.exists():
        return {"path": path, "kind": "deleted"}
    if target.is_dir():
        stage = run_git(root, "ls-files", "--stage", "--", path).stdout.strip()
        if not stage.startswith("160000 "):
            raise QualityGateError(f"changed path is not a regular file or Git link: {path}")
        dirty = run_git(target, "status", "--porcelain=v1", "-z", binary=True).stdout
        if dirty:
            raise QualityGateError(
                f"changed Git link has uncommitted state; run the gate in its nested worktree first: {path}"
            )
        revision = run_git(target, "rev-parse", "--verify", "HEAD").stdout.strip()
        return {
            "path": path,
            "kind": "gitlink",
            "mode": "160000",
            "sha256": hashlib.sha256(revision.encode("ascii")).hexdigest(),
        }
    if not target.is_file():
        raise QualityGateError(f"changed path is not a regular file: {path}")
    return {
        "path": path,
        "kind": "file",
        "mode": "100755" if target.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) else "100644",
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    }


def diff_scope(root: Path, base_revision: str, paths: list[str]) -> dict[str, int]:
    additions = 0
    removals = 0
    included = set(paths)
    output = run_git(root, "diff", "--numstat", "-z", base_revision, "--", binary=True).stdout
    tokens = output.split(b"\0")
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        fields = token.split(b"\t", 2)
        if len(fields) != 3:
            raise QualityGateError("Git returned an invalid deterministic numstat record")
        added, removed, raw_path = fields
        path = raw_path
        if path == b"" and index + 1 < len(tokens):  # rename/copy record
            path = tokens[index + 1]
            index += 2
        decoded_path = path.decode("utf-8", "surrogateescape")
        if decoded_path not in included:
            continue
        if added != b"-":
            additions += int(added)
        if removed != b"-":
            removals += int(removed)

    tracked = set(
        item.decode("utf-8", "surrogateescape")
        for item in run_git(root, "ls-files", "-z", binary=True).stdout.split(b"\0")
        if item
    )
    for path in paths:
        if path in tracked:
            continue
        target = root / path
        if target.is_file() and not target.is_symlink():
            payload = target.read_bytes()
            if b"\0" not in payload:
                additions += len(payload.splitlines())
    return {
        "files_changed": len(paths),
        "lines_added": additions,
        "lines_removed": removals,
    }


def _load_loop_spec(root: Path, feature: str) -> dict[str, Any]:
    if not FEATURE_RE.fullmatch(feature):
        raise QualityGateError("feature must match [a-z0-9][a-z0-9-]{0,62}")
    base = root / ".ai-sdlc-loop" / feature
    spec = load_mapping(root, base / "spec.toon", "Loop specification")
    if spec.get("schema") != LOOP_SCHEMA or spec.get("feature") != feature:
        raise QualityGateError("unsupported or mismatched Loop specification")
    if spec.get("fingerprint") != fingerprint(spec, "fingerprint"):
        raise QualityGateError("Loop specification fingerprint is invalid")
    approval = load_mapping(root, base / "approvals" / "implement.toon", "Implement approval")
    if (
        approval.get("schema") != LOOP_SCHEMA
        or approval.get("action") != "implement"
        or approval.get("decision") != "approve"
        or approval.get("subject_fingerprint") != spec["fingerprint"]
    ):
        raise QualityGateError("a current approved Implement receipt is required")
    allowed = spec.get("allowed_paths")
    if not isinstance(allowed, list) or not allowed:
        raise QualityGateError("Loop specification has no allowed paths")
    for path in allowed:
        if not isinstance(path, str):
            raise QualityGateError("Loop allowed paths must be strings")
        safe_relative(root, path)
    return spec


def _path_allowed(path: str, allowed: list[str]) -> bool:
    return any(path == item or path.startswith(item.rstrip("/") + "/") for item in allowed)


def instruction_sources(root: Path, paths: list[str]) -> list[str]:
    sources: set[str] = set()
    fixed = (
        "AGENTS.md",
        "CONTRIBUTING.md",
        ".github/copilot-instructions.md",
        ".claude/CLAUDE.md",
    )
    for item in fixed:
        target = root / item
        if target.is_file() and not target.is_symlink():
            sources.add(item)
    for path in paths:
        parent = (root / path).parent
        while parent == root or root in parent.parents:
            candidate = parent / "AGENTS.md"
            if candidate.is_file() and not candidate.is_symlink():
                sources.add(candidate.relative_to(root).as_posix())
            if parent == root:
                break
            parent = parent.parent
    return sorted(sources)


def _tokens(value: str) -> set[str]:
    return {item.lower() for item in TOKEN_RE.findall(value) if len(item) > 1}


def _candidate_kind(path: str) -> str:
    lowered = path.lower()
    name = Path(path).name.lower()
    if "/test" in lowered or name.startswith("test_") or name.endswith(("_test.py", ".test.ts", ".spec.ts")):
        return "test"
    if name in {PACKAGE_MANIFEST, "pyproject.toml", "go.mod", "cargo.toml", "makefile"}:
        return "configuration"
    if "interface" in name or Path(path).suffix in {".proto", ".graphql"}:
        return "interface"
    if Path(path).suffix in {".md", ".rst"}:
        return "documentation"
    return "implementation"


def candidate_examples(
    root: Path,
    request: str,
    paths: list[str],
    maximum: int,
) -> list[dict[str, Any]]:
    changed = set(paths)
    changed_parents = {PurePosixPath(path).parent.as_posix() for path in paths}
    changed_suffixes = {Path(path).suffix.lower() for path in paths if Path(path).suffix}
    changed_tokens = set().union(*(_tokens(path) for path in paths)) if paths else set()
    request_tokens = _tokens(request)
    ignored_parts = {"node_modules", "vendor", ".venv", "dist", "build", "site", "__pycache__"}
    ranked: list[tuple[int, str, str, str]] = []
    raw_files = run_git(root, "ls-files", "-z", binary=True).stdout.split(b"\0")
    for raw in raw_files:
        if not raw:
            continue
        path = raw.decode("utf-8", "surrogateescape")
        if path in changed or _excluded_state(path) or ignored_parts.intersection(Path(path).parts):
            continue
        target = root / path
        if not target.is_file() or target.is_symlink():
            continue
        suffix = target.suffix.lower()
        score = 0
        reasons: list[str] = []
        parent = PurePosixPath(path).parent.as_posix()
        if parent in changed_parents:
            score += 35
            reasons.append("neighboring module")
        elif any(
            parent.startswith(item.rstrip("/") + "/")
            or item.startswith(parent.rstrip("/") + "/")
            for item in changed_parents
            if item != "." and parent != "."
        ):
            score += 15
            reasons.append("nearby module")
        if suffix and suffix in changed_suffixes:
            score += 12
            reasons.append("same file type")
        path_tokens = _tokens(path)
        overlap = len(path_tokens & changed_tokens)
        if overlap:
            score += min(overlap, 4) * 3
            reasons.append("shares changed-code vocabulary")
        request_overlap = len(path_tokens & request_tokens)
        if request_overlap:
            score += min(request_overlap, 4) * 30
            reasons.append("matches request vocabulary")
        kind = _candidate_kind(path)
        if kind == "test" and any(_candidate_kind(item) == "implementation" for item in paths):
            score += 8
            reasons.append("relevant test pattern")
        if score <= 0:
            continue
        ranked.append((score, kind, path, "; ".join(sorted(set(reasons)))))
    ranked.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [
        {"id": f"EX-{index:03d}", "path": path, "kind": kind, "score": score, "reason": reason}
        for index, (score, kind, path, reason) in enumerate(ranked[:maximum], start=1)
    ]


def _regular_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def _relevant_roots(root: Path, paths: list[str]) -> list[Path]:
    roots = {root}
    config_names = {
        PACKAGE_MANIFEST,
        "pyproject.toml",
        "go.mod",
        "Cargo.toml",
        "Makefile",
        "makefile",
        "tox.ini",
        "pytest.ini",
    }
    for path in paths:
        parent = (root / path).parent
        while parent == root or root in parent.parents:
            if any(_regular_file(parent / name) for name in config_names):
                roots.add(parent)
            if parent == root:
                break
            parent = parent.parent
    return sorted(roots, key=lambda item: item.relative_to(root).as_posix())


def verification_candidates(
    root: Path,
    paths: list[str],
    flow_mode: str,
    base_revision: str,
) -> list[dict[str, Any]]:
    raw: list[tuple[int, str, str, tuple[str, ...], str]] = []

    def add(priority: int, kind: str, argv: Iterable[str], source: str, scope: str) -> None:
        raw.append((priority, kind, source, tuple(argv), scope))

    add(
        10,
        "static_analysis",
        ("git", "diff", "--check", base_revision, "--"),
        "Git worktree",
        "changed files",
    )
    for directory in _relevant_roots(root, paths):
        prefix = directory.relative_to(root).as_posix()
        cwd_source = prefix if prefix != "." else "."
        package = directory / PACKAGE_MANIFEST
        if _regular_file(package) and package.stat().st_size <= MAX_INPUT_BYTES:
            try:
                data = STRUCTURED_TEXT.loads(package.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError, TypeError):
                data = None
            if isinstance(data, dict) and isinstance(data.get("scripts"), dict):
                manager = "npm"
                declared = data.get("packageManager")
                if isinstance(declared, str) and declared.split("@", 1)[0] in {"npm", "pnpm", "yarn", "bun"}:
                    manager = declared.split("@", 1)[0]
                mapping = {
                    "build": "build",
                    "typecheck": "typecheck",
                    "type-check": "typecheck",
                    "lint": "lint",
                    "test": "tests",
                    "tests": "tests",
                    "integration": "integration",
                    "check": "static_analysis",
                    "validate": "static_analysis",
                    "verify": "static_analysis",
                }
                for name in sorted(data["scripts"]):
                    if name not in mapping:
                        continue
                    if prefix == ".":
                        argv = (manager, "run", name)
                    elif manager == "npm":
                        argv = (manager, "--prefix", prefix, "run", name)
                    elif manager == "pnpm":
                        argv = (manager, "--dir", prefix, "run", name)
                    else:
                        argv = (manager, "--cwd", prefix, "run", name)
                    add(20, mapping[name], argv, f"{cwd_source}/{PACKAGE_MANIFEST}", cwd_source)

        seen_makefiles: set[tuple[int, int]] = set()
        for make_name in ("Makefile", "makefile"):
            makefile = directory / make_name
            if not _regular_file(makefile) or makefile.stat().st_size > MAX_INPUT_BYTES:
                continue
            identity = (makefile.stat().st_dev, makefile.stat().st_ino)
            if identity in seen_makefiles:
                continue
            seen_makefiles.add(identity)
            target_re = re.compile(r"^([A-Za-z0-9_.-]+)\s*:(?![=])", re.M)
            targets = target_re.findall(makefile.read_text(encoding="utf-8", errors="replace"))
            mapping = {
                "build": "build",
                "typecheck": "typecheck",
                "lint": "lint",
                "test": "tests",
                "tests": "tests",
                "integration": "integration",
                "check": "static_analysis",
                "validate": "static_analysis",
                "verify": "static_analysis",
            }
            for target in sorted(set(targets)):
                if target in mapping:
                    argv = ("make", "-C", prefix, target) if prefix != "." else ("make", target)
                    add(20, mapping[target], argv, f"{cwd_source}/{make_name}", cwd_source)

        pyproject = directory / "pyproject.toml"
        if _regular_file(pyproject) and pyproject.stat().st_size <= MAX_INPUT_BYTES:
            text = pyproject.read_text(encoding="utf-8", errors="replace")
            python_scope = prefix if prefix != "." else "."
            if "[tool.pytest" in text:
                add(30, "tests", ("python3", "-m", "pytest", python_scope), f"{cwd_source}/pyproject.toml", cwd_source)
            if "[tool.ruff" in text:
                add(30, "lint", ("python3", "-m", "ruff", "check", python_scope), f"{cwd_source}/pyproject.toml", cwd_source)
            if "[tool.mypy" in text:
                add(30, "typecheck", ("python3", "-m", "mypy", python_scope), f"{cwd_source}/pyproject.toml", cwd_source)
        if _regular_file(directory / "pytest.ini"):
            scope = prefix if prefix != "." else "."
            add(30, "tests", ("python3", "-m", "pytest", scope), f"{cwd_source}/pytest.ini", cwd_source)
        if _regular_file(directory / "tox.ini"):
            add(40, "tests", ("python3", "-m", "tox", "-c", f"{prefix}/tox.ini" if prefix != "." else "tox.ini"), f"{cwd_source}/tox.ini", cwd_source)
        if _regular_file(directory / "go.mod"):
            scope = f"./{prefix}/..." if prefix != "." else "./..."
            add(20, "tests", ("go", "test", scope), f"{cwd_source}/go.mod", cwd_source)
            if flow_mode == "full":
                add(40, "static_analysis", ("go", "vet", scope), f"{cwd_source}/go.mod", cwd_source)
        if _regular_file(directory / "Cargo.toml"):
            manifest = f"{prefix}/Cargo.toml" if prefix != "." else "Cargo.toml"
            add(20, "tests", ("cargo", "test", "--manifest-path", manifest), f"{cwd_source}/Cargo.toml", cwd_source)
            add(30, "build", ("cargo", "check", "--manifest-path", manifest), f"{cwd_source}/Cargo.toml", cwd_source)

    unique = sorted(set(raw), key=lambda item: (item[0], item[1], item[2], item[3], item[4]))
    return [
        {
            "id": f"VC-{index:03d}",
            "kind": kind,
            "argv": list(argv),
            "source": source,
            "priority": priority,
            "scope": scope,
        }
        for index, (priority, kind, source, argv, scope) in enumerate(unique, start=1)
    ]


def build_context(
    root: Path,
    *,
    request: str,
    base_reference: str,
    feature: str,
    maximum: int,
    flow_mode: str,
) -> dict[str, Any]:
    if maximum < 2 or maximum > 5:
        raise QualityGateError("max-candidates must be between 2 and 5")
    if flow_mode not in {"quick", "full"}:
        raise QualityGateError("flow mode must be quick or full")
    request = normalize_request(request)
    base_revision = resolve_revision(root, base_reference)
    head_revision = resolve_revision(root, "HEAD")
    spec: dict[str, Any] | None = None
    if feature:
        spec = _load_loop_spec(root, feature)
        if base_revision != head_revision:
            raise QualityGateError("Loop quality context must use a base that resolves to current HEAD")
        if request != normalize_request(_text(spec.get("request"), "Loop specification request")):
            raise QualityGateError("quality-gate request must exactly match the current Loop specification")
    paths = changed_paths(root, base_revision)
    if not paths:
        raise QualityGateError("engineering quality gate requires a non-empty implementation diff")
    if spec is not None:
        outside = [path for path in paths if not _path_allowed(path, spec["allowed_paths"])]
        if outside:
            raise QualityGateError("changes outside approved Loop paths: " + ", ".join(outside))
    records = [file_record(root, path) for path in paths]
    spec_fingerprint = spec["fingerprint"] if spec is not None else ""
    if spec is not None:
        change_value = {"spec_fingerprint": spec_fingerprint, "files": records}
    else:
        change_value = {
            "base_revision": base_revision,
            "head_revision": head_revision,
            "files": records,
        }
    change_fingerprint = fingerprint({**change_value, "fingerprint": ""}, "fingerprint")
    context: dict[str, Any] = {
        "schema": CONTEXT_SCHEMA,
        "request": request,
        "flow_mode": flow_mode,
        "feature": feature,
        "base_reference": base_reference,
        "base_revision": base_revision,
        "head_revision": head_revision,
        "spec_fingerprint": spec_fingerprint,
        "max_candidates": maximum,
        "changed_files": records,
        "change_scope": diff_scope(root, base_revision, paths),
        "instruction_sources": instruction_sources(root, paths),
        "candidate_examples": candidate_examples(root, request, paths, maximum),
        "verification_candidates": verification_candidates(root, paths, flow_mode, base_revision),
        "change_fingerprint": change_fingerprint,
    }
    context["context_fingerprint"] = fingerprint(context, "context_fingerprint")
    validate_context(root, context)
    return context


def validate_context(root: Path, value: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(value, CONTEXT_KEYS, "quality context")
    if value.get("schema") != CONTEXT_SCHEMA:
        raise QualityGateError("unsupported quality context schema")
    _text(value["request"], "quality context request")
    if value.get("flow_mode") not in {"quick", "full"}:
        raise QualityGateError("quality context flow_mode is invalid")
    feature = _text(value["feature"], "quality context feature", allow_empty=True)
    if feature and not FEATURE_RE.fullmatch(feature):
        raise QualityGateError("quality context feature is invalid")
    for key in ("base_reference", "base_revision", "head_revision", "change_fingerprint", "context_fingerprint"):
        _text(value[key], f"quality context {key}")
    for key in ("base_revision", "head_revision"):
        if not re.fullmatch(r"[0-9a-f]{40,64}", value[key]):
            raise QualityGateError(f"quality context {key} is not a commit object ID")
    for key in ("change_fingerprint", "context_fingerprint"):
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", value[key]):
            raise QualityGateError(f"quality context {key} is invalid")
    _text(value["spec_fingerprint"], "quality context spec_fingerprint", allow_empty=True)
    maximum = _integer(value["max_candidates"], "quality context max_candidates", minimum=2)
    if maximum > 5:
        raise QualityGateError("quality context max_candidates must be <= 5")
    changed_files = _list(value["changed_files"], "quality context changed_files")
    if not changed_files:
        raise QualityGateError("quality context requires a non-empty implementation diff")
    seen_paths: set[str] = set()
    for index, item in enumerate(changed_files, start=1):
        record = _mapping(item, f"changed file {index}")
        expected = (
            {"path", "kind"}
            if record.get("kind") == "deleted"
            else {"path", "kind", "mode", "sha256"}
        )
        _exact_keys(record, expected, f"changed file {index}")
        path = safe_relative(root, _text(record["path"], f"changed file {index} path"))
        if path in seen_paths:
            raise QualityGateError(f"duplicate changed path: {path}")
        seen_paths.add(path)
        if record["kind"] not in {"file", "deleted", "gitlink"}:
            raise QualityGateError(f"changed file {index} kind is invalid")
        if record["kind"] in {"file", "gitlink"}:
            if not re.fullmatch(
                r"[0-9a-f]{64}",
                _text(record["sha256"], f"changed file {index} sha256"),
            ):
                raise QualityGateError(f"changed file {index} sha256 is invalid")
            expected_mode = {"100644", "100755"} if record["kind"] == "file" else {"160000"}
            if record["mode"] not in expected_mode:
                raise QualityGateError(f"changed file {index} mode is invalid")
    if [item["path"] for item in changed_files] != sorted(seen_paths):
        raise QualityGateError("changed_files must use canonical path order")
    scope = _mapping(value["change_scope"], "quality context change_scope", {"files_changed", "lines_added", "lines_removed"})
    for key in scope:
        _integer(scope[key], f"quality context change_scope.{key}")
    if scope["files_changed"] != len(changed_files):
        raise QualityGateError("change_scope.files_changed does not match changed_files")
    sources = _string_list(value["instruction_sources"], "instruction_sources")
    for source in sources:
        safe_relative(root, source, require_existing=True)
    if sources != sorted(sources):
        raise QualityGateError("instruction_sources must use canonical order")
    candidates = _list(value["candidate_examples"], "candidate_examples")
    if len(candidates) > maximum:
        raise QualityGateError("candidate_examples exceeds max_candidates")
    expected_candidates = []
    for index, item in enumerate(candidates, start=1):
        candidate = _mapping(item, f"candidate example {index}", {"id", "path", "kind", "score", "reason"})
        if candidate["id"] != f"EX-{index:03d}":
            raise QualityGateError("candidate example IDs must be canonical")
        safe_relative(root, _text(candidate["path"], f"candidate example {index} path"), require_existing=True)
        _text(candidate["kind"], f"candidate example {index} kind")
        _integer(candidate["score"], f"candidate example {index} score")
        _text(candidate["reason"], f"candidate example {index} reason")
        expected_candidates.append(candidate)
    ranked = sorted(expected_candidates, key=lambda item: (-item["score"], item["kind"], item["path"]))
    if candidates != ranked:
        raise QualityGateError("candidate_examples must use canonical rank order")
    verification = _list(value["verification_candidates"], "verification_candidates")
    rank = []
    for index, item in enumerate(verification, start=1):
        candidate = _mapping(item, f"verification candidate {index}", {"id", "kind", "argv", "source", "priority", "scope"})
        if candidate["id"] != f"VC-{index:03d}":
            raise QualityGateError("verification candidate IDs must be canonical")
        if candidate["kind"] not in VERIFICATION_KINDS:
            raise QualityGateError(f"verification candidate {index} kind is invalid")
        _string_list(
            candidate["argv"],
            f"verification candidate {index} argv",
            nonempty=True,
            unique=False,
        )
        _text(candidate["source"], f"verification candidate {index} source")
        _integer(candidate["priority"], f"verification candidate {index} priority")
        _text(candidate["scope"], f"verification candidate {index} scope")
        rank.append(candidate)
    expected_rank = sorted(rank, key=lambda item: (item["priority"], item["kind"], item["source"], tuple(item["argv"])))
    if verification != expected_rank:
        raise QualityGateError("verification_candidates must use canonical order")
    if value["context_fingerprint"] != fingerprint(value, "context_fingerprint"):
        raise QualityGateError("quality context fingerprint is invalid")
    return value


def _normalize_strings(values: list[str]) -> list[str]:
    return sorted(set(values))


def _validate_repository_profile(root: Path, value: Any) -> dict[str, Any]:
    profile = _mapping(
        value,
        "repository_profile",
        {"architecture", "conventions", "representative_examples", "example_shortfall_reason", "applicable_rules"},
    )
    architecture = _mapping(profile["architecture"], "repository_profile.architecture", {"pattern", "relevant_layers"})
    _text(architecture["pattern"], "repository_profile.architecture.pattern")
    architecture["relevant_layers"] = _normalize_strings(
        _string_list(architecture["relevant_layers"], "repository_profile.architecture.relevant_layers")
    )
    conventions = _list(profile["conventions"], "repository_profile.conventions")
    normalized_conventions = []
    for index, item in enumerate(conventions, start=1):
        convention = _mapping(item, f"repository convention {index}", {"name", "value", "evidence"})
        _text(convention["name"], f"repository convention {index} name")
        _text(convention["value"], f"repository convention {index} value")
        convention["evidence"] = _normalize_strings(
            _string_list(convention["evidence"], f"repository convention {index} evidence", nonempty=True)
        )
        normalized_conventions.append(convention)
    profile["conventions"] = sorted(normalized_conventions, key=lambda item: (item["name"], item["value"]))
    examples = _string_list(profile["representative_examples"], "repository_profile.representative_examples")
    if len(examples) > 5:
        raise QualityGateError("representative_examples must contain at most five paths")
    for example in examples:
        safe_relative(root, example, require_existing=True)
    profile["representative_examples"] = sorted(examples)
    shortfall = _text(profile["example_shortfall_reason"], "repository_profile.example_shortfall_reason", allow_empty=True)
    if len(examples) < 2 and not shortfall.strip():
        raise QualityGateError("fewer than two representative examples requires example_shortfall_reason")
    if len(examples) >= 2 and shortfall.strip():
        raise QualityGateError("example_shortfall_reason must be empty when two or more examples exist")
    profile["applicable_rules"] = _normalize_strings(
        _string_list(profile["applicable_rules"], "repository_profile.applicable_rules", nonempty=True)
    )
    return profile


def _validate_finding(root: Path, value: Any, label: str, resolution: str) -> dict[str, Any]:
    finding = _mapping(value, label, FINDING_KEYS)
    finding_id = _text(finding["id"], f"{label}.id")
    if not FINDING_RE.fullmatch(finding_id):
        raise QualityGateError(f"{label}.id must match QG-###")
    if finding["severity"] not in SEVERITIES:
        raise QualityGateError(f"{label}.severity is invalid")
    if finding["category"] not in CATEGORIES:
        raise QualityGateError(f"{label}.category is invalid")
    safe_relative(root, _text(finding["file"], f"{label}.file"))
    _text(finding["location"], f"{label}.location", allow_empty=True)
    for key in ("issue", "impact", "recommended_fix"):
        _text(finding[key], f"{label}.{key}")
    finding["evidence"] = _normalize_strings(_string_list(finding["evidence"], f"{label}.evidence", nonempty=True))
    _boolean(finding["blocking"], f"{label}.blocking")
    if finding["severity"] == "high" and not finding["blocking"]:
        raise QualityGateError(f"{label}: High findings are always blocking")
    if finding["severity"] == "low" and finding["blocking"]:
        raise QualityGateError(f"{label}: Low findings cannot be blocking")
    if finding["resolution"] != resolution:
        raise QualityGateError(f"{label}.resolution must be {resolution}")
    fix = _text(finding["fix"], f"{label}.fix", allow_empty=True)
    reason = _text(finding["reason_not_fixed"], f"{label}.reason_not_fixed", allow_empty=True)
    if resolution == "fixed":
        if not fix.strip() or reason.strip():
            raise QualityGateError(f"{label} requires fix text and an empty reason_not_fixed")
    else:
        if fix.strip() or not reason.strip():
            raise QualityGateError(f"{label} requires reason_not_fixed and an empty fix")
    return finding


def _finding_sort(value: dict[str, Any]) -> tuple[Any, ...]:
    return (
        SEVERITIES.index(value["severity"]),
        CATEGORIES.index(value["category"]),
        value["file"],
        value["location"],
        value["id"],
    )


def _validate_verification(value: Any, label: str) -> dict[str, Any]:
    record = _mapping(value, label, VERIFICATION_KEYS)
    identifier = _text(record["id"], f"{label}.id")
    if not VERIFICATION_RE.fullmatch(identifier):
        raise QualityGateError(f"{label}.id must match KIND-###")
    if record["kind"] not in VERIFICATION_KINDS:
        raise QualityGateError(f"{label}.kind is invalid")
    if record["phase"] not in VERIFICATION_PHASES:
        raise QualityGateError(f"{label}.phase is invalid")
    _boolean(record["required"], f"{label}.required")
    if record["status"] not in VERIFICATION_STATUSES:
        raise QualityGateError(f"{label}.status is invalid")
    command = _string_list(record["command"], f"{label}.command", unique=False)
    evidence = _normalize_strings(_string_list(record["evidence"], f"{label}.evidence", nonempty=True))
    record["evidence"] = evidence
    _text(record["reason"], f"{label}.reason")
    exit_code = record["exit_code"]
    status = record["status"]
    if status == "pass":
        if (
            not command
            or isinstance(exit_code, bool)
            or not isinstance(exit_code, int)
            or exit_code != 0
        ):
            raise QualityGateError(f"{label}: pass requires argv and exit_code 0")
    elif status == "fail":
        if not command or isinstance(exit_code, bool) or not isinstance(exit_code, int) or exit_code == 0 or not evidence:
            raise QualityGateError(f"{label}: fail requires argv, nonzero exit_code, and evidence")
    else:
        if exit_code is not None:
            raise QualityGateError(f"{label}: {status} requires null exit_code")
        if status == "not_run" and not command:
            raise QualityGateError(f"{label}: not_run requires the applicable argv")
        if status == "unavailable" and command:
            raise QualityGateError(f"{label}: unavailable requires an empty command")
    return record


def _verification_sort(value: dict[str, Any]) -> tuple[Any, ...]:
    return (
        VERIFICATION_PHASES.index(value["phase"]),
        0 if value["required"] else 1,
        VERIFICATION_KINDS.index(value["kind"]),
        value["id"],
    )


def _validate_draft(root: Path, draft: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(draft, DRAFT_KEYS, "quality report draft")
    if draft.get("schema") != DRAFT_SCHEMA:
        raise QualityGateError("unsupported quality report draft schema")
    if draft.get("status") not in REPORT_STATUSES:
        raise QualityGateError("quality report draft status is invalid")
    _text(draft["summary"], "quality report draft summary")
    draft["repository_profile"] = _validate_repository_profile(root, draft["repository_profile"])
    fixed = [
        _validate_finding(root, item, f"fixed finding {index}", "fixed")
        for index, item in enumerate(_list(draft["findings_fixed"], "findings_fixed"), start=1)
    ]
    remaining = [
        _validate_finding(root, item, f"remaining finding {index}", "remaining")
        for index, item in enumerate(_list(draft["remaining_findings"], "remaining_findings"), start=1)
    ]
    identifiers = [item["id"] for item in fixed + remaining]
    if len(identifiers) != len(set(identifiers)):
        raise QualityGateError("finding IDs must be unique")
    draft["findings_fixed"] = sorted(fixed, key=_finding_sort)
    draft["remaining_findings"] = sorted(remaining, key=_finding_sort)
    verification = [
        _validate_verification(item, f"verification record {index}")
        for index, item in enumerate(_list(draft["verification"], "verification"), start=1)
    ]
    if not verification:
        raise QualityGateError("verification must record at least one pass, failure, or unavailable check")
    verification_ids = [item["id"] for item in verification]
    if len(verification_ids) != len(set(verification_ids)):
        raise QualityGateError("verification IDs must be unique")
    draft["verification"] = sorted(verification, key=_verification_sort)
    scope = _mapping(draft["change_scope"], "draft change_scope", {"new_dependencies", "unrelated_changes"})
    scope["new_dependencies"] = _normalize_strings(_string_list(scope["new_dependencies"], "change_scope.new_dependencies"))
    scope["unrelated_changes"] = _normalize_strings(_string_list(scope["unrelated_changes"], "change_scope.unrelated_changes"))
    quality = _mapping(draft["quality_evidence"], "quality_evidence", {"repository_consistency", "correctness", "testing", "simplicity"})
    for key in quality:
        quality[key] = _normalize_strings(_string_list(quality[key], f"quality_evidence.{key}", nonempty=True))
    decision = _mapping(draft["final_decision"], "final_decision", {"ready_for_next_stage", "blocking_reasons"})
    ready = _boolean(decision["ready_for_next_stage"], "final_decision.ready_for_next_stage")
    decision["blocking_reasons"] = _normalize_strings(_string_list(decision["blocking_reasons"], "final_decision.blocking_reasons"))

    blockers = [item for item in remaining if item["severity"] == "high" or (item["severity"] == "medium" and item["blocking"])]
    required_gaps = [
        item
        for item in verification
        if item["required"]
        and item["status"] != "pass"
        and not (fixed and item["phase"] == "before_fix")
    ]
    unrelated = scope["unrelated_changes"]
    if fixed:
        if not any(item["phase"] == "before_fix" for item in verification):
            raise QualityGateError("fixed findings require before_fix verification evidence")
        post_fix = [item for item in verification if item["required"] and item["phase"] in {"after_fix", "final"}]
        if not post_fix or any(item["status"] != "pass" for item in post_fix):
            raise QualityGateError("fixed findings require passing required after_fix or final verification")
    should_block = bool(blockers or required_gaps or unrelated)
    status = draft["status"]
    if status in {"PASS", "PASS_WITH_FINDINGS"}:
        if not ready or decision["blocking_reasons"]:
            raise QualityGateError(f"{status} requires ready_for_next_stage=true and no blocking reasons")
        if should_block:
            raise QualityGateError(f"{status} cannot contain blockers, required verification gaps, or unrelated changes")
        optional_gaps = any(not item["required"] and item["status"] != "pass" for item in verification)
        if status == "PASS" and (remaining or optional_gaps):
            raise QualityGateError("PASS requires no remaining findings or optional verification gaps")
        if status == "PASS_WITH_FINDINGS" and not (remaining or optional_gaps):
            raise QualityGateError("PASS_WITH_FINDINGS requires a nonblocking remainder or optional verification gap")
    else:
        if ready or not decision["blocking_reasons"]:
            raise QualityGateError("FAIL requires ready_for_next_stage=false and blocking reasons")
        if not should_block:
            raise QualityGateError("FAIL requires an evidence-backed blocking condition")
    return draft


def _context_path_for(root: Path, context: dict[str, Any], path: Path) -> str:
    return bounded_path(root, path).relative_to(root).as_posix()


def _current_context(root: Path, stored: dict[str, Any]) -> dict[str, Any]:
    return build_context(
        root,
        request=stored["request"],
        base_reference=stored["base_reference"],
        feature=stored["feature"],
        maximum=stored["max_candidates"],
        flow_mode=stored["flow_mode"],
    )


def validate_final_report(
    root: Path,
    report: dict[str, Any],
    *,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate a finalized report; exported for the Loop runtime gate."""
    _exact_keys(report, REPORT_KEYS, "final quality report")
    if report.get("schema") != REPORT_SCHEMA:
        raise QualityGateError("unsupported final quality report schema")
    if report.get("report_fingerprint") != fingerprint(report, "report_fingerprint"):
        raise QualityGateError("quality report fingerprint is invalid")
    context_path = gate_artifact_path(
        root,
        _text(report["context_path"], "quality report context_path"),
        "context",
    ).relative_to(root).as_posix()
    if context is None:
        context = load_mapping(root, root / context_path, "quality context")
    validate_context(root, context)
    if report.get("context_fingerprint") != context["context_fingerprint"]:
        raise QualityGateError("quality report context fingerprint is stale or mismatched")
    if report.get("change_fingerprint") != context["change_fingerprint"]:
        raise QualityGateError("quality report change fingerprint is stale or mismatched")
    final_scope = _mapping(
        report["change_scope"],
        "final change_scope",
        {"files_changed", "lines_added", "lines_removed", "new_dependencies", "unrelated_changes"},
    )
    for key in ("files_changed", "lines_added", "lines_removed"):
        _integer(final_scope[key], f"final change_scope.{key}")
        if final_scope[key] != context["change_scope"][key]:
            raise QualityGateError(f"final change_scope.{key} does not match the current context")
    draft = copy.deepcopy({key: report[key] for key in DRAFT_KEYS})
    draft["schema"] = DRAFT_SCHEMA
    draft["change_scope"] = {
        "new_dependencies": final_scope["new_dependencies"],
        "unrelated_changes": final_scope["unrelated_changes"],
    }
    _validate_draft(root, draft)
    candidate_paths = {item["path"] for item in context["candidate_examples"]}
    selected_examples = set(draft["repository_profile"]["representative_examples"])
    if not selected_examples.issubset(candidate_paths):
        outside = sorted(selected_examples - candidate_paths)
        raise QualityGateError("representative examples were not emitted by bounded context: " + ", ".join(outside))
    normalized = copy.deepcopy(draft)
    normalized["schema"] = REPORT_SCHEMA
    normalized["context_path"] = context_path
    normalized["context_fingerprint"] = report["context_fingerprint"]
    normalized["change_fingerprint"] = report["change_fingerprint"]
    normalized["change_scope"] = {
        **context["change_scope"],
        "new_dependencies": draft["change_scope"]["new_dependencies"],
        "unrelated_changes": draft["change_scope"]["unrelated_changes"],
    }
    normalized["report_fingerprint"] = report["report_fingerprint"]
    if report != normalized:
        raise QualityGateError("final quality report is not canonically normalized")
    return report


def verify_report_current(root: Path, report_path: Path) -> dict[str, Any]:
    """Load a report, validate its signatures, and reject repository drift."""
    root = project_root(root)
    report_path = gate_artifact_path(root, report_path, "report")
    report = load_mapping(root, report_path, "final quality report")
    validate_final_report(root, report)
    context = load_mapping(root, root / report["context_path"], "quality context")
    current = _current_context(root, context)
    if current["context_fingerprint"] != context["context_fingerprint"]:
        raise QualityGateError("quality context is stale for the current repository state")
    if current["change_fingerprint"] != report["change_fingerprint"]:
        raise QualityGateError("quality report is stale for the current implementation diff")
    if report["status"] not in {"PASS", "PASS_WITH_FINDINGS"} or not report["final_decision"]["ready_for_next_stage"]:
        raise QualityGateError("quality report is current but not ready for the next stage")
    return report


def default_report_path(feature: str) -> Path:
    if feature:
        return Path(".ai-sdlc-loop") / feature / "quality-gate.toon"
    return Path(".ai-sdlc") / "engineering-quality-gate" / "quality-report.toon"


def cli_toon_path(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise QualityGateError(f"{label} must be repository-relative")
    if path.suffix != ".toon":
        raise QualityGateError(f"{label} must use a .toon extension")
    return path


def cmd_context(args: argparse.Namespace) -> None:
    root = project_root(args.root)
    flow_mode = "full" if args.full_flow else "quick"
    context = build_context(
        root,
        request=args.request,
        base_reference=args.base,
        feature=args.feature or "",
        maximum=args.max_candidates,
        flow_mode=flow_mode,
    )
    if args.output:
        output = cli_toon_path(args.output, "context output")
        output = gate_artifact_path(root, output, "context")
        atomic_write(root, output, context)
        print(f"{bounded_path(root, output).relative_to(root).as_posix()} {context['context_fingerprint']}")
    else:
        print(encode_toon(context), end="")


def cmd_finalize(args: argparse.Namespace) -> None:
    root = project_root(args.root)
    context_path = gate_artifact_path(
        root,
        cli_toon_path(args.context, "context path"),
        "context",
    )
    draft_path = gate_artifact_path(
        root,
        cli_toon_path(args.draft, "draft path"),
        "draft",
    )
    raw_output = cli_toon_path(args.output, "report output") if args.output else default_report_path("")
    output = gate_artifact_path(root, raw_output, "report")
    if len({context_path, draft_path, output}) != 3:
        raise QualityGateError("context, draft, and report artifact paths must be distinct")
    context = load_mapping(root, context_path, "quality context")
    validate_context(root, context)
    current = _current_context(root, context)
    if current["context_fingerprint"] != context["context_fingerprint"]:
        raise QualityGateError("quality context is stale; regenerate it before finalizing")
    if not args.output:
        output = gate_artifact_path(root, default_report_path(context["feature"]), "report")
        if len({context_path, draft_path, output}) != 3:
            raise QualityGateError("context, draft, and report artifact paths must be distinct")
    draft = load_mapping(root, draft_path, "quality report draft")
    draft = _validate_draft(root, draft)
    report: dict[str, Any] = dict(draft)
    report["schema"] = REPORT_SCHEMA
    report["context_path"] = _context_path_for(root, context, context_path)
    report["context_fingerprint"] = context["context_fingerprint"]
    report["change_fingerprint"] = context["change_fingerprint"]
    report["change_scope"] = {
        **context["change_scope"],
        "new_dependencies": draft["change_scope"]["new_dependencies"],
        "unrelated_changes": draft["change_scope"]["unrelated_changes"],
    }
    report["report_fingerprint"] = fingerprint(report, "report_fingerprint")
    validate_final_report(root, report, context=context)
    atomic_write(root, output, report)
    print(f"{bounded_path(root, output).relative_to(root).as_posix()} {report['report_fingerprint']}")


def cmd_verify(args: argparse.Namespace) -> None:
    root = project_root(args.root)
    report_path = gate_artifact_path(
        root,
        cli_toon_path(args.report, "report path"),
        "report",
    )
    report = verify_report_current(root, report_path)
    print(f"current {report['status']} {report['report_fingerprint']}")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    commands = value.add_subparsers(dest="command_name", required=True)

    def add_state_boundary(command: argparse.ArgumentParser) -> None:
        command.add_argument("--state-check", action="store_true")
        command.add_argument("--begin-state", action="store_true")
        command.add_argument("--complete-state", action="store_true")

    value.add_argument("--state-check", dest="root_state_check", action="store_true")
    value.add_argument("--begin-state", dest="root_begin_state", action="store_true")
    value.add_argument("--complete-state", dest="root_complete_state", action="store_true")

    context = commands.add_parser("context", help="compile deterministic bounded repository context")
    add_state_boundary(context)
    context.add_argument("--root", default=".")
    context.add_argument("--request", required=True)
    context.add_argument("--base", default="HEAD")
    context.add_argument("--feature")
    context.add_argument("--max-candidates", type=int, default=5)
    context.add_argument("--output")
    modes = context.add_mutually_exclusive_group()
    modes.add_argument("--quick-flow", action="store_true")
    modes.add_argument("--full-flow", action="store_true")
    context.set_defaults(handler=cmd_context)
    finalize = commands.add_parser("finalize", help="validate and sign a current evidence report")
    add_state_boundary(finalize)
    finalize.add_argument("--root", default=".")
    finalize.add_argument("--context", required=True)
    finalize.add_argument("--draft", required=True)
    finalize.add_argument("--output")
    finalize.set_defaults(handler=cmd_finalize)
    verify = commands.add_parser("verify", help="reject invalid, non-ready, or stale report evidence")
    add_state_boundary(verify)
    verify.add_argument("--root", default=".")
    verify.add_argument("--report", required=True)
    verify.set_defaults(handler=cmd_verify)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.begin_state or args.complete_state or args.root_begin_state or args.root_complete_state:
            raise QualityGateError(
                "engineering quality evidence cannot begin or complete the owning lifecycle state"
            )
        args.handler(args)
    except QualityGateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
