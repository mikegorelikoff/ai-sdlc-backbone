#!/usr/bin/env python3
"""Executable discovery contracts: determinism, evidence and safe persistence."""

from __future__ import annotations

import copy
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts/requirements_discovery.py"
spec = importlib.util.spec_from_file_location("discovery_under_test", SCRIPT)
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "request.md").write_text("Reduce approval waiting time. Consider bulk approval.\n", encoding="utf-8")
        (self.root / "pilot.md").write_text("A low-value batch pilot was implemented; outcomes were not measured.\n", encoding="utf-8")
        self.context = discovery.prepare(self.root, "example", "request.md", ["pilot.md"], "quick")
        self.context_path = "context.toon"
        self.save(self.context_path, self.context)

    def save(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(discovery.encoded(value))

    def run_cli(self, *args, ok=True, script=SCRIPT, env=None):
        result = subprocess.run([sys.executable, str(script), *args, "--root", str(self.root)],
                                text=True, encoding="utf-8", capture_output=True, env=env)
        if ok:
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        else:
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        return result

    def draft(self, context=None):
        context = context or self.context
        sources = {s["path"]: s["id"] for s in context["sources"]}
        raw, past = sources["request.md"], sources["pilot.md"]
        value = discovery.scaffold(context, "2026-09-07")
        value["evidence_limits"] = ["Pilot outcomes were not measured; the current bottleneck is unknown"]
        value["problem"] = {"summary": "Reduce waiting for approvals", "current_process": "Cases await a reviewer",
                            "actors": ["Requester", "Reviewer"], "desired_outcome": "Less waiting with correct decisions",
                            "constraints": ["Preserve required individual reviews"], "success_measures": ["Time waiting for assignment"]}
        value["observations"] = [
            {"id": "REQ-001", "kind": "fact", "statement": "Requester reports long waits", "source_ids": [raw], "impact": "Approval lead time", "material": True},
            {"id": "GAP-001", "kind": "unknown", "statement": "Where is waiting concentrated?", "source_ids": [], "impact": "Choice of workflow change", "material": True},
        ]
        value["precedents"] = [{"id": "PRE-001", "source_ids": [past], "decision": "Try low-value batch review",
                                "status": "implemented", "outcome": "", "outcome_source_ids": [],
                                "applicability": "Similar approval workflow", "differences": "Current eligibility is unknown"}]
        value["options"] = [{"id": f"OPT-00{i}", "title": title, "status": "candidate", "rejection_reason": "",
                             "beneficiary": "Requester", "value": benefit, "workflow": workflow,
                             "business_rules": ["Keep reviewer accountability"], "source_ids": [raw],
                             "precedent_ids": ["PRE-001"] if i == 2 else [], "observation_ids": ["GAP-001", "REQ-001"],
                             "evidence_kind": "sourced", "dependencies": ["Operations owner"],
                             "risks": ["May target the wrong cause of delay"], "reversibility": "Revert the pilot process",
                             "cost_assumptions": "No estimate; ask the operations owner", "tradeoffs": "Pilot learning requires reviewer time"}
                            for i, title, benefit, workflow in [
                                (1, "Improve assignment", "Reduce idle queue time", "Triage before individual review"),
                                (2, "Limited batch pilot", "Test reduced review effort", "Group eligible cases; review exceptions individually")]]
        value["questions"] = [{"id": "Q-001", "observation_ids": ["GAP-001"], "option_ids": ["OPT-001", "OPT-002"],
                               "stakeholder": "Operations analyst", "question": "Where does the time accumulate?",
                               "purpose": "Choose the intervention", "priority": "before-selection",
                               "evidence_location": "Recent approval event timestamps", "method": "Audit a representative sample",
                               "decision_impact": "Assignment delay supports OPT-001; review effort motivates testing OPT-002",
                               "response_status": "open", "answer": "", "answer_source_ids": []}]
        value["recommendation"] = {"preferred_option_id": "OPT-001", "criteria": ["Policy compatibility", "Observed waiting stage"],
                                   "rationale": "Start with assignment if timestamps confirm idle waiting",
                                   "change_conditions": ["Review effort dominates waiting"], "single_option_reason": "",
                                   "next_owner": "Operations analyst", "next_action": "Inspect approval timestamps",
                                   "expected_evidence": "Sample audit identifying the waiting stage"}
        return value

    def test_prepare_is_byte_stable_with_reordered_sources_and_relocated_root(self):
        first = self.run_cli("prepare", "--feature", "example", "--request", "request.md", "--source", "pilot.md", "--quick-flow").stdout
        second = self.run_cli("prepare", "--feature", "example", "--request", "request.md", "--source", "request.md", "--source", "pilot.md", "--source", "pilot.md", "--quick-flow").stdout
        self.assertEqual(first, second)
        with tempfile.TemporaryDirectory() as directory:
            other = Path(directory).resolve()
            for path in ("request.md", "pilot.md"):
                shutil.copyfile(self.root / path, other / path)
            relocated = discovery.prepare(other, "example", "request.md", ["pilot.md"], "quick")
            self.assertEqual(discovery.encoded(self.context), discovery.encoded(relocated))
        self.assertFalse((self.root / "specs-refiniment").exists())
        self.assertFalse((self.root / ".ai-sdlc-loop").exists())

    def test_source_identity_survives_edits_but_fingerprint_changes(self):
        (self.root / "pilot.md").write_text("Pilot outcome measured later.\n", encoding="utf-8")
        changed = discovery.prepare(self.root, "example", "request.md", ["pilot.md"], "quick")
        self.assertEqual([s["id"] for s in self.context["sources"]], [s["id"] for s in changed["sources"]])
        self.assertNotEqual(self.context["fingerprint"], changed["fingerprint"])

    def test_scaffold_is_deterministic_incomplete_and_requires_explicit_date(self):
        args = ("scaffold", "--context", self.context_path, "--as-of", "2026-09-07")
        first = self.run_cli(*args).stdout
        self.assertEqual(first, self.run_cli(*args).stdout)
        value = discovery.codec.loads(first)
        self.assertEqual([], value["options"])
        self.assertEqual([], value["questions"])
        with self.assertRaises(ValueError):
            discovery.validate_draft(self.context, value)
        self.run_cli("scaffold", "--context", self.context_path, ok=False)
        for invalid in ("20260907", "2026-W37-1", "2026-02-30"):
            self.run_cli("scaffold", "--context", self.context_path, "--as-of", invalid, "--write", ok=False)
        self.assertFalse((self.root / discovery.locations("example")["draft"]).exists())

    def test_canonical_analysis_order_and_utf8_output(self):
        value = self.draft()
        value["problem"]["summary"] = "Вопрос | <script>alert(1)</script>\n[ссылка](file)"
        first = discovery.finalize(self.context, value)
        for field in ("observations", "precedents", "options", "questions"):
            value[field].reverse()
        value["questions"][0]["option_ids"].reverse()
        value["problem"]["actors"].reverse()
        self.assertEqual(discovery.encoded(first), discovery.encoded(discovery.finalize(self.context, value)))
        self.save("draft.toon", value)
        result = self.run_cli("finalize", "--context", self.context_path, "--draft", "draft.toon",
                              env={**os.environ, "PYTHONIOENCODING": "cp1252"})
        self.assertIn("Вопрос", result.stdout)
        if discovery.PREFIX == "ai-sdlc":
            rendered = discovery.render_markdown(first).decode()
            self.assertNotIn("<script>", rendered)
            self.assertIn("&lt;script&gt;", rendered)
            self.assertIn("outcomes were not measured", rendered)
            self.assertIn("Audit a representative sample", rendered)

    def test_full_workflow_and_idempotent_writes(self):
        self.save("draft.toon", self.draft())
        self.run_cli("validate", "--context", self.context_path, "--draft", "draft.toon")
        args = ("finalize", "--context", self.context_path, "--draft", "draft.toon", "--write")
        first = self.run_cli(*args)
        target = discovery.locations("example")
        report = self.root / target["report"]
        self.assertEqual(first.stdout.encode(), report.read_bytes())
        mtime = report.stat().st_mtime_ns
        self.assertEqual(first.stdout, self.run_cli(*args).stdout)
        self.assertEqual(mtime, report.stat().st_mtime_ns)
        self.run_cli("verify", "--report", target["report"])
        self.assertEqual(discovery.PREFIX == "ai-sdlc", bool(list(self.root.rglob("requirements-discovery.md"))))

    def test_no_history_is_valid_only_as_explicit_hypothesis(self):
        value = self.draft()
        value["precedents"] = []
        for option in value["options"]:
            option["precedent_ids"] = []
            option["source_ids"] = []
            option["evidence_kind"] = "hypothesis"
            option["tradeoffs"] = "No verified precedent was supplied; validate applicability in an interview"
        report = discovery.finalize(self.context, value)
        self.assertEqual("awaiting-answers", report["decision_status"])
        self.assertEqual([], report["analysis"]["precedents"])

    def test_malformed_and_unsupported_analysis_is_rejected_without_writes(self):
        def field(path, value):
            def mutate(draft):
                node = draft
                for key in path[:-1]:
                    node = node[key]
                node[path[-1]] = value
            return mutate
        mutations = [
            field(["schema"], "unknown/v1"), field(["problem", "actors"], "not an array"),
            field(["observations", 0, "material"], 1), field(["observations", 0, "source_ids"], []),
            field(["observations", 1, "id"], "REQ-001"), field(["questions", 0, "option_ids"], ["OPT-999"]),
            field(["questions", 0, "option_ids"], ["OPT-001"]), field(["questions", 0, "observation_ids"], ["REQ-001"]),
            field(["questions", 0, "stakeholder"], ""), field(["questions", 0, "method"], " "),
            field(["questions", 0, "decision_impact"], ""), field(["questions", 0, "response_status"], "answered"),
            field(["questions", 0, "answer"], "unverified reply"), field(["questions", 0, "priority"], "urgent"),
            field(["questions", 0, "option_ids"], ["OPT-001", "OPT-001"]),
            field(["precedents", 0, "outcome"], "Cut waiting by 80%"),
            field(["precedents", 0, "status"], "outcome-measured"),
            field(["options", 0, "precedent_ids"], ["PRE-999"]),
            field(["recommendation", "preferred_option_id"], "OPT-999"),
            field(["decision", "status"], "accepted"), field(["as_of"], "2026-02-30"),
            field(["context_fingerprint"], "0" * 64), lambda d: d.update(extra="silently lost data"),
        ]
        for i, mutate in enumerate(mutations):
            with self.subTest(case=i):
                value = self.draft()
                mutate(value)
                self.save("invalid.toon", value)
                self.run_cli("finalize", "--context", self.context_path, "--draft", "invalid.toon", "--write", ok=False)
                self.assertFalse((self.root / discovery.locations("example")["report"]).exists())

    def test_acceptance_requires_recorded_owner_answer_and_no_selection_blocker(self):
        (self.root / "owner.md").write_text("2026-09-07 Operations owner selects assignment improvement after sample audit.\n", encoding="utf-8")
        context = discovery.prepare(self.root, "example", "request.md", ["pilot.md", "owner.md"], "full")
        owner = next(s["id"] for s in context["sources"] if s["path"] == "owner.md")
        value = self.draft(context)
        value["decision"] = {"status": "accepted", "selected_option_id": "OPT-001", "owner": "Operations owner",
                             "source_ids": [owner], "decided_at": "2026-09-07"}
        with self.assertRaises(ValueError):
            discovery.finalize(context, value)
        value["questions"][0].update(response_status="answered", answer="The sample shows assignment delay", answer_source_ids=[owner])
        report = discovery.finalize(context, value)
        self.assertEqual("accepted", report["decision_status"])
        self.assertEqual("local-structural-not-authenticated", report["trust"])
        value["decision"]["source_ids"] = []
        with self.assertRaises(ValueError):
            discovery.finalize(context, value)

    def test_stale_and_tampered_sources_fail_read_only(self):
        self.save("draft.toon", self.draft())
        self.run_cli("finalize", "--context", self.context_path, "--draft", "draft.toon", "--write")
        target = discovery.locations("example")["report"]
        before = (self.root / target).read_bytes()
        (self.root / "pilot.md").write_text("Different pilot data", encoding="utf-8")
        self.run_cli("verify", "--report", target, ok=False)
        self.assertEqual(before, (self.root / target).read_bytes())
        self.run_cli("finalize", "--context", self.context_path, "--draft", "draft.toon", "--write", "--replace", ok=False)
        self.assertEqual(before, (self.root / target).read_bytes())

    def test_report_and_markdown_tampering_fail(self):
        self.save("draft.toon", self.draft())
        self.run_cli("finalize", "--context", self.context_path, "--draft", "draft.toon", "--write")
        target = discovery.locations("example")
        original = discovery.load(self.root, target["report"])
        broken = copy.deepcopy(original)
        broken["analysis"]["recommendation"]["rationale"] = "Tampered recommendation"
        self.save(target["report"], broken)
        self.run_cli("verify", "--report", target["report"], ok=False)
        self.save(target["report"], original)
        if "markdown" in target:
            (self.root / target["markdown"]).write_text("Tampered projection", encoding="utf-8")
            self.run_cli("verify", "--report", target["report"], ok=False)

    def test_changed_outputs_need_explicit_replace(self):
        self.save("draft.toon", self.draft())
        args = ("finalize", "--context", self.context_path, "--draft", "draft.toon", "--write")
        original = self.run_cli(*args).stdout
        changed = self.draft()
        changed["recommendation"]["rationale"] = "Changed but still conditional recommendation"
        self.save("draft.toon", changed)
        self.run_cli(*args, ok=False)
        target = discovery.locations("example")["report"]
        self.assertEqual(original.encode(), (self.root / target).read_bytes())
        updated = self.run_cli(*args, "--replace").stdout
        self.assertNotEqual(original, updated)
        self.run_cli("verify", "--report", target)

    def test_unsafe_paths_invalid_utf8_size_and_self_source_are_rejected(self):
        for path in ("../request.md", "/tmp/request.md", "C:/request.md", "a/../request.md", ".git/config", "a\\b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                discovery.prepare(self.root, "example", path, [], "quick")
        for name in ("../bad", "bad/name", "UPPER", "x" * 81):
            with self.assertRaises(ValueError):
                discovery.prepare(self.root, name, "request.md", [], "quick")
        (self.root / "bad.md").write_bytes(b"\xff")
        self.run_cli("prepare", "--feature", "example", "--request", "bad.md", ok=False)
        (self.root / "bad.md").write_bytes(b"x" * (discovery.MAX_SOURCE_BYTES + 1))
        self.run_cli("prepare", "--feature", "example", "--request", "bad.md", ok=False)
        self.run_cli("prepare", "--feature", "example", "--request", discovery.locations("example")["report"], ok=False)

    def test_symlink_source_or_output_does_not_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory).resolve()
            (outside / "sentinel").write_text("preserve")
            try:
                (self.root / "linked").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("host cannot create symlink fixtures")
            self.run_cli("prepare", "--feature", "example", "--request", "linked/sentinel", ok=False)
            base = "specs-refiniment" if discovery.PREFIX == "ai-sdlc" else ".ai-sdlc-loop"
            (self.root / base).symlink_to(outside, target_is_directory=True)
            self.save("draft.toon", self.draft())
            self.run_cli("finalize", "--context", self.context_path, "--draft", "draft.toon", "--write", ok=False)
            self.assertEqual(["sentinel"], [p.name for p in outside.iterdir()])

    def test_multi_file_failure_restores_previous_outputs(self):
        outputs = {"result/a.toon": b"old a", "result/b.toon": b"old b"}
        discovery.atomic_write_many(self.root, outputs)
        os.chmod(self.root / "result/a.toon", 0o640)
        mode = (self.root / "result/a.toon").stat().st_mode & 0o777
        real_replace = discovery.os.replace
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated second output failure")
            real_replace(source, target)

        with patch.object(discovery.os, "replace", side_effect=fail_second):
            with self.assertRaises(OSError):
                discovery.atomic_write_many(self.root, {path: b"new" for path in outputs}, replace=True)
        for path, original in outputs.items():
            self.assertEqual(original, (self.root / path).read_bytes())
        self.assertEqual(mode, (self.root / "result/a.toon").stat().st_mode & 0o777)
        self.assertEqual([], list(self.root.rglob(".discovery-*")))

    def test_installed_helper_uses_only_sibling_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / ".agent/skills"
            shutil.copytree(SKILL_ROOT, installed / SKILL_ROOT.name, ignore=shutil.ignore_patterns("__pycache__"))
            runtime = SKILL_ROOT.parent / (discovery.PREFIX + "-shared-runtime")
            shutil.copytree(runtime, installed / runtime.name, ignore=shutil.ignore_patterns("__pycache__"))
            script = installed / SKILL_ROOT.name / "scripts/requirements_discovery.py"
            self.save("draft.toon", self.draft())
            result = self.run_cli("finalize", "--context", self.context_path, "--draft", "draft.toon", script=script)
            self.assertEqual(discovery.encoded(discovery.finalize(self.context, self.draft())), result.stdout.encode())

    def test_full_flow_precedence_and_context_mode_mismatch(self):
        result = self.run_cli("prepare", "--feature", "example", "--request", "request.md", "--quick-flow", "--full-flow")
        self.assertEqual("full", discovery.codec.loads(result.stdout)["flow_mode"])
        self.save("draft.toon", self.draft())
        self.run_cli("validate", "--context", self.context_path, "--draft", "draft.toon", "--full-flow", ok=False)

    def test_conflicting_positions_can_come_from_one_document(self):
        (self.root / "request.md").write_text("Every case requires individual review. Approve all cases in a batch.\n", encoding="utf-8")
        context = discovery.prepare(self.root, "example", "request.md", ["pilot.md"], "quick")
        value = self.draft(context)
        value["observations"][1].update(kind="contradiction", statement="The request contains conflicting individual and batch rules",
                                        source_ids=[context["request_source_id"]])
        self.assertEqual("complete", discovery.finalize(context, value)["packet_status"])

    def test_stdin_request_is_a_reproducible_snapshot_not_a_live_source_claim(self):
        command = [sys.executable, str(SCRIPT), "prepare", "--root", str(self.root), "--feature", "example",
                   "--request-stdin", "--source", "pilot.md", "--quick-flow"]
        content = "Разбери запрос: $(touch unexpected) <script>execute me</script>\n"
        first = subprocess.run(command, input=content, text=True, encoding="utf-8", capture_output=True, check=True)
        second = subprocess.run(command, input=content, text=True, encoding="utf-8", capture_output=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        context = discovery.codec.loads(first.stdout)
        snapshot = next(s for s in context["sources"] if s["kind"] == "snapshot")
        self.assertEqual(content, snapshot["content"])
        self.assertEqual("stdin:request", snapshot["path"])
        self.assertEqual(context, discovery.check_context(self.root, context))
        self.assertFalse((self.root / "unexpected").exists())
        snapshot["content"] = "tampered"
        with self.assertRaises(ValueError):
            discovery.check_context(self.root, context)

    def test_preparation_and_scaffolding_write_only_canonical_feature_files(self):
        target = discovery.locations("example")
        self.run_cli("prepare", "--feature", "example", "--request", "request.md", "--source", "pilot.md", "--quick-flow", "--write")
        self.assertEqual(discovery.encoded(self.context), (self.root / target["context"]).read_bytes())
        result = self.run_cli("scaffold", "--context", target["context"], "--as-of", "2026-09-07", "--write")
        self.assertEqual(result.stdout.encode(), (self.root / target["draft"]).read_bytes())
        self.assertFalse((self.root / target["report"]).exists())

    def test_state_checks_are_explicit_read_only_and_transitions_are_rejected(self):
        self.save("draft.toon", self.draft())
        args = ("validate", "--context", self.context_path, "--draft", "draft.toon")
        self.run_cli(*args, "--state-check", ok=False)
        relative = ("specs-refiniment/example/_ai_sdlc/state.toon" if discovery.PREFIX == "ai-sdlc"
                    else ".ai-sdlc-loop/example/state.toon")
        self.save(relative, {"feature": "example", "stage": "existing"})
        original = (self.root / relative).read_bytes()
        self.run_cli(*args, "--state-check")
        self.run_cli(*args, "--begin-state", ok=False)
        self.run_cli(*args, "--complete-state", ok=False)
        self.assertEqual(original, (self.root / relative).read_bytes())
        self.save(relative, {"feature": "another-feature"})
        self.run_cli(*args, "--state-check", ok=False)


if __name__ == "__main__":
    unittest.main()
