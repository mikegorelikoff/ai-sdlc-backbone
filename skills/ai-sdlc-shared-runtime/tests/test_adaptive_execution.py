"""Risk policy, evidence reuse, bounded retries and source freshness."""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ai_sdlc_adaptive as a
from ai_sdlc_source_reads import read_bytes, source_scope

KNOWN = {"familiar": True, "covered": True, "confident": True}

class AdaptiveTests(unittest.TestCase):
    def test_classification_scenarios(self):
        cases = [
            ("fix tiny bug", ["app.py"], KNOWN, "FAST"),
            ("update documentation", ["docs/guide.md"], {}, "FAST"),
            ("implement localized feature", ["app.py"], KNOWN, "STANDARD"),
            ("implement feature", ["api/a.py", "ui/a.ts"], KNOWN, "STANDARD"),
            ("change architecture", ["app.py"], KNOWN, "DEEP"),
            ("security-sensitive change", ["app.py"], KNOWN, "DEEP"),
            ("fix tiny bug", ["app.py"], {}, "STANDARD"),
            ("fix tiny bug", ["auth/session.py"], KNOWN, "DEEP"),
            ("update documentation", ["docs/guide.md"], {"migration": True}, "DEEP"),
        ]
        for request, paths, facts, expected in cases:
            with self.subTest(request=request, facts=facts):
                self.assertEqual(a.classify(request, paths, facts)["mode"], expected)
        self.assertEqual(a.classify("tiny " * 1000, ["a.py"], {})["mode"], "STANDARD")

    def test_escalation_reuses_work_and_is_monotonic(self):
        task = a.new_task("fix tiny bug", ["a.py"], KNOWN)
        task["plan"] = ["preserved work"]
        pack = task["context_pack"]
        self.assertTrue(a.escalate(task, observed={"dependency_change": True}))
        self.assertEqual(task["decision"]["mode"], "STANDARD")
        self.assertIs(task["context_pack"], pack)
        self.assertTrue(a.escalate(task, observed={"architecture": True}))
        self.assertEqual(task["decision"]["mode"], "DEEP")
        a.escalate(task, observed={"architecture": False})
        self.assertEqual(task["decision"]["mode"], "DEEP")
        self.assertEqual(task["plan"], ["preserved work"])
        self.assertEqual(task["metrics"]["escalations"], 2)

    def test_context_incremental_reuse_and_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = root / "a.py"
            path.write_text("def example(): pass")
            task = a.new_task("fix tiny bug", ["a.py"], KNOWN)
            a.refresh_context(task, root, ["a.py"], {"constraints": ["preserve API"]})
            record = task["context_pack"]["relevant_files"]["a.py"]
            a.refresh_context(task, root)
            self.assertIs(task["context_pack"]["relevant_files"]["a.py"], record)
            self.assertEqual(record["symbols"], ["example"])
            path.write_text("def changed(): pass")
            a.refresh_context(task, root)
            self.assertNotEqual(task["context_pack"]["relevant_files"]["a.py"]["sha256"], record["sha256"])
            path.unlink(); a.refresh_context(task, root)
            self.assertEqual(task["context_pack"]["relevant_files"]["a.py"]["sha256"], "missing")
            self.assertEqual(task["context_pack"]["constraints"], ["preserve API"])

    def test_context_rejects_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in ["../a", ".git/config", ".env", "/etc/passwd"]:
                with self.subTest(path=path), self.assertRaises(ValueError):
                    a.refresh_context(a.new_task("change"), root, [path])
            (root / "link").symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                a.refresh_context(a.new_task("change"), root, ["link/a.py"])

    def test_only_triggered_capabilities(self):
        fast = a.new_task("fix tiny bug", ["a.py"], KNOWN)
        self.assertEqual(fast["strategy"]["capabilities"], {})
        self.assertEqual(fast["strategy"]["stages"], ["context", "implement", "verify"])
        self.assertEqual(fast["strategy"]["checks"], ["targeted-tests", "diff-check"])
        normal = a.new_task("feature", ["a.py"], {"boundary_behavior": True})
        self.assertEqual(list(normal["strategy"]["capabilities"]), ["edge-case-hunter"])
        self.assertIn("compact-plan", normal["strategy"]["stages"])

    def test_bounded_retries_and_no_unchanged_review(self):
        task = a.new_task("feature")
        for index in range(3):
            self.assertEqual(a.verification_action(task, str(index), [["test"]]), "run")
            a.record_verification(task, str(index), [["test"]], False)
            with self.assertRaises(ValueError):
                a.verification_action(task, str(index), [["test"]])
        with self.assertRaises(ValueError):
            a.verification_action(task, "new-source", [["test"]])
        self.assertEqual(task["result"], "blocked")
        a.escalate(task, observed={"architecture": True})
        self.assertEqual(len(task["verification"]), 3)

    def test_success_terminates_and_changed_state_needs_verification(self):
        task = a.new_task("feature")
        a.record_verification(task, "snapshot", [["test"]], True)
        self.assertEqual(task["result"], "done")
        self.assertEqual(a.verification_action(task, "snapshot", [["test"]]), "done")
        self.assertEqual(a.verification_action(task, "changed", [["test"]]), "run")

    def test_full_workflow_retained_and_cannot_lower_risk(self):
        deep = a.new_task("tiny fix", ["docs/a.md"], full=True)
        self.assertEqual(deep["decision"]["mode"], "DEEP")
        self.assertEqual(deep["strategy"]["stages"], ["context", "planning", "readiness", "sdd", "implement", "verify"])
        self.assertFalse(deep["strategy"]["authorizes_execution"])

    def test_invalid_signals_fail_closed(self):
        for values in [{"security": "false"}, {"files": -1}, {"files": True}, {"unknown": 0}]:
            with self.assertRaises(ValueError):
                a.classify("request", observed=values)
        for value in ["security=0", "files=-1", "made_up=true"]:
            with self.assertRaises(ValueError): a.signals([value])

    def test_discovered_security_and_failed_assumptions_raise_depth(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.py').write_text('def authenticate(): pass')
            task = a.new_task('fix tiny bug', ['a.py'], KNOWN)
            a.refresh_context(task, root, ['a.py'])
            self.assertEqual(task['decision']['mode'], 'DEEP')
        task = a.new_task('fix tiny bug', ['a.py'], KNOWN)
        a.record_verification(task, 'first', [['test']], False)
        self.assertEqual(task['decision']['mode'], 'STANDARD')
        a.record_verification(task, 'repaired', [['test']], False)
        self.assertEqual(task['decision']['mode'], 'DEEP')
        self.assertEqual(task['metrics']['verification_iterations'], 2)

    def test_explicit_minimum_does_not_invent_architecture_evidence(self):
        task = a.new_task('fix tiny bug', ['a.py'], KNOWN)
        a.raise_minimum(task, 'DEEP')
        self.assertEqual(task['decision']['mode'], 'DEEP')
        self.assertNotIn('architecture', task['decision']['signals'])

    def test_unknown_metrics_are_not_zero_and_known_stages_accumulate(self):
        task = a.new_task("feature")
        a.stage_event(task, "implement", 2.0, skills=["implementation"])
        a.stage_event(task, "verify", 0.1, model_calls=0, tool_calls=1, context_tokens=0)
        self.assertIsNone(task["metrics"]["model_calls"])
        self.assertGreaterEqual(task["metrics"]["total_seconds"], 0)
        self.assertEqual(len(task["metrics"]["stages"]), 2)

    def test_source_reuse_is_scoped_and_invalidates_on_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.py"; path.write_bytes(b"one")
            original = Path.read_bytes; reads = []
            def tracked(p): reads.append(p); return original(p)
            @source_scope
            def decision():
                self.assertEqual(read_bytes(path), b"one")
                self.assertEqual(read_bytes(path), b"one")
                path.write_bytes(b"two")
                self.assertEqual(read_bytes(path), b"two")
            with patch.object(Path, "read_bytes", tracked): decision()
            self.assertEqual(len(reads), 2)
            self.assertEqual(read_bytes(path), b"two")

if __name__ == "__main__": unittest.main()
