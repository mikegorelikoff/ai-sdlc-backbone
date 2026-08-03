---
type: "ai-sdlc.commit-message"
title: "Commit Message"
description: "Validated Conventional Commit message for the whole-codebase AST graph."
tags:
  - "ai-sdlc"
  - "commit"
  - "whole-codebase-graph"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "commit-message.md"
  path: "specs/019-whole-codebase-graph/commit-message.md"
  workspace: "implementation"
  skill: "ai-sdlc-conventional-commit"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids:
    - "DEC-006"
    - "T001"
    - "T002"
    - "T003"
    - "T004"
    - "T005"
    - "T006"
    - "T007"
    - "T008"
    - "T009"
    - "T010"
  related_artifacts:
    - "specs/019-whole-codebase-graph/commit-readiness.md"
    - "specs/019-whole-codebase-graph/validation.md"
    - "specs/019-whole-codebase-graph/code-review.md"
    - "specs/019-whole-codebase-graph/security-review.md"
  validation:
    - "validate_commit_msg.py --full-flow --require-traceability"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-conventional-commit"
    - "commit-message"
    - "approved"
---

# Commit Message

````text
feat(context-cache): index whole codebase with AST graph

Business context

Reduce repeated broad repository reads by making code structure searchable in
the local context layer while preserving deterministic harness authority,
bounded context engineering, and safe direct-read recovery.

Implementation details

- parse TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust,
  Kotlin, and Swift with exact hash-locked Tree-sitter runtimes
- build stable file, chunk, symbol, occurrence, call, import, path, adjacency,
  and specification-trace relations in the atomic local cache lifecycle
- isolate parsers with time, environment, network, graph-size, and traversal
  bounds; reject incomplete ASTs and recover to authoritative direct reads
- integrate lexical and symbol seeds with deterministic typed graph expansion,
  TOON receipts, context economics, documentation, and release audits

Change flow

Safe corpus inventory -> pinned parser preflight -> isolated AST parsing ->
atomic graph publication -> lexical and symbol seeding -> bounded typed
traversal -> context v4 acceptance gates -> packed evidence or direct read

Mermaid diagram

```mermaid
flowchart LR
  S[Safe corpus] --> P[Pinned parser preflight]
  P --> A[Isolated AST parsing]
  A --> G[Atomic typed graph]
  G --> R[Bounded retrieval]
  R --> C[Context v4 gates]
  C -->|complete and economic| E[Packed evidence]
  C -->|failure or low savings| D[Direct read]
```

How to test

- run the 31 focused context-cache, language, graph, and retrieval tests
- run the offline hash-locked install smoke and two-build full-corpus audit
- run shared-runtime, documentation, refinement, SDD, and diff-hygiene gates
- verify the canonical TOON receipt against the finalized workspace

Validation

- 12/12 canonical validation commands passed
- 31/31 focused tests passed across all twelve language grammars
- 178/178 shared-runtime tests and 47/47 documentation tests passed
- full-corpus determinism, 100 percent critical recall, parser fault recovery,
  code review, and security review passed with no unresolved finding

Spec: specs/019-whole-codebase-graph
Task: T001, T002, T003, T004, T005, T006, T007, T008, T009, T010
Validation: specs/019-whole-codebase-graph/_ai_sdlc/validation-receipt.toon
````
