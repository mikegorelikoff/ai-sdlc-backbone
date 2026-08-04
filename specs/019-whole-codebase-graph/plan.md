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
  at: "2026-08-04T09:35:19Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "plan.md"
  path: "specs/019-whole-codebase-graph/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
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
- AC-001: requirements.md -> test-cases.md (TC-003, TC-004, TC-024) -> tasks.md (T002, T007, T008, T010) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-001, TC-005, TC-007) -> tasks.md (T001, T003, T007, T008) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-002, TC-006, TC-008) -> tasks.md (T001, T003, T007, T008, T010) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-009, TC-020) -> tasks.md (T004, T005, T007, T008) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-011, TC-012) -> tasks.md (T004, T007, T008, T010) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-010, TC-013, TC-014) -> tasks.md (T004, T005, T007, T008) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-015, TC-016, TC-017, TC-018) -> tasks.md (T006, T007, T008, T010) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-001, TC-018, TC-019, TC-021, TC-022, TC-023, TC-024) -> tasks.md (T001, T006, T007, T008, T009, T010, T011, T012) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Add hash-locked offline parser bundle, twelve-language TOON policy, preflight, and install guidance.; refs: FR-002, NFR-002, NFR-005, NFR-007, AC-002, AC-003, AC-008, TC-001, TC-002, TC-008, TC-023, DEC-006; output: parser-lock.toon, language-policy.toon, offline setup/preflight code, and target contract.
- [x] T002: Implement safe corpus classification and explicit file/exclusion accounting.; refs: FR-001, AC-001, TC-003, TC-004, TC-024; output: reconciled file inventory and exclusion facts.
- [x] T003: Implement policy-driven Tree-sitter extraction for all twelve languages including Kotlin and Swift.; refs: FR-002, FR-004, AC-002, AC-003, TC-005, TC-006, TC-007, TC-008; output: canonical AST symbol, occurrence, import, and provable-call facts.
- [x] T004: Implement graph schema v2, stable identities, typed relations, trace hubs, bounds, and atomic v1 migration.; refs: FR-003, FR-004, FR-005, AC-004, AC-005, AC-006, TC-009, TC-010, TC-011, TC-012; output: verified bounded heterogeneous graph projection.
- [x] T005: Implement affected-file incremental refresh, invalidation, source recheck, stats, and verification.; refs: FR-006, FR-008, AC-004, AC-006, TC-013, TC-014, TC-020; output: fresh deterministic lifecycle and TOON diagnostics.
- [x] T006: Implement symbol-aware seed ranking, bounded typed traversal, qualified disambiguation, and pack acceptance.; refs: FR-007, FR-008, AC-007, AC-008, TC-015, TC-016, TC-017, TC-018, TC-019; output: deterministic economical graph retrieval with direct-read fallback.
- [x] T007: Add twelve-language, graph lifecycle, retrieval, fallback, and unsafe-input fixtures and automated cases TC-001 through TC-024.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-023, TC-024; output: focused deterministic test suites and TOON fixture manifests.
- [x] T008: Implement and execute two-run real-corpus release audit plus fault injection.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, TC-021, TC-022, DEC-007; output: deterministic audit evidence with production_ready gate and token economics.
- [x] T009: Run full validation, security testing, code review, compatibility, docs, install, and diff gates.; refs: AC-008, TC-021, TC-022, TC-023, TC-024, DEC-007; output: validation.md, security-review.md, code-review.md, and zero unresolved release blockers.
- [x] T010: Document graph setup, supported targets/languages, Kotlin/Swift parity, commands, schema, bounds, diagnostics, fallback, purge, privacy, offline operation, and production criteria; refresh generated catalogs.; refs: FR-001, FR-002, FR-005, FR-006, FR-007, FR-008, AC-001, AC-003, AC-005, AC-007, AC-008, TC-001, TC-019, TC-020, TC-023, TC-024, DEC-006, DEC-007; output: current skill contract, operator guide, parser provenance guidance, and generated references.
- [x] T011: Provision and verify the complete pinned graph runtime before protected Python 3.10 and 3.13 CI tests.; refs: AC-008, TC-001, TC-023, DEC-008; output: target-specific Linux TOON locks and offline installer/preflight gates.
- [ ] T012: Prove both protected Linux CI targets and publish the immutable corrective release.; refs: AC-008, TC-001, TC-023, DEC-008; output: green Python 3.10 and 3.13 jobs, completed validation evidence, tag v4.2.2, and published release.

## Task Dependencies
- T001: depends on none
- T002: depends on T001
- T003: depends on T001, T002
- T004: depends on T003
- T005: depends on T004
- T006: depends on T005
- T007: depends on T001, T002, T003, T004, T005, T006
- T008: depends on T007
- T009: depends on T008
- T010: depends on T001, T005, T006, T007
- T011: depends on T001, T007, T009
- T012: depends on T011

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-08-04

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
