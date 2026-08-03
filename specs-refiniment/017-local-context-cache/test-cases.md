---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T10:12:47Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "test-cases.md"
  path: "specs-refiniment/017-local-context-cache/test-cases.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-cases"
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
    - "TC-010"
    - "TC-011"
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
    - "specs-refiniment/017-local-context-cache/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-cases"
    - "test-cases"
    - "review"
---

# test-cases.md

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
Sources directly consumed or traced by this stage: specs-refiniment/017-local-context-cache/backlog-gap-review.md; specs-refiniment/017-local-context-cache/backlog.md; specs-refiniment/017-local-context-cache/business-context.md; specs-refiniment/017-local-context-cache/decision-log.md; specs-refiniment/017-local-context-cache/delivery-gap-review.md; specs-refiniment/017-local-context-cache/delivery-spec.md; specs-refiniment/017-local-context-cache/discovery.md; specs-refiniment/017-local-context-cache/goal-capability-map.md; specs-refiniment/017-local-context-cache/index.md; specs-refiniment/017-local-context-cache/prfaq.md; specs-refiniment/017-local-context-cache/qa-gap-review.md; specs-refiniment/017-local-context-cache/qa-strategy.md; specs-refiniment/017-local-context-cache/qa.md; specs-refiniment/017-local-context-cache/release-slicing.md; specs-refiniment/017-local-context-cache/requirements-readiness.md; specs-refiniment/017-local-context-cache/research.md; specs-refiniment/017-local-context-cache/test-cases.md; specs-refiniment/017-local-context-cache/user-stories.md; specs/017-local-context-cache/decision-log.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/index.md; specs/017-local-context-cache/plan.md; specs/017-local-context-cache/qa.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/tasks.md; specs/017-local-context-cache/test-cases.md. External findings are registered with locators and limitations in `specs-refiniment/017-local-context-cache/research.md`.

## Scenario Matrix
| Scenario ID | Requirement Ref | Type | Preconditions | Expected Outcome |
| --- | --- | --- | --- | --- |
| SCN-001 | FR-001 | Installation | Default and module fixtures | Inventories are unchanged and additive |
| SCN-002 | FR-003 | Incremental | Changed and deleted files | State equals clean rebuild |
| SCN-003 | FR-004; FR-005 | Retrieval | Exact ID and related files | Stable ranked bounded evidence |
| SCN-004 | FR-006; FR-007 | Context | StepCard; anchors; token budget | Complete pack or explicit direct_read |
| SCN-005 | FR-008 | Security | Injection-shaped repository text | Evidence cannot authorize action |
| SCN-006 | FR-009; FR-010 | Recovery and evaluation | Corrupt DB and golden queries | Recovery and stable benchmark receipts |

## Detailed Test Cases
| Test ID | Scenario Ref | Steps | Expected Result | Priority | Automation |
| --- | --- | --- | --- | --- | --- |
| TC-001 | SCN-001 | Install default; install with context-cache module; list skills | Counts are 45 and 46 with only cache added | P0 | Yes |
| TC-002 | SCN-002 | Build fixture with excluded content; inspect index | Only allowed regular text files are indexed | P0 | Yes |
| TC-003 | SCN-002 | Modify and delete files; refresh; compare clean rebuild | Documents; chunks; edges; fingerprints match | P0 | Yes |
| TC-005 | SCN-003 | Query exact FR and decision twice | Same ranked results and fingerprint | P0 | Yes |
| TC-006 | SCN-003 | Query seed with path and trace relations | Related evidence respects depth and fan-out | P1 | Yes |
| TC-007 | SCN-004 | Pack with StepCard and anchors | StepCard retained and critical recall is 100 percent | P0 | Yes |
| TC-009 | SCN-004 | Pack fixture below savings threshold | Strategy is direct_read with reasons | P0 | Yes |
| TC-010 | SCN-005 | Query injection-shaped evidence | Authority is evidence_only and no action executes | P0 | Yes |
| TC-011 | SCN-006 | Corrupt database; run verify | Failure receipt identifies rebuild or purge recovery | P0 | Yes |
| TC-013 | SCN-006 | Run golden benchmark twice | Thresholds pass and fingerprints match | P0 | Yes |

## Permission and Negative Cases
The cache has read-only repository evidence authority and local derived-state write authority only for explicit build or purge operations. Tests deny symlink traversal, secret ingestion, authority escalation from retrieved text, hidden network activity, and implicit installation. Failure cases assert transaction rollback, stale detection, corrupt-state recovery, bounded traversal, and direct_read when context gates fail.

## Expected Results
Each case asserts operation status, selected strategy, ranked paths and line ranges, authority class, anchor counts, token estimates, skip reasons, graph depth, stable fingerprint, and any derived-state change. Error cases assert a machine-readable TOON reason and no partial database mutation. Installation cases assert exact skill inventories for default and module profiles.

## Layer Mapping
Path, chunk, ranking, graph, and pack logic map to unit tests. SQLite consistency and incremental parity map to integration tests. Installer and module inventory map to installation smoke tests. Context-pack compatibility maps to shared contract tests. Documentation and terminology map to docs validation. End-to-end golden queries map to the benchmark suite.

## Automation Plan
Implement TC-001 through TC-013 as deterministic Python tests and a benchmark subcommand that emits `ai-sdlc-context-cache-benchmark/v1` TOON. Add fixtures for every exclusion and recovery path. Wire focused suites into repository validation and retain a separate optional manual/live evaluation list for model-dependent quality questions.
