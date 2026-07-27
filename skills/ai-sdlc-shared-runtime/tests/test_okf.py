#!/usr/bin/env python3
"""Focused OKF v0.2 contract tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SCRIPTS))

from ai_sdlc_okf import (  # noqa: E402
    concept_metadata,
    migrate_bundle,
    migrate_concept_text,
    render_concept,
    render_frontmatter,
    concept_profile,
    validate_bundle,
    write_bundle_indexes,
)


class OkfContractTests(unittest.TestCase):
    def test_concept_has_portable_identity_and_default_actor(self) -> None:
        text = render_concept("# Requirements\n", profile_key="requirements.md")
        metadata = concept_metadata(text)
        self.assertEqual(metadata["type"], "ai-sdlc.requirements")
        self.assertEqual(metadata["status"], "draft")
        self.assertEqual(metadata["generated_by"], "process:ai-sdlc")
        self.assertTrue(metadata["generated_at"].endswith("Z"))

    def test_existing_actor_is_preserved_and_override_is_validated(self) -> None:
        original = render_concept(
            "# Requirements\n",
            profile_key="requirements.md",
            generated_by_override="human:maintainer",
        )
        migrated = migrate_concept_text(original, profile_key="requirements.md")
        self.assertEqual(concept_metadata(migrated)["generated_by"], "human:maintainer")
        with self.assertRaisesRegex(ValueError, "generated.by"):
            migrate_concept_text(
                original,
                profile_key="requirements.md",
                generated_by_override="anonymous",
            )

    def test_verification_requires_complete_evidence(self) -> None:
        with self.assertRaisesRegex(ValueError, "verified requires"):
            render_frontmatter(
                profile=concept_profile("requirements.md"),
                status="draft",
                generated_by="process:ai-sdlc",
                generated_at="2026-07-27T00:00:00Z",
                verified_by="human:reviewer",
            )

    def test_metadata_refresh_preserves_and_content_change_clears_verification(self) -> None:
        verified = "\n".join(
            render_frontmatter(
                profile=concept_profile("requirements.md"),
                status="stable",
                generated_by="process:ai-sdlc",
                generated_at="2026-07-27T00:00:00Z",
                verified_by="human:reviewer",
                verified_at="2026-07-27T01:00:00Z",
                verification_evidence=("validation:ok",),
                extension_lines=("producer_extension:", '  value: "kept"'),
            )
        ) + "# Requirements\n"
        metadata_only = render_concept(
            "# Requirements\n",
            profile_key="requirements.md",
            existing_text=verified,
            meaningful_change=False,
        )
        self.assertIn("\nverified:\n", metadata_only)
        self.assertIn("producer_extension:", metadata_only)
        changed = render_concept(
            "# Requirements changed\n",
            profile_key="requirements.md",
            existing_text=verified,
            meaningful_change=True,
        )
        self.assertNotIn("\nverified:\n", changed)
        self.assertIn("producer_extension:", changed)

    def test_bundle_indexes_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "feature"
            root.mkdir()
            (root / "requirements.md").write_text(
                render_concept("# Requirements\n", profile_key="requirements.md"),
                encoding="utf-8",
            )
            nested = root / "notes"
            nested.mkdir()
            (nested / "design.md").write_text(
                render_concept("# Design\n", profile_key="design.md"),
                encoding="utf-8",
            )
            write_bundle_indexes(root)
            self.assertEqual(validate_bundle(root), [])
            self.assertIn('okf_version: "0.2"', (root / "index.md").read_text())
            self.assertFalse((nested / "index.md").read_text().startswith("---"))

    def test_conflict_preflight_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "feature"
            root.mkdir()
            good = root / "requirements.md"
            bad = root / "design.md"
            good.write_text("# Requirements\n", encoding="utf-8")
            bad.write_text("---\ntype: \"wrong.type\"\n---\n# Design\n", encoding="utf-8")
            before = {path: path.read_bytes() for path in (good, bad)}
            with self.assertRaisesRegex(ValueError, "conflicts"):
                migrate_bundle(root, apply=True)
            self.assertEqual(before, {path: path.read_bytes() for path in (good, bad)})

    def test_runtime_paths_have_no_legacy_reader_or_writer(self) -> None:
        script_roots = (ROOT / "skills").glob("*/scripts/*.py")
        combined = "\n".join(path.read_text(encoding="utf-8") for path in script_roots)
        self.assertNotIn('workspace / "specs-index.md"', combined)
        self.assertNotIn('root / "project-context.md"', combined)
        self.assertNotIn('"_ai_sdlc/project-context.toon"', combined)
        self.assertNotIn('write_root / "modules.md"', combined)

    def test_durable_writer_families_import_the_shared_contract(self) -> None:
        writers = (
            "ai-sdlc-architecture/scripts/architecture.py",
            "ai-sdlc-change-set/scripts/change_set.py",
            "ai-sdlc-delivery-graph/scripts/delivery_graph.py",
            "ai-sdlc-doctor/scripts/doctor.py",
            "ai-sdlc-host-adapter/scripts/adapter.py",
            "ai-sdlc-package-trust/scripts/package_trust.py",
            "ai-sdlc-project-context/scripts/project_context.py",
            "ai-sdlc-quality-lenses/scripts/quality_lens_report.py",
            "ai-sdlc-workflow/scripts/workflow.py",
        )
        for relative in writers:
            with self.subTest(writer=relative):
                self.assertIn(
                    "ai_sdlc_okf",
                    (ROOT / "skills" / relative).read_text(encoding="utf-8"),
                )


if __name__ == "__main__":
    unittest.main()
