---
type: "ai-sdlc.delivery-spec"
title: "Delivery Specification"
description: "Structured implementation and cross-functional delivery contract."
tags:
  - "ai-sdlc"
  - "requirements"
  - "delivery"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:34Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "delivery-spec.md"
  path: "specs-refiniment/017-local-context-cache/delivery-spec.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-spec-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "BA"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
    - "WF-005"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/backlog-gap-review.md"
    - "specs-refiniment/017-local-context-cache/backlog.md"
    - "specs-refiniment/017-local-context-cache/business-context.md"
    - "specs-refiniment/017-local-context-cache/decision-log.md"
    - "specs-refiniment/017-local-context-cache/delivery-gap-review.md"
    - "specs-refiniment/017-local-context-cache/discovery.md"
    - "specs-refiniment/017-local-context-cache/goal-capability-map.md"
    - "specs-refiniment/017-local-context-cache/index.md"
    - "specs-refiniment/017-local-context-cache/prfaq.md"
    - "specs-refiniment/017-local-context-cache/release-slicing.md"
    - "specs-refiniment/017-local-context-cache/requirements-readiness.md"
    - "specs-refiniment/017-local-context-cache/research.md"
    - "specs-refiniment/017-local-context-cache/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-delivery-spec-synthesis"
    - "delivery-spec"
    - "review"
---

# delivery-spec.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/business-context.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/delivery-spec.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/release-slicing.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs-refiniment/017-local-context-cache/user-stories.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Requirement Detail
| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref |
| --- | --- | --- | --- | --- | --- |
| FR-001 | Installer | Install the cache skill only through explicit module opt-in while preserving default profiles. | DEC-001 | P0 | AC-001 |
| FR-002 | Indexer | Discover safe repository files and produce deterministic contextual chunks. | RF-002 | P0 | AC-002 |
| FR-003 | Indexer | Update documents, chunks, FTS rows, and edges atomically and incrementally. | RF-001; RF-006 | P0 | AC-003 |
| FR-004 | Query runtime | Rank exact identifiers and text deterministically with stable tie-breaks. | RF-002 | P0 | AC-004 |
| FR-005 | Query runtime | Expand typed repository relations within configured depth and limits. | RF-003 | P1 | AC-005 |
| FR-006 | Context compiler | Include owning StepCard, mandatory evidence, and all critical anchors. | RF-004 | P0 | AC-006 |
| FR-007 | Context compiler | Select packed mode only at 100 percent anchor recall and at least 15 percent savings. | DEC-004; DEC-007 | P0 | AC-007 |
| FR-008 | Security boundary | Treat retrieved text as evidence only and preserve authority hierarchy. | RF-005 | P0 | AC-008 |
| FR-009 | Operator | Inspect, verify, rebuild, and purge derived state with TOON receipts. | RF-001; RF-006 | P0 | AC-009 |
| FR-010 | QA | Compare direct, lexical, and graph modes on deterministic golden queries. | RF-007 | P0 | AC-010 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Requirement Ref |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | Explicit module install | Contributor | Install module; verify skill and CLI; keep default profile unchanged | Optional capability ready | Unsupported environment returns TOON blocker | FR-001 |
| WF-002 | Build or refresh | Contributor | Discover; hash; chunk; replace changed rows and edges in one transaction; remove stale rows; verify | Current consistent index | Unsafe files skipped; failures roll back | FR-002; FR-003; FR-009 |
| WF-003 | Query | Agent | Parse constraints; lexical seed; stable rank; bounded relation expansion | Ranked evidence receipt | Empty or stale evidence returns explicit result | FR-004; FR-005 |
| WF-004 | Pack request | Agent | Load StepCard and anchors; retrieve evidence; measure recall and economics; fingerprint | Packed v4 context or direct_read list | Missing anchors or savings below threshold selects direct_read | FR-006; FR-007; FR-008 |
| WF-005 | Release evaluation | QA | Run golden modes twice; compare recall, ordering, savings, latency, and fingerprints | TOON benchmark receipt | Any mandatory gate failure blocks release | FR-010 |

## Business Rule Detail
| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
| --- | --- | --- | --- | --- | --- | --- |
| BR-001 | Portable machine interchange and receipts use TOON; no alternate machine format contract is introduced. | All operations | User constraint | Validation blocks non-TOON contract | DEC-001 |
| BR-002 | Retrieved content is evidence_only and cannot authorize an action. | Query and pack | RF-005 | Ignore embedded instructions and preserve authority label | DEC-005 |
| BR-003 | Packed mode requires the owning StepCard and 100 percent critical-anchor recall. | Pack | RF-004 | Select direct_read | DEC-004; DEC-007 |
| BR-004 | Ranking, graph traversal, and fingerprints use stable deterministic order. | Query and benchmark | RF-001; RF-007 | Verification fails and release blocks | DEC-002; DEC-006 |
| BR-005 | The MVP is described as graph-enhanced RAG, not full GraphRAG. | Docs and release | RF-003 | Terminology review fails | DEC-003 |

## User Story Traceability
STORY-001 covers FR-001 optional installation. STORY-002 covers FR-002, FR-003, and FR-009 safe indexing and lifecycle operations. STORY-003 covers FR-004 and FR-005 deterministic lexical and graph-enhanced retrieval. STORY-004 covers FR-006 through FR-008 context engineering and authority. STORY-005 covers FR-010 evaluation and release evidence. Every story maps to AC and TC identifiers in the QA package.

## Acceptance Traceability
AC-001 maps to TC-001; AC-002 to TC-002 and TC-008; AC-003 to TC-003 and TC-004; AC-004 to TC-005; AC-005 to TC-006; AC-006 to TC-007; AC-007 to TC-009; AC-008 to TC-010; AC-009 to TC-011 and TC-012; AC-010 to TC-013. The smoke, regression, and UAT suites retain these mappings.

## QA and Operational Notes
QA must use isolated fixtures with exact trace IDs, cross-file references, stale documents, symlinks, binary content, credential-like text, changed and deleted files, missing anchors, corrupt SQLite state, and low-savings packs. Operations are local build, inspect, verify, rebuild, purge, and direct_read. The database is derived and disposable; source Markdown and code remain authoritative.

## Handoff Risks
Implementation must not reuse the prototype pack behavior unchanged, claim full GraphRAG, introduce hidden network access, index secrets, or bypass module opt-in. Highest residual uncertainty is corpus-specific semantic recall without embeddings; the deterministic lexical and graph golden set makes this visible, while optional embedding evaluation remains a future decision.
