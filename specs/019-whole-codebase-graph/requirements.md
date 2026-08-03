---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T20:58:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "requirements.md"
  path: "specs/019-whole-codebase-graph/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-003"
    - "DEC-006"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "TC-001"
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/branch-plan.md"
    - "specs/019-whole-codebase-graph/decision-log.md"
    - "specs/019-whole-codebase-graph/design.md"
    - "specs/019-whole-codebase-graph/plan.md"
    - "specs/019-whole-codebase-graph/qa.md"
    - "specs/019-whole-codebase-graph/tasks.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
---

# Requirements

## Goal
Build an optional, production-gated local code graph that accounts for the whole safe repository corpus and uses deterministic Tree-sitter AST facts for TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift to improve retrieval speed and reduce repeated context tokens without changing repository authority.

## Problem Statement
The feature-018 cache indexes text chunks and a small relation set, so trace-ID cliques dominate its graph and code navigation lacks symbols, occurrences, typed AST relations, completeness proof, and bounded graph economics. Agents must repeatedly read broad source sets even when the needed definition or reference neighborhood is local.

## Scope
Extend the optional context-cache module with pinned offline parser preflight, whole-safe-corpus classification, twelve-language AST extraction, stable file/chunk/symbol/occurrence/hub identities, bounded typed relations, atomic full and incremental refresh, symbol-aware retrieval, deterministic TOON diagnostics, golden fixtures, real-corpus economics, installer guidance, and fail-closed direct-read fallback.

## Actors
Agents and developers query and pack evidence. Repository maintainers install and warm the optional graph runtime. Harness maintainers own policy and compatibility. Engineering owns parser, schema, and retrieval implementation. QA and Security own deterministic, supply-chain, offline, safety, and production gates.

## Inputs
Safe repository files, path/exclusion policy, feature-018 cache state, strict graph-policy.toon, a hash-locked preinstalled Tree-sitter bundle, owning StepCard constraints, query text, mandatory anchors, and token budgets.

## Outputs
A disposable SQLite graph projection plus canonical TOON build, preflight, stats, verify, query, pack, fallback, benchmark, and release-audit receipts. Accepted packs remain ai-sdlc-context-pack/v4; every rejection returns authoritative direct_read paths and a stable reason.

## Functional Requirements
FR-001 account for every safe eligible file as indexed or explicitly excluded. FR-002 parse all selected-language files with pinned Tree-sitter grammars for exactly twelve languages, including Kotlin and Swift. FR-003 create stable file, chunk, qualified-symbol, occurrence, and hub IDs. FR-004 create typed contains, defines, references, imports, provable calls, path-reference, test-target, spec-trace, and adjacent relations. FR-005 bound fan-out and total graph growth and replace trace cliques with hubs. FR-006 emit deterministic TOON coverage, parser, graph, freshness, bounds, and fingerprint diagnostics. FR-007 combine lexical seeds, symbol matches, bounded typed traversal, and deterministic packing. FR-008 reject missing, stale, partial, unsafe, corrupt, timed-out, incomplete, or uneconomical graph evidence and preserve direct reads.

## Non-Functional Requirements
NFR-001 deterministic IDs, ordering, fingerprints, receipts, ranking, and repeatable builds. NFR-002 offline warm/query with no runtime parser download or SQLite extension loading. NFR-003 atomic publication, bounded work, safe incremental invalidation, and prior-valid-cache preservation. NFR-004 path confinement, unsafe-input exclusion, evidence-only authority, and no content leakage in observations. NFR-005 all portable machine contracts use TOON exclusively. NFR-006 accepted golden packs save at least 25 percent against direct-read baseline while retaining every critical anchor. NFR-007 graph mode requires CPython 3.10 through 3.14 on declared wheel targets; unsupported hosts retain feature-018 lexical/direct behavior.

## Constraints
The verified graph runtime is Tree-sitter 0.25.2 plus twelve independently pinned grammar wheels recorded with exact versions and current macOS arm64 CPython 3.11 SHA-256 values in parser-lock.toon. The initially considered bundled parser pack is rejected because full-corpus validation reproduced a native crash on valid Python under its selected runtime. Every parse is isolated in a bounded subprocess. No network access is permitted during preflight, warm, query, pack, verify, or audit. Regex and heuristics may assist unsupported-text discovery but may never emit AST-complete symbols or semantic edges. Kotlin and Swift have the same completeness gate as the other ten languages. Derived writes stay below .ai-sdlc/cache; portable machine contracts are TOON only.

## Acceptance Criteria
- AC-001 Pass when every safe eligible file is accounted and excluded inputs have stable reasons without leaked content.
- AC-002 Pass when all twelve languages produce expected AST definitions, occurrences, imports, and only provable relations, with Kotlin and Swift mandatory.
- AC-003 Pass when a missing grammar or selected-language parse error makes graph_complete false and prevents graph-backed acceptance.
- AC-004 Pass when clean builds yield stable heterogeneous IDs, typed records, canonical order, complete diagnostics, and equal fingerprints.
- AC-005 Pass when trace hubs eliminate pairwise trace cliques and configured per-relation and total bounds hold, while a bound breach rejects the graph.
- AC-006 Pass when full and incremental refresh never publish stale, partial, mixed-schema, or source-drifted state and preserve the prior valid graph.
- AC-007 Pass when golden queries achieve complete expected path/symbol recall and accepted packs preserve anchors with savings of at least 0.25.
- AC-008 Pass when parser install/offline, unsafe input, stale/corrupt/timeout fallback, default-install compatibility, security, validation, and release audits all pass before production_ready is yes.

## Out of Scope
Remote graph services, runtime grammar downloads, embeddings, LLM extraction, community detection, probabilistic entity resolution, unsupported-language AST claims, cross-repository indexes, source-of-truth replacement, daemon operation, and latency SLO claims.

## Assumptions
The optional graph environment can use CPython 3.10 or newer and install locked wheels before offline operation. Tree-sitter concrete syntax trees are sufficient for deterministic structural facts; cross-file semantic resolution is emitted only when exact local evidence proves it. SQLite FTS5 remains available or the runtime fails safely to direct reads.

## Open Questions
No blocking product or expected-behavior question remains. Deferred roadmap items are additional languages, embeddings, looser semantic resolution, extra wheel targets, and a future downloader-based parser pack. Owner: Harness Maintainers. Impact: none on feature-019 implementation; each item stays out of scope and cannot weaken offline or completeness gates. Resolution and next step: implement the accepted twelve-language locked design; raise a separate SDD before changing any deferred boundary.

## Decision Status
Resolved for implementation: exactly twelve mandatory AST languages; Tree-sitter only for completeness; unsupported safe text remains searchable as unsupported_ast; stable qualified identities and trace hubs; Tree-sitter 0.25.2 plus twelve hash-locked grammar wheels on the verified CPython 3.11 macOS arm64 target; per-file process isolation; TOON-only portable contracts; direct_read on every acceptance failure; and a 25 percent minimum accepted-pack saving. DEC-006 supersedes the crash-prone bundled-parser choice in DEC-003. Owner: Harness Maintainers. Release remains blocked until TC-001 through TC-024 and independent reviews pass.
