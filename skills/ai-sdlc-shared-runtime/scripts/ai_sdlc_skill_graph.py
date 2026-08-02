#!/usr/bin/env python3
"""Generate and check canonical executable skill-graph projections."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ai_sdlc_steps as steps_runtime  # noqa: E402
from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon  # noqa: E402


REPORT_SCHEMA = "ai-sdlc-skill-graph-generation/v2"


def atomic_write(path: Path, content: str) -> None:
    """Replace one generated projection atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_manifest(skill_root: Path) -> dict[str, Any]:
    """Read one TOON-only v2 manifest without accepting alternate sources."""
    path = skill_root / "steps" / "manifest.toon"
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{skill_root.name}: missing regular steps/manifest.toon")
    try:
        value = decode_toon(path.read_text(encoding="utf-8"))
    except (OSError, ToonDecodeError) as exc:
        raise ValueError(f"{path}: cannot decode manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: manifest root must be a mapping")
    if value.get("schema") != steps_runtime.SCHEMA:
        raise ValueError(
            f"{skill_root.name}: expected {steps_runtime.SCHEMA}; "
            "regenerate the skill graph as TOON v2"
        )
    return value


def router_prefix(text: str) -> str:
    """Preserve frontmatter and the concise skill-specific routing card."""
    marker = "\n## Step Selector"
    if marker in text:
        return text.split(marker, 1)[0].rstrip()
    return text.rstrip()


def generate_router(skill_root: Path, manifest: dict[str, Any]) -> str:
    """Render SKILL.md progressive-disclosure projection from the graph."""
    prefix = router_prefix((skill_root / "SKILL.md").read_text(encoding="utf-8"))
    lines = [
        prefix,
        "",
        "## Step Selector",
        "",
        "This table is generated from `steps/manifest.toon`. The manifest and linked",
        "step documents are canonical; regenerate this projection after graph changes.",
        "",
        "| Step | Ready when | Depends on | Operation | Load |",
        "| --- | --- | --- | --- | --- |",
    ]
    for step in manifest["steps"]:
        phases = ", ".join(f"`{value}`" for value in step["condition"]["phases"])
        dependencies = ", ".join(f"`{value}`" for value in step["depends_on"]) or "none"
        lines.append(
            f"| `{step['id']}` | {phases} | {dependencies} | "
            f"`{step['operation']}` | "
            f"[`{step['path']}`]({step['path']}) — `{step['load']}` |"
        )
    lines.extend(
        [
            "",
            "## Progressive Disclosure Contract",
            "",
            "- Resolve the phase entrypoint and dependency-ready set with",
            "  `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`; never invent a step path.",
            "- Read only the emitted StepCard and its selected context. Pass completed step",
            "  IDs back to the selector before requesting the next ready node.",
            "- Treat `direct_read` as an explicit context strategy. Block only when mandatory",
            "  evidence or critical anchors are missing.",
            "- Explore is read-only. After Apply, journal every selected owning-skill step,",
            "  including analysis and validation nodes, before advancing the graph.",
            "- In a source checkout use `skills/<skill>/...`; in a Codex project install",
            "  use `.agents/skills/<skill>/...`, and in a Claude Code project install use",
            "  `.claude/skills/<skill>/...`.",
            "",
        ]
    )
    return "\n".join(lines)


def skill_roots(skills_root: Path, selected: set[str]) -> list[Path]:
    """Resolve the exact regular skill directories in stable name order."""
    if skills_root.is_symlink() or not skills_root.is_dir():
        raise ValueError(f"invalid skills root: {skills_root}")
    roots = [
        path
        for path in sorted(skills_root.iterdir())
        if path.is_dir()
        and not path.is_symlink()
        and path.name.startswith("ai-sdlc-")
        and (path / "SKILL.md").is_file()
    ]
    if selected:
        missing = sorted(selected - {path.name for path in roots})
        if missing:
            raise ValueError("unknown selected skills: " + ", ".join(missing))
        roots = [path for path in roots if path.name in selected]
    if not roots:
        raise ValueError("no installable skills found")
    return roots


def root_from_skills_root(skills_root: Path) -> Path:
    """Map source and project-scoped skill layouts to their owning root."""
    resolved = skills_root.resolve()
    if resolved.name != "skills":
        raise ValueError("--skills-root must end in skills")
    return resolved.parent.parent if resolved.parent.name in {".agents", ".claude"} else resolved.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, required=True)
    parser.add_argument("--skill", action="append", default=[])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--format", choices=("toon",), default="toon")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument(
        "--state-workspace",
        choices=("refinement", "implementation"),
    )
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        parser.error("skill-graph projection cannot mutate lifecycle state")

    skills_root = args.skills_root.resolve()
    root = root_from_skills_root(skills_root)
    report: list[dict[str, object]] = []
    try:
        roots = skill_roots(skills_root, set(args.skill))
        for skill_root in roots:
            manifest = read_manifest(skill_root)
            expected = generate_router(skill_root, manifest)
            router_path = skill_root / "SKILL.md"
            actual = router_path.read_text(encoding="utf-8")
            if args.check and actual != expected:
                raise ValueError(
                    f"{skill_root.name}: generated SKILL.md projection is stale"
                )
            if args.generate and actual != expected:
                atomic_write(router_path, expected)

            _validated_root, validated = steps_runtime.load_manifest(
                root, skill_root.name
            )
            report.append(
                {
                    "skill": skill_root.name,
                    "schema": validated["schema"],
                    "nodes": len(validated["steps"]),
                    "router": "valid",
                }
            )

        result = {
            "schema": REPORT_SCHEMA,
            "mode": "generate" if args.generate else "check",
            "skills": len(report),
            "nodes": sum(int(item["nodes"]) for item in report),
            "result": "valid",
            "items": report,
        }
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(encode_toon(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
