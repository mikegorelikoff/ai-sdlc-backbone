---
type: "ai-sdlc.test-suite"
title: "Test Suite"
description: "Executable smoke, regression, and acceptance suite definitions."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:51Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "test-suite.md"
  path: "specs-refiniment/017-local-context-cache/test-suite.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-case-and-suite-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "QA"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-009"
    - "TC-011"
    - "TC-012"
    - "TC-013"
  related_artifacts:
    - "specs-refiniment/017-local-context-cache/backlog-gap-review.md"
    - "specs-refiniment/017-local-context-cache/backlog.md"
    - "specs-refiniment/017-local-context-cache/business-context.md"
    - "specs-refiniment/017-local-context-cache/decision-log.md"
    - "specs-refiniment/017-local-context-cache/delivery-gap-review.md"
    - "specs-refiniment/017-local-context-cache/delivery-spec.md"
    - "specs-refiniment/017-local-context-cache/discovery.md"
    - "specs-refiniment/017-local-context-cache/goal-capability-map.md"
    - "specs-refiniment/017-local-context-cache/index.md"
    - "specs-refiniment/017-local-context-cache/prfaq.md"
    - "specs-refiniment/017-local-context-cache/qa-gap-review.md"
    - "specs-refiniment/017-local-context-cache/qa-strategy.md"
    - "specs-refiniment/017-local-context-cache/qa.md"
    - "specs-refiniment/017-local-context-cache/release-slicing.md"
    - "specs-refiniment/017-local-context-cache/requirements-readiness.md"
    - "specs-refiniment/017-local-context-cache/research.md"
    - "specs-refiniment/017-local-context-cache/test-cases.md"
    - "specs-refiniment/017-local-context-cache/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-case-and-suite-synthesis"
    - "test-suite"
    - "review"
---

# test-suite.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/business-context.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/delivery-spec.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/qa-gap-review.md; specs-refiniment/017-local-context-cache/qa-strategy.md; specs-refiniment/017-local-context-cache/qa.md; specs-refiniment/017-local-context-cache/release-slicing.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs-refiniment/017-local-context-cache/test-cases.md; specs-refiniment/017-local-context-cache/test-suite.md; specs-refiniment/017-local-context-cache/user-stories.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Suite Coverage Matrix
| Suite | Purpose | Test IDs | Trigger | Environment | Owner |
| --- | --- | --- | --- | --- | --- |
| Smoke | Prove opt-in build-query-pack-verify | TC-001; TC-003; TC-005; TC-007; TC-011 | Every module change | Local FTS5 fixture | QA |
| Regression | Protect safety; determinism; compatibility | TC-001 through TC-013 | Pull request and release | Offline temporary repositories | QA |
| UAT | Demonstrate contributor token-efficient workflow | TC-001; TC-005; TC-006; TC-007; TC-009; TC-012 | Release candidate | Representative repository fixture | Maintainer and QA |

## Smoke Suite
SMOKE-001 installs the module, builds the fixture index, retrieves an exact requirement, creates an anchor-complete pack, and verifies the database. It includes TC-001, TC-003, TC-005, TC-007, and TC-011. Entry requires FTS5; exit requires all P0 outputs and deterministic fingerprints to pass.

## Regression Suite
REG-001 includes TC-002 through TC-012 and protects safe discovery, incremental parity, ranking, graph bounds, context-pack v4, direct_read fallback, authority, integrity, purge, default install inventory, compatibility, docs, and TOON-only contracts. Exit requires no regression and no changed public default behavior.

## UAT Suite
UAT-001 demonstrates that a contributor opts in, finds an exact ID and a related decision, receives a minimal high-signal context pack with every mandatory anchor, observes at least 15 percent estimated savings or an honest direct_read fallback, and purges the derived cache without changing sources. It uses TC-001, TC-005, TC-006, TC-007, TC-009, and TC-012.

## Entry Criteria
Delivery spec and decisions are finalized; implementation tests exist; FTS5 capability is known; fixture repositories contain declared anchors and relations; the module is installable; and the benchmark command emits TOON. The cache database starts absent or is explicitly rebuilt for each independent suite.

## Exit Criteria
All P0 cases pass; every FR and AC maps to at least one test; smoke, regression, and UAT have no blocker; mandatory-anchor recall is 100 percent; repeated fingerprints match; excluded-file ingestion is zero; packed-mode savings meets 15 percent or direct_read is selected; docs, compatibility, security, and installer gates pass.

## Execution Dependencies
Suite execution depends only on the repository checkout, Python, SQLite FTS5, temporary writable storage, and Git for tracked fixture coverage. Tests are offline and provider-neutral. If FTS5 is absent, capability-block behavior is tested and the release environment must be corrected before cache certification.
