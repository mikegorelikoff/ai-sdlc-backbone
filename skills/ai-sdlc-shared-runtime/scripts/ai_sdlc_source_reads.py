"""Bounded source reuse during one read-only routing decision.

Never cache across Apply, command execution, or separate calls. Stat identity is
checked on every reuse; content hashes and mandatory-anchor validation remain
unchanged. This is an I/O optimization, not an evidence authority.
"""
from contextvars import ContextVar
from functools import wraps
from pathlib import Path

_scope = ContextVar("ai_sdlc_source_reads", default=None)


def source_scope(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        if _scope.get() is not None:
            return function(*args, **kwargs)
        token = _scope.set({"files": {}, "bytes": 0, "reads": 0, "hits": 0})
        try:
            return function(*args, **kwargs)
        finally:
            _scope.reset(token)
    return wrapped


def read_bytes(path: Path) -> bytes:
    scope = _scope.get()
    if scope is None:
        return path.read_bytes()
    stat = path.stat()
    identity = (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
    key = str(path.absolute())
    cached = scope["files"].get(key)
    if cached and cached[0] == identity:
        scope["hits"] += 1
        return cached[1]
    value = path.read_bytes()
    scope["reads"] += 1
    # Keep routing memory bounded even in unusually large repositories.
    if len(value) <= 262144 and scope["bytes"] + len(value) <= 16 * 1024 * 1024:
        scope["files"][key] = (identity, value)
        scope["bytes"] += len(value)
    return value


def read_text(path: Path) -> str:
    return read_bytes(path).decode("utf-8")


def metrics() -> dict:
    scope = _scope.get()
    return {key: scope[key] for key in ("bytes", "reads", "hits")} if scope else {}
