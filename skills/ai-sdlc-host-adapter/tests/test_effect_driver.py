#!/usr/bin/env python3
"""Tests for bounded idempotent effect execution."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/effect_driver.py"
SPEC = importlib.util.spec_from_file_location("effect_driver", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
DRIVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DRIVER)


def negotiation(side_effect: str = "workspace-write") -> dict:
    return {
        "schema": "ai-sdlc-capability-negotiation/v2",
        "adapter": {"id": "full-host"},
        "compatible": True,
        "fingerprint": "a" * 64,
        "step": {"step_fingerprint": "b" * 64},
        "mapping": {"host_operation": "host.action"},
        "side_effect": side_effect,
        "required_capabilities": ["external.write"] if side_effect == "external-write" else ["filesystem.read", "filesystem.write"],
    }


def request(negotiated: dict, *, driver: str = "workspace.write-text", arguments: dict | None = None) -> dict:
    value = {
        "schema": "ai-sdlc-effect-request/v1",
        "driver": driver,
        "adapter_id": "full-host",
        "negotiation_fingerprint": negotiated["fingerprint"],
        "step_fingerprint": "b" * 64,
        "context_fingerprint": "c" * 64,
        "operation": "host.action",
        "side_effect": negotiated["side_effect"],
        "capabilities": negotiated["required_capabilities"],
        "approval_ref": "APR-001" if negotiated["side_effect"] == "external-write" else "",
        "arguments": arguments or {"path": "out/result.txt", "content": "stable\n", "expected_sha256": ""},
        "idempotency_key": "",
    }
    value["idempotency_key"] = DRIVER.digest(DRIVER.semantic_request(value))
    return value


class EffectDriverTests(unittest.TestCase):
    def test_workspace_write_replays_one_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            negotiated = negotiation()
            effect = request(negotiated)
            first = DRIVER.execute(root, effect, negotiated)
            second = DRIVER.execute(root, effect, negotiated)
            self.assertEqual(first, second)
            self.assertEqual((root / "out/result.txt").read_text(encoding="utf-8"), "stable\n")
            self.assertEqual(len(list((root / "_ai_sdlc/effects").glob("*.toon"))), 1)

    def test_changed_payload_cannot_reuse_idempotency_key(self) -> None:
        negotiated = negotiation()
        effect = request(negotiated)
        effect["arguments"]["content"] = "changed\n"
        with self.assertRaisesRegex(ValueError, "idempotency key mismatch"):
            DRIVER.validate_request(effect, negotiated)

    def test_path_traversal_and_secret_keys_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            negotiated = negotiation()
            traversal = request(negotiated, arguments={"path": "../escape", "content": "x", "expected_sha256": ""})
            with self.assertRaisesRegex(ValueError, "traversal"):
                DRIVER.execute(root, traversal, negotiated)
            external = negotiation("external-write")
            unsafe = request(
                external,
                driver="external.toon-post",
                arguments={"url": "https://example.com/hook", "allowed_hosts": ["example.com"], "payload": {"token": "not-stored"}, "timeout_seconds": 1},
            )
            with self.assertRaisesRegex(ValueError, "secret-bearing"):
                DRIVER.validate_request(unsafe, external)

    def test_external_driver_requires_approval_and_allowlist(self) -> None:
        negotiated = negotiation("external-write")
        effect = request(
            negotiated,
            driver="external.toon-post",
            arguments={"url": "https://example.com/hook", "allowed_hosts": ["example.com"], "payload": {"event": "complete"}, "timeout_seconds": 1},
        )
        effect["approval_ref"] = ""
        effect["idempotency_key"] = DRIVER.digest(DRIVER.semantic_request(effect))
        with self.assertRaisesRegex(ValueError, "requires approval"):
            DRIVER.validate_request(effect, negotiated)

    def test_external_driver_emits_deterministic_evidence(self) -> None:
        class Response:
            status = 202
            def __enter__(self):
                return self
            def __exit__(self, *_args):
                return False
            def read(self, _limit):
                return b"accepted"

        class Opener:
            def __init__(self):
                self.call_count = 0
            def open(self, *_args, **_kwargs):
                self.call_count += 1
                return Response()

        with tempfile.TemporaryDirectory() as directory:
            negotiated = negotiation("external-write")
            effect = request(
                negotiated,
                driver="external.toon-post",
                arguments={"url": "https://example.com/hook", "allowed_hosts": ["example.com"], "payload": {"event": "complete"}, "timeout_seconds": 1},
            )
            opener = Opener()
            with mock.patch.object(DRIVER.urllib.request, "build_opener", return_value=opener):
                receipt = DRIVER.execute(Path(directory), effect, negotiated)
            self.assertEqual(receipt["evidence"]["status_code"], 202)
            self.assertEqual(opener.call_count, 1)
            self.assertEqual(DRIVER.execute(Path(directory), effect, negotiated), receipt)
            self.assertEqual(opener.call_count, 1)

    def test_external_driver_installs_a_no_redirect_handler(self) -> None:
        negotiated = negotiation("external-write")
        effect = request(
            negotiated,
            driver="external.toon-post",
            arguments={"url": "https://example.com/hook", "allowed_hosts": ["example.com"], "payload": {"event": "complete"}, "timeout_seconds": 1},
        )
        with mock.patch.object(DRIVER.urllib.request, "build_opener", side_effect=ValueError("redirect blocked")) as build:
            with self.assertRaisesRegex(ValueError, "redirect blocked"):
                DRIVER.external_toon_post(effect["arguments"], effect["idempotency_key"])
        self.assertIsInstance(build.call_args.args[0], DRIVER.NoRedirect)


if __name__ == "__main__":
    unittest.main()
