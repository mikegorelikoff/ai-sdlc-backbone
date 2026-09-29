#!/usr/bin/env python3
"""Unified telemetry recording and querying for AI SDLC Harness (Backbone).

Implements the unified TelemetryEvent v1 schema (schema: ai-sdlc-telemetry/v1).
Pure TOON append-only time-series stream stored at .ai/telemetry/sessions.toon.
Enforces POSIX flock concurrency, secret redaction, user resolution, and zero token fabrication.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime
import os
import re
import secrets
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    import ai_sdlc_toon as toon_codec
except ImportError:
    try:
        import toon as toon_codec  # type: ignore
    except ImportError:
        toon_codec = None  # type: ignore

try:
    import fcntl
except ImportError:
    fcntl = None  # type: ignore

SCHEMA_VERSION = "ai-sdlc-telemetry/v1"
DEFAULT_PRODUCT = "ai-sdlc-backbone"
DEFAULT_VERSION = "5.7.0"
CROCKFORD_BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

SECRET_PATTERNS = [
    re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)([^\s\"']+)"),
    re.compile(r"(?i)(bearer\s+)([a-zA-Z0-9_\-\.]{10,})"),
    re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)([^\s\"']+)"),
    re.compile(r"(?i)(token\s*[:=]\s*)([^\s\"']+)"),
    re.compile(r"(?i)(password\s*[:=]\s*)([^\s\"']+)"),
    re.compile(r"(?i)(secret\s*[:=]\s*)([^\s\"']+)"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b"),
    re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z-_]{35}\b"),
]

CANONICAL_ROLES = {
    "business-analyst",
    "product-manager",
    "product-owner",
    "qa-engineer",
    "software-architect",
    "software-engineer",
}

_last_ulid_ms = 0
_last_ulid_entropy = 0


def generate_ulid(now_ms: int | None = None) -> str:
    """Generate a 26-character monotonic Crockford Base32 ULID."""
    global _last_ulid_ms, _last_ulid_entropy
    if now_ms is None:
        now_ms = int(time.time() * 1000)

    if now_ms <= _last_ulid_ms:
        now_ms = _last_ulid_ms
        _last_ulid_entropy = (_last_ulid_entropy + 1) & ((1 << 80) - 1)
        if _last_ulid_entropy == 0:
            now_ms += 1
            _last_ulid_ms = now_ms
            _last_ulid_entropy = secrets.randbits(80)
    else:
        _last_ulid_ms = now_ms
        _last_ulid_entropy = secrets.randbits(80)

    t = now_ms
    t_chars: list[str] = []
    for _ in range(10):
        t_chars.append(CROCKFORD_BASE32[t & 0x1F])
        t >>= 5
    t_part = "".join(reversed(t_chars))

    r = _last_ulid_entropy
    r_chars: list[str] = []
    for _ in range(16):
        r_chars.append(CROCKFORD_BASE32[r & 0x1F])
        r >>= 5
    r_part = "".join(reversed(r_chars))

    return t_part + r_part


def format_iso_ms(dt: datetime.datetime | None = None) -> str:
    """Format datetime as UTC ISO 8601 with milliseconds (YYYY-MM-DDTHH:MM:SS.mmmZ)."""
    if dt is None:
        dt = datetime.datetime.now(datetime.timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)
    ms = dt.microsecond // 1000
    return f"{dt.strftime('%Y-%m-%dT%H:%M:%S')}.{ms:03d}Z"


def redact_text(text: str) -> str:
    """Strip bearer tokens, API keys, and private keys from text."""
    if not isinstance(text, str):
        return text
    result = text
    for pattern in SECRET_PATTERNS:
        result = pattern.sub(r"\1[REDACTED]" if pattern.groups >= 1 else "[REDACTED]", result)
    return result


def sanitize_data(val: Any) -> Any:
    """Recursively redact secrets from data structures."""
    if val is None or isinstance(val, (bool, int, float)):
        return val
    if isinstance(val, str):
        return redact_text(val)
    if isinstance(val, dict):
        return {str(k): sanitize_data(v) for k, v in val.items()}
    if isinstance(val, (list, tuple, set)):
        return [sanitize_data(item) for item in val]
    return redact_text(str(val))


def find_repository_root(start_dir: Path | str | None = None) -> Path:
    """Locate the git or workspace root directory."""
    try:
        current = Path(start_dir).resolve() if start_dir else Path.cwd().resolve()
        for candidate in [current] + list(current.parents):
            if (candidate / ".git").exists() or (candidate / ".ai-sdlc").exists() or (candidate / ".ai-sdlc-loop").exists():
                return candidate
    except Exception:
        pass
    return Path.cwd().resolve()


def get_telemetry_file_path(root: Path | str | None = None) -> Path:
    """Resolve the storage path for pure TOON telemetry (.ai/telemetry/sessions.toon)."""
    repo_root = Path(root).resolve() if root else find_repository_root()
    return repo_root / ".ai" / "telemetry" / "sessions.toon"


def _acquire_lock(fd: int, timeout: float = 2.0, retry_delay: float = 0.05) -> bool:
    """Acquire POSIX non-blocking flock with retry and timeout."""
    if fcntl is None:
        return True
    deadline = time.time() + timeout
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (BlockingIOError, OSError):
            if time.time() >= deadline:
                return False
            time.sleep(retry_delay)


def _release_lock(fd: int) -> None:
    """Release POSIX lock safely."""
    if fcntl is not None:
        with contextlib.suppress(Exception):
            fcntl.flock(fd, fcntl.LOCK_UN)


def _run_git_cmd(args: list[str], root: Path) -> str:
    """Run git command safely and return stripped stdout."""
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
            timeout=2.0,
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
    except Exception:
        pass
    return ""


def resolve_user(root: Path | str | None = None) -> dict[str, str]:
    """Resolve user {name, email, role} from .customization.toon or ~/.config/ai-sdlc/config.toon with git/env fallback."""
    repo_root = Path(root).resolve() if root else find_repository_root()
    user_name = ""
    user_email = ""
    user_role = ""

    # Check candidates for config
    candidates = [
        repo_root / ".customization.toon",
        Path.cwd() / ".customization.toon",
        Path.home() / ".config" / "ai-sdlc" / "config.toon",
    ]
    for candidate in candidates:
        if candidate.is_file():
            try:
                content = candidate.read_text(encoding="utf-8")
                if toon_codec:
                    data = toon_codec.loads(content)
                    if isinstance(data, dict):
                        vals = data.get("values", {})
                        if isinstance(vals, dict) and "user" in vals and isinstance(vals["user"], dict):
                            u = vals["user"]
                            user_name = str(u.get("name") or "")
                            user_email = str(u.get("email") or "")
                            user_role = str(u.get("role") or "")
                            if not user_name and "git" in u and isinstance(u["git"], dict):
                                user_name = str(u["git"].get("name") or "")
                            if not user_email and "git" in u and isinstance(u["git"], dict):
                                user_email = str(u["git"].get("email") or "")
                            if user_name or user_email or user_role:
                                break
            except Exception:
                pass

    # Fallbacks for name
    if not user_name:
        user_name = (
            os.environ.get("AI_SDLC_USER_NAME")
            or _run_git_cmd(["config", "user.name"], repo_root)
            or os.environ.get("GIT_AUTHOR_NAME")
            or os.environ.get("USER")
            or os.environ.get("USERNAME")
            or "unknown"
        )

    # Fallbacks for email
    if not user_email:
        user_email = (
            os.environ.get("AI_SDLC_USER_EMAIL")
            or _run_git_cmd(["config", "user.email"], repo_root)
            or os.environ.get("GIT_AUTHOR_EMAIL")
            or os.environ.get("EMAIL")
            or ""
        )

    # Fallbacks for role
    if not user_role:
        env_role = os.environ.get("AI_SDLC_USER_ROLE", "").strip()
        user_role = env_role if env_role in CANONICAL_ROLES else "software-engineer"
    elif user_role not in CANONICAL_ROLES:
        user_role = "software-engineer"

    return {
        "email": redact_text(user_email),
        "name": redact_text(user_name),
        "role": user_role,
    }


def resolve_git(root: Path | str | None = None) -> dict[str, str]:
    """Resolve git {name, email, repository, branch, commit} safely."""
    repo_root = Path(root).resolve() if root else find_repository_root()

    name = _run_git_cmd(["config", "user.name"], repo_root) or os.environ.get("GIT_AUTHOR_NAME", "")
    email = _run_git_cmd(["config", "user.email"], repo_root) or os.environ.get("GIT_AUTHOR_EMAIL", "")
    repo = _run_git_cmd(["remote", "get-url", "origin"], repo_root) or repo_root.name
    branch = _run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"], repo_root) or os.environ.get("GIT_BRANCH") or "main"
    commit = _run_git_cmd(["rev-parse", "HEAD"], repo_root) or os.environ.get("GIT_COMMIT") or "unknown"

    return {
        "branch": redact_text(branch),
        "commit": redact_text(commit),
        "email": redact_text(email),
        "name": redact_text(name),
        "repository": redact_text(repo),
    }


def normalize_status(status: str | None) -> str:
    """Normalize status to 'success' | 'error' | 'fail' | 'blocked'."""
    if not status:
        return "success"
    st = status.lower().strip()
    if st in ("completed", "passed", "success", "ok"):
        return "success"
    if st in ("failed", "fail", "abandoned"):
        return "fail"
    if st in ("error", "exception", "crashed"):
        return "error"
    if st in ("blocked", "pending"):
        return "blocked"
    return "success"


def record_telemetry_event(
    skill: str | dict[str, Any],
    *,
    status: str = "success",
    timestamp_start: str | None = None,
    timestamp_end: str | None = None,
    duration_ms: int | None = None,
    product: str | None = None,
    version: str | None = None,
    user: dict[str, Any] | None = None,
    git: dict[str, Any] | None = None,
    task: dict[str, Any] | None = None,
    models: list[dict[str, Any]] | None = None,
    error: dict[str, str] | None = None,
    parent_event_id: str | None = None,
    usage_available: bool | None = None,
    root: Path | str | None = None,
    **kwargs: Any,
) -> dict[str, Any] | None:
    """Record a unified TelemetryEvent v1 into .ai/telemetry/sessions.toon.

    Guaranteed fail-open exception shielding: returns the event dictionary on success,
    or None on failure without raising.
    """
    try:
        repo_root = Path(root).resolve() if root else find_repository_root()

        # Generate monotonic ULID
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        event_id = generate_ulid(int(now_dt.timestamp() * 1000))

        # Timestamps and duration
        ts_end = timestamp_end or format_iso_ms(now_dt)
        if duration_ms is not None:
            calc_dur = max(0, int(duration_ms))
        else:
            calc_dur = 0

        if timestamp_start:
            ts_start = timestamp_start
        elif duration_ms is not None and duration_ms > 0:
            start_dt = now_dt - datetime.timedelta(milliseconds=calc_dur)
            ts_start = format_iso_ms(start_dt)
        else:
            ts_start = ts_end

        # Source
        source_prod = product or DEFAULT_PRODUCT
        source_ver = version or DEFAULT_VERSION
        source_obj = {"product": source_prod, "version": source_ver}

        # User resolution
        resolved_user = resolve_user(repo_root)
        if user and isinstance(user, dict):
            for k in ("name", "email", "role"):
                if k in user and user[k]:
                    resolved_user[k] = redact_text(str(user[k]))

        # Git resolution
        resolved_git = resolve_git(repo_root)
        if git and isinstance(git, dict):
            for k in ("name", "email", "repository", "branch", "commit"):
                if k in git and git[k]:
                    resolved_git[k] = redact_text(str(git[k]))

        # Skill resolution
        if isinstance(skill, dict):
            skill_obj = {
                "name": redact_text(str(skill.get("name", "unknown"))),
                "version": redact_text(str(skill.get("version", source_ver))),
            }
        else:
            skill_obj = {
                "name": redact_text(str(skill)),
                "version": redact_text(str(version or "1.0.0")),
            }

        # Task resolution
        task_obj = None
        if task and isinstance(task, dict):
            task_obj = {
                "id": redact_text(str(task.get("id", ""))),
                "owner": redact_text(str(task.get("owner", ""))),
                "title": redact_text(str(task.get("title", ""))),
                "type": redact_text(str(task.get("type", ""))),
            }

        # Model usage and token fabrication prevention
        # STRICT: if model token usage is not available from runner/model,
        # usage_available=False and models=[] (models[0]:). Zero token fabrication!
        clean_models: list[dict[str, Any]] = []
        is_usage_available = False
        if models and isinstance(models, list) and len(models) > 0 and usage_available is not False:
            is_usage_available = True
            for m in models:
                if isinstance(m, dict):
                    clean_models.append({
                        "cache_read_tokens": int(m.get("cache_read_tokens", 0)),
                        "cache_write_tokens": int(m.get("cache_write_tokens", 0)),
                        "input_tokens": int(m.get("input_tokens", 0)),
                        "model": redact_text(str(m.get("model", "unknown"))),
                        "output_tokens": int(m.get("output_tokens", 0)),
                        "provider": redact_text(str(m.get("provider", "unknown"))),
                        "reasoning_tokens": int(m.get("reasoning_tokens", 0)),
                        "total_tokens": int(m.get("total_tokens", int(m.get("input_tokens", 0)) + int(m.get("output_tokens", 0)))),
                    })
        else:
            is_usage_available = False
            clean_models = []

        # Status and error
        norm_status = normalize_status(status)
        error_obj = None
        if error and isinstance(error, dict):
            error_obj = {
                "code": redact_text(str(error.get("code", "ERROR"))),
                "message": redact_text(str(error.get("message", ""))),
            }
        elif norm_status in ("error", "fail") and kwargs.get("error_message"):
            error_obj = {
                "code": redact_text(str(kwargs.get("error_code", "ERROR"))),
                "message": redact_text(str(kwargs["error_message"])),
            }

        event_payload: dict[str, Any] = {
            "duration_ms": calc_dur,
            "error": error_obj,
            "event_id": event_id,
            "git": resolved_git,
            "models": clean_models,
            "parent_event_id": str(parent_event_id) if parent_event_id else None,
            "skill": skill_obj,
            "source": source_obj,
            "status": norm_status,
            "task": task_obj,
            "timestamp_end": ts_end,
            "timestamp_start": ts_start,
            "usage_available": is_usage_available,
            "user": resolved_user,
        }

        # Persist event fail-open
        append_ok = _append_event_to_file(event_payload, repo_root)
        return event_payload if append_ok else None

    except Exception:
        # Strict fail-open shielding
        return None


def _append_event_to_file(event: dict[str, Any], root: Path) -> bool:
    """Append event to .ai/telemetry/sessions.toon with flock and fail-open exception shielding."""
    try:
        telemetry_file = get_telemetry_file_path(root)
        telemetry_file.parent.mkdir(parents=True, exist_ok=True)

        event_id = event["event_id"]
        if toon_codec:
            raw_chunk = toon_codec.encode_toon({event_id: event})
        else:
            # Fallback simple serializer if codec unavailable
            lines = [f'"{event_id}":']
            for k in sorted(event):
                lines.append(f"  {k}: {event[k]}")
            raw_chunk = "\n".join(lines) + "\n"

        indented_chunk = "\n".join("  " + line if line else "" for line in raw_chunk.splitlines()) + "\n"

        with open(telemetry_file, "a+", encoding="utf-8") as f:
            if not _acquire_lock(f.fileno(), timeout=3.0):
                return False
            try:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0:
                    f.write(f"schema: {SCHEMA_VERSION}\nevents:\n")
                f.write(indented_chunk)
                f.flush()
            finally:
                _release_lock(f.fileno())

        return True
    except Exception:
        return False


def read_telemetry_events(
    root: Path | str | None = None,
    event_id: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Read telemetry events from .ai/telemetry/sessions.toon."""
    telemetry_file = get_telemetry_file_path(root)
    if not telemetry_file.is_file():
        return []

    try:
        content = telemetry_file.read_text(encoding="utf-8", errors="replace")
        if not toon_codec:
            return []
        data = toon_codec.loads(content)
        if not isinstance(data, dict):
            return []
        events_dict = data.get("events", {})
        if not isinstance(events_dict, dict):
            return []

        results: list[dict[str, Any]] = []
        for eid, edata in events_dict.items():
            if isinstance(edata, dict):
                if event_id and str(eid) != str(event_id) and edata.get("event_id") != str(event_id):
                    continue
                results.append(edata)

        if limit is not None and limit > 0:
            results = results[-limit:]

        return results
    except Exception:
        return []


