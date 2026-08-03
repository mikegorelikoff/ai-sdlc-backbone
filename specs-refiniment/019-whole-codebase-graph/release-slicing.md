---
type: "ai-sdlc.release-slicing"
title: "Release Slicing and Readiness"
description: "MVP and release slices, sequencing, and backlog readiness."
tags:
  - "ai-sdlc"
  - "planning"
  - "release"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:46:24Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "release-slicing.md"
  path: "specs-refiniment/019-whole-codebase-graph/release-slicing.md"
  workspace: "refinement"
  skill: "ai-sdlc-release-slicing-and-backlog-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-003"
    - "AC-008"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-005"
    - "SC-001"
    - "SC-021"
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
    - "specs-refiniment/019-whole-codebase-graph/backlog.md"
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/goal-capability-map.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
    - "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-release-slicing-and-backlog-readiness-review"
    - "release-slicing"
    - "approved"
---

# release-slicing.md

## Feature Summary
- Confirmed facts: Feature 019 is one production MVP delivered through five internal promotion slices: parser feasibility, corpus/AST foundation, deterministic graph, retrieval/fallback, and release proof.
- Evidence: backlog.md and user-stories.md.
- Open questions/blockers: None for slicing.

## Actors and Stakeholders
- Confirmed facts: Engineering and Security own early feasibility; Maintainers and Engineering own graph delivery; Agent/Developer validate value; QA and Security own promotion and release gates.
- Evidence: role and story matrices.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: All twelve languages and US-001 through US-012 are required for the production MVP. Slices are integration checkpoints, not permission to ship partial language support as complete.
- Evidence: DEC-002, DEC-003, and backlog priority.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: Each slice produces an independently testable internal outcome while preserving direct-read fallback. Promotion stops on parser, coverage, determinism, bounds, freshness, recall, economics, or safety failure.
- Evidence: WF-001 through WF-004 and SC-001 through SC-021.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Promotion and release criteria trace to AC-001 through AC-008 and USAC-001 through USAC-024.
- Evidence: user-stories.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Release slices preserve offline runtime, pinned grammars, local SQLite, atomic publication, deterministic TOON receipts, bounded traversal, and optional installation.
- Evidence: DEC-005 and DEC-006.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser feasibility is the first risk-reduction gate. No calendar dates or capacity are invented; logical ordering follows hard dependencies.
- Evidence: backlog-gap-review.md and backlog.md.
- Open questions/blockers: None.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 define the slices. No language, safety, determinism, or economics gate is deferred.
- Evidence: decision-log.md.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: Final promotion requires SM-001 through SM-007; intermediate slices use narrower evidence but never claim production readiness.
- Evidence: discovery.md Success Measures.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon. Budget-omitted next_reads were directly inspected in their named source sections.
- Evidence: Full-flow release scan fingerprint 99a293a5baf8f2228fbe86669d6623226d70e90d08dd3a0a6fc17b059bbde158.
- Open questions/blockers: Release Slices are defined below; no upstream gap remains.

## MVP Slice
- Confirmed facts: The MVP is the union of RS-0 through RS-4. Must-have outcomes are all twelve parsers, complete accounting, stable bounded graph, incremental freshness, symbol-aware retrieval, at least 25 percent accepted-pack savings, deterministic diagnostics, safe fallback, offline optional installation, and passing production gates.
- Evidence: EPIC-001 through EPIC-005 and US-001 through US-012.
- Open questions/blockers: None. A partial slice may be merged internally behind optional behavior but cannot be released as graph-complete.

