#!/usr/bin/env python3
"""Cross-skill integration tests for ai-sdlc-spec-state."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from spec_state import ensure_config_or_wizard, fetch_spec_state, publish_spec_state, status_spec_state
from spec_state_config import CONFIG_FILENAME, load_config


class TestCrossSkillIntegration(unittest.TestCase):
    """Verify that calling skills deterministically invoke spec-state and trigger wizard when needed."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.temp_dir.name)
        self.repo_dir = self.root / "inventory-service"
        self.repo_dir.mkdir()
        (self.repo_dir / "pyproject.toml").write_text('[project]\nname = "inventory-service"\nversion = "1.2.0"\n', encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_downstream_skill_entry_triggers_wizard_when_config_absent(self):
        # 1. Config does not exist initially
        self.assertFalse((self.repo_dir / CONFIG_FILENAME).exists())

        # 2. Downstream skill calls fetch_spec_state
        res = fetch_spec_state(feature="stock-replenishment", root=self.repo_dir, interactive=False)

        # 3. Verify wizard created the config deterministically
        self.assertTrue((self.repo_dir / CONFIG_FILENAME).is_file())
        cfg = load_config(root=self.repo_dir)
        self.assertEqual(cfg.repository.id, "inventory-service")
        self.assertEqual(cfg.repository.version, "1.2.0")

        # 4. Context was staged for the downstream skill
        staged_context = Path(res["staged_context"])
        self.assertTrue(staged_context.is_dir())

    def test_downstream_skill_publish_writes_spec_id_and_commits(self):
        # Publish without pre-existing config also bootstraps via wizard
        pub_res = publish_spec_state(
            feature="barcode-scanner",
            artifacts={
                "spec": "# Barcode Spec",
                "plan": "# Barcode Plan",
            },
            ticket_id="INV-99",
            logical_spec_id="SPEC-GLOBAL-INVENTORY",
            root=self.repo_dir,
            interactive=False,
        )
        self.assertEqual(pub_res["feature"], "barcode-scanner")
        self.assertIn("spec", pub_res["published"])
        spec_text = Path(pub_res["published"]["spec"]).read_text(encoding="utf-8")
        self.assertIn("spec_id: SPEC-GLOBAL-INVENTORY", spec_text)
        self.assertIn("ticket_id: INV-99", spec_text)


if __name__ == "__main__":
    unittest.main()
