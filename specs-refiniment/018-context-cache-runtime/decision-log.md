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
  at: "2026-08-03T11:36:00Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "decision-log.md"
  path: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "draft"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
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
| DEC-001 | 2026-08-03 | accepted | Harness Maintainers | Build feature 018 as a stacked branch from feature 017 commit ef67851 | The runtime integration depends on the optional cache introduced by feature 017 and must not force an unrequested merge or push | Merge 017 first; duplicate the cache; stacked branch | branch-plan.md; delivery-spec.md; implementation SDD | AC-001; T001 |
| DEC-002 | 2026-08-03 | accepted | Product and Architecture | Activate runtime cache integration automatically only when the optional context-cache skill is installed; otherwise preserve direct reads | Default installation and authority behavior must stay unchanged while module users receive automatic value | Mandatory cache; manual-only cache; installed-module auto mode | discovery.md; delivery-spec.md; runtime policy | FR-001; AC-001; TC-001 |
| DEC-003 | 2026-08-03 | accepted | Architecture and Security | Keep the disposable index in DELETE journal mode with atomic replacement and serialize warmers through a separate control database using bounded BEGIN IMMEDIATE | SQLite documents one writer at a time; host SQLite 3.51.0 predates the WAL-reset fix in 3.51.3; rollback journal avoids enabling an affected mode | Unconditional WAL; filesystem lock; control database | delivery-spec.md; qa-strategy.md; context-cache runtime | FR-002; NFR-001; AC-002; TC-002 |
| DEC-004 | 2026-08-03 | accepted | Harness Maintainers | Resolve strict TOON runtime policy by defaults plus exact skill and step overrides and clamp every request to the owning manifest budget | Step-level behavior must be auditable and deterministic without changing context-pack/v4 | Hidden code defaults only; add fields to all manifests; TOON policy overlay | delivery-spec.md; runtime-policy.schema.toon; tests | FR-003; AC-003; TC-003 |
| DEC-005 | 2026-08-03 | accepted | Security and Operations | Persist only bounded aggregate operation counters and token economics in the control database; never persist query text, prompts, retrieved content, credentials, or identity | Production observability is required but repository evidence and user prompts create privacy and injection risk | Full event payloads; no observability; aggregate counters | delivery-spec.md; security review; observe receipt | FR-005; NFR-003; AC-005; TC-005 |
| DEC-006 | 2026-08-03 | accepted | Product | Keep autonomous daemons, remote embeddings, full GraphRAG extraction, and network telemetry outside feature 018 | The accepted next task is operational integration of the deterministic local cache, not a new retrieval model or service | Add daemon and embeddings now; focused runtime integration | discovery.md; release-slicing.md; delivery-spec.md | AC-008; T008 |
| DEC-007 | 2026-08-03 | accepted | QA | Keep correctness and token economics deterministic; report latency only as observational evidence and never mix wall-clock values into golden fingerprints | Existing context-pack policy requires byte-stable receipts while production diagnosis still needs bounded operational counters | Latency in golden receipts; no latency evidence; separate observational tier | qa-strategy.md; qa-readiness.md; validation.md | NFR-004; AC-007; TC-007 |
