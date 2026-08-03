---
type: "ai-sdlc.backlog-gap-review"
title: "Backlog Requirements Gap Review"
description: "Planning gaps and backlog-blocking ambiguity."
tags:
  - "ai-sdlc"
  - "review"
  - "backlog"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:40:54Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "backlog-gap-review.md"
  path: "specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-requirements-gap-review"
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
    - "AC-003"
    - "AC-005"
    - "AC-007"
    - "AC-008"
    - "BR-001"
    - "BR-007"
    - "CAP-001"
    - "CAP-007"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-005"
    - "WF-001"
    - "WF-004"
  related_artifacts:
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
    - "ai-sdlc-backlog-requirements-gap-review"
    - "backlog-gap-review"
    - "approved"
---

# backlog-gap-review.md

## Feature Summary
- Confirmed facts: Feature 019 is ready for backlog decomposition into five P0 epics covering safe inventory and AST parsing, deterministic graph persistence, token-efficient retrieval, operations/fallback, and production readiness.
- Evidence: goal-capability-map.md and requirements-readiness.md.
- Open questions/blockers: None.

## Actors and Stakeholders
- Confirmed facts: Agent, developer, maintainer, QA, and Security roles have distinct needs, boundaries, owners, and success criteria.
- Evidence: goal-capability-map.md Role Matrix.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: MVP and non-goals are explicit; all twelve AST languages, including Kotlin and Swift, are P0 and cannot be silently deferred.
- Evidence: DEC-002 and EPIC-001 through EPIC-005.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: Warm, query, incremental refresh, and reject/fallback paths are explicit and can each become stories and tests.
- Evidence: WF-001 through WF-004.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: FR-001 through FR-008, BR-001 through BR-007, and AC-001 through AC-008 provide testable behavior and planning constraints.
- Evidence: discovery.md and prfaq.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite, Tree-sitter, pinned grammars, StepCard contracts, TOON-only portable machine data, offline execution, stable ordering, and bounded graph growth are explicit.
- Evidence: DEC-003 through DEC-006.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Feature 018 is the runtime base. Parser versions, hashes, wheels, and ABI proof are implementation tasks and release gates. Graph explosion, stale state, secrets, false references, and economics each require dedicated work.
- Evidence: delivery-gap-review.md Gap Matrix and EPIC-005.
- Open questions/blockers: None for decomposition.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted; there are no planning assumptions requiring user clarification.
- Evidence: decision-log.md.
- Open questions/blockers: Exact parser pins are intentionally owned by Engineering and Security with objective validation.

## Success Measures
- Confirmed facts: Each epic can trace to SM-001 through SM-007 and AC-001 through AC-008.
- Evidence: goal-capability-map.md Outcome Traceability.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon.
- Evidence: Full-flow scan fingerprint 1d2a684312dddc63fdf3bfc6d31abc1e7d4a52bd6d9e5ded4340e9f878f8a998 with gaps[0] and next_reads[0].
- Open questions/blockers: None.

## Planning Evidence
- Confirmed facts: Five measurable goals map to seven capabilities and five P0 epics without orphaned work. Roles, MVP, failure rules, dependencies, priority drivers, and release gates are explicit.
- Evidence: goal-capability-map.md tables; requirements-readiness.md score 9/10.
- Open questions/blockers: None.

## Gap Matrix
| Area | Gap | Evidence | Planning Impact | Severity | Owner |
| --- | --- | --- | --- | --- | --- |
| Parser bundle | Exact pins, hashes, wheel matrix, and ABI result must be produced | DEC-006; EPIC-005 | Create explicit packaging and install-smoke stories | Major implementation gate; not a decomposition blocker | Engineering and Security |
| Language semantics | Twelve per-language AST fixtures and extraction expectations must be executable | AC-002; AC-003 | Create one parameterized coverage story with language-specific fixture tasks | Major release gate; not a decomposition blocker | Engineering and QA |
| Graph economics | Final corpus benchmark does not exist before implementation | AC-005; AC-007 | Create boundedness, recall, and token-economics stories | Major release gate; not a decomposition blocker | QA |
| Latency | No normative latency target | SM-006 | Benchmark observationally; do not block correctness planning | Minor | Engineering |

## Priority and Scope Gaps
- Confirmed facts: No priority or scope gap blocks planning. EPIC-001 through EPIC-005 are P0 because parser completeness, graph correctness, retrieval value, fallback safety, and production evidence jointly define the MVP.
- Evidence: goal-capability-map.md Epic Map.
- Open questions/blockers: Post-MVP semantic embeddings, remote GraphRAG, and global community summaries remain excluded.

## Dependency Gaps
- Confirmed facts: No dependency is hidden. The backlog must sequence parser research and install proof before graph-complete release, schema/identity before retrieval, and graph/query implementation before economics evidence.
- Evidence: CAP-001 through CAP-007 dependencies and delivery gap matrix.
- Open questions/blockers: Parser distribution may fail on a supported target; the backlog must preserve direct-read fallback and block release rather than reduce language scope.

## Planning Verdict
- Confirmed facts: READY for backlog and story decomposition. No blocker, scope ambiguity, missing actor, missing rule, missing priority driver, or unresolved external dependency requires clarification.
- Evidence: Full-flow scan gaps[0], readiness 9/10, and complete goal-to-epic traceability.
- Open questions/blockers: Production readiness remains conditional on executable implementation evidence, not further product discovery.
