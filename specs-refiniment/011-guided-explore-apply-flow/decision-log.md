---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "decision-log.md"
  path: "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
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
| DEC-001 | 2026-07-26 | accepted | Product | Use `ai-sdlc-flow` as recommended Explore→Apply entrypoint; direct skills remain advanced. | Stakeholder feedback | Keep direct skills only; add public CLI | All refinement artifacts | AC-001, AC-009 |
| DEC-002 | 2026-07-26 | accepted | Product | Explore is read-only; Apply revalidates a fingerprint and performs one checkpoint. | Safety and transparency feedback | Multi-step Apply; implicit approval | Workflow, delivery spec, QA | AC-002, AC-003 |
| DEC-003 | 2026-07-26 | accepted | Repository Maintainers | Preserve tool-owned refinement and implementation roots; reject overrides, symlinks, and divergence. | Repository layout and rollback evidence | Collapse roots; user-selected roots | Routing and filesystem tests | AC-004 |
| DEC-004 | 2026-07-26 | accepted | Product | Expand roles only from request evidence. | Role-creep feedback | Always simulate every project role | Planning and QA | AC-005 |
| DEC-005 | 2026-07-26 | accepted | Repository Maintainers | Accept packs only at 100% anchor recall and 15% net savings including rereads. | Context benchmark and readability feedback | Always pack; token-only threshold | Context and QA | AC-007 |
| DEC-006 | 2026-07-26 | accepted | Engineering | Review spec and code before AI rationale or prior verdicts. | Missed-defect and anchoring feedback | Rationale-first review | Review and QA | AC-008 |
| DEC-007 | 2026-07-26 | accepted | Product | Exclude global installation repair. | Explicit scope choice | Include installer repair | All refinement artifacts | Scope boundary |
