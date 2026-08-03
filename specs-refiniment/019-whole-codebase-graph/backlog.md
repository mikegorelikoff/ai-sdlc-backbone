---
type: "ai-sdlc.backlog"
title: "Delivery Backlog"
description: "Epics, stories, acceptance summaries, dependencies, and delivery tasks."
tags:
  - "ai-sdlc"
  - "planning"
  - "backlog"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:42:46Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "backlog.md"
  path: "specs-refiniment/019-whole-codebase-graph/backlog.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-decomposition-and-task-planning"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-008"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "EPIC-005"
    - "US-001"
    - "US-002"
    - "US-003"
    - "US-004"
    - "US-005"
    - "US-006"
    - "US-007"
    - "US-008"
    - "US-009"
    - "US-010"
    - "US-011"
    - "US-012"
    - "WF-001"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/goal-capability-map.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-backlog-decomposition-and-task-planning"
    - "backlog"
    - "approved"
---

# backlog.md

## Feature Summary
- Confirmed facts: The delivery backlog preserves all five P0 epics and decomposes them into focused MVP stories for parser packaging, twelve-language AST extraction, deterministic graph persistence, incremental freshness, retrieval, fallback, operations, and release evidence.
- Evidence: goal-capability-map.md and backlog-gap-review.md.
- Open questions/blockers: None.

## Actors and Stakeholders
- Confirmed facts: Each story has one primary actor: Agent, Developer, Harness Maintainer, Engineering, QA, or Security. Cross-functional work has explicit owners.
- Evidence: Role Matrix and Story Backlog.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: All stories are MVP/P0. Kotlin and Swift have the same coverage gate as the other ten languages. Remote services, runtime downloads, LLM extraction, embeddings, and heuristic completeness remain excluded.
- Evidence: DEC-002 through DEC-006.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: US-001 through US-004 deliver warm foundations; US-005 through US-007 graph persistence and freshness; US-008 and US-009 retrieval; US-010 operations and fallback; US-011 and US-012 production verification.
- Evidence: WF-001 through WF-004.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Every story traces to FR, BR, AC, capability, and epic IDs; graph-complete cannot be accepted without all twelve AST languages.
- Evidence: AC-001 through AC-008 and Acceptance Summary.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Work covers schema migration, stable IDs, typed bounded relations, coverage receipts, offline parser loading, TOON-only portable outputs, deterministic ranking, and atomic SQLite publication.
- Evidence: DEC-003 through DEC-006.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser pinning precedes AST acceptance; schema precedes retrieval; fixtures precede graph-complete; retrieval precedes economics proof. Failed platform support blocks release, not scope.
- Evidence: backlog-gap-review.md.
- Open questions/blockers: None.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 control the backlog; no unrecorded scope assumption is used.
- Evidence: decision-log.md.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: Backlog exit requires SM-001 through SM-007 and AC-001 through AC-008 with production evidence.
- Evidence: discovery.md.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon.
- Evidence: Full-flow decomposition scan fingerprint 4c5cc8f847072307018545b78630b2f5c9bce996ff839228d2fd530af9bde1dc with gaps[0].
- Open questions/blockers: None.

## Epic Backlog
| Epic ID | Outcome | Actors | Priority | Dependencies |
| --- | --- | --- | --- | --- |
| EPIC-001 | Safe corpus and all twelve parsers produce explicit coverage | Maintainer; Engineering; QA; Security | P0 | Feature 018; parser bundle |
| EPIC-002 | Stable bounded graph publishes atomically and refreshes incrementally | Engineering; QA | P0 | EPIC-001; SQLite |
| EPIC-003 | Symbol-aware retrieval achieves recall and token savings | Agent; Developer; QA | P0 | EPIC-002; StepCard |
| EPIC-004 | Operators receive deterministic diagnostics and safe fallback | Maintainer; Agent; Security | P0 | EPIC-001 through EPIC-003 |
| EPIC-005 | Offline install and full validation prove production readiness | Engineering; QA; Security | P0 | All prior epics |

