---
type: "ai-sdlc.requirements-readiness"
title: "Requirements Readiness Review"
description: "Requirements quality assessment and readiness verdict."
tags:
  - "ai-sdlc"
  - "review"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:38:09Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "requirements-readiness.md"
  path: "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
  workspace: "refinement"
  skill: "ai-sdlc-requirements-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "BR-001"
    - "BR-007"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "WF-001"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-requirements-readiness-review"
    - "requirements-readiness"
    - "approved"
---

# requirements-readiness.md

## Feature Summary
- Confirmed facts: Feature 019 adds a deterministic local heterogeneous code graph to the feature 018 cache for twelve Tree-sitter languages: TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift.
- Evidence: discovery.md, prfaq.md, and delivery-gap-review.md.
- Open questions/blockers: None for requirements readiness.

## Actors and Stakeholders
- Confirmed facts: Developers and AI agents consume retrieval; Harness Maintainers own implementation and packaging; QA owns deterministic coverage, recall, and economics; Security owns exclusions and dependency review.
- Evidence: upstream Actors and Stakeholders sections.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: MVP includes complete safe-file accounting, twelve-language AST extraction, stable nodes and typed bounded edges, incremental refresh, symbol-aware query and pack, TOON receipts, safe fallback, tests, docs, and install smoke. Remote calls, runtime downloads, LLM extraction, and heuristic completeness are excluded.
- Evidence: DEC-002 through DEC-006 and upstream MVP.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: WF-001 through WF-004 define atomic warm, bounded query traversal, incremental refresh, and explicit rejection/direct-read fallback.
- Evidence: discovery.md Acceptance Criteria and Workflows; delivery-gap-review.md.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: FR-001 through FR-008, BR-001 through BR-007, and AC-001 through AC-008 are observable and traceable. AST completeness requires successful Tree-sitter parsing for all selected-language files.
- Evidence: discovery.md Requirements and Business Rules plus Acceptance Criteria; prfaq.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite is derived local storage; Tree-sitter grammars are pinned and preinstalled; runtime is offline; machine contracts are TOON; identical inputs produce byte-stable IDs, ordering, ranking, receipts, and fingerprints.
- Evidence: DEC-003, DEC-005, DEC-006.
- Open questions/blockers: Package versions and hashes are implementation evidence, not an unresolved product rule.

## Dependencies, Risks, and Constraints
- Confirmed facts: Feature 018, Python, SQLite FTS5, Tree-sitter, twelve grammars, and shared StepCard contracts are required. ABI drift, incomplete AST coverage, graph explosion, stale publication, and secret ingestion have named release gates.
- Evidence: discovery risks, prfaq launch risks, delivery gap matrix.
- Open questions/blockers: No design blocker; parser bundle proof blocks release.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted. No material product assumption is hidden. Kotlin and Swift are required first-class languages.
- Evidence: decision-log.md and explicit user direction.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: Gates require complete safe-file accounting and selected-language AST coverage, zero stale accepted nodes, bounded edges, full golden recall, at least 25 percent pack savings, and deterministic fingerprints.
- Evidence: SM-001 through SM-007 and AC-001 through AC-008.
- Open questions/blockers: Latency remains observational.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon.
- Evidence: requirements_readiness_score.py full-flow fingerprint a5279f8a8203d746d35b3a4abb384c02a9ac7c189847a002a10985959afc4d18 with gaps[0] and next_reads[0].
- Open questions/blockers: None.

## Readiness Score
- Confirmed facts: 9/10, Ready for downstream planning, design, and implementation.
- Evidence: Every checklist dimension has explicit evidence and acceptance criteria; the one remaining point is reserved for implementation-time parser bundle and ABI proof.
- Open questions/blockers: None for proceeding.

## Dimension Assessment
| Dimension | Evidence | Status | Gap | Owner |
| --- | --- | --- | --- | --- |
| Customer and problem | Explicit repeated-search and token-cost pain | Ready | None | Product |
| Value | Faster symbol-aware retrieval and >=25 percent pack savings | Ready | None | Product and QA |
| Scope | Twelve languages, MVP, and non-goals explicit | Ready | None | Architecture |
| Scenarios | WF-001 through WF-004 | Ready | None | Engineering |
| Acceptance | AC-001 through AC-008 | Ready | None | QA |
| Risks | P0 risks have release gates | Ready with implementation evidence | Parser bundle proof | Engineering and Security |
| Decisions | DEC-001 through DEC-007 accepted | Ready | None | Harness Maintainers |

## Blocking Gaps
- Confirmed facts: No requirements blocker remains.
- Evidence: Full-flow readiness scan reports gaps[0]; delivery gap review reports GO.
- Open questions/blockers: Parser versions, hashes, wheel availability, and ABI compatibility block production release if unproven, but do not block design or implementation.

## Required Follow-Up
- Confirmed facts: Engineering must select and pin the parser bundle, implement per-language fixtures, and prove offline installation. QA must verify AC-001 through AC-008; Security must review supply chain and exclusions.
- Evidence: DEC-006, DEC-007, and delivery gap matrix.
- Open questions/blockers: Follow-up owners and exit evidence are explicit.

## Readiness Verdict
- Confirmed facts: READY for goal/capability mapping and the remaining full-flow cascade. Downstream work can proceed without inventing customer, scope, workflow, safety, or acceptance behavior.
- Evidence: Score 9/10; all required dimensions ready; scan gaps[0].
- Open questions/blockers: Production release remains conditional on complete implementation and verification evidence.
