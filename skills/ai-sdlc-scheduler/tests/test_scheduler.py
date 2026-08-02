#!/usr/bin/env python3
"""Focused deterministic scheduler tests."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/scheduler.py"
SPEC = importlib.util.spec_from_file_location("ai_sdlc_scheduler", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
SCHEDULER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCHEDULER)


def plan() -> dict:
    context = "a" * 64
    graph = "b" * 64
    tasks = []
    for task_id, dependencies in (("task-a", []), ("task-b", ["task-a"])):
        tasks.append({
            "id": task_id,
            "depends_on": dependencies,
            "context": {"fingerprint": context},
            "step_fingerprint": graph,
            "max_attempts": 2,
        })
    return {"schema": "ai-sdlc-run-plan/v2", "fingerprint": "c" * 64, "tasks": tasks}


class SchedulerTests(unittest.TestCase):
    def create(self, directory: str) -> tuple[Path, dict]:
        state_path = Path(directory) / "scheduler.toon"
        state = SCHEDULER.initial_state("run-1", plan(), 100)
        SCHEDULER.atomic_write(state_path, state)
        return state_path, state

    def test_claim_is_deterministic_and_revision_guarded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, state = self.create(directory)
            claimed = SCHEDULER.mutate(
                state_path, 0, 100,
                SCHEDULER.claim_action("worker-a", 30, "a" * 64, 100),
            )
            self.assertEqual(claimed["tasks"][0]["status"], "leased")
            self.assertEqual(claimed["tasks"][0]["lease"]["nonce"], SCHEDULER.digest({
                "run": "run-1", "task": "task-a", "worker": "worker-a", "attempt": 1, "revision": 0,
            }))
            with self.assertRaisesRegex(ValueError, "revision mismatch"):
                SCHEDULER.mutate(
                    state_path, state["revision"], 100,
                    SCHEDULER.claim_action("worker-b", 30, "a" * 64, 100),
                )

    def test_expired_lease_recovers_without_terminal_duplication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, _ = self.create(directory)
            claimed = SCHEDULER.mutate(
                state_path, 0, 100,
                SCHEDULER.claim_action("worker-a", 10, "a" * 64, 100),
            )
            recovered = SCHEDULER.mutate(
                state_path, claimed["revision"], 111,
                SCHEDULER.recovery_action(111),
            )
            self.assertEqual(recovered["ready"], ["task-a"])
            self.assertEqual(recovered["tasks"][0]["attempts"], 1)
            self.assertEqual(recovered["tasks"][0]["terminal"], {})

    def test_stale_context_fails_before_lease(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, original = self.create(directory)
            with self.assertRaisesRegex(ValueError, "stale context"):
                SCHEDULER.mutate(
                    state_path, 0, 100,
                    SCHEDULER.claim_action("worker-a", 10, "d" * 64, 100),
                )
            self.assertEqual(SCHEDULER.read_toon(state_path), original)

    def test_stale_worker_cannot_commit_after_reclaim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, _ = self.create(directory)
            first = SCHEDULER.mutate(
                state_path, 0, 100,
                SCHEDULER.claim_action("worker-a", 10, "a" * 64, 100),
            )
            old_nonce = first["tasks"][0]["lease"]["nonce"]
            recovered = SCHEDULER.mutate(
                state_path, 1, 111,
                SCHEDULER.recovery_action(111),
            )
            second = SCHEDULER.mutate(
                state_path, recovered["revision"], 111,
                SCHEDULER.claim_action("worker-b", 10, "a" * 64, 111),
            )
            with self.assertRaisesRegex(ValueError, "stale or foreign"):
                SCHEDULER.mutate(
                    state_path, second["revision"], 112,
                    SCHEDULER.terminal_action("task-a", "worker-a", old_nonce, "succeeded", "e" * 64, 112),
                )

    def test_replay_reconstructs_projection_and_rejects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, _ = self.create(directory)
            claimed = SCHEDULER.mutate(
                state_path, 0, 100,
                SCHEDULER.claim_action("worker-a", 10, "a" * 64, 100),
            )
            self.assertEqual(SCHEDULER.replay_state(claimed), claimed)
            tampered = dict(claimed)
            tampered["ready"] = ["task-b"]
            tampered = SCHEDULER.fingerprinted(tampered)
            with self.assertRaisesRegex(ValueError, "projection differs"):
                SCHEDULER.validate_state(tampered)

    def test_attempt_budget_exhaustion_is_terminal_and_replayable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, _ = self.create(directory)
            first = SCHEDULER.mutate(state_path, 0, 100, SCHEDULER.claim_action("worker-a", 1, "a" * 64, 100))
            recovered = SCHEDULER.mutate(state_path, first["revision"], 101, SCHEDULER.recovery_action(101))
            second = SCHEDULER.mutate(state_path, recovered["revision"], 101, SCHEDULER.claim_action("worker-b", 1, "a" * 64, 101))
            recovered_again = SCHEDULER.mutate(state_path, second["revision"], 102, SCHEDULER.recovery_action(102))
            exhausted = SCHEDULER.mutate(state_path, recovered_again["revision"], 102, SCHEDULER.claim_action("worker-c", 1, "a" * 64, 102))
            self.assertEqual(exhausted["tasks"][0]["status"], "blocked")
            self.assertEqual(exhausted["status"], "blocked")
            self.assertEqual(SCHEDULER.replay_state(exhausted), exhausted)

    def test_heartbeat_extends_only_a_live_matching_lease(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, _ = self.create(directory)
            claimed = SCHEDULER.mutate(state_path, 0, 100, SCHEDULER.claim_action("worker-a", 10, "a" * 64, 100))
            nonce = claimed["tasks"][0]["lease"]["nonce"]
            extended = SCHEDULER.mutate(
                state_path, claimed["revision"], 105,
                SCHEDULER.heartbeat_action("task-a", "worker-a", nonce, 20, 105),
            )
            self.assertEqual(extended["tasks"][0]["lease"]["expires_at"], 125)
            self.assertEqual(SCHEDULER.replay_state(extended), extended)
            with self.assertRaisesRegex(ValueError, "expired lease"):
                SCHEDULER.mutate(
                    state_path, extended["revision"], 125,
                    SCHEDULER.heartbeat_action("task-a", "worker-a", nonce, 20, 125),
                )

    def test_parallelism_bound_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ready_plan = plan()
            ready_plan["tasks"][1]["depends_on"] = []
            state_path = Path(directory) / "scheduler.toon"
            SCHEDULER.atomic_write(state_path, SCHEDULER.initial_state("run-1", ready_plan, 100, max_parallelism=1))
            claimed = SCHEDULER.mutate(state_path, 0, 100, SCHEDULER.claim_action("worker-a", 30, "a" * 64, 100))
            with self.assertRaisesRegex(ValueError, "parallelism limit"):
                SCHEDULER.mutate(state_path, 1, 100, SCHEDULER.claim_action("worker-b", 30, "a" * 64, 100))

    def test_concurrent_processes_issue_one_lease_for_one_revision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_path, _ = self.create(directory)
            command = [
                sys.executable, str(SCRIPT), "claim", "--state", str(state_path),
                "--expected-revision", "0", "--worker", "worker-a",
                "--lease-seconds", "30", "--context-fingerprint", "a" * 64, "--now", "100",
            ]
            first = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            second_command = command.copy()
            second_command[second_command.index("worker-a")] = "worker-b"
            second = subprocess.Popen(second_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            first.communicate(timeout=10)
            second.communicate(timeout=10)
            self.assertEqual(sorted([first.returncode, second.returncode]), [0, 1])
            final = SCHEDULER.validate_state(SCHEDULER.read_toon(state_path))
            self.assertEqual(sum(task["status"] == "leased" for task in final["tasks"]), 1)


if __name__ == "__main__":
    unittest.main()
