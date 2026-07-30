#!/usr/bin/env python3
"""Validate and route sourced research artifacts."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402
from typing import Any

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_okf import migrate_concept_text, write_bundle_indexes  # noqa: E402


SCHEMA = "ai-sdlc-research-input/v1"
COLLECTIONS = ("questions", "sources", "findings", "open_questions")


def toon(value: object) -> str:
    """Escape one machine scalar."""
    if isinstance(value, list):
        value = "/".join(str(item) for item in value)
    return re.sub(r"[\r\n,]+", "; ", str(value)).strip()


def portable_feature_root(root: Path) -> str:
    """Return a repository-relative feature path without host identity."""
    if root.parent.name in {"specs", "specs-refiniment"}:
        return f"{root.parent.name}/{root.name}"
    return root.name


def load(path: Path) -> tuple[dict[str, Any], list[str]]:
    """Load research input safely."""
    try:
        value = toon_codec.loads(path.read_text(encoding="utf-8"))
    except (OSError, toon_codec.ToonDecodeError) as exc:
        return {}, [f"cannot read research input: {exc}"]
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        return {}, [f"input schema must be {SCHEMA}"]
    return value, []


def required(item: dict[str, Any], fields: tuple[str, ...], prefix: str) -> list[str]:
    """Validate required text fields."""
    return [f"{prefix}: {field} is required" for field in fields if not isinstance(item.get(field), str) or not item.get(field, "").strip()]


def list_text(item: dict[str, Any], field: str, prefix: str) -> list[str]:
    """Validate one non-empty string list."""
    value = item.get(field)
    return [] if isinstance(value, list) and value and all(isinstance(entry, str) and entry.strip() for entry in value) else [f"{prefix}: {field} must be non-empty"]


def validate(value: dict[str, Any], full_flow: bool) -> list[str]:
    """Validate questions, sources, citations, and limitations."""
    errors: list[str] = []
    if not isinstance(value.get("topic"), str) or not value.get("topic", "").strip():
        errors.append("topic is required")
    if value.get("scope") not in {"internal", "external", "mixed"}:
        errors.append("scope must be internal, external, or mixed")
    for name in COLLECTIONS:
        if not isinstance(value.get(name), list) or not all(isinstance(item, dict) for item in value.get(name, [])):
            errors.append(f"{name} must be an array of objects")
    if errors:
        return errors
    ids: dict[str, list[str]] = {name: [] for name in COLLECTIONS}
    for name in COLLECTIONS:
        for item in value[name]:
            ids[name].append(str(item.get("id", "")))
        if len(ids[name]) != len(set(ids[name])):
            errors.append(f"{name}: IDs must be unique")
    for index, item in enumerate(value["questions"], start=1):
        prefix = f"questions {index}"
        errors.extend(required(item, ("id", "question"), prefix))
        errors.extend(list_text(item, "trace_targets", prefix))
    for index, item in enumerate(value["sources"], start=1):
        prefix = f"sources {index}"
        errors.extend(required(item, ("id", "title", "locator", "type", "accessed_at", "credibility", "notes"), prefix))
        if isinstance(item.get("accessed_at"), str):
            try:
                date.fromisoformat(item["accessed_at"])
            except ValueError:
                errors.append(f"{prefix}: accessed_at must be ISO date")
    source_ids = set(ids["sources"])
    for index, item in enumerate(value["findings"], start=1):
        prefix = f"findings {index}"
        errors.extend(required(item, ("id", "statement", "limitations"), prefix))
        errors.extend(list_text(item, "source_ids", prefix))
        errors.extend(list_text(item, "trace_targets", prefix))
        if isinstance(item.get("source_ids"), list) and any(source not in source_ids for source in item["source_ids"]):
            errors.append(f"{prefix}: source_ids must reference registered sources")
        if item.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"{prefix}: invalid confidence")
    for index, item in enumerate(value["open_questions"], start=1):
        errors.extend(required(item, ("id", "question", "owner", "next_action"), f"open_questions {index}"))
    if full_flow:
        if len(value["sources"]) < 2:
            errors.append("full flow requires at least two sources")
        if len({item.get("type") for item in value["sources"]}) < 2:
            errors.append("full flow requires at least two source types")
    if value.get("scope") in {"external", "mixed"} and not any(
        isinstance(item.get("locator"), str) and item["locator"].startswith(("http://", "https://"))
        for item in value["sources"]
    ):
        errors.append("external or mixed scope requires at least one direct HTTP(S) source")
    return errors


def render_toon(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render bounded machine research output."""
    return toon_codec.encode_toon(
        {
            "schema": "ai-sdlc-research/v1",
            "feature_root": portable_feature_root(root),
            "flow_mode": flow,
            "scope": value["scope"],
            "topic": value["topic"],
            "questions": value["questions"],
            "sources": value["sources"],
            "findings": value["findings"],
            "open_questions": value["open_questions"],
        }
    )


def render_markdown(root: Path, flow: str, value: dict[str, Any]) -> str:
    """Render readable sourced research with metadata."""
    refs = sorted({ref for name in ("questions", "findings") for item in value[name] for ref in item["trace_targets"]})
    workspace = "implementation" if root.parent.name == "specs" else "refinement"
    feature_root = portable_feature_root(root)
    lines = ["---", "artifact_metadata:", '  schema: "ai-sdlc-research-metadata/v1"', f'  feature: "{toon(root.name)}"', '  artifact: "research.md"', f'  path: "{feature_root}/research.md"', f'  workspace: "{workspace}"', '  skill: "ai-sdlc-research"', f'  flow_mode: "{flow}"', f'  state_file: "{feature_root}/_ai_sdlc/state.toon"', '  status: "review"', f'  updated_at: "{date.today().isoformat()}"', "  trace_ids:"]
    lines.extend(f'    - "{toon(ref)}"' for ref in refs)
    lines.extend(["  metatags:", '    - "ai-sdlc"', '    - "research"', '    - "evidence"', '    - "traceable"', "---", "", "# Research", "", f"## Topic\n\n{value['topic']}"])
    for name in COLLECTIONS:
        lines.extend(["", f"## {name.replace('_', ' ').title()}"])
        lines.extend(["", "- None."] if not value[name] else ["", *["- " + "; ".join(f"{key}: {toon(field)}" for key, field in item.items()) for item in value[name]]])
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    """Write one research artifact atomically."""
    if any(component.is_symlink() for component in (path, *list(path.parents)[:4])):
        raise SystemExit(f"ERROR: output path contains symlink component: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    """Validate and route research reports."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature_root", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--format", choices=("markdown", "toon"), default="markdown")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    parser.add_argument("--generated-by")
    args = parser.parse_args()
    root = args.feature_root.resolve()
    if args.begin_state or args.complete_state:
        print("ERROR: research generation is read-only with respect to lifecycle state")
        return 1
    if not root.is_dir():
        print(f"ERROR: feature root does not exist: {root}")
        return 1
    if args.state_check and not (root / "_ai_sdlc/state.toon").is_file():
        print("ERROR: canonical state is missing")
        return 1
    value, errors = load(args.input)
    if not errors:
        errors.extend(validate(value, args.full_flow))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    flow = "full" if args.full_flow else "quick" if args.quick_flow else "default"
    human = migrate_concept_text(
        render_markdown(root, flow, value),
        profile_key="research.md",
        generated_by_override=args.generated_by,
    )
    machine = render_toon(root, flow, value)
    if args.write:
        atomic_write(root / "research.md", human)
        atomic_write(root / "_ai_sdlc/research.toon", machine)
        write_bundle_indexes(root)
    print(machine if args.format == "toon" else human, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
