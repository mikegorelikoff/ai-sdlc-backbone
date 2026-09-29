#!/usr/bin/env python3
"""Comprehensive test suite for unified AI SDLC Telemetry (Backbone).

Validates:
1. Pure TOON serialization (schema: ai-sdlc-telemetry/v1, ULID Crockford Base32, zero non-TOON files).
2. Zero token fabrication (strict usage_available=False and models=[] when unavailable).
3. User identity resolution (.customization.toon, ~/.config/ai-sdlc/config.toon, git/env fallback).
4. Secret redaction (bearer tokens, API keys, private keys).
5. POSIX flock concurrency and retry.
6. Fail-open exception shielding under filesystem/permission faults.
7. CLI commands (record, read, dump).
8. Automatic hook via usage_journal (record_skill_end and track_skill).
"""

from __future__ import annotations

import concurrent.futures
import fcntl
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

# Ensure shared runtime scripts are on path
_TEST_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _TEST_DIR.parent / "scripts"
import sys
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import ai_sdlc_telemetry as telemetry
import ai_sdlc_toon as toon_codec
import usage_journal


class TelemetryTests(unittest.TestCase):
    """Test suite covering the unified TelemetryEvent v1 contract."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.root = Path(self.temp_dir)
        self.telemetry_file = self.root / ".ai" / "telemetry" / "sessions.toon"

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pure_toon_serialization(self) -> None:
        """Verify TelemetryEvent v1 produces pure TOON in .ai/telemetry/sessions.toon with no non-TOON files."""
        ev = telemetry.record_telemetry_event(
            skill="ai-sdlc-specify",
            status="success",
            duration_ms=250,
            task={"id": "feat-100", "type": "feature", "title": "Add Telemetry", "owner": "Alice"},
            root=self.root,
        )
        self.assertIsNotNone(ev)
        self.assertEqual(ev["status"], "success")
        self.assertEqual(ev["duration_ms"], 250)
        self.assertTrue(self.telemetry_file.is_file())

        # Verify no non-TOON files created anywhere under .ai
        ai_dir = self.root / ".ai"
        for p in ai_dir.rglob("*"):
            if p.is_file():
                self.assertEqual(p.suffix, ".toon", f"Non-TOON file detected: {p}")

        # Verify valid TOON content and schema
        raw = self.telemetry_file.read_text(encoding="utf-8")
        self.assertTrue(raw.startswith("schema: ai-sdlc-telemetry/v1\nevents:\n"))

        decoded = toon_codec.loads(raw)
        self.assertEqual(decoded["schema"], "ai-sdlc-telemetry/v1")
        self.assertIn("events", decoded)
        events = decoded["events"]
        self.assertEqual(len(events), 1)

        event_id = ev["event_id"]
        self.assertIn(event_id, events)
        entry = events[event_id]

        # Verify 26-char Crockford Base32 monotonic ULID
        self.assertEqual(len(event_id), 26)
        self.assertTrue(all(c in telemetry.CROCKFORD_BASE32 for c in event_id))

        # Verify all mandatory schema fields
        self.assertEqual(entry["event_id"], event_id)
        self.assertEqual(entry["duration_ms"], 250)
        self.assertEqual(entry["status"], "success")
        self.assertIsNone(entry["error"])
        self.assertIsNone(entry["parent_event_id"])
        self.assertEqual(entry["skill"]["name"], "ai-sdlc-specify")
        self.assertEqual(entry["source"]["product"], "ai-sdlc-backbone")
        self.assertIn("timestamp_start", entry)
        self.assertIn("timestamp_end", entry)
        self.assertIn("user", entry)
        self.assertIn("git", entry)
        self.assertEqual(entry["task"]["id"], "feat-100")

    def test_zero_token_fabrication(self) -> None:
        """Verify strict zero token fabrication: when models not provided, models=[] and usage_available=False."""
        # Case 1: No model token usage provided
        ev1 = telemetry.record_telemetry_event(
            skill="ai-sdlc-review",
            root=self.root,
        )
        self.assertIsNotNone(ev1)
        self.assertFalse(ev1["usage_available"])
        self.assertEqual(ev1["models"], [])

        # Case 2: Explicit model token usage provided
        ev2 = telemetry.record_telemetry_event(
            skill="ai-sdlc-sdd",
            models=[{
                "provider": "anthropic",
                "model": "claude-3-7-sonnet",
                "input_tokens": 1200,
                "output_tokens": 400,
                "total_tokens": 1600,
                "cache_read_tokens": 800,
                "cache_write_tokens": 100,
                "reasoning_tokens": 50,
            }],
            root=self.root,
        )
        self.assertIsNotNone(ev2)
        self.assertTrue(ev2["usage_available"])
        self.assertEqual(len(ev2["models"]), 1)
        m = ev2["models"][0]
        self.assertEqual(m["provider"], "anthropic")
        self.assertEqual(m["model"], "claude-3-7-sonnet")
        self.assertEqual(m["input_tokens"], 1200)
        self.assertEqual(m["output_tokens"], 400)
        self.assertEqual(m["total_tokens"], 1600)
        self.assertEqual(m["cache_read_tokens"], 800)
        self.assertEqual(m["cache_write_tokens"], 100)
        self.assertEqual(m["reasoning_tokens"], 50)

        # Check raw serialization in TOON: models[0]: for empty, table for non-empty
        raw = self.telemetry_file.read_text(encoding="utf-8")
        decoded = toon_codec.loads(raw)
        ev1_decoded = decoded["events"][ev1["event_id"]]
        ev2_decoded = decoded["events"][ev2["event_id"]]
        self.assertEqual(ev1_decoded["models"], [])
        self.assertFalse(ev1_decoded["usage_available"])
        self.assertEqual(len(ev2_decoded["models"]), 1)
        self.assertTrue(ev2_decoded["usage_available"])

    def test_user_identity_resolution_from_customization(self) -> None:
        """Verify user resolution from .customization.toon layer."""
        customization = self.root / ".customization.toon"
        customization.write_text(
            "schema: ai-sdlc-config/v1\n"
            "values:\n"
            "  user:\n"
            "    name: \"Alice Architect\"\n"
            "    email: \"alice@company.internal\"\n"
            "    role: \"software-architect\"\n",
            encoding="utf-8",
        )

        user_info = telemetry.resolve_user(self.root)
        self.assertEqual(user_info["name"], "Alice Architect")
        self.assertEqual(user_info["email"], "alice@company.internal")
        self.assertEqual(user_info["role"], "software-architect")

        ev = telemetry.record_telemetry_event(skill="ai-sdlc-architecture", root=self.root)
        self.assertEqual(ev["user"]["name"], "Alice Architect")
        self.assertEqual(ev["user"]["email"], "alice@company.internal")
        self.assertEqual(ev["user"]["role"], "software-architect")

    def test_user_identity_resolution_from_home_config(self) -> None:
        """Verify user resolution from ~/.config/ai-sdlc/config.toon when .customization.toon is absent."""
        fake_home = self.root / "fake_home"
        cfg_dir = fake_home / ".config" / "ai-sdlc"
        cfg_dir.mkdir(parents=True)
        cfg_file = cfg_dir / "config.toon"
        cfg_file.write_text(
            "schema: ai-sdlc-config/v1\n"
            "values:\n"
            "  user:\n"
            "    name: \"Bob Product\"\n"
            "    email: \"bob@company.internal\"\n"
            "    role: \"product-manager\"\n",
            encoding="utf-8",
        )

        with patch("pathlib.Path.home", return_value=fake_home):
            user_info = telemetry.resolve_user(self.root)
            self.assertEqual(user_info["name"], "Bob Product")
            self.assertEqual(user_info["email"], "bob@company.internal")
            self.assertEqual(user_info["role"], "product-manager")

    def test_user_identity_fallback_to_env(self) -> None:
        """Verify user identity falls back to environment variables and defaults."""
        env_vars = {
            "AI_SDLC_USER_NAME": "Carol QA",
            "AI_SDLC_USER_EMAIL": "carol@company.internal",
            "AI_SDLC_USER_ROLE": "qa-engineer",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            # Point away from any local customization or home config
            fake_home = self.root / "no_config"
            with patch("pathlib.Path.home", return_value=fake_home):
                user_info = telemetry.resolve_user(self.root)
                self.assertEqual(user_info["name"], "Carol QA")
                self.assertEqual(user_info["email"], "carol@company.internal")
                self.assertEqual(user_info["role"], "qa-engineer")

    def test_secret_redaction(self) -> None:
        """Verify stripping bearer tokens, sk- API keys, and private keys."""
        secret_token = "sk-12345678901234567890123456"
        bearer_auth = "Authorization: Bearer mySecretToken123456789"
        rsa_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0\n-----END RSA PRIVATE KEY-----"

        ev = telemetry.record_telemetry_event(
            skill="ai-sdlc-security",
            status="error",
            error={"code": "AUTH_FAILED", "message": f"Failed with {secret_token} and {bearer_auth}"},
            task={"id": "sec-1", "type": "task", "title": f"Key inspection {rsa_key}", "owner": "test"},
            root=self.root,
        )
        self.assertIsNotNone(ev)
        err_msg = ev["error"]["message"]
        task_title = ev["task"]["title"]

        self.assertNotIn("sk-1234567890", err_msg)
        self.assertNotIn("mySecretToken123456789", err_msg)
        self.assertIn("[REDACTED]", err_msg)
        self.assertNotIn("MIIEowIBAAKCAQEA0", task_title)
        self.assertIn("[REDACTED]", task_title)

    def test_fail_open_behavior(self) -> None:
        """Verify recording never raises exceptions even when filesystem is broken or read-only."""
        # Simulate unwriteable directory by pointing to invalid path or mocking open
        with patch("builtins.open", side_effect=PermissionError("Read-only filesystem")):
            result = telemetry.record_telemetry_event(
                skill="ai-sdlc-specify",
                root=self.root,
            )
            # Must return None without raising
            self.assertIsNone(result)

    def test_concurrency_flocking(self) -> None:
        """Verify multi-threaded / concurrent appending preserves valid TOON without interleaving corruption."""
        num_events = 20

        def append_one(i: int) -> str | None:
            res = telemetry.record_telemetry_event(
                skill=f"ai-sdlc-worker-{i}",
                duration_ms=i * 10,
                root=self.root,
            )
            return res["event_id"] if res else None

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(append_one, i) for i in range(num_events)]
            recorded_ids = [f.result() for f in futures]

        self.assertEqual(len(recorded_ids), num_events)
        self.assertTrue(all(rid is not None for rid in recorded_ids))

        # Check that file is completely valid TOON and all events exist
        raw = self.telemetry_file.read_text(encoding="utf-8")
        data = toon_codec.loads(raw)
        events = data.get("events", {})
        self.assertEqual(len(events), num_events)
        for rid in recorded_ids:
            self.assertIn(rid, events)

    def test_cli_record_read_and_dump(self) -> None:
        """Verify record, read, and dump CLI subcommands."""
        # 1. Record via CLI
        code = telemetry.main([
            "record",
            "--skill", "ai-sdlc-verify",
            "--status", "success",
            "--duration-ms", "150",
            "--task-id", "CLI-01",
            "--root", str(self.root),
        ])
        self.assertEqual(code, 0)
        self.assertTrue(self.telemetry_file.is_file())

        # 2. Read events via helper
        events = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["skill"]["name"], "ai-sdlc-verify")
        self.assertEqual(events[0]["task"]["id"], "CLI-01")

        # 3. Dump raw TOON
        dumped = telemetry.dump_telemetry(root=self.root)
        self.assertTrue(dumped.startswith("schema: ai-sdlc-telemetry/v1"))
        self.assertIn("ai-sdlc-verify", dumped)

    def test_usage_journal_integration(self) -> None:
        """Verify automatic telemetry appending when usage_journal records skill.end or track_skill."""
        # Test record_event with skill.end
        usage_journal.record_event(
            "skill.end",
            {
                "skill": "ai-sdlc-specify",
                "status": "completed",
                "duration_ms": 320,
                "feature": "feat-journal",
            },
            root=self.root,
        )

        events = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["skill"]["name"], "ai-sdlc-specify")
        self.assertEqual(events[0]["status"], "success")
        self.assertEqual(events[0]["duration_ms"], 320)
        self.assertEqual(events[0]["task"]["id"], "feat-journal")

        # Test track_skill context manager
        with usage_journal.track_skill("ai-sdlc-implement", feature="feat-track", root=self.root):
            time.sleep(0.01)

        events2 = telemetry.read_telemetry_events(root=self.root)
        self.assertEqual(len(events2), 2)
        self.assertEqual(events2[1]["skill"]["name"], "ai-sdlc-implement")
        self.assertEqual(events2[1]["task"]["id"], "feat-track")
        self.assertTrue(events2[1]["duration_ms"] > 0)


if __name__ == "__main__":
    unittest.main()
