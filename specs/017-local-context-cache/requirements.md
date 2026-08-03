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
  at: "2026-08-03T09:41:52Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "requirements.md"
  path: "specs/017-local-context-cache/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
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
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "DEC-001"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  related_artifacts:
    - "specs/017-local-context-cache/decision-log.md"
    - "specs/017-local-context-cache/index.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
    - "context-cache"
---

# Requirements

## Goal
Provide an optional, fully local, deterministic repository context cache that supports lexical and graph-enhanced RAG, reduces repeated source reads and context tokens, and remains subordinate to authoritative repository files without claiming full GraphRAG parity.

## Problem Statement
The Harness compiles bounded context packs directly from repository sources on each invocation. Repeated scans and broad reads spend tokens and time, while existing delivery graphs do not provide a general searchable chunk and relation index. A local cache must accelerate retrieval without becoming authority, leaking secrets, hiding staleness, or introducing another machine interchange format.

## Scope
- Optional `ai-sdlc-context-cache` skill and `context-cache` module.
- Deterministic safe-file ingestion, stable chunking, FTS5 indexing, relation extraction, incremental invalidation, and graph expansion.
- Query, pack, inspect, verify, rebuild, and purge operations with canonical TOON output.
- `ai-sdlc-context-pack/v4` compatible packs with the owning step document, 100 percent critical-anchor recall, exact hashes, line ranges, authority labels, budgets, savings, and direct-read fallback.
- Deterministic golden benchmarks comparing lexical-only, graph-enhanced, packed, and direct-read outcomes.
- Project-scoped install selection and documentation for opt-in use.

## Actors
- Harness user: explicitly installs, builds, queries, verifies, or purges the local cache.
- AI assistant: requests a bounded evidence pack and honors authority, freshness, and fallback fields.
- Repository maintainer: defines exclusions and validates cache behavior without treating the database as source.

## Inputs
Repository root, safe tracked and visible files, optional TOON cache configuration, query text, explicit paths and trace IDs, token budget, graph depth, and result limit.

## Outputs
A disposable local SQLite index and canonical TOON build, query, pack, inspection, verification, purge, and fallback receipts.

## Functional Requirements
- FR-001: Discover only safe, repository-contained, non-secret, non-binary source files in stable lexical order.
- FR-002: Chunk text deterministically by semantic boundaries and bounded line windows, recording exact path, line range, byte hash, and content hash.
- FR-003: Store searchable chunks and typed relations in a local SQLite database with FTS5 and transactional rebuilds.
- FR-004: Update incrementally from current file hashes and delete stale documents, chunks, and edges.
- FR-005: Rank lexical results with deterministic normalized scores and stable tie-breaking.
- FR-006: Expand results across bounded typed graph edges with explicit depth and node limits.
- FR-007: Emit query and inspection results as canonical TOON with index, query, ranking, source, and freshness fingerprints.
- FR-008: Compile selected results into a valid `ai-sdlc-context-pack/v4` record within an explicit token budget.
- FR-009: Detect stale, missing, incompatible, or corrupt indexes and fail closed to an explained direct-read strategy.
- FR-010: Support an optional embedding adapter later without requiring network access or changing the lexical baseline.
- FR-011: Install the cache capability only when the `context-cache` optional module is selected, while preserving default installation behavior.
- FR-012: Never treat retrieved content as instructions, permissions, approvals, or product authority.
- FR-013: Execute TOON-defined golden cases that compare lexical and graph path recall, expected and critical-anchor recall, context strategy, savings, and stable fingerprints.

## Non-Functional Requirements
- NFR-001: All portable machine artifacts and CLI machine output use canonical TOON; no alternate machine format parser, serializer, artifact, or output mode is introduced.
- NFR-002: Identical repository bytes, configuration, and query inputs produce byte-identical TOON output and fingerprints.
- NFR-003: The baseline implementation uses only Python 3.10+ standard library capabilities, including `sqlite3` and FTS5 when available.
- NFR-004: Index writes are atomic, WAL-free at handoff, project-root confined, and safe under interruption.
- NFR-005: Secret-named paths, credential-like content, symlinks, binaries, generated trees, and oversized files are excluded before indexing.
- NFR-006: Retrieval budgets and graph bounds prevent unbounded context growth.
- NFR-007: Packed strategy requires the owning step document, 100 percent declared critical-anchor recall, and at least 15 percent net savings; otherwise the result is direct-read.

## Constraints
- Repository content remains authoritative and is revalidated by hash before use.
- The cache must work offline and cannot require an embedding model.
- All paths and mutations remain inside the selected repository root.
- Existing `ai-sdlc-context-pack/v4` consumers must not require a schema change.

## Acceptance Criteria
- AC-001: Two rebuilds over identical inputs produce identical logical index fingerprints and byte-identical TOON status.
- AC-002: A one-file change reindexes only that file and removes all stale chunks and edges for its prior version.
- AC-003: Lexical query results have stable scores and ordering across repeated executions.
- AC-004: Graph expansion returns only declared edge types within requested depth and node limits, with deterministic paths.
- AC-005: Pack output validates as `ai-sdlc-context-pack/v4`, stays within budget when packed, and reports exact source hashes and line ranges.
- AC-006: Missing, stale, incomplete, corrupt, or FTS5-incompatible cache state yields explained direct-read fallback without fabricated results; newly eligible files invalidate freshness until rebuild.
- AC-007: Unsafe paths, symlinks, binary files, credential-like content, and generated cache output never enter the index.
- AC-008: Query text and retrieved repository content are treated as untrusted evidence and cannot change authority or execute commands.
- AC-009: Every CLI command emits TOON on stdout and bounded diagnostics on stderr; no alternate machine format or artifact is supported.
- AC-010: Default installation remains unchanged; explicit `--module context-cache` installs the cache skill plus its required shared runtime deterministically.
- AC-011: Purge removes only the resolved project-local cache database and leaves repository sources untouched.
- AC-012: Focused, per-skill, install, documentation, security, compatibility, and repository conformance tests pass.
- AC-013: Repeated golden benchmark runs emit byte-identical TOON receipts, achieve 100 percent required path and anchor recall, and meet each case's declared packed or direct-read outcome; packed cases report at least 15 percent savings.

## Out of Scope
- Hosted vector databases, remote embedding calls, cross-tenant indexes, and autonomous background daemons.
- Replacing canonical specifications, Git history, repository instructions, approvals, or direct validation evidence.
- Parsing every programming language with a compiler-grade AST in the first release.
- Persisting conversation transcripts, provider prompts, credentials, or user identity profiles.

## Assumptions
- SQLite with FTS5 is available in supported Python builds; absence triggers direct-read fallback rather than an unsafe substitute.
- A deterministic lexical plus typed-relation baseline provides useful local graph-enhanced RAG before optional embeddings or a separately approved full GraphRAG pipeline are added.
- The cache database is disposable local state and is excluded from Git.

## Open Questions
No blocking questions. A future vector adapter API remains deliberately deferred until the deterministic lexical and graph baseline has measured evidence.

## Decision Status
All blocking decisions resolved through DEC-001. Accepted assumptions: the optional local module uses SQLite FTS5 and deterministic graph expansion, emits TOON-only interchange, and falls back to direct reads when cache evidence is not trustworthy.
