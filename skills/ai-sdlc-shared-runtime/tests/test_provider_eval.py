#!/usr/bin/env python3
"""Tests for strict provider execution receipt validation."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills/ai-sdlc-shared-runtime/scripts"
sys.path.insert(0, str(SCRIPTS))

import ai_sdlc_provider_eval as provider_eval  # noqa: E402
import ai_sdlc_skill_eval as skill_eval  # noqa: E402


class ProviderEvalTests(unittest.TestCase):
    def protocol(self) -> dict[str, object]:
        return skill_eval.live_protocol_receipt(ROOT / "skills")

    def observation(self, protocol: dict[str, object]) -> dict[str, object]:
        live = protocol["protocol"]
        assert isinstance(live, dict)
        return {
            "schema": provider_eval.OBSERVATION_SCHEMA,
            "execution_mode": "provider",
            "protocol_fingerprint": provider_eval.digest(live),
            "provider": "fixture-provider",
            "host": "fixture-host",
            "model": "fixture-model",
            "execution_id": "fixture:tc-012:1",
            "executed_at": "2026-08-03T00:00:00+03:00",
            "scenario_version": live["scenario_version"],
            "agent_attested": True,
            "scenario_results": [
                {"id": scenario["id"], "status": "passed", "score": 100,
                 "evidence": [f"fixture:{scenario['id']}"]}
                for scenario in live["scenarios"]
            ],
            "effect_receipts": ["fixture:effect:1"],
            "recovery_evidence": ["fixture:recovery:1"],
        }

    def test_complete_attested_provider_execution_passes_byte_stably(self) -> None:
        protocol = self.protocol()
        observation = self.observation(protocol)
        first = provider_eval.receipt(protocol, observation)
        second = provider_eval.receipt(protocol, observation)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "passed")
        self.assertTrue(first["agent_attested"])
        self.assertEqual(first["scenario_version"], "tc-012/v1")
        self.assertEqual(first["thresholds"], protocol["protocol"]["thresholds"])

    def test_unattested_execution_stays_pending(self) -> None:
        protocol = self.protocol()
        observation = self.observation(protocol)
        observation["agent_attested"] = False
        result = provider_eval.receipt(protocol, observation)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["execution_mode"], "offline-or-unattested")

    def test_incomplete_or_contradictory_results_are_rejected(self) -> None:
        protocol = self.protocol()
        incomplete = self.observation(protocol)
        incomplete["scenario_results"] = incomplete["scenario_results"][:-1]
        with self.assertRaisesRegex(ValueError, "complete scenario set"):
            provider_eval.receipt(protocol, incomplete)
        contradictory = self.observation(protocol)
        contradictory["scenario_results"][0]["score"] = 0
        with self.assertRaisesRegex(ValueError, "contradicts score"):
            provider_eval.receipt(protocol, contradictory)

    def test_protocol_binding_and_timestamp_are_strict(self) -> None:
        protocol = self.protocol()
        wrong = self.observation(protocol)
        wrong["protocol_fingerprint"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
            provider_eval.receipt(protocol, wrong)
        bad_time = self.observation(protocol)
        bad_time["executed_at"] = "2026-08-03"
        with self.assertRaisesRegex(ValueError, "include an offset"):
            provider_eval.receipt(protocol, bad_time)


if __name__ == "__main__":
    unittest.main()
