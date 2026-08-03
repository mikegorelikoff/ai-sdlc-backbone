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
  at: "2026-08-03T19:26:36Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "decision-log.md"
  path: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
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
| DEC-001 | 2026-08-03 | accepted | Harness Maintainers | Stack feature 019 on feature 018 commit 31a8c80 | Whole-codebase graph depends on the production cache runtime | Rebase on main and duplicate runtime; stacked feature | discovery.md; implementation branch | AC-001; T001 |
| DEC-002 | 2026-08-03 | accepted | Product and Architecture | Support twelve AST languages in MVP | User selected ten popular languages and explicitly added Kotlin and Swift | All existing suffixes; ten languages; twelve languages | discovery.md; delivery-spec.md; parser policy | AC-002; TC-002 |
| DEC-003 | 2026-08-03 | accepted | Architecture | Require Tree-sitter AST for every selected language | Regex heuristics cannot prove symbol or reference coverage | Regex extraction; language servers; Tree-sitter | discovery.md; design.md; tests | AC-002; AC-003; TC-002; TC-003 |
| DEC-004 | 2026-08-03 | accepted | Product and Security | Keep unsupported languages searchable but mark them unsupported_ast | Whole-corpus retrieval must not fabricate code-graph completeness | Exclude unsupported code; heuristic graph; explicit status | discovery.md; coverage receipt | AC-001; AC-008; TC-009 |
| DEC-005 | 2026-08-03 | accepted | Architecture | Use stable file, chunk, and qualified-symbol identities with bounded relation fan-out | Current graph has 275048 trace-ID edges and needs bounded growth | Unbounded cliques; no trace edges; bounded hubs and typed relations | discovery.md; design.md | AC-004; AC-005; TC-005 |
| DEC-006 | 2026-08-03 | accepted | Security and Operations | Preinstall pinned parser runtime and grammars; runtime remains offline and optional | Production warm cannot download code or grammars | On-demand downloads; vendored binaries; optional pinned wheels | discovery.md; install tests; security review | AC-006; AC-008; TC-006 |
| DEC-007 | 2026-08-03 | accepted | QA | Require full AST coverage, deterministic recall, bounded graph size, and at least 25 percent accepted-pack savings | File coverage alone does not prove useful or economical code retrieval | Coverage only; latency gate; deterministic quality and savings | discovery.md; qa-strategy.md; validation.md | AC-007; TC-007; TC-010 |
