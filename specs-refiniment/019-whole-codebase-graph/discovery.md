---
type: "ai-sdlc.discovery"
title: "Working Backwards Discovery"
description: "Customer problem, audience, value, scope, and discovery evidence."
tags:
  - "ai-sdlc"
  - "discovery"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:37:02Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "discovery.md"
  path: "specs-refiniment/019-whole-codebase-graph/discovery.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "discovery"
    - "approved"
    - "whole-codebase-graph"
---

# discovery.md

## Feature Summary
- Confirmed facts: Feature 019 upgrades the local cache from a mostly chunk-level evidence graph into a bounded heterogeneous code graph for twelve languages. Every safe source file remains searchable, while supported code receives AST-derived file, symbol, definition, reference, import, and containment structure.
- Evidence: The current repository build indexed 1264 of 1268 safe text candidates into 3040 chunks and 284243 edges, but only 282 import edges existed and 275048 trace-ID edges dominated the graph. The user explicitly requires AST parsing and added Kotlin and Swift to the initial ten-language set.
- Open questions/blockers: None for discovery. The implementation must verify and pin the complete twelve-grammar bundle for offline installation before release.

## Actors and Stakeholders
- Confirmed facts: AI coding agents and developers are primary users. Harness maintainers own graph contracts and parser packaging; repository maintainers own source policy; QA owns coverage, freshness, retrieval, and economics gates; Security owns source exclusion and dependency review.
- Evidence: Feature 018 already places cache acceptance inside ordinary StepCard compilation and assigns maintainers, QA, and Security to the corresponding runtime boundaries.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: MVP languages are TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift. Their recognized source suffixes must parse through a pinned Tree-sitter grammar before graph-complete status. Safe Git-visible docs, specs, and configs remain document and chunk nodes. Binary, vendor, generated, ignored, oversized, symlinked, path-escaping, and secret-like inputs remain excluded.
- Evidence: The initial ten-language list followed current popularity and existing suffix support; the user explicitly added Kotlin and Swift. Tree-sitter provides incremental concrete syntax trees and maintained parsers for all twelve.
- Open questions/blockers: No product blocker. Grammar versions and wheel hashes are an implementation decision that must be pinned.

## Workflows and Failure Paths
- Confirmed facts: WF-001 warm discovers the safe corpus, classifies languages, parses every supported code file, extracts deterministic nodes and edges, rechecks sources, and atomically publishes. WF-002 query selects lexical seeds, expands through bounded typed graph edges, ranks stable evidence, and packs within the StepCard budget. WF-003 incremental warm reparses only changed code and rebuilds affected relations. WF-004 any missing parser, AST error above tolerance, stale source, corrupt cache, timeout, or coverage gap returns an explicit direct-read path and reason.
- Evidence: Existing warm, freshness, atomic replacement, query, pack, and direct-read paths provide the lifecycle skeleton.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: FR-001 index every safe eligible repository file as a file node. FR-002 parse all selected-language files with pinned Tree-sitter AST. FR-003 create stable file, chunk, and symbol identities. FR-004 create contains, defines, references, imports, calls when provable, path-reference, test-target, spec-trace, and adjacent-chunk edges. FR-005 bound fan-out and remove trace cliques. FR-006 expose TOON coverage and graph statistics. FR-007 query and pack use typed graph paths. FR-008 preserve direct-read authority and feature 018 safety.
- Evidence: Baseline shows broad document coverage but missing symbol intelligence and pathological trace-edge dominance.
- Open questions/blockers: None.

