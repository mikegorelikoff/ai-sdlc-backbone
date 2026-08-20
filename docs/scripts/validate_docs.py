#!/usr/bin/env python3
"""Validate stable public documentation contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAV = ["Home:", "Start here:", "How it works:", "Guides:", "Reference:", "Project:"]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    positions = [config.find(item) for item in NAV]
    if -1 in positions or positions != sorted(positions):
        fail("public navigation is missing or out of order")
    for relative in [
        "docs/index.md", "docs/start-here/index.md", "docs/how-it-works/index.md",
        "docs/guides/index.md", "docs/reference/index.md", "docs/project/index.md",
        "docs/assets/stylesheets/ai-sdlc.css",
    ]:
        if not (ROOT / relative).is_file():
            fail(f"missing public documentation contract: {relative}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ordered = [
        "# AI SDLC Backbone", "Structure delivery. Control context. Measure adoption.",
        "## Why use it?", "## Quick start", "## Expected result", "## Workflow",
        "## Scope", "## Documentation paths", "## AI SDLC product family",
        "## Security and privacy", "## Status", "## Contributing", "## License",
    ]
    indexes = [readme.find(item) for item in ordered]
    if -1 in indexes or indexes != sorted(indexes):
        fail("README contract is missing or out of order")
    for relative in ["README.md", "docs/index.md", "docs/start-here/index.md"]:
        content = (ROOT / relative).read_text(encoding="utf-8")
        if content.count("npx ai-sdlc-backbone") != 1:
            fail(f"{relative} must contain exactly one primary install command")
    print("documentation source contracts: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
