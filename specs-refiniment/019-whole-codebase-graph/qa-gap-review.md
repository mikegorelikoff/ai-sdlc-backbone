---
type: "ai-sdlc.qa-gap-review"
title: "QA Requirements Gap Review"
description: "Testability gaps, missing rules, and QA blockers."
tags:
  - "ai-sdlc"
  - "review"
  - "qa"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:55:30Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "qa-gap-review.md"
  path: "specs-refiniment/019-whole-codebase-graph/qa-gap-review.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa-requirements-gap-review"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-005"
    - "AC-007"
    - "AC-008"
    - "BR-001"
    - "BR-010"
    - "DEC-001"
    - "DEC-006"
    - "DEC-007"
    - "SC-001"
    - "SC-002"
    - "SC-005"
    - "SC-007"
    - "SC-009"
    - "SC-012"
    - "SC-014"
    - "SC-016"
    - "SC-017"
    - "SC-019"
    - "SC-021"
    - "WF-001"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/backlog.md"
    - "specs-refiniment/019-whole-codebase-graph/business-context.md"
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-spec.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/goal-capability-map.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
    - "specs-refiniment/019-whole-codebase-graph/qa.md"
    - "specs-refiniment/019-whole-codebase-graph/release-slicing.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
    - "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa-requirements-gap-review"
    - "qa-gap-review"
    - "approved"
---

# qa-gap-review.md

## Feature Summary
- Confirmed facts: The package defines a production-gated local heterogeneous code graph for the entire safe corpus and mandatory AST semantics for twelve languages, including Kotlin and Swift.
- Evidence: delivery-spec.md FR-001 through FR-008; qa.md QA-001 through QA-012.
- Open questions/blockers: No test-design blocker. Implementation evidence remains pending and is correctly classified as a release gate.

## Actors and Stakeholders
- Confirmed facts: Consumer, operator, implementer, QA, Security, and maintainer roles have explicit permissions, restrictions, expected outcomes, and signoff ownership.
- Evidence: business-context.md Actor and Permission Matrix; qa.md Actors and Stakeholders.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: MVP includes all twelve selected languages, safe-file accounting, AST graph construction, bounded relations, incremental freshness, query/pack integration, diagnostics, offline optional installation, and direct-read fallback. Unsafe and non-source categories are explicitly excluded.
- Evidence: discovery.md Scope and Boundaries; release-slicing.md RS-0 through RS-4.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: WF-001 through WF-004 define observable end states for build, retrieval, incremental refresh, and rejection. Missing grammar, parse failure, drift, corruption, unsafe input, bounds breach, timeout, recall failure, and economics failure have deterministic fallback behavior.
- Evidence: delivery-spec.md Workflow Detail; qa.md QA-001 through QA-012.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: AC-001 through AC-008, FR-001 through FR-008, BR-001 through BR-010, USAC-001 through USAC-024, and SM-001 through SM-007 are measurable and linked. TOON-only output and no heuristic completeness are explicit.
- Evidence: delivery-spec.md Acceptance Traceability and Business Rule Detail; user-stories.md Acceptance Criteria Matrix.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite storage, offline parser operation, deterministic ordering/identity/fingerprints, atomic publication, bounded graph growth, and authoritative direct reads have observable tests.
- Evidence: discovery.md Data, Integrations, and Non-Functional Requirements; QA-005 through QA-011.
- Open questions/blockers: Exact pins and target matrix are implementation inputs, not missing expected behavior.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser bundle, AST semantic fidelity, graph bounds, freshness, retrieval recall/economics, exclusions, and backward compatibility each have an owner and release gate.
- Evidence: release-slicing.md Release Risks; qa.md Risk-Based Coverage.
- Open questions/blockers: Execution evidence is pending. Owner: Engineering, QA, and Security. Impact: release cannot pass yet. Resolution: implement and execute RS-0 through RS-4.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 resolve scope, parser technology, completeness authority, unsupported-file behavior, graph identity/bounds, offline packaging, and production gates. No unrecorded testing assumption changes expected results.
- Evidence: decision-log.md.
- Open questions/blockers: Parser version selection remains open only at implementation detail level. Owner: Engineering and Security. Impact: test data can be designed, but install tests cannot execute. Resolution: lock compatible artifacts in RS-0.

