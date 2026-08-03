---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T20:58:03Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "design.md"
  path: "specs/019-whole-codebase-graph/design.md"
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
    - "TC-001"
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/branch-plan.md"
    - "specs/019-whole-codebase-graph/decision-log.md"
    - "specs/019-whole-codebase-graph/plan.md"
    - "specs/019-whole-codebase-graph/qa.md"
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/tasks.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
---

# Design

## Overview
Upgrade the feature-018 disposable projection to graph schema v2. Discovery classifies every safe file, parser preflight proves all grammars needed by the observed selected-language corpus, AST adapters emit canonical facts, graph construction links only bounded evidence-backed relations, and query/pack accepts graph evidence only after completeness, freshness, integrity, anchor, and economics gates.

## Architecture
The shared StepCard runtime remains the control plane and direct files remain authoritative. The optional context-cache process is a derived local projection. A candidate database is built or refreshed under the repository cache root, verified against source snapshots and policy bounds, then atomically replaces the accepted database. Parser loading is local-only and import-time network guards remain active.

## Components
context_cache.py retains CLI, lifecycle, FTS, packing, and observations. code_graph.py owns language classification, version preflight, isolated AST walking, canonical facts, qualified IDs, typed relation linking, hub construction, bounds, stats, and verification. language-policy.toon maps suffixes and twelve grammar keys. parser-lock.toon records Tree-sitter 0.25.2, twelve exact grammar packages including Kotlin and Swift, Python/target scope, macOS arm64 wheel filenames and SHA-256 values, licenses, and offline safety. Focused fixtures, install_graph_smoke.py, and release_graph_audit.py provide executable gates.

## Interfaces and Contracts
Commands build, warm, query, pack, verify, purge, observe, reset-observations, graph-preflight, graph-stats, and graph-audit emit TOON only. The graph receipt schema reports corpus accounting, required/available/parser-error language rows, graph_complete, node/edge counts by kind, max fan-out, configured bounds, source and graph fingerprints, incremental change counts, strategy, and reason. Existing context-pack/v4 remains unchanged and is accepted only with graph_complete yes when graph mode is requested.

## Data Model
SQLite v2 adds files, symbols, occurrences, graph_nodes, graph_edges, language_coverage, exclusions, and graph_metadata while retaining documents, chunks, FTS, and observations. IDs are SHA-256-derived from normalized repository path plus content identity, qualified symbol path/kind/name, occurrence role/range, or hub namespace/key. Edge uniqueness is source, target, kind, evidence range; every query orders by explicit stable keys. Spec traces target one hub per normalized trace ID rather than pairwise chunk edges.

## Error Handling
Missing package, incompatible Python/ABI, absent grammar, parser exception, error node above policy, invalid UTF-8, limit breach, unsafe path, source drift, mixed schema, integrity failure, stale fingerprint, timeout, incomplete recall, missing anchor, and poor savings are stable reason-coded failures. Candidate publication is discarded; a prior verified graph may remain stored but is not accepted when stale. Runtime returns direct_read without authority expansion.

## Security Considerations
Use only hash-locked preinstalled wheels and verify declared license/source metadata. Deny runtime network, dynamic library paths outside the installed distribution, SQLite extensions, symlink escape, secrets, oversized files, ignored trees, and cache self-ingestion. Treat source and parser output as untrusted evidence, bound AST depth/node count/text extraction, parameterize SQL, sanitize reasons, and never persist prompts, credentials, identity, or raw observation content.

## Observability
Deterministic stats expose safe/discovered/indexed/excluded counts, per-language files/parses/errors/grammar status, node and edge distributions, relation fan-out maxima, graph growth ratios, freshness, fingerprints, changed/retained/removed fact counts, recall, raw/packed tokens, and savings. Wall-clock timings are observational and excluded from canonical fingerprints and golden byte comparisons.

## Risks and Tradeoffs
Twelve independent grammar wheels increase lock maintenance but avoid runtime downloads and isolate grammar/runtime compatibility. The rejected bundled alternative reproduced a native Python parser crash during corpus audit; per-file subprocess isolation now converts any future native crash or timeout into graph-incomplete direct fallback. Generic policy-driven AST walking provides consistent structural coverage but deliberately under-resolves semantics. Strict completeness and economics lower hit rate but preserve correctness. Full graph relations are deterministically rebuilt after affected document updates, trading some refresh work for simpler verification while stable unaffected IDs remain unchanged.

## Validation Strategy
Implement and execute TC-001 through TC-024. Run parser lock/offline preflight, twelve language fixtures including Kotlin and Swift, parse-error/missing-grammar gates, deterministic clean builds, v1-to-v2 atomic migration, dense-graph bounds, incremental mutation/drift, golden recall/disambiguation/economics, fallback, stats, unsafe-input, full existing regression, docs/install smoke, security review, code review, and two-run real-corpus release audit.

## Migration Notes
Schema v1 cache files are disposable. Warm builds v2 in a candidate and atomically publishes only after verification; it never mutates v1 in place. Default/core installs and Python 3.9 continue feature-018 lexical/direct behavior. Graph installation is explicit, optional, and reversible by purging derived state or removing its locked environment.
