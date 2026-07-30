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
  at: "2026-07-30T09:39:17Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "plan.md"
  path: "specs/015-executable-skill-harness-v4/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T002, T006, T007, T010) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T006, T007, T009, T010) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T002, T003, T007, T010) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T003, T007, T010) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005) -> tasks.md (T002, T004, T007, T010) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006) -> tasks.md (T004, T007, T010) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-007) -> tasks.md (T005, T007, T010) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-008) -> tasks.md (T005, T007, T010) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-009) -> tasks.md (T005, T007, T010) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-010) -> tasks.md (T001, T006, T007, T009, T010) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-011) -> tasks.md (T008, T009, T010) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-012) -> tasks.md (T008, T009, T010) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-013) -> tasks.md (T001, T007, T009, T010) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Add v4 TOON contracts, the shared canonical codec, and graph model with hard-cut schema diagnostics.; refs: FR-001, FR-009, FR-011, AC-001, AC-010, AC-013, DEC-002, DEC-007; output: v2 skill graph plus StepCard, workflow, run, flow, context, adapter, handoff, eval, and complete test-suite contracts
- [x] T002: Upgrade the selector to validate DAG semantics, resolve ready steps, emit StepCards, and compile context-complete run plans.; refs: FR-001, FR-004, AC-001, AC-003, AC-005, DEC-002; output: `ai_sdlc_steps.py` v4 selector and compiler
- [x] T003: Implement per-step deterministic context compilation and sufficiency gates.; refs: FR-003, NFR-003, NFR-004, AC-003, AC-004, DEC-004; output: context pack v4 compiler and deterministic safety/economics tests
- [x] T004: Upgrade runtime to run v2 with per-step TOON journals, strict protocol order, evidence, retries, idempotency, replay, and context-pack validation.; refs: FR-005, NFR-002, AC-005, AC-006, DEC-003; output: durable runtime v2 implementation and hard-cut schema diagnostics
- [x] T005: Integrate full StepCards across flow, workflow, host adapter, and handoff while preserving Explore zero-write.; refs: FR-006, FR-007, AC-007, AC-008, AC-009, DEC-006; output: flow v3, workflow v2, adapter v2, and handoff v2 integration
- [x] T006: Build deterministic semantic scaffolding, router generation, drift checks, and convert all 44 skill graphs.; refs: FR-001, FR-002, FR-009, AC-001, AC-002, AC-010; output: generator tooling plus 44 v2 manifests and generated routers, with no legacy conversion mode
- [x] T007: Add codec, schema, selector, context, flow, runtime, adapter, security, installed-layout, and TOON-only repository tests.; refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-013, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-013; output: focused positive, blocked, invalid, replay, drift, zero-write, malformed-input, context-safety, and repository-absence suites
- [x] T008: Add all-skill deterministic eval receipts, complete per-file test execution, and provider-neutral live protocol validation.; refs: FR-008, AC-011, AC-012, TC-011, TC-012, DEC-005; output: `ai_sdlc_skill_eval.py`, `ai_sdlc_test_suite.py`, deterministic scenario matrix, live protocol, and receipt contracts
- [x] T009: Update compatibility baseline, registries, context-engineering concepts, maintainer guidance, public references, decisions, and changelog for the TOON-only v4 hard cut.; refs: FR-010, FR-011, AC-002, AC-010, AC-011, AC-012, AC-013, DEC-007; output: synchronized v4 documentation and generated catalogs
- [x] T010: Execute SDD, all-skill, compatibility, package, security, TOON canonicality, documentation-build, and diff validation; record deterministic receipts and the remaining live release gate.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013; output: current validation report, 94-file test-suite evidence, and auditable deterministic TOON receipts

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T001
- T004: depends on T002
- T005: depends on T002, T003, T004
- T006: depends on T001, T002, T003
- T007: depends on T003, T004, T005, T006
- T008: depends on T006, T007
- T009: depends on T006, T008
- T010: depends on T007, T008, T009

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-30

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
