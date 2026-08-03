---
type: "ai-sdlc.delivery-gap-review"
title: "Delivery Package Gap Review"
description: "Delivery gaps, contradictions, blockers, and readiness findings."
tags:
  - "ai-sdlc"
  - "review"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:35:52Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "delivery-gap-review.md"
  path: "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-package-gap-review"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "BR-001"
    - "BR-007"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-delivery-package-gap-review"
    - "delivery-gap-review"
    - "approved"
---

# delivery-gap-review.md

## Feature Summary
- Confirmed facts: Feature 019 turns the existing local context cache into a deterministic heterogeneous code graph while preserving safe whole-corpus lexical retrieval. The graph-complete contract covers TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift through Tree-sitter ASTs.
- Evidence: discovery.md Feature Summary and prfaq.md Press Release; baseline indexed 1264 documents and 3040 chunks but exposed only 282 import edges while 275048 trace-ID edges dominated.
- Open questions/blockers: No product blocker. Parser packaging remains an implementation and release verification gate.

## Actors and Stakeholders
- Confirmed facts: Developers and AI coding agents consume symbol-aware retrieval. Harness maintainers own schema, parsers, and release packaging; repository maintainers own source policy; QA owns coverage, determinism, recall, and economics; Security owns exclusions and dependency review.
- Evidence: discovery.md and prfaq.md Actors and Stakeholders.
- Open questions/blockers: None; ownership is sufficient for decomposition.

## Scope and Boundaries
- Confirmed facts: MVP includes safe-file inventory, AST extraction for exactly twelve selected languages, file/chunk/symbol/occurrence nodes, typed bounded relations, incremental refresh, graph stats, query and pack integration, direct-read fallback, TOON receipts, tests, documentation, and install smoke. Unsupported safe text remains searchable with unsupported_ast status. Remote services, runtime grammar downloads, LLM extraction, and heuristic AST-completeness claims are excluded.
- Evidence: DEC-002 through DEC-006; discovery.md Scope and Boundaries and MVP and Priorities.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: WF-001 atomically warms a complete graph; WF-002 combines lexical seeds with bounded typed traversal; WF-003 reparses changed files and invalidates removed facts; WF-004 rejects graph acceptance on missing grammar, parse failure, stale source, corrupt database, fan-out breach, or timeout and falls back to direct reads.
- Evidence: discovery.md WF-001 through WF-004 and prfaq.md Workflows and Failure Paths.
- Open questions/blockers: None; retry, rejection, fallback, and rollback behavior are explicit.

## Requirements and Business Rules
- Confirmed facts: Every safe eligible file is accounted for; every selected-language file must parse before graph-complete; IDs, ordering, ranking, and fingerprints are deterministic; relation fan-out is bounded; stale or partial graphs are not accepted; runtime is offline; portable machine contracts are TOON only.
- Evidence: BR-001 through BR-007, FR-001 through FR-008, and DEC-003 through DEC-007.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite is local derived storage; Tree-sitter supplies concrete syntax trees; pinned grammar packages are installed before runtime; StepCard integration remains optional and fail-open to safe direct reads. Identical inputs must yield byte-stable graph and receipt fingerprints.
- Evidence: discovery.md Data, Integrations, and Non-Functional Requirements; feature 018 runtime contract.
- Open questions/blockers: Exact pinned package versions and hashes are intentionally deferred to implementation evidence and must not be guessed in refinement.

## Dependencies, Risks, and Constraints
- Confirmed facts: Feature 019 depends on feature 018 commit 31a8c80, Python, SQLite FTS5, Tree-sitter, twelve grammar implementations, TOON contracts, and supported-platform installation. P0 risks are incomplete AST coverage, grammar ABI drift, stale publication, graph explosion, secret ingestion, and silent fallback.
- Evidence: DEC-001, DEC-005, DEC-006, DEC-007; discovery.md Discovery Risks and Dependencies; prfaq.md Launch Risks.
- Open questions/blockers: No decomposition blocker. Release must block until parser availability and ABI checks pass for all twelve languages.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted. Kotlin and Swift are first-class required AST languages, not optional extensions. No material product assumption remains unresolved.
- Evidence: decision-log.md and user direction.
- Open questions/blockers: Parser version selection is an engineering choice constrained by offline, pinned, hash-verifiable installation and supported-platform smoke tests.

