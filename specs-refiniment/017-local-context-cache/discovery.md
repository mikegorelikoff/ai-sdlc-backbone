---
type: "ai-sdlc.discovery"
title: "Working Backwards Discovery"
description: "Customer problem, audience, value, scope, and discovery evidence."
tags:
  - "ai-sdlc"
  - "discovery"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:11:28Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "discovery.md"
  path: "specs-refiniment/017-local-context-cache/discovery.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "PM"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-010"
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/decision-log.md"
    - "specs-refiniment/017-local-context-cache/index.md"
    - "specs-refiniment/017-local-context-cache/research.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "discovery"
    - "review"
---

# discovery.md

## Feature Summary
AI SDLC Harness maintainers and repository contributors need an optional local retrieval layer that reduces repeated broad reads while preserving deterministic skill execution. The MVP installs only on explicit module opt-in and provides local lexical search, typed relation expansion, context-pack assembly, inspection, verification, benchmarking, and safe direct-read fallback. It is graph-enhanced RAG, not a claim of full LLM-extracted GraphRAG parity.

## Actors and Stakeholders
Primary users are repository contributors and AI agents running installed skills. Maintainers own module compatibility and release gates; QA owns deterministic retrieval and context-economics evidence; Architecture owns future embedding or provider-backed GraphRAG adapters; Security owns authority and untrusted-content boundaries. No remote service or external data processor is required by the MVP.

## Scope and Boundaries
In scope are an opt-in context-cache module, SQLite FTS5 lexical retrieval, deterministic line chunks with document and heading context, typed repository relations, bounded expansion, TOON receipts, context-pack v4 integration, incremental rebuilds, integrity verification, benchmarks, documentation, and installer coverage. Out of scope are mandatory installation, hidden network calls, alternate machine format interchange, autonomous authorization, vector-provider lock-in, LLM entity extraction, community summaries, and global GraphRAG search.

## Workflows and Failure Paths
A user opts into the module, builds or refreshes the index, queries or requests a context pack, and receives ranked evidence with source paths, hashes, authority labels, and stable fingerprints. Changed and deleted files update transactionally. Unsupported FTS5, stale fingerprints, corrupt indexes, missing StepCards, incomplete critical-anchor recall, poor token economics, unsafe paths, or insufficient evidence produce a TOON failure receipt and direct-read recovery instead of partial context.

## Requirements and Business Rules
FR-001 through FR-010 define optional installation, deterministic discovery and indexing, lexical and graph retrieval, v4 context assembly, authority preservation, safe fallback, verification, and evaluation. BR-001 forbids alternate machine format contracts; BR-002 treats retrieved content as evidence only; BR-003 requires the owning StepCard and all critical anchors; BR-004 requires deterministic ordering and stable tie-breaks; BR-005 forbids release claims without benchmark evidence.

## Data, Integrations, and Non-Functional Requirements
The local SQLite database stores repository-relative document metadata, content fingerprints, deterministic chunks, FTS rows, and typed edges. Inputs are repository files, Git metadata when available, skill StepCards, trace IDs, and query constraints. NFRs require offline operation, same-transaction index consistency, deterministic output, bounded traversal, no secret indexing, 100 percent critical-anchor recall, at least 15 percent net savings for packed mode, and TOON-only portable receipts.

## Dependencies, Risks, and Constraints
The MVP depends on Python standard-library SQLite with FTS5, the shared context-pack v4 contract, module-aware installation, Git-aware discovery, and existing TOON codecs. Main risks are stale or inconsistent indexes, lexical recall gaps, overclaiming GraphRAG, prompt injection in repository text, excessive index cost, and misleading token-savings estimates. Each risk has a deterministic fallback, verification check, benchmark, owner, and release gate.

## Decisions, Assumptions, and Open Questions
DEC-001 selects an optional SQLite FTS5 module. DEC-002 selects contextual lexical retrieval as the offline baseline. DEC-003 names the MVP graph-enhanced RAG and defers full GraphRAG. DEC-004 integrates with context-pack v4 and direct-read fallback. DEC-005 preserves instruction hierarchy. DEC-006 defines incremental fingerprinted indexing. DEC-007 sets 100 percent mandatory-anchor recall and a 15 percent net-savings packed-mode threshold. OQ-002 owner is Architecture; impact is limited to post-MVP semantic recall; next step is a provider-neutral adapter evaluation. OQ-003 owner is Product and Architecture; impact is limited to future global search; resolution is deferred until MVP benchmark evidence exists.

