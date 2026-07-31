#!/usr/bin/env python3
"""Tests for the deterministic harness-owned installer."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
ROOT = Path(__file__).resolve().parents[3]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ai_sdlc_install as native_install
from ai_sdlc_install import InstallError, consumer_mutation_lock, install
import ai_sdlc_install_record as install_record


LEGACY_MACHINE_SUFFIX = "." + "".join(chr(value) for value in (106, 115, 111, 110))


class NativeInstallTests(unittest.TestCase):
    def source_fixture(self, root: Path) -> Path:
        source = root / "source"
        names = ["ai-sdlc-flow", "ai-sdlc-shared-runtime"]
        (source / "config").mkdir(parents=True)
        (source / "config/ai-sdlc-managed-skills.txt").write_text(
            "".join(f"{name}\n" for name in names),
            encoding="utf-8",
        )
        for name in names:
            skill = source / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: fixture\n---\n",
                encoding="utf-8",
            )
            (skill / "steps").mkdir()
            (skill / "steps/manifest.toon").write_text(
                "schema: ai-sdlc-steps/v2\n",
                encoding="utf-8",
            )
        subprocess.run(["git", "init", str(source)], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "-C", str(source), "add", "."], check=True)
        subprocess.run(
            [
                "git", "-C", str(source),
                "-c", "user.name=Fixture",
                "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false",
                "commit", "-m", "fixture source",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        return source

    def run_install(self, source: Path, consumer: Path, **overrides: object) -> tuple[int, Path, Path]:
        consumer.mkdir(parents=True, exist_ok=True)
        if not (consumer / ".git").exists():
            subprocess.run(["git", "init", str(consumer)], check=True, stdout=subprocess.DEVNULL)
        arguments = {
            "source": source,
            "root": consumer,
            "revision": subprocess.check_output(
                ["git", "-C", str(source), "rev-parse", "HEAD"],
                text=True,
            ).strip(),
            "agent": "codex",
            "requested": ["ai-sdlc-flow", "ai-sdlc-shared-runtime"],
            "replace_reviewed": False,
        }
        arguments.update(overrides)
        return install(**arguments)  # type: ignore[arg-type]

    def test_install_is_deterministic_and_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            first = root / "consumer-a"
            second = root / "consumer-b"
            count, record, lock = self.run_install(source, first)
            self.run_install(source, second)

            self.assertEqual(count, 2)
            self.assertEqual(lock.read_bytes(), (second / ".ai-sdlc/harness-install-lock.toon").read_bytes())
            self.assertFalse(list(first.rglob("*" + LEGACY_MACHINE_SUFFIX)))
            self.assertEqual(install_record.validate(record, first / ".agents/skills"), [])

    def test_existing_difference_requires_explicit_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            consumer = root / "consumer"
            self.run_install(source, consumer)
            accepted_lock = (consumer / ".ai-sdlc/harness-install-lock.toon").read_bytes()
            installed = consumer / ".agents/skills/ai-sdlc-flow/SKILL.md"
            installed.write_text("locally changed\n", encoding="utf-8")

            with self.assertRaisesRegex(InstallError, "review it before --replace-reviewed"):
                self.run_install(source, consumer)
            self.assertEqual(
                (consumer / ".ai-sdlc/harness-install-lock.toon").read_bytes(),
                accepted_lock,
            )

            self.run_install(source, consumer, replace_reviewed=True)
            self.assertIn("name: ai-sdlc-flow", installed.read_text(encoding="utf-8"))

    def test_non_toon_machine_artifact_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            (source / "skills/ai-sdlc-flow" / ("legacy" + LEGACY_MACHINE_SUFFIX)).write_text(
                "{}\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(
                [
                    "git", "-C", str(source),
                    "-c", "user.name=Fixture",
                    "-c", "user.email=fixture@example.invalid",
                    "-c", "commit.gpgsign=false",
                    "commit", "-m", "add rejected artifact",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )

            with self.assertRaisesRegex(InstallError, "non-TOON machine artifact"):
                self.run_install(source, root / "consumer")

    def test_unvalidated_agent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)

            with self.assertRaisesRegex(InstallError, "currently validates project scope only for agent codex"):
                self.run_install(source, root / "consumer", agent="claude-code")

    def test_dirty_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            (source / "skills/ai-sdlc-flow/dirty.txt").write_text("uncommitted\n", encoding="utf-8")

            with self.assertRaisesRegex(InstallError, "source checkout is dirty"):
                self.run_install(source, root / "consumer")

    def test_missing_local_source_path_fails_without_remote_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            consumer = Path(temp)
            subprocess.run(["git", "init", str(consumer)], check=True, stdout=subprocess.DEVNULL)
            environment = os.environ.copy()
            environment["AI_SDLC_SOURCE"] = str(consumer / "missing-source")
            environment["AI_SDLC_PYTHON"] = sys.executable
            result = subprocess.run(
                ["sh", str(ROOT / "install.sh"), "codex"],
                cwd=consumer,
                env=environment,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 65)
            self.assertIn("local path that does not exist", result.stderr)

    def test_legacy_installer_lock_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            consumer = root / "consumer"
            consumer.mkdir()
            (consumer / ("skills-lock" + LEGACY_MACHINE_SUFFIX)).write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(InstallError, "review and remove"):
                self.run_install(source, consumer)

    def test_linked_managed_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            consumer = root / "consumer"
            outside = root / "outside"
            consumer.mkdir()
            outside.mkdir()
            (consumer / ".agents").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(InstallError, "must not be a symbolic link"):
                self.run_install(source, consumer)

    def test_concurrent_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            consumer = root / "consumer"
            consumer.mkdir()
            subprocess.run(["git", "init", str(consumer)], check=True, stdout=subprocess.DEVNULL)

            with consumer_mutation_lock(consumer):
                with self.assertRaisesRegex(InstallError, "already mutating"):
                    self.run_install(source, consumer)

    def test_caught_apply_failure_restores_previous_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.source_fixture(root)
            consumer = root / "consumer"
            self.run_install(source, consumer)
            accepted_lock = (consumer / ".ai-sdlc/harness-install-lock.toon").read_bytes()
            accepted_files = {
                name: (consumer / ".agents/skills" / name / "SKILL.md").read_bytes()
                for name in ("ai-sdlc-flow", "ai-sdlc-shared-runtime")
            }
            for name in accepted_files:
                path = source / "skills" / name / "SKILL.md"
                path.write_text(path.read_text(encoding="utf-8") + "\nUpdated.\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(
                [
                    "git", "-C", str(source),
                    "-c", "user.name=Fixture",
                    "-c", "user.email=fixture@example.invalid",
                    "-c", "commit.gpgsign=false",
                    "commit", "-m", "updated fixture source",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )

            real_replace = native_install.os.replace

            def fail_second_skill(source_path: object, destination_path: object) -> None:
                source_text = str(source_path)
                destination = Path(destination_path)  # type: ignore[arg-type]
                if (
                    destination.as_posix().endswith(
                        "/.agents/skills/ai-sdlc-shared-runtime"
                    )
                    and "backup-skills" not in source_text
                ):
                    raise OSError("injected apply failure")
                real_replace(source_path, destination_path)  # type: ignore[arg-type]

            with mock.patch.object(native_install.os, "replace", side_effect=fail_second_skill):
                with self.assertRaisesRegex(OSError, "injected apply failure"):
                    self.run_install(source, consumer, replace_reviewed=True)

            self.assertEqual(
                (consumer / ".ai-sdlc/harness-install-lock.toon").read_bytes(),
                accepted_lock,
            )
            for name, expected in accepted_files.items():
                self.assertEqual(
                    (consumer / ".agents/skills" / name / "SKILL.md").read_bytes(),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
