---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "plan.md"
  path: "specs/012-deduplicate-skill-entrypoints/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/012-deduplicate-skill-entrypoints/_ai_sdlc/state.toon"
  decision_log: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
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
- AC-001: requirements.md -> test-cases.md (TC-001) -> tasks.md (T001, T006) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T002, T005, T006) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T002, T005, T006) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T001, T006) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005) -> tasks.md (T002, T006) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-006) -> tasks.md (T004, T006) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Extend flow intent routing with every unique navigator route and preserve ambiguity handling.; refs: FR-001, FR-003, FR-004, AC-001, AC-004, DEC-001; output: updated flow core, CLI behavior, and route evidence
- [x] T002: Remove `skills/ai-sdlc-navigator/` and all runtime inventory, manifest, compatibility, install, catalog, documentation, and test references.; refs: FR-002, FR-005, AC-002, AC-003, AC-005, DEC-001; output: one canonical entrypoint and 44-skill inventories
- [x] T003: Migrate navigator fixtures into flow tests and add stale-reference and exact-inventory coverage.; refs: TC-001, TC-002, TC-003, TC-004, TC-005; output: focused routing, removal, packaging, and compatibility tests
- [x] T004: Run focused and repository validation, repair stale generated artifacts, and record outcomes.; refs: TC-006, AC-006; output: passing validation evidence
- [x] T005: Replace navigator guidance with flow, add the migration note, regenerate catalogs, and verify 44-skill documentation.; refs: FR-006, AC-002, AC-003, DEC-001; output: updated README, onboarding, reference, migration, and generated docs
- [x] T006: Complete spec-first review, synchronize SDD task plans, and prepare handoff.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006; output: completed tasks and validated plan projections

## Task Dependencies
- T001: depends on previous applicable task / none
- T002: depends on T001
- T003: depends on T001, T002
- T004: depends on T003
- T005: depends on T002
- T006: depends on T004, T005

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-07-27

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
