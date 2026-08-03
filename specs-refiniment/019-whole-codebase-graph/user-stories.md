---
type: "ai-sdlc.user-stories"
title: "User Story Decomposition"
description: "User stories, acceptance criteria, scenarios, priority, and value."
tags:
  - "ai-sdlc"
  - "planning"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:44:37Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "user-stories.md"
  path: "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  workspace: "refinement"
  skill: "ai-sdlc-user-story-decomposition"
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
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "EPIC-005"
    - "SC-001"
    - "SC-002"
    - "SC-003"
    - "SC-004"
    - "SC-005"
    - "SC-006"
    - "SC-007"
    - "SC-008"
    - "SC-009"
    - "SC-010"
    - "SC-011"
    - "SC-012"
    - "SC-013"
    - "SC-014"
    - "SC-015"
    - "SC-016"
    - "SC-017"
    - "SC-018"
    - "SC-019"
    - "SC-020"
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
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-user-story-decomposition"
    - "user-stories"
    - "approved"
---

# user-stories.md

## Feature Summary
- Confirmed facts: Twelve actor-based MVP stories cover the complete path from pinned parsers and safe corpus accounting through AST graph construction, retrieval, fallback, and production evidence.
- Evidence: backlog.md and EPIC-001 through EPIC-005.
- Open questions/blockers: None.

## Actors and Stakeholders
- Confirmed facts: Stories name Security Engineer, Harness Maintainer, Software Engineer, QA Engineer, AI coding agent, and Developer outcomes; ownership never grants extra authority.
- Evidence: goal-capability-map.md Role Matrix.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift are equally required. Unsupported safe text remains lexical evidence with unsupported_ast.
- Evidence: DEC-002 through DEC-004.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: Primary, alternate, boundary, negative, failure/retry, and support/admin scenarios cover warm, incremental refresh, query, pack, diagnostics, corruption, missing grammar, unsafe source, and install failure.
- Evidence: WF-001 through WF-004 and Scenario Coverage Matrix.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Story acceptance criteria refine AC-001 through AC-008 without changing the accepted business rules.
- Evidence: discovery.md Acceptance Criteria and Acceptance Criteria Matrix.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Stories require local SQLite, pinned offline Tree-sitter parsers, stable identifiers and ordering, typed bounded traversal, TOON-only portable receipts, and direct-read authority.
- Evidence: DEC-003 through DEC-006.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser proof and fixtures precede graph-complete; schema precedes query; full behavior precedes release verification. Risks have negative scenarios and owned acceptance.
- Evidence: backlog.md Priorities and Dependencies.
- Open questions/blockers: None.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted; all stories are P0/MVP and use no hidden assumption.
- Evidence: decision-log.md.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: The story set proves complete accounting and AST coverage, zero stale acceptance, bounded graph growth, full golden recall, at least 25 percent pack savings, and deterministic fingerprints.
- Evidence: SM-001 through SM-007.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon.
- Evidence: Full-flow story scan fingerprint 11904e43d9a730104ca3dad2411ed2f971b5797e8e00676aaee41d9c190e0723.
- Open questions/blockers: Scenario coverage is supplied below; no upstream product gap remains.