## Success Measures
- Confirmed facts: Required gates are 100 percent safe-file accounting, 100 percent selected-language AST coverage for graph-complete state, zero stale accepted nodes, bounded graph growth, 100 percent golden expected path and symbol recall, at least 25 percent accepted-pack token savings, and deterministic fingerprints.
- Evidence: SM-001 through SM-007 and DEC-007.
- Open questions/blockers: Latency is observational and does not weaken deterministic acceptance.

## Source Coverage
- Confirmed facts: Reviewed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; specs-refiniment/018-context-cache-runtime/delivery-spec.md; specs/018-context-cache-runtime/validation.md; skills/ai-sdlc-context-cache/scripts/context_cache.py; repository corpus baseline; and primary Tree-sitter, SCIP, GraphRAG, and GitHub language evidence cited upstream.
- Evidence: delivery_gap_scan.py reported current package sources, no additional next_reads, and zero gaps.
- Open questions/blockers: None.

## Evidence Reviewed
- Confirmed facts: The package defines actors, trigger, happy path, observable outcome, permission and acceptance rules, failure and rollback paths, MVP boundary, required dependencies, ownership, and measurable release gates.
- Evidence: WF-001 through WF-004; BR-001 through BR-007; DEC-001 through DEC-007; SM-001 through SM-007; deterministic full-flow scan fingerprint 74b883e22052cde9b6c64a66c309f3b8a966a424da6500c186e9b657028a21c4.
- Open questions/blockers: None.

## Gap Matrix
| Area | Gap | Evidence | Impact | Severity | Owner | Resolution |
| --- | --- | --- | --- | --- | --- | --- |
| Parser packaging | Exact versions, wheels, ABI compatibility, and hashes are not yet selected | DEC-006; launch risks | Could prevent full twelve-language installation | High, non-blocking for decomposition; blocking for release | Engineering and Security | Research, pin, hash, and exercise supported-platform install smoke during implementation |
| Parser semantics | Per-language definition and reference extraction rules require executable fixtures | DEC-003; DEC-007 | Incorrect symbol edges or false completeness | High, non-blocking for decomposition; blocking for graph-complete acceptance | Engineering and QA | Define language fixtures and require coverage receipts for all twelve languages |
| Performance | Latency target is observational | SM-006; discovery Success Measures | Does not affect correctness, but may affect usability | Low | Engineering | Benchmark and report without including wall time in deterministic fingerprints |

## Contradictions
- Confirmed facts: No contradiction exists between customer value, MVP, metrics, and scope. The earlier ten-language proposal was explicitly superseded by the accepted twelve-language scope adding Kotlin and Swift.
- Evidence: DEC-002 and updated discovery.md and prfaq.md.
- Open questions/blockers: None.

## Blocking Questions
- Confirmed facts: No unanswered actor, trigger, permission, MVP, data-source, failure-handling, or launch-dependency question blocks story or specification synthesis.
- Evidence: Full-flow deterministic scan returned gaps[0] and next_reads[0]; the upstream package explicitly assigns every release-sensitive unknown to an implementation gate.
- Open questions/blockers: None for decomposition. The release question is evidence-based: which pinned parser package set passes all supported-platform and ABI tests?

## Readiness Verdict
- Confirmed facts: GO for requirements readiness review and downstream decomposition. The package is specific enough to create requirements, stories, architecture, tests, and implementation tasks without inventing product behavior.
- Evidence: All mandatory gap-review dimensions are present; no blocking gap or contradiction was found; accepted decisions and measurable gates provide traceability.
- Open questions/blockers: GO is conditional only at release time on twelve-language parser packaging, AST fixture coverage, security review, boundedness, determinism, freshness, and token-economics evidence.