## Release Slice Matrix
| Slice | Value | Stories | Dependencies | Exit Criteria | Risks |
| --- | --- | --- | --- | --- | --- |
| RS-0 Parser feasibility | Retire supply-chain and platform risk early | US-001; US-012 install subset | Feature 018 baseline | Twelve pinned grammars load offline; hashes, licenses, ABI, and supported-target smoke pass | Wheel/platform gap |
| RS-1 Corpus and AST foundation | Account for every file and prove twelve-language AST coverage | US-002; US-003; US-004 | RS-0 | AC-001 through AC-003 and twelve fixtures pass, including Kotlin and Swift | Parser semantics, false completeness |
| RS-2 Deterministic bounded graph | Persist stable fresh graph without clique growth | US-005; US-006; US-007 | RS-1 | Stable fingerprints, declared bounds, atomic refresh, zero stale accepted nodes | Graph explosion, stale edges |
| RS-3 Retrieval and safe operations | Deliver symbol-aware token-efficient search with direct fallback | US-008; US-009; US-010 | RS-2 | Golden recall, stable ranking, >=25 percent accepted savings, deterministic TOON fallback | Recall or token regression |
| RS-4 Production evidence | Prove release readiness end to end | US-011; remaining US-012 | RS-0 through RS-3 | AC-001 through AC-008, security, install, docs, compatibility, and repository corpus gates pass twice | Cross-platform or integration regression |

## Sequencing and Dependencies
- Confirmed facts: RS-0 precedes RS-1; RS-1 precedes schema acceptance in RS-2; RS-2 precedes graph retrieval in RS-3; RS-4 consumes all evidence. Within slices, policy/schema work and fixture/test work may run in parallel once their inputs exist.
- Evidence: Story Dependencies and Risks plus T-001 through T-012.
- Open questions/blockers: No fake sprint dates; implementation can adjust parallelism without changing promotion order.

## Milestones and Readiness
- M0: Parser bundle selected; exit on offline twelve-language load and integrity receipt.
- M1: AST coverage complete; exit on every safe file accounted and all twelve fixture suites passing.
- M2: Graph core complete; exit on schema, stable identity, fan-out, hub, incremental, and atomic-publication tests.
- M3: Retrieval complete; exit on golden recall, deterministic rank, TOON diagnostics, and >=25 percent accepted-pack savings.
- M4: Production ready; exit on full validation, security, code review, install smoke, docs, compatibility, and clean repository evidence.
- Backlog readiness: 9/10. Stories are estimable and traceable; the remaining point requires implementation-time parser and benchmark evidence.

## Release Risks
| Risk | Early warning | Mitigation | Owner | Gate |
| --- | --- | --- | --- | --- |
| Grammar wheel or ABI gap | Any selected grammar fails clean install/import | Stop at RS-0; pin compatible artifacts or build reviewed wheels; never reduce scope silently | Engineering and Security | USAC-001; USAC-002; USAC-023 |
| Incomplete AST semantics | Fixture misses expected symbol/reference | Keep graph_complete false and correct adapter/query | Engineering and QA | USAC-005 through USAC-008 |
| Graph explosion | Fan-out or total-edge receipt exceeds policy | Use typed bounds and hub nodes; reject candidate | Engineering | USAC-011; USAC-012 |
| Stale publication | Deleted/changed facts remain or source drifts mid-build | Atomic source recheck and previous-graph retention | Engineering and QA | USAC-013; USAC-014 |
| Recall or token regression | Golden evidence missing or savings below 25 percent | Direct-read fallback; tune ranking without weakening recall | Engineering and QA | USAC-015 through USAC-018 |
| Unsafe ingestion or hidden network | Secret/symlink included or network attempted | Fail closed, exclusion receipt, offline test | Security | USAC-019; USAC-023; USAC-024 |

## Release Verdict
- Confirmed facts: READY FOR DELIVERY PLANNING, score 9/10. Top reasons: complete goal-to-task traceability; explicit logical slices and promotion gates; no hidden scope or dependency. Production release is not yet ready and requires RS-0 through RS-4 implementation evidence.
- Evidence: Backlog and story readiness plus slice matrix.
- Open questions/blockers: No planning blocker. Next required owner is BA/delivery specification followed by QA and SDD implementation.