## Story Detail Matrix
| Story ID | Epic ID | Actor | Story | Value | Priority | MVP |
| --- | --- | --- | --- | --- | --- | --- |
| US-001 | EPIC-001 | Security Engineer | As a Security Engineer, I want a pinned and hash-verified offline parser bundle so that graph construction has a reviewable supply chain | Safe reproducible installation | P0 | Yes |
| US-002 | EPIC-001 | Harness Maintainer | As a Harness Maintainer, I want every safe file classified and accounted for so that whole-codebase claims are auditable | Complete corpus visibility | P0 | Yes |
| US-003 | EPIC-001 | Software Engineer | As a Software Engineer, I want AST-derived symbols and occurrences for all twelve languages so that navigation is precise | Trustworthy code intelligence | P0 | Yes |
| US-004 | EPIC-001 | QA Engineer | As a QA Engineer, I want executable fixtures for every language so that graph-complete is evidence-backed | Prevent false completeness | P0 | Yes |
| US-005 | EPIC-002 | Software Engineer | As a Software Engineer, I want stable heterogeneous graph records so that identical source yields identical evidence | Determinism and traceability | P0 | Yes |
| US-006 | EPIC-002 | Software Engineer | As a Software Engineer, I want bounded typed relations and trace hubs so that graph size cannot explode | Predictable local cost | P0 | Yes |
| US-007 | EPIC-002 | Harness Maintainer | As a Harness Maintainer, I want incremental atomic refresh so that accepted graph facts never become stale | Fresh reliable retrieval | P0 | Yes |
| US-008 | EPIC-003 | AI coding agent | As an AI coding agent, I want lexical plus bounded graph search so that I can find definitions and dependencies with fewer reads | Faster focused context | P0 | Yes |
| US-009 | EPIC-003 | AI coding agent | As an AI coding agent, I want budgeted deterministic packs so that context savings do not sacrifice required evidence | Token efficiency | P0 | Yes |
| US-010 | EPIC-004 | Harness Maintainer | As a Harness Maintainer, I want coverage diagnostics and explicit fallback reasons so that failures are safe and actionable | Operability and authority safety | P0 | Yes |
| US-011 | EPIC-005 | QA Engineer | As a QA Engineer, I want end-to-end graph gates so that production claims are reproducible | Release confidence | P0 | Yes |
| US-012 | EPIC-005 | Security Engineer | As a Security Engineer, I want install and exclusion validation so that the optional module remains offline and safe | Secure production adoption | P0 | Yes |

## Acceptance Criteria Matrix
| AC ID | Story ID | Given | When | Then | Rule Covered |
| --- | --- | --- | --- | --- | --- |
| USAC-001 | US-001 | Clean supported environment and locked artifacts | Optional module installs | All parser artifacts match pins and hashes with no runtime download | AC-006 |
| USAC-002 | US-001 | Missing or ABI-incompatible grammar | Parser preflight runs | Graph-complete is rejected with deterministic reason | AC-003; AC-006 |
| USAC-003 | US-002 | Safe repository corpus | Discovery runs twice | Every file has one stable accounted status and fingerprints match | AC-001; AC-004 |
| USAC-004 | US-002 | Unsupported safe text | Warm completes | File stays searchable and is marked unsupported_ast | AC-008 |
| USAC-005 | US-003 | Valid fixtures for twelve languages | AST extraction runs | Expected definitions, occurrences, imports, containment, and provable references are emitted | AC-002 |
| USAC-006 | US-003 | Parser returns errors beyond policy | Warm evaluates coverage | Graph-complete is false; heuristic output cannot substitute | AC-003 |
| USAC-007 | US-004 | Fixture matrix including Kotlin and Swift | Coverage suite runs | All twelve languages pass expected-node and expected-edge assertions | AC-002; AC-003 |
| USAC-008 | US-004 | One fixture deliberately lacks a grammar | Coverage suite runs | Suite fails with the named language and no reduced-scope success | AC-002 |
| USAC-009 | US-005 | Identical normalized inputs | Graph builds twice | Node, occurrence, edge, ordering, and graph fingerprints are byte-identical | AC-004 |
| USAC-010 | US-005 | Schema upgrade from feature 018 | Warm runs | Publication is atomic and old derived schema is not partially accepted | AC-004 |
| USAC-011 | US-006 | Repeated trace IDs and dense references | Edge construction runs | Hub and relation limits hold without pairwise clique expansion | AC-005 |
| USAC-012 | US-006 | Fan-out policy breach | Verification runs | Graph is rejected and direct_read reason names the breached policy | AC-005; AC-008 |
| USAC-013 | US-007 | Changed and deleted files | Incremental warm completes | Only affected facts change and zero removed facts remain accepted | AC-004 |
| USAC-014 | US-007 | Source changes during warm | Publication recheck runs | Candidate graph is discarded and previous valid graph remains | AC-008 |
| USAC-015 | US-008 | Golden symbol/path queries | Query runs | All expected evidence appears in stable rank order | AC-007 |
| USAC-016 | US-008 | Ambiguous same-name symbols | Typed traversal runs | Results retain qualified identities and bounded explanations | AC-004; AC-005 |
| USAC-017 | US-009 | Candidate pack meets recall and savings | Pack compiles | Critical anchors are retained and savings are at least 25 percent | AC-007 |
| USAC-018 | US-009 | Pack misses anchors or savings threshold | Pack compiles | Result is direct_read with explicit reason | AC-008 |
| USAC-019 | US-010 | Missing grammar, parse error, stale/corrupt graph, timeout, or unsafe source | Query or warm runs | TOON receipt is deterministic and direct reads remain authoritative | AC-006; AC-008 |
| USAC-020 | US-010 | Healthy graph | Stats runs twice | Coverage, language, node, edge, bound, and fingerprint fields match | AC-004 |
| USAC-021 | US-011 | Golden and real repository corpora | Full suite runs twice | SM-001 through SM-007 pass with stable evidence | AC-001 through AC-008 |
| USAC-022 | US-011 | Any release gate fails | Release audit runs | Production-ready verdict is withheld | DEC-007 |
| USAC-023 | US-012 | Supported install targets | Offline smoke runs | Optional install and twelve-parser preflight pass without network | AC-006 |
| USAC-024 | US-012 | Secret, ignored, oversized, binary, or symlink input | Discovery runs | Input is excluded with safe accounting and no content leakage | AC-001; AC-008 |

