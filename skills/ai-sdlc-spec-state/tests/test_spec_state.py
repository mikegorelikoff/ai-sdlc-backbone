#!/usr/bin/env python3
"""Comprehensive test suite for ai-sdlc-spec-state."""

from __future__ import annotations

import datetime
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

_SHARED = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
import ai_sdlc_toon as toon_codec  # noqa: E402

from spec_state_config import (
    CONFIG_FILENAME,
    SCHEMA_NAME,
    SpecStateConfig,
    init_config,
    load_config,
    validate_config,
)
from spec_state_rotation import (
    ImpactScorer,
    apply_retention,
    check_index_freshness,
    check_rotation_triggers,
    generate_repository_index,
    rotate_baseline_and_decisions,
)
from spec_state_storage import (
    GitStorage,
    publish_feature_artifacts,
    resolve_spec_hierarchy,
)


class TestSpecStateConfig(unittest.TestCase):
    """Configuration parsing, validation, and initialization tests."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_config_creates_valid_file(self):
        cfg = init_config(
            target_path=self.path,
            repo_id="payment-service",
            version="2.1.0",
            storage_repo="./mock-storage",
            branch="main",
            root="specs",
        )
        self.assertTrue((self.path / CONFIG_FILENAME).is_file())
        self.assertEqual(cfg.repository.id, "payment-service")
        self.assertEqual(cfg.repository.version, "2.1.0")
        self.assertEqual(cfg.storage.repository, "./mock-storage")
        self.assertEqual(cfg.storage.branch, "main")
        self.assertEqual(cfg.lifecycle.refresh_index_after_days, 14)
        self.assertEqual(cfg.lifecycle.rotation_spec_threshold, 50)
        self.assertEqual(cfg.retention.keep_current_baseline, 1)
        self.assertEqual(cfg.retention.keep_previous_baselines, 2)

    def test_init_config_existing_without_force_fails(self):
        init_config(target_path=self.path, repo_id="first")
        with self.assertRaises(FileExistsError):
            init_config(target_path=self.path, repo_id="second", force=False)

    def test_validate_config_detects_errors(self):
        invalid_data = {
            "schema": "wrong-schema/v1",
            "enabled": "not-a-bool",
            "storage": {
                "provider": "s3",  # only git allowed
                "repository": "",
                "branch": "",
                "root": "",
            },
            "repository": {
                "id": "invalid ID with spaces!",
                "version": "",
            },
            "lifecycle": {
                "refresh_index_after_days": 0,
                "rotation_spec_threshold": -5,
            },
            "retention": {
                "keep_current_baseline": 0,
                "keep_previous_baselines": -1,
            },
            "multi_repo": {
                "strategy": "invalid-strategy",
            },
        }
        errors = validate_config(invalid_data)
        self.assertGreaterEqual(len(errors), 7)
        self.assertTrue(any("schema must be" in e for e in errors))
        self.assertTrue(any("storage.provider must be 'git'" in e for e in errors))
        self.assertTrue(any("repository.id must be" in e for e in errors))
        self.assertTrue(any("refresh_index_after_days" in e for e in errors))
        self.assertTrue(any("multi_repo.strategy" in e for e in errors))

    def test_load_config_missing_raises_file_not_found(self):
        empty_dir = self.path / "empty"
        empty_dir.mkdir()
        with self.assertRaises(FileNotFoundError):
            load_config(root=empty_dir)


class TestSpecStateStorageAndHierarchy(unittest.TestCase):
    """Storage management, artifact publishing, and hierarchy detection."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.temp_dir.name)
        self.project_dir = self.root / "my-project"
        self.project_dir.mkdir()
        self.storage_repo_dir = self.root / "agent-planning-storage"
        self.storage_repo_dir.mkdir()

        # Initialize local storage git repo
        subprocess.run(["git", "init", "-b", "main"], cwd=self.storage_repo_dir, check=True, capture_output=True)
        # Configure test git user
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=self.storage_repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=self.storage_repo_dir, check=True)

        # Create config pointing to local storage repo
        self.config = init_config(
            target_path=self.project_dir,
            repo_id="auth-service",
            version="1.0.0",
            storage_repo=str(self.storage_repo_dir),
            branch="main",
            root="specs",
        )
        self.storage = GitStorage(self.config, workspace_root=self.project_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_publish_feature_artifacts(self):
        spec_content = "# Auth Feature Spec\n\nRequirements for OAuth2 login."
        plan_content = "# Implementation Plan\n\nSteps to implement."
        dec_content = "# Decision Log\n\nDEC-001: Use PKCE."

        res = publish_feature_artifacts(
            config=self.config,
            storage=self.storage,
            feature="oauth2-login",
            artifact_files={
                "spec": spec_content,
                "plan": plan_content,
                "decisions": dec_content,
            },
            ticket_id="AUTH-101",
            logical_spec_id="SPEC-AUTH-GLOBAL",
        )

        self.assertEqual(res["feature"], "oauth2-login")
        self.assertIn("spec", res["published"])
        self.assertIn("plan", res["published"])
        self.assertIn("decisions", res["published"])

        spec_file = Path(res["published"]["spec"])
        self.assertTrue(spec_file.is_file())
        file_text = spec_file.read_text(encoding="utf-8")
        self.assertIn("spec_id: SPEC-AUTH-GLOBAL", file_text)
        self.assertIn("ticket_id: AUTH-101", file_text)
        self.assertIn("repository_id: auth-service", file_text)

        # Check git commit
        git_log = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"], cwd=self.storage_repo_dir, capture_output=True, text=True, check=True
        )
        self.assertIn("synchronize artifacts for feature 'oauth2-login'", git_log.stdout)

    def test_spec_hierarchy_resolution(self):
        specs_dir = self.storage.get_repo_specs_dir()

        # Seed storage with baseline, index, older specs, and incremental specs
        b_file = specs_dir / "baselinespec-auth-service-1.0.0-20260901.md"
        b_file.write_text("# Baseline 1.0.0", encoding="utf-8")

        i_file = specs_dir / "20260920-auth-service.md"
        i_file.write_text("# Index", encoding="utf-8")

        da_file = specs_dir / "decision-knowledgebase-auth-service-1.0.0-20260901.md"
        da_file.write_text("# Decision Archive", encoding="utf-8")

        # Spec newer than baseline
        inc_spec = specs_dir / "20260915-token-refresh-spec.md"
        inc_spec.write_text("# Incremental Spec", encoding="utf-8")

        # Spec older than baseline
        old_spec = specs_dir / "20260820-legacy-spec.md"
        old_spec.write_text("# Old Spec", encoding="utf-8")

        # Decision log newer than archive
        inc_dec = specs_dir / "20260916-token-decisions.md"
        inc_dec.write_text("# Incremental Decisions", encoding="utf-8")

        hierarchy = resolve_spec_hierarchy(self.storage)

        self.assertIsNotNone(hierarchy.latest_baseline)
        self.assertEqual(hierarchy.latest_baseline_version, "1.0.0")
        self.assertEqual(hierarchy.latest_baseline_date, "20260901")

        self.assertIsNotNone(hierarchy.latest_index)
        self.assertEqual(hierarchy.latest_index_date, "20260920")

        self.assertIsNotNone(hierarchy.latest_decision_archive)
        self.assertEqual(hierarchy.latest_decision_archive_date, "20260901")

        # Only specs >= 20260901 should be incremental
        self.assertEqual(len(hierarchy.feature_specs_since_baseline), 1)
        self.assertEqual(hierarchy.feature_specs_since_baseline[0].name, "20260915-token-refresh-spec.md")

        self.assertEqual(len(hierarchy.decision_logs_since_archive), 1)
        self.assertEqual(hierarchy.decision_logs_since_archive[0].name, "20260916-token-decisions.md")


