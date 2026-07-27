---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "plan.md"
  path: "specs/011-guided-explore-apply-flow/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs/011-guided-explore-apply-flow/decision-log.md"
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
- AC-001: requirements.md -> test-cases.md (TC-001, TC-002) -> tasks.md (T003, T006, T008) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-003, TC-004) -> tasks.md (T004, T006, T008, T009) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-005, TC-006) -> tasks.md (T002, T004, T006, T008) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-007, TC-008, TC-009, TC-010) -> tasks.md (T002, T004, T006, T008) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-011, TC-012) -> tasks.md (T002, T004, T006, T008) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-013, TC-014) -> tasks.md (T002, T004, T006, T008) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-015, TC-016) -> tasks.md (T002, T004, T006, T008) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-017, TC-018) -> tasks.md (T004, T007, T008, T009, T011) -> qa.md -> decision-log.md
- AC-009: requirements.md -> test-cases.md (TC-019) -> tasks.md (T005, T007, T008, T009, T010, T011) -> qa.md -> decision-log.md
- AC-010: requirements.md -> test-cases.md (TC-020) -> tasks.md (T001, T007, T008, T009, T010, T011) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Confirm affected-module boundaries, canonical/generated ownership, exact validation commands, and DecisionCard schema version.; refs: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, AC-010, DEC-008, DEC-009, DEC-010; output: finalized implementation notes in design.md and stable affected-file inventory
- [x] T002: Implement canonical shared DecisionCard, fingerprint, role/rigor selection, context-economics decision, and workspace guards; synchronize the installed mirror.; refs: FR-003, FR-005, FR-006, FR-007, FR-008, AC-003, AC-004, AC-005, AC-006, AC-007, DEC-009, DEC-010; output: skills/_shared/ai_sdlc_flow.py; shared-runtime mirror; focused helper updates
- [x] T003: Make navigator classification intent-first and expose reusable route evidence without recency-first fallback.; refs: FR-001, AC-001, DEC-001; output: skills/ai-sdlc-navigator/scripts/navigate.py
- [x] T004: Create `ai-sdlc-flow` skill, reference contract, Explore renderer, fingerprinted one-action Apply adapter, and spec-first review phase.; refs: FR-002, FR-003, FR-004, FR-006, FR-007, FR-008, FR-009, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, DEC-008, DEC-012; output: skills/ai-sdlc-flow/SKILL.md; skills/ai-sdlc-flow/references/flow-contract.md; skills/ai-sdlc-flow/scripts/flow.py
- [x] T005: Integrate flow with module/managed-skill inventories, project-scoped packaging, compatibility, and installed-runtime smoke paths.; refs: FR-010, AC-009, DEC-007; output: module inventory; managed-skill inventory; compatibility/install-smoke updates
- [x] T006: Add unit and integration fixtures for intent, DecisionCard parity, zero-write Explore, fingerprint drift, one-action Apply, roots, roles, rigor, and context economics.; refs: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007; output: flow, navigator, shared-runtime, path, and context test modules
- [x] T007: Add blind-review, clean-review, direct-skill compatibility, installed packaging, catalog, and docs regression coverage.; refs: TC-017, TC-018, TC-019, TC-020, AC-008, AC-009, AC-010; output: review fixtures and compatibility/catalog/docs test updates
- [x] T008: Run focused suites, correct failures within SDD scope, and record deterministic command outcomes.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020; output: validation evidence in QA/plan status
- [x] T009: Run full SDD, refinement, compatibility, docs, catalog, and install-smoke gates; perform manual readability and blind-review checks.; refs: AC-002, AC-008, AC-009, AC-010, TC-003, TC-004, TC-017, TC-018, TC-019, TC-020; output: final validation receipt and signoff evidence
- [x] T010: Update generated skill catalogs, workflow maps, role entrypoints, onboarding, README, and reference documentation to recommend `ai-sdlc-flow` and retain direct skills as advanced.; refs: FR-010, AC-009, AC-010, DEC-001; output: generated catalogs and canonical docs sources
- [x] T011: Review the final diff spec-first, reconcile independent findings, update SDD traceability and plans, and prepare validation handoff.; refs: FR-009, AC-008, AC-009, AC-010, DEC-006, DEC-012; output: approved SDD status; review evidence; updated plan.md and plan.toon

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T001, T002
- T004: depends on T002, T003
- T005: depends on T004
- T006: depends on T002, T003, T004
- T007: depends on T004, T005
- T008: depends on T006, T007
- T009: depends on T008
- T010: depends on T004, T005
- T011: depends on T009, T010

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-27

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
