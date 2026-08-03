---
type: "ai-sdlc.qa-readiness"
title: "QA Traceability and Readiness"
description: "Requirements-to-test traceability and execution readiness."
tags:
  - "ai-sdlc"
  - "qa"
  - "review"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:54Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "qa-readiness.md"
  path: "specs-refiniment/017-local-context-cache/qa-readiness.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa-traceability-and-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/017-local-context-cache/decision-log.md"
  status: "review"
  owner: "QA"
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
    - "TC-009"
    - "TC-010"
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
    - "specs-refiniment/017-local-context-cache/test-suite.md"
    - "specs-refiniment/017-local-context-cache/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa-traceability-and-readiness-review"
    - "qa-readiness"
    - "review"
---

# qa-readiness.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/business-context.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/delivery-spec.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/qa-gap-review.md; specs-refiniment/017-local-context-cache/qa-readiness.md; specs-refiniment/017-local-context-cache/qa-strategy.md; specs-refiniment/017-local-context-cache/qa.md; specs-refiniment/017-local-context-cache/release-slicing.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs-refiniment/017-local-context-cache/test-cases.md; specs-refiniment/017-local-context-cache/test-suite.md; specs-refiniment/017-local-context-cache/user-stories.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Requirement-to-Test Traceability
| Requirement | Acceptance Ref | Test IDs | Suite | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| FR-001 | AC-001 | TC-001 | Smoke; Regression | Covered | None |
| FR-002; FR-003 | AC-002; AC-003 | TC-002; TC-003; TC-004 | Regression | Covered by design | Execution pending implementation |
| FR-004; FR-005 | AC-004; AC-005 | TC-005; TC-006 | Smoke; Regression; UAT | Covered by design | Execution pending implementation |
| FR-006; FR-007 | AC-006; AC-007 | TC-007; TC-009 | Smoke; Regression; UAT | Blocked | Prototype correction required |
| FR-008 | AC-008 | TC-010 | Regression | Covered by design | Execution pending implementation |
| FR-009; FR-010 | AC-009; AC-010 | TC-011; TC-012; TC-013 | Smoke; Regression | Blocked | Verify and benchmark evidence required |

## Risk Coverage
Anchor loss, stale state, partial transactions, unsafe discovery, injection-shaped evidence, ranking drift, graph explosion, insufficient savings, installer regression, and misleading terminology each have P0 or P1 cases and named owners. Lexical paraphrase limitations have golden coverage and explicit residual risk; embeddings and full GraphRAG are not falsely counted as covered.

## Coverage Gaps
No MVP requirement lacks a planned deterministic test. Live-provider answer quality, embedding recall, and global community search are intentionally out of scope and recorded as roadmap gaps, not hidden release coverage. Repository-scale latency thresholds beyond bounded completion are observational for the first release and must be reported rather than fabricated.

## Execution Readiness Evidence
| Evidence Area | Required Signal | Present | Gap | Impact |
| --- | --- | --- | --- | --- |
| Requirements | FR and AC identifiers with rules | Yes | None | Test design ready |
| Test Cases | Executable steps and expected outcomes | Yes | Implementation execution pending | Release blocked |
| Suites | Smoke; regression; UAT mappings | Yes | None | Execution can be sequenced |
| Risks | P0 safety and correctness coverage | Yes | None | Risk-based scope defined |
| Blockers | Pack and benchmark tasks with owners | Yes | Code not yet corrected | Release blocked |
| Automation | Deterministic Python and TOON benchmark plan | Yes | Benchmark command pending | AC-010 pending |

## Blocked Coverage
There is no blocked MVP coverage once the benchmark command and corrected pack implementation land. Until then, TC-007, TC-009, and TC-013 are planned but not execution-ready and therefore keep implementation release status blocked. Owners are Dev for implementation and QA for receipt validation; the next action is encoded in the SDD tasks.

## QA Readiness Verdict
The specification is ready for implementation and the QA design is traceable, but the product is not release-ready until implementation evidence exists. Readiness score is 9/10 for test design: every MVP requirement has a case and suite, risks and fallbacks are explicit, and deterministic thresholds are approved. Execution status remains blocked on the corrected pack and benchmark code.
