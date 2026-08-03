---
type: "ai-sdlc.prfaq"
title: "PRFAQ Package"
description: "Working-backwards press release, FAQ, and business requirements."
tags:
  - "ai-sdlc"
  - "discovery"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:31:28Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "prfaq.md"
  path: "specs-refiniment/019-whole-codebase-graph/prfaq.md"
  workspace: "refinement"
  skill: "ai-sdlc-prfaq-package-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "WF-001"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-prfaq-package-synthesis"
    - "prfaq"
    - "approved"
    - "whole-codebase-graph"
---

# prfaq.md

## Feature Summary
- Confirmed facts: Feature 019 adds an offline heterogeneous code graph to the optional context cache. Twelve selected languages receive Tree-sitter AST-derived symbol and relationship structure; the full safe repository corpus remains searchable and provenance-linked.
- Evidence: discovery.md captures the measured graph gap, accepted language scope, workflows, and success gates.
- Open questions/blockers: None.

## Actors and Stakeholders
- Confirmed facts: Developers and AI coding agents consume graph results. Harness maintainers own implementation and parser packaging; repository maintainers own source policy; QA owns deterministic coverage and economics; Security owns exclusions and dependency review.
- Evidence: discovery.md Actors and Stakeholders.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: AST languages are TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift. Other safe text remains document/chunk evidence with explicit unsupported_ast status. Remote services, model calls, daemons, cross-repository graphs, LLM entities, and community summaries are excluded.
- Evidence: DEC-002 through DEC-004.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: Warm performs complete inventory, AST parsing, deterministic extraction, bounded linking, source recheck, and atomic publish. Query combines lexical seeds with typed graph traversal and pack gates. Changed files reparse incrementally. Missing grammar, parse failure, stale state, corruption, excessive graph growth, timeout, or low savings returns explicit direct reads.
- Evidence: WF-001 through WF-004 in discovery.md.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: BR-001 every safe file has a file node or explicit exclusion. BR-002 every selected-language file must have a successful AST before graph-complete status. BR-003 identifiers and ordering are deterministic. BR-004 edge fan-out and totals are bounded. BR-005 derived content remains evidence-only. BR-006 no runtime network access. BR-007 incomplete or uneconomic graph context falls back to direct reads.
- Evidence: FR-001 through FR-008 and DEC-003 through DEC-007.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite stores disposable file, chunk, symbol, occurrence, and typed-edge projections plus FTS5 content. TOON is the only portable machine format. Pinned Tree-sitter runtime and twelve grammars are installation dependencies. Determinism, atomicity, path confinement, offline operation, bounded resource use, and incremental freshness are P0.
- Evidence: discovery.md Data, Integrations, and Non-Functional Requirements.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Feature 018 runtime, Python, SQLite, Tree-sitter, twelve grammar wheels, shared StepCard contracts, and supported-platform install smoke are required. Key risks are grammar ABI drift, parser availability, graph explosion, false links, source leakage, installation size, and token regression.
- Evidence: discovery.md and DEC-005 through DEC-007.
- Open questions/blockers: No product question; packaging validation is a release gate.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted. The feature is stacked on 018, supports twelve AST languages, forbids heuristic completeness claims, bounds relations, stays offline and optional, and requires at least 25 percent savings for accepted packs.
- Evidence: specs-refiniment/019-whole-codebase-graph/decision-log.md.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: 100 percent safe-file accounting; 100 percent selected-language AST coverage for graph-complete state; zero stale accepted nodes; bounded edge counts; 100 percent golden path and symbol recall; at least 25 percent accepted-pack savings; byte-stable fingerprints.
- Evidence: SM-001 through SM-007 in discovery.md.
- Open questions/blockers: Latency is observational only.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; feature 018 delivery and validation evidence; current cache code and guide; repository measurements; official Tree-sitter, GraphRAG, SCIP, and GitHub popularity sources.
- Evidence: Discovery Source Coverage and current state.
- Open questions/blockers: None.

## Press Release
- Confirmed facts: Headline: AI SDLC Harness turns the safe repository corpus into a fresh local code graph for faster, smaller agent context. Developers and agents can discover definitions, references, imports, tests, specifications, and related evidence across twelve popular languages without uploading source code or repeatedly reading broad file sets. The optional module builds an incremental Tree-sitter graph, proves coverage and freshness, and returns a bounded context pack only when it is complete and saves at least 25 percent tokens. Otherwise, the Harness names the authoritative direct-read paths. The MVP is local, offline, project-scoped, and includes no daemon, remote embeddings, or LLM extraction.
- Evidence: Validated discovery value proposition, MVP, and success measures.
- Open questions/blockers: None.

## Customer FAQ
- Confirmed facts: Who benefits? Developers and AI agents working repeatedly in medium or large repositories. What changes? Queries can follow AST-derived symbols and dependencies instead of relying only on lexical chunks. Is every file uploaded? No; processing and storage remain project-local. Which languages? TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift. What if parsing fails? The graph is marked incomplete and the request uses explicit direct reads. What is the limitation? Unsupported languages remain searchable text but do not claim symbol completeness.
- Evidence: Discovery customer, scope, workflow, and failure-path sections.
- Open questions/blockers: None.

## Internal FAQ
- Confirmed facts: MVP owns file inventory, AST extraction, stable symbol and occurrence nodes, bounded typed relations, incremental rebuild, stats, query, pack, tests, docs, and install support. Maintainers own parsers and graph schema; QA owns golden coverage and savings; Security owns supply chain and exclusions. Grammars are pinned and installed before runtime, so warm never downloads. Rollback disables the policy or purges derived state and restores feature 018 direct behavior.
- Evidence: DEC-002 through DEC-007 and Operations, Launch, and Support.
- Open questions/blockers: None.

## Business Requirements
- Confirmed facts: BRD-001 reduce repeated context reads through symbol-aware local retrieval. BRD-002 preserve authoritative source and StepCard behavior. BRD-003 cover the complete safe corpus and all twelve AST languages transparently. BRD-004 provide deterministic incremental state and coverage receipts. BRD-005 remain offline, private, optional, bounded, and recoverable. BRD-006 prove recall and at least 25 percent token savings before accepting packed context.
- Evidence: Requirements, business rules, and success measures in discovery.md.
- Open questions/blockers: None.

## Launch Risks
- Confirmed facts: Launch blocks on any missing selected grammar, unsupported platform wheel, ABI mismatch, incomplete AST accounting, stale node, unbounded relation, secret-path regression, default-install drift, or failed golden economics case. Warning-only risks are host latency and larger optional installation size. Rollback is direct-read policy or purge of derived state.
- Evidence: Discovery Risks and Dependencies plus DEC-006 and DEC-007.
- Open questions/blockers: None.
