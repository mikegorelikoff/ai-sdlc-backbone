---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-15T13:25:37Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "025-adaptive-execution"
  artifact: "qa.md"
  path: "specs/025-adaptive-execution/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/025-adaptive-execution/_ai_sdlc/state.toon"
  decision_log: "specs/025-adaptive-execution/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-09-15"
  updated_at: "2026-09-15"
  trace_ids:
    - "TC-001"
    - "TC-014"
  related_artifacts:
    - "specs/025-adaptive-execution/decision-log.md"
    - "specs/025-adaptive-execution/design.md"
    - "specs/025-adaptive-execution/index.md"
    - "specs/025-adaptive-execution/plan.md"
    - "specs/025-adaptive-execution/requirements.md"
    - "specs/025-adaptive-execution/tasks.md"
    - "specs/025-adaptive-execution/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
---

# QA

## Change Summary
Adaptive depth with conservative escalation, shared context, bounded verification and telemetry.

## Acceptance Scenarios
Execute TC-001 through TC-014 and negative freshness/authorization tests.

## Regression Targets
Loop spec/approval/quality/verification/promotion; Harness flow fingerprints and step manifests; installation and generated catalogs.

## Risk Notes
Never accept a mode or telemetry record as approval or proof of semantic correctness.

## Validation Commands
Executed checks:

- Shared runtime regression discovery in a temporary Python 3.11 environment with repository hash-locked parsers: 206 tests; one canonical-text contract failure in the new execution-map wording, corrected and rerun through test_skill_eval.py. All other tests passed, including nested per-skill suites.
- Final adaptive policy suite: 13 tests passed, including newly added automatic risk discovery and minimum-depth checks.
- Loop regression discovery: 84 tests passed. After final follow-up changes, targeted adaptive and flow tests rerun.
- Harness flow tests: 31 passed; semantic step tests: 19 passed.
- Documentation suite: 47 passed after updating exact script inventory counts for the added helpers/test.
- Both product catalog/source checks and strict MkDocs builds/rendered-link validation passed.
- Emulated project, selective and disposable-global installation smoke matrices passed.
- Python compilation, Loop shell syntax, compatibility check and both git diff --check gates passed.

Use Python 3.10+ for the supported runtime. The macOS system Python 3.9 installer failure was an environment mismatch. Python 3.11 needed the existing locked graph-parser packages; installed into a disposable /tmp environment, without changing repository dependency contracts.

## Manual Checks
Inspect execution map, representative benchmark output and final diff for retained gates.

## Signoff
Engineering validation complete after focused regression repairs. Measured routing/read and concurrency improvements are recorded in design.md and raw benchmark TOON. No live model run was measured; host-level token/call savings and 2–5 minute delivery targets remain unverified. Existing protected gates and separate commit authority remain enforced.

