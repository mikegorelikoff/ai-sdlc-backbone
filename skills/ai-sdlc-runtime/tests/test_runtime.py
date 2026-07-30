#!/usr/bin/env python3
"""Tests for the TOON-only resumable v2 runtime."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-runtime/scripts/runtime.py"
HASH_A = "a" * 64
HASH_B = "b" * 64


def digest(value: object) -> str:
    return hashlib.sha256(toon_codec.encode_toon(value).encode("utf-8")).hexdigest()


def context_pack(
    skill: str,
    step_id: str,
    source_fingerprint: str,
) -> dict[str, object]:
    content = (
        "# Fixture\n\n## Entry\n\nUse bounded input.\n\n"
        "## Procedure\n\nExecute deterministically.\n\n"
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
        "reason": "direct read preserves complete fixture instructions",
        "selected": [
            {
                "path": path,
                "sha256": source_fingerprint,
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


class RuntimeTests(unittest.TestCase):
    """Exercise journals, readiness, idempotency, retries, and recovery."""

    def cli(self, repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3",
                str(SCRIPT),
                str(repository),
                *args,
                "--format",
                "toon",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def task(
        self,
        task_id: str,
        *,
        depends_on: list[str],
        side_effect: str,
        commit_boundary: str,
        attempts: int,
        failure: str,
        fingerprint: str,
    ) -> dict[str, object]:
        step_id = task_id.lower()
        skill = "ai-sdlc-fixture"
        return {
            "id": task_id,
            "schema": "ai-sdlc-step-card/v1",
            "skill": skill,
            "step_id": step_id,
            "path": f"steps/{step_id}.md",
            "step_type": "action",
            "status": "pending",
            "depends_on": depends_on,
            "operation": f"run-{step_id}",
            "capabilities": ["filesystem.read"],
            "side_effect": side_effect,
            "context": context_pack(skill, step_id, fingerprint),
            "gates": ["fixture-ready"],
            "outputs": ["fixture-evidence"],
            "max_attempts": attempts,
            "max_tokens": 100,
            "commit_boundary": commit_boundary,
            "on_failure": failure,
            "load": "required",
            "reason": "execute the bounded runtime fixture",
            "ready": True,
            "graph_fingerprint": HASH_B,
            "step_fingerprint": fingerprint,
            "idempotency_scope": f"{skill}:{step_id}:{HASH_B}",
        }

    def plan(
        self,
        repository: Path,
        *,
        two_tasks: bool = True,
        attempts: int = 2,
        failure: str = "retry",
        max_steps: int = 4,
        max_failures: int = 3,
        max_tokens: int = 200,
    ) -> Path:
        tasks = [
            self.task(
                "T001",
                depends_on=[],
                side_effect="workspace-write",
                commit_boundary="after-step",
                attempts=attempts,
                failure=failure,
                fingerprint=HASH_A,
            )
        ]
        if two_tasks:
            tasks.append(
                self.task(
                    "T002",
                    depends_on=["T001"],
                    side_effect="none",
                    commit_boundary="none",
                    attempts=1,
                    failure="block",
                    fingerprint=HASH_B,
                )
            )
        semantic = {
            "schema": "ai-sdlc-run-plan/v2",
            "skill": "ai-sdlc-fixture",
            "entrypoint": "execute",
            "role": "software-engineer",
            "action": "fixture",
            "manifest_fingerprint": HASH_A,
            "graph_fingerprint": HASH_B,
            "selection_fingerprint": "c" * 64,
            "targets": ["t001"],
            "budgets": {
                "max_steps": max_steps,
                "max_failures": max_failures,
                "max_tokens": max_tokens,
            },
            "tasks": tasks,
        }
        value = {**semantic, "fingerprint": digest(semantic)}
        path = repository / "plan.toon"
        path.write_text(toon_codec.encode_toon(value), encoding="utf-8")
        return path

    def start(self, repository: Path, plan: Path) -> dict[str, object]:
        result = self.cli(
            repository,
            "--start",
            "--run-id",
            "run-1",
            "--plan",
            str(plan),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return toon_codec.loads(result.stdout)

    def start_task(self, repository: Path) -> dict[str, object]:
        result = self.cli(repository, "--next", "--run-id", "run-1")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return toon_codec.loads(result.stdout)

    def succeed_first(self, repository: Path) -> dict[str, object]:
        result = self.cli(
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
            "10",
            "--commit",
            "abcdef1",
            "--evidence",
            "tests:passed",
            "--effect-receipt",
            "workspace-effect-1",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return toon_codec.loads(result.stdout)

    def test_dependency_readiness_and_complete_event_set(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository))
            first = self.start_task(repository)
            self.assertEqual(first["state"]["running_task"], "T001")
            self.assertNotIn("T002", first["state"]["ready_tasks"])
            success = self.succeed_first(repository)
            self.assertEqual(success["state"]["ready_tasks"], ["T002"])
            self.start_task(repository)
            completed = toon_codec.loads(
                self.cli(
                    repository,
                    "--record",
                    "--run-id",
                    "run-1",
                    "--task",
                    "T002",
                    "--outcome",
                    "succeeded",
                    "--result-fingerprint",
                    HASH_B,
                    "--tokens",
                    "5",
                    "--evidence",
                    "validation:passed",
                ).stdout
            )
            self.assertEqual(completed["state"]["status"], "completed")
            journal = repository / "_ai_sdlc/runs/run-1/journal"
            events = [
                toon_codec.loads(path.read_text(encoding="utf-8"))
                for path in sorted(journal.glob("*.toon"))
            ]
            for task_id in ("T001", "T002"):
                types = [
                    event["type"]
                    for event in events
                    if event["task_id"] == task_id
                ]
                self.assertEqual(
                    types,
                    [
                        "task-planned",
                        "task-started",
                        "task-terminal",
                        "task-evidence",
                        "task-result",
                    ],
                )

    def test_next_and_result_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            first = self.start_task(repository)
            second = toon_codec.loads(
                self.cli(repository, "--next", "--run-id", "run-1").stdout
            )
            self.assertTrue(second["idempotent"])
            self.assertEqual(first["state"]["sequence"], second["state"]["sequence"])
            recorded = self.succeed_first(repository)
            repeated = self.succeed_first(repository)
            self.assertTrue(repeated["idempotent"])
            self.assertEqual(
                recorded["state"]["sequence"],
                repeated["state"]["sequence"],
            )

    def test_completion_replay_rejects_evidence_or_effect_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            self.start_task(repository)
            completed = self.succeed_first(repository)
            sequence = completed["state"]["sequence"]
            changed_evidence = self.cli(
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
                "10",
                "--commit",
                "abcdef1",
                "--evidence",
                "tests:different",
                "--effect-receipt",
                "workspace-effect-1",
            )
            self.assertEqual(changed_evidence.returncode, 1)
            self.assertIn("idempotency replay payload", changed_evidence.stdout)
            changed_effect = self.cli(
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
                "10",
                "--commit",
                "abcdef1",
                "--evidence",
                "tests:passed",
                "--effect-receipt",
                "workspace-effect-2",
            )
            self.assertEqual(changed_effect.returncode, 1)
            self.assertIn("idempotency replay payload", changed_effect.stdout)
            status = toon_codec.loads(
                self.cli(repository, "--status", "--run-id", "run-1").stdout
            )
            self.assertEqual(status["state"]["sequence"], sequence)

    def test_completion_resumes_after_durable_effect_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            started = self.start_task(repository)["state"]
            task = next(item for item in started["tasks"] if item["id"] == "T001")
            record = {
                "outcome": "succeeded",
                "result_fingerprint": HASH_A,
                "tokens": 10,
                "commit": "abcdef1",
                "reason": "",
            }
            evidence = ["tests:passed"]
            effect_receipt = "workspace-effect-1"
            completion = digest(
                {
                    "schema": "ai-sdlc-task-completion/v1",
                    "record": record,
                    "evidence": evidence,
                    "effect_receipt": effect_receipt,
                }
            )
            journal = repository / "_ai_sdlc/runs/run-1/journal"
            previous = started["event_fingerprint"]
            for sequence, event_type, payload in (
                (
                    4,
                    "task-terminal",
                    {
                        "outcome": "succeeded",
                        "completion_fingerprint": completion,
                    },
                ),
                (
                    5,
                    "task-evidence",
                    {
                        "evidence": evidence,
                        "effect_receipt": effect_receipt,
                    },
                ),
            ):
                semantic = {
                    "schema": "ai-sdlc-run-event/v2",
                    "seq": sequence,
                    "type": event_type,
                    "run_id": "run-1",
                    "task_id": "T001",
                    "attempt": 1,
                    "idempotency_key": task["idempotency_key"],
                    "payload": payload,
                    "previous": previous,
                }
                event = {**semantic, "fingerprint": digest(semantic)}
                (journal / f"{sequence:06d}.toon").write_text(
                    toon_codec.encode_toon(event),
                    encoding="utf-8",
                )
                previous = event["fingerprint"]

            resumed = self.succeed_first(repository)
            self.assertEqual(resumed["state"]["status"], "completed")
            self.assertEqual(resumed["state"]["sequence"], 6)
            types = [
                toon_codec.loads(path.read_text(encoding="utf-8"))["type"]
                for path in sorted(journal.glob("*.toon"))
            ]
            self.assertEqual(
                types,
                [
                    "run-started",
                    "task-planned",
                    "task-started",
                    "task-terminal",
                    "task-evidence",
                    "task-result",
                ],
            )

    def test_idempotency_key_and_effect_receipt_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            started = self.start_task(repository)
            key = next(
                task["idempotency_key"]
                for task in started["state"]["tasks"]
                if task["id"] == "T001"
            )
            missing = self.cli(
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
                "1",
                "--commit",
                "abcdef1",
            )
            self.assertIn("effect receipt", missing.stdout)
            mismatch = self.cli(
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
                "1",
                "--commit",
                "abcdef1",
                "--effect-receipt",
                "effect-1",
                "--idempotency-key",
                "f" * 64,
            )
            self.assertIn("idempotency key", mismatch.stdout)
            self.assertRegex(key, r"^[a-f0-9]{64}$")

    def test_retry_cannot_bypass_a_stopped_failure_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(
                repository,
                self.plan(
                    repository,
                    two_tasks=False,
                    attempts=2,
                    max_failures=1,
                ),
            )
            self.start_task(repository)
            stopped = toon_codec.loads(
                self.cli(
                    repository,
                    "--record",
                    "--run-id",
                    "run-1",
                    "--task",
                    "T001",
                    "--outcome",
                    "failed",
                    "--tokens",
                    "1",
                    "--reason",
                    "fixture failure",
                ).stdout
            )
            self.assertEqual(stopped["state"]["status"], "stopped")
            retry = self.cli(
                repository,
                "--retry",
                "T001",
                "--run-id",
                "run-1",
                "--reason",
                "must not bypass budget",
            )
            self.assertEqual(retry.returncode, 1)
            self.assertIn("illegal retry transition", retry.stdout)

    def test_retry_policy_and_attempt_limit_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(
                repository,
                self.plan(repository, two_tasks=False, attempts=2),
            )
            self.start_task(repository)
            failed = toon_codec.loads(
                self.cli(
                    repository,
                    "--record",
                    "--run-id",
                    "run-1",
                    "--task",
                    "T001",
                    "--outcome",
                    "failed",
                    "--tokens",
                    "1",
                    "--reason",
                    "fixture failure",
                ).stdout
            )
            self.assertEqual(failed["state"]["status"], "paused")
            retried = toon_codec.loads(
                self.cli(
                    repository,
                    "--retry",
                    "T001",
                    "--run-id",
                    "run-1",
                    "--reason",
                    "safe retry",
                ).stdout
            )
            self.assertEqual(retried["state"]["ready_tasks"], ["T001"])
            self.start_task(repository)
            self.cli(
                repository,
                "--record",
                "--run-id",
                "run-1",
                "--task",
                "T001",
                "--outcome",
                "failed",
                "--tokens",
                "1",
                "--reason",
                "fixture failure again",
            )
            exhausted = self.cli(
                repository,
                "--retry",
                "T001",
                "--run-id",
                "run-1",
                "--reason",
                "unsafe extra retry",
            )
            self.assertEqual(exhausted.returncode, 1)
            self.assertIn("exhausted max attempts", exhausted.stdout)

    def test_commit_boundary_rejects_without_writing_events(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            started = self.start_task(repository)
            rejected = self.cli(
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
                "2",
                "--effect-receipt",
                "effect-1",
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("commit evidence", rejected.stdout)
            malformed = self.cli(
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
                "2",
                "--commit",
                "not-a-commit",
                "--effect-receipt",
                "effect-1",
            )
            self.assertEqual(malformed.returncode, 1)
            self.assertIn("commit evidence", malformed.stdout)
            status = toon_codec.loads(
                self.cli(repository, "--status", "--run-id", "run-1").stdout
            )
            self.assertEqual(
                status["state"]["sequence"],
                started["state"]["sequence"],
            )

    def test_resume_repairs_projection_from_valid_journal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            self.start_task(repository)
            state_path = repository / "_ai_sdlc/runs/run-1/state.toon"
            state_path.write_text("broken:\n   indentation\n", encoding="utf-8")
            resumed_result = self.cli(
                repository,
                "--resume",
                "--run-id",
                "run-1",
            )
            self.assertEqual(
                resumed_result.returncode,
                0,
                resumed_result.stdout + resumed_result.stderr,
            )
            resumed = toon_codec.loads(resumed_result.stdout)
            self.assertTrue(resumed["recovered"])
            saved = toon_codec.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["fingerprint"], resumed["state"]["fingerprint"])

    def test_corrupt_journal_and_duplicate_start_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan = self.plan(repository, two_tasks=False)
            self.start(repository, plan)
            duplicate = self.cli(
                repository,
                "--start",
                "--run-id",
                "run-1",
                "--plan",
                str(plan),
            )
            self.assertEqual(duplicate.returncode, 1)
            first_event = (
                repository / "_ai_sdlc/runs/run-1/journal/000001.toon"
            )
            event = toon_codec.loads(first_event.read_text(encoding="utf-8"))
            event["payload"]["plan_fingerprint"] = HASH_B
            first_event.write_text(
                toon_codec.encode_toon(event),
                encoding="utf-8",
            )
            resumed = self.cli(repository, "--resume", "--run-id", "run-1")
            self.assertEqual(resumed.returncode, 1)
            self.assertIn("fingerprint mismatch", resumed.stdout)

    def test_journal_rejects_evidence_before_terminal_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            self.start(repository, self.plan(repository, two_tasks=False))
            started = self.start_task(repository)["state"]
            task = next(item for item in started["tasks"] if item["id"] == "T001")
            semantic = {
                "schema": "ai-sdlc-run-event/v2",
                "seq": 4,
                "type": "task-evidence",
                "run_id": "run-1",
                "task_id": "T001",
                "attempt": 1,
                "idempotency_key": task["idempotency_key"],
                "payload": {
                    "evidence": ["out-of-order"],
                    "effect_receipt": "workspace-effect-1",
                },
                "previous": started["event_fingerprint"],
            }
            event = {**semantic, "fingerprint": digest(semantic)}
            journal = repository / "_ai_sdlc/runs/run-1/journal"
            (journal / "000004.toon").write_text(
                toon_codec.encode_toon(event),
                encoding="utf-8",
            )
            result = self.cli(repository, "--status", "--run-id", "run-1")
            self.assertEqual(result.returncode, 1)
            self.assertIn("illegal task-evidence transition", result.stdout)

    def test_symlinked_runtime_parent_cannot_escape_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            repository = Path(temp)
            (repository / "_ai_sdlc").symlink_to(
                Path(outside),
                target_is_directory=True,
            )
            plan = self.plan(repository, two_tasks=False)
            result = self.cli(
                repository,
                "--start",
                "--run-id",
                "run-1",
                "--plan",
                str(plan),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("symlink", result.stdout)
            self.assertFalse((Path(outside) / "runs/run-1/state.toon").exists())

    def test_tampered_context_pack_fails_before_run_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repository = Path(temp)
            plan_path = self.plan(repository, two_tasks=False)
            plan = toon_codec.loads(plan_path.read_text(encoding="utf-8"))
            plan["tasks"][0]["context"]["reason"] = "tampered"
            semantic = dict(plan)
            semantic.pop("fingerprint")
            plan["fingerprint"] = digest(semantic)
            plan_path.write_text(
                toon_codec.encode_toon(plan),
                encoding="utf-8",
            )
            result = self.cli(
                repository,
                "--start",
                "--run-id",
                "run-1",
                "--plan",
                str(plan_path),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("context failed validation", result.stdout)
            self.assertFalse((repository / "_ai_sdlc/runs/run-1").exists())


if __name__ == "__main__":
    unittest.main()
