---
type: "ai-sdlc.goal-capability-map"
title: "Goal, Capability, and Epic Map"
description: "Business goals mapped to roles, capabilities, and outcome-oriented epics."
tags:
  - "ai-sdlc"
  - "planning"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:39:22Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "goal-capability-map.md"
  path: "specs-refiniment/019-whole-codebase-graph/goal-capability-map.md"
  workspace: "refinement"
  skill: "ai-sdlc-goal-capability-and-epic-mapping"
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
    - "AC-007"
    - "AC-008"
    - "BR-001"
    - "BR-007"
    - "CAP-001"
    - "CAP-002"
    - "CAP-003"
    - "CAP-004"
    - "CAP-005"
    - "CAP-006"
    - "CAP-007"
    - "DEC-001"
    - "DEC-002"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "EPIC-005"
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
    - "GOAL-004"
    - "GOAL-005"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-goal-capability-and-epic-mapping"
    - "goal-capability-map"
    - "approved"
---

# goal-capability-map.md

## Feature Summary
- Confirmed facts: Feature 019 provides deterministic local graph navigation across the safe corpus, with full Tree-sitter AST coverage for twelve selected languages and token-efficient retrieval.
- Evidence: requirements-readiness.md score 9/10 and AC-001 through AC-008.
- Open questions/blockers: None.

## Actors and Stakeholders
- Confirmed facts: Developers and AI agents navigate code; maintainers operate and package the graph; QA verifies coverage and economics; Security protects source and dependency boundaries.
- Evidence: discovery.md and requirements-readiness.md.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: The mapping covers inventory, AST parsing, graph persistence, query/pack consumption, operations, safety, and verification for TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift.
- Evidence: DEC-002 through DEC-007.
- Open questions/blockers: Remote or heuristic graph extraction is out of scope.

## Workflows and Failure Paths
- Confirmed facts: WF-001 warm, WF-002 retrieve, WF-003 incrementally refresh, and WF-004 reject/fallback map directly to capabilities and epics below.
- Evidence: discovery.md.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: AC-001 through AC-008 and BR-001 through BR-007 define complete accounting, AST proof, deterministic identity, bounded graph, offline execution, TOON contracts, and safe fallback.
- Evidence: discovery.md Acceptance Criteria and prfaq.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite derived storage, pinned Tree-sitter grammars, offline runtime, stable fingerprints, and optional StepCard integration are delivery necessities.
- Evidence: DEC-005 and DEC-006.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser packaging, ABI compatibility, bounded edges, stale prevention, exclusions, and economics are first-class epic risks with owned gates.
- Evidence: delivery-gap-review.md and requirements-readiness.md.
- Open questions/blockers: Parser proof blocks release only.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted; no capability or epic relies on an unrecorded assumption.
- Evidence: decision-log.md.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: Goals map to complete accounting, complete AST coverage, zero stale acceptance, bounded graph size, full golden recall, at least 25 percent token savings, and deterministic fingerprints.
- Evidence: SM-001 through SM-007.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon.
- Evidence: Full-flow mapping scan fingerprint a5a8c1d6d4d19e452ff7e7e80935763cce38593c239cc2252df929c729714140.
- Open questions/blockers: None.

## Business Goals
| Goal ID | Goal | Metric | Target | Owner | Source |
| --- | --- | --- | --- | --- | --- |
| GOAL-001 | Make the entire safe repository discoverable through one local graph | Accounted safe files | 100 percent | Harness Maintainers | SM-001 |
| GOAL-002 | Provide trustworthy code intelligence across selected languages | Successful AST coverage | 100 percent for all twelve languages | Engineering and QA | SM-002; AC-002 |
| GOAL-003 | Reduce repeated context consumption | Accepted-pack token savings | At least 25 percent | Product and QA | SM-006; AC-007 |
| GOAL-004 | Preserve deterministic and safe agent behavior | Stale accepted nodes and fingerprint drift | Zero stale nodes; identical fingerprints | QA and Security | SM-003; SM-007 |
| GOAL-005 | Keep local graph cost bounded and operable | Relation and total edge bounds | No declared bound breach | Engineering | SM-004 |