def dump_telemetry(root: Path | str | None = None) -> str:
    """Return raw content of .ai/telemetry/sessions.toon."""
    telemetry_file = get_telemetry_file_path(root)
    if not telemetry_file.is_file():
        return f"schema: {SCHEMA_VERSION}\nevents:\n"
    try:
        return telemetry_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return f"schema: {SCHEMA_VERSION}\nevents:\n"


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for ai_sdlc_telemetry."""
    parser = argparse.ArgumentParser(description="AI SDLC Telemetry Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # record
    record_parser = subparsers.add_parser("record", help="Record a telemetry event")
    record_parser.add_argument("--skill", required=True, help="Skill name")
    record_parser.add_argument("--skill-version", default="1.0.0", help="Skill version")
    record_parser.add_argument("--status", choices=["success", "error", "fail", "blocked"], default="success")
    record_parser.add_argument("--duration-ms", type=int, help="Duration in milliseconds")
    record_parser.add_argument("--product", choices=["ai-sdlc-backbone", "ai-sdlc-loop"], help="Product name")
    record_parser.add_argument("--task-id", help="Task ID")
    record_parser.add_argument("--task-type", help="Task type")
    record_parser.add_argument("--task-title", help="Task title")
    record_parser.add_argument("--task-owner", help="Task owner")
    record_parser.add_argument("--parent-event-id", help="Parent event ID")
    record_parser.add_argument("--error-code", help="Error code")
    record_parser.add_argument("--error-message", help="Error message")
    record_parser.add_argument("--root", type=Path, help="Project root directory")

    # read
    read_parser = subparsers.add_parser("read", help="Read telemetry events")
    read_parser.add_argument("--event-id", help="Filter by specific event ID")
    read_parser.add_argument("--limit", type=int, help="Limit number of events returned")
    read_parser.add_argument("--root", type=Path, help="Project root directory")

    # dump
    dump_parser = subparsers.add_parser("dump", help="Dump raw sessions.toon content")
    dump_parser.add_argument("--root", type=Path, help="Project root directory")

    args = parser.parse_args(argv)

    if args.command == "record":
        task_info = None
        if args.task_id or args.task_type or args.task_title or args.task_owner:
            task_info = {
                "id": args.task_id or "",
                "type": args.task_type or "",
                "title": args.task_title or "",
                "owner": args.task_owner or "",
            }

        error_info = None
        if args.error_code or args.error_message:
            error_info = {
                "code": args.error_code or "ERROR",
                "message": args.error_message or "",
            }

        ev = record_telemetry_event(
            skill={"name": args.skill, "version": args.skill_version},
            status=args.status,
            duration_ms=args.duration_ms,
            product=args.product,
            task=task_info,
            error=error_info,
            parent_event_id=args.parent_event_id,
            root=args.root,
        )
        if ev:
            print(f"Recorded event {ev['event_id']}")
            return 0
        else:
            print("Failed to record telemetry event (fail-open)", file=sys.stderr)
            return 1

    elif args.command == "read":
        events = read_telemetry_events(root=args.root, event_id=args.event_id, limit=args.limit)
        doc = {"schema": SCHEMA_VERSION, "events": {e["event_id"]: e for e in events}}
        if toon_codec:
            print(toon_codec.dumps(doc))
        else:
            print(doc)
        return 0

    elif args.command == "dump":
        print(dump_telemetry(root=args.root), end="")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
