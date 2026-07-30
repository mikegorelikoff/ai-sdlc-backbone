#!/usr/bin/env python3
"""Validate links, assets, and Material contracts in built documentation."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Targets(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []
        self.h1_count = 0
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and not any(name == "alt" and value is not None for name, value in attrs):
            self.images_without_alt += 1
        wanted = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if wanted is None:
            return
        for name, value in attrs:
            if name == wanted and value:
                self.values.append(value)


def target_path(source: Path, target: str, site: Path) -> Path | None:
    if target.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#")):
        return None
    path_text = unquote(urlsplit(target).path)
    if not path_text:
        return None
    site_prefix = "/ai-sdlc-harness/"
    if path_text.startswith(site_prefix):
        candidate = (site / path_text.removeprefix(site_prefix)).resolve()
    elif path_text.startswith("/"):
        return site / "__invalid_root_absolute_target__"
    else:
        candidate = (source.parent / path_text).resolve()
    if path_text.endswith("/") or candidate.is_dir():
        candidate /= "index.html"
    return candidate


def validate(site: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    html_files = sorted(site.rglob("*.html"))
    if len(html_files) < 44:
        errors.append(f"rendered page count is {len(html_files)}; expected at least 44 including 404")
    checked = 0
    for source in html_files:
        parser = Targets()
        parser.feed(source.read_text(encoding="utf-8"))
        if parser.h1_count != 1:
            errors.append(f"{source.relative_to(site)}: expected one accessible h1; found {parser.h1_count}")
        if parser.images_without_alt:
            errors.append(f"{source.relative_to(site)}: {parser.images_without_alt} image(s) missing alt text")
        for target in parser.values:
            resolved = target_path(source, target, site)
            if resolved is None:
                continue
            checked += 1
            if not resolved.exists():
                errors.append(f"{source.relative_to(site)}: broken rendered target {target}")
    index = site / "index.html"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        for token in (
            "mkdocs-material-9.7.7",
            'data-md-color-scheme="default"',
            'class="product-hero"',
            'id="the-problem"',
            'id="choose-your-path"',
            'id="ai-sdlc-product-family"',
        ):
            if token not in text:
                errors.append(f"index.html: missing rendered Material contract {token}")
    for relative in ("assets/stylesheets/ai-sdlc.css",):
        if not (site / relative).exists():
            errors.append(f"rendered asset missing: {relative}")
    forbidden = "." + "".join(chr(value) for value in (106, 115, 111, 110))
    for path in sorted(site.rglob("*")):
        if path.is_file() and path.suffix.lower() == forbidden:
            errors.append(
                f"rendered alternate machine artifact: {path.relative_to(site)}"
            )
    return errors, checked


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
    if not site.is_dir():
        print(f"ERROR: rendered site directory missing: {site}")
        return 1
    errors, checked = validate(site)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Rendered site valid: {len(list(site.rglob('*.html')))} HTML pages, {checked} local targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
