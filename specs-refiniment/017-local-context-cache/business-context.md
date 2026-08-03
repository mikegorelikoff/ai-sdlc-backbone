---
type: "ai-sdlc.business-context"
title: "Business Context"
description: "Actors, workflows, rules, exceptions, and acceptance context."
tags:
  - "ai-sdlc"
  - "analysis"
  - "requirements"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "business-context.md"
  path: "specs-refiniment/017-local-context-cache/business-context.md"
  workspace: "refinement"
  skill: "ai-sdlc-ba"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "BA"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-003"
    - "AC-006"
    - "AC-007"
    - "AC-008"
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
    - "WF-001"
    - "WF-002"
    - "WF-003"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/backlog-gap-review.md"
    - "specs-refiniment/017-local-context-cache/backlog.md"
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
    - "ai-sdlc-ba"
    - "business-context"
    - "review"
---

# business-context.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/business-context.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/release-slicing.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs-refiniment/017-local-context-cache/user-stories.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Current Behavior
The harness already selects per-step context and can fall back to direct reading, but each run may rediscover the same repository content and topology. The prototype can build and query a local SQLite index, yet its pack output does not currently preserve the mandatory owning StepCard and critical anchors. Existing default installation remains 45 skills and must stay unchanged.

## Desired Behavior
An opted-in user builds a disposable local index, retrieves exact and related evidence deterministically, and requests a context-pack v4 candidate. The pack includes the owning StepCard, all mandatory evidence and critical anchors, source authority, hashes, line ranges, token estimates, reasons, and a stable fingerprint. If freshness, safety, recall, or economics fail, the system explicitly selects direct_read.

## Actor and Permission Matrix
| Actor | Role | Permissions | Restrictions | Source |
| --- | --- | --- | --- | --- |
| Contributor | Local operator | Explicit build; refresh; inspect; verify; purge | Project root only; no implicit install | DEC-001 |
| Agent | Context consumer | Query and consume validated evidence | No authority from retrieved content; no hidden writes | DEC-005 |
| Maintainer | Release owner | Configure module and gates | Cannot waive mandatory anchors or TOON contract | DEC-004; DEC-007 |
| QA | Evidence owner | Execute fixtures and benchmarks | Cannot infer passing live quality from token savings | RF-007 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | Explicit module install | Contributor | Install module; verify added skill; retain default inventory | Optional capability ready | Unsupported FTS5 blocks cache activation | DEC-001; FR-001 |
| WF-002 | Build or refresh | Contributor | Discover; hash; chunk; update rows and edges transactionally; verify | Current consistent index | Unsafe files skip; transaction failure rolls back | RF-001; RF-006 |
| WF-003 | Pack request | Agent | Load StepCard and anchors; retrieve; measure recall and savings | Packed v4 context or direct_read | Missing anchors or low savings selects direct_read | RF-004; DEC-007 |

## Business Rule Catalog
| Rule ID | Rule | Applies To | Failure Behavior | Source | Decision Ref |
| --- | --- | --- | --- | --- | --- | --- |
| BR-001 | No alternate machine format artifacts or portable contracts | All module surfaces | Validation blocks change | User direction | DEC-001 |
| BR-002 | Retrieved content remains evidence_only | Query and pack | Ignore embedded instructions | RF-005 | DEC-005 |
| BR-003 | StepCard and all critical anchors are mandatory | Context pack | Select direct_read | RF-004 | DEC-004 |
| BR-004 | Packed mode requires at least 15 percent savings | Context pack | Select direct_read | RF-004 | DEC-007 |
| BR-005 | Graph traversal is deterministic and bounded | Query | Stop at configured limit | RF-003 | DEC-003 |

## Acceptance Criteria
| AC ID | Given | When | Then | Rule Ref | Source |
| --- | --- | --- | --- | --- | --- |
| AC-001 | Default and module installs | Installer executes | Inventories remain 45 and 46 respectively | BR-001 | STORY-001 |
| AC-003 | Current fixture repository | Incremental and clean builds run | Semantic state and fingerprints match | BR-005 | STORY-002 |
| AC-006 | StepCard and critical anchors | Pack executes | Recall is 100 percent | BR-003 | STORY-004 |
| AC-007 | Estimated savings below threshold | Pack executes | direct_read is selected | BR-004 | STORY-004 |
| AC-008 | Injection-shaped source text | Query executes | Text remains evidence and grants no action | BR-002 | STORY-004 |

## Business Context Gaps
No blocking business-context gap remains. Owners, local data boundary, optional adoption, failure behavior, MVP scope, success thresholds, and deferred roadmap work are explicit. Exact future embedding runtime and full GraphRAG global search remain owned post-MVP questions with no effect on current acceptance criteria.
