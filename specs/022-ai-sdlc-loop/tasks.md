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
  at: "2026-09-01T09:52:05Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "tasks.md"
  path: "specs/022-ai-sdlc-loop/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-09-01"
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
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "AC-017"
    - "AC-018"
    - "AC-019"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
    - "NFR-009"
    - "NFR-010"
    - "NFR-011"
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
    - "TC-025"
    - "TC-026"
    - "TC-027"
    - "TC-028"
    - "TC-029"
    - "TC-030"
    - "TC-031"
    - "TC-032"
    - "TC-033"
    - "TC-034"
    - "TC-035"
    - "TC-036"
    - "TC-037"
    - "TC-038"
    - "TC-039"
  related_artifacts:
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/code-review.md"
    - "specs/022-ai-sdlc-loop/commit-message.md"
    - "specs/022-ai-sdlc-loop/commit-readiness.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/security-review.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
    - "specs/022-ai-sdlc-loop/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "approved"
    - "engineering-quality-gate"
    - "ai-sdlc-loop"
---

# Tasks

## Implementation
- [x] T001. Build deterministic contracts, canonical fingerprints, local state, safe paths, approvals, evidence, status, and promotion.
Output: stdlib runtime and versioned `ai-sdlc-loop/v1` artifacts.
Refs: FR-003, FR-004, FR-006, FR-007, FR-008, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-009, AC-002, AC-003, AC-004, AC-005, AC-006, AC-008
- [x] T002. Build portable transactional installer for all three profiles and the exact Loop package.
Output: `install.py`, `install.sh`, TOON install records, and verify action.
Refs: FR-001, FR-002, FR-015, NFR-002, NFR-003, NFR-006, NFR-009, AC-001, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013
- [x] T003. Author the routed full-flow skill graph, delivery-control owners, canonical step manifests/documents, and public project trust/release files.
Output: working skills, shared runtime, README, license, security, contributing, changelog, and CI.
Refs: FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, NFR-007, NFR-008, NFR-009, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013
- [x] T004. Publish the validated repository and pin its exact commit as `products/ai-sdlc-loop`.
Output: public GitHub identity and Harness gitlink.
Refs: FR-009, AC-007
- [x] T011. Implement the canonical Harness engineering quality gate, deterministic context/report helper, schemas, examples, v2 step graph, and skill-local tests.
Output: `skills/ai-sdlc-engineering-quality-gate` with canonical TOON context/report contracts and safe report finalizer.
Refs: FR-017, FR-018, FR-019, FR-020, NFR-010, NFR-011, AC-016, AC-017, AC-018, AC-019, TC-032, TC-033, TC-034, TC-035, TC-036, TC-037
Depends on: T001
- [x] T012. Build the autonomous Loop adaptation and enforce the mandatory post-Implement gate.
Output: `ai-sdlc-loop-engineering-quality-gate`, twenty-member installer inventory, orchestrator route, current-report enforcement, status, and promotion wiring.
Refs: FR-001, FR-005, FR-006, FR-008, FR-010, FR-011, FR-015, FR-017, FR-018, FR-019, FR-020, NFR-001, NFR-003, NFR-009, NFR-010, NFR-011, AC-001, AC-013, AC-015, AC-016, AC-017, AC-018, AC-019, TC-032, TC-038, TC-039
Depends on: T011
- [x] T013. Register and route the canonical skill in Harness core and default discovery without changing unrelated lifecycle contracts.
Output: core module entry, managed inventories, compatibility counts, direct flow route, and source-backed generated catalog inputs.
Refs: FR-020, AC-015, AC-019, TC-032, TC-039
Depends on: T011

## Testing
- [x] T005. Implement TC-001 through TC-019 plus TC-025 through TC-031 regression coverage.
Output: install, workflow, security, promotion, docs, and repository-trust tests.
Refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-025, TC-026, TC-027, TC-028, TC-029, TC-030, TC-031
- [ ] T006. Run hosted OS, release identity, submodule, parent regression, and manual UAT gates.
Output: evidence for TC-020 through TC-024 and release readiness.
Refs: TC-020, TC-021, TC-022, TC-023, TC-024, AC-007
- [x] T007. Run the original SDD, security, validation, code-review, and repository-required checks.
Output: auditable validation and review receipts for the previous Loop revision.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007
- [x] T014. Implement and execute deterministic quality-gate fixtures and integration tests.
Output: TC-032 through TC-039 evidence for determinism, path independence, typed findings, safe fixes, verification truthfulness, stale reports, mandatory routing, exact inventory, and core discovery.
Refs: TC-032, TC-033, TC-034, TC-035, TC-036, TC-037, TC-038, TC-039, AC-015, AC-016, AC-017, AC-018, AC-019
Depends on: T011, T012, T013

## Documentation
- [x] T008. Update parent product-family references, decision log, and changelog without changing canonical navigation or duplicated explanations.
Output: contract-compliant Harness documentation linked to Loop.
Refs: FR-009, NFR-008, AC-007
- [x] T009. Verify every published Loop and Harness command against parser, help, tests, or reproducible fixtures.
Output: command-validation evidence and zero unsupported examples.
Refs: NFR-008, TC-018, TC-023
- [x] T010. Add the standalone Loop MkDocs site, source-backed reference checks, strict CI build, and GitHub Pages deployment.
Output: `mkdocs.yml`, six-section `docs/`, docs dependency pins, workflow, and TC-031 regression.
Refs: FR-016, NFR-008, AC-014, TC-031
- [x] T015. Publish source-backed usage, three realistic examples, the example quality report, inventories, changelogs, decision logs, generated catalogs, and refreshed validation evidence.
Output: contract-compliant Harness and Loop documentation plus current SDD, quality, and deterministic validation receipts.
Refs: FR-016, FR-020, NFR-008, AC-014, AC-019, TC-032, TC-039
Depends on: T011, T012, T013, T014
