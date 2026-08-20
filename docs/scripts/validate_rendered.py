#!/usr/bin/env python3
"""Check required rendered pages and public wording."""

from pathlib import Path
import sys


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    required = ["index.html", "start-here/index.html", "how-it-works/index.html", "reference/index.html", "project/index.html"]
    for relative in required:
        path = site / relative
        if not path.is_file():
            raise SystemExit(f"missing rendered page: {relative}")
    home = (site / "index.html").read_text(encoding="utf-8")
    if "AI SDLC Harness" not in home or "Structure delivery" not in home:
        raise SystemExit("rendered home is missing product contract")
    print("rendered documentation: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