### Acceptance Criteria
- AC-001: Every safe eligible repository file has a deterministic file node or explicit exclusion reason.
- AC-002: TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift fixtures parse through the pinned Tree-sitter bundle.
- AC-003: Graph-complete is false when any selected-language file lacks a successful AST; heuristic extraction never claims completeness.
- AC-004: Stable file, chunk, symbol, and occurrence identifiers plus deterministic ordering yield byte-identical fingerprints for identical inputs.
- AC-005: Every relation obeys declared per-node fan-out and total edge bounds; repeated trace IDs use bounded hubs instead of cliques.
- AC-006: Warm and query make no network calls and a missing or incompatible grammar produces an explicit TOON reason and direct-read fallback.
- AC-007: Golden queries achieve 100 percent expected path and symbol recall and accepted packs save at least 25 percent tokens.
- AC-008: Unsupported safe text remains searchable with unsupported_ast status; stale, partial, unsafe, or corrupt graph evidence is never accepted.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite remains local derived storage. Portable policies, stats, query results, benchmarks, and receipts remain TOON only. Parser grammars must be installed ahead of runtime use; warm and query perform no network calls. Node and edge ordering, identifiers, fingerprints, query ranking, and coverage receipts must be byte-stable for identical inputs.
- Evidence: Existing cache already uses rollback journal, atomic replacement, FTS5, stable hashes, TOON output, and no network path.
- Open questions/blockers: Exact optional-module packaging must keep default installation unchanged.

## Dependencies, Risks, and Constraints
- Confirmed facts: Dependencies are feature 018 commit 31a8c80, Python, SQLite FTS5 for cached retrieval, Tree-sitter runtime, twelve pinned grammars, and shared TOON and StepCard contracts. Principal risks are grammar ABI drift, wheel availability, AST error recovery, graph explosion, false reference edges, installation size, and token regression.
- Evidence: Official Tree-sitter bindings use separately installed language implementations; current trace-ID clique demonstrates why fan-out limits are mandatory.
- Open questions/blockers: Parser distribution for all twelve languages must be proven on supported installation targets before release.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 stack feature 019 on completed feature 018. DEC-002 support exactly twelve AST languages in MVP after the explicit Kotlin and Swift addition. DEC-003 use Tree-sitter for every selected language; no regex fallback may claim AST completeness. DEC-004 unsupported languages remain searchable evidence with explicit unsupported_ast status. DEC-005 use stable content and qualified-symbol identities with bounded edges. DEC-006 keep runtime offline and optional. DEC-007 require measurable token savings and full coverage receipts.
- Evidence: The user requires AST for every selected language and explicitly expanded the initial ten with Kotlin and Swift.
- Open questions/blockers: None. The accepted list is TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift.

## Success Measures
- Confirmed facts: SM-001 100 percent of safe eligible files appear as file nodes or explicit exclusions. SM-002 100 percent of safe selected-language files have successful AST coverage or the cache is not graph-complete. SM-003 zero stale accepted nodes after mutation. SM-004 graph edge count remains within declared per-relation fan-out and total bounds. SM-005 golden expected-path and expected-symbol recall is 100 percent. SM-006 accepted packs save at least 25 percent tokens. SM-007 identical inputs produce identical graph and receipt fingerprints.
- Evidence: Existing gates already prove source freshness and pack economics; feature 019 extends them to code-graph completeness.
- Open questions/blockers: Latency remains observational and is not part of deterministic fingerprints.

## Source Coverage
- Confirmed facts: Consumed the user requirement; docs/how-to/use-local-context-cache.md; specs-refiniment/018-context-cache-runtime/delivery-spec.md; specs/018-context-cache-runtime/validation.md; skills/ai-sdlc-context-cache/scripts/context_cache.py; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; repository baseline measurements; official Tree-sitter, SCIP, Microsoft GraphRAG, and GitHub Octoverse sources.
- Evidence: Baseline measured 1268 candidates, 1264 indexed documents, 3040 chunks, 284243 edges, 204 Python files, 914 Python chunks, 282 import edges, and 275048 trace-ID edges.
- Open questions/blockers: None.

## Customer and Problem Evidence
- Confirmed facts: The primary customer is a developer or AI coding agent repeatedly exploring a medium or large repository. The problem is repeated broad reading and grep-style discovery that spends tokens without reliable symbol, definition, reference, or dependency structure.
- Evidence: The user explicitly wants the whole supported codebase in a graph for faster search and token savings. Current measurements prove that file coverage alone does not provide code intelligence.
- Open questions/blockers: None.

