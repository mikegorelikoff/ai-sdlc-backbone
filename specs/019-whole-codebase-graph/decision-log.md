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
  at: "2026-08-03T20:05:54Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "decision-log.md"
  path: "specs/019-whole-codebase-graph/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-branching"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
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
    - "ai-sdlc-branching"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-002 | 2026-08-03 | Accepted | Harness Maintainers | Require exactly twelve Tree-sitter AST languages including Kotlin and Swift; any observed selected-language parse or grammar failure makes graph_complete false | Refinement DEC-002/003; AC-002/003; TC-005/008 | Fewer languages; heuristic fallback; partial completeness | requirements.md; design.md; test-cases.md | AC-002; AC-003; TC-005; TC-007; TC-008 |
| DEC-003 | 2026-08-03 | Accepted | Harness Maintainers | Pin the bundled tree-sitter-language-pack 0.13.0 line for offline graph mode on CPython 3.10-3.14 and require hash/ABI/license preflight before acceptance | Upstream bundled-wheel API and Python support; DEC-006; TC-001/023 | Latest downloader-based pack; twelve independent wheels; runtime download | design.md; requirements.md; parser-lock.toon | AC-008; TC-001; TC-002; TC-023 |
| DEC-004 | 2026-08-03 | Accepted | Harness Maintainers | Store file, chunk, symbol, occurrence, and hub nodes with stable qualified identities; use typed bounded edges and trace hubs instead of pairwise trace cliques | Baseline 275048 trace-id edges dominated 284243 total; SCIP and GraphRAG output models | Keep chunk graph; unbounded direct links; probabilistic resolution | design.md; tasks.md | AC-004; AC-005; TC-009; TC-011; TC-016 |
| DEC-005 | 2026-08-03 | Accepted | Harness Maintainers | Preserve direct files as authority and accept graph packs only when complete, fresh, bounded, anchor-complete, and at least 25 percent smaller; all portable machine contracts are TOON | Feature-018 context-pack/v4 gates; NFR-005/006; AC-007/008 | Graph as authority; alternate machine output; best-effort incomplete packs | requirements.md; design.md; qa.md | AC-007; AC-008; TC-017; TC-018; TC-019 |
| DEC-006 | 2026-08-03 | Accepted | Harness Maintainers | Supersede DEC-003 bundle choice with Tree-sitter 0.25.2 plus twelve separate pinned grammar wheels and per-file network-denied subprocess isolation | Full-corpus run reproduced exit -11 on valid docs/scripts/build_catalog.py with the bundled parser/runtime; separate Python grammar on 0.25.2 parsed 9619 nodes and the full corpus completed twice | Keep crash-prone bundle; parse in harness process; runtime downloads | requirements.md; design.md; parser-lock.toon; code_graph.py | AC-002; AC-003; AC-008; TC-001; TC-002; TC-021; TC-023 |
| DEC-008 | 2026-08-04 | Accepted | Harness Maintainers | Treat a clean protected CI runner as a release target: download exact versions, verify Linux wheel bytes against target-specific TOON locks, install offline, and prove all twelve grammars before graph-required tests | The v4.2.1 Python 3.10 and 3.13 jobs failed with parser-preflight-failed because no graph runtime was installed | Skip graph tests; install floating packages; hash-lock and offline-verify the complete runtime | parser-lock-linux-cp310.toon; parser-lock-linux-cp313.toon; skills-ci.yml | AC-008; TC-001; TC-023; T011 |
