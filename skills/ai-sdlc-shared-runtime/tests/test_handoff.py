#!/usr/bin/env python3
"""Tests for the journal-backed handoff v2 contract."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_SHARED = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = _SHARED / "ai_sdlc_handoff.py"
RUNTIME = ROOT / "skills/ai-sdlc-runtime/scripts/runtime.py"
HASH_A = "a" * 64


def digest(value: object) -> str:
    return hashlib.sha256(toon_codec.encode_toon(value).encode("utf-8")).hexdigest()


def context_pack(skill: str, step_id: str) -> dict[str, object]:
    content = (
        "# Validate\n\n## Entry\n\nInspect evidence.\n\n"
        "## Procedure\n\nRun deterministic checks.\n\n"
        "## Exit\n\nReturn validation evidence.\n"
    )
    path = f"{skill}/steps/{step_id}.md"
    tokens = max(1, (len(content) + 3) // 4)
    semantic = {
        "schema": "ai-sdlc-context-pack/v4",
        "skill": skill,
        "step_id": step_id,
        "budget_tokens": 100,
        "raw_tokens": tokens,
        "packed_tokens": tokens,
        "savings_percent": 0.0,
        "critical_total": 3,
        "critical_retained": 3,
        "critical_recall_percent": 100.0,
        "sufficient": True,
        "strategy": "direct_read",
        "reason": "direct read preserves the validation procedure",
        "selected": [
            {
                "path": path,
                "sha256": HASH_A,
                "authority": "skill_instruction",
                "start_line": 1,
                "end_line": len(content.splitlines()),
                "estimated_tokens": tokens,
                "strategy": "mandatory-step-document",
                "reasons": ["mandatory:step-document"],
                "matched_terms": [],
                "content": content,
            }
        ],
        "skipped": [],
        "direct_read_paths": [path],
    }
    return {**semantic, "fingerprint": digest(semantic)}


def contract_text(skill: Path) -> str:
    text = skill.read_text(encoding="utf-8")
    manifest = toon_codec.loads(
        (skill.parent / "steps" / "manifest.toon").read_text(encoding="utf-8")
    )
    return text + "\n".join(
        (skill.parent / step["path"]).read_text(encoding="utf-8")
        for step in manifest["steps"]
    )


class HandoffTests(unittest.TestCase):
    def runtime_cli(
        self,
        repository: Path,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(RUNTIME), str(repository), *args],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def run_handoff(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def create_run(self, repository: Path, *, complete: bool) -> Path:
        skill = "ai-sdlc-validation"
        step_id = "validate"
        graph_fingerprint = "b" * 64
        task = {
            "id": "T001",
            "schema": "ai-sdlc-step-card/v1",
            "skill": skill,
            "step_id": step_id,
            "path": "steps/03-validate-and-handoff.md",
            "step_type": "validation",
            "status": "pending",
            "depends_on": [],
            "operation": "validate-evidence",
            "capabilities": ["filesystem.read"],
            "side_effect": "none",
            "context": context_pack(skill, step_id),
            "gates": ["acceptance"],
            "outputs": ["validation-evidence"],
            "max_attempts": 1,
            "max_tokens": 100,
            "commit_boundary": "none",
            "on_failure": "block",
            "load": "required",
            "reason": "validate evidence before the handoff",
            "ready": True,
            "graph_fingerprint": graph_fingerprint,
            "step_fingerprint": HASH_A,
            "idempotency_scope": (
                f"{skill}:{step_id}:{graph_fingerprint}"
            ),
        }
        semantic = {
            "schema": "ai-sdlc-run-plan/v2",
            "skill": "ai-sdlc-validation",
            "entrypoint": "validate",
            "role": "qa-engineer",
            "action": "validation",
            "manifest_fingerprint": HASH_A,
            "graph_fingerprint": graph_fingerprint,
            "selection_fingerprint": "c" * 64,
            "targets": ["validate"],
            "budgets": {
                "max_steps": 1,
                "max_failures": 1,
                "max_tokens": 100,
            },
            "tasks": [task],
        }
        plan = {**semantic, "fingerprint": digest(semantic)}
        plan_path = repository / "plan.toon"
        plan_path.write_text(toon_codec.encode_toon(plan), encoding="utf-8")
        started = self.runtime_cli(
            repository,
            "--start",
            "--run-id",
            "run-1",
            "--plan",
            str(plan_path),
        )
        self.assertEqual(started.returncode, 0, started.stdout + started.stderr)
        if complete:
            self.assertEqual(
                self.runtime_cli(
                    repository,
                    "--next",
                    "--run-id",
                    "run-1",
                ).returncode,
                0,
            )
            completed = self.runtime_cli(
                repository,
                "--record",
                "--run-id",
                "run-1",
                "--task",
                "T001",
                "--outcome",
                "succeeded",
                "--result-fingerprint",
                HASH_A,
                "--tokens",
                "5",
                "--evidence",
                "tests:passed",
            )
            self.assertEqual(
                completed.returncode,
                0,
                completed.stdout + completed.stderr,
            )
        return repository / "_ai_sdlc/runs/run-1"

    def test_complete_handoff_contains_run_evidence_and_next_action(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir = self.create_run(Path(temp), complete=True)
            result = self.run_handoff(
                "--run-dir",
                str(run_dir),
                "--current-owner",
                "QA",
                "--next-required",
                "ai-sdlc-commit-prep|Prepare commit|Use commit prep|commit-readiness.md",
                "--next-optional",
                "ai-sdlc-security-testing|Review boundaries|Use security testing|security-review.md",
                "--format",
                "toon",
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            value = toon_codec.loads(result.stdout)
            self.assertEqual(value["schema"], "ai-sdlc-handoff/v2")
            self.assertEqual(value["result"], "complete")
            self.assertEqual(value["steps"][0]["status"], "succeeded")
            self.assertEqual(value["steps"][0]["evidence"], ["tests:passed"])
            self.assertEqual(
                value["next_required"]["skill"],
                "ai-sdlc-commit-prep",
            )

    def test_stale_state_projection_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            run_dir = self.create_run(Path(temp), complete=False)
            (run_dir / "state.toon").write_text("corrupt\n", encoding="utf-8")
            result = self.run_handoff(
                "--run-dir",
                str(run_dir),
                "--current-owner",
                "Dev",
                "--next-required",
                "ai-sdlc-runtime|Resume run|Use runtime resume|state.toon",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("resume the run first", result.stdout)

    def test_every_skill_documents_handoff_v2(self) -> None:
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=skill):
                text = contract_text(skill)
                self.assertIn("ai-sdlc-handoff/v2", text)
                self.assertIn("next_required", text)
                self.assertIn("next_optional", text)


if __name__ == "__main__":
    unittest.main()
