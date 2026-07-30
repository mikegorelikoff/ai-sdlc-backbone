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
  at: "2026-07-27T12:28:55Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "plan.md"
  path: "specs/013-role-guided-installable-flow/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T002, T010) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002, TC-003, TC-004) -> tasks.md (T002, T008, T010) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-005) -> tasks.md (T003, T007, T010) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-006, TC-007, TC-008) -> tasks.md (T004, T007, T010) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-009) -> tasks.md (T004, T007, T010) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-010) -> tasks.md (T004, T007, T010) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-011) -> tasks.md (T003, T004, T013, T007, T010) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-012) -> tasks.md (T004, T007, T010) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-008, TC-013) -> tasks.md (T005, T007, T010) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-014) -> tasks.md (T007, T010) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-015) -> tasks.md (T006, T014, T010, T017) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-016) -> tasks.md (T009, T016, T023, T010) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-017) -> tasks.md (T011, T012, T015) -> qa.md -> decision-log.md
- AC-014: requirements.md -> test-cases.md (TC-018) -> tasks.md (T012, T015, T017) -> qa.md -> decision-log.md
- AC-015: requirements.md -> test-cases.md (TC-012, TC-019) -> tasks.md (T011, T015) -> qa.md -> decision-log.md
- AC-016: requirements.md -> test-cases.md (TC-011, TC-015, TC-020) -> tasks.md (T013, T014, T015, T016, T017) -> qa.md -> decision-log.md
- AC-017: requirements.md -> test-cases.md (TC-021, TC-022) -> tasks.md (T018, T019, T022, T023, T024) -> qa.md -> decision-log.md
- AC-018: requirements.md -> test-cases.md (TC-023, TC-025) -> tasks.md (T019, T020, T021, T022, T023) -> qa.md -> decision-log.md
- AC-019: requirements.md -> test-cases.md (TC-021) -> tasks.md (T018, T022, T023) -> qa.md -> decision-log.md
- AC-020: requirements.md -> test-cases.md (TC-022, TC-024) -> tasks.md (T020, T021, T022, T023, T024) -> qa.md -> decision-log.md
- AC-021: requirements.md -> test-cases.md (TC-023, TC-025) -> tasks.md (T020, T022, T023) -> qa.md -> decision-log.md
- AC-022: requirements.md -> test-cases.md (TC-026) -> tasks.md (T018, T022, T023, T024) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Consolidate all shared helpers under `skills/ai-sdlc-shared-runtime` and remove `_shared` plus synchronization fallbacks.; refs: REQ-001, AC-001; output: One canonical installable runtime and migrated imports.
- [x] T002: Move runtime tests/install smoke and migrate CI, validators, and documentation paths.; refs: REQ-001, REQ-007, AC-001, AC-002; output: Runtime-owned test harness and no repository-only fallback.
- [x] T003: Add schemas, registries, five role contracts, and JIT flow-step references.; refs: REQ-002, REQ-003, AC-003, AC-007; output: Validated declarative flow assets.
- [x] T004: Implement deterministic role/action selection, handoffs, JIT context, fingerprints, and `ai-sdlc-flow/v3`.; refs: REQ-002, REQ-003, REQ-004, AC-004, AC-005, AC-006, AC-007, AC-008; output: v2 runtime router and thin flow entrypoint.
- [x] T005: Extend bounded `values.flow` configuration and validation.; refs: REQ-005, AC-009; output: Role aliases, menu mode, and safe context selectors.
- [x] T006: Update reference generation and public installation/flow documentation.; refs: REQ-006, AC-011; output: Drift-checked, source-neutral role-guided documentation.
- [x] T011: Define and implement the `ai-sdlc-skill-steps/v1` manifest schema and canonical selector runtime.; refs: REQ-008, REQ-010, AC-013, AC-015; output: Safe deterministic manifest validation and JIT selection CLI.
- [x] T012: Migrate all 44 skills to concise routers and skill-owned step manifests while preserving normative sections.; refs: REQ-008, REQ-009, AC-013, AC-014; output: Complete prepare/execute/validate step packages and <120-line routers.
- [x] T013: Expand flow's six steps and include the owning-skill step in DecisionCard JIT context.; refs: REQ-003, REQ-010, AC-007, AC-016; output: Complete flow phases plus cross-package contained step selection.
- [x] T014: Update documentation generation, compatibility, packaging, and install validation for step manifests.; refs: REQ-011, AC-011, AC-016; output: Generated selector tables and installed step integrity checks.
- [x] T018: Add the shared OKF renderer, bounded parser, profile contract, provenance/trust rules, bundle indexer, conformance CLI, and atomic migration support.; refs: REQ-012, REQ-013, REQ-014, AC-017, AC-019, AC-022; output: One installable standard-library OKF v0.2 authority.
- [x] T019: Migrate lifecycle profile, SDD, specialized feature, and external-snapshot writers to the shared OKF contract.; refs: REQ-012, REQ-014, AC-017, AC-018; output: Conformant feature bundles and snapshots with explicit profiles.
- [x] T020: Migrate change-set and repository runtime Markdown writers, replace human specs indexes, and hard-cut project-context/module paths.; refs: REQ-013, REQ-015, AC-018, AC-020, AC-021; output: Conformant change/runtime bundles with no legacy output routes.
- [x] T021: Centralize OKF guidance in one shared reference and update skill steps, routing docs, generated catalogs, packaging, and compatibility checks.; refs: REQ-011, REQ-012, REQ-013, AC-018, AC-020; output: Lean skill contracts and source-of-truth OKF documentation.
- [x] T007: Add focused runtime, flow, role, selector, config, safety, and context-economics tests.; refs: AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010; output: Automated TC-005 through TC-014 coverage.
- [x] T008: Run full, selective, and disposable-global installation smoke tests.; refs: AC-002; output: Isolated installation evidence for TC-002 through TC-004.
- [x] T009: Run SDD, docs, focused, and repository-wide validation.; refs: AC-012; output: Passing deterministic validation receipt.
- [x] T015: Add manifest, selector, contract-preservation, size-budget, flow-integration, docs, and installed-layout tests.; refs: AC-013, AC-014, AC-015, AC-016; output: Automated TC-017 through TC-020 coverage.
- [x] T016: Rerun the full validation matrix and independent review after step migration.; refs: AC-012, AC-016; output: Current zero-failure receipt and approved review addendum.
- [x] T022: Add focused OKF unit, writer-contract, path-hard-cut, migration, index, and installation tests.; refs: AC-017, AC-018, AC-019, AC-020, AC-021, AC-022; output: Automated TC-021 through TC-026 coverage.
- [x] T023: Run Feature 013 conformance, SDD gates, full runtime/docs/install validation, and refresh the validation receipt and review.; refs: AC-012, AC-017, AC-018, AC-019, AC-020, AC-021, AC-022; output: Current validation and review evidence for the OKF-expanded diff.
- [x] T010: Prepare the original independent code-review boundary, spec comparison, validation receipt, and handoff evidence.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012; output: Review-ready Feature 013 package with traceability.
- [x] T017: Document progressive-disclosure authoring, selector usage, directory layout, and migration rules without naming external source systems.; refs: REQ-009, REQ-011, AC-011, AC-014, AC-016; output: Maintainer and contributor guidance for skill steps.
- [x] T024: Migrate both Feature 013 artifact trees to OKF v0.2, generate their bundle indexes, and record DEC-003 traceability across refinement and implementation.; refs: REQ-012, REQ-013, REQ-015, AC-017, AC-020, AC-022; output: Portable Feature 013 refinement and implementation bundles.

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on previous applicable task / none
- T003: depends on previous applicable task / none
- T004: depends on previous applicable task / none
- T005: depends on previous applicable task / none
- T006: depends on previous applicable task / none
- T011: depends on previous applicable task / none
- T012: depends on previous applicable task / none
- T013: depends on previous applicable task / none
- T014: depends on previous applicable task / none
- T018: depends on previous applicable task / none
- T019: depends on previous applicable task / none
- T020: depends on previous applicable task / none
- T021: depends on previous applicable task / none
- T007: depends on previous applicable task / none
- T008: depends on previous applicable task / none
- T009: depends on previous applicable task / none
- T015: depends on previous applicable task / none
- T016: depends on previous applicable task / none
- T022: depends on previous applicable task / none
- T023: depends on previous applicable task / none
- T010: depends on previous applicable task / none
- T017: depends on previous applicable task / none
- T024: depends on previous applicable task / none

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-27

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
