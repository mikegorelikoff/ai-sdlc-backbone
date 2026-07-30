#!/usr/bin/env python3
"""Compile deterministic, per-step context without network or model calls."""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from ai_sdlc_toon import encode_toon


SCHEMA = "ai-sdlc-context-pack/v4"
PACK_FIELDS = {
    "schema",
    "skill",
    "step_id",
    "budget_tokens",
    "raw_tokens",
    "packed_tokens",
    "savings_percent",
    "critical_total",
    "critical_retained",
    "critical_recall_percent",
    "sufficient",
    "strategy",
    "reason",
    "selected",
    "skipped",
    "direct_read_paths",
    "fingerprint",
}
RANGE_FIELDS = {
    "path",
    "sha256",
    "authority",
    "start_line",
    "end_line",
    "estimated_tokens",
    "strategy",
    "reasons",
    "matched_terms",
    "content",
}
AUTHORITIES = {
    "skill_instruction",
    "repository_instruction",
    "evidence_only",
}
RANGE_STRATEGIES = {
    "mandatory-step-document",
    "full-source",
    "lexical-range",
    "prefix-fallback",
}
IGNORED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site",
    "vendor",
}
TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".toon",
    ".jsx",
    ".md",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
INSTRUCTION_PATHS = {
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
}
SECRET_NAME = re.compile(
    r"(?:^|[._-])(?:secret|token|credential|password|private[-_]?key)(?:[._-]|$)",
    re.IGNORECASE,
)
QUERY_STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "before",
    "context",
    "execute",
    "from",
    "into",
    "only",
    "skill",
    "step",
    "that",
    "the",
    "this",
    "using",
    "with",
}


@dataclass(frozen=True)
class ContextRange:
    """One exact source range selected for a step."""

    path: str
    sha256: str
    authority: str
    start_line: int
    end_line: int
    estimated_tokens: int
    strategy: str
    reasons: tuple[str, ...]
    matched_terms: tuple[str, ...]
    content: str


@dataclass(frozen=True)
class StepContextPack:
    """Portable context result attached to a StepCard."""

    schema: str
    skill: str
    step_id: str
    budget_tokens: int
    raw_tokens: int
    packed_tokens: int
    savings_percent: float
    critical_total: int
    critical_retained: int
    critical_recall_percent: float
    sufficient: bool
    strategy: str
    reason: str
    selected: tuple[ContextRange, ...]
    skipped: tuple[str, ...]
    direct_read_paths: tuple[str, ...]
    fingerprint: str


def canonical(value: object) -> str:
    """Serialize a value with stable ordering and no insignificant whitespace."""
    return encode_toon(value)


