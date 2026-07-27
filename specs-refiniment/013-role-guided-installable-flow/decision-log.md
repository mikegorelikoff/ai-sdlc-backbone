---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "decision-log.md"
  path: "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/013-role-guided-installable-flow/decision-log.md"
  status: "draft"
  owner: "Product Manager"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-27 | accepted | User and Harness Maintainer | Use one canonical installable runtime, five neutral JIT role references, one active role, bounded selector configuration, transparent prerequisite handoffs, and an ai-sdlc-flow/v2 hard cut. | Accepted implementation plan and explicit full-flow choices in the active conversation. | Dual runtime mirror; one-release shim; vendored helpers; installable role skills; fixed flow-only routing. | specs-refiniment/013-role-guided-installable-flow/*; specs/013-role-guided-installable-flow/*; skills/ai-sdlc-shared-runtime; skills/ai-sdlc-flow; docs | REQ-001; REQ-002; REQ-003; REQ-004; AC-001; AC-002; AC-003; AC-004; AC-005 |
