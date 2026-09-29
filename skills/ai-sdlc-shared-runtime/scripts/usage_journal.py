#!/usr/bin/env python3
"""Deterministic local usage journal for AI SDLC Loop.

Append-only, session-based, event-sourced behavioral logging in .toon format.
Enforces data minimization, secret redaction, and fail-open resilience.
"""

from __future__ import annotations

import contextlib
import datetime
import hashlib
import os
import re
import secrets
import sys
import time
from pathlib import Path
from typing import Any

# Ensure toon encoder/decoder from shared runtime is available
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

try:
    from toon import ToonDecodeError, decode_toon, encode_toon
except ImportError:
    # Graceful fallback in case toon.py is packaged under ai_sdlc_toon
    try:
        from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon  # type: ignore
    except ImportError:
        decode_toon = None  # type: ignore
        encode_toon = None  # type: ignore
        ToonDecodeError = Exception  # type: ignore

try:
    import fcntl
except ImportError:
    fcntl = None  # type: ignore

SCHEMA_VERSION = "ai-sdlc-usage/v1"
RUNTIME_VERSION = "5.7.0"

# Regex patterns for secret redaction
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

# Sensitive keys that should not be recorded directly in full text
PROHIBITED_KEY_PATTERNS = re.compile(
    r"(?i)^(prompt|raw_prompt|user_prompt|code|source_code|source_content|transcript|model_prose|model_output|stdout|stderr|raw_output)$"
)


def _now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _iso_now() -> str:
    return _now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")


def _redact_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    result = text
    for pattern in SECRET_PATTERNS:
        result = pattern.sub(r"\1[REDACTED]" if pattern.groups >= 1 else "[REDACTED]", result)
    return result


def _sanitize_value(key: str, val: Any) -> Any:
    """Sanitize data for strict minimization and secret prevention."""
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        # If key is sensitive, avoid storing large text
        if PROHIBITED_KEY_PATTERNS.match(key):
            # If it's a short reference, keep it, else summarize
            if len(val) <= 120 and not ("\n" in val or "def " in val or "import " in val):
                return _redact_text(val)
            return "[MINIMIZED_REFERENCE]"
        if len(val) > 400:
            val = val[:397] + "..."
        return _redact_text(val)
    if isinstance(val, dict):
        return {
            str(k): _sanitize_value(str(k), v)
            for k, v in val.items()
            if not PROHIBITED_KEY_PATTERNS.match(str(k))
        }
    if isinstance(val, (list, tuple, set)):
        return [_sanitize_value(key, item) for item in val]
    return _redact_text(str(val))


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


def get_usage_dir(root: Path | None = None) -> Path:
    """Resolve the usage directory (.ai-sdlc/usage or .ai-sdlc-loop/usage)."""
    repo_root = root if root else find_repository_root()
    if (repo_root / ".ai-sdlc").is_dir():
        return repo_root / ".ai-sdlc" / "usage"
    if (repo_root / ".ai-sdlc-loop").is_dir():
        return repo_root / ".ai-sdlc-loop" / "usage"
    return repo_root / ".ai-sdlc" / "usage"


def get_project_ref(root: Path) -> str:
    """Compute an immutable fingerprint of the project root."""
    try:
        resolved = str(root.resolve()).encode("utf-8")
        return "sha256:" + hashlib.sha256(resolved).hexdigest()[:16]
    except Exception:
        return "sha256:unknown"


def get_active_session_id(root: Path | None = None) -> str:
    """Get or generate the active session ID for the current context."""
    env_id = os.environ.get("AI_SDLC_SESSION_ID") or os.environ.get("AI_SDLC_LOOP_SESSION_ID")
    if env_id and re.match(r"^[0-9]{8}T[0-9]{6}Z-[a-f0-9]{4,}$", env_id):
        return env_id

    repo_root = root if root else find_repository_root()
    usage_dir = get_usage_dir(repo_root)
    session_pointer = usage_dir / "current_session.toon"
    if session_pointer.is_file():
        try:
            content = session_pointer.read_text(encoding="utf-8")
            if decode_toon:
                data = decode_toon(content)
                sid = data.get("session_id")
                if sid and isinstance(sid, str):
                    os.environ["AI_SDLC_SESSION_ID"] = sid
                    return sid
        except Exception:
            pass

    # Generate new session ID: YYYYMMDDTHHMMSSZ-<random_token>
    now_str = _now_utc().strftime("%Y%m%dT%H%M%SZ")
    random_token = secrets.token_hex(2)
    session_id = f"{now_str}-{random_token}"
    os.environ["AI_SDLC_SESSION_ID"] = session_id

    try:
        session_pointer.parent.mkdir(parents=True, exist_ok=True)
        session_pointer.write_text(f"session_id: {session_id}\nupdated_at: {_iso_now()}\n", encoding="utf-8")
    except Exception:
        pass

    return session_id


