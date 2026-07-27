---
type: "ai-sdlc.decision-log"
title: "Decision Log"
description: "Auditable decisions, evidence, alternatives, and traceability."
tags:
  - "ai-sdlc"
  - "decision"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T12:13:45Z"
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
| DEC-003 | 2026-07-27 | accepted | Repository Maintainers | Make all durable runtime-generated Markdown native OKF v0.2, replace human workspace indexes with feature bundle indexes, and move project context to `_ai_sdlc/context/project-context.md` without legacy runtime fallback. | User requested OKF for specs and all generated Markdown; repository inspection found duplicated manual frontmatter, ambiguous bundle roots, and incompatible root context/index paths. | Add only `type`; lifecycle bundles only; retain duplicate human indexes and root context; selected shared renderer plus feature/change/runtime bundles and explicit migration. | all refinement artifacts; delivery-spec.md; qa-readiness.md; delivery-handoff-review.md; implementation SDD | REQ-012; REQ-013; REQ-014; REQ-015; AC-017; AC-018; AC-019; AC-020; AC-021; AC-022 |
