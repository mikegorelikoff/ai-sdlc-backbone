---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "decision-log.md"
  path: "specs/013-role-guided-installable-flow/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
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
| DEC-001 | 2026-07-27 | accepted | Engineering | Use one installable shared runtime, five neutral role contracts, one active role, JIT step/reference selectors, bounded configuration, and a hard `ai-sdlc-flow/v2` cut. | Accepted refinement package and user direction. | Dual runtime; compatibility shim; role skill duplicates. | requirements.md; design.md | REQ-001; AC-001; AC-006 |
| DEC-002 | 2026-07-27 | accepted | Repository Maintainers | Adopt per-skill step manifests and just-in-time procedural loading for all 44 installable skills | User feedback found the six flow steps incomplete and the 104–330-line SKILL.md bodies too expensive to load as a whole | Keep monolithic SKILL.md; add flow-only steps; create role-specific skill duplicates; selected common manifests plus skill-owned step files | requirements.md; design.md; test-cases.md; qa.md; tasks.md; every skill SKILL.md and steps/ directory; shared selector runtime; generated docs | AC-013; AC-014; AC-015; AC-016; TC-017; TC-018; TC-019; TC-020 |
