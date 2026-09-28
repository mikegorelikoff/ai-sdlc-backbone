#!/usr/bin/env python3
"""Example demonstration of how downstream AI SDLC skills interact with ai-sdlc-spec-state."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from spec_state_config import CONFIG_FILENAME, load_config
from spec_state import (
    ensure_config_or_wizard,
    fetch_spec_state,
    publish_spec_state,
    refresh_index,
    rotate_spec_state,
    status_spec_state,
)


def run_cross_skill_demo():
    print("=" * 80)
    print("  AI SDLC Cross-Skill Specification State Workflow Demonstration")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        project_dir = root / "payment-service"
        project_dir.mkdir()
        storage_dir = root / "agent-planning-storage"
        storage_dir.mkdir()

        # Step 1: Downstream skill (e.g., ai-sdlc-sdd) starts a task
        print("\n--- PHASE 1: Downstream Skill Starts Feature Work ---")
        print(f"Simulating feature task in repository: {project_dir.name}")
        print("Checking if .sdlc.toon configuration exists...")

        # Deterministic check: missing config automatically triggers Wizard
        config = ensure_config_or_wizard(
            root=project_dir,
            interactive=False,  # Automated wizard mode for scripting/CI
        )
        print(f"Wizard successfully configured: {config.config_path}")
        print(f"  Repository ID: {config.repository.id}")
        print(f"  Storage: {config.storage.repository}:{config.storage.branch}")

        # Step 2: Fetch compact specification context hierarchy
        print("\n--- PHASE 2: Fetching Specification Context Hierarchy ---")
        fetch_result = fetch_spec_state(feature="stripe-checkout", root=project_dir)
        print("Retrieved specification hierarchy:")
        print(f"  Sync state: {fetch_result['sync_state']}")
        print(f"  Index status: {fetch_result['index']['status']}")
        print(f"  Staged context folder: {fetch_result['staged_context']}")

        # Step 3: Refresh structural index if needed
        print("\n--- PHASE 3: Structural Repository Index Generation ---")
        idx_res = refresh_index(force=True, root=project_dir)
        print(f"Structural index generated: {Path(idx_res['path']).name}")

        # Step 4: Downstream SDD finishes implementation artifacts & publishes
        print("\n--- PHASE 4: Publishing Feature Artifacts Before PR ---")
        spec_text = """# Feature: Stripe Checkout

## Requirements
REQ-001: Support 3D Secure 2.0 authentication.
REQ-002: Webhook signature verification for event delivery.
"""
        plan_text = """# Implementation Plan: Stripe Checkout
1. Integrate Stripe SDK
2. Implement checkout session controller
3. Add webhook endpoint with secret verification
"""
        decisions_text = """# Decision Log: Stripe Checkout
| ID | Date | Status | Owner | Decision | Context |
| DEC-001 | 2026-09-28 | accepted | Payments Team | Use Stripe Hosted Checkout | Reduces PCI-DSS scope |
"""

        pub_res = publish_spec_state(
            feature="stripe-checkout",
            artifacts={
                "spec": spec_text,
                "plan": plan_text,
                "decisions": decisions_text,
            },
            ticket_id="PAY-882",
            logical_spec_id="SPEC-PAY-GLOBAL",
            root=project_dir,
        )
        print(f"Published feature: {pub_res['feature']}")
        for kind, p in pub_res["published"].items():
            print(f"  - {kind}: {Path(p).name}")

        # Step 5: Check status and rotation triggers
        print("\n--- PHASE 5: Inspecting Status & Rotation Health ---")
        st_res = status_spec_state(root=project_dir)
        print(f"Incremental feature specs: {st_res['metrics']['specs_since_baseline']} / {st_res['metrics']['spec_threshold']}")
        print(f"Rotation recommended: {st_res['rotation']['baseline_rotation_recommended']}")

        # Step 6: Atomic Baseline & Decision Rotation
        print("\n--- PHASE 6: Executing Atomic Baseline & Decision Rotation ---")
        rot_res = rotate_spec_state(force=True, root=project_dir)
        print(f"Rotation status: {rot_res['status']}")
        print(f"  New Baseline: {Path(rot_res['baseline']).name}")
        print(f"  New Decision Knowledgebase: {Path(rot_res['decision_archive']).name}")
        print(f"  New Index: {Path(rot_res['index']).name}")

        print("\n" + "=" * 80)
        print("  Workflow completed successfully with zero token bloat!")
        print("=" * 80)


if __name__ == "__main__":
    run_cross_skill_demo()
