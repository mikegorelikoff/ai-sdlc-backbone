#!/usr/bin/env python3
"""Build and query a deterministic local repository context cache."""

from __future__ import annotations

import argparse
import copy
import hashlib
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unicodedata
from collections import defaultdict, deque
from dataclasses import asdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from ai_sdlc_step_context import (  # noqa: E402
    SCHEMA as PACK_SCHEMA,
    digest as pack_digest,
    token_estimate,
    validate_step_context_pack,
)
from ai_sdlc_steps import load_manifest  # noqa: E402
from ai_sdlc_toon import decode_toon, encode_toon  # noqa: E402


DB_SCHEMA = "ai-sdlc-context-cache/v1"
RECEIPT_SCHEMA = "ai-sdlc-context-cache-receipt/v1"
QUERY_SCHEMA = "ai-sdlc-context-query/v1"
ERROR_SCHEMA = "ai-sdlc-context-cache-error/v1"
BENCHMARK_CASES_SCHEMA = "ai-sdlc-context-cache-benchmark-cases/v1"
BENCHMARK_SCHEMA = "ai-sdlc-context-cache-benchmark/v1"
DEFAULT_CACHE = ".ai-sdlc/cache/context-cache.sqlite3"
MAX_FILE_BYTES = 262_144
MAX_FILES = 20_000
CHUNK_LINES = 60
CHUNK_OVERLAP = 8
MAX_QUERY_TERMS = 32
TEXT_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt",
    ".md", ".php", ".py", ".rb", ".rs", ".sh", ".sql", ".swift",
    ".toml", ".toon", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}
TEXT_NAMES = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "Makefile"}
IGNORED_PARTS = {
    ".git", ".venv", "__pycache__", "build", "dist", "node_modules", "site",
    "vendor", ".mypy_cache", ".pytest_cache",
}
SECRET_NAME = re.compile(
    r"(?:^|[._-])(?:secret|token|credential|password|private[-_]?key)(?:[._-]|$)",
    re.IGNORECASE,
)
CREDENTIAL_CONTENT = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[:=]\s*[\"']?[A-Za-z0-9+/_.-]{16,}"
)
TRACE_ID = re.compile(r"\b(?:AC|TC|FR|NFR|REQ|DEC|T)-?\d{1,5}\b", re.IGNORECASE)
IMPORT_LINE = re.compile(
    r"^\s*(?:from\s+([A-Za-z0-9_.]+)\s+import|import\s+([A-Za-z0-9_.]+)|"
    r"(?:use|require)\s*\(?[\"']([^\"']+)[\"']|#include\s*[<\"]([^>\"]+))",
    re.MULTILINE,
)
PATH_REFERENCE = re.compile(
    r"(?<![A-Za-z0-9_.-])([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.[A-Za-z0-9]+)"
)
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{1,63}")
STOPWORDS = {
    "about", "after", "also", "and", "before", "build", "context", "for",
    "from", "have", "into", "local", "more", "only", "query", "repository",
    "that", "the", "this", "use", "using", "with",
}
EDGE_KINDS = {"same-document", "trace-id", "import", "path-reference"}


class CacheError(RuntimeError):
    """Raised for bounded cache contract failures."""


def canonical(value: object) -> str:
    return encode_toon(value)


