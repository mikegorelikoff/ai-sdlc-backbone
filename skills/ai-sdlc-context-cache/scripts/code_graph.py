#!/usr/bin/env python3
"""Deterministic Tree-sitter code graph primitives for the local context cache."""

from __future__ import annotations

import hashlib
import importlib.metadata
import os
import re
import socket
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))
from ai_sdlc_toon import decode_toon, encode_toon  # noqa: E402


GRAPH_SCHEMA = "ai-sdlc-code-graph/v1"
PREFLIGHT_SCHEMA = "ai-sdlc-code-graph-preflight/v1"
STATS_SCHEMA = "ai-sdlc-code-graph-stats/v1"
TREE_SITTER_VERSION = "0.25.2"
GRAMMAR_PACKAGES: dict[str, tuple[str, str, str, str]] = {
    "typescript": ("tree-sitter-typescript", "0.23.2", "tree_sitter_typescript", "language_typescript"),
    "python": ("tree-sitter-python", "0.25.0", "tree_sitter_python", "language"),
    "javascript": ("tree-sitter-javascript", "0.25.0", "tree_sitter_javascript", "language"),
    "java": ("tree-sitter-java", "0.23.5", "tree_sitter_java", "language"),
    "csharp": ("tree-sitter-c-sharp", "0.23.5", "tree_sitter_c_sharp", "language"),
    "php": ("tree-sitter-php", "0.24.1", "tree_sitter_php", "language_php"),
    "shell": ("tree-sitter-bash", "0.25.1", "tree_sitter_bash", "language"),
    "cpp": ("tree-sitter-cpp", "0.23.4", "tree_sitter_cpp", "language"),
    "go": ("tree-sitter-go", "0.25.0", "tree_sitter_go", "language"),
    "rust": ("tree-sitter-rust", "0.24.2", "tree_sitter_rust", "language"),
    "kotlin": ("tree-sitter-kotlin", "1.1.0", "tree_sitter_kotlin", "language"),
    "swift": ("tree-sitter-swift", "0.7.3", "tree_sitter_swift", "language"),
}

LANGUAGE_SUFFIXES: dict[str, tuple[str, ...]] = {
    "typescript": (".ts", ".tsx"),
    "python": (".py",),
    "javascript": (".js", ".jsx"),
    "java": (".java",),
    "csharp": (".cs",),
    "php": (".php",),
    "shell": (".sh",),
    "cpp": (".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"),
    "go": (".go",),
    "rust": (".rs",),
    "kotlin": (".kt", ".kts"),
    "swift": (".swift",),
}
GRAMMAR_KEYS = {language: ("bash" if language == "shell" else language) for language in LANGUAGE_SUFFIXES}
SUFFIX_LANGUAGE = {
    suffix: language
    for language, suffixes in LANGUAGE_SUFFIXES.items()
    for suffix in suffixes
}

