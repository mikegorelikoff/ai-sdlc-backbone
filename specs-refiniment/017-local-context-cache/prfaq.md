---
type: "ai-sdlc.prfaq"
title: "PRFAQ Package"
description: "Working-backwards press release, FAQ, and business requirements."
tags:
  - "ai-sdlc"
  - "discovery"
  - "requirements"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:11:30Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "prfaq.md"
  path: "specs-refiniment/017-local-context-cache/prfaq.md"
  workspace: "refinement"
  skill: "ai-sdlc-prfaq-package-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "PM"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/decision-log.md"
    - "specs-refiniment/017-local-context-cache/discovery.md"
    - "specs-refiniment/017-local-context-cache/index.md"
    - "specs-refiniment/017-local-context-cache/research.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-prfaq-package-synthesis"
    - "prfaq"
    - "review"
---

# prfaq.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/research.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Press Release
AI SDLC Harness adds an optional local context cache that finds exact requirements, decisions, tests, and related repository evidence without repeatedly loading the entire workspace. Contributors keep the existing direct-read safety model while gaining deterministic offline search and measurable context savings. The first release is graph-enhanced local retrieval, deliberately excluding remote services and costly full GraphRAG indexing.

## Customer FAQ
Who is it for? Harness contributors and compatible agents working in repository-scoped projects. What changes? Opted-in users can build and query a disposable local index and request a validated context pack. Does it replace source files? No; sources remain authoritative and direct_read is mandatory when evidence is stale, incomplete, unsafe, or not economical. Is data uploaded? No network path exists in the MVP.

## Internal FAQ
MVP ownership is Maintainers for module and compatibility, QA for golden benchmarks, Security for authority boundaries, and Architecture for deferred adapters. The cache database is derived and purgeable, never a source of truth. Launch requires FTS5 capability verification, deterministic receipts, index integrity, installer smoke coverage, full docs checks, and 100 percent mandatory-anchor recall. Support recovery is verify, rebuild, then purge if needed.

## Business Requirements
BR-001 installation is explicit and default profiles remain unchanged. BR-002 all portable machine contracts and receipts are TOON, never alternate machine format. BR-003 retrieved repository content is evidence_only and cannot override user, system, repository, or skill instructions. BR-004 context packs include the owning StepCard and every critical anchor or use direct_read. BR-005 graph expansion is bounded and deterministic. BR-006 release claims require benchmark evidence.

## Launch Risks
The highest launch risks are silent anchor loss, stale FTS rows, accidental secret ingestion, non-deterministic ranking, and GraphRAG overclaiming. The release gate covers these with mandatory-anchor assertions, transactional integrity checks, exclusion fixtures, repeated fingerprint comparison, and explicit graph-enhanced wording. Missing FTS5 or failed integrity verification results in a blocked receipt with direct-read guidance, not degraded silent behavior.