def digest(value: object) -> str:
    """Return a deterministic SHA-256 digest."""
    if not isinstance(value, str):
        value = canonical(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def token_estimate(text: str) -> int:
    """Use the repository-wide deterministic character approximation."""
    return max(1, (len(text) + 3) // 4)


def _valid_hash(value: object) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-f0-9]{64}", value))


def _unique_strings(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, (list, tuple))
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def validate_step_context_pack(
    value: object,
    *,
    expected_skill: str = "",
    expected_step_id: str = "",
    require_sufficient: bool = False,
) -> dict[str, Any]:
    """Validate a complete v4 context pack without coercion or repair."""
    if not isinstance(value, dict) or set(value) != PACK_FIELDS:
        raise ValueError("STEP_CONTEXT_INVALID: context pack fields are invalid")
    if value["schema"] != SCHEMA:
        raise ValueError(
            f"STEP_CONTEXT_SCHEMA_MISMATCH: received {value['schema']!r}; "
            f"expected {SCHEMA}"
        )
    for field, expected in (
        ("skill", expected_skill),
        ("step_id", expected_step_id),
    ):
        actual = value[field]
        if not isinstance(actual, str) or not actual:
            raise ValueError(f"STEP_CONTEXT_INVALID: {field} is required")
        if expected and actual != expected:
            raise ValueError(
                f"STEP_CONTEXT_INVALID: {field} {actual!r} does not match "
                f"{expected!r}"
            )

    for field, minimum in (
        ("budget_tokens", 64),
        ("raw_tokens", 0),
        ("packed_tokens", 0),
        ("critical_total", 0),
        ("critical_retained", 0),
    ):
        amount = value[field]
        if (
            not isinstance(amount, int)
            or isinstance(amount, bool)
            or amount < minimum
        ):
            raise ValueError(
                f"STEP_CONTEXT_INVALID: {field} must be an integer >= {minimum}"
            )
    if value["packed_tokens"] > value["raw_tokens"]:
        raise ValueError(
            "STEP_CONTEXT_INVALID: packed_tokens cannot exceed raw_tokens"
        )
    if value["critical_retained"] > value["critical_total"]:
        raise ValueError(
            "STEP_CONTEXT_INVALID: critical_retained exceeds critical_total"
        )

    selected_value = value["selected"]
    if not isinstance(selected_value, (list, tuple)):
        raise ValueError("STEP_CONTEXT_INVALID: selected must be an array")
    selected = list(selected_value)
    selected_paths: list[str] = []
    selected_tokens = 0
    for index, item in enumerate(selected):
        prefix = f"STEP_CONTEXT_INVALID: selected[{index}]"
        if not isinstance(item, dict) or set(item) != RANGE_FIELDS:
            raise ValueError(f"{prefix} fields are invalid")
        if not isinstance(item["path"], str) or not item["path"]:
            raise ValueError(f"{prefix}.path is required")
        selected_paths.append(item["path"])
        if not _valid_hash(item["sha256"]):
            raise ValueError(f"{prefix}.sha256 must be a SHA-256 value")
        if item["authority"] not in AUTHORITIES:
            raise ValueError(f"{prefix}.authority is invalid")
        for field, minimum in (
            ("start_line", 1),
            ("end_line", 0),
            ("estimated_tokens", 1),
        ):
            amount = item[field]
            if (
                not isinstance(amount, int)
                or isinstance(amount, bool)
                or amount < minimum
            ):
                raise ValueError(f"{prefix}.{field} is invalid")
        if item["end_line"] and item["end_line"] < item["start_line"]:
            raise ValueError(f"{prefix} line range is inverted")
        if item["strategy"] not in RANGE_STRATEGIES:
            raise ValueError(f"{prefix}.strategy is invalid")
        if not _unique_strings(item["reasons"], nonempty=True):
            raise ValueError(f"{prefix}.reasons must be unique and non-empty")
        if not _unique_strings(item["matched_terms"]):
            raise ValueError(f"{prefix}.matched_terms must be unique strings")
        if not isinstance(item["content"], str):
            raise ValueError(f"{prefix}.content must be text")
        if item["estimated_tokens"] != token_estimate(item["content"]):
            raise ValueError(f"{prefix}.estimated_tokens does not match content")
        selected_tokens += item["estimated_tokens"]
    if len(selected_paths) != len(set(selected_paths)):
        raise ValueError("STEP_CONTEXT_INVALID: selected paths must be unique")
    if selected_tokens != value["packed_tokens"]:
        raise ValueError(
            "STEP_CONTEXT_INVALID: packed_tokens does not match selected ranges"
        )

    if not _unique_strings(value["skipped"]):
        raise ValueError("STEP_CONTEXT_INVALID: skipped must be unique strings")
    if list(value["skipped"]) != sorted(value["skipped"]):
        raise ValueError("STEP_CONTEXT_INVALID: skipped must be sorted")
    if not _unique_strings(value["direct_read_paths"]):
        raise ValueError(
            "STEP_CONTEXT_INVALID: direct_read_paths must be unique strings"
        )
    if not isinstance(value["sufficient"], bool):
        raise ValueError("STEP_CONTEXT_INVALID: sufficient must be boolean")
    if value["strategy"] not in {"packed", "direct_read"}:
        raise ValueError("STEP_CONTEXT_INVALID: strategy is invalid")
    if not isinstance(value["reason"], str) or not value["reason"]:
        raise ValueError("STEP_CONTEXT_INVALID: reason is required")
    for field in ("savings_percent", "critical_recall_percent"):
        if not isinstance(value[field], (int, float)) or isinstance(
            value[field],
            bool,
        ):
            raise ValueError(f"STEP_CONTEXT_INVALID: {field} must be numeric")

    expected_savings = round(
        (
            (value["raw_tokens"] - value["packed_tokens"])
            / value["raw_tokens"]
            * 100.0
        )
        if value["raw_tokens"]
        else 0.0,
        2,
    )
    if float(value["savings_percent"]) != expected_savings:
        raise ValueError(
            "STEP_CONTEXT_INVALID: savings_percent does not match token counts"
        )
    expected_recall = round(
        (
            value["critical_retained"]
            / value["critical_total"]
            * 100.0
        )
        if value["critical_total"]
        else 100.0,
        2,
    )
    if float(value["critical_recall_percent"]) != expected_recall:
        raise ValueError(
            "STEP_CONTEXT_INVALID: critical recall does not match anchor counts"
        )
    if value["strategy"] == "packed":
        if not value["sufficient"]:
            raise ValueError(
                "STEP_CONTEXT_INVALID: packed strategy requires sufficient context"
            )
        if value["packed_tokens"] > value["budget_tokens"]:
            raise ValueError(
                "STEP_CONTEXT_INVALID: packed strategy exceeds its token budget"
            )
        if value["direct_read_paths"]:
            raise ValueError(
                "STEP_CONTEXT_INVALID: packed strategy cannot request direct reads"
            )
    elif list(value["direct_read_paths"]) != selected_paths:
        raise ValueError(
            "STEP_CONTEXT_INVALID: direct-read paths must match selected ranges"
        )
    if require_sufficient and value["sufficient"] is not True:
        raise ValueError("STEP_CONTEXT_INSUFFICIENT: required context is incomplete")

    claimed = value["fingerprint"]
    if not _valid_hash(claimed):
        raise ValueError("STEP_CONTEXT_INVALID: fingerprint must be a SHA-256 value")
    semantic = copy.deepcopy(value)
    semantic.pop("fingerprint")
    if digest(semantic) != claimed:
        raise ValueError("STEP_CONTEXT_INVALID: fingerprint mismatch")
    return copy.deepcopy(value)


def _query_terms(values: Iterable[str]) -> tuple[str, ...]:
    terms: set[str] = set()
    for value in values:
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{2,}", value.lower()):
            normalized = token.replace("_", "-").strip("-")
            if normalized and normalized not in QUERY_STOPWORDS:
                terms.add(normalized)
    return tuple(sorted(terms)[:64])


def _safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        bool(value)
        and not path.is_absolute()
        and ".." not in path.parts
        and "\\" not in value
        and not set(path.parts) & IGNORED_PARTS
        and not SECRET_NAME.search(value)
    )


