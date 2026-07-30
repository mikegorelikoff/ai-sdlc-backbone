#!/usr/bin/env python3
"""Tests for portable install-record validation."""

from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ai_sdlc_install_record as install_record


class InstallRecordTests(unittest.TestCase):
    def fixture(self, root: Path, *, selection: str = "explicit-skills") -> tuple[Path, Path]:
        skills = root / ".agents/skills"
        names = ["ai-sdlc-flow", "ai-sdlc-shared-runtime"]
        for name in names:
            (skills / name).mkdir(parents=True)
        record = root / ".ai-sdlc/harness-install.toon"
        record.parent.mkdir(parents=True)
        (record.parent / "harness-managed-skills.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
        record.write_text(toon_codec.dumps({
            "schema": "ai-sdlc-install-record/v1", "revision": "a" * 40,
            "skills_cli": "1.5.19", "agent": "codex", "selection": selection,
            "inventory": ".ai-sdlc/harness-managed-skills.txt",
        }), encoding="utf-8")
        return record, skills

    def test_valid_record_matches_installed_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            record, skills = self.fixture(Path(temp))
            self.assertEqual(install_record.validate(record, skills), [])

    def test_unrelated_installed_skill_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            record, skills = self.fixture(Path(temp))
            (skills / "third-party-skill").mkdir()
            self.assertEqual(install_record.validate(record, skills), [])

    def test_missing_managed_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            record, skills = self.fixture(Path(temp))
            (skills / "ai-sdlc-flow").rmdir()
            self.assertTrue(any("managed skills are not installed" in error for error in install_record.validate(record, skills)))

    def test_explicit_subset_requires_shared_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            record, skills = self.fixture(Path(temp))
            (record.parent / "harness-managed-skills.txt").write_text("ai-sdlc-flow\n", encoding="utf-8")
            self.assertTrue(any("must include ai-sdlc-shared-runtime" in error for error in install_record.validate(record, skills)))

    def test_truncated_all_skills_inventory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            record, skills = self.fixture(Path(temp), selection="all-skills")
            self.assertTrue(any("packaged full-skill inventory" in error for error in install_record.validate(record, skills)))


if __name__ == "__main__":
    unittest.main()
