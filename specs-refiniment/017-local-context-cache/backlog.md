---
type: "ai-sdlc.backlog"
title: "Delivery Backlog"
description: "Epics, stories, acceptance summaries, dependencies, and delivery tasks."
tags:
  - "ai-sdlc"
  - "planning"
  - "backlog"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:06Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "backlog.md"
  path: "specs-refiniment/017-local-context-cache/backlog.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-decomposition-and-task-planning"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "PM"
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
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "TASK-001"
    - "TASK-002"
    - "TASK-003"
    - "TASK-004"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/backlog-gap-review.md"
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
    - "ai-sdlc-backlog-decomposition-and-task-planning"
    - "backlog"
    - "review"
---

# backlog.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Epic Backlog
| Epic ID | Outcome | Actors | Priority | Dependencies |
| --- | --- | --- | --- | --- |
| EPIC-001 | Transactional safe local index | Contributor | P0 | FTS5; TOON |
| EPIC-002 | Deterministic lexical and relation search | Agent | P0 | EPIC-001 |
| EPIC-003 | Anchor-complete context pack or direct_read | Agent | P0 | EPIC-002; v4 contract |
| EPIC-004 | Verified optional release | Maintainer; QA | P0 | EPIC-001 through EPIC-003 |

## Story Backlog
| Story ID | Epic Ref | Actor | Story | Priority | MVP |
| --- | --- | --- | --- | --- | --- |
| STORY-001 | EPIC-004 | Contributor | Opt into the cache module without changing default installs | P0 | Yes |
| STORY-002 | EPIC-001 | Contributor | Build and refresh a safe transactional local index | P0 | Yes |
| STORY-003 | EPIC-002 | Agent | Retrieve exact and related evidence deterministically | P0 | Yes |
| STORY-004 | EPIC-003 | Agent | Receive anchor-complete context or explicit direct_read | P0 | Yes |
| STORY-005 | EPIC-004 | QA | Verify integrity and benchmark release claims | P0 | Yes |

## Acceptance Summary
AC-001 opt-in installation preserves the default profile. AC-002 safe discovery excludes disallowed content. AC-003 incremental builds converge to a clean rebuild. AC-004 exact identifiers and contextual chunks rank deterministically. AC-005 bounded edges add relevant cross-file evidence. AC-006 StepCard and critical anchors reach 100 percent recall. AC-007 insufficient economics selects direct_read. AC-008 evidence cannot grant authority. AC-009 verify detects stale or corrupt state. AC-010 golden benchmarks and all regression gates pass.

## Priorities and Dependencies
Sequence P0 as contract and pack correctness, transactional index and safety, retrieval and bounded graph, then benchmark and installer/docs integration. Query depends on build; graph expansion depends on lexical seeds; pack depends on validated retrieval plus StepCard anchors; release depends on verify and benchmark receipts. Embedding and full GraphRAG work is post-MVP and cannot block the local lexical release.

## Cross-Functional Tasks
| Task ID | Owner | Output | Dependencies | Refs |
| --- | --- | --- | --- | --- |
| TASK-001 | Dev | Correct v4 pack with StepCard and anchors | STORY-004 | FR-006; AC-006 |
| TASK-002 | Dev and QA | Golden benchmark command and fixtures | STORY-003; STORY-004 | FR-010; DEC-007 |
| TASK-003 | Security | Authority and exclusion validation | STORY-002; STORY-004 | FR-008 |
| TASK-004 | Documentation | Graph-enhanced wording and operator guide | STORY-001 through STORY-005 | DEC-003 |

## Definition of Ready
Every MVP story has an actor, observable outcome, requirement and AC references, dependency, risk, and test owner. No story depends on an unresolved product rule. Implementation begins only from the updated full-flow SDD; release begins only after deterministic tests, compatibility, docs, security, module installation, and benchmark receipts pass.