def get_session_file_path(
    session_id: str,
    root: Path | None = None,
    date_str: str | None = None,
) -> Path:
    """Resolve the session .toon file path."""
    repo_root = root if root else find_repository_root()
    if not date_str:
        # Extract from session_id if format is YYYYMMDDTHHMMSSZ-...
        m = re.match(r"^(\d{4})(\d{2})(\d{2})T", session_id)
        if m:
            date_str = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        else:
            date_str = _now_utc().strftime("%Y-%m-%d")
    return get_usage_dir(repo_root) / "sessions" / date_str / f"{session_id}.toon"


def init_session(
    session_id: str | None = None,
    root: Path | None = None,
    project_ref: str | None = None,
    runtime_version: str | None = None,
) -> Path | None:
    """Initialize a session file with header if it doesn't already exist."""
    try:
        repo_root = root if root else find_repository_root()
        sid = session_id if session_id else get_active_session_id(repo_root)
        session_file = get_session_file_path(sid, repo_root)

        if not session_file.is_file():
            session_file.parent.mkdir(parents=True, exist_ok=True)
            pref = project_ref or get_project_ref(repo_root)
            rver = runtime_version or RUNTIME_VERSION
            now_iso = _iso_now()

            header = (
                f"schema: {SCHEMA_VERSION}\n"
                f"session_id: {sid}\n"
                f"started_at: {now_iso}\n"
                f"project_ref: {pref}\n"
                f"runtime_version: {rver}\n\n"
                f"events:\n"
            )
            session_file.write_text(header, encoding="utf-8")

            # Record session.start event as seq 1
            record_event(
                "session.start",
                {"runtime_version": rver, "project_ref": pref},
                session_id=sid,
                root=repo_root,
            )

        return session_file
    except Exception:
        # Fail-open: never raise
        return None


def _get_next_sequence_and_offset(path: Path) -> int:
    """Determine the next monotonic event sequence number for a session file."""
    if not path.is_file():
        return 1
    max_seq = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line_str = line.strip()
                if line_str.startswith("seq:"):
                    parts = line_str.split(":", 1)
                    if len(parts) == 2:
                        val = parts[1].strip()
                        if val.isdigit():
                            max_seq = max(max_seq, int(val))
    except Exception:
        return 1
    return max_seq + 1