## Success Measures
The release gate requires deterministic repeated outputs and fingerprints, 100 percent mandatory StepCard and critical-anchor recall, no unsafe or excluded file ingestion, successful stale and corruption recovery, stable module installation, and passing golden queries for exact IDs, cross-file relations, and failure paths. Packed mode must show at least 15 percent estimated net token savings; otherwise the expected successful result is explicit direct_read. Live-model quality evaluation remains optional and separate.

## Source Coverage
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/research.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Customer and Problem Evidence
Confirmed user direction asks for a custom local cache that behaves like RAG or GraphRAG, saves request tokens, and searches repository knowledge. Current direct reading is authoritative but repeatedly reloads broad files and reconstructs relationships, increasing context cost and inconsistency. Research RF-001 through RF-007 confirms a portable lexical baseline, graph-enhanced positioning, context-pack integration, security boundaries, and the need for deterministic evaluation.

## Current Process and Alternatives
Today skills select direct files and build context packs from repository evidence; repeated sessions may reread the same content and recompute topology. Alternatives are direct_read only, an external vector database, provider-managed file search, or full Microsoft-style GraphRAG indexing. Direct reading remains fallback; external services violate the local optional baseline; full GraphRAG adds LLM indexing cost and complexity before local value is measured.

## Value Proposition and Business Goals
For harness contributors and agents who repeatedly inspect the same repository evidence, the optional module finds exact identifiers and related files locally, then produces a bounded v4-compatible pack so they can spend context on decisions rather than rediscovery. GOAL-001 is reliable context reduction without correctness loss; GOAL-002 is deterministic offline retrieval; GOAL-003 is safe optional adoption without changing the default installation.

## Users, Roles, and Scenarios
Contributors build, refresh, query, pack, inspect, verify, benchmark, and purge a project-local cache. Agents consume only validated evidence packs and never gain authority from retrieved content. Maintainers validate compatibility and docs. QA executes golden cases and regression suites. Architecture evaluates later embedding and full GraphRAG adapters only after the lexical baseline is measured.

## MVP and Priorities
Must have: opt-in install, safe discovery, transactional incremental FTS5 index, contextual chunks, deterministic lexical ranking, bounded typed-relation expansion, StepCard and critical-anchor preservation, TOON receipts, inspect/verify/purge, direct-read fallback, and benchmark gates. Should have: changed-path narrowing and richer repository relations. Could have later: local embeddings and reranking. Won't have now: remote indexing, mandatory cache, LLM entity/community extraction, or global GraphRAG.

## Functional and Non-Functional Needs
Functional needs map to FR-001 through FR-010 and AC-001 through AC-010. The system must expose build, query, pack, inspect, verify, benchmark, and purge operations; update only changed content; remove stale rows; and explain selection and skips. Non-functional needs include offline portability, deterministic tie-breaks and fingerprints, bounded cost, same-transaction consistency, secret and symlink exclusion, authority labels, and context-economics measurement.

## Operations, Launch, and Support
The module is enabled with an explicit installer flag and stores its disposable database under the project-local ignored cache path. Documentation covers build, verify, query, pack, benchmark, fallback, and purge. Release is blocked until module install smoke tests, deterministic unit and integration tests, docs validation, compatibility checks, and golden benchmark receipts pass. Recovery is rebuild or purge; direct_read remains available throughout.

## Discovery Risks and Dependencies
SQLite builds without FTS5, malformed repository files, stale content, injection-shaped text, large generated trees, weak lexical recall, and graph fan-out are the major risks. Capability detection, exclusions, hashes, bounded traversal, evidence-only authority, stable ordering, benchmark thresholds, and direct_read mitigate them. The shared TOON codec, context-pack v4, Git metadata, and module installer are required dependencies.
