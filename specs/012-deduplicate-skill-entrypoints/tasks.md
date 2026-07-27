---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "tasks.md"
  path: "specs/012-deduplicate-skill-entrypoints/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/012-deduplicate-skill-entrypoints/_ai_sdlc/state.toon"
  decision_log: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  status: "review"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "DEC-001"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
  related_artifacts:
    - "specs/012-deduplicate-skill-entrypoints/branch-plan.md"
    - "specs/012-deduplicate-skill-entrypoints/code-review.md"
    - "specs/012-deduplicate-skill-entrypoints/decision-log.md"
    - "specs/012-deduplicate-skill-entrypoints/design.md"
    - "specs/012-deduplicate-skill-entrypoints/plan.md"
    - "specs/012-deduplicate-skill-entrypoints/qa.md"
    - "specs/012-deduplicate-skill-entrypoints/requirements.md"
    - "specs/012-deduplicate-skill-entrypoints/test-cases.md"
    - "specs/012-deduplicate-skill-entrypoints/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
    - "deduplication"
---

# Tasks

## Implementation
- [x] T001. Extend flow intent routing with every unique navigator route and preserve ambiguity handling.
  Refs: FR-001, FR-003, FR-004, AC-001, AC-004, DEC-001
  Output: updated flow core, CLI behavior, and route evidence
- [x] T002. Remove `skills/ai-sdlc-navigator/` and all runtime inventory, manifest, compatibility, install, catalog, documentation, and test references.
  Refs: FR-002, FR-005, AC-002, AC-003, AC-005, DEC-001
  Depends on: T001
  Output: one canonical entrypoint and 44-skill inventories

## Testing
- [x] T003. Migrate navigator fixtures into flow tests and add stale-reference and exact-inventory coverage.
  Refs: TC-001, TC-002, TC-003, TC-004, TC-005
  Depends on: T001, T002
  Output: focused routing, removal, packaging, and compatibility tests
- [x] T004. Run focused and repository validation, repair stale generated artifacts, and record outcomes.
  Refs: TC-006, AC-006
  Depends on: T003
  Output: passing validation evidence

## Documentation
- [x] T005. Replace navigator guidance with flow, add the migration note, regenerate catalogs, and verify 44-skill documentation.
  Refs: FR-006, AC-002, AC-003, DEC-001
  Depends on: T002
  Output: updated README, onboarding, reference, migration, and generated docs
- [x] T006. Complete spec-first review, synchronize SDD task plans, and prepare handoff.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006
  Depends on: T004, T005
  Output: completed tasks and validated plan projections