## Success Measures
- Confirmed facts: The thresholds are exact: 100 percent accounting, mandatory supported-language AST coverage or graph_complete false, zero stale accepted facts, declared fan-out/total bounds, 100 percent golden recall, at least 25 percent savings for accepted packs, and byte-identical deterministic fingerprints.
- Evidence: SM-001 through SM-007 and qa.md Signoff Criteria.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/business-context.md; specs-refiniment/019-whole-codebase-graph/delivery-spec.md; specs-refiniment/019-whole-codebase-graph/qa.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; and /Users/mikegorelikov/.agents/skills/ai-sdlc-qa-requirements-gap-review/references/qa-gap-review-framework.md.
- Evidence: Full-flow scan and direct reads of acceptance, workflow, risk, QA scenario, environment, command, and signoff ranges, including budget-omitted next reads.
- Open questions/blockers: None.

## QA Evidence Reviewed
| Evidence | Testability result |
| --- | --- |
| AC-001 through AC-008 | Observable and quantitatively gated |
| FR-001 through FR-008 | Actor/system and failure behavior specified |
| BR-001 through BR-010 | Valid/invalid behavior and fallback specified |
| USAC-001 through USAC-024 | Given/when/then outcomes cover primary and negative paths |
| SC-001 through SC-021 | Launch-critical, boundary, failure, permission, and retry coverage present |
| QA-001 through QA-012 | Actor, setup, action, expected evidence, and risk complete |
| RS-0 through RS-4 | Dependencies and promotion gates explicit |

## Testability Gap Matrix
| Area | Gap | Evidence | Test Impact | Severity | Owner | Resolution |
| --- | --- | --- | --- | --- | --- | --- |
| Parser artifacts | Versions, hashes, licenses, wheels, and ABI receipt do not exist before implementation | DEC-006; QA-001 | Install cases can be specified but not executed | High release gate; not a test-design blocker | Engineering and Security | Produce RS-0 lock and offline smoke evidence |
| Supported targets | Exact Python/platform matrix is not yet bound | QA Test Data and Environment | Parameterization awaits implementation packaging decision | High release gate; not a test-design blocker | Engineering and Security | Declare targets before implementing install matrix |
| Executable commands | Final test module and CLI paths do not exist | qa.md Validation Commands | Case intent is complete; invocation is pending | Medium implementation follow-up | Engineering and QA | Bind command paths in SDD and validation artifact |
| Real-corpus baseline | Post-implementation graph/economics measurements do not exist | AC-005; AC-007 | Expected thresholds are known; observed values pending | High release gate | QA | Run two clean repository corpus audits in RS-4 |

## Negative and Edge Coverage
- Confirmed facts: Negative coverage includes omitted/incompatible grammar, malformed AST, unsupported suffix, excluded/secret/symlink/path-escape input, dense fan-out, stale/corrupt/partial graph, source drift, changed/renamed/deleted files, ambiguous symbols, timeout, recall loss, savings below threshold, and optional-dependency absence.
- Evidence: SC-002, SC-005 through SC-007, SC-009 through SC-012, SC-014, SC-016, SC-017, SC-019 through SC-021; qa.md QA-003, QA-004, QA-006, QA-007, QA-010, QA-011.
- Open questions/blockers: None.

## Data and Environment Gaps
- Confirmed facts: Required fixture categories and deterministic controls are defined, including one minimal and one relationship-rich fixture for every language and mandatory Kotlin/Swift parity.
- Evidence: qa.md Test Data and Environment.
- Open questions/blockers: Concrete fixture files and target environments are pending. Owner: Engineering and QA. Impact: execution cannot start, but test synthesis can. Resolution: create them with the implementation and preserve the declared expected semantics.

## Blocking Questions
- Confirmed facts: The mandatory framework questions are answered: every core workflow has an outcome; roles and permissions are explicit; valid/invalid rules exist; failures define retention or direct_read; all twelve stories are P0/MVP; QA-001 through QA-012 are launch-critical.
- Evidence: business-context.md, delivery-spec.md, user-stories.md, release-slicing.md, and qa.md.
- Open questions/blockers: Zero questions block test strategy or test-case synthesis.

## QA Gap Verdict
- Confirmed facts: GO for test scope, strategy, test-case, and suite synthesis. The package is testable without inventing behavior.
- Evidence: No Blocker gap exists; four implementation-time evidence gaps have owners, impact, and resolution and do not alter expected results.
- Open questions/blockers: Production remains NO-GO until parser, implementation, security, validation, and corpus evidence closes every High release gate.
