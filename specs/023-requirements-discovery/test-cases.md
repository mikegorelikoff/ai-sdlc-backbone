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
  at: "2026-09-07T18:49:57Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "023-requirements-discovery"
  artifact: "test-cases.md"
  path: "specs/023-requirements-discovery/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/023-requirements-discovery/_ai_sdlc/state.toon"
  decision_log: "specs/023-requirements-discovery/decision-log.md"
  status: "review"
  owner: "implementation agent"
  created_at: "2026-09-07"
  updated_at: "2026-09-07"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
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
  related_artifacts:
    - "specs/023-requirements-discovery/decision-log.md"
    - "specs/023-requirements-discovery/design.md"
    - "specs/023-requirements-discovery/index.md"
    - "specs/023-requirements-discovery/plan.md"
    - "specs/023-requirements-discovery/qa.md"
    - "specs/023-requirements-discovery/requirements.md"
    - "specs/023-requirements-discovery/tasks.md"
    - "specs/023-requirements-discovery/validation.md"
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
Discovery instructions, deterministic source preparation and report validation, safe artifact writes, package portability and documentation; existing product tests cover installer and graph regression.

## Scenario Matrix
| ID | Scenario | Expected result | Refs |
| --- | --- | --- | --- |
| TC-001 | Source graph selection | Dependency-ready v2 steps | AC-001 |
| TC-002 | Raw request and prior pilot | Source-linked options and targeted questions | AC-002 |
| TC-003 | Missing history and owner replies | Hypotheses and unresolved decision; no approval | AC-003 |
| TC-004 | Product catalogs and docs | Source-backed discovery and valid pages | AC-005 |
| TC-005 | Repeat sources, reorder arguments/records, relocate project | Byte-identical context, scaffold and finalized output | AC-006 |
| TC-006 | Wrong schema/type, duplicate/dangling IDs, uncovered gaps/options, missing decision evidence | Nonzero failure and no output write | AC-007 |
| TC-007 | Source digest or finalized report changes | Read-only verify fails | AC-008 |
| TC-008 | Traversal, symlink, collision, simulated output failure and repeat write | Containment, explicit replace, idempotence and rollback | AC-009 |
| TC-009 | Installed helper in each product and profile | No source-checkout or cross-product dependency | AC-004 |
| TC-010 | Multiline Unicode and all semantic fields | Full canonical TOON and escaped readable Harness Markdown | AC-002, AC-006 |

## Layer Mapping
Pure schema/reference validation; CLI subprocess tests; filesystem mutation/rollback tests; installed package checks; static business scenario walkthrough and docs gates.

## Automation Plan
Run positive and negative helper tests in isolated temporary projects for both products; test identical input permutations and source drift. Extend installed selection tests to invoke the shipped helper and use the existing docs suite.

## Open Gaps
Deterministic tests do not prove model reasoning quality, stakeholder authenticity or real business outcomes.