def _read_text(base: Path, relative: str) -> tuple[str | None, str | None, Path | None]:
    if not _safe_relative(relative):
        return None, "unsafe-or-secret-path", None
    path = base / relative
    try:
        resolved = path.resolve(strict=False)
        resolved.relative_to(base.resolve())
    except ValueError:
        return None, "path-escape", None
    if path.is_symlink():
        return None, "symlink", None
    if not resolved.is_file():
        return None, "missing", None
    try:
        data = resolved.read_bytes()
    except OSError:
        return None, "unreadable", None
    if len(data) > 262_144:
        return None, "oversized", None
    if b"\0" in data:
        return None, "binary", None
    return data.decode("utf-8", errors="replace"), None, resolved


def _authority(display_path: str) -> str:
    return (
        "repository_instruction"
        if display_path in INSTRUCTION_PATHS
        else "evidence_only"
    )


def _select_range(
    content: str,
    allowed_tokens: int,
    terms: tuple[str, ...],
) -> tuple[str, int, int, str, tuple[str, ...]]:
    """Select one exact, deterministic contiguous range."""
    lines = content.splitlines(keepends=True)
    if not lines:
        return "", 1, 0, "full-source", ()
    character_limit = max(1, allowed_tokens * 4)
    if len(content) <= character_limit:
        lowered = content.lower()
        matched = tuple(term for term in terms if term in lowered)
        return content, 1, len(lines), "full-source", matched

    scores: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        lowered = line.lower()
        scores.append((sum(lowered.count(term) for term in terms), index))
    score, best = max(scores, key=lambda item: (item[0], -item[1]))
    if score <= 0:
        excerpt = content[:character_limit]
        end = excerpt.count("\n") + (0 if excerpt.endswith("\n") else 1)
        return excerpt, 1, end, "prefix-fallback", ()

    start = max(0, best - 3)
    for candidate in range(best, max(-1, best - 13), -1):
        if re.match(r"^\s{0,3}#{1,6}\s+", lines[candidate]):
            start = candidate
            break
    end = min(len(lines), best + 4)
    excerpt = "".join(lines[start:end])
    forward = True
    while len(excerpt) < character_limit and (start > 0 or end < len(lines)):
        if forward and end < len(lines):
            end += 1
        elif start > 0:
            start -= 1
        elif end < len(lines):
            end += 1
        forward = not forward
        excerpt = "".join(lines[start:end])
    excerpt = excerpt[:character_limit]
    lowered = excerpt.lower()
    matched = tuple(term for term in terms if term in lowered)
    end_line = start + excerpt.count("\n") + (0 if excerpt.endswith("\n") else 1)
    return excerpt, start + 1, end_line, "lexical-range", matched


