#!/usr/bin/env python3
"""Functional tests for deterministic engineering quality-gate evidence."""

from __future__ import annotations

import copy
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OBJECT_SUFFIX = "." + bytes((106, 115, 111, 110)).decode("ascii")
SCRIPT = (
    ROOT
    / "skills"
    / "ai-sdlc-engineering-quality-gate"
    / "scripts"
    / "engineering_quality_gate.py"
)
RUNTIME = ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from ai_sdlc_toon import decode_toon, encode_toon


class EngineeringQualityGateTests(unittest.TestCase):
    """Exercise the helper through its public command-line interface."""

    maxDiff = None

    def run_command(
        self,
        *arguments: str | Path,
        expected: int = 0,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *(str(item) for item in arguments)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def git(self, repository: Path, *arguments: str) -> str:
        environment = dict(os.environ)
        environment.update(
            {
                "LC_ALL": "C",
                "GIT_AUTHOR_DATE": "2025-01-01T00:00:00+0000",
                "GIT_COMMITTER_DATE": "2025-01-01T00:00:00+0000",
            }
        )
        result = subprocess.run(
            ["git", *arguments],
            cwd=repository,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"git {' '.join(arguments)} failed:\n{result.stderr}",
        )
        return result.stdout.strip()

    def create_repository(self, parent: Path, name: str = "repository") -> Path:
        repository = parent / name
        (repository / "app").mkdir(parents=True)
        (repository / "tests").mkdir()
        (repository / "AGENTS.md").write_text(
            "# Repository instructions\n\nKeep services small and explicit.\n",
            encoding="utf-8",
        )
        (repository / "Makefile").write_text(
            "test:\n\tpython3 -m unittest discover -s tests\n\n"
            "lint:\n\tpython3 -m compileall app\n",
            encoding="utf-8",
        )
        (repository / "app" / "service.py").write_text(
            "def normalize(value):\n    return value.strip().lower()\n",
            encoding="utf-8",
        )
        (repository / "app" / "account_service.py").write_text(
            "def account_name(value):\n    return value.strip()\n",
            encoding="utf-8",
        )
        (repository / "app" / "order_service.py").write_text(
            "def order_name(value):\n    return value.strip()\n",
            encoding="utf-8",
        )
        (repository / "tests" / "test_service.py").write_text(
            "import unittest\n\n"
            "class ServiceTests(unittest.TestCase):\n"
            "    def test_placeholder(self):\n"
            "        self.assertTrue(True)\n",
            encoding="utf-8",
        )
        self.git(repository, "init", "-q")
        self.git(repository, "config", "user.name", "Quality Gate Tests")
        self.git(repository, "config", "user.email", "quality-gate@example.invalid")
        self.git(repository, "add", ".")
        self.git(repository, "commit", "--no-gpg-sign", "-qm", "baseline")
        (repository / "app" / "service.py").write_text(
            "def normalize(value):\n"
            "    if value is None:\n"
            "        return \"\"\n"
            "    return value.strip().lower()\n",
            encoding="utf-8",
        )
        return repository

    def context_path(self, repository: Path) -> Path:
        return repository / ".ai-sdlc" / "engineering-quality-gate" / "context.toon"

    def draft_path(self, repository: Path) -> Path:
        return repository / ".ai-sdlc" / "engineering-quality-gate" / "quality-gate-draft.toon"

    def report_path(self, repository: Path) -> Path:
        return repository / ".ai-sdlc" / "engineering-quality-gate" / "quality-report.toon"

    def compile_context(self, repository: Path, *, output: Path | None = None) -> dict[str, Any]:
        target = output or self.context_path(repository)
        self.run_command(
            "context",
            "--root",
            repository,
            "--request",
            "Add safe account normalization to the service",
            "--base",
            "HEAD",
            "--max-candidates",
            "5",
            "--quick-flow",
            "--output",
            target.relative_to(repository),
        )
        decoded = decode_toon(target.read_text(encoding="utf-8"))
        self.assertIsInstance(decoded, dict)
        return decoded

    def verification(
        self,
        identifier: str,
        *,
        phase: str = "final",
        required: bool = True,
        status: str = "pass",
    ) -> dict[str, Any]:
        if status == "unavailable":
            command: list[str] = []
            exit_code: int | None = None
        else:
            command = ["python3", "-m", "unittest", "discover", "-s", "tests"]
            exit_code = 0 if status == "pass" else (1 if status == "fail" else None)
        return {
            "id": identifier,
            "kind": "tests",
            "phase": phase,
            "required": required,
            "status": status,
            "command": command,
            "exit_code": exit_code,
            "evidence": [f"Deterministic test evidence for {identifier}"],
            "reason": "The repository test command was evaluated.",
        }

    def draft(
        self,
        context: dict[str, Any],
        *,
        status: str = "PASS",
        fixed: list[dict[str, Any]] | None = None,
        remaining: list[dict[str, Any]] | None = None,
        verification: list[dict[str, Any]] | None = None,
        ready: bool = True,
        blocking_reasons: list[str] | None = None,
    ) -> dict[str, Any]:
        examples = [item["path"] for item in context["candidate_examples"][:2]]
        return {
            "schema": "ai-sdlc-engineering-quality-gate-draft/v1",
            "status": status,
            "summary": "Repository-grounded review found the implementation ready.",
            "repository_profile": {
                "architecture": {
                    "pattern": "small service modules",
                    "relevant_layers": ["application"],
                },
                "conventions": [
                    {
                        "name": "service shape",
                        "value": "small functions with explicit normalization",
                        "evidence": examples or ["No comparable tracked implementation was available."],
                    }
                ],
                "representative_examples": examples,
                "example_shortfall_reason": (
                    "The bounded repository context exposed fewer than two comparable files."
                    if len(examples) < 2
                    else ""
                ),
                "applicable_rules": ["Keep service behavior explicit and covered by tests."],
            },
            "findings_fixed": fixed or [],
            "remaining_findings": remaining or [],
            "verification": verification or [self.verification("VERIFY-001")],
            "change_scope": {
                "new_dependencies": [],
                "unrelated_changes": [],
            },
            "quality_evidence": {
                "repository_consistency": ["Compared the change with neighboring service modules."],
                "correctness": ["Reviewed null and normalized-string behavior."],
                "testing": ["Recorded an executed deterministic repository test command."],
                "simplicity": ["The change adds no dependency or new abstraction."],
            },
            "final_decision": {
                "ready_for_next_stage": ready,
                "blocking_reasons": blocking_reasons or [],
            },
        }

    def finding(
        self,
        *,
        resolution: str,
        severity: str = "medium",
        blocking: bool = False,
    ) -> dict[str, Any]:
        fixed = resolution == "fixed"
        return {
            "id": "QG-001",
            "severity": severity,
            "category": "correctness",
            "file": "app/service.py",
            "location": "normalize",
            "issue": "The initial implementation did not make null behavior explicit.",
            "evidence": ["app/service.py accepts caller-controlled input."],
            "impact": "A null input could fail before repository validation runs.",
            "recommended_fix": "Handle the repository-supported empty input explicitly.",
            "blocking": blocking,
            "resolution": resolution,
            "fix": "Added explicit null handling and a focused regression check." if fixed else "",
            "reason_not_fixed": "Product behavior requires clarification." if not fixed else "",
        }

    def write_toon(self, path: Path, value: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encode_toon(value), encoding="utf-8")

    def finalize(
        self,
        repository: Path,
        draft: dict[str, Any],
        *,
        expected: int = 0,
    ) -> subprocess.CompletedProcess[str]:
        self.write_toon(self.draft_path(repository), draft)
        return self.run_command(
            "finalize",
            "--root",
            repository,
            "--context",
            self.context_path(repository).relative_to(repository),
            "--draft",
            self.draft_path(repository).relative_to(repository),
            "--output",
            self.report_path(repository).relative_to(repository),
            expected=expected,
        )

    def test_context_is_identical_across_equivalent_roots_and_repeated_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            first = self.create_repository(parent, "first")
            second = parent / "second"
            shutil.copytree(first, second, symlinks=True)

            first_context = self.compile_context(first)
            second_context = self.compile_context(second)
            first_bytes = self.context_path(first).read_bytes()
            second_bytes = self.context_path(second).read_bytes()

            self.assertEqual(first_bytes, second_bytes)
            self.assertEqual(first_context, second_context)
            self.assertNotIn(str(first), first_bytes.decode("utf-8"))
            self.assertNotIn(str(second), second_bytes.decode("utf-8"))
            self.assertGreaterEqual(len(first_context["candidate_examples"]), 2)
            self.assertIn(first_context["changed_files"][0]["mode"], {"100644", "100755"})
            make_sources = [
                item["source"]
                for item in first_context["verification_candidates"]
                if item["source"].lower().endswith("/makefile")
            ]
            self.assertEqual({"./Makefile"}, set(make_sources))
            self.assertEqual(2, len(make_sources))

            repeated = first / ".ai-sdlc" / "engineering-quality-gate" / "quality-gate-context.toon"
            repeated_context = self.compile_context(first, output=repeated)
            self.assertEqual(first_context, repeated_context)
            self.assertEqual(first_bytes, repeated.read_bytes())

    def test_context_without_output_is_read_only_canonical_toon(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            result = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Add safe account normalization to the service",
                "--base",
                "HEAD",
                "--quick-flow",
                "--state-check",
            )
            context = decode_toon(result.stdout)
            self.assertEqual("ai-sdlc-engineering-quality-gate-context/v1", context["schema"])
            self.assertEqual(result.stdout, encode_toon(context))
            self.assertFalse(self.context_path(repository).exists())

            transition = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Add safe account normalization to the service",
                "--begin-state",
                expected=2,
            )
            self.assertIn("cannot begin or complete", transition.stderr)

    def test_pass_report_finalizes_and_verifies_as_current(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            context = self.compile_context(repository)

            self.finalize(repository, self.draft(context))
            report = decode_toon(self.report_path(repository).read_text(encoding="utf-8"))

            self.assertEqual(report["schema"], "ai-sdlc-engineering-quality-gate/v1")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["context_fingerprint"], context["context_fingerprint"])
            self.assertEqual(report["change_fingerprint"], context["change_fingerprint"])
            self.assertEqual(
                report["change_scope"]["files_changed"],
                context["change_scope"]["files_changed"],
            )
            self.assertTrue(report["final_decision"]["ready_for_next_stage"])
            self.assertRegex(report["report_fingerprint"], r"^sha256:[0-9a-f]{64}$")

            verified = self.run_command(
                "verify",
                "--root",
                repository,
                "--report",
                self.report_path(repository).relative_to(repository),
            )
            self.assertIn("current PASS sha256:", verified.stdout)

    def test_diff_change_changes_context_and_makes_signed_report_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            original_context = self.compile_context(repository)
            self.finalize(repository, self.draft(original_context))

            (repository / "app" / "service.py").write_text(
                "def normalize(value):\n"
                "    if value is None:\n"
                "        return \"\"\n"
                "    return value.strip().casefold()\n",
                encoding="utf-8",
            )
            stale = self.run_command(
                "verify",
                "--root",
                repository,
                "--report",
                self.report_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("stale", stale.stderr)

            refreshed_path = (
                repository
                / ".ai-sdlc"
                / "engineering-quality-gate"
                / "quality-gate-post-fix-context.toon"
            )
            refreshed = self.compile_context(repository, output=refreshed_path)
            self.assertNotEqual(original_context["change_fingerprint"], refreshed["change_fingerprint"])
            self.assertNotEqual(original_context["context_fingerprint"], refreshed["context_fingerprint"])

    def test_file_mode_and_reserved_basename_source_drift_make_report_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            basename_source = repository / "app" / "context.toon"
            basename_source.write_text("domain context\n", encoding="utf-8")
            context = self.compile_context(repository)
            self.assertIn("app/context.toon", [item["path"] for item in context["changed_files"]])
            self.finalize(repository, self.draft(context))

            basename_source.write_text("changed domain context\n", encoding="utf-8")
            stale_content = self.run_command(
                "verify",
                "--root",
                repository,
                "--report",
                self.report_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("stale", stale_content.stderr)

            context = self.compile_context(repository)
            self.finalize(repository, self.draft(context))
            service = repository / "app" / "service.py"
            service.chmod(service.stat().st_mode | 0o111)
            stale_mode = self.run_command(
                "verify",
                "--root",
                repository,
                "--report",
                self.report_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("stale", stale_mode.stderr)

    def test_malformed_and_unsubstantiated_fail_drafts_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            context = self.compile_context(repository)

            malformed = self.draft(context)
            malformed["unexpected"] = "not permitted"
            result = self.finalize(repository, malformed, expected=2)
            self.assertIn("invalid keys", result.stderr)

            unsubstantiated_fail = self.draft(
                context,
                status="FAIL",
                ready=False,
                blocking_reasons=["Review did not approve delivery."],
            )
            result = self.finalize(repository, unsubstantiated_fail, expected=2)
            self.assertIn("evidence-backed blocking condition", result.stderr)

    def test_valid_fail_report_is_not_accepted_as_ready_current_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            context = self.compile_context(repository)
            high_finding = self.finding(
                resolution="remaining",
                severity="high",
                blocking=True,
            )
            failure = self.draft(
                context,
                status="FAIL",
                remaining=[high_finding],
                ready=False,
                blocking_reasons=["QG-001 is an unresolved High finding."],
            )
            self.finalize(repository, failure)

            rejected = self.run_command(
                "verify",
                "--root",
                repository,
                "--report",
                self.report_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("not ready", rejected.stderr.lower())

    def test_unsafe_and_symlink_output_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            repository = self.create_repository(parent)
            escaped = parent / "escaped.toon"

            unsafe = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the service change",
                "--output",
                "../escaped.toon",
                expected=2,
            )
            self.assertIn("unsafe repository-relative path", unsafe.stderr)
            self.assertFalse(escaped.exists())

            absolute = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the service change",
                "--output",
                repository / "absolute.toon",
                expected=2,
            )
            self.assertIn("repository-relative", absolute.stderr)
            self.assertFalse((repository / "absolute.toon").exists())

            wrong_extension = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the service change",
                "--output",
                "context" + OBJECT_SUFFIX,
                expected=2,
            )
            self.assertIn(".toon extension", wrong_extension.stderr)
            self.assertFalse((repository / ("context" + OBJECT_SUFFIX)).exists())

            arbitrary = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the service change",
                "--output",
                "arbitrary.toon",
                expected=2,
            )
            self.assertIn("canonical quality-gate state directory", arbitrary.stderr)
            self.assertFalse((repository / "arbitrary.toon").exists())

            outside = parent / "outside.toon"
            outside.write_text("sentinel\n", encoding="utf-8")
            link = repository / "context.toon"
            link.symlink_to(outside)
            symlink = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the service change",
                "--output",
                "context.toon",
                expected=2,
            )
            self.assertIn("symlink", symlink.stderr.lower())
            self.assertEqual(outside.read_text(encoding="utf-8"), "sentinel\n")

    def test_fixed_findings_require_before_and_passing_post_fix_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            context = self.compile_context(repository)
            finding = self.finding(resolution="fixed")

            missing_before = self.draft(
                context,
                fixed=[copy.deepcopy(finding)],
                verification=[self.verification("VERIFY-002", phase="after_fix")],
            )
            result = self.finalize(repository, missing_before, expected=2)
            self.assertIn("before_fix verification evidence", result.stderr)

            failing_after = self.draft(
                context,
                fixed=[copy.deepcopy(finding)],
                verification=[
                    self.verification("VERIFY-001", phase="before_fix"),
                    self.verification("VERIFY-002", phase="after_fix", status="fail"),
                ],
            )
            result = self.finalize(repository, failing_after, expected=2)
            self.assertIn("passing required after_fix or final verification", result.stderr)

            corrected = self.draft(
                context,
                fixed=[copy.deepcopy(finding)],
                verification=[
                    self.verification("VERIFY-001", phase="before_fix", status="fail"),
                    self.verification("VERIFY-002", phase="after_fix"),
                ],
            )
            self.finalize(repository, corrected)
            report = decode_toon(self.report_path(repository).read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["findings_fixed"][0]["id"], "QG-001")
            self.assertEqual(
                [item["phase"] for item in report["verification"]],
                ["before_fix", "after_fix"],
            )

    def test_verification_contract_rejects_invalid_ids_and_non_integer_pass_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = self.create_repository(Path(temporary))
            context = self.compile_context(repository)

            invalid_id = self.draft(
                context,
                verification=[self.verification("VERIFY-AFTER")],
            )
            rejected_id = self.finalize(repository, invalid_id, expected=2)
            self.assertIn("must match KIND-###", rejected_id.stderr)

            boolean_code = self.verification("VERIFY-001")
            boolean_code["exit_code"] = True
            rejected_boolean = self.finalize(
                repository,
                self.draft(context, verification=[boolean_code]),
                expected=2,
            )
            self.assertIn("pass requires argv and exit_code 0", rejected_boolean.stderr)

            float_code = self.draft(context)
            self.write_toon(self.draft_path(repository), float_code)
            literal = self.draft_path(repository).read_text(encoding="utf-8")
            self.draft_path(repository).write_text(
                literal.replace("exit_code: 0\n", "exit_code: 0.0\n", 1),
                encoding="utf-8",
            )
            rejected_float = self.run_command(
                "finalize",
                "--root",
                repository,
                "--context",
                self.context_path(repository).relative_to(repository),
                "--draft",
                self.draft_path(repository).relative_to(repository),
                "--output",
                self.report_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("pass requires argv and exit_code 0", rejected_float.stderr)

            duplicate_argv = self.verification("VERIFY-001")
            duplicate_argv["command"] = ["python3", "-m", "unittest", "unittest"]
            self.finalize(repository, self.draft(context, verification=[duplicate_argv]))

    def test_empty_diff_external_config_symlink_and_artifact_overwrite_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            repository = self.create_repository(parent)
            self.git(repository, "restore", "app/service.py")
            empty = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the service change",
                expected=2,
            )
            self.assertIn("non-empty implementation diff", empty.stderr)

            external = parent / ("external-package" + OBJECT_SUFFIX)
            external.write_text(
                '{"scripts":{"verify":"external-command"}}\n',
                encoding="utf-8",
            )
            manifest = repository / "app" / ("package" + OBJECT_SUFFIX)
            manifest.symlink_to(external)
            self.git(repository, "add", "app/package" + OBJECT_SUFFIX)
            self.git(repository, "commit", "--no-gpg-sign", "-qm", "add symlink fixture")
            (repository / "app" / "service.py").write_text(
                "def normalize(value):\n    return value.strip().casefold()\n",
                encoding="utf-8",
            )
            context = self.compile_context(repository)
            self.assertNotIn(
                "app/package" + OBJECT_SUFFIX,
                [item["source"] for item in context["verification_candidates"]],
            )

            self.write_toon(self.draft_path(repository), self.draft(context))
            original_context = self.context_path(repository).read_bytes()
            overwrite = self.run_command(
                "finalize",
                "--root",
                repository,
                "--context",
                self.context_path(repository).relative_to(repository),
                "--draft",
                self.draft_path(repository).relative_to(repository),
                "--output",
                self.context_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("report artifact", overwrite.stderr)
            self.assertEqual(original_context, self.context_path(repository).read_bytes())

    def test_dirty_nested_git_worktree_is_rejected_until_reviewed_separately(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            nested = self.create_repository(parent, "nested")
            self.git(nested, "add", "app/service.py")
            self.git(nested, "commit", "--no-gpg-sign", "-qm", "nested implementation")

            repository = self.create_repository(parent, "parent")
            self.git(repository, "restore", "app/service.py")
            self.git(
                repository,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-q",
                str(nested),
                "modules/nested",
            )
            self.git(repository, "add", ".gitmodules", "modules/nested")
            self.git(repository, "commit", "--no-gpg-sign", "-qm", "add nested repository")
            (repository / "modules" / "nested" / "app" / "service.py").write_text(
                "def normalize(value):\n    return value.casefold()\n",
                encoding="utf-8",
            )

            rejected = self.run_command(
                "context",
                "--root",
                repository,
                "--request",
                "Review the nested implementation change",
                "--output",
                self.context_path(repository).relative_to(repository),
                expected=2,
            )
            self.assertIn("run the gate in its nested worktree first", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