class TestSpecStateRotationAndLifecycle(unittest.TestCase):
    """Index freshness, rotation triggers, rotation execution, and retention tests."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.temp_dir.name)
        self.project_dir = self.root / "proj"
        self.project_dir.mkdir()
        self.storage_dir = self.root / "storage"
        self.storage_dir.mkdir()
        subprocess.run(["git", "init", "-b", "main"], cwd=self.storage_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=self.storage_dir, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=self.storage_dir, check=True)

        self.config = init_config(
            target_path=self.project_dir,
            repo_id="billing",
            version="2.0.0",
            storage_repo=str(self.storage_dir),
            branch="main",
            root="specs",
        )
        self.storage = GitStorage(self.config, workspace_root=self.project_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_check_index_freshness(self):
        # Missing index
        res = check_index_freshness(None, threshold_days=14)
        self.assertEqual(res["status"], "missing")
        self.assertTrue(res["needs_refresh"])

        # Fresh index (today)
        today_str = datetime.date.today().strftime("%Y%m%d")
        fresh_index = self.project_dir / f"{today_str}-billing.md"
        fresh_index.write_text("# Fresh Index", encoding="utf-8")
        res = check_index_freshness(fresh_index, threshold_days=14)
        self.assertEqual(res["status"], "fresh")
        self.assertFalse(res["needs_refresh"])
        self.assertEqual(res["age_days"], 0)

        # Stale index (30 days ago)
        old_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y%m%d")
        stale_index = self.project_dir / f"{old_date}-billing.md"
        stale_index.write_text("# Stale Index", encoding="utf-8")
        res = check_index_freshness(stale_index, threshold_days=14)
        self.assertEqual(res["status"], "needs-refresh")
        self.assertTrue(res["needs_refresh"])
        self.assertEqual(res["age_days"], 30)

    def test_check_rotation_triggers(self):
        specs_dir = self.storage.get_repo_specs_dir()

        # Seed a baseline with version 1.0.0 while config is 2.0.0 (version bump)
        b_file = specs_dir / "baselinespec-billing-1.0.0-20260101.md"
        b_file.write_text("# Baseline 1.0.0", encoding="utf-8")

        hierarchy = resolve_spec_hierarchy(self.storage)
        triggers = check_rotation_triggers(self.config, hierarchy)

        self.assertTrue(triggers["baseline_rotation_recommended"])
        self.assertTrue(triggers["version_changed"])
        self.assertIn("version bumped from 1.0.0 to 2.0.0", triggers["reason"])

    def test_rotate_baseline_and_decisions(self):
        specs_dir = self.storage.get_repo_specs_dir()

        # Add existing baseline and some incremental specs
        b_file = specs_dir / "baselinespec-billing-1.9.0-20260101.md"
        b_file.write_text("# Old Baseline\nInitial scope.", encoding="utf-8")

        da_file = specs_dir / "decision-knowledgebase-billing-1.9.0-20260101.md"
        da_file.write_text("# Old Decisions\nDEC-1: DB choice.", encoding="utf-8")

        s1 = specs_dir / "20260201-invoicing-spec.md"
        s1.write_text("---\nrepository_id: billing\n---\n# Invoicing\nInvoice generation rules.", encoding="utf-8")

        d1 = specs_dir / "20260201-invoicing-decisions.md"
        d1.write_text("---\nrepository_id: billing\n---\n# Decisions\nUse PDF generator.", encoding="utf-8")

        hierarchy = resolve_spec_hierarchy(self.storage)
        rot_res = rotate_baseline_and_decisions(self.config, self.storage, hierarchy, force=True)

        self.assertEqual(rot_res["status"], "rotated")
        self.assertEqual(rot_res["specs_compacted"], 1)
        self.assertEqual(rot_res["decisions_compacted"], 1)

        # Check newly created baseline and decision knowledgebase
        new_b = Path(rot_res["baseline"])
        self.assertTrue(new_b.is_file())
        b_text = new_b.read_text(encoding="utf-8")
        self.assertIn("Invoice generation rules.", b_text)
        self.assertIn("Supersedes baseline: `baselinespec-billing-1.9.0-20260101.md`", b_text)

        new_da = Path(rot_res["decision_archive"])
        self.assertTrue(new_da.is_file())
        da_text = new_da.read_text(encoding="utf-8")
        self.assertIn("Use PDF generator.", da_text)
        self.assertIn("Supersedes decision knowledgebase", da_text)

    def test_apply_retention_policy(self):
        specs_dir = self.storage.get_repo_specs_dir()

        # Create 4 baselines: retention keeps 1 current + 2 previous = 3 total
        b1 = specs_dir / "baselinespec-billing-1.0.0-20260101.md"
        b1.write_text("# B1", encoding="utf-8")
        b2 = specs_dir / "baselinespec-billing-1.1.0-20260201.md"
        b2.write_text("# B2", encoding="utf-8")
        b3 = specs_dir / "baselinespec-billing-1.2.0-20260301.md"
        b3.write_text("# B3", encoding="utf-8")
        b4 = specs_dir / "baselinespec-billing-1.3.0-20260401.md"
        b4.write_text("# B4", encoding="utf-8")

        # Old spec before oldest retained baseline (20260201)
        old_spec = specs_dir / "20251215-prehistoric-spec.md"
        old_spec.write_text("# Old", encoding="utf-8")

        hierarchy = resolve_spec_hierarchy(self.storage)

        # Skipped when cleanup is False and force is False
        res = apply_retention(self.config, self.storage, hierarchy, force=False)
        self.assertEqual(res["status"], "skipped_by_policy")

        # Force cleanup
        res = apply_retention(self.config, self.storage, hierarchy, force=True)
        self.assertEqual(res["status"], "cleaned")
        self.assertIn("baselinespec-billing-1.0.0-20260101.md", res["cleaned"])
        self.assertIn("20251215-prehistoric-spec.md", res["cleaned"])

        # Retained baselines: B4, B3, B2
        self.assertEqual(len(res["retained_baselines"]), 3)
        self.assertTrue((specs_dir / "archive" / "baselinespec-billing-1.0.0-20260101.md").is_file())

    def test_impact_scorer(self):
        scorer = ImpactScorer()
        files = [
            "src/service.py",
            "models/contract.toon",
            "docs/README.md",
            "tests/test_service.py",
        ]
        score = scorer.calculate_impact(files)
        # service.py (1) + contract.toon (3) + docs (0) + tests (0) = 4
        self.assertEqual(score, 4)
        self.assertFalse(scorer.should_refresh_index(score, threshold=10))
        self.assertTrue(scorer.should_refresh_index(score, threshold=4))


class TestSpecStateCLI(unittest.TestCase):
    """End-to-end command-line tests."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.temp_dir.name)
        self.script = _SCRIPTS / "spec_state.py"
        self.storage_repo = self.root / "storage-repo"
        self.storage_repo.mkdir()
        subprocess.run(["git", "init", "-b", "main"], cwd=self.storage_repo, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=self.storage_repo, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=self.storage_repo, check=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(self.script), *args],
            cwd=self.root,
            check=False,
            text=True,
            capture_output=True,
        )

    def test_cli_lifecycle(self):
        # 1. init
        init_res = self.run_cli("init", "--repo-id", "order-svc", "--storage-repo", str(self.storage_repo))
        self.assertEqual(init_res.returncode, 0, init_res.stderr)
        self.assertTrue((self.root / CONFIG_FILENAME).is_file())

        # 2. status
        status_res = self.run_cli("status", "--format", "json")
        self.assertEqual(status_res.returncode, 0, status_res.stderr)
        self.assertIn('"id": "order-svc"', status_res.stdout)

        # 3. refresh-index
        ref_res = self.run_cli("refresh-index", "--force", "--format", "json")
        self.assertEqual(ref_res.returncode, 0, ref_res.stderr)
        self.assertIn('"status": "refreshed"', ref_res.stdout)

        # 4. publish
        spec_dummy = self.root / "order-spec.md"
        spec_dummy.write_text("# Order Creation Spec", encoding="utf-8")
        pub_res = self.run_cli("publish", "--feature", "order-creation", "--spec", str(spec_dummy), "--format", "json")
        self.assertEqual(pub_res.returncode, 0, pub_res.stderr)
        self.assertIn('"feature": "order-creation"', pub_res.stdout)

        # 5. fetch
        fetch_res = self.run_cli("fetch", "--format", "json")
        self.assertEqual(fetch_res.returncode, 0, fetch_res.stderr)
        self.assertIn('"status": "success"', fetch_res.stdout)
        self.assertIn("repository-index.md", fetch_res.stdout)

    def test_cli_wizard_command(self):
        # Run wizard in fresh directory without .sdlc.toon
        sub_dir = self.root / "sub-project"
        sub_dir.mkdir()
        (sub_dir / "pyproject.toml").write_text('[project]\nname = "wz-service"\nversion = "3.2.1"\n', encoding="utf-8")

        res = subprocess.run(
            ["python3", str(self.script), "wizard", "--target", str(sub_dir), "--non-interactive"],
            cwd=sub_dir,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue((sub_dir / CONFIG_FILENAME).is_file())
        cfg = load_config(root=sub_dir)
        self.assertEqual(cfg.repository.id, "wz-service")
        self.assertEqual(cfg.repository.version, "3.2.1")


class TestSpecStateWizardAndDetection(unittest.TestCase):
    """Auto-detection and wizard behavior tests."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_detect_from_pyproject(self):
        from spec_state_config import detect_repo_id, detect_repo_version

        (self.path / "pyproject.toml").write_text('name = "cool-app"\nversion = "1.5.0"\n', encoding="utf-8")
        self.assertEqual(detect_repo_id(self.path), "cool-app")
        self.assertEqual(detect_repo_version(self.path), "1.5.0")

    def test_run_wizard_scaffolds_with_overrides(self):
        from spec_state_config import run_wizard

        cfg = run_wizard(
            workspace_root=self.path,
            interactive=False,
            defaults_override={
                "repo_id": "analytics-core",
                "version": "2.0.0",
                "storage_repo": "./storage",
                "refresh_days": 7,
                "rotation_specs": 25,
            },
        )
        self.assertTrue((self.path / CONFIG_FILENAME).is_file())
        self.assertEqual(cfg.repository.id, "analytics-core")
        self.assertEqual(cfg.lifecycle.refresh_index_after_days, 7)
        self.assertEqual(cfg.lifecycle.rotation_spec_threshold, 25)


if __name__ == "__main__":
    unittest.main()
