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
  at: "2026-09-28T10:00:00Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "026-usage-coach"
  artifact: "qa.md"
  path: "specs/026-usage-coach/qa.md"
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
    - "TC-001"
    - "TC-016"
  related_artifacts:
    - "specs/026-usage-coach/decision-log.md"
    - "specs/026-usage-coach/design.md"
    - "specs/026-usage-coach/index.md"
    - "specs/026-usage-coach/plan.md"
    - "specs/026-usage-coach/requirements.md"
    - "specs/026-usage-coach/tasks.md"
    - "specs/026-usage-coach/test-cases.md"
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
Implementation of local repository-native usage journaling, fail-safe event recording, on-demand behavioral metrics derivation, and the `ai-sdlc-loop-usage-coach` skill.

## Acceptance Scenarios
Execute TC-001 through TC-016 covering:
- Append-only journal writing and monotonic sequence keying
- Data minimization and secret token redaction
- Fail-open exception handling during logging
- Full event taxonomy emission
- Scenario A (canonical flow), Scenario B (evidence lag), Scenario C (rework cycles), Scenario D (ignored recommendations), Scenario E (handoff discoverability), Scenario F (capability gap)
- Coach CLI subcommands: report, analyze, suggest, feedback, explain
- Respectful timing and non-intrusive behavior

## Regression Targets
- AI SDLC Loop core skill execution (`loop.py`, `engineering_quality_gate.py`, `flow.py`)
- Skill inventory count verification (28 skills) across installer, doctor, smoke test, and docs
- Catalog and strict documentation build checks

## Risk Notes
- Journal logging must NEVER fail a build or user action; fail-open semantics are mandatory.
- Recommendations are strictly advisory; coaching advice must never grant approvals or bypass quality gates.
- No network connections or external telemetry endpoints.

## Validation Commands
```bash
# Spec validation
python3 skills/ai-sdlc-sdd/scripts/check_clarify.py specs/026-usage-coach
python3 skills/ai-sdlc-sdd/scripts/check_checklist.py specs/026-usage-coach
python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/026-usage-coach
python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/026-usage-coach

# Loop test suites
python3 -m unittest discover -s products/ai-sdlc-loop/tests -v
python3 -m unittest discover -s products/ai-sdlc-loop/skills/ai-sdlc-loop-usage-coach/tests -v

# Doctor and install checks
python3 products/ai-sdlc-loop/skills/ai-sdlc-loop-doctor/scripts/doctor.py --check-skills
python3 products/ai-sdlc-loop/packaging/windows/smoke.py

# Documentation catalogs
python3 docs/scripts/build_catalog.py --check
```

## Manual Checks
- Verify session TOON files in `.ai-sdlc-loop/usage/sessions/` conform to the strict append-only format.
- Confirm coach CLI outputs well-formatted structured Markdown with exact citations.
- Confirm no raw prompt text or passwords appear in any session file.

## Signoff
Implementation and verification completed with zero telemetry, zero mutable global databases, full fail-open safety, and all tests passing across 28 registered Loop skills.
