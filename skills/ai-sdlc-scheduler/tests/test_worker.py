#!/usr/bin/env python3
"""Integration tests for scheduler-to-runtime worker dispatch."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


WORKER = module("scheduler_worker_test", ROOT / "skills/ai-sdlc-scheduler/scripts/worker.py")
RUNTIME_FIXTURE = module("runtime_fixture_for_worker", ROOT / "skills/ai-sdlc-runtime/tests/test_runtime.py")


class WorkerTests(unittest.TestCase):
    def test_dispatch_runs_one_step_and_compare_commits_scheduler(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            plan_path = RUNTIME_FIXTURE.RuntimeTests().plan(repository)
            plan = WORKER.SCHEDULER.read_toon(plan_path)
            state_path = repository / "_ai_sdlc/scheduler/run-1/state.toon"
            WORKER.SCHEDULER.atomic_write(
                state_path,
                WORKER.SCHEDULER.initial_state("run-1", plan, 100),
            )
            dispatched = WORKER.dispatch(
                repository, plan_path, state_path, 0, "worker-a", 30, 100,
            )
            record = dispatched["dispatch"]
            self.assertEqual(record["task_id"], "T001")
            runtime_dir = repository / "_ai_sdlc/runs" / record["runtime_run_id"]
            runtime_plan, runtime_state, recovered = WORKER.RUNTIME.load_run(runtime_dir, record["runtime_run_id"])
            self.assertFalse(recovered)
            runtime_state, idempotent = WORKER.RUNTIME.record_task(
                runtime_dir,
                runtime_state,
                runtime_plan,
                "T001",
                {
                    "outcome": "succeeded",
                    "result_fingerprint": "d" * 64,
                    "tokens": 10,
                    "commit": "abcdef1",
                    "reason": "",
                },
                ["tests:passed"],
                "effect-receipt-1",
                "",
            )
            self.assertFalse(idempotent)
            committed = WORKER.commit(
                repository,
                repository / "_ai_sdlc/scheduler/run-1/dispatches" / f"{record['lease_nonce']}.toon",
                state_path,
                1,
                110,
            )
            self.assertEqual(committed["scheduler"]["tasks"][0]["status"], "succeeded")
            self.assertEqual(committed["scheduler"]["ready"], ["T002"])

    def test_commit_rejects_nonterminal_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            plan_path = RUNTIME_FIXTURE.RuntimeTests().plan(repository)
            plan = WORKER.SCHEDULER.read_toon(plan_path)
            state_path = repository / "_ai_sdlc/scheduler/run-1/state.toon"
            WORKER.SCHEDULER.atomic_write(state_path, WORKER.SCHEDULER.initial_state("run-1", plan, 100))
            dispatched = WORKER.dispatch(repository, plan_path, state_path, 0, "worker-a", 30, 100)
            dispatch_path = repository / "_ai_sdlc/scheduler/run-1/dispatches" / f"{dispatched['dispatch']['lease_nonce']}.toon"
            with self.assertRaisesRegex(ValueError, "not durably terminal"):
                WORKER.commit(repository, dispatch_path, state_path, 1, 101)

    def test_worker_rejects_state_outside_repository_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = root / "repository"
            repository.mkdir()
            plan_path = RUNTIME_FIXTURE.RuntimeTests().plan(repository)
            plan = WORKER.SCHEDULER.read_toon(plan_path)
            outside = root / "outside-state.toon"
            original = WORKER.SCHEDULER.initial_state("outside", plan, 100)
            WORKER.SCHEDULER.atomic_write(outside, original)
            with self.assertRaisesRegex(ValueError, "escapes repository"):
                WORKER.dispatch(repository, plan_path, outside, 0, "worker-a", 30, 100)
            self.assertEqual(WORKER.SCHEDULER.read_toon(outside), original)

    def test_commit_rejects_dispatch_bound_to_another_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            plan_path = RUNTIME_FIXTURE.RuntimeTests().plan(repository)
            plan = WORKER.SCHEDULER.read_toon(plan_path)
            first = repository / "_ai_sdlc/scheduler/run-1/state.toon"
            second = repository / "_ai_sdlc/scheduler/run-2/state.toon"
            WORKER.SCHEDULER.atomic_write(first, WORKER.SCHEDULER.initial_state("run-1", plan, 100))
            WORKER.SCHEDULER.atomic_write(second, WORKER.SCHEDULER.initial_state("run-2", plan, 100))
            dispatched = WORKER.dispatch(repository, plan_path, first, 0, "worker-a", 30, 100)
            dispatch_path = repository / "_ai_sdlc/scheduler/run-1/dispatches" / f"{dispatched['dispatch']['lease_nonce']}.toon"
            with self.assertRaisesRegex(ValueError, "not bound"):
                WORKER.commit(repository, dispatch_path, second, 0, 101)

    def test_dispatch_rejects_journal_definitions_that_differ_from_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            plan_path = RUNTIME_FIXTURE.RuntimeTests().plan(repository)
            plan = WORKER.SCHEDULER.read_toon(plan_path)
            state_path = repository / "_ai_sdlc/scheduler/run-1/state.toon"
            state = WORKER.SCHEDULER.initial_state("run-1", plan, 100)
            state["events"][0]["payload"]["tasks"][1]["depends_on"] = []
            event = state["events"][0]
            semantic_event = dict(event)
            semantic_event.pop("fingerprint")
            event["fingerprint"] = WORKER.SCHEDULER.digest(semantic_event)
            state["event_fingerprint"] = event["fingerprint"]
            state = WORKER.SCHEDULER.replay_state(state)
            WORKER.SCHEDULER.atomic_write(state_path, state)
            with self.assertRaisesRegex(ValueError, "definitions differ"):
                WORKER.dispatch(repository, plan_path, state_path, 0, "worker-a", 30, 100)


if __name__ == "__main__":
    unittest.main()
