---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "branch-plan.md"
  path: "specs/012-deduplicate-skill-entrypoints/branch-plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "quick"
  state_file: "specs/012-deduplicate-skill-entrypoints/_ai_sdlc/state.toon"
  decision_log: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  status: "approved"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts:
    - "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "branch-plan"
    - "approved"
---

# branch-plan.md

## Implementation
- Branch: `feature/012-deduplicate-skill-entrypoints`.
- Base: committed `feature/011-guided-explore-apply-flow` because the retained flow package is not on main.
- Scope: consolidate navigator behavior into flow and remove the duplicate navigator package.

## Testing
- Require flow routing regression, compatibility, module, install-smoke, and docs/catalog validation.

## Documentation
- Add a migration note from `ai-sdlc-navigator` to `ai-sdlc-flow` and regenerate catalogs.
