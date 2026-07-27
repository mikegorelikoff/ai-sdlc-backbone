---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "012-deduplicate-skill-entrypoints"
  artifact: "decision-log.md"
  path: "specs/012-deduplicate-skill-entrypoints/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
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
    - "ai-sdlc-branching"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-27 | accepted | Repository Maintainers | Retain ai-sdlc-flow and remove ai-sdlc-navigator after migrating its unique routes and context signals | 45 unique skill IDs; only flow and navigator share the same intent-routing entrypoint responsibility | Keep both; remove flow; retain flow and remove navigator | requirements.md; design.md; tasks.md; skills/ai-sdlc-flow; inventories and docs | FR-001; FR-002; AC-001; AC-002 |
