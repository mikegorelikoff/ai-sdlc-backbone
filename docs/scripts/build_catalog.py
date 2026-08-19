#!/usr/bin/env python3
"""Validate that no private generated catalog is published."""

from pathlib import Path
import argparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    reference = Path(__file__).resolve().parents[1] / "reference"
    forbidden = [
        path for path in reference.glob("skills*.md")
        if path.name != "skills-overview.md"
    ]
    if (reference / "skills").exists():
        forbidden.append(reference / "skills")
    if forbidden:
        raise SystemExit(f"private skill catalog must not be public: {forbidden[0]}")
    print("public catalog boundary: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
