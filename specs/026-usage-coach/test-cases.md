---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-28T10:00:00Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "026-usage-coach"
  artifact: "test-cases.md"
  path: "specs/026-usage-coach/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/026-usage-coach/_ai_sdlc/state.toon"
  decision_log: "specs/026-usage-coach/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-09-28"
  updated_at: "2026-09-28"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
  related_artifacts:
    - "specs/026-usage-coach/decision-log.md"
    - "specs/026-usage-coach/design.md"
    - "specs/026-usage-coach/index.md"
    - "specs/026-usage-coach/plan.md"
    - "specs/026-usage-coach/qa.md"
    - "specs/026-usage-coach/requirements.md"
    - "specs/026-usage-coach/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
---

# Test Cases

## Scope
Verification of local session usage journaling, data minimization and secret redaction, fail-safe error recovery, on-demand analytics derivation, interactive coach CLI, evidence-backed advice rendering, and full Loop regression compatibility across 28 skills.

## Scenario Matrix
TC-001: AC-001; Append-only TOON session journal creation and monotonic sequence keying.
TC-002: AC-002; Data minimization and secret redaction during event capture.
TC-003: AC-003; Fail-open resilience when journal directory is read-only or corrupted.
TC-004: AC-004; Complete event taxonomy recording across skill lifecycle, user decisions, artifacts, quality gates, and transitions.
TC-005: AC-005; Skill coverage and discoverability analysis across multiple sessions (Scenario A & E).
TC-006: AC-005; Evidence lag and late gating detection (Scenario B).
TC-007: AC-005; Recurring rework cycle and loop detection (Scenario C).
TC-008: AC-005; Ignored recommendation tracking and fatigue prevention (Scenario D).
TC-009: AC-005; Missing capability and recurring friction signal detection (Scenario F).
TC-010: AC-006; Coach CLI report command with session and date window filtering.
TC-011: AC-006; Coach CLI analyze and suggest commands for active session context.
TC-012: AC-006; Coach CLI feedback and explain commands.
TC-013: AC-007; Structured evidence-backed advice rendering and schema compliance.
TC-014: AC-007; Timing policy verification (silent in rapid flow, speaks on repeated friction / milestone / request).
TC-015: AC-008; Gate preservation (coach cannot approve, bypass quality gate, or commit).
TC-016: AC-008; Loop full regression suite and doctor verification with 28 registered skills.

## Layer Mapping
- Unit tests: `usage_journal.py` serialization, sanitization, monotonic keys, scanning; `coach.py` analytics, motifs, suggestion logic.
- Integration tests: Loop runtime hook emissions in `test_usage_coach.py` simulating Scenarios A-F.
- CLI tests: Invocation of `coach.py` subcommands with arguments and stdout validation.
- System tests: `doctor.py`, `install.py`, and Windows launcher/smoke validation with 28 skills.

## Automation Plan
- Execute Python unittest suites: `python3 -m unittest discover -s skills/ai-sdlc-loop-usage-coach/tests -v` and `python3 -m unittest discover -s tests -v` in `products/ai-sdlc-loop`.
- Validate doc catalogs: `python3 docs/scripts/build_catalog.py --check`.

## Open Gaps
None. All scenarios are verified using local deterministic test fixtures without mock external services.
