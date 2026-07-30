#!/usr/bin/env python3
"""Tests for deterministic all-skill and live-protocol evaluation."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = REPO_ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

SPEC = importlib.util.spec_from_file_location(
    "ai_sdlc_skill_eval", SCRIPT_DIR / "ai_sdlc_skill_eval.py"
)
assert SPEC and SPEC.loader
skill_eval = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(skill_eval)

from ai_sdlc_toon import decode_toon, encode_toon  # noqa: E402


class SkillEvalTests(unittest.TestCase):
    def test_deterministic_subset_is_byte_stable(self) -> None:
        selected = {"ai-sdlc-flow", "ai-sdlc-sdd"}
        first = skill_eval.deterministic_receipt(
            REPO_ROOT / "skills", selected=selected
        )
        second = skill_eval.deterministic_receipt(
            REPO_ROOT / "skills", selected=selected
        )
        first_bytes = encode_toon(first)
        self.assertEqual(first_bytes, encode_toon(second))
        self.assertEqual(decode_toon(first_bytes), first)
        self.assertEqual(first["schema"], "ai-sdlc-eval-receipt/v1")
        self.assertEqual(first["skills"], 2)
        self.assertEqual(first["scenarios"], 10)
        self.assertEqual(first["failed"], 0)
        self.assertEqual(first["result"], "passed")
        for item in first["items"]:
            self.assertEqual(
                [case["scenario"] for case in item["scenarios"]],
                list(skill_eval.SCENARIOS),
            )

    def test_live_protocol_is_offline_and_portable(self) -> None:
        receipt = skill_eval.live_protocol_receipt(REPO_ROOT / "skills")
        self.assertEqual(receipt["result"], "passed")
        self.assertEqual(receipt["failed"], 0)
        self.assertTrue(receipt["protocol"]["provider_neutral"])
        template = receipt["portable_receipt_template"]
        self.assertEqual(template["status"], "pending")
        self.assertEqual(template["provider"], "")
        self.assertEqual(template["scenario_results"], [])
        self.assertEqual(decode_toon(encode_toon(receipt)), receipt)

    def test_explicit_receipt_output_is_repository_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "root"
            root.mkdir()
            outside = parent / "outside.toon"
            with self.assertRaisesRegex(ValueError, "escapes repository root"):
                skill_eval.atomic_output(root, outside, "schema: fixture\n")
            self.assertFalse(outside.exists())

    def test_repository_has_only_canonical_toon_machine_artifacts(self) -> None:
        forbidden_bytes = bytes((106, 115, 111, 110))
        forbidden_suffix = "." + forbidden_bytes.decode("ascii")
        path_violations: list[str] = []
        decode_violations: list[str] = []
        canonical_violations: list[str] = []
        for path in REPO_ROOT.rglob("*"):
            if (
                ".git" in path.parts
                or "site" in path.parts
                or "__pycache__" in path.parts
            ):
                continue
            if path.is_file() and path.suffix.lower() == forbidden_suffix:
                path_violations.append(path.relative_to(REPO_ROOT).as_posix())
            if not path.is_file() or path.suffix != ".toon":
                continue
            relative = path.relative_to(REPO_ROOT)
            text = path.read_text(encoding="utf-8")
            try:
                value = decode_toon(text)
            except Exception as exc:  # exact path evidence is more useful here
                decode_violations.append(f"{relative.as_posix()}: {exc}")
                continue
            canonical_owner = (
                path.name.endswith(".schema.toon")
                or relative.parts[:1] in {("compatibility",), ("config",), ("modules",)}
                or (
                    len(relative.parts) >= 3
                    and relative.parts[0] == "skills"
                    and relative.parts[-2:] == ("steps", "manifest.toon")
                )
                or "fixtures" in relative.parts
            )
            if canonical_owner and encode_toon(value) != text:
                canonical_violations.append(relative.as_posix())

        inventory = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=REPO_ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout.split(b"\0")
        text_violations: list[str] = []
        for item in inventory:
            if not item:
                continue
            relative = Path(item.decode("utf-8"))
            path = REPO_ROOT / relative
            if path.is_file() and forbidden_bytes in path.read_bytes().lower():
                text_violations.append(relative.as_posix())

        self.assertEqual(path_violations, [])
        self.assertEqual(text_violations, [])
        self.assertEqual(decode_violations, [])
        self.assertEqual(canonical_violations, [])


if __name__ == "__main__":
    unittest.main()
