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
  at: "2026-08-03T10:10:07Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "decision-log.md"
  path: "specs-refiniment/017-local-context-cache/decision-log.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "draft"
  owner: "PM"
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
| DEC-001 | 2026-08-03 | accepted | Maintainers | Ship the cache as an explicit optional module backed by local SQLite FTS5 | User direction; RF-001; default-profile compatibility | Mandatory cache; external service; optional local module | delivery-spec.md; modules/context-cache/module.toon | FR-001; AC-001; TC-001 |
| DEC-002 | 2026-08-03 | accepted | Architecture | Use contextual lexical retrieval with stable deterministic ranking as the offline baseline | RF-002; exact identifiers are central to repository work | Embeddings only; BM25 baseline; custom lexical baseline | delivery-spec.md; qa-strategy.md | FR-002; FR-004; TC-005 |
| DEC-003 | 2026-08-03 | accepted | Product and Architecture | Describe MVP as graph-enhanced RAG and defer full GraphRAG entity and community pipelines | GraphRAG primary paper and official docs; RF-003 | Claim GraphRAG parity; remove graph; bounded typed relations | research.md; prfaq.md; delivery-spec.md | FR-005; AC-005; TC-006 |
| DEC-004 | 2026-08-03 | accepted | Maintainers | Reuse context-pack v4 and require the owning StepCard plus every critical anchor | RF-004; current prototype gap | Separate cache pack; optional anchors; v4 integration | delivery-spec.md; qa-readiness.md | FR-006; AC-006; TC-007 |
| DEC-005 | 2026-08-03 | accepted | Security | Treat all retrieved repository content as evidence_only and preserve instruction hierarchy | RF-005; OWASP and OpenAI security guidance | Trust local text; heuristic filtering only; authority labels and capability limits | business-context.md; qa.md | FR-008; AC-008; TC-010 |
| DEC-006 | 2026-08-03 | accepted | Architecture | Use repository-relative paths and content fingerprints with same-transaction replacement and stale removal | RF-001; RF-006; SQLite and Git contracts | Full rebuild only; mtime identity; semantic fingerprints | delivery-spec.md; test-cases.md | FR-003; FR-009; TC-003; TC-011 |
| DEC-007 | 2026-08-03 | accepted | Maintainers and QA | Gate packed mode at 100 percent mandatory-anchor recall and at least 15 percent estimated net savings; otherwise use direct_read | RF-004; RF-007; context-pack v4 policy | Best-effort packs; savings-only gate; strict recall and economics gate | qa-strategy.md; qa-readiness.md; delivery-handoff-review.md | FR-007; FR-010; AC-007; AC-010; TC-009; TC-013 |