def _repository_candidates(
    root: Path,
    *,
    explicit_paths: Iterable[str],
    terms: tuple[str, ...],
    trace_ids: tuple[str, ...],
    selectors: set[str],
) -> list[tuple[str, int, tuple[str, ...]]]:
    """Return bounded repository candidates ordered by deterministic priority."""
    candidates: dict[str, tuple[int, set[str]]] = {}

    def add(path: str, priority: int, reason: str) -> None:
        current = candidates.get(path)
        if current is None:
            candidates[path] = (priority, {reason})
        else:
            candidates[path] = (max(priority, current[0]), current[1] | {reason})

    if "repository-instructions" in selectors and (root / "AGENTS.md").is_file():
        add("AGENTS.md", 100, "repository-instructions")

    for relative in explicit_paths:
        add(relative, 100, "explicit-path")
        path = PurePosixPath(relative)
        if "changed-path-topology" in selectors and path.name:
            stem = Path(path.name).stem
            for candidate in (
                f"tests/test_{stem}.py",
                f"tests/{stem}_test.py",
                f"{path.parent.as_posix()}/tests/test_{stem}.py",
            ):
                if candidate != relative and (root / candidate).is_file():
                    add(candidate, 85, f"topology:{relative}")

    if "feature-traces" in selectors and (terms or trace_ids):
        needles = tuple(value.lower() for value in (*terms, *trace_ids) if value)
        scanned = 0
        for workspace in ("specs", "specs-refiniment"):
            base = root / workspace
            if not base.is_dir() or base.is_symlink():
                continue
            for path in sorted(base.rglob("*.md")):
                if scanned >= 1_500:
                    break
                scanned += 1
                try:
                    relative = path.relative_to(root).as_posix()
                except ValueError:
                    continue
                text, error, _ = _read_text(root, relative)
                if error or text is None:
                    continue
                lowered = text.lower()
                matches = sum(1 for needle in needles if needle in lowered)
                if matches:
                    add(relative, 70 + min(matches, 20), "feature-trace")

    return [
        (path, priority, tuple(sorted(reasons)))
        for path, (priority, reasons) in sorted(
            candidates.items(), key=lambda item: (-item[1][0], item[0])
        )
    ]