## Story Backlog
| Story ID | Epic Ref | Actor | Story | Priority | MVP |
| --- | --- | --- | --- | --- | --- |
| US-001 | EPIC-001 | Security Engineer | Pin and hash an offline-compatible Tree-sitter runtime and twelve grammar packages | P0 | Yes |
| US-002 | EPIC-001 | Harness Maintainer | Classify every safe file by language and explicit AST support status | P0 | Yes |
| US-003 | EPIC-001 | Software Engineer | Parse all twelve languages and extract definitions, occurrences, imports, and provable references | P0 | Yes |
| US-004 | EPIC-001 | QA Engineer | Exercise one executable AST fixture per language including Kotlin and Swift | P0 | Yes |
| US-005 | EPIC-002 | Software Engineer | Persist stable file, chunk, symbol, occurrence, and relation records | P0 | Yes |
| US-006 | EPIC-002 | Software Engineer | Bound typed relations and replace trace cliques with hubs | P0 | Yes |
| US-007 | EPIC-002 | Harness Maintainer | Incrementally update changed files and atomically remove stale facts | P0 | Yes |
| US-008 | EPIC-003 | AI coding agent | Query lexical seeds plus bounded symbol and dependency traversal | P0 | Yes |
| US-009 | EPIC-003 | AI coding agent | Build a budgeted context pack with deterministic ranking and savings gate | P0 | Yes |
| US-010 | EPIC-004 | Harness Maintainer | Inspect coverage and receive explicit TOON fallback reasons without authority escalation | P0 | Yes |
| US-011 | EPIC-005 | QA Engineer | Prove determinism, recall, freshness, boundedness, and economics on golden and repository corpora | P0 | Yes |
| US-012 | EPIC-005 | Security Engineer | Prove safe optional installation, offline runtime, exclusion policy, and dependency integrity | P0 | Yes |

## Acceptance Summary
- US-001: clean optional installation resolves pinned artifacts and runtime warm performs no downloads.
- US-002: every safe file has one deterministic accounted status.
- US-003: all selected-language files parse or graph_complete is false; no heuristic claims AST.
- US-004: twelve fixtures expose expected definitions and references, explicitly including Kotlin and Swift.
- US-005: identical sources yield identical stable IDs and graph fingerprint.
- US-006: each relation stays within declared fan-out and trace IDs do not form cliques.
- US-007: changed and deleted files leave zero stale accepted nodes after atomic publication.
- US-008: golden symbol and path queries return all expected evidence in stable order.
- US-009: accepted packs retain critical anchors and save at least 25 percent tokens.
- US-010: missing grammar, parse failure, stale/corrupt graph, unsafe source, fan-out breach, or timeout yields an explicit TOON reason and direct_read.
- US-011: AC-001 through AC-008 pass twice with byte-identical deterministic evidence.
- US-012: supported-platform install smoke, hash verification, offline checks, and secret/symlink regressions pass.

## Priorities and Dependencies
- Confirmed facts: Sequence US-001 and US-002; then US-003 and US-004; then US-005 through US-007; then US-008 through US-010; finish with US-011 and US-012. Tests are written alongside their owning behavior, not deferred.
- Evidence: capability dependencies and backlog gap matrix.
- Open questions/blockers: No date or staffing assumption is needed.

## Cross-Functional Tasks
| Task ID | Owner | Output | Dependencies | Refs |
| --- | --- | --- | --- | --- |
| T-001 | Engineering and Security | Locked parser dependency set with versions, hashes, licenses, ABI receipt | None | US-001; DEC-006 |
| T-002 | Engineering | Language policy and twelve AST adapters/queries | T-001 | US-002; US-003 |
| T-003 | QA | Twelve language fixtures and expected symbol/reference matrix | T-002 | US-004; AC-002 |
| T-004 | Engineering | Schema migration, stable identity, node/edge persistence | T-002 | US-005; DEC-005 |
| T-005 | Engineering and QA | Fan-out policy, trace hubs, boundedness tests | T-004 | US-006; AC-005 |
| T-006 | Engineering and QA | Incremental invalidation and atomic publication tests | T-004 | US-007; AC-004 |
| T-007 | Engineering | Symbol-aware query, traversal, scoring, and pack integration | T-004; T-005 | US-008; US-009 |
| T-008 | Security and Engineering | Coverage diagnostics, offline enforcement, direct-read fallback | T-001; T-007 | US-010; AC-006; AC-008 |
| T-009 | QA | Golden recall, full-corpus determinism, freshness, and economics suite | T-003 through T-008 | US-011; DEC-007 |
| T-010 | Operations and Documentation | Optional installer, smoke matrix, guide, troubleshooting, release evidence | T-001; T-009 | US-012 |
| T-011 | Security | Dependency, secret, path, symlink, and untrusted-content review | T-001; T-008 | US-012 |
| T-012 | Harness Maintainers | Changelog, generated catalogs, compatibility, and release gate updates | T-009 through T-011 | EPIC-005 |

## Definition of Ready
- Confirmed facts: Every story has an actor, observable outcome, MVP and P0 status, acceptance summary, dependencies, value, and owner-linked tasks. No story is too large for SDD decomposition because language-specific behavior is parameterized but independently fixture-verified.
- Evidence: Tables above and backlog-structures.md quality bar.
- Open questions/blockers: Ready for detailed user-story decomposition.
