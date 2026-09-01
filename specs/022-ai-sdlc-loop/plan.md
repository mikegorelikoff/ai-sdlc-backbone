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
  at: "2026-09-01T11:26:28Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "plan.md"
  path: "specs/022-ai-sdlc-loop/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-09-01"
  updated_at: "2026-09-01"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T002, T012, T007) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-004) -> tasks.md (T001, T007) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-006) -> tasks.md (T001, T007) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-010) -> tasks.md (T001, T007) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-013) -> tasks.md (T001, T007) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-016) -> tasks.md (T001, T007) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-018) -> tasks.md (T003, T004, T006, T007, T008) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-025) -> tasks.md (T001, T002, T003) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-026) -> tasks.md (T002, T003) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-027) -> tasks.md (T002, T003) -> qa.md -> decision-log.md
- AC-011: requirements.md -> test-cases.md (TC-028) -> tasks.md (T002, T003) -> qa.md -> decision-log.md
- AC-012: requirements.md -> test-cases.md (TC-029) -> tasks.md (T002, T003) -> qa.md -> decision-log.md
- AC-013: requirements.md -> test-cases.md (TC-030) -> tasks.md (T002, T003, T012) -> qa.md -> decision-log.md
- AC-014: requirements.md -> test-cases.md (TC-031) -> tasks.md (T010, T015) -> qa.md -> decision-log.md
- AC-015: requirements.md -> test-cases.md (TC-032, TC-038) -> tasks.md (T012, T013, T014) -> qa.md -> decision-log.md
- AC-016: requirements.md -> test-cases.md (TC-033, TC-037) -> tasks.md (T011, T012, T014) -> qa.md -> decision-log.md
- AC-017: requirements.md -> test-cases.md (TC-034, TC-035) -> tasks.md (T011, T012, T014) -> qa.md -> decision-log.md
- AC-018: requirements.md -> test-cases.md (TC-036, TC-037) -> tasks.md (T011, T012, T014) -> qa.md -> decision-log.md
- AC-019: requirements.md -> test-cases.md (TC-032, TC-039) -> tasks.md (T011, T012, T013, T014, T015) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Build deterministic contracts, canonical fingerprints, local state, safe paths, approvals, evidence, status, and promotion.; refs: FR-003, FR-004, FR-006, FR-007, FR-008, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-009, AC-002, AC-003, AC-004, AC-005, AC-006, AC-008; output: stdlib runtime and versioned `ai-sdlc-loop/v1` artifacts.
- [x] T002: Build portable transactional installer for all three profiles and the exact Loop package.; refs: FR-001, FR-002, FR-015, NFR-002, NFR-003, NFR-006, NFR-009, AC-001, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013; output: `install.py`, `install.sh`, TOON install records, and verify action.
- [x] T003: Author the routed full-flow skill graph, delivery-control owners, canonical step manifests/documents, and public project trust/release files.; refs: FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, NFR-007, NFR-008, NFR-009, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013; output: working skills, shared runtime, README, license, security, contributing, changelog, and CI.
- [x] T004: Publish the validated repository and pin its exact commit as `products/ai-sdlc-loop`.; refs: FR-009, AC-007; output: public GitHub identity and Harness gitlink.
- [x] T011: Implement the canonical Harness engineering quality gate, deterministic context/report helper, schemas, examples, v2 step graph, and skill-local tests.; refs: FR-017, FR-018, FR-019, FR-020, NFR-010, NFR-011, AC-016, AC-017, AC-018, AC-019, TC-032, TC-033, TC-034, TC-035, TC-036, TC-037; output: `skills/ai-sdlc-engineering-quality-gate` with canonical TOON context/report contracts and safe report finalizer.
- [x] T012: Build the autonomous Loop adaptation and enforce the mandatory post-Implement gate.; refs: FR-001, FR-005, FR-006, FR-008, FR-010, FR-011, FR-015, FR-017, FR-018, FR-019, FR-020, NFR-001, NFR-003, NFR-009, NFR-010, NFR-011, AC-001, AC-013, AC-015, AC-016, AC-017, AC-018, AC-019, TC-032, TC-038, TC-039; output: `ai-sdlc-loop-engineering-quality-gate`, twenty-member installer inventory, orchestrator route, current-report enforcement, status, and promotion wiring.
- [x] T013: Register and route the canonical skill in Harness core and default discovery without changing unrelated lifecycle contracts.; refs: FR-020, AC-015, AC-019, TC-032, TC-039; output: core module entry, managed inventories, compatibility counts, direct flow route, and source-backed generated catalog inputs.
- [x] T005: Implement TC-001 through TC-019 plus TC-025 through TC-031 regression coverage.; refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-025, TC-026, TC-027, TC-028, TC-029, TC-030, TC-031; output: install, workflow, security, promotion, docs, and repository-trust tests.
- [ ] T006: Run hosted OS, release identity, submodule, parent regression, and manual UAT gates.; refs: TC-020, TC-021, TC-022, TC-023, TC-024, AC-007; output: evidence for TC-020 through TC-024 and release readiness.
- [x] T007: Run the original SDD, security, validation, code-review, and repository-required checks.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007; output: auditable validation and review receipts for the previous Loop revision.
- [x] T014: Implement and execute deterministic quality-gate fixtures and integration tests.; refs: TC-032, TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-039, AC-015, AC-016, AC-017, AC-018, AC-019; output: TC-032 through TC-039 evidence for determinism, path independence, typed findings, safe fixes, verification truthfulness, stale reports, mandatory routing, exact inventory, and core discovery.
- [x] T008: Update parent product-family references, decision log, and changelog without changing canonical navigation or duplicated explanations.; refs: FR-009, NFR-008, AC-007; output: contract-compliant Harness documentation linked to Loop.
- [x] T009: Verify every published Loop and Harness command against parser, help, tests, or reproducible fixtures.; refs: NFR-008, TC-018, TC-023; output: command-validation evidence and zero unsupported examples.
- [x] T010: Add the standalone Loop MkDocs site, source-backed reference checks, strict CI build, and GitHub Pages deployment.; refs: FR-016, NFR-008, AC-014, TC-031; output: `mkdocs.yml`, six-section `docs/`, docs dependency pins, workflow, and TC-031 regression.
- [x] T015: Publish source-backed usage, three realistic examples, the example quality report, inventories, changelogs, decision logs, generated catalogs, and refreshed validation evidence.; refs: FR-016, FR-020, NFR-008, AC-014, AC-019, TC-032, TC-039; output: contract-compliant Harness and Loop documentation plus current SDD, quality, and deterministic validation receipts.

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on previous applicable task / none
- T003: depends on previous applicable task / none
- T004: depends on previous applicable task / none
- T011: depends on T001
- T012: depends on T011
- T013: depends on T011
- T005: depends on previous applicable task / none
- T006: depends on previous applicable task / none
- T007: depends on previous applicable task / none
- T014: depends on T011, T012, T013
- T008: depends on previous applicable task / none
- T009: depends on previous applicable task / none
- T010: depends on previous applicable task / none
- T015: depends on T011, T012, T013, T014

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-09-01

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
