#!/usr/bin/env python3
"""Tests for the shared full-fidelity TOON encoder."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ai_sdlc_toon import ToonDecodeError, decode_toon, encode_toon


class ToonTests(unittest.TestCase):
    def test_nested_records_and_uniform_tables(self) -> None:
        value = {
            "schema": "example/v1",
            "active": True,
            "tags": ["delivery", "42", "needs,quote"],
            "owner": {"name": "Ada", "team": None},
            "items": [{"id": "T001", "done": True}, {"id": "T002", "done": False}],
        }
        self.assertEqual(
            encode_toon(value),
            "active: true\n"
            "items[2]{done,id}:\n"
            "  true,T001\n"
            "  false,T002\n"
            "owner:\n"
            "  name: Ada\n"
            "  team: null\n"
            "schema: example/v1\n"
            'tags[3]: delivery,"42","needs,quote"\n',
        )

    def test_non_uniform_arrays_retain_nested_data(self) -> None:
        value = {"events": [{"type": "start", "data": {"step": 1}}, {"type": "stop", "reasons": ["budget", "policy"]}]}
        rendered = encode_toon(value)
        self.assertIn("events[2]:\n", rendered)
        self.assertIn("  - data:\n      step: 1\n    type: start\n", rendered)
        self.assertIn("  - reasons[2]: budget,policy\n    type: stop\n", rendered)

    def test_quotes_ambiguous_values_and_rejects_non_finite_numbers(self) -> None:
        self.assertEqual(encode_toon({"values": ["", " true ", "null", "1", "-item"]}), 'values[5]: ""," true ","null","1","-item"\n')
        with self.assertRaises(ValueError):
            encode_toon({"bad": float("nan")})

    def test_round_trip_covers_empty_and_nested_containers(self) -> None:
        values = (
            {},
            [],
            {"empty_mapping": {}, "empty_list": []},
            [{"nested": [[], {}, {"value": "stable"}]}],
        )
        for value in values:
            with self.subTest(value=value):
                rendered = encode_toon(value)
                self.assertEqual(decode_toon(rendered), value)
                self.assertEqual(encode_toon(decode_toon(rendered)), rendered)

    def test_decoder_rejects_malformed_or_ambiguous_input(self) -> None:
        invalid = (
            "",
            "items[2]: one\n",
            "key: first\nkey: second\n",
            "root:\n   child: odd-indent\n",
            'value: "unterminated\n',
        )
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ToonDecodeError):
                    decode_toon(value)


if __name__ == "__main__":
    unittest.main()
