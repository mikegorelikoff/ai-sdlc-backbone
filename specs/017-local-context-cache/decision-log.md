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
  at: "2026-08-03T09:41:23Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "decision-log.md"
  path: "specs/017-local-context-cache/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-08-03 | accepted | Harness Maintainers | Ship context cache as an optional local module using SQLite FTS5 plus deterministic graph-enhanced expansion; keep repository files authoritative and emit only TOON machine interchange | User requested a separately installable local RAG or GraphRAG cache to reduce tokens and search repository knowledge; existing context-pack/v4 is the integration boundary | Built-in lexical and graph retrieval; mandatory vector service; remote RAG service | requirements.md; design.md; tasks.md; ai-sdlc-context-cache; modules/context-cache/module.toon | AC-001 through AC-013; TC-001 through TC-013 |
| DEC-002 | 2026-08-03 | accepted | Product and Architecture | Position the MVP as graph-enhanced RAG and defer full GraphRAG entity extraction, community summaries, and global search | RF-003 and Microsoft GraphRAG primary sources distinguish typed local relations from the full pipeline | Claim full GraphRAG; remove relations; precise graph-enhanced wording | requirements.md; design.md; docs/how-to/use-local-context-cache.md | FR-006; AC-004; TC-004 |
| DEC-003 | 2026-08-03 | accepted | Harness Maintainers | Require the owning step document and 100 percent critical-anchor recall before packed context is sufficient | RF-004 and upstream DEC-004 identify the prototype's missing mandatory context | Cache hits only; optional anchors; manifest-resolved mandatory context | design.md; context-cache runtime; test-cases.md | NFR-007; AC-005; TC-005 |
| DEC-004 | 2026-08-03 | accepted | QA and Maintainers | Gate packed cases at at least 15 percent net savings and add deterministic TOON golden benchmarks; keep latency observational | RF-004; RF-007; deterministic output requirement | Unmeasured claims; non-deterministic timing receipts; stable quality and economics receipt | context-cache runtime; benchmark schemas; qa.md | FR-013; NFR-007; AC-013; TC-013 |