## Scenario Coverage Matrix
| Scenario ID | Story ID | Type | Trigger | Expected Outcome | AC Ref |
| --- | --- | --- | --- | --- | --- |
| SC-001 | US-001 | Primary | Install parser module | Pinned bundle verifies | USAC-001 |
| SC-002 | US-001 | Failure/retry | ABI mismatch | Graph acceptance blocks deterministically | USAC-002 |
| SC-003 | US-002 | Primary | Discover mixed corpus | Every safe file accounted | USAC-003; USAC-004 |
| SC-004 | US-003 | Primary | Parse twelve fixtures | AST facts emitted | USAC-005 |
| SC-005 | US-003 | Negative | Parse error beyond policy | No completeness claim | USAC-006 |
| SC-006 | US-004 | Boundary | Kotlin and Swift fixtures | Same mandatory gate as other languages | USAC-007 |
| SC-007 | US-004 | Negative | Grammar omitted | Coverage suite fails named language | USAC-008 |
| SC-008 | US-005 | Alternate | Repeat full build | Byte-stable graph | USAC-009 |
| SC-009 | US-006 | Boundary | Dense trace/reference corpus | Bounds and hubs hold | USAC-011 |
| SC-010 | US-006 | Negative | Bound breach | Reject and fallback | USAC-012 |
| SC-011 | US-007 | Primary | Modify/delete source | Affected facts refresh, stale facts disappear | USAC-013 |
| SC-012 | US-007 | Failure/retry | Source mutates mid-build | Candidate discarded; prior graph retained | USAC-014 |
| SC-013 | US-008 | Primary | Query symbol/path | Expected evidence returned | USAC-015 |
| SC-014 | US-008 | Alternate | Ambiguous name | Qualified bounded results | USAC-016 |
| SC-015 | US-009 | Primary | Economical pack | Accepted at >=25 percent savings | USAC-017 |
| SC-016 | US-009 | Negative | Recall/economics fails | direct_read | USAC-018 |
| SC-017 | US-010 | Support/admin | Inspect failure | Deterministic TOON diagnostics | USAC-019; USAC-020 |
| SC-018 | US-011 | Primary | Full release suite twice | All gates stable and passing | USAC-021 |
| SC-019 | US-011 | Negative | Any gate fails | No production-ready claim | USAC-022 |
| SC-020 | US-012 | Permission | Unsafe or secret path | Excluded without leakage | USAC-024 |
| SC-021 | US-012 | Boundary | Supported offline target | Install and parser preflight pass | USAC-023 |

## Story Dependencies and Risks
- Confirmed facts: US-001/US-002 precede US-003/US-004; US-005/US-006 precede US-007 through US-010; US-011/US-012 close the release. Parser unavailability, AST ambiguity, stale publication, graph explosion, recall loss, token regression, and unsafe ingestion each have a blocking AC.
- Evidence: Matrices above and backlog.md dependencies.
- Open questions/blockers: None.

## Story Readiness
- Confirmed facts: Every story has a concrete actor, value, P0/MVP status, dependencies, at least one primary acceptance criterion, and negative/boundary coverage where risk requires it. Test cases can be derived without inventing behavior.
- Evidence: Story, acceptance, and scenario matrices; full-flow scan.
- Open questions/blockers: Ready for release slicing and QA synthesis.
