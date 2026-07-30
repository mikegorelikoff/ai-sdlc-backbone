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
| DEC-001 | 2026-07-27 | accepted | Engineering | Use one installable shared runtime, five neutral role contracts, one active role, JIT step/reference selectors, bounded configuration, and a hard `ai-sdlc-flow/v3` cut. | Accepted refinement package and user direction. | Dual runtime; compatibility shim; role skill duplicates. | requirements.md; design.md | REQ-001; AC-001; AC-006 |
| DEC-002 | 2026-07-27 | accepted | Repository Maintainers | Adopt per-skill step manifests and just-in-time procedural loading for all 44 installable skills | User feedback found the six flow steps incomplete and the 104–330-line SKILL.md bodies too expensive to load as a whole | Keep monolithic SKILL.md; add flow-only steps; create role-specific skill duplicates; selected common manifests plus skill-owned step files | requirements.md; design.md; test-cases.md; qa.md; tasks.md; every skill SKILL.md and steps/ directory; shared selector runtime; generated docs | AC-013; AC-014; AC-015; AC-016; TC-017; TC-018; TC-019; TC-020 |
| DEC-003 | 2026-07-27 | accepted | Repository Maintainers | Make all durable runtime-generated Markdown native OKF v0.2, replace human workspace indexes with feature bundle indexes, and move project context to `_ai_sdlc/context/project-context.md` without legacy runtime fallback. | User requested OKF for specs and all generated Markdown; repository inspection found duplicated manual frontmatter, ambiguous bundle roots, and incompatible root context/index paths. | Add only `type`; lifecycle bundles only; retain duplicate human indexes and root context; selected shared renderer plus feature/change/runtime bundles and explicit migration. | requirements.md; design.md; test-cases.md; qa.md; tasks.md; shared runtime; every durable Markdown generator; skill steps; docs; Feature 013 artifacts | REQ-012; REQ-013; REQ-014; REQ-015; AC-017; AC-018; AC-019; AC-020; AC-021; AC-022; TC-021; TC-022; TC-023; TC-024; TC-025; TC-026 |