SYMBOL_KINDS: dict[str, dict[str, str]] = {
    "typescript": {"function_declaration": "function", "class_declaration": "class", "method_definition": "method", "interface_declaration": "interface", "enum_declaration": "enum", "type_alias_declaration": "type"},
    "javascript": {"function_declaration": "function", "class_declaration": "class", "method_definition": "method", "generator_function_declaration": "function"},
    "python": {"function_definition": "function", "class_definition": "class"},
    "java": {"class_declaration": "class", "interface_declaration": "interface", "enum_declaration": "enum", "record_declaration": "record", "method_declaration": "method", "constructor_declaration": "constructor"},
    "csharp": {"class_declaration": "class", "interface_declaration": "interface", "struct_declaration": "struct", "enum_declaration": "enum", "record_declaration": "record", "method_declaration": "method", "constructor_declaration": "constructor"},
    "php": {"function_definition": "function", "method_declaration": "method", "class_declaration": "class", "interface_declaration": "interface", "trait_declaration": "trait", "enum_declaration": "enum"},
    "shell": {"function_definition": "function"},
    "cpp": {"function_definition": "function", "class_specifier": "class", "struct_specifier": "struct", "enum_specifier": "enum", "namespace_definition": "namespace"},
    "go": {"function_declaration": "function", "method_declaration": "method", "type_declaration": "type"},
    "rust": {"function_item": "function", "struct_item": "struct", "enum_item": "enum", "trait_item": "trait", "impl_item": "impl", "mod_item": "module", "type_item": "type"},
    "kotlin": {"function_declaration": "function", "class_declaration": "class", "object_declaration": "object", "type_alias": "type"},
    "swift": {"function_declaration": "function", "class_declaration": "class", "protocol_declaration": "protocol", "struct_declaration": "struct", "enum_declaration": "enum", "actor_declaration": "actor", "typealias_declaration": "type"},
}
CALL_TYPES = {
    "call", "call_expression", "function_call", "invocation_expression",
    "command", "method_invocation", "object_creation_expression",
    "function_call_expression",
}
IMPORT_TYPES = {
    "import_statement", "import_declaration", "import_directive", "using_directive",
    "use_declaration", "include_directive", "require_expression", "package_clause",
    "import", "import_header", "namespace_use_declaration", "source_command",
    "preproc_include",
}
IDENTIFIER_TYPES = {
    "identifier", "simple_identifier", "type_identifier", "field_identifier",
    "property_identifier", "namespace_identifier", "constant", "name", "word",
}
MAX_AST_NODES_PER_FILE = 200_000
MAX_AST_DEPTH = 512
MAX_SYMBOLS_PER_FILE = 20_000
MAX_OCCURRENCES_PER_FILE = 100_000
MAX_EDGES_PER_KIND = 250_000
MAX_TOTAL_EDGES = 1_000_000
TRACE_HUB_MEMBERS = 2_048
PARSE_TIMEOUT_SECONDS = 8
LOCK_SCHEMA = "ai-sdlc-code-graph-parser-lock/v1"


class GraphError(RuntimeError):
    """A code graph could not meet its completeness or bounds contract."""


def _hash(parts: Iterable[object]) -> str:
    value = "\x1f".join(str(part) for part in parts)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def language_for_path(relative: str) -> str | None:
    return SUFFIX_LANGUAGE.get(Path(relative).suffix.lower())


def parser_lock_errors(value: object) -> list[str]:
    """Reject partial or drifted parser locks before trusting wheel hashes."""
    if not isinstance(value, dict) or value.get("schema") != LOCK_SCHEMA:
        return ["invalid-parser-lock-schema"]
    errors: list[str] = []
    runtime = value.get("runtime")
    if not isinstance(runtime, dict) or runtime.get("name") != "tree-sitter" or runtime.get("version") != TREE_SITTER_VERSION:
        errors.append("invalid-parser-runtime")
    grammar_rows = value.get("grammars")
    observed_grammars: dict[str, tuple[str, str, object]] = {}
    if isinstance(grammar_rows, list):
        for row in grammar_rows:
            if isinstance(row, dict) and isinstance(row.get("language"), str):
                language = str(row["language"])
                if language in observed_grammars:
                    errors.append(f"duplicate-grammar:{language}")
                observed_grammars[language] = (
                    str(row.get("package", "")), str(row.get("version", "")),
                    row.get("required"),
                )
    expected_grammars = {
        language: (package, version, True)
        for language, (package, version, _module, _function) in GRAMMAR_PACKAGES.items()
    }
    if observed_grammars != expected_grammars:
        errors.append("incomplete-or-drifted-grammar-lock")
    wheel_rows = value.get("wheels")
    observed_wheels: list[str] = []
    if isinstance(wheel_rows, list):
        for row in wheel_rows:
            if not isinstance(row, dict):
                errors.append("invalid-wheel-row")
                continue
            name = str(row.get("name", ""))
            filename = str(row.get("filename", ""))
            digest_value = str(row.get("sha256", ""))
            observed_wheels.append(name)
            if not filename or Path(filename).name != filename:
                errors.append(f"invalid-wheel-filename:{name}")
            if not re.fullmatch(r"[0-9a-f]{64}", digest_value):
                errors.append(f"invalid-wheel-hash:{name}")
    expected_wheels = {"tree-sitter", *(row[0] for row in GRAMMAR_PACKAGES.values())}
    if len(observed_wheels) != len(set(observed_wheels)) or set(observed_wheels) != expected_wheels:
        errors.append("incomplete-or-duplicate-wheel-lock")
    if value.get("runtime_download_allowed") is not False or value.get("portable_format") != "toon":
        errors.append("invalid-parser-lock-policy")
    return sorted(set(errors))


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return ""


