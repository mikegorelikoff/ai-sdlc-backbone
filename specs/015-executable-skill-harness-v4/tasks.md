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
  at: "2026-07-30T09:37:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "tasks.md"
  path: "specs/015-executable-skill-harness-v4/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "validated"
  owner: "Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
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
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
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
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/branch-plan.md"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/design.md"
    - "specs/015-executable-skill-harness-v4/index.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/qa.md"
    - "specs/015-executable-skill-harness-v4/requirements.md"
    - "specs/015-executable-skill-harness-v4/research.md"
    - "specs/015-executable-skill-harness-v4/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "validated"
    - "harness-v4"
---

# Tasks

## Implementation
- [x] T001. Add v4 TOON contracts, the shared canonical codec, and graph model with hard-cut schema diagnostics.
  Refs: FR-001, FR-009, FR-011, AC-001, AC-010, AC-013, DEC-002, DEC-007
  Output: v2 skill graph plus StepCard, workflow, run, flow, context, adapter, handoff, eval, and complete test-suite contracts
- [x] T002. Upgrade the selector to validate DAG semantics, resolve ready steps, emit StepCards, and compile context-complete run plans.
  Refs: FR-001, FR-004, AC-001, AC-003, AC-005, DEC-002
  Depends on: T001
  Output: `ai_sdlc_steps.py` v4 selector and compiler
- [x] T003. Implement per-step deterministic context compilation and sufficiency gates.
  Refs: FR-003, NFR-003, NFR-004, AC-003, AC-004, DEC-004
  Depends on: T001
  Output: context pack v4 compiler and deterministic safety/economics tests
- [x] T004. Upgrade runtime to run v2 with per-step TOON journals, strict protocol order, evidence, retries, idempotency, replay, and context-pack validation.
  Refs: FR-005, NFR-002, AC-005, AC-006, DEC-003
  Depends on: T002
  Output: durable runtime v2 implementation and hard-cut schema diagnostics
- [x] T005. Integrate full StepCards across flow, workflow, host adapter, and handoff while preserving Explore zero-write.
  Refs: FR-006, FR-007, AC-007, AC-008, AC-009, DEC-006
  Depends on: T002, T003, T004
  Output: flow v3, workflow v2, adapter v2, and handoff v2 integration

## Testing
- [x] T006. Build deterministic semantic scaffolding, router generation, drift checks, and convert all 44 skill graphs.
  Refs: FR-001, FR-002, FR-009, AC-001, AC-002, AC-010
  Depends on: T001, T002, T003
  Output: generator tooling plus 44 v2 manifests and generated routers, with no legacy conversion mode
- [x] T007. Add codec, schema, selector, context, flow, runtime, adapter, security, installed-layout, and TOON-only repository tests.
  Refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-013, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-013
  Depends on: T003, T004, T005, T006
  Output: focused positive, blocked, invalid, replay, drift, zero-write, malformed-input, context-safety, and repository-absence suites
- [x] T008. Add all-skill deterministic eval receipts, complete per-file test execution, and provider-neutral live protocol validation.
  Refs: FR-008, AC-011, AC-012, TC-011, TC-012, DEC-005
  Depends on: T006, T007
  Output: `ai_sdlc_skill_eval.py`, `ai_sdlc_test_suite.py`, deterministic scenario matrix, live protocol, and receipt contracts

## Documentation
- [x] T009. Update compatibility baseline, registries, context-engineering concepts, maintainer guidance, public references, decisions, and changelog for the TOON-only v4 hard cut.
  Refs: FR-010, FR-011, AC-002, AC-010, AC-011, AC-012, AC-013, DEC-007
  Depends on: T006, T008
  Output: synchronized v4 documentation and generated catalogs
- [x] T010. Execute SDD, all-skill, compatibility, package, security, TOON canonicality, documentation-build, and diff validation; record deterministic receipts and the remaining live release gate.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013
  Depends on: T007, T008, T009
  Output: current validation report, 95-file test-suite evidence, and auditable deterministic TOON receipts
- [x] T011. Replace the incompatible external consumer path with a deterministic native installer, portable TOON record and lock, installed digest validation, native smoke, and immutable v4.0.1 correction.
  Refs: NFR-007, NFR-008, AC-010, AC-013, DEC-009
  Depends on: T007, T009, T010
  Output: native installer, install record v2, install lock v1, corrective documentation, and fresh tagged-install gate