def record_event(
    event_type: str,
    data: dict[str, Any] | None = None,
    *,
    session_id: str | None = None,
    root: Path | None = None,
) -> int:
    """Append a single event to the session's usage journal.
    
    Guaranteed fail-open: returns the sequence number on success, or 0 on error without raising.
    """
    try:
        repo_root = root if root else find_repository_root()
        sid = session_id if session_id else get_active_session_id(repo_root)
        session_file = get_session_file_path(sid, repo_root)

        if not session_file.is_file():
            # If init_session was not called, create file with header
            session_file.parent.mkdir(parents=True, exist_ok=True)
            pref = get_project_ref(repo_root)
            header = (
                f"schema: {SCHEMA_VERSION}\n"
                f"session_id: {sid}\n"
                f"started_at: {_iso_now()}\n"
                f"project_ref: {pref}\n"
                f"runtime_version: {RUNTIME_VERSION}\n\n"
                f"events:\n"
            )
            session_file.write_text(header, encoding="utf-8")

        next_seq = _get_next_sequence_and_offset(session_file)
        event_key = f"e{next_seq:06d}"
        now_iso = _iso_now()

        payload: dict[str, Any] = {
            "seq": next_seq,
            "ts": now_iso,
            "type": event_type,
        }

        if data:
            for k, v in data.items():
                if k not in payload and not PROHIBITED_KEY_PATTERNS.match(k):
                    payload[k] = _sanitize_value(k, v)

        # Encode event payload using encode_toon
        if encode_toon:
            raw_encoded = encode_toon(payload).strip()
        else:
            # Fallback simple TOON serializer
            lines = []
            for k, v in sorted(payload.items()):
                if isinstance(v, bool):
                    lines.append(f"{k}: {'true' if v else 'false'}")
                elif isinstance(v, (int, float)):
                    lines.append(f"{k}: {v}")
                elif isinstance(v, str):
                    lines.append(f'{k}: "{v}"')
                else:
                    lines.append(f"{k}: {v}")
            raw_encoded = "\n".join(lines)

        # Indent event key by 2 spaces, and body by 4 spaces
        indented_body = "\n".join(f"    {line}" for line in raw_encoded.splitlines())
        event_chunk = f"  {event_key}:\n{indented_body}\n"

        # Append atomically to session file
        with open(session_file, "a", encoding="utf-8") as f:
            if fcntl:
                with contextlib.suppress(Exception):
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(event_chunk)
            f.flush()
            if fcntl:
                with contextlib.suppress(Exception):
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        # Record unified telemetry event fail-open for skill.end
        if event_type == "skill.end":
            with contextlib.suppress(Exception):
                import ai_sdlc_telemetry
                t_skill = data.get("skill", "unknown") if data else "unknown"
                t_status = data.get("status", "success") if data else "success"
                t_dur = data.get("duration_ms") if data else None
                t_task = None
                if data and (data.get("feature") or data.get("task_id")):
                    t_task = {
                        "id": str(data.get("feature") or data.get("task_id", "")),
                        "type": str(data.get("task_kind", "feature")),
                        "title": str(data.get("title", "")),
                        "owner": str(data.get("owner", "")),
                    }
                t_models = data.get("models") if data else None
                t_usage = data.get("usage_available") if data else None
                ai_sdlc_telemetry.record_telemetry_event(
                    skill=t_skill,
                    status=t_status,
                    duration_ms=t_dur,
                    task=t_task,
                    models=t_models,
                    usage_available=t_usage,
                    root=repo_root,
                )

        return next_seq
    except Exception:
        # Strict fail-open contract: do not break caller under any circumstances
        return 0


