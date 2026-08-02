---
type: "ai-sdlc.tasks"
title: "Implementation Tasks"
description: "Traceable implementation task breakdown and status."
tags:
  - "ai-sdlc"
  - "sdd"
  - "tasks"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-02T21:57:49Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "tasks.md"
  path: "specs/016-production-harness-completion/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
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
    - "AC-009"
    - "AC-010"
    - "DEC-001"
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
    - "specs/016-production-harness-completion/plan.md"
    - "specs/016-production-harness-completion/qa.md"
    - "specs/016-production-harness-completion/requirements.md"
    - "specs/016-production-harness-completion/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "approved"
    - "production-harness"
---

# Tasks

## Implementation
- [x] T001. Implement the deterministic scheduler state, journal, lease, recovery, and replay contracts.
Output: New scheduler skill with canonical schemas, CLI, state store, and injected clock.
Refs: FR-001, FR-002, FR-006, AC-001, AC-002, AC-004, AC-005, TC-001, TC-002, TC-004, TC-005, DEC-001
Depends on: none
- [x] T002. Integrate runtime dispatch with scheduler leases and compare-and-commit terminal outcomes.
Output: Worker protocol integration preserving existing StepCard and runtime fingerprints.
Refs: FR-001, FR-002, AC-001, AC-002, AC-004, TC-001, TC-002, TC-004
Depends on: T001
- [x] T003. Implement executable effect-driver request, registry, policy, and receipt boundary.
Output: Versioned adapter driver contracts and bounded reference drivers without a generic shell executor.
Refs: FR-003, AC-003, AC-005, TC-003, TC-005, DEC-001
Depends on: T001
- [x] T004. Bind runtime recovery to durable effect receipts and stale-worker rejection.
Output: Exact-once effect integration across lease expiry, retry, replay, and interrupted completion.
Refs: FR-002, FR-003, AC-002, AC-003, TC-002, TC-003
Depends on: T002, T003

## Testing
- [x] T005. Add scheduler model, contention, crash-point, adapter abuse, and replay suites.
Output: Deterministic unit and integration coverage for TC-001 through TC-005.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, TC-001, TC-002, TC-003, TC-004, TC-005
Depends on: T001, T002, T003, T004
- [x] T006. Implement provider-execution runner and strict receipt verifier, then execute TC-006 in an authorized provider host.
Output: Provider-neutral runner, negative offline cases, and a genuine release-owned provider receipt.
Refs: FR-004, AC-006, AC-007, TC-006, TC-007, DEC-001
Depends on: T002, T003
- [x] T007. Add explicit native install profiles and two-clean-install smoke for every advertised host family.
Output: Profile registry, safe destination resolution, discovery verification, deterministic records, and clean-install evidence.
Refs: FR-005, AC-008, TC-008, DEC-001
Depends on: T003
- [x] T008. Run complete security, conformance, regression, documentation, and compatibility validation.
Output: Current validation receipts covering all acceptance criteria and test cases.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010
Depends on: T005, T006, T007

## Documentation
- [x] T009. Publish operator, adapter-author, provider-evaluation, install-profile, migration, and release documentation.
Output: Updated canonical guides, references, changelog, catalogs, and release readiness notes.
Refs: AC-006, AC-007, AC-008, AC-009, AC-010, TC-006, TC-007, TC-008, TC-009, TC-010
Depends on: T005, T006, T007, T008