def _get_parser(language: str, path: str = "") -> Any:
    from tree_sitter import Language, Parser
    _package, _version, module_name, function_name = GRAMMAR_PACKAGES[language]
    if language == "typescript" and Path(path).suffix.lower() == ".tsx":
        function_name = "language_tsx"
    module = __import__(module_name)
    binding = getattr(module, function_name)()
    return Parser(Language(binding))


def preflight(required_languages: Iterable[str] | None = None) -> dict[str, object]:
    required = sorted(set(required_languages or LANGUAGE_SUFFIXES))
    runtime_version = _package_version("tree-sitter")
    python_supported = (3, 10) <= sys.version_info[:2] <= (3, 14)
    package_versions = {
        language: _package_version(package)
        for language, (package, _version, _module, _function) in GRAMMAR_PACKAGES.items()
    }
    package_ok = runtime_version == TREE_SITTER_VERSION and all(
        package_versions[language] == GRAMMAR_PACKAGES[language][1]
        for language in LANGUAGE_SUFFIXES
    )
    rows: list[dict[str, object]] = []
    loader = None
    loader_error = ""
    if python_supported and package_ok:
        try:
            loader = _get_parser
        except Exception as exc:  # native loader boundary
            loader_error = f"{type(exc).__name__}:{str(exc)[:160]}"
    for language in required:
        grammar = GRAMMAR_KEYS.get(language, "")
        status = "missing"
        reason = loader_error or "parser-runtime-unavailable"
        if language not in LANGUAGE_SUFFIXES:
            reason = "unknown-selected-language"
        elif loader is not None:
            try:
                parser = loader(language)
                tree = parser.parse(b"")
                ready = tree.root_node is not None
                if language == "typescript":
                    ready = ready and loader(language, "fixture.tsx").parse(b"").root_node is not None
                status = "ready" if ready else "missing"
                reason = "pinned-grammar-loaded" if status == "ready" else "empty-root"
            except Exception as exc:  # native parser boundary
                reason = f"{type(exc).__name__}:{str(exc)[:160]}"
        rows.append({"language": language, "grammar": grammar, "status": status, "reason": reason})
    complete = python_supported and package_ok and all(row["status"] == "ready" for row in rows)
    return {
        "schema": PREFLIGHT_SCHEMA,
        "status": "ready" if complete else "unavailable",
        "complete": complete,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_supported": python_supported,
        "runtime_version": runtime_version,
        "expected_runtime_version": TREE_SITTER_VERSION,
        "grammar_packages": [
            {
                "language": language,
                "package": GRAMMAR_PACKAGES[language][0],
                "version": package_versions[language],
                "expected_version": GRAMMAR_PACKAGES[language][1],
            }
            for language in sorted(LANGUAGE_SUFFIXES)
        ],
        "runtime_network": "denied",
        "languages": rows,
    }


@dataclass(frozen=True)
class AstFactSet:
    path: str
    language: str
    source_sha256: str
    root_type: str
    node_count: int
    symbols: tuple[tuple[object, ...], ...]
    occurrences: tuple[tuple[object, ...], ...]
    imports: tuple[tuple[object, ...], ...]
    calls: tuple[tuple[object, ...], ...]


def _text(source: bytes, node: Any, cap: int = 512) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")[:cap]


def _name_node(node: Any) -> Any | None:
    for field in ("name", "declarator", "function", "type"):
        candidate = node.child_by_field_name(field)
        if candidate is not None:
            if candidate.type in IDENTIFIER_TYPES:
                return candidate
            stack = [candidate]
            while stack:
                item = stack.pop(0)
                if item.type in IDENTIFIER_TYPES:
                    return item
                stack[0:0] = list(item.named_children)
    for child in node.named_children:
        if child.type in IDENTIFIER_TYPES:
            return child
    return None


