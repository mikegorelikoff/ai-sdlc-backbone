#!/usr/bin/env python3
"""Tests for ai-sdlc-loop-usage-coach skill scripts."""

from __future__ import annotations

import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add shared runtime and coach script to sys.path
SHARED_PATH = Path(__file__).resolve().parents[3] / "skills" / "ai-sdlc-shared-runtime" / "scripts"
if not SHARED_PATH.is_dir():
    SHARED_PATH = Path(__file__).resolve().parents[3] / "ai-sdlc-loop-shared-runtime" / "scripts"
COACH_PATH = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SHARED_PATH))
sys.path.insert(0, str(COACH_PATH))

import coach
import usage_journal
try:
    from ai_sdlc_toon import decode_toon
except ImportError:
    from toon import decode_toon


class CoachScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.root = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_explain_signals(self):
        # Known signal
        self.assertEqual(0, coach.cmd_explain("rework-cycle"))
        self.assertEqual(0, coach.cmd_explain("evidence-lag"))
        self.assertEqual(0, coach.cmd_explain("handoff-discoverability"))
        # Unknown signal
        self.assertEqual(1, coach.cmd_explain("unknown-xyz"))

    def test_empty_report_and_analyze(self):
        self.assertEqual(0, coach.cmd_report(root=self.root))
        self.assertEqual(0, coach.cmd_analyze(session_id="20260928T094812Z-a83f", root=self.root))

    def test_suggest_and_feedback(self):
        # Create a session with rework cycle
        sid = "20260928T094812Z-a83f"
        for _ in range(4):
            usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-implement"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-implement", "status": "completed"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.start", {"skill": "ai-sdlc-loop-engineering-quality-gate"}, session_id=sid, root=self.root)
            usage_journal.record_event("skill.end", {"skill": "ai-sdlc-loop-engineering-quality-gate", "status": "failed"}, session_id=sid, root=self.root)

        # Run suggest
        exit_code = coach.cmd_suggest(session_id=sid, root=self.root)
        self.assertEqual(0, exit_code)

        # Record feedback
        fb_exit = coach.cmd_feedback(
            suggestion_id="sug-rework-1",
            outcome="accepted",
            notes="helpful advice",
            session_id=sid,
            root=self.root,
        )
        self.assertEqual(0, fb_exit)

        # Verify feedback event was journaled
        sessions = usage_journal.scan_sessions(root=self.root)
        self.assertEqual(1, len(sessions))
        events = sessions[0]["events"]
        feedback_events = [ev for ev in events.values() if ev.get("type") == "coach.feedback"]
        self.assertEqual(1, len(feedback_events))
        self.assertEqual("sug-rework-1", feedback_events[0]["suggestion_id"])
        self.assertEqual("accepted", feedback_events[0]["outcome"])


if __name__ == "__main__":
    unittest.main()
