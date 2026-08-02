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
  at: "2026-08-02T21:13:56Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "test-cases.md"
  path: "specs/016-production-harness-completion/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
  status: "approved"
  owner: "QA and Harness Maintainers"
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
    - "AC-009"
    - "AC-010"
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
    - "specs/016-production-harness-completion/decision-log.md"
    - "specs/016-production-harness-completion/design.md"
    - "specs/016-production-harness-completion/index.md"
    - "specs/016-production-harness-completion/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
    - "production-harness"
---

# Test Cases

## Scope
- Cover scheduler safety and determinism, executable adapter enforcement, provider evidence authenticity states, per-step context freshness, install profile reproducibility, and repository-wide TOON conformance.

## Scenario Matrix
| ID | Requirement | Scenario | Verifiable outcome |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Concurrent workers claim one ready task | Exactly one live lease is issued and all projections use stable ready ordering. |
| TC-002 | AC-002 | Worker stops after effect receipt and lease expires | Recovery reuses the receipt or resumes the missing phase without a second effect. |
| TC-003 | AC-003 | Driver request contains an undeclared capability or changed idempotency payload | Execution fails before the operation and no success receipt is committed. |
| TC-004 | AC-004 | Replay identical journal twice | Canonical TOON projections are byte-identical. |
| TC-005 | AC-005 | Context source changes after compilation | Claim or dispatch rejects the stale fingerprint before durable work starts. |
| TC-006 | AC-006 | Authorized provider executes the pinned live scenarios | Receipt records complete execution identity, evidence, scores, thresholds, and verdict. |
| TC-007 | AC-007 | Offline protocol validation requests certification | Result remains pending and cannot be promoted to provider-passed. |
| TC-008 | AC-008 | Install each profile twice from the same revision | Records and per-skill digests match byte-for-byte and discovery verification succeeds. |
| TC-009 | AC-009 | Scan tracked source, generated docs, and owned machine artifacts | Only canonical TOON machine representation is present and every TOON artifact decodes. |
| TC-010 | AC-010 | Run complete delivery validation | Focused, integration, security, docs, compatibility, and install gates all pass. |

## Layer Mapping
- Unit: scheduler transitions, leases, driver validation, receipt validation, profile resolution.
- Service: scheduler journal store, effect registry, evaluator modes, installer profile engine.
- Integration: concurrent workers, crash points, exact-once effect boundary, runtime dispatch, fresh installs.
- Release: authorized provider TC-006 and full repository validation.

## Automation Plan
- Inject deterministic clocks, worker IDs, and failure points for exhaustive scheduler transitions.
- Use subprocess workers against disposable repositories for contention and crash recovery.
- Use bounded fake drivers to count effects and verify idempotency.
- Validate provider receipts with signed-in host metadata supplied at runtime; keep offline fixtures explicitly non-certified.
- Execute clean profile installs in isolated temporary consumer repositories and compare canonical bytes.

## Open Gaps
- Genuine TC-006 execution depends on an authorized provider session. Repository work must complete the runner and verifier first; certification remains pending until real execution evidence exists.
- Additional host profiles remain unadvertised until their exact discovery and clean-install contracts can be verified.