def extract(path: str, text: str, source_sha256: str) -> AstFactSet:
    language = language_for_path(path)
    if language is None:
        raise GraphError(f"unsupported-ast-language:{path}")
    gate = preflight([language])
    if not gate["complete"]:
        raise GraphError(f"parser-preflight-failed:{language}")
    source = text.encode("utf-8")
    tree = _get_parser(language, path).parse(source)
    if tree.root_node.has_error:
        error_nodes: list[Any] = []
        pending = [tree.root_node]
        while pending:
            candidate = pending.pop()
            if candidate.is_error or candidate.is_missing:
                error_nodes.append(candidate)
            pending.extend(candidate.children)
        kotlin_implicit_separators = (
            language == "kotlin"
            and not any(node.is_error for node in error_nodes)
            and all(
                node.is_missing
                and node.type in {"_automatic_semicolon", "_class_member_semi"}
                for node in error_nodes
            )
        )
        if not kotlin_implicit_separators:
            raise GraphError(f"parse-error:{language}:{path}")
    symbols: list[tuple[object, ...]] = []
    occurrences: list[tuple[object, ...]] = []
    imports: list[tuple[object, ...]] = []
    calls: list[tuple[object, ...]] = []
    definition_ranges: set[tuple[int, int]] = set()
    symbol_ordinals: dict[tuple[str, str], int] = defaultdict(int)
    stack: list[tuple[Any, int, tuple[str, ...]]] = [(tree.root_node, 0, ())]
    node_count = 0
    kinds = SYMBOL_KINDS[language]
    while stack:
        node, depth, containers = stack.pop()
        node_count += 1
        if node_count > MAX_AST_NODES_PER_FILE or depth > MAX_AST_DEPTH:
            raise GraphError(f"ast-bound-exceeded:{language}:{path}")
        next_containers = containers
        symbol_kind = kinds.get(node.type)
        if symbol_kind:
            name_node = _name_node(node)
            if name_node is not None:
                name = _text(source, name_node, 240).strip()
                if name:
                    qualified = ".".join((*containers, name))
                    ordinal_key = (symbol_kind, qualified)
                    ordinal = symbol_ordinals[ordinal_key]
                    symbol_ordinals[ordinal_key] += 1
                    symbol_id = _hash((
                        "symbol", path, language, symbol_kind, qualified, ordinal,
                    ))
                    symbols.append((symbol_id, path, language, symbol_kind, name, qualified, node.start_byte, node.end_byte, node.start_point.row + 1, node.end_point.row + 1))
                    definition_ranges.add((name_node.start_byte, name_node.end_byte))
                    occurrences.append((_hash(("occurrence", path, "definition", name_node.start_byte, name_node.end_byte, qualified)), path, symbol_id, "definition", name, qualified, name_node.start_byte, name_node.end_byte, name_node.start_point.row + 1, name_node.end_point.row + 1))
                    next_containers = (*containers, name)
        if node.type in IMPORT_TYPES:
            raw = " ".join(_text(source, node, 1024).split())
            imports.append((_hash(("import", path, node.start_byte, node.end_byte, raw)), path, language, raw, node.start_byte, node.end_byte, node.start_point.row + 1, node.end_point.row + 1))
        elif language == "shell" and node.type == "command":
            raw = " ".join(_text(source, node, 1024).split())
            command_name = raw.split(maxsplit=1)[0] if raw else ""
            if command_name in {"source", "."}:
                imports.append((_hash(("import", path, node.start_byte, node.end_byte, raw)), path, language, raw, node.start_byte, node.end_byte, node.start_point.row + 1, node.end_point.row + 1))
        if node.type in CALL_TYPES:
            name_node = _name_node(node)
            if name_node is not None:
                name = _text(source, name_node, 240).strip()
                if name:
                    calls.append((_hash(("call", path, node.start_byte, node.end_byte, name)), path, language, name, node.start_byte, node.end_byte, node.start_point.row + 1, node.end_point.row + 1))
        if node.type in IDENTIFIER_TYPES and (node.start_byte, node.end_byte) not in definition_ranges:
            name = _text(source, node, 240).strip()
            if name:
                containing = ".".join(containers)
                occurrences.append((_hash(("occurrence", path, "reference", node.start_byte, node.end_byte, name, containing)), path, "", "reference", name, containing, node.start_byte, node.end_byte, node.start_point.row + 1, node.end_point.row + 1))
        for child in reversed(node.named_children):
            stack.append((child, depth + 1, next_containers))
    if len(symbols) > MAX_SYMBOLS_PER_FILE or len(occurrences) > MAX_OCCURRENCES_PER_FILE:
        raise GraphError(f"fact-bound-exceeded:{language}:{path}")
    return AstFactSet(path, language, source_sha256, tree.root_node.type, node_count, tuple(sorted(set(symbols))), tuple(sorted(set(occurrences))), tuple(sorted(set(imports))), tuple(sorted(set(calls))))


