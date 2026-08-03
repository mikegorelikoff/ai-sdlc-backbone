---
type: "ai-sdlc.backlog-gap-review"
title: "Backlog Requirements Gap Review"
description: "Planning gaps and backlog-blocking ambiguity."
tags:
  - "ai-sdlc"
  - "review"
  - "backlog"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:03Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "backlog-gap-review.md"
  path: "specs-refiniment/017-local-context-cache/backlog-gap-review.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-requirements-gap-review"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "BA"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
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
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/decision-log.md"
    - "specs-refiniment/017-local-context-cache/delivery-gap-review.md"
    - "specs-refiniment/017-local-context-cache/discovery.md"
    - "specs-refiniment/017-local-context-cache/goal-capability-map.md"
    - "specs-refiniment/017-local-context-cache/index.md"
    - "specs-refiniment/017-local-context-cache/prfaq.md"
    - "specs-refiniment/017-local-context-cache/requirements-readiness.md"
    - "specs-refiniment/017-local-context-cache/research.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-backlog-requirements-gap-review"
    - "backlog-gap-review"
    - "review"
---

# backlog-gap-review.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Planning Evidence
The planning package includes research findings RF-001 through RF-007, accepted decisions DEC-001 through DEC-007, explicit actors, workflows, requirements, acceptance targets, failure paths, dependencies, MVP and non-goals. The default 45-skill install boundary and optional 46th skill behavior are measurable. No external date, capacity, vendor, or remote-service assumption is required for logical sequencing.

## Gap Matrix
| Area | Gap | Evidence | Planning Impact | Severity | Owner |
| --- | --- | --- | --- | --- | --- |
| Context pack | Prototype omits mandatory StepCard and anchors | RF-004; current tests | Adds P0 correction before release | Blocker | Dev |
| Positioning | GraphRAG term overstates MVP | RF-003 | Requires consistent backlog and docs wording | High | PM and Documentation |

## Priority and Scope Gaps
No priority blocker remains. P0 work protects correctness and safety: transactional index, StepCard and anchors, authority labels, fallback, verification, and golden benchmarks. P1 improves relation coverage and diagnostics. P2 roadmap items include embeddings, reranking, and provider-backed GraphRAG. Full GraphRAG and remote services are explicitly excluded from the MVP.

## Dependency Gaps
Required dependencies have owners and validation paths: SQLite FTS5 capability detection, shared TOON codec, context-pack v4, module installer, Git-aware discovery, and deterministic test fixtures. No missing third-party account or service blocks implementation. Host SQLite without FTS5 blocks module activation and produces guidance to use direct_read or a supported runtime.

## Planning Verdict
Ready for backlog decomposition. Goals, roles, MVP, business rules, dependency order, risk drivers, and acceptance thresholds are concrete enough to split work without inventing behavior. Dates and capacity are intentionally absent; release planning uses dependency and evidence sequencing rather than fabricated sprint commitments.