## Current Process and Alternatives
- Confirmed facts: Today agents use direct reads, lexical FTS5 seeds, chunk adjacency, trace IDs, imports, and literal path references. Alternatives are repeated grep and file reads, external remote code search, full LLM GraphRAG extraction, language-server or SCIP indexes, or a local Tree-sitter graph.
- Evidence: Sourcegraph distinguishes search-based navigation from precise symbol indexes; Microsoft GraphRAG separates documents, text units, entities, and relationships.
- Open questions/blockers: None. The local Tree-sitter option best preserves offline deterministic operation.

## Value Proposition and Business Goals
- Confirmed facts: For developers and agents who repeatedly explore repositories, the feature provides a fresh local code graph so they can find definitions, related symbols, dependencies, tests, and specifications with less context, unlike repeated broad reads or a chunk graph without code structure. The business goal is lower token cost and faster evidence discovery without weakening authority.
- Evidence: The requested outcome is faster search and savings; feature 018 already establishes safe pack acceptance and observation totals.
- Open questions/blockers: None.

## Users, Roles, and Scenarios
- Confirmed facts: Agents query concepts or symbols during StepCard execution; developers run graph inspection for navigation and impact analysis; maintainers warm, verify, diagnose coverage, and purge; QA runs golden coverage and economics cases; Security audits exclusions and parser supply chain. Negative scenarios include unsupported suffix, missing grammar, parse error, source drift, excessive fan-out, corruption, and low savings.
- Evidence: These roles extend the accepted feature 018 operational model.
- Open questions/blockers: None.

## MVP and Priorities
- Confirmed facts: Must-have: twelve-language Tree-sitter AST, complete file inventory, stable symbols, typed bounded edges, incremental rebuild, graph stats, symbol-aware query, direct fallback, TOON receipts, tests, docs, and benchmarks. Should-have: call edges only when syntax proves a local target and test-to-source relations. Could-have: optional SCIP import. Won't-have now: remote embeddings, LLM entity extraction, daemon, community summaries, cross-repository graph, or language-server processes.
- Evidence: The user selected ten popular languages and then explicitly added Kotlin and Swift.
- Open questions/blockers: None.

## Functional and Non-Functional Needs
- Confirmed facts: Functional needs are language detection, parser availability validation, AST traversal, symbol extraction, occurrence linking, graph persistence, bounded traversal, coverage inspection, incremental invalidation, and StepCard integration. Non-functional needs are determinism, offline operation, fail-closed completeness, atomic publication, privacy, path confinement, bounded memory and edge count, optional installation, and no default-flow regression.
- Evidence: Feature 018 supplies the lifecycle controls; Tree-sitter and SCIP guidance supply the parser and symbol-index model.
- Open questions/blockers: None.

## Operations, Launch, and Support
- Confirmed facts: Launch stays opt-in through the context-cache module. Installation must preinstall the parser runtime and all twelve grammars so production warm never downloads. Operators receive warm, verify, graph-stats, query, benchmark, observations, reset, and purge commands with TOON output. Rollback removes derived state or disables policy and restores direct reads.
- Evidence: Existing module installation and direct-read fallback are established production controls.
- Open questions/blockers: Supported platform wheel validation for the twelve-grammar bundle is required in the install smoke suite.

## Discovery Risks and Dependencies
- Confirmed facts: P0 risks are incomplete AST coverage silently accepted, supply-chain or ABI mismatch, stale publication, graph explosion, authority escalation, and secret ingestion. P1 risks are installation size, parser-specific extraction variance, irrelevant expansions, and insufficient savings. Owners are Harness Maintainers, Security, and QA.
- Evidence: Current trace-ID clique and separate grammar distribution requirements make boundedness and packaging first-class release gates.
- Open questions/blockers: None; every P0 risk has a required design or test gate.
