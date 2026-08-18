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
  at: "2026-08-17T11:50:05Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "tasks.md"
  path: "specs/022-ai-sdlc-loop/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
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
    - "specs/022-ai-sdlc-loop/branch-plan.md"
    - "specs/022-ai-sdlc-loop/decision-log.md"
    - "specs/022-ai-sdlc-loop/design.md"
    - "specs/022-ai-sdlc-loop/index.md"
    - "specs/022-ai-sdlc-loop/plan.md"
    - "specs/022-ai-sdlc-loop/qa.md"
    - "specs/022-ai-sdlc-loop/requirements.md"
    - "specs/022-ai-sdlc-loop/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "approved"
    - "ai-sdlc-loop"
---

# Tasks

## Implementation
- [x] T001. Build deterministic contracts, canonical fingerprints, local state, safe paths, approvals, evidence, status, and promotion.
Output: stdlib runtime and versioned `ai-sdlc-loop/v1` artifacts.
Refs: FR-003, FR-004, FR-006, FR-007, FR-008, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-009, AC-002, AC-003, AC-004, AC-005, AC-006, AC-008
- [x] T002. Build portable transactional installer for all three profiles and the exact sixteen-skill plus shared-runtime package.
Output: `install.py`, `install.sh`, seventeen-member TOON install records, and verify action.
Refs: FR-001, FR-002, FR-015, NFR-002, NFR-003, NFR-006, NFR-009, AC-001, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013
- [x] T003. Author the routed full-flow skill graph, eleven delivery-control owners, canonical step manifests/documents, and public project trust/release files.
Output: sixteen working skills, shared runtime, README, license, security, contributing, changelog, and CI.
Refs: FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, NFR-007, NFR-008, NFR-009, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013
- [x] T004. Publish the validated repository and pin its exact commit as `products/ai-sdlc-loop`.
Output: public GitHub identity and Harness gitlink.
Refs: FR-009, AC-007

## Testing
- [x] T005. Implement TC-001 through TC-019 plus TC-025 through TC-030 TOON/skill-graph regression coverage before runtime completion.
Output: install, workflow, security, promotion, docs, and repository-trust tests.
Refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-025, TC-026, TC-027, TC-028, TC-029, TC-030, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013
- [ ] T006. Run hosted OS, release identity, submodule, parent regression, and manual UAT gates.
Output: evidence for TC-020 through TC-024 and release readiness.
Refs: TC-020, TC-021, TC-022, TC-023, TC-024, AC-007
- [x] T007. Run SDD, security, validation, code-review, and repository-required checks.
Output: auditable validation and review receipts.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007

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