def _fact_payload(fact: AstFactSet) -> dict[str, object]:
    return {
        "schema": "ai-sdlc-code-graph-ast-facts/v1",
        "status": "ready",
        "path": fact.path,
        "language": fact.language,
        "source_sha256": fact.source_sha256,
        "root_type": fact.root_type,
        "node_count": fact.node_count,
        "symbols": [list(row) for row in fact.symbols],
        "occurrences": [list(row) for row in fact.occurrences],
        "imports": [list(row) for row in fact.imports],
        "calls": [list(row) for row in fact.calls],
    }


def _parser_environment() -> dict[str, str]:
    """Keep repository parsers isolated from credentials and user import hooks."""
    allowed = ("LANG", "LC_ALL", "SYSTEMROOT", "TEMP", "TMP", "TMPDIR", "WINDIR")
    environment = {key: os.environ[key] for key in allowed if key in os.environ}
    environment.update({
        "AI_SDLC_RUNTIME_NETWORK": "denied",
        "NO_PROXY": "*",
        "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1",
        "no_proxy": "*",
    })
    return environment


def extract_isolated(path: str, text: str, source_sha256: str) -> AstFactSet:
    environment = _parser_environment()
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--extract", path, source_sha256],
            input=text,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=PARSE_TIMEOUT_SECONDS,
            check=False,
            env=environment,
        )
    except subprocess.TimeoutExpired as exc:
        raise GraphError(f"parser-timeout:{language_for_path(path)}:{path}") from exc
    if result.returncode != 0:
        reason = result.stderr.strip()[:240] or f"exit-{result.returncode}"
        raise GraphError(f"parser-process-failed:{language_for_path(path)}:{path}:{reason}")
    try:
        payload = decode_toon(result.stdout)
    except (TypeError, ValueError) as exc:
        raise GraphError(f"parser-output-invalid:{language_for_path(path)}:{path}") from exc
    if not isinstance(payload, dict) or payload.get("status") != "ready":
        raise GraphError(f"parser-output-incomplete:{language_for_path(path)}:{path}")
    return AstFactSet(
        str(payload["path"]), str(payload["language"]), str(payload["source_sha256"]),
        str(payload["root_type"]), int(payload["node_count"]),
        tuple(tuple(row) for row in payload["symbols"]),
        tuple(tuple(row) for row in payload["occurrences"]),
        tuple(tuple(row) for row in payload["imports"]),
        tuple(tuple(row) for row in payload["calls"]),
    )