def compile_step_context(
    *,
    root: Path,
    skill_root: Path,
    skill: str,
    step: dict[str, object],
    explicit_paths: Iterable[str] = (),
    goal: str = "",
    trace_ids: Iterable[str] = (),
) -> StepContextPack:
    """Compile the smallest safe context that satisfies one step contract."""
    root = root.resolve()
    skill_root = skill_root.resolve()
    context = step["context"]
    if not isinstance(context, dict):
        raise ValueError("STEP_CONTEXT_INVALID: context contract must be an object")
    budget = int(context["budget_tokens"])
    critical = tuple(str(value) for value in context["critical_anchors"])
    selectors = {str(value) for value in context["selectors"]}
    trace = tuple(sorted({str(value) for value in trace_ids if str(value)}))
    step_id = str(step["id"])
    step_path = str(step["path"])
    terms = _query_terms((skill, step_id, str(step["reason"]), goal, *trace))

    selected: list[ContextRange] = []
    skipped: list[str] = []
    raw_tokens = 0

    step_text, step_error, step_resolved = _read_text(skill_root, step_path)
    if step_error or step_text is None or step_resolved is None:
        skipped.append(f"{skill}/{step_path}:{step_error or 'missing'}")
        step_text = ""
    else:
        raw_tokens += token_estimate(step_text)
        selected.append(
            ContextRange(
                path=f"{skill}/{step_path}",
                sha256=hashlib.sha256(step_resolved.read_bytes()).hexdigest(),
                authority="skill_instruction",
                start_line=1,
                end_line=len(step_text.splitlines()),
                estimated_tokens=token_estimate(step_text),
                strategy="mandatory-step-document",
                reasons=("mandatory:step-document",),
                matched_terms=tuple(term for term in terms if term in step_text.lower()),
                content=step_text,
            )
        )

    candidates = _repository_candidates(
        root,
        explicit_paths=tuple(explicit_paths),
        terms=terms,
        trace_ids=trace,
        selectors=selectors,
    )
    readable: list[tuple[str, int, tuple[str, ...], str, Path]] = []
    for relative, priority, reasons in candidates:
        text, error, resolved = _read_text(root, relative)
        if error or text is None or resolved is None:
            skipped.append(f"{relative}:{error or 'missing'}")
            continue
        raw_tokens += token_estimate(text)
        readable.append((relative, priority, reasons, text, resolved))

    used = sum(item.estimated_tokens for item in selected)
    remaining = max(0, budget - used)
    for relative, _priority, reasons, text, resolved in readable:
        if remaining <= 0:
            skipped.append(f"{relative}:budget-exhausted")
            continue
        allowance = min(remaining, token_estimate(text), 1_200)
        excerpt, start, end, strategy, matched = _select_range(text, allowance, terms)
        tokens = token_estimate(excerpt)
        selected.append(
            ContextRange(
                path=relative,
                sha256=hashlib.sha256(resolved.read_bytes()).hexdigest(),
                authority=_authority(relative),
                start_line=start,
                end_line=end,
                estimated_tokens=tokens,
                strategy=strategy,
                reasons=reasons,
                matched_terms=matched,
                content=excerpt,
            )
        )
        remaining = max(0, remaining - tokens)

    packed_tokens = sum(item.estimated_tokens for item in selected)
    mandatory_content = step_text
    retained = sum(1 for anchor in critical if anchor in mandatory_content)
    recall = round((retained / len(critical) * 100.0) if critical else 100.0, 2)
    savings = round(
        ((raw_tokens - packed_tokens) / raw_tokens * 100.0) if raw_tokens else 0.0,
        2,
    )
    missing = [anchor for anchor in critical if anchor not in mandatory_content]
    sufficient = bool(step_text) and not missing
    threshold = float(context["min_savings_percent"])
    within_budget = packed_tokens <= budget
    packed_is_economic = savings >= threshold and within_budget
    strategy = "packed" if sufficient and packed_is_economic else "direct_read"
    reasons: list[str] = []
    if missing:
        reasons.append("missing critical anchors: " + ", ".join(missing))
    if not step_text:
        reasons.append("mandatory step document is unavailable")
    if savings < threshold:
        reasons.append(
            f"net savings {savings:.2f}% are below {threshold:.2f}%"
        )
    if not within_budget:
        reasons.append(f"packed context {packed_tokens} exceeds budget {budget}")
    if not reasons:
        reasons.append("critical recall and context economics meet the step contract")
    direct_paths = (
        tuple(item.path for item in selected)
        if strategy == "direct_read"
        else ()
    )
    semantic = {
        "schema": SCHEMA,
        "skill": skill,
        "step_id": step_id,
        "budget_tokens": budget,
        "raw_tokens": raw_tokens,
        "packed_tokens": packed_tokens,
        "savings_percent": savings,
        "critical_total": len(critical),
        "critical_retained": retained,
        "critical_recall_percent": recall,
        "sufficient": sufficient,
        "strategy": strategy,
        "reason": "; ".join(reasons),
        "selected": [asdict(item) for item in selected],
        "skipped": sorted(skipped),
        "direct_read_paths": direct_paths,
    }
    result = StepContextPack(
        schema=SCHEMA,
        skill=skill,
        step_id=step_id,
        budget_tokens=budget,
        raw_tokens=raw_tokens,
        packed_tokens=packed_tokens,
        savings_percent=savings,
        critical_total=len(critical),
        critical_retained=retained,
        critical_recall_percent=recall,
        sufficient=sufficient,
        strategy=strategy,
        reason="; ".join(reasons),
        selected=tuple(selected),
        skipped=tuple(sorted(skipped)),
        direct_read_paths=direct_paths,
        fingerprint=digest(semantic),
    )
    validate_step_context_pack(
        asdict(result),
        expected_skill=skill,
        expected_step_id=step_id,
    )
    return result
