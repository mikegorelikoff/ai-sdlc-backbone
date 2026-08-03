---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:36:47Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "test-cases.md"
  path: "specs/018-context-cache-runtime/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
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
  related_artifacts:
    - "specs/018-context-cache-runtime/branch-plan.md"
    - "specs/018-context-cache-runtime/decision-log.md"
    - "specs/018-context-cache-runtime/design.md"
    - "specs/018-context-cache-runtime/index.md"
    - "specs/018-context-cache-runtime/plan.md"
    - "specs/018-context-cache-runtime/qa.md"
    - "specs/018-context-cache-runtime/requirements.md"
    - "specs/018-context-cache-runtime/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
---

# Test Cases

## Scope
TC-001 through TC-012 cover activation, concurrency, drift, policy, pack acceptance, observations, fault fallback, determinism, confinement, installed integration, corrupt recovery, and operational totals. Deferred remote retrieval and deterministic latency thresholds are excluded.

## Scenario Matrix
| ID | Requirement | Scenario | Verifiable outcome |
| --- | --- | --- | --- |
| TC-001 | AC-001 | compile same step with module absent and source checkout only | direct paths equal baseline and no cache state is created |
| TC-002 | AC-002 | run synchronized warmers on stale state | all terminate with one fresh logical fingerprint and no partial state |
| TC-003 | AC-002, AC-008 | mutate a source while candidate builds | stale candidate is rejected; retry is bounded; outcome is fresh or direct |
| TC-004 | AC-003 | resolve exact, malformed, and over-budget policies | valid exact values apply within manifest; invalid values recover safely |
| TC-005 | AC-004 | validate good and owner, anchor, hash, authority, budget, savings failures | only the complete fresh economical v4 pack is accepted |
| TC-006 | AC-005 | record sentinel-bearing operations then inspect and reset | sentinel is absent, fields are allowlisted, and reset empties rows |
| TC-007 | AC-006 | inject timeout, corruption, contention, FTS5 absence, and validation faults | stable reason-coded direct paths return |
| TC-008 | AC-007 | run identical fixture repeatedly | receipts and fingerprints are byte-identical with timing excluded |
| TC-009 | AC-008 | exercise excluded path, symlink, and offline guard | reads and writes stay confined and network count remains zero |
| TC-010 | AC-001, AC-004 | install optional module and compile ordinary StepCard | validated packed context is selected only after every gate passes |
| TC-011 | AC-002, AC-006 | corrupt accepted or control state then warm | safe rebuild or direct fallback occurs without source mutation |
| TC-012 | AC-005, AC-007 | produce known operation outcomes and reset | aggregate counts and token arithmetic exactly match expected values |

## Layer Mapping
Unit: policy, validation, schema, token math, reasons. Component: cache warm, verify, observations, recovery, confinement. Integration: installed/absent StepCard and bounded process. Multi-process: convergence and atomicity. Release: regression, docs/install, security, code review, and UAT. Each failed layer blocks dependents.

## Automation Plan
Implement cases in skills/ai-sdlc-context-cache/tests/test_context_cache.py and skills/ai-sdlc-shared-runtime/tests/test_steps.py with deterministic temporary fixtures and bounded processes. Run focused files first, then full shared runtime and docs. Map tests to AC/TC references through artifact traceability and descriptive names.

## Open Gaps
No blocked or manual-only P0 case exists. Owner: QA Maintainers. Impact: test execution can begin without inventing expected behavior, while release approval remains pending. Resolution and next step: execute current focused/full validation plus independent security and code review receipts. Cross-runtime latency distribution and future patched-runtime WAL behavior are informational or separate-scope work owned by future roadmap decisions.
