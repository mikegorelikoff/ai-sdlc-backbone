---
type: "ai-sdlc.release-slicing"
title: "Release Slicing and Readiness"
description: "MVP and release slices, sequencing, and backlog readiness."
tags:
  - "ai-sdlc"
  - "planning"
  - "release"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:12Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "release-slicing.md"
  path: "specs-refiniment/017-local-context-cache/release-slicing.md"
  workspace: "refinement"
  skill: "ai-sdlc-release-slicing-and-backlog-readiness-review"
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "RISK-001"
    - "RISK-002"
    - "RISK-003"
    - "RISK-004"
    - "RISK-005"
    - "RISK-006"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/backlog-gap-review.md"
    - "specs-refiniment/017-local-context-cache/backlog.md"
    - "specs-refiniment/017-local-context-cache/decision-log.md"
    - "specs-refiniment/017-local-context-cache/delivery-gap-review.md"
    - "specs-refiniment/017-local-context-cache/discovery.md"
    - "specs-refiniment/017-local-context-cache/goal-capability-map.md"
    - "specs-refiniment/017-local-context-cache/index.md"
    - "specs-refiniment/017-local-context-cache/prfaq.md"
    - "specs-refiniment/017-local-context-cache/requirements-readiness.md"
    - "specs-refiniment/017-local-context-cache/research.md"
    - "specs-refiniment/017-local-context-cache/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-release-slicing-and-backlog-readiness-review"
    - "release-slicing"
    - "review"
---

# release-slicing.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/release-slicing.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs-refiniment/017-local-context-cache/user-stories.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## MVP Slice
Slice 1 establishes the TOON contracts, optional install, safe discovery, SQLite capability checks, and transactional incremental index. Slice 2 adds deterministic lexical query and bounded relation expansion. Slice 3 integrates StepCard and critical anchors into context-pack v4 with direct-read fallback. Slice 4 adds inspect, verify, purge, golden benchmarks, docs, security review, compatibility, and release evidence.

## Release Slice Matrix
| Slice | Value | Stories | Dependencies | Exit Criteria | Risks |
| --- | --- | --- | --- | --- | --- |
| R1 | Safe optional index | STORY-001; STORY-002 | FTS5; installer | Clean and incremental parity; exclusions pass | SQLite variance |
| R2 | Deterministic retrieval | STORY-003 | R1 | Exact and relation golden queries pass | Recall; fan-out |
| R3 | Safe context savings | STORY-004 | R2; context-pack v4 | 100 percent anchors; economics fallback | Anchor loss |
| R4 | Releasable module | STORY-005 | R1 through R3 | Full validation and benchmark receipt | Misleading claims |

## Sequencing and Dependencies
Contracts and discovery rules precede storage; storage precedes retrieval; lexical seeds precede graph expansion; validated retrieval and mandatory evidence precede context packing; deterministic evaluation precedes public claims. Independent documentation and installer fixtures can run alongside retrieval after contracts stabilize. No calendar dates are inferred because capacity was not supplied.

## Milestones and Readiness
M1 contract and storage ready when clean and incremental builds match. M2 retrieval ready when repeated lexical and graph queries produce identical order and fingerprints. M3 context ready when StepCard and anchors have 100 percent recall and poor economics select direct_read. M4 release ready when module smoke, regression, security, docs, compatibility, and benchmark receipts pass.

## Release Risks
RISK-001 stale index is mitigated by fingerprints and verify/rebuild. RISK-002 anchor loss is blocked by 100 percent recall. RISK-003 prompt injection is contained by evidence-only authority and no action capability. RISK-004 SQLite variance is handled by capability checks. RISK-005 GraphRAG overclaiming is prevented by terminology tests and documentation review. RISK-006 weak retrieval is exposed by golden queries.

## Release Verdict
Ready for implementation sequencing, not yet ready for release. The logical slices, dependencies, owners, DoR and exit criteria are explicit. Release remains blocked until the current pack gap is fixed and deterministic benchmark, security, installer, compatibility, and documentation evidence all pass.
