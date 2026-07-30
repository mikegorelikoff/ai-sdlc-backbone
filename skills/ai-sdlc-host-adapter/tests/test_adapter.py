#!/usr/bin/env python3
"""Tests for StepCard-aware host adapter v2 negotiation."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills/ai-sdlc-host-adapter"
SCRIPT = SKILL / "scripts/adapter.py"
FIXTURES = SKILL / "references/fixtures"


def digest(value: object) -> str:
    return hashlib.sha256(toon_codec.encode_toon(value).encode("utf-8")).hexdigest()


def context_pack(skill: str, step_id: str) -> dict[str, object]:
    content = (
        "# Execute\n\n## Entry\n\nInspect inputs.\n\n"
        "## Procedure\n\nExecute the approved action.\n\n"
        "## Exit\n\nReturn evidence.\n"
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
        "reason": "direct read preserves all execution instructions",
        "selected": [
            {
                "path": path,
                "sha256": "c" * 64,
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


class AdapterTests(unittest.TestCase):
    def card(
        self,
        *,
        step_type: str = "action",
        side_effect: str = "workspace-write",
        ready: bool = True,
    ) -> dict[str, object]:
        skill = "ai-sdlc-sdd"
        step_id = "execute"
        graph_fingerprint = "a" * 64
        return {
            "schema": "ai-sdlc-step-card/v1",
            "skill": skill,
            "step_id": step_id,
            "path": "steps/02-execute.md",
            "step_type": step_type,
            "depends_on": ["context"],
            "operation": "execute-procedure",
            "capabilities": ["filesystem.read"],
            "side_effect": side_effect,
            "gates": ["authorization"],
            "outputs": ["execution-evidence"],
            "max_attempts": 1,
            "commit_boundary": "after-step",
            "on_failure": "block",
            "load": "required",
            "reason": "execute the approved procedure",
            "context": context_pack(skill, step_id),
            "ready": ready,
            "graph_fingerprint": graph_fingerprint,
            "step_fingerprint": "b" * 64,
            "idempotency_scope": (
                f"{skill}:{step_id}:{graph_fingerprint}"
            ),
        }

    def request(
        self,
        repository: Path,
        card: dict[str, object],
        *,
        concurrency: int = 4,
        isolation: bool = True,
    ) -> Path:
        path = repository / "request.toon"
        path.write_text(
            toon_codec.encode_toon(
                {
                    "schema": "ai-sdlc-capability-request/v2",
                    "step_card": card,
                    "concurrency": concurrency,
                    "isolation_required": isolation,
                }
            ),
            encoding="utf-8",
        )
        return path

    def cli(
        self,
        repository: Path,
        adapter: str,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3",
                str(SCRIPT),
                str(repository),
                "--adapter",
                str(FIXTURES / adapter),
                *args,
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_full_host_maps_step_card_and_evidence_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, self.card())
            result = self.cli(
                repository,
                "full-host.toon",
                "--negotiate",
                "--request",
                str(request),
                "--write",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            value = toon_codec.loads(result.stdout)
            self.assertTrue(value["compatible"])
            self.assertEqual(value["mapping"]["portable"], "step.action")
            self.assertEqual(value["side_effect"], "workspace-write")
            self.assertIn("filesystem.write", value["required_capabilities"])
            self.assertTrue(value["evidence_required"])
            self.assertEqual(
                value["idempotency_scope"],
                f"ai-sdlc-sdd:execute:{'a' * 64}",
            )
            self.assertTrue(
                (
                    repository
                    / "_ai_sdlc/adapters/full-host/negotiation.toon"
                ).is_file()
            )

    def test_sequential_host_clamps_concurrency(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, self.card(), concurrency=8)
            first = self.cli(
                repository,
                "sequential-host.toon",
                "--negotiate",
                "--request",
                str(request),
            )
            second = self.cli(
                repository,
                "sequential-host.toon",
                "--negotiate",
                "--request",
                str(request),
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            value = toon_codec.loads(first.stdout)
            self.assertEqual(value["limits"]["effective_concurrency"], 1)
            reasons = [item["reason"] for item in value["fallbacks"]]
            self.assertIn("host-concurrency-clamped", reasons)
            self.assertIn("sequential-isolation-fallback", reasons)

    def test_read_only_host_rejects_write_step(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, self.card())
            result = self.cli(
                repository,
                "read-only-host.toon",
                "--negotiate",
                "--request",
                str(request),
            )
            self.assertEqual(result.returncode, 2)
            value = toon_codec.loads(result.stdout)
            self.assertFalse(value["compatible"])
            self.assertIn("step.action", value["unsupported_operations"])
            self.assertIn("filesystem.write", value["missing_capabilities"])

    def test_not_ready_and_legacy_contracts_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            request = self.request(repository, self.card(ready=False))
            result = self.cli(
                repository,
                "full-host.toon",
                "--negotiate",
                "--request",
                str(request),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("context-ready", result.stdout)
            adapter = toon_codec.loads(
                (FIXTURES / "full-host.toon").read_text(encoding="utf-8")
            )
            adapter["schema"] = "ai-sdlc-host-adapter/legacy"
            path = repository / "legacy.toon"
            path.write_text(toon_codec.encode_toon(adapter), encoding="utf-8")
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    str(repository),
                    "--adapter",
                    str(path),
                    "--validate",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                check=False,
            )
            self.assertIn("ADAPTER_SCHEMA_MISMATCH", result.stdout)


if __name__ == "__main__":
    unittest.main()
