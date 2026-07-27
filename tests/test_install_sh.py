#!/usr/bin/env python3
"""Offline contract tests for the public shell installer."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.sh"


class InstallShellTests(unittest.TestCase):
    def run_installer(
        self,
        *arguments: str,
        overrides: dict[str, str] | None = None,
        include_npx: bool = True,
        npx_status: int = 0,
        stdin_mode: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            record = fixture / "npx-record"
            environment = os.environ.copy()
            environment["NPX_RECORD"] = str(record)
            environment["NPX_STATUS"] = str(npx_status)
            environment["PATH"] = str(fixture) if include_npx else ""
            if overrides:
                environment.update(overrides)

            if include_npx:
                fake_npx = fixture / "npx"
                fake_npx.write_text(
                    "#!/bin/sh\n"
                    "printf 'telemetry=%s\\n' \"${DISABLE_TELEMETRY-}\" > \"$NPX_RECORD\"\n"
                    "printf 'arg=%s\\n' \"$@\" >> \"$NPX_RECORD\"\n"
                    "exit \"$NPX_STATUS\"\n",
                    encoding="utf-8",
                )
                fake_npx.chmod(0o755)

            command = (
                ["/bin/sh", "-s", "--", *arguments]
                if stdin_mode
                else ["/bin/sh", str(INSTALLER), *arguments]
            )
            result = subprocess.run(
                command,
                cwd=fixture,
                env=environment,
                input=INSTALLER.read_text(encoding="utf-8") if stdin_mode else None,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            lines = record.read_text(encoding="utf-8").splitlines() if record.exists() else []
            return result, lines

    def test_default_codex_invocation(self) -> None:
        result, lines = self.run_installer("codex")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            lines,
            [
                "telemetry=1",
                "arg=-y",
                "arg=skills@1.5.19",
                "arg=add",
                "arg=mikegorelikoff/ai-sdlc-harness",
                "arg=--skill",
                "arg=*",
                "arg=--agent",
                "arg=codex",
                "arg=-y",
            ],
        )

    def test_other_agent_is_preserved_as_one_argument(self) -> None:
        result, lines = self.run_installer("claude code")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("arg=claude code", lines)

    def test_stdin_curl_shape_is_supported(self) -> None:
        result, lines = self.run_installer("claude-code", stdin_mode=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("arg=claude-code", lines)

    def test_source_and_cli_version_can_be_overridden(self) -> None:
        result, lines = self.run_installer(
            "cursor",
            overrides={
                "AI_SDLC_SOURCE": "/reviewed/harness",
                "AI_SDLC_SKILLS_CLI_VERSION": "9.8.7",
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("arg=skills@9.8.7", lines)
        self.assertIn("arg=/reviewed/harness", lines)

    def test_help_and_invalid_arity_do_not_invoke_npx(self) -> None:
        help_result, help_lines = self.run_installer("--help")
        missing_result, missing_lines = self.run_installer()
        extra_result, extra_lines = self.run_installer("codex", "extra")

        self.assertEqual(help_result.returncode, 0)
        self.assertIn("Usage: install.sh AGENT", help_result.stdout)
        self.assertEqual(help_lines, [])
        self.assertEqual(missing_result.returncode, 64)
        self.assertEqual(missing_lines, [])
        self.assertEqual(extra_result.returncode, 64)
        self.assertEqual(extra_lines, [])

    def test_missing_npx_has_actionable_error(self) -> None:
        result, lines = self.run_installer("codex", include_npx=False)

        self.assertEqual(result.returncode, 127)
        self.assertIn("requires Node.js and npx", result.stderr)
        self.assertEqual(lines, [])

    def test_delegated_exit_status_is_preserved(self) -> None:
        result, _ = self.run_installer("codex", npx_status=23)

        self.assertEqual(result.returncode, 23)


if __name__ == "__main__":
    unittest.main()