## Role Matrix
| Actor | Role | Need | Permission Boundary | Source |
| --- | --- | --- | --- | --- |
| AI coding agent | Retrieval consumer | Compact definitions, references, and related evidence | Cache is advisory; direct reads remain authoritative | WF-002; AC-008 |
| Developer | Navigation consumer | Fast symbol and impact discovery | Read-only local query and stats | PRFAQ |
| Harness Maintainer | Operator and owner | Warm, diagnose, purge, package, and evolve schema | May manage derived cache and optional dependencies | DEC-006 |
| QA | Gate owner | Deterministic coverage, recall, freshness, and economics evidence | Cannot waive graph-complete requirements | DEC-007 |
| Security | Boundary owner | Safe discovery and supply-chain assurance | Blocks unsafe sources or unverified parser bundle | DEC-004; DEC-006 |

## Capability Map
| Capability ID | Capability | Goal Ref | Actors | Dependencies |
| --- | --- | --- | --- | --- |
| CAP-001 | Safe whole-corpus inventory and explicit accounting | GOAL-001; GOAL-004 | Maintainer; QA; Security | Existing discovery policy |
| CAP-002 | Twelve-language AST parsing and symbol extraction | GOAL-002; GOAL-004 | Agent; Developer; Engineering; QA | Pinned Tree-sitter runtime and grammars |
| CAP-003 | Stable heterogeneous graph persistence with bounded relations | GOAL-001; GOAL-004; GOAL-005 | Engineering; QA | SQLite; identity and fan-out policy |
| CAP-004 | Symbol-aware lexical plus graph retrieval and budgeted packing | GOAL-003; GOAL-004 | Agent; Developer | CAP-001 through CAP-003; StepCard contracts |
| CAP-005 | Incremental freshness and atomic publication | GOAL-004; GOAL-005 | Maintainer; Agent; QA | Source snapshots; atomic database replacement |
| CAP-006 | Coverage, diagnostics, safe fallback, and offline operations | GOAL-002; GOAL-004 | Maintainer; QA; Security | TOON receipts; direct-read path |
| CAP-007 | Production verification and optional installation | GOAL-002; GOAL-003; GOAL-004 | Engineering; QA; Security | Fixtures, smoke tests, parser hashes |

## Epic Map
| Epic ID | Epic | Capability Ref | Outcome | Priority | Risks |
| --- | --- | --- | --- | --- | --- |
| EPIC-001 | Safe corpus and parser foundation | CAP-001; CAP-002 | Every eligible file is accounted for and every selected-language file has verified AST status | P0 | Missing grammar, ABI drift, unsafe input |
| EPIC-002 | Deterministic bounded code graph | CAP-003; CAP-005 | Stable nodes and typed relations publish atomically without clique growth or stale facts | P0 | Graph explosion, stale edges, nondeterminism |
| EPIC-003 | Token-efficient graph retrieval | CAP-004 | Agents find expected paths and symbols with at least 25 percent accepted-pack savings | P0 | False relations, recall loss, token regression |
| EPIC-004 | Operations, fallback, and observability | CAP-006 | Failures are explicit TOON receipts and direct reads remain available | P0 | Silent degradation, authority inversion |
| EPIC-005 | Twelve-language production readiness | CAP-007 | Offline install, fixtures, security, and full validation prove release readiness | P0 | Wheel gaps, supply-chain drift, platform incompatibility |

## Outcome Traceability
- Confirmed facts: GOAL-001 maps to CAP-001/CAP-003 and EPIC-001/EPIC-002; GOAL-002 maps to CAP-002/CAP-006/CAP-007 and EPIC-001/EPIC-004/EPIC-005; GOAL-003 maps to CAP-004/CAP-007 and EPIC-003/EPIC-005; GOAL-004 maps to every operational capability and all epics; GOAL-005 maps to CAP-003/CAP-005 and EPIC-002. No goal, capability, or epic is orphaned.
- Evidence: Tables above and AC-001 through AC-008.
- Open questions/blockers: None.
