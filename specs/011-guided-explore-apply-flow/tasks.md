---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "tasks.md"
  path: "specs/011-guided-explore-apply-flow/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
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
    - "DEC-001"
    - "DEC-006"
    - "DEC-007"
    - "DEC-008"
    - "DEC-009"
    - "DEC-010"
    - "DEC-012"
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
  related_artifacts:
    - "specs/011-guided-explore-apply-flow/branch-plan.md"
    - "specs/011-guided-explore-apply-flow/decision-log.md"
    - "specs/011-guided-explore-apply-flow/design.md"
    - "specs/011-guided-explore-apply-flow/plan.md"
    - "specs/011-guided-explore-apply-flow/qa.md"
    - "specs/011-guided-explore-apply-flow/requirements.md"
    - "specs/011-guided-explore-apply-flow/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "approved"
---

# Tasks

## Implementation
- [x] T001. Confirm affected-module boundaries, canonical/generated ownership, exact validation commands, and DecisionCard schema version.
  Refs: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, AC-010, DEC-008, DEC-009, DEC-010
  Output: finalized implementation notes in design.md and stable affected-file inventory
- [x] T002. Implement canonical shared DecisionCard, fingerprint, role/rigor selection, context-economics decision, and workspace guards; synchronize the installed mirror.
  Refs: FR-003, FR-005, FR-006, FR-007, FR-008, AC-003, AC-004, AC-005, AC-006, AC-007, DEC-009, DEC-010
  Depends on: T001
  Output: skills/_shared/ai_sdlc_flow.py; shared-runtime mirror; focused helper updates
- [x] T003. Make navigator classification intent-first and expose reusable route evidence without recency-first fallback.
  Refs: FR-001, AC-001, DEC-001
  Depends on: T001, T002
  Output: skills/ai-sdlc-navigator/scripts/navigate.py
- [x] T004. Create `ai-sdlc-flow` skill, reference contract, Explore renderer, fingerprinted one-action Apply adapter, and spec-first review phase.
  Refs: FR-002, FR-003, FR-004, FR-006, FR-007, FR-008, FR-009, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, DEC-008, DEC-012
  Depends on: T002, T003
  Output: skills/ai-sdlc-flow/SKILL.md; skills/ai-sdlc-flow/references/flow-contract.md; skills/ai-sdlc-flow/scripts/flow.py
- [x] T005. Integrate flow with module/managed-skill inventories, project-scoped packaging, compatibility, and installed-runtime smoke paths.
  Refs: FR-010, AC-009, DEC-007
  Depends on: T004
  Output: module inventory; managed-skill inventory; compatibility/install-smoke updates

## Testing
- [x] T006. Add unit and integration fixtures for intent, DecisionCard parity, zero-write Explore, fingerprint drift, one-action Apply, roots, roles, rigor, and context economics.
  Refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007
  Depends on: T002, T003, T004
  Output: flow, navigator, shared-runtime, path, and context test modules
- [x] T007. Add blind-review, clean-review, direct-skill compatibility, installed packaging, catalog, and docs regression coverage.
  Refs: TC-017, TC-018, TC-019, TC-020, AC-008, AC-009, AC-010
  Depends on: T004, T005
  Output: review fixtures and compatibility/catalog/docs test updates
- [x] T008. Run focused suites, correct failures within SDD scope, and record deterministic command outcomes.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020
  Depends on: T006, T007
  Output: validation evidence in QA/plan status
- [x] T009. Run full SDD, refinement, compatibility, docs, catalog, and install-smoke gates; perform manual readability and blind-review checks.
  Refs: AC-002, AC-008, AC-009, AC-010, TC-003, TC-004, TC-017, TC-018, TC-019, TC-020
  Depends on: T008
  Output: final validation receipt and signoff evidence

## Documentation
- [x] T010. Update generated skill catalogs, workflow maps, role entrypoints, onboarding, README, and reference documentation to recommend `ai-sdlc-flow` and retain direct skills as advanced.
  Refs: FR-010, AC-009, AC-010, DEC-001
  Depends on: T004, T005
  Output: generated catalogs and canonical docs sources
- [x] T011. Review the final diff spec-first, reconcile independent findings, update SDD traceability and plans, and prepare validation handoff.
  Refs: FR-009, AC-008, AC-009, AC-010, DEC-006, DEC-012
  Depends on: T009, T010
  Output: approved SDD status; review evidence; updated plan.md and plan.toon
