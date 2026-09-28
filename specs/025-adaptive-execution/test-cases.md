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
  at: "2026-09-15T13:25:36Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "025-adaptive-execution"
  artifact: "test-cases.md"
  path: "specs/025-adaptive-execution/test-cases.md"
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
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
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
  related_artifacts:
    - "specs/025-adaptive-execution/decision-log.md"
    - "specs/025-adaptive-execution/design.md"
    - "specs/025-adaptive-execution/index.md"
    - "specs/025-adaptive-execution/plan.md"
    - "specs/025-adaptive-execution/qa.md"
    - "specs/025-adaptive-execution/requirements.md"
    - "specs/025-adaptive-execution/tasks.md"
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
Adaptive policy and integration across both products.

## Scenario Matrix
TC-001: AC-001; tiny bug FAST
TC-002: AC-001; documentation FAST
TC-003: AC-002; localized feature STANDARD
TC-004: AC-002; multi-module feature STANDARD or DEEP
TC-005: AC-003; architecture DEEP
TC-006: AC-003; security DEEP
TC-007: AC-004; FAST complexity escalation
TC-008: AC-004; STANDARD architecture escalation
TC-009: AC-005; context reuse and refresh
TC-010: AC-005; irrelevant skills omitted
TC-011: AC-006; deterministic check preference
TC-012: AC-006; bounded failed verification
TC-013: AC-007; success terminates
TC-014: AC-007; legacy full workflow retained

## Layer Mapping
Unit policy and context tests; subprocess CLI integration; existing gate tests; deterministic benchmark.

## Automation Plan
Run new policy tests in both distributions and existing shared runtime and Loop tests. Check install packaging and docs catalogs.

## Open Gaps
Live model latency and actual host token use require external host instrumentation; mark unavailable rather than zero.