def digest(value: object) -> str:
    if not isinstance(value, str):
        value = canonical(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def resolve_root(value: Path) -> Path:
    root = value.resolve()
    if not root.is_dir() or root.is_symlink():
        raise CacheError("repository root must be a regular directory")
    return root


def resolve_cache(root: Path, value: Path | None) -> Path:
    root = root.resolve()
    candidate = value or Path(DEFAULT_CACHE)
    if not candidate.is_absolute():
        candidate = root / candidate
    if candidate.suffix != ".sqlite3":
        raise CacheError("cache path must end with .sqlite3")
    if candidate.is_symlink():
        raise CacheError("cache path must not be a symbolic link")
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise CacheError("cache path escapes the repository root") from exc
    if resolved == root:
        raise CacheError("cache path must not be the repository root")
    return resolved


def safe_relative(relative: str) -> bool:
    path = PurePosixPath(relative)
    return (
        bool(relative)
        and not path.is_absolute()
        and ".." not in path.parts
        and "\\" not in relative
        and not set(path.parts) & IGNORED_PARTS
        and not relative.startswith(".ai-sdlc/cache/")
        and not SECRET_NAME.search(relative)
        and (path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES)
    )


def discover(root: Path) -> list[str]:
    root = root.resolve()
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        candidates = result.stdout.splitlines()
    else:
        candidates = [
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        ]
    return sorted({item for item in candidates if safe_relative(item)})[:MAX_FILES]


def read_source(root: Path, relative: str) -> tuple[str | None, str | None, str]:
    root = root.resolve()
    if not safe_relative(relative):
        return None, "unsafe-or-secret-path", ""
    path = root / relative
    if path.is_symlink():
        return None, "symlink", ""
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None, "missing-or-path-escape", ""
    if not resolved.is_file():
        return None, "not-regular-file", ""
    try:
        data = resolved.read_bytes()
    except OSError:
        return None, "unreadable", ""
    source_hash = hashlib.sha256(data).hexdigest()
    if len(data) > MAX_FILE_BYTES:
        return None, "oversized", source_hash
    if b"\0" in data:
        return None, "binary", source_hash
    text = data.decode("utf-8", errors="replace")
    if CREDENTIAL_CONTENT.search(text):
        return None, "credential-like-content", source_hash
    return text, None, source_hash


def authority(relative: str) -> str:
    """Keep every cache-derived repository range below instruction authority."""
    return "evidence_only"


def heading_for(lines: list[str], start: int) -> str:
    for index in range(start, -1, -1):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", lines[index])
        if match:
            return match.group(1)[:160]
    return ""


def chunks_for(relative: str, text: str, source_hash: str) -> list[dict[str, Any]]:
    lines = text.splitlines(keepends=True)
    if not lines:
        lines = [""]
    chunks: list[dict[str, Any]] = []
    start = 0
    ordinal = 0
    while start < len(lines):
        end = min(len(lines), start + CHUNK_LINES)
        content = "".join(lines[start:end])
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        chunk_id = digest(
            {
                "content": content_hash,
                "end_line": end,
                "path": relative,
                "start_line": start + 1,
            }
        )
        traces = sorted({match.upper().replace("T-", "T") for match in TRACE_ID.findall(content)})
        chunks.append(
            {
                "id": chunk_id,
                "path": relative,
                "ordinal": ordinal,
                "start_line": start + 1,
                "end_line": end,
                "sha256": content_hash,
                "source_sha256": source_hash,
                "estimated_tokens": token_estimate(content),
                "heading": heading_for(lines, start),
                "trace_ids": traces,
                "content": content,
            }
        )
        if end == len(lines):
            break
        start = end - CHUNK_OVERLAP
        ordinal += 1
    return chunks


def normalize_terms(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).lower()
    terms = {
        token.replace("_", "-").strip("-")
        for token in WORD.findall(normalized)
        if token.lower() not in STOPWORDS
    }
    return sorted(term for term in terms if len(term) >= 2)[:MAX_QUERY_TERMS]


def initialize(connection: sqlite3.Connection) -> None:
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA journal_mode=DELETE")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS documents (
            path TEXT PRIMARY KEY,
            sha256 TEXT NOT NULL,
            byte_size INTEGER NOT NULL,
            line_count INTEGER NOT NULL,
            authority TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            path TEXT NOT NULL REFERENCES documents(path) ON DELETE CASCADE,
            ordinal INTEGER NOT NULL,
            start_line INTEGER NOT NULL,
            end_line INTEGER NOT NULL,
            sha256 TEXT NOT NULL,
            source_sha256 TEXT NOT NULL,
            estimated_tokens INTEGER NOT NULL,
            heading TEXT NOT NULL,
            trace_ids TEXT NOT NULL,
            content TEXT NOT NULL,
            UNIQUE(path, ordinal)
        );
        CREATE TABLE IF NOT EXISTS edges (
            source_chunk TEXT NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
            target_chunk TEXT NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            label TEXT NOT NULL,
            PRIMARY KEY(source_chunk, target_chunk, kind, label)
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
            chunk_id UNINDEXED, content, heading, path, trace_ids,
            tokenize='unicode61 remove_diacritics 2'
        );
        """
    )


def metadata(connection: sqlite3.Connection) -> dict[str, str]:
    return {str(row[0]): str(row[1]) for row in connection.execute("SELECT key, value FROM metadata ORDER BY key")}


def set_metadata(connection: sqlite3.Connection, key: str, value: str) -> None:
    connection.execute(
        "INSERT INTO metadata(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def semantic_rows(connection: sqlite3.Connection) -> dict[str, object]:
    return {
        "documents": [list(row) for row in connection.execute(
            "SELECT path, sha256, byte_size, line_count, authority FROM documents ORDER BY path"
        )],
        "chunks": [list(row) for row in connection.execute(
            "SELECT id, path, ordinal, start_line, end_line, sha256, source_sha256, estimated_tokens, heading, trace_ids FROM chunks ORDER BY path, ordinal"
        )],
        "edges": [list(row) for row in connection.execute(
            "SELECT source_chunk, target_chunk, kind, label FROM edges ORDER BY source_chunk, target_chunk, kind, label"
        )],
    }


def config_fingerprint() -> str:
    return digest(
        {
            "chunk_lines": CHUNK_LINES,
            "chunk_overlap": CHUNK_OVERLAP,
            "db_schema": DB_SCHEMA,
            "max_file_bytes": MAX_FILE_BYTES,
            "text_suffixes": sorted(TEXT_SUFFIXES),
        }
    )


def rebuild_edges(connection: sqlite3.Connection) -> None:
    connection.execute("DELETE FROM edges")
    rows = [
        {
            "id": row[0], "path": row[1], "ordinal": row[2], "content": row[3],
            "trace_ids": row[4].split() if row[4] else [],
        }
        for row in connection.execute(
            "SELECT id, path, ordinal, content, trace_ids FROM chunks ORDER BY path, ordinal"
        )
    ]
    by_path: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_trace: dict[str, list[str]] = defaultdict(list)
    path_first: dict[str, str] = {}
    stem_paths: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        by_path[row["path"]].append(row)
        path_first.setdefault(row["path"], row["id"])
        stem_paths[Path(row["path"]).stem.lower()].append(row["path"])
        for trace in row["trace_ids"]:
            by_trace[trace].append(row["id"])

    edges: set[tuple[str, str, str, str]] = set()
    for path, items in sorted(by_path.items()):
        for left, right in zip(items, items[1:]):
            edges.add((left["id"], right["id"], "same-document", path))
            edges.add((right["id"], left["id"], "same-document", path))
    for trace, ids in sorted(by_trace.items()):
        ordered = sorted(set(ids))[:64]
        for source in ordered:
            for target in ordered:
                if source != target:
                    edges.add((source, target, "trace-id", trace))
    known_paths = set(path_first)
    for row in rows:
        targets: set[tuple[str, str]] = set()
        for match in IMPORT_LINE.finditer(row["content"]):
            raw = next((value for value in match.groups() if value), "")
            stem = Path(raw.replace(".", "/")).stem.lower()
            for path in stem_paths.get(stem, []):
                if path != row["path"]:
                    targets.add((path, raw))
        for raw in PATH_REFERENCE.findall(row["content"]):
            normalized = PurePosixPath(raw).as_posix()
            if normalized in known_paths and normalized != row["path"]:
                targets.add((normalized, raw))
        for target_path, label in sorted(targets):
            kind = "path-reference" if "/" in label else "import"
            edges.add((row["id"], path_first[target_path], kind, label[:160]))
    connection.executemany(
        "INSERT INTO edges(source_chunk, target_chunk, kind, label) VALUES(?, ?, ?, ?)",
        sorted(edges),
    )


def build(root: Path, cache: Path, rebuild: bool = False) -> dict[str, object]:
    root = root.resolve()
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.parent.is_symlink():
        raise CacheError("cache parent must not be a symbolic link")
    descriptor, temporary_name = tempfile.mkstemp(prefix=".context-cache-", suffix=".sqlite3", dir=cache.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        if cache.is_file() and not rebuild:
            shutil.copy2(cache, temporary)
        connection = sqlite3.connect(temporary)
        try:
            initialize(connection)
            current_meta = metadata(connection)
            if current_meta and (
                current_meta.get("schema") != DB_SCHEMA
                or current_meta.get("config_fingerprint") != config_fingerprint()
            ):
                raise CacheError("cache schema or configuration is incompatible; use --rebuild")
            existing = {
                str(row[0]): str(row[1])
                for row in connection.execute("SELECT path, sha256 FROM documents ORDER BY path")
            }
            discovered = discover(root)
            accepted: dict[str, tuple[str, str]] = {}
            excluded: list[str] = []
            for relative in discovered:
                text, error, source_hash = read_source(root, relative)
                if error or text is None:
                    excluded.append(f"{relative}:{error or 'unreadable'}")
                    continue
                accepted[relative] = (text, source_hash)

            removed = sorted(set(existing) - set(accepted))
            changed = sorted(
                relative for relative, (_text, source_hash) in accepted.items()
                if existing.get(relative) != source_hash
            )
            unchanged = sorted(set(accepted) - set(changed))
            with connection:
                for relative in removed + changed:
                    old_ids = [row[0] for row in connection.execute("SELECT id FROM chunks WHERE path=?", (relative,))]
                    if old_ids:
                        connection.executemany("DELETE FROM chunk_fts WHERE chunk_id=?", [(value,) for value in old_ids])
                    connection.execute("DELETE FROM documents WHERE path=?", (relative,))
                for relative in changed:
                    text, source_hash = accepted[relative]
                    connection.execute(
                        "INSERT INTO documents(path, sha256, byte_size, line_count, authority) VALUES(?, ?, ?, ?, ?)",
                        (
                            relative,
                            source_hash,
                            len(text.encode("utf-8")),
                            len(text.splitlines()),
                            authority(relative),
                        ),
                    )
                    for item in chunks_for(relative, text, source_hash):
                        trace_text = " ".join(item["trace_ids"])
                        connection.execute(
                            "INSERT INTO chunks(id, path, ordinal, start_line, end_line, sha256, source_sha256, estimated_tokens, heading, trace_ids, content) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                item["id"], item["path"], item["ordinal"], item["start_line"],
                                item["end_line"], item["sha256"], item["source_sha256"],
                                item["estimated_tokens"], item["heading"], trace_text, item["content"],
                            ),
                        )
                        connection.execute(
                            "INSERT INTO chunk_fts(chunk_id, content, heading, path, trace_ids) VALUES(?, ?, ?, ?, ?)",
                            (item["id"], item["content"], item["heading"], item["path"], trace_text),
                        )
                rebuild_edges(connection)
                logical = semantic_rows(connection)
                cache_fingerprint = digest(logical)
                repository_fingerprint = digest(logical["documents"])
                set_metadata(connection, "schema", DB_SCHEMA)
                set_metadata(connection, "config_fingerprint", config_fingerprint())
                set_metadata(connection, "cache_fingerprint", cache_fingerprint)
                set_metadata(connection, "repository_fingerprint", repository_fingerprint)
            connection.execute("PRAGMA optimize")
        finally:
            connection.close()
        os.replace(temporary, cache)
    finally:
        if temporary.exists():
            temporary.unlink()
    counts = inspect_counts(cache)
    return receipt(
        "build",
        "ready",
        "fresh deterministic index built",
        True,
        cache_fingerprint,
        repository_fingerprint,
        {
            **counts,
            "changed": len(changed),
            "discovered": len(discovered),
            "excluded": len(excluded),
            "removed": len(removed),
            "unchanged": len(unchanged),
        },
    )


def open_cache(cache: Path) -> sqlite3.Connection:
    if not cache.is_file() or cache.is_symlink():
        raise CacheError("context cache is missing")
    try:
        connection = sqlite3.connect(f"file:{cache}?mode=ro", uri=True)
        current = metadata(connection)
    except sqlite3.Error as exc:
        raise CacheError(f"context cache is corrupt or unreadable: {exc}") from exc
    if current.get("schema") != DB_SCHEMA or current.get("config_fingerprint") != config_fingerprint():
        connection.close()
        raise CacheError("context cache is incompatible")
    return connection


def inspect_counts(cache: Path) -> dict[str, int]:
    connection = open_cache(cache)
    try:
        return {
            "chunks": int(connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]),
            "documents": int(connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]),
            "edges": int(connection.execute("SELECT COUNT(*) FROM edges").fetchone()[0]),
        }
    finally:
        connection.close()


def freshness(root: Path, connection: sqlite3.Connection) -> tuple[bool, list[str], list[str]]:
    root = root.resolve()
    indexed = {
        str(relative): str(claimed)
        for relative, claimed in connection.execute(
            "SELECT path, sha256 FROM documents ORDER BY path"
        )
    }
    current: dict[str, str] = {}
    for relative in discover(root):
        text, error, actual = read_source(root, relative)
        if not error and text is not None:
            current[relative] = actual
    stale: list[str] = []
    for relative, claimed in sorted(indexed.items()):
        actual = current.get(relative)
        if actual is None:
            stale.append(f"{relative}:missing-or-excluded")
        elif actual != claimed:
            stale.append(f"{relative}:hash-mismatch")
    stale.extend(
        f"{relative}:unindexed"
        for relative in sorted(set(current) - set(indexed))
    )
    return not stale, stale, sorted(current)


def receipt(
    command: str,
    status: str,
    reason: str,
    fresh: bool,
    cache_fingerprint: str,
    repository_fingerprint: str,
    counts: dict[str, int],
) -> dict[str, object]:
    return {
        "schema": RECEIPT_SCHEMA,
        "command": command,
        "status": status,
        "reason": reason,
        "fresh": fresh,
        "cache_fingerprint": cache_fingerprint,
        "repository_fingerprint": repository_fingerprint,
        "counts": counts,
    }


def inspect(root: Path, cache: Path, command: str = "inspect") -> dict[str, object]:
    connection = open_cache(cache)
    try:
        current = metadata(connection)
        fresh, stale, _paths = freshness(root, connection)
        reason = "all indexed source hashes match" if fresh else "; ".join(stale[:16])
        return receipt(
            command,
            "ready" if fresh else "stale",
            reason,
            fresh,
            current["cache_fingerprint"],
            current["repository_fingerprint"],
            {
                "chunks": int(connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]),
                "documents": int(connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]),
                "edges": int(connection.execute("SELECT COUNT(*) FROM edges").fetchone()[0]),
                "stale": len(stale),
            },
        )
    finally:
        connection.close()


def row_for(connection: sqlite3.Connection, chunk_id: str) -> dict[str, Any]:
    row = connection.execute(
        "SELECT id, path, start_line, end_line, source_sha256, estimated_tokens, heading, trace_ids, content FROM chunks WHERE id=?",
        (chunk_id,),
    ).fetchone()
    if row is None:
        raise CacheError("cache edge references a missing chunk")
    return {
        "chunk_id": row[0], "path": row[1], "start_line": row[2], "end_line": row[3],
        "source_sha256": row[4], "estimated_tokens": row[5], "heading": row[6],
        "trace_ids": row[7].split() if row[7] else [], "content": row[8],
    }


def lexical_candidates(connection: sqlite3.Connection, terms: list[str], cap: int) -> list[str]:
    expression = " OR ".join(f'"{term}"' for term in terms)
    try:
        return [
            str(row[0])
            for row in connection.execute(
                "SELECT chunk_id FROM chunk_fts WHERE chunk_fts MATCH ? ORDER BY chunk_id LIMIT ?",
                (expression, cap),
            )
        ]
    except sqlite3.Error as exc:
        raise CacheError(f"FTS5 query failed: {exc}") from exc


def score_row(row: dict[str, Any], terms: list[str]) -> tuple[int, list[str]]:
    content = row["content"].lower()
    heading = row["heading"].lower()
    path = row["path"].lower()
    matched = [term for term in terms if term in content or term in heading or term in path]
    score = sum(content.count(term) * 100 for term in matched)
    score += sum(250 for term in matched if term in heading)
    score += sum(180 for term in matched if term in path)
    score += len(set(row["trace_ids"]) & {term.upper() for term in terms}) * 300
    return score, matched


def query(
    root: Path,
    cache: Path,
    query_text: str,
    limit: int,
    graph_depth: int,
    graph_limit: int,
) -> dict[str, object]:
    if not 1 <= limit <= 100:
        raise CacheError("limit must be between 1 and 100")
    if not 0 <= graph_depth <= 4:
        raise CacheError("graph depth must be between 0 and 4")
    if not 1 <= graph_limit <= 500:
        raise CacheError("graph limit must be between 1 and 500")
    terms = normalize_terms(query_text)
    if not terms:
        return query_receipt(query_text, terms, "direct_read", "query has no indexable terms", False, "", [], [], [])
    connection = open_cache(cache)
    try:
        current = metadata(connection)
        fresh, stale, indexed_paths = freshness(root, connection)
        if not fresh:
            return query_receipt(
                query_text, terms, "direct_read", "; ".join(stale[:16]), False,
                current["cache_fingerprint"], [], indexed_paths[:limit], stale,
            )
        seed_ids = lexical_candidates(connection, terms, max(limit * 8, 64))
        rows: dict[str, dict[str, Any]] = {}
        best: dict[str, tuple[int, int, list[dict[str, str]]]] = {}
        queue: deque[tuple[str, int, list[dict[str, str]]]] = deque()
        for chunk_id in seed_ids:
            row = row_for(connection, chunk_id)
            rows[chunk_id] = row
            base, matched = score_row(row, terms)
            if base <= 0:
                continue
            row["matched_terms"] = matched
            best[chunk_id] = (base, 0, [])
            queue.append((chunk_id, 0, []))
        visited = set(seed_ids)
        expanded = 0
        while queue and expanded < graph_limit:
            source, distance, path_edges = queue.popleft()
            if distance >= graph_depth:
                continue
            neighbors = connection.execute(
                "SELECT target_chunk, kind, label FROM edges WHERE source_chunk=? ORDER BY kind, label, target_chunk",
                (source,),
            ).fetchall()
            for target, kind, label in neighbors:
                if kind not in EDGE_KINDS or expanded >= graph_limit:
                    continue
                expanded += 1
                next_path = path_edges + [{"kind": str(kind), "label": str(label), "from": source}]
                target_row = rows.setdefault(str(target), row_for(connection, str(target)))
                lexical, matched = score_row(target_row, terms)
                target_row["matched_terms"] = matched
                seed_score = best[source][0]
                propagated = max(1, seed_score // (2 + distance))
                candidate = (max(lexical, propagated), distance + 1, next_path)
                previous = best.get(str(target))
                if previous is None or (candidate[0], -candidate[1], canonical(candidate[2])) > (previous[0], -previous[1], canonical(previous[2])):
                    best[str(target)] = candidate
                if target not in visited:
                    visited.add(str(target))
                    queue.append((str(target), distance + 1, next_path))

        ordered = sorted(
            best,
            key=lambda chunk_id: (
                -best[chunk_id][0], best[chunk_id][1], rows[chunk_id]["path"],
                rows[chunk_id]["start_line"], chunk_id,
            ),
        )[:limit]
        results: list[dict[str, object]] = []
        for chunk_id in ordered:
            row = rows[chunk_id]
            score, distance, graph_path = best[chunk_id]
            results.append(
                {
                    "chunk_id": chunk_id,
                    "path": row["path"],
                    "start_line": row["start_line"],
                    "end_line": row["end_line"],
                    "sha256": row["source_sha256"],
                    "authority": authority(row["path"]),
                    "estimated_tokens": row["estimated_tokens"],
                    "score": score,
                    "distance": distance,
                    "matched_terms": row.get("matched_terms", []),
                    "graph_path": graph_path,
                    "content": row["content"],
                }
            )
        if not results:
            return query_receipt(
                query_text, terms, "direct_read", "no fresh cache result matched",
                True, current["cache_fingerprint"], [], indexed_paths[:limit], [],
            )
        return query_receipt(
            query_text, terms, "cached", "fresh lexical and bounded graph evidence matched",
            True, current["cache_fingerprint"], results, [], [],
        )
    finally:
        connection.close()


def query_receipt(
    query_text: str,
    terms: list[str],
    strategy: str,
    reason: str,
    fresh: bool,
    cache_fingerprint: str,
    results: list[dict[str, object]],
    direct_paths: list[str],
    skipped: list[str],
) -> dict[str, object]:
    semantic: dict[str, object] = {
        "schema": QUERY_SCHEMA,
        "query": query_text,
        "terms": terms,
        "strategy": strategy,
        "reason": reason,
        "fresh": fresh,
        "cache_fingerprint": cache_fingerprint,
        "results": results,
        "direct_read_paths": sorted(set(direct_paths)),
        "skipped": sorted(set(skipped)),
    }
    semantic["fingerprint"] = digest(semantic)
    return semantic


def mandatory_step_range(
    root: Path,
    skill: str,
    step_id: str,
    terms: list[str],
) -> tuple[dict[str, object], list[str]]:
    """Resolve the owning step document and its declared critical anchors."""
    try:
        skill_root, manifest = load_manifest(root, skill)
    except ValueError as exc:
        raise CacheError(str(exc)) from exc
    steps = manifest.get("steps", [])
    step = next(
        (
            item
            for item in steps
            if isinstance(item, dict) and item.get("id") == step_id
        ),
        None,
    )
    if step is None:
        raise CacheError(f"owning skill has no step {step_id!r}")
    relative = str(step["path"])
    resolved = (skill_root / relative).resolve()
    try:
        resolved.relative_to(skill_root)
    except ValueError as exc:
        raise CacheError("owning step document escapes its skill root") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise CacheError("owning step document is unavailable")
    text = resolved.read_text(encoding="utf-8")
    context = step.get("context")
    if not isinstance(context, dict):
        raise CacheError("owning step context contract is invalid")
    anchors = [str(value) for value in context.get("critical_anchors", [])]
    return (
        {
            "path": f"{skill}/{relative}",
            "sha256": hashlib.sha256(resolved.read_bytes()).hexdigest(),
            "authority": "skill_instruction",
            "start_line": 1,
            "end_line": len(text.splitlines()),
            "estimated_tokens": token_estimate(text),
            "strategy": "mandatory-step-document",
            "reasons": ["mandatory:step-document"],
            "matched_terms": [term for term in terms if term in text.lower()],
            "content": text,
        },
        anchors,
    )


def pack(
    root: Path,
    cache: Path,
    query_text: str,
    skill: str,
    step_id: str,
    budget_tokens: int,
    limit: int,
    graph_depth: int,
    graph_limit: int,
) -> dict[str, object]:
    if budget_tokens < 64:
        raise CacheError("budget tokens must be at least 64")
    result = query(root, cache, query_text, limit, graph_depth, graph_limit)
    candidates = list(result["results"])
    step_range, critical = mandatory_step_range(
        root, skill, step_id, list(result.get("terms", []))
    )
    selected: list[dict[str, object]] = [step_range]
    skipped = list(result.get("skipped", []))
    seen_paths: set[str] = {str(step_range["path"])}
    used = int(step_range["estimated_tokens"])
    raw = used + sum(int(item["estimated_tokens"]) for item in candidates)
    for item in candidates:
        path = str(item["path"])
        tokens = int(item["estimated_tokens"])
        if path in seen_paths:
            skipped.append(f"{path}:duplicate-path")
            continue
        if used + tokens > budget_tokens:
            skipped.append(f"{path}:budget-exhausted")
            continue
        selected.append(
            {
                "path": path,
                "sha256": item["sha256"],
                "authority": item["authority"],
                "start_line": item["start_line"],
                "end_line": item["end_line"],
                "estimated_tokens": tokens,
                "strategy": "lexical-range",
                "reasons": [
                    f"cache-score:{item['score']}",
                    f"graph-distance:{item['distance']}",
                ],
                "matched_terms": item["matched_terms"],
                "content": item["content"],
            }
        )
        seen_paths.add(path)
        used += tokens
    mandatory_content = str(step_range["content"])
    retained = sum(1 for anchor in critical if anchor in mandatory_content)
    recall = round((retained / len(critical) * 100.0) if critical else 100.0, 2)
    missing = [anchor for anchor in critical if anchor not in mandatory_content]
    savings = round(((raw - used) / raw * 100.0) if raw else 0.0, 2)
    within_budget = used <= budget_tokens
    cache_usable = result["strategy"] == "cached" and len(selected) > 1
    economic = savings >= 15.0 and within_budget
    sufficient = not missing and bool(mandatory_content)
    strategy = "packed" if cache_usable and economic and sufficient else "direct_read"
    direct_paths = [] if strategy == "packed" else [str(item["path"]) for item in selected]
    reason_parts = [str(result["reason"])]
    if savings < 15.0:
        reason_parts.append(f"net savings {savings:.2f}% are below 15.00%")
    if len(selected) == 1:
        reason_parts.append("no cache range fits the context budget")
    if missing:
        reason_parts.append("missing critical anchors: " + ", ".join(missing))
    if not within_budget:
        reason_parts.append(
            f"packed context {used} exceeds budget {budget_tokens}"
        )
    semantic: dict[str, object] = {
        "schema": PACK_SCHEMA,
        "skill": skill,
        "step_id": step_id,
        "budget_tokens": budget_tokens,
        "raw_tokens": raw,
        "packed_tokens": used,
        "savings_percent": savings,
        "critical_total": len(critical),
        "critical_retained": retained,
        "critical_recall_percent": recall,
        "sufficient": sufficient,
        "strategy": strategy,
        "reason": "; ".join(reason_parts),
        "selected": selected,
        "skipped": sorted(set(skipped)),
        "direct_read_paths": direct_paths,
    }
    semantic["fingerprint"] = pack_digest(copy.deepcopy(semantic))
    validate_step_context_pack(
        semantic,
        expected_skill=skill,
        expected_step_id=step_id,
    )
    return semantic


def percentage(found: int, total: int) -> float:
    return round((found / total * 100.0) if total else 100.0, 2)


def load_benchmark_cases(path: Path) -> list[dict[str, object]]:
    """Load and strictly validate deterministic golden cases from TOON."""
    if path.is_symlink() or not path.is_file():
        raise CacheError("benchmark cases must be a regular TOON file")
    try:
        value = decode_toon(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CacheError(f"cannot decode benchmark cases: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "cases"}:
        raise CacheError("benchmark cases must contain only schema and cases")
    if value.get("schema") != BENCHMARK_CASES_SCHEMA:
        raise CacheError(f"benchmark cases schema must be {BENCHMARK_CASES_SCHEMA}")
    cases = value.get("cases")
    required = {
        "id", "query", "expected_paths", "expected_anchors", "skill",
        "step_id", "budget_tokens", "expected_strategy",
    }
    if not isinstance(cases, list) or not cases:
        raise CacheError("benchmark cases must be a non-empty array")
    identifiers: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or set(case) != required:
            raise CacheError(f"benchmark case {index + 1} fields are invalid")
        if not all(isinstance(case[field], str) and case[field] for field in ("id", "query", "skill", "step_id")):
            raise CacheError(f"benchmark case {index + 1} text fields are invalid")
        identifiers.append(str(case["id"]))
        for field in ("expected_paths", "expected_anchors"):
            items = case[field]
            if not isinstance(items, list) or not items or not all(isinstance(item, str) and item for item in items):
                raise CacheError(f"benchmark case {index + 1} {field} is invalid")
        budget = case["budget_tokens"]
        if not isinstance(budget, int) or isinstance(budget, bool) or budget < 64:
            raise CacheError(f"benchmark case {index + 1} budget_tokens is invalid")
        if case["expected_strategy"] not in {"packed", "direct_read"}:
            raise CacheError(f"benchmark case {index + 1} expected_strategy is invalid")
    if len(identifiers) != len(set(identifiers)):
        raise CacheError("benchmark case IDs must be unique")
    return cases


def benchmark(
    root: Path,
    cache: Path,
    cases_path: Path,
    limit: int,
    graph_depth: int,
    graph_limit: int,
) -> dict[str, object]:
    """Compare lexical, graph-enhanced, and packed retrieval deterministically."""
    cases = load_benchmark_cases(cases_path)
    results: list[dict[str, object]] = []
    for case in cases:
        query_text = str(case["query"])
        expected_paths = sorted(set(str(value) for value in case["expected_paths"]))
        expected_anchors = sorted(set(str(value) for value in case["expected_anchors"]))
        lexical = query(root, cache, query_text, limit, 0, graph_limit)
        graph = query(root, cache, query_text, limit, graph_depth, graph_limit)
        packed = pack(
            root,
            cache,
            query_text,
            str(case["skill"]),
            str(case["step_id"]),
            int(case["budget_tokens"]),
            limit,
            graph_depth,
            graph_limit,
        )
        lexical_paths = {str(item["path"]) for item in lexical["results"]}
        graph_paths = {str(item["path"]) for item in graph["results"]}
        selected_content = "\n".join(str(item["content"]) for item in packed["selected"])
        lexical_found = len(set(expected_paths) & lexical_paths)
        graph_found = len(set(expected_paths) & graph_paths)
        anchors_found = sum(1 for anchor in expected_anchors if anchor in selected_content)
        expected_strategy = str(case["expected_strategy"])
        passed = (
            percentage(graph_found, len(expected_paths)) == 100.0
            and percentage(anchors_found, len(expected_anchors)) == 100.0
            and float(packed["critical_recall_percent"]) == 100.0
            and packed["strategy"] == expected_strategy
            and (expected_strategy != "packed" or float(packed["savings_percent"]) >= 15.0)
        )
        results.append(
            {
                "id": case["id"],
                "status": "passed" if passed else "failed",
                "expected_strategy": expected_strategy,
                "actual_strategy": packed["strategy"],
                "lexical_recall_percent": percentage(lexical_found, len(expected_paths)),
                "graph_recall_percent": percentage(graph_found, len(expected_paths)),
                "expected_anchor_recall_percent": percentage(anchors_found, len(expected_anchors)),
                "critical_anchor_recall_percent": packed["critical_recall_percent"],
                "savings_percent": packed["savings_percent"],
                "lexical_fingerprint": lexical["fingerprint"],
                "graph_fingerprint": graph["fingerprint"],
                "pack_fingerprint": packed["fingerprint"],
            }
        )
    semantic: dict[str, object] = {
        "schema": BENCHMARK_SCHEMA,
        "status": "passed" if all(item["status"] == "passed" for item in results) else "failed",
        "case_count": len(results),
        "passed_count": sum(1 for item in results if item["status"] == "passed"),
        "latency_measurement": "separate-observational-tier",
        "cases": results,
    }
    semantic["fingerprint"] = digest(semantic)
    return semantic


def purge(root: Path, cache: Path) -> dict[str, object]:
    root = root.resolve()
    cache = cache.resolve(strict=False)
    try:
        relative = cache.relative_to(root)
    except ValueError as exc:
        raise CacheError("purge target escapes the repository") from exc
    if cache.suffix != ".sqlite3" or cache.is_symlink() or ".." in relative.parts:
        raise CacheError("purge target is unsafe")
    removed = 0
    for target in (cache, Path(str(cache) + "-wal"), Path(str(cache) + "-shm")):
        if target.is_symlink():
            raise CacheError("purge target sidecar must not be a symbolic link")
        if target.exists():
            if not target.is_file():
                raise CacheError("purge target must be a regular file")
            target.unlink()
            removed += 1
    return receipt("purge", "removed", "project-local cache state removed", False, "", "", {"removed": removed})


def error_receipt(command: str, message: str) -> dict[str, object]:
    semantic: dict[str, object] = {
        "schema": ERROR_SCHEMA,
        "command": command,
        "status": "error",
        "reason": message[:500],
        "strategy": "direct_read",
    }
    semantic["fingerprint"] = digest(semantic)
    return semantic


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--quick-flow", action="store_true")
    cli.add_argument("--full-flow", action="store_true")
    cli.add_argument("--feature", default="<feature-name>")
    cli.add_argument("--state-check", action="store_true")
    cli.add_argument("--begin-state", action="store_true")
    cli.add_argument("--complete-state", action="store_true")
    cli.add_argument("--decision-ref")
    cli.add_argument("--assumption")
    cli.add_argument("--state-workspace", choices=("refinement", "implementation"))
    commands = cli.add_subparsers(dest="command", required=True)
    for name in ("build", "query", "pack", "benchmark", "inspect", "verify", "purge"):
        child = commands.add_parser(name)
        child.add_argument("--root", type=Path, default=Path.cwd())
        child.add_argument("--cache", type=Path)
        if name in {"query", "pack"}:
            child.add_argument("--query", required=True)
            child.add_argument("--limit", type=int, default=12)
            child.add_argument("--graph-depth", type=int, default=1)
            child.add_argument("--graph-limit", type=int, default=64)
        if name == "pack":
            child.add_argument("--skill", required=True)
            child.add_argument("--step-id", required=True)
            child.add_argument("--budget-tokens", type=int, default=4000)
        if name == "benchmark":
            child.add_argument("--cases", type=Path, required=True)
            child.add_argument("--limit", type=int, default=12)
            child.add_argument("--graph-depth", type=int, default=1)
            child.add_argument("--graph-limit", type=int, default=64)
        if name == "build":
            child.add_argument("--rebuild", action="store_true")
    return cli


def main() -> int:
    args = parser().parse_args()
    if args.begin_state or args.complete_state:
        print("context-cache: lifecycle mutation is not supported by this optional utility", file=sys.stderr)
        return 2
    try:
        root = resolve_root(args.root)
        cache = resolve_cache(root, args.cache)
        if args.command == "build":
            output = build(root, cache, args.rebuild)
        elif args.command == "query":
            output = query(root, cache, args.query, args.limit, args.graph_depth, args.graph_limit)
        elif args.command == "pack":
            output = pack(
                root, cache, args.query, args.skill, args.step_id, args.budget_tokens,
                args.limit, args.graph_depth, args.graph_limit,
            )
        elif args.command == "benchmark":
            output = benchmark(
                root, cache, args.cases, args.limit, args.graph_depth,
                args.graph_limit,
            )
        elif args.command in {"inspect", "verify"}:
            output = inspect(root, cache, args.command)
        elif args.command == "purge":
            output = purge(root, cache)
        else:
            raise CacheError("unknown command")
    except (CacheError, OSError, sqlite3.Error, ValueError) as exc:
        print(encode_toon(error_receipt(args.command, str(exc))), end="")
        print(f"context-cache: {str(exc)[:500]}", file=sys.stderr)
        return 1
    print(encode_toon(output), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
