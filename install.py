#!/usr/bin/env python3
"""Cross-platform AI SDLC Harness project installer bootstrap."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit


DEFAULT_REMOTE = "https://github.com/mikegorelikoff/ai-sdlc-harness.git"
DEFAULT_REVISION = "v4.4.0"
PROFILES = ("agent-project", "claude-code-project", "codex-project")
REVISION_RE = re.compile(r"[A-Za-z0-9._-]+")
SHA_RE = re.compile(r"[0-9a-f]{40}")


class BootstrapError(RuntimeError):
    """Raised when bootstrap trust or platform preconditions fail."""


def run_git(*arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require_git(result: subprocess.CompletedProcess[str], action: str) -> str:
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise BootstrapError(f"{action} failed: {detail}")
    return result.stdout.strip()


def normalize_remote(value: str) -> str:
    """Accept a reviewed URL/SSH locator or GitHub owner/repository shorthand."""
    if not value or "\x00" in value or any(character.isspace() for character in value):
        raise BootstrapError("AI_SDLC_SOURCE remote contains unsupported whitespace or control characters")
    if value.startswith(("http://", "https://", "git://")):
        parsed = urlsplit(value)
        if parsed.username is not None or parsed.password is not None:
            raise BootstrapError(
                "credential-bearing remote URLs are not supported; configure Git credentials externally"
            )
        return value
    if value.startswith(("ssh://", "git@")):
        return value
    if re.fullmatch(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+", value):
        return f"https://github.com/{value}.git"
    raise BootstrapError("AI_SDLC_SOURCE must be a local checkout or reviewed Git remote")


def is_explicit_local_source(value: str, candidate: Path) -> bool:
    """Recognize local path syntax before a missing path can resemble a remote."""
    return (
        candidate.is_absolute()
        or value.startswith(("/", "./", "../", "~/", ".\\", "..\\", "~\\", "\\\\"))
        or re.match(r"^[A-Za-z]:[\\/]", value) is not None
    )


def verify_local_source(source: Path, requested: str | None) -> tuple[Path, str]:
    source = source.resolve()
    head = require_git(run_git("-C", str(source), "rev-parse", "--verify", "HEAD"), "source revision")
    if requested:
        resolved = require_git(
            run_git("-C", str(source), "rev-parse", "--verify", f"{requested}^{{commit}}"),
            "requested source revision",
        )
        if resolved != head:
            raise BootstrapError("AI_SDLC_REVISION does not resolve to the local source HEAD")
    return source, head


def checkout_remote(remote: str, revision: str, destination: Path) -> tuple[Path, str]:
    if not REVISION_RE.fullmatch(revision):
        raise BootstrapError("AI_SDLC_REVISION contains unsupported characters")
    require_git(run_git("init", str(destination)), "source initialization")
    require_git(run_git("-C", str(destination), "remote", "add", "origin", remote), "source remote")
    if SHA_RE.fullmatch(revision):
        require_git(run_git("-C", str(destination), "fetch", "--depth", "1", "origin", revision), "source fetch")
        require_git(run_git("-C", str(destination), "checkout", "--detach", "FETCH_HEAD"), "source checkout")
    else:
        refspec = f"refs/tags/{revision}:refs/tags/{revision}"
        require_git(run_git("-C", str(destination), "fetch", "--depth", "1", "origin", refspec), "release fetch")
        tag_type = require_git(run_git("-C", str(destination), "cat-file", "-t", revision), "release tag inspection")
        if tag_type != "tag":
            raise BootstrapError("AI_SDLC_REVISION must name an annotated release tag")
        require_git(run_git("-C", str(destination), "checkout", "--detach", f"{revision}^{{commit}}"), "release checkout")
    head = require_git(run_git("-C", str(destination), "rev-parse", "--verify", "HEAD"), "checked-out revision")
    if SHA_RE.fullmatch(revision) and head != revision:
        raise BootstrapError(f"expected source revision {revision}, found {head}")
    if not SHA_RE.fullmatch(revision):
        tagged = require_git(run_git("-C", str(destination), "rev-list", "-n", "1", revision), "release resolution")
        if tagged != head:
            raise BootstrapError("release tag does not resolve to the checked-out source revision")
    return destination, head


def local_script_source() -> Path | None:
    """Return the checkout containing this file, unless executed from stdin."""
    candidate = Path(__file__)
    if candidate.name.startswith("<"):
        return None
    root = candidate.resolve().parent
    return root if (root / "config/ai-sdlc-managed-skills.txt").is_file() else None


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Install AI SDLC Harness skills into the current Git project.",
        epilog=(
            "Use codex-project or claude-code-project for their fixed roots. "
            "Use agent-project --skills-root PATH for another Agent Skills-compatible host. "
            "Use update to recover the existing profile and selection from its verified TOON record."
        ),
    )
    value.add_argument("command", choices=(*PROFILES, "update"))
    value.add_argument("--skills-root", help="Project-relative skills directory; required for agent-project")
    value.add_argument("--module", action="append", default=[], help="Optional module id; repeatable")
    return value


def main() -> int:
    if sys.version_info < (3, 10):
        print("ERROR: AI SDLC Harness requires Python 3.10 or newer.", file=sys.stderr)
        return 65
    if shutil.which("git") is None:
        print("ERROR: AI SDLC Harness installer requires Git.", file=sys.stderr)
        return 127
    args = parser().parse_args()
    source_value = os.environ.get("AI_SDLC_SOURCE")
    requested = os.environ.get("AI_SDLC_REVISION")
    replace = os.environ.get("AI_SDLC_INSTALL_REPLACE", "0") == "1"
    try:
        updating = args.command == "update"
        if updating and (args.skills_root is not None or args.module):
            raise BootstrapError("update recovers --skills-root and modules from the existing install record")
        with tempfile.TemporaryDirectory(prefix="ai-sdlc-harness-") as temporary:
            source: Path
            revision: str
            if source_value:
                candidate = Path(source_value).expanduser()
                if candidate.exists():
                    if not candidate.is_dir():
                        raise BootstrapError("AI_SDLC_SOURCE local path is not a directory")
                    source, revision = verify_local_source(candidate, requested)
                elif is_explicit_local_source(source_value, candidate):
                    raise BootstrapError("AI_SDLC_SOURCE names a local path that does not exist")
                else:
                    source, revision = checkout_remote(
                        normalize_remote(source_value),
                        requested or DEFAULT_REVISION,
                        Path(temporary) / "source",
                    )
            else:
                local = local_script_source()
                if local is not None:
                    source, revision = verify_local_source(local, requested)
                else:
                    source, revision = checkout_remote(
                        DEFAULT_REMOTE,
                        requested or DEFAULT_REVISION,
                        Path(temporary) / "source",
                    )
            installer = source / "skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_install.py"
            if not installer.is_file():
                raise BootstrapError("resolved source does not contain the native installer")
            command = [
                sys.executable, "-B", str(installer),
                "--source", str(source),
                "--root", str(Path.cwd().resolve()),
                "--revision", revision,
            ]
            if updating:
                command.append("--update-existing")
                print(f'Updating AI SDLC Harness from revision "{revision}"...')
            else:
                command.extend(("--profile", args.command))
                if args.skills_root is not None:
                    command.extend(("--skills-root", args.skills_root))
                for module in args.module:
                    command.extend(("--module", module))
                if replace:
                    command.append("--replace-reviewed")
                print(f'Installing AI SDLC Harness profile "{args.command}" from revision "{revision}"...')
            return subprocess.run(command, check=False).returncode
    except (BootstrapError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 65


if __name__ == "__main__":
    raise SystemExit(main())
