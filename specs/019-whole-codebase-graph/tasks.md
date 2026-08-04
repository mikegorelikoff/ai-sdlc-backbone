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
  at: "2026-08-03T21:57:38Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "tasks.md"
  path: "specs/019-whole-codebase-graph/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-04"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-006"
    - "DEC-007"
    - "NFR-002"
    - "NFR-005"
    - "NFR-007"
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
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/branch-plan.md"
    - "specs/019-whole-codebase-graph/code-review.md"
    - "specs/019-whole-codebase-graph/decision-log.md"
    - "specs/019-whole-codebase-graph/design.md"
    - "specs/019-whole-codebase-graph/plan.md"
    - "specs/019-whole-codebase-graph/qa.md"
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/security-review.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
    - "specs/019-whole-codebase-graph/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "approved"
    - "implemented"
---

# Tasks

## Implementation
- [x] T001. Add hash-locked offline parser bundle, twelve-language TOON policy, preflight, and install guidance.
Output: parser-lock.toon, language-policy.toon, offline setup/preflight code, and target contract.
Refs: FR-002, NFR-002, NFR-005, NFR-007, AC-002, AC-003, AC-008, TC-001, TC-002, TC-008, TC-023, DEC-006
Depends on: none
- [x] T002. Implement safe corpus classification and explicit file/exclusion accounting.
Output: reconciled file inventory and exclusion facts.
Refs: FR-001, AC-001, TC-003, TC-004, TC-024
Depends on: T001
- [x] T003. Implement policy-driven Tree-sitter extraction for all twelve languages including Kotlin and Swift.
Output: canonical AST symbol, occurrence, import, and provable-call facts.
Refs: FR-002, FR-004, AC-002, AC-003, TC-005, TC-006, TC-007, TC-008
Depends on: T001, T002
- [x] T004. Implement graph schema v2, stable identities, typed relations, trace hubs, bounds, and atomic v1 migration.
Output: verified bounded heterogeneous graph projection.
Refs: FR-003, FR-004, FR-005, AC-004, AC-005, AC-006, TC-009, TC-010, TC-011, TC-012
Depends on: T003
- [x] T005. Implement affected-file incremental refresh, invalidation, source recheck, stats, and verification.
Output: fresh deterministic lifecycle and TOON diagnostics.
Refs: FR-006, FR-008, AC-004, AC-006, TC-013, TC-014, TC-020
Depends on: T004
- [x] T006. Implement symbol-aware seed ranking, bounded typed traversal, qualified disambiguation, and pack acceptance.
Output: deterministic economical graph retrieval with direct-read fallback.
Refs: FR-007, FR-008, AC-007, AC-008, TC-015, TC-016, TC-017, TC-018, TC-019
Depends on: T005

## Testing
- [x] T007. Add twelve-language, graph lifecycle, retrieval, fallback, and unsafe-input fixtures and automated cases TC-001 through TC-024.
Output: focused deterministic test suites and TOON fixture manifests.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-023, TC-024
Depends on: T001, T002, T003, T004, T005, T006
- [x] T008. Implement and execute two-run real-corpus release audit plus fault injection.
Output: deterministic audit evidence with production_ready gate and token economics.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, TC-021, TC-022, DEC-007
Depends on: T007
- [x] T009. Run full validation, security testing, code review, compatibility, docs, install, and diff gates.
Output: validation.md, security-review.md, code-review.md, and zero unresolved release blockers.
Refs: AC-008, TC-021, TC-022, TC-023, TC-024, DEC-007
Depends on: T008

## Documentation
- [x] T010. Document graph setup, supported targets/languages, Kotlin/Swift parity, commands, schema, bounds, diagnostics, fallback, purge, privacy, offline operation, and production criteria; refresh generated catalogs.
Output: current skill contract, operator guide, parser provenance guidance, and generated references.
Refs: FR-001, FR-002, FR-005, FR-006, FR-007, FR-008, AC-001, AC-003, AC-005, AC-007, AC-008, TC-001, TC-019, TC-020, TC-023, TC-024, DEC-006, DEC-007
Depends on: T001, T005, T006, T007
- [x] T011. Provision and verify the complete pinned graph runtime before protected Python 3.10 and 3.13 CI tests.
Output: target-specific Linux TOON locks and offline installer/preflight gates.
Refs: AC-008, TC-001, TC-023, DEC-008
Depends on: T001, T007, T009
- [x] T012. Prove both protected Linux CI targets and prepare the immutable corrective release.
Output: green Python 3.10 and 3.13 jobs, completed validation evidence, and v4.2.2 release metadata.
Refs: AC-008, TC-001, TC-023, DEC-008
Depends on: T011