def initialize(connection: Any) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS code_files (
            id TEXT PRIMARY KEY, path TEXT UNIQUE NOT NULL, language TEXT NOT NULL,
            source_sha256 TEXT NOT NULL, ast_status TEXT NOT NULL, root_type TEXT NOT NULL,
            node_count INTEGER NOT NULL, reason TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS symbols (
            id TEXT PRIMARY KEY, path TEXT NOT NULL, language TEXT NOT NULL, kind TEXT NOT NULL,
            name TEXT NOT NULL, qualified_name TEXT NOT NULL, start_byte INTEGER NOT NULL,
            end_byte INTEGER NOT NULL, start_line INTEGER NOT NULL, end_line INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS occurrences (
            id TEXT PRIMARY KEY, path TEXT NOT NULL, symbol_id TEXT NOT NULL, role TEXT NOT NULL,
            name TEXT NOT NULL, container TEXT NOT NULL, start_byte INTEGER NOT NULL,
            end_byte INTEGER NOT NULL, start_line INTEGER NOT NULL, end_line INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS ast_imports (
            id TEXT PRIMARY KEY, path TEXT NOT NULL, language TEXT NOT NULL, raw TEXT NOT NULL,
            start_byte INTEGER NOT NULL, end_byte INTEGER NOT NULL,
            start_line INTEGER NOT NULL, end_line INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS ast_calls (
            id TEXT PRIMARY KEY, path TEXT NOT NULL, language TEXT NOT NULL, name TEXT NOT NULL,
            start_byte INTEGER NOT NULL, end_byte INTEGER NOT NULL,
            start_line INTEGER NOT NULL, end_line INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS graph_nodes (
            id TEXT PRIMARY KEY, kind TEXT NOT NULL, path TEXT NOT NULL, label TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS graph_edges (
            source_id TEXT NOT NULL, target_id TEXT NOT NULL, kind TEXT NOT NULL,
            label TEXT NOT NULL, evidence_path TEXT NOT NULL,
            PRIMARY KEY(source_id, target_id, kind, label, evidence_path)
        );
        CREATE TABLE IF NOT EXISTS graph_exclusions (
            path TEXT PRIMARY KEY, reason TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS language_coverage (
            language TEXT PRIMARY KEY, files INTEGER NOT NULL, parsed INTEGER NOT NULL,
            errors INTEGER NOT NULL, grammar_status TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS symbols_name_idx ON symbols(name, qualified_name, path);
        CREATE INDEX IF NOT EXISTS occurrences_name_idx ON occurrences(name, path, start_byte);
        CREATE INDEX IF NOT EXISTS graph_edges_source_idx ON graph_edges(source_id, kind, target_id);
        """
    )


def rebuild(connection: Any, accepted: dict[str, tuple[str, str]], excluded: Iterable[str]) -> dict[str, object]:
    initialize(connection)
    for table in ("code_files", "symbols", "occurrences", "ast_imports", "ast_calls", "graph_nodes", "graph_edges", "graph_exclusions", "language_coverage"):
        connection.execute(f"DELETE FROM {table}")
    for item in sorted(excluded):
        path, _, reason = item.partition(":")
        connection.execute("INSERT OR REPLACE INTO graph_exclusions(path, reason) VALUES(?, ?)", (path, reason or "excluded"))
    selected = {path: value for path, value in accepted.items() if language_for_path(path)}
    required_languages = sorted({language_for_path(path) for path in selected if language_for_path(path)})
    gate = preflight(required_languages)
    errors: list[str] = []
    facts: list[AstFactSet] = []
    grammar_status = {str(row["language"]): str(row["status"]) for row in gate["languages"]}
    file_ids = {path: _hash(("file", path)) for path in accepted}
    for path in sorted(accepted):
        connection.execute(
            "INSERT INTO graph_nodes VALUES(?, ?, ?, ?)",
            (file_ids[path], "file", path, path),
        )
    for path, (text, source_sha256) in sorted(selected.items()):
        language = language_for_path(path)
        assert language is not None
        file_id = file_ids[path]
        try:
            fact = extract_isolated(path, text, source_sha256)
            facts.append(fact)
            connection.execute("INSERT INTO code_files VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (file_id, path, language, source_sha256, "parsed", fact.root_type, fact.node_count, ""))
        except GraphError as exc:
            reason = str(exc)[:240]
            errors.append(f"{path}:{reason}")
            connection.execute("INSERT INTO code_files VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (file_id, path, language, source_sha256, "error", "", 0, reason))
    by_name: dict[str, list[str]] = defaultdict(list)
    edges: set[tuple[str, str, str, str, str]] = set()
    trace_members: dict[str, list[str]] = defaultdict(list)
    for chunk_id, path, ordinal, trace_text in connection.execute(
        "SELECT id, path, ordinal, trace_ids FROM chunks ORDER BY path, ordinal"
    ):
        connection.execute(
            "INSERT INTO graph_nodes VALUES(?, ?, ?, ?)",
            (str(chunk_id), "chunk", str(path), f"{path}:{ordinal}"),
        )
        if str(path) in file_ids:
            edges.add((file_ids[str(path)], str(chunk_id), "contains", "chunk", str(path)))
        for trace in str(trace_text).split():
            trace_members[trace].append(str(chunk_id))
    for trace, members in sorted(trace_members.items()):
        hub_id = _hash(("trace-hub", trace))
        connection.execute("INSERT INTO graph_nodes VALUES(?, ?, ?, ?)", (hub_id, "trace-hub", "", trace))
        for chunk_id in sorted(set(members))[:TRACE_HUB_MEMBERS]:
            evidence_path = str(connection.execute("SELECT path FROM chunks WHERE id=?", (chunk_id,)).fetchone()[0])
            edges.add((chunk_id, hub_id, "spec-trace", trace, evidence_path))
    for source, target, kind, label in connection.execute(
        "SELECT source_chunk, target_chunk, kind, label FROM edges "
        "WHERE kind != 'trace-id' ORDER BY source_chunk, target_chunk, kind, label"
    ):
        evidence = connection.execute("SELECT path FROM chunks WHERE id=?", (source,)).fetchone()
        graph_kind = "adjacent" if str(kind) == "same-document" else str(kind)
        edges.add((str(source), str(target), graph_kind, str(label)[:160], str(evidence[0]) if evidence else ""))
    for fact in facts:
        file_id = file_ids[fact.path]
        for symbol in fact.symbols:
            connection.execute("INSERT INTO symbols VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", symbol)
            symbol_id, path, _language, kind, name, qualified, *_ = symbol
            connection.execute("INSERT INTO graph_nodes VALUES(?, ?, ?, ?)", (symbol_id, "symbol", path, qualified))
            by_name[str(name)].append(str(symbol_id))
            edges.add((file_id, str(symbol_id), "defines", str(kind), str(path)))
        connection.executemany("INSERT INTO occurrences VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fact.occurrences)
        connection.executemany("INSERT INTO ast_imports VALUES(?, ?, ?, ?, ?, ?, ?, ?)", fact.imports)
        connection.executemany("INSERT INTO ast_calls VALUES(?, ?, ?, ?, ?, ?, ?, ?)", fact.calls)
    symbol_path = {str(row[0]): str(row[1]) for row in connection.execute("SELECT id, path FROM symbols")}
    for occurrence in connection.execute("SELECT id, path, role, name FROM occurrences WHERE role='reference' ORDER BY path, start_byte, id"):
        occurrence_id, path, _role, name = map(str, occurrence)
        connection.execute("INSERT INTO graph_nodes VALUES(?, ?, ?, ?)", (occurrence_id, "occurrence", path, name))
        candidates = sorted({
            symbol_id for symbol_id in by_name.get(name, [])
            if symbol_path.get(symbol_id) == path
        })
        if len(candidates) == 1:
            edges.add((occurrence_id, candidates[0], "references", name[:160], path))
    for call in connection.execute("SELECT id, path, name FROM ast_calls ORDER BY path, start_byte, id"):
        call_id, path, name = map(str, call)
        connection.execute("INSERT INTO graph_nodes VALUES(?, ?, ?, ?)", (call_id, "call", path, name))
        candidates = sorted({
            symbol_id for symbol_id in by_name.get(name, [])
            if symbol_path.get(symbol_id) == path
        })
        if len(candidates) == 1:
            edges.add((call_id, candidates[0], "calls", name[:160], path))
    stems: dict[str, list[str]] = defaultdict(list)
    for path in accepted:
        stems[Path(path).stem.lower()].append(path)
    for import_id, path, raw in connection.execute("SELECT id, path, raw FROM ast_imports ORDER BY path, start_byte, id"):
        normalized_tokens = set(re.findall(r"[a-z0-9_]+", str(raw).lower()))
        matches = sorted({
            candidate
            for stem, paths in stems.items()
            if stem and stem in normalized_tokens
            for candidate in paths
            if candidate != path
        })
        if len(matches) == 1:
            edges.add((file_ids[str(path)], file_ids[matches[0]], "imports", str(raw)[:160], str(path)))
    for path in sorted(accepted):
        stem = Path(path).stem.lower()
        target_stem = ""
        if stem.startswith("test_"):
            target_stem = stem[5:]
        elif stem.endswith("_test"):
            target_stem = stem[:-5]
        candidates = sorted(candidate for candidate in stems.get(target_stem, []) if candidate != path)
        if target_stem and len(candidates) == 1:
            edges.add((file_ids[path], file_ids[candidates[0]], "test-target", target_stem, path))
    connection.executemany("INSERT INTO graph_edges VALUES(?, ?, ?, ?, ?)", sorted(edges))
    edge_counts = Counter(str(row[0]) for row in connection.execute("SELECT kind FROM graph_edges"))
    if any(count > MAX_EDGES_PER_KIND for count in edge_counts.values()) or sum(edge_counts.values()) > MAX_TOTAL_EDGES:
        raise GraphError("graph-edge-bound-exceeded")
    coverage_rows = []
    for language in LANGUAGE_SUFFIXES:
        files = sum(1 for path in selected if language_for_path(path) == language)
        parsed = sum(1 for fact in facts if fact.language == language)
        count_errors = files - parsed
        status = grammar_status.get(language, "not_required" if files == 0 else "missing")
        connection.execute("INSERT INTO language_coverage VALUES(?, ?, ?, ?, ?)", (language, files, parsed, count_errors, status))
        coverage_rows.append({"language": language, "files": files, "parsed": parsed, "errors": count_errors, "grammar_status": status})
    complete = not errors and all(row["parsed"] == row["files"] and (row["files"] == 0 or row["grammar_status"] == "ready") for row in coverage_rows)
    return {
        "schema": GRAPH_SCHEMA,
        "graph_complete": complete,
        "selected_files": len(selected),
        "parsed_files": len(facts),
        "errors": errors,
        "coverage": coverage_rows,
        "nodes": int(connection.execute("SELECT COUNT(*) FROM graph_nodes").fetchone()[0]),
        "edges": int(connection.execute("SELECT COUNT(*) FROM graph_edges").fetchone()[0]),
        "symbols": int(connection.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]),
        "occurrences": int(connection.execute("SELECT COUNT(*) FROM occurrences").fetchone()[0]),
        "edge_counts": [[kind, edge_counts[kind]] for kind in sorted(edge_counts)],
    }


def stats(connection: Any) -> dict[str, object]:
    coverage = [list(row) for row in connection.execute("SELECT language, files, parsed, errors, grammar_status FROM language_coverage ORDER BY language")]
    complete = all(int(row[1]) == int(row[2]) and int(row[3]) == 0 and (int(row[1]) == 0 or row[4] == "ready") for row in coverage)
    edge_counts = [list(row) for row in connection.execute("SELECT kind, COUNT(*) FROM graph_edges GROUP BY kind ORDER BY kind")]
    max_fanout = int(connection.execute("SELECT COALESCE(MAX(total), 0) FROM (SELECT COUNT(*) AS total FROM graph_edges GROUP BY source_id, kind)").fetchone()[0])
    return {
        "schema": STATS_SCHEMA,
        "graph_complete": complete,
        "coverage": coverage,
        "counts": {
            "files": int(connection.execute("SELECT COUNT(*) FROM graph_nodes WHERE kind='file'").fetchone()[0]),
            "ast_files": int(connection.execute("SELECT COUNT(*) FROM code_files").fetchone()[0]),
            "symbols": int(connection.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]),
            "occurrences": int(connection.execute("SELECT COUNT(*) FROM occurrences").fetchone()[0]),
            "nodes": int(connection.execute("SELECT COUNT(*) FROM graph_nodes").fetchone()[0]),
            "edges": int(connection.execute("SELECT COUNT(*) FROM graph_edges").fetchone()[0]),
            "exclusions": int(connection.execute("SELECT COUNT(*) FROM graph_exclusions").fetchone()[0]),
        },
        "edge_counts": edge_counts,
        "max_fanout": max_fanout,
        "bounds": {"max_edges_per_kind": MAX_EDGES_PER_KIND, "max_total_edges": MAX_TOTAL_EDGES},
    }


def _deny_network() -> None:
    def denied(*_args: object, **_kwargs: object) -> object:
        raise OSError("runtime network denied")
    socket.create_connection = denied  # type: ignore[assignment]
    socket.socket.connect = denied  # type: ignore[assignment]


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] != "--extract":
        print("usage: code_graph.py --extract PATH SOURCE_SHA256", file=sys.stderr)
        return 2
    _deny_network()
    try:
        fact = extract(sys.argv[2], sys.stdin.read(), sys.argv[3])
    except GraphError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(encode_toon(_fact_payload(fact)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
