---
type: "ai-sdlc.implementation-plan"
title: "Implementation Plan"
description: "Ordered implementation and validation plan."
tags:
  - "ai-sdlc"
  - "sdd"
  - "planning"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-02T21:57:49Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "plan.md"
  path: "specs/016-production-harness-completion/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "plan"
    - "draft"
---

# plan.md

## Upstream Refinement Sources
- Refinement index: `specs-refiniment/_ai_sdlc/specs-index.toon`
- Refinement state: `specs-refiniment/<feature-name>/_ai_sdlc/state.toon`
- Delivery spec: `specs-refiniment/<feature-name>/delivery-spec.md`
- QA readiness: `specs-refiniment/<feature-name>/qa-readiness.md`
- Decision trace: `decision-log.md`

## SDD Artifact Links
- Requirements: `requirements.md`
- Design: `design.md`
- Test cases: `test-cases.md`
- QA: `qa.md`
- Tasks: `tasks.md`
- Machine plan: `_ai_sdlc/plan.toon`
- Decision log: `decision-log.md`

## Cross-Artifact Trace Map
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T002, T005, T008) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T001, T002, T004, T005, T008) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T003, T004, T005, T008) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T001, T002, T005, T008) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005) -> tasks.md (T001, T003, T005, T008) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006) -> tasks.md (T006, T008, T009) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-007) -> tasks.md (T006, T008, T009) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-008) -> tasks.md (T007, T008, T009) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-009) -> tasks.md (T008, T009) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-010) -> tasks.md (T008, T009) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Implement the deterministic scheduler state, journal, lease, recovery, and replay contracts.; refs: FR-001, FR-002, FR-006, AC-001, AC-002, AC-004, AC-005, TC-001, TC-002, TC-004, TC-005, DEC-001; output: New scheduler skill with canonical schemas, CLI, state store, and injected clock.
- [x] T002: Integrate runtime dispatch with scheduler leases and compare-and-commit terminal outcomes.; refs: FR-001, FR-002, AC-001, AC-002, AC-004, TC-001, TC-002, TC-004; output: Worker protocol integration preserving existing StepCard and runtime fingerprints.
- [x] T003: Implement executable effect-driver request, registry, policy, and receipt boundary.; refs: FR-003, AC-003, AC-005, TC-003, TC-005, DEC-001; output: Versioned adapter driver contracts and bounded reference drivers without a generic shell executor.
- [x] T004: Bind runtime recovery to durable effect receipts and stale-worker rejection.; refs: FR-002, FR-003, AC-002, AC-003, TC-002, TC-003; output: Exact-once effect integration across lease expiry, retry, replay, and interrupted completion.
- [x] T005: Add scheduler model, contention, crash-point, adapter abuse, and replay suites.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, TC-001, TC-002, TC-003, TC-004, TC-005; output: Deterministic unit and integration coverage for TC-001 through TC-005.
- [x] T006: Implement provider-execution runner and strict receipt verifier, then execute TC-006 in an authorized provider host.; refs: FR-004, AC-006, AC-007, TC-006, TC-007, DEC-001; output: Provider-neutral runner, negative offline cases, and a genuine release-owned provider receipt.
- [x] T007: Add explicit native install profiles and two-clean-install smoke for every advertised host family.; refs: FR-005, AC-008, TC-008, DEC-001; output: Profile registry, safe destination resolution, discovery verification, deterministic records, and clean-install evidence.
- [x] T008: Run complete security, conformance, regression, documentation, and compatibility validation.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010; output: Current validation receipts covering all acceptance criteria and test cases.
- [x] T009: Publish operator, adapter-author, provider-evaluation, install-profile, migration, and release documentation.; refs: AC-006, AC-007, AC-008, AC-009, AC-010, TC-006, TC-007, TC-008, TC-009, TC-010; output: Updated canonical guides, references, changelog, catalogs, and release readiness notes.

## Task Dependencies
- T001: depends on none
- T002: depends on T001
- T003: depends on T001
- T004: depends on T002, T003
- T005: depends on T001, T002, T003, T004
- T006: depends on T002, T003
- T007: depends on T003
- T008: depends on T005, T006, T007
- T009: depends on T005, T006, T007, T008

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-08-03

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
