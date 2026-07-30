---
type: "ai-sdlc.tasks"
title: "Implementation Tasks"
description: "Traceable implementation task breakdown and status."
tags:
  - "ai-sdlc"
  - "sdd"
  - "tasks"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "tasks.md"
  path: "specs/013-role-guided-installable-flow/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
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
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-004"
    - "REQ-005"
    - "REQ-006"
    - "REQ-007"
    - "REQ-008"
    - "REQ-009"
    - "REQ-010"
    - "REQ-011"
    - "TC-002"
    - "TC-004"
    - "TC-005"
    - "TC-014"
    - "TC-017"
    - "TC-020"
  related_artifacts:
    - "specs/013-role-guided-installable-flow/branch-plan.md"
    - "specs/013-role-guided-installable-flow/code-review.md"
    - "specs/013-role-guided-installable-flow/decision-log.md"
    - "specs/013-role-guided-installable-flow/design.md"
    - "specs/013-role-guided-installable-flow/plan.md"
    - "specs/013-role-guided-installable-flow/qa.md"
    - "specs/013-role-guided-installable-flow/requirements.md"
    - "specs/013-role-guided-installable-flow/test-cases.md"
    - "specs/013-role-guided-installable-flow/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
---

# Tasks

## Implementation
- [x] T001. Consolidate all shared helpers under `skills/ai-sdlc-shared-runtime` and remove `_shared` plus synchronization fallbacks.
  Output: One canonical installable runtime and migrated imports.
  Refs: REQ-001, AC-001
- [x] T002. Move runtime tests/install smoke and migrate CI, validators, and documentation paths.
  Output: Runtime-owned test harness and no repository-only fallback.
  Refs: REQ-001, REQ-007, AC-001, AC-002
- [x] T003. Add schemas, registries, five role contracts, and JIT flow-step references.
  Output: Validated declarative flow assets.
  Refs: REQ-002, REQ-003, AC-003, AC-007
- [x] T004. Implement deterministic role/action selection, handoffs, JIT context, fingerprints, and `ai-sdlc-flow/v3`.
  Output: v2 runtime router and thin flow entrypoint.
  Refs: REQ-002, REQ-003, REQ-004, AC-004, AC-005, AC-006, AC-007, AC-008
- [x] T005. Extend bounded `values.flow` configuration and validation.
  Output: Role aliases, menu mode, and safe context selectors.
  Refs: REQ-005, AC-009
- [x] T006. Update reference generation and public installation/flow documentation.
  Output: Drift-checked, source-neutral role-guided documentation.
  Refs: REQ-006, AC-011
- [x] T011. Define and implement the `ai-sdlc-skill-steps/v1` manifest schema and canonical selector runtime.
  Output: Safe deterministic manifest validation and JIT selection CLI.
  Refs: REQ-008, REQ-010, AC-013, AC-015
- [x] T012. Migrate all 44 skills to concise routers and skill-owned step manifests while preserving normative sections.
  Output: Complete prepare/execute/validate step packages and <120-line routers.
  Refs: REQ-008, REQ-009, AC-013, AC-014
- [x] T013. Expand flow's six steps and include the owning-skill step in DecisionCard JIT context.
  Output: Complete flow phases plus cross-package contained step selection.
  Refs: REQ-003, REQ-010, AC-007, AC-016
- [x] T014. Update documentation generation, compatibility, packaging, and install validation for step manifests.
  Output: Generated selector tables and installed step integrity checks.
  Refs: REQ-011, AC-011, AC-016
- [x] T018. Add the shared OKF renderer, bounded parser, profile contract, provenance/trust rules, bundle indexer, conformance CLI, and atomic migration support.
  Output: One installable standard-library OKF v0.2 authority.
  Refs: REQ-012, REQ-013, REQ-014, AC-017, AC-019, AC-022
- [x] T019. Migrate lifecycle profile, SDD, specialized feature, and external-snapshot writers to the shared OKF contract.
  Output: Conformant feature bundles and snapshots with explicit profiles.
  Refs: REQ-012, REQ-014, AC-017, AC-018
- [x] T020. Migrate change-set and repository runtime Markdown writers, replace human specs indexes, and hard-cut project-context/module paths.
  Output: Conformant change/runtime bundles with no legacy output routes.
  Refs: REQ-013, REQ-015, AC-018, AC-020, AC-021
- [x] T021. Centralize OKF guidance in one shared reference and update skill steps, routing docs, generated catalogs, packaging, and compatibility checks.
  Output: Lean skill contracts and source-of-truth OKF documentation.
  Refs: REQ-011, REQ-012, REQ-013, AC-018, AC-020

## Testing
- [x] T007. Add focused runtime, flow, role, selector, config, safety, and context-economics tests.
  Output: Automated TC-005 through TC-014 coverage.
  Refs: AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010
- [x] T008. Run full, selective, and disposable-global installation smoke tests.
  Output: Isolated installation evidence for TC-002 through TC-004.
  Refs: AC-002
- [x] T009. Run SDD, docs, focused, and repository-wide validation.
  Output: Passing deterministic validation receipt.
  Refs: AC-012
- [x] T015. Add manifest, selector, contract-preservation, size-budget, flow-integration, docs, and installed-layout tests.
  Output: Automated TC-017 through TC-020 coverage.
  Refs: AC-013, AC-014, AC-015, AC-016
- [x] T016. Rerun the full validation matrix and independent review after step migration.
  Output: Current zero-failure receipt and approved review addendum.
  Refs: AC-012, AC-016
- [x] T022. Add focused OKF unit, writer-contract, path-hard-cut, migration, index, and installation tests.
  Output: Automated TC-021 through TC-026 coverage.
  Refs: AC-017, AC-018, AC-019, AC-020, AC-021, AC-022
- [x] T023. Run Feature 013 conformance, SDD gates, full runtime/docs/install validation, and refresh the validation receipt and review.
  Output: Current validation and review evidence for the OKF-expanded diff.
  Refs: AC-012, AC-017, AC-018, AC-019, AC-020, AC-021, AC-022

## Documentation
- [x] T010. Prepare the original independent code-review boundary, spec comparison, validation receipt, and handoff evidence.
  Output: Review-ready Feature 013 package with traceability.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012
- [x] T017. Document progressive-disclosure authoring, selector usage, directory layout, and migration rules without naming external source systems.
  Output: Maintainer and contributor guidance for skill steps.
  Refs: REQ-009, REQ-011, AC-011, AC-014, AC-016
- [x] T024. Migrate both Feature 013 artifact trees to OKF v0.2, generate their bundle indexes, and record DEC-003 traceability across refinement and implementation.
  Output: Portable Feature 013 refinement and implementation bundles.
  Refs: REQ-012, REQ-013, REQ-015, AC-017, AC-020, AC-022