def format_duration_ms(ms: int | float | None) -> str:
    """Format milliseconds into a human-readable duration string."""
    if ms is None or ms < 0:
        return "0s"
    total_sec = ms / 1000.0
    if total_sec < 1.0:
        return f"{int(ms)}ms"
    if total_sec < 60.0:
        return f"{total_sec:.1f}s"
    minutes = int(total_sec // 60)
    seconds = total_sec % 60
    if minutes < 60:
        return f"{minutes}m {seconds:.1f}s"
    hours = int(minutes // 60)
    minutes = minutes % 60
    return f"{hours}h {minutes}m {int(seconds)}s"


def record_skill_start(
    skill: str,
    *,
    trigger: str = "user",
    phase: str | None = None,
    task_kind: str | None = None,
    feature: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
    **kwargs: Any,
) -> int:
    """Record a skill.start event in the session usage journal."""
    payload = {
        "skill": skill,
        "trigger": trigger,
        "phase": phase,
        "task_kind": task_kind,
        "feature": feature,
        **kwargs,
    }
    return record_event(
        "skill.start",
        {k: v for k, v in payload.items() if v is not None},
        session_id=session_id,
        root=root,
    )


def record_skill_end(
    skill: str,
    *,
    status: str = "completed",
    duration_ms: int | None = None,
    start_time: float | None = None,
    feature: str | None = None,
    task_kind: str | None = None,
    phase: str | None = None,
    artifacts: Any = None,
    session_id: str | None = None,
    root: Path | None = None,
    **kwargs: Any,
) -> int:
    """Record a skill.end event with duration in milliseconds."""
    calc_duration = duration_ms
    if calc_duration is None and start_time is not None:
        calc_duration = max(1, int((time.perf_counter() - start_time) * 1000))

    payload = {
        "skill": skill,
        "status": status,
        "duration_ms": calc_duration,
        "feature": feature,
        "task_kind": task_kind,
        "phase": phase,
        "artifacts": artifacts,
        **kwargs,
    }
    return record_event(
        "skill.end",
        {k: v for k, v in payload.items() if v is not None},
        session_id=session_id,
        root=root,
    )


@contextlib.contextmanager
def track_skill(
    skill: str,
    *,
    trigger: str = "user",
    phase: str | None = None,
    task_kind: str | None = None,
    feature: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
    **kwargs: Any,
):
    """Context manager to automatically time and record skill execution fail-open."""
    start_mono = time.perf_counter()
    try:
        record_skill_start(
            skill,
            trigger=trigger,
            phase=phase,
            task_kind=task_kind,
            feature=feature,
            session_id=session_id,
            root=root,
            **kwargs,
        )
    except Exception:
        pass
    status = "completed"
    try:
        yield
    except KeyboardInterrupt:
        status = "abandoned"
        raise
    except SystemExit as exc:
        status = "completed" if exc.code in (0, None) else "failed"
        raise
    except Exception:
        status = "failed"
        raise
    finally:
        duration_ms = max(1, int((time.perf_counter() - start_mono) * 1000))
        rec_ok = False
        try:
            seq = record_skill_end(
                skill,
                status=status,
                duration_ms=duration_ms,
                phase=phase,
                task_kind=task_kind,
                feature=feature,
                session_id=session_id,
                root=root,
                **kwargs,
            )
            rec_ok = bool(seq > 0)
        except Exception:
            pass
        if not rec_ok:
            with contextlib.suppress(Exception):
                import ai_sdlc_telemetry
                t_task = None
                if feature:
                    t_task = {"id": str(feature), "type": str(task_kind or "skill"), "title": "", "owner": ""}
                ai_sdlc_telemetry.record_telemetry_event(
                    skill=skill,
                    status=status,
                    duration_ms=duration_ms,
                    task=t_task,
                    root=root,
                )


def record_task_start(
    task_id: str,
    *,
    feature: str | None = None,
    task_kind: str | None = None,
    title: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
    **kwargs: Any,
) -> int:
    """Record the start of a logical task or feature lifecycle."""
    payload = {
        "task_id": task_id,
        "feature": feature or task_id,
        "task_kind": task_kind,
        "title": title,
        **kwargs,
    }
    return record_event(
        "task.start",
        {k: v for k, v in payload.items() if v is not None},
        session_id=session_id,
        root=root,
    )


def record_task_end(
    task_id: str,
    *,
    status: str = "completed",
    duration_ms: int | None = None,
    start_time: float | None = None,
    feature: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
    **kwargs: Any,
) -> int:
    """Record the completion or closure of a logical task."""
    calc_duration = duration_ms
    if calc_duration is None and start_time is not None:
        calc_duration = max(1, int((time.perf_counter() - start_time) * 1000))

    payload = {
        "task_id": task_id,
        "feature": feature or task_id,
        "status": status,
        "duration_ms": calc_duration,
        **kwargs,
    }
    return record_event(
        "task.end",
        {k: v for k, v in payload.items() if v is not None},
        session_id=session_id,
        root=root,
    )


@contextlib.contextmanager
def track_task(
    task_id: str,
    *,
    feature: str | None = None,
    task_kind: str | None = None,
    title: str | None = None,
    session_id: str | None = None,
    root: Path | None = None,
    **kwargs: Any,
):
    """Context manager to track whole task execution duration and status."""
    start_mono = time.perf_counter()
    record_task_start(
        task_id,
        feature=feature,
        task_kind=task_kind,
        title=title,
        session_id=session_id,
        root=root,
        **kwargs,
    )
    status = "completed"
    try:
        yield
    except KeyboardInterrupt:
        status = "abandoned"
        raise
    except Exception:
        status = "failed"
        raise
    finally:
        duration_ms = max(1, int((time.perf_counter() - start_mono) * 1000))
        record_task_end(
            task_id,
            status=status,
            duration_ms=duration_ms,
            feature=feature,
            session_id=session_id,
            root=root,
            **kwargs,
        )


def scan_sessions(
    root: Path | None = None,
    *,
    limit: int | None = None,
    since_days: int | None = None,
    session_id: str | None = None,
) -> list[dict[str, Any]]:
    """Scan and parse session journal files on-demand.
    
    Skips corrupted files safely.
    """
    sessions: list[dict[str, Any]] = []
    try:
        repo_root = root if root else find_repository_root()
        candidate_dirs = [
            repo_root / ".ai-sdlc" / "usage" / "sessions",
            repo_root / ".ai-sdlc-loop" / "usage" / "sessions",
        ]
        now = _now_utc()
        session_files: list[Path] = []
        for usage_dir in candidate_dirs:
            if not usage_dir.is_dir():
                continue
            for date_dir in sorted(usage_dir.iterdir()):
                if date_dir.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}$", date_dir.name):
                    if since_days is not None:
                        try:
                            dir_date = datetime.date.fromisoformat(date_dir.name)
                            diff = (now.date() - dir_date).days
                            if diff > since_days:
                                continue
                        except Exception:
                            pass
                    for sfile in sorted(date_dir.glob("*.toon")):
                        if session_id:
                            if sfile.stem == session_id:
                                session_files.append(sfile)
                        else:
                            session_files.append(sfile)

        for sfile in session_files:
            try:
                content = sfile.read_text(encoding="utf-8", errors="replace")
                if decode_toon:
                    parsed = decode_toon(content)
                    if isinstance(parsed, dict) and "events" in parsed:
                        sessions.append(parsed)
            except Exception:
                # Corrupted files are safely ignored
                continue

        if limit is not None and limit > 0:
            sessions = sessions[-limit:]

    except Exception:
        pass

    return sessions


def derive_signals(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """Derive behavioral patterns, graphs, and friction motifs from session histories.
    
    Never invents facts. Derives strictly from journaled events.
    """
    total_events = 0
    all_events: list[dict[str, Any]] = []

    skill_coverage: dict[str, dict[str, Any]] = {}
    discoverability: dict[str, dict[str, int]] = {}
    transitions: dict[str, int] = {}
    rework_cycles: list[dict[str, Any]] = []
    gate_timings: list[dict[str, Any]] = []
    evidence_lags: list[dict[str, Any]] = []
    decision_churn: dict[str, int] = {}
    context_switches: list[dict[str, Any]] = []
    ignored_recommendations: list[dict[str, Any]] = []
    capability_gaps: list[dict[str, Any]] = []
    task_durations: dict[str, dict[str, Any]] = {}
    skill_durations: dict[str, dict[str, Any]] = {}

    for session in sessions:
        sid = session.get("session_id", "unknown")
        events_dict = session.get("events", {})
        if not isinstance(events_dict, dict):
            continue

        # Sort events by sequence
        s_events: list[dict[str, Any]] = []
        for ekey, edata in events_dict.items():
            if isinstance(edata, dict):
                edata["_session_id"] = sid
                edata["_key"] = ekey
                s_events.append(edata)
        s_events.sort(key=lambda x: int(x.get("seq", 0)))

        total_events += len(s_events)
        all_events.extend(s_events)

        # Track session-specific sequence for motif detection
        session_skills: list[str] = []
        pending_implement_step: int | None = None
        pending_implement_time: str | None = None
        active_features: set[str] = set()
        active_task_kinds: set[str] = set()
        last_recommended_skill: str | None = None
        last_recommendation_seq: int | None = None

        for idx, ev in enumerate(s_events):
            etype = ev.get("type", "")
            ts = ev.get("ts", "")
            skill = ev.get("skill") or ev.get("current_skill")
            trigger = ev.get("trigger", "unspecified")
            status = ev.get("status")
            task_kind = ev.get("task_kind")
            phase = ev.get("phase")

            if task_kind:
                active_task_kinds.add(task_kind)
            feature = ev.get("feature") or ev.get("project_ref")
            if feature:
                active_features.add(str(feature))

            # 5.1 Skill Coverage & 5.2 Discoverability
            if etype == "skill.start" and skill:
                session_skills.append(skill)
                cov = skill_coverage.setdefault(
                    skill,
                    {
                        "count": 0,
                        "last_used": ts,
                        "phases": {},
                        "task_kinds": {},
                        "triggers": {},
                        "statuses": {"completed": 0, "failed": 0, "blocked": 0, "retried": 0},
                    },
                )
                cov["count"] += 1
                cov["last_used"] = max(cov["last_used"], ts)
                if phase:
                    cov["phases"][phase] = cov["phases"].get(phase, 0) + 1
                if task_kind:
                    cov["task_kinds"][task_kind] = cov["task_kinds"].get(task_kind, 0) + 1
                cov["triggers"][trigger] = cov["triggers"].get(trigger, 0) + 1

                disc = discoverability.setdefault(
                    skill,
                    {"user": 0, "handoff": 0, "router": 0, "coach": 0, "recovery": 0, "other": 0},
                )
                if trigger in disc:
                    disc[trigger] += 1
                else:
                    disc["other"] += 1

                # Check if an earlier coach recommendation was ignored
                if last_recommended_skill:
                    if skill != last_recommended_skill:
                        ignored_recommendations.append(
                            {
                                "session_id": sid,
                                "recommended": last_recommended_skill,
                                "selected": skill,
                                "seq": ev.get("seq"),
                            }
                        )
                    last_recommended_skill = None

                # Track implementation steps for gate timing and lag
                if "implement" in skill:
                    pending_implement_step = idx
                    pending_implement_time = ts

            elif etype == "skill.end" and skill:
                if skill in skill_coverage:
                    cov = skill_coverage[skill]
                    if status in cov["statuses"]:
                        cov["statuses"][status] += 1
                    if ev.get("retry"):
                        cov["statuses"]["retried"] += 1

                # Missing capability detection (blocked status with manual work needed)
                if status == "blocked" and ev.get("reason"):
                    capability_gaps.append(
                        {
                            "session_id": sid,
                            "skill": skill,
                            "reason": ev.get("reason"),
                            "seq": ev.get("seq"),
                        }
                    )

                # Duration tracking
                dur = ev.get("duration_ms")
                if dur is not None and isinstance(dur, (int, float)):
                    d_ms = int(dur)
                    if d_ms >= 0:
                        sd = skill_durations.setdefault(
                            skill,
                            {
                                "total_ms": 0,
                                "count": 0,
                                "min_ms": d_ms,
                                "max_ms": d_ms,
                                "avg_ms": 0,
                                "formatted_total": "0s",
                                "formatted_avg": "0s",
                            },
                        )
                        sd["total_ms"] += d_ms
                        sd["count"] += 1
                        sd["min_ms"] = min(sd["min_ms"], d_ms)
                        sd["max_ms"] = max(sd["max_ms"], d_ms)
                        sd["avg_ms"] = int(sd["total_ms"] / sd["count"])
                        sd["formatted_total"] = format_duration_ms(sd["total_ms"])
                        sd["formatted_avg"] = format_duration_ms(sd["avg_ms"])

                        task_ref = ev.get("task_id") or ev.get("feature") or (list(active_features)[0] if active_features else None)
                        if task_ref:
                            t_key = str(task_ref)
                            td = task_durations.setdefault(
                                t_key,
                                {
                                    "task_id": t_key,
                                    "total_ms": 0,
                                    "formatted_total": "0s",
                                    "skills": {},
                                    "events_count": 0,
                                    "first_ts": ts,
                                    "last_ts": ts,
                                },
                            )
                            td["total_ms"] += d_ms
                            td["formatted_total"] = format_duration_ms(td["total_ms"])
                            td["events_count"] += 1
                            if ts:
                                td["last_ts"] = max(td.get("last_ts", ""), ts)
                            sk_entry = td["skills"].setdefault(skill, {"total_ms": 0, "count": 0, "formatted": "0s"})
                            sk_entry["total_ms"] += d_ms
                            sk_entry["count"] += 1
                            sk_entry["formatted"] = format_duration_ms(sk_entry["total_ms"])

            # Task level lifecycle events
            if etype in ("task.start", "task.end"):
                t_ref = ev.get("task_id") or ev.get("feature")
                if t_ref:
                    t_key = str(t_ref)
                    td = task_durations.setdefault(
                        t_key,
                        {
                            "task_id": t_key,
                            "total_ms": 0,
                            "formatted_total": "0s",
                            "skills": {},
                            "events_count": 0,
                            "first_ts": ts,
                            "last_ts": ts,
                        },
                    )
                    td["events_count"] += 1
                    dur = ev.get("duration_ms")
                    if dur is not None and isinstance(dur, (int, float)):
                        d_ms = int(dur)
                        if d_ms > 0 and td["total_ms"] == 0:
                            td["total_ms"] = d_ms
                            td["formatted_total"] = format_duration_ms(d_ms)

            # 5.3 Sequence Graph & Transitions
            if etype == "workflow.transition":
                prev = ev.get("previous_skill")
                curr = ev.get("current_skill")
                if prev and curr:
                    t_key = f"{prev} -> {curr}"
                    transitions[t_key] = transitions.get(t_key, 0) + 1

            # 5.5 Gate Timing & 5.6 Evidence Lag
            if etype in ("quality_gate.executed", "verification.executed") or (
                skill and ("gate" in skill or "verify" in skill) and etype == "skill.start"
            ):
                if pending_implement_step is not None:
                    steps_since_impl = idx - pending_implement_step
                    gate_timings.append(
                        {
                            "session_id": sid,
                            "steps_lag": steps_since_impl,
                            "gate_type": etype,
                            "impl_ts": pending_implement_time,
                            "gate_ts": ts,
                        }
                    )
                    if etype in ("verification.passed", "evidence.persisted") or (
                        ev.get("passed") is True
                    ):
                        evidence_lags.append(
                            {
                                "session_id": sid,
                                "steps": steps_since_impl,
                                "seq": ev.get("seq"),
                            }
                        )
                        pending_implement_step = None

            # 5.7 Decision Churn
            if etype in ("artifact.updated", "artifact.validated") and ev.get("artifact_ref"):
                aref = str(ev.get("artifact_ref"))
                decision_churn[aref] = decision_churn.get(aref, 0) + 1

            # Recommendation observation
            if etype == "coach.suggest":
                last_recommended_skill = ev.get("suggested_skill")
                last_recommendation_seq = ev.get("seq")

            # 5.10 Manual Override detection
            if etype == "user.override":
                capability_gaps.append(
                    {
                        "session_id": sid,
                        "action": "user.override",
                        "override_target": ev.get("override_target"),
                        "reason": ev.get("reason", "manual intervention"),
                        "seq": ev.get("seq"),
                    }
                )

        # 5.4 Rework / Loop detection in session skills sequence
        # Detect patterns A -> B -> A
        if len(session_skills) >= 3:
            for i in range(len(session_skills) - 2):
                if session_skills[i] == session_skills[i + 2] and session_skills[i] != session_skills[i + 1]:
                    cycle_key = f"{session_skills[i]} -> {session_skills[i+1]} -> {session_skills[i]}"
                    rework_cycles.append(
                        {
                            "session_id": sid,
                            "pattern": cycle_key,
                            "start_step": i,
                        }
                    )
        # Also detect implement -> gate -> implement -> gate
        if len(session_skills) >= 4:
            for i in range(len(session_skills) - 3):
                if (
                    session_skills[i] == session_skills[i + 2]
                    and session_skills[i + 1] == session_skills[i + 3]
                ):
                    cycle_key = f"{session_skills[i]} -> {session_skills[i+1]} -> {session_skills[i]} -> {session_skills[i+1]}"
                    rework_cycles.append(
                        {
                            "session_id": sid,
                            "pattern": cycle_key,
                            "start_step": i,
                        }
                    )

        # 5.8 Context switching: multiple tasks/features in one session
        if len(active_task_kinds) > 1:
            context_switches.append(
                {
                    "session_id": sid,
                    "task_kinds": sorted(list(active_task_kinds)),
                    "features": sorted(list(active_features)),
                }
            )

    # Compute rework time loss from skill durations in rework cycles
    total_rework_ms = 0
    for cycle in rework_cycles:
        patt = cycle.get("pattern", "")
        # Sum avg durations of participating skills
        for sk in patt.split(" -> "):
            if sk in skill_durations:
                total_rework_ms += skill_durations[sk].get("avg_ms", 0)

    time_analytics = {
        "task_durations": task_durations,
        "skill_durations": skill_durations,
        "rework_time_loss": {
            "total_rework_ms": total_rework_ms,
            "formatted_rework": format_duration_ms(total_rework_ms),
            "cycles_count": len(rework_cycles),
        },
    }

    return {
        "summary": {
            "total_sessions": len(sessions),
            "total_events": total_events,
            "scanned_at": _iso_now(),
        },
        "skill_coverage": skill_coverage,
        "discoverability": discoverability,
        "transitions": transitions,
        "rework_cycles": rework_cycles,
        "gate_timings": gate_timings,
        "evidence_lags": evidence_lags,
        "decision_churn": decision_churn,
        "context_switches": context_switches,
        "ignored_recommendations": ignored_recommendations,
        "capability_gaps": capability_gaps,
        "time_analytics": time_analytics,
    }
