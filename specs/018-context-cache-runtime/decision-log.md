---
type: "ai-sdlc.decision-log"
title: "Decision Log"
description: "Auditable decisions, evidence, alternatives, and traceability."
tags:
  - "ai-sdlc"
  - "decision"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:31:33Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "decision-log.md"
  path: "specs/018-context-cache-runtime/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "full"
  state_file: "specs/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-branching"
    - "decision-log"
    - "approved"
---
# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-08-03 | accepted | Harness Maintainers | Build feature 018 as a stacked branch from feature 017 commit ef67851 | Runtime integration depends on the optional cache introduced by feature 017 | Merge 017 first; duplicate the cache; stacked branch | branch-plan.md; delivery-spec.md; implementation SDD | AC-001; T001 |
| DEC-002 | 2026-08-03 | accepted | Product and Architecture | Activate cache integration only when the optional context-cache skill is project-installed; otherwise preserve direct reads | Default installation and authority behavior must remain unchanged | Mandatory cache; manual-only cache; installed-module auto mode | requirements.md; design.md; runtime policy | FR-001; AC-001; TC-001 |
| DEC-003 | 2026-08-03 | accepted | Architecture and Security | Keep the disposable index in DELETE journal mode with atomic replacement and serialize warmers through a separate control database and bounded immediate transaction | Single-writer coordination and crash recovery must remain local and deterministic | WAL; filesystem lock; control database | design.md; qa.md; context-cache runtime | FR-002; NFR-001; AC-002; TC-002 |
| DEC-004 | 2026-08-03 | accepted | Harness Maintainers | Resolve strict TOON runtime policy by defaults plus exact skill and step overrides, clamped to the owning manifest | Step behavior must remain auditable without widening StepCard authority or budget | Hidden defaults; manifest changes; TOON policy overlay | design.md; runtime-policy.toon; tests | FR-003; AC-003; TC-004 |
| DEC-005 | 2026-08-03 | accepted | Security and Operations | Persist only allowlisted aggregate operation counters and token economics | Queries, prompts, content, credentials, and identity must not enter observations | Full payload events; no observability; aggregate counters | design.md; security-review.md; tests | FR-005; NFR-003; AC-005; TC-006 |
| DEC-006 | 2026-08-03 | accepted | Product | Keep daemons, remote embeddings, full GraphRAG extraction, and network telemetry out of feature 018 | The scope is operational integration of deterministic local retrieval | Add services now; focused local integration | requirements.md; design.md; tasks.md | AC-008; T008 |
| DEC-007 | 2026-08-03 | accepted | QA | Keep correctness and token economics deterministic; latency remains observational and outside golden fingerprints | Byte-stable receipts and production diagnosis are both required | Golden latency; no latency evidence; separate observation tier | qa.md; validation.md; test-cases.md | NFR-004; AC-007; TC-008 |
