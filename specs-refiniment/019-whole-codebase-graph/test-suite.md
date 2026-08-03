---
type: "ai-sdlc.test-suite"
title: "Test Suite"
description: "Executable smoke, regression, and acceptance suite definitions."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T20:00:55Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "test-suite.md"
  path: "specs-refiniment/019-whole-codebase-graph/test-suite.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-case-and-suite-synthesis"
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
    - "BR-010"
    - "DEC-001"
    - "DEC-007"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
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
    - "specs-refiniment/019-whole-codebase-graph/qa-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/qa-strategy.md"
    - "specs-refiniment/019-whole-codebase-graph/qa.md"
    - "specs-refiniment/019-whole-codebase-graph/release-slicing.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
    - "specs-refiniment/019-whole-codebase-graph/test-cases.md"
    - "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-case-and-suite-synthesis"
    - "test-suite"
    - "approved"
---

# test-suite.md

## Feature Summary
- Confirmed facts: The suite package groups TC-001 through TC-024 into fast feedback, risk regression, security/negative, stakeholder UAT, and full production-release execution for the twelve-language whole-codebase graph.
- Evidence: test-cases.md and qa-strategy.md.
- Open questions/blockers: No suite-design blocker; implementation is required before entry criteria can be met.

## Actors and Stakeholders
- Confirmed facts: Engineering runs focused unit/integration suites; QA runs smoke, regression, UAT, and release audit; Security signs install/offline/exclusion coverage; Harness Maintainers accept operational behavior and production verdict.
- Evidence: qa.md and qa-strategy.md.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: Suites include all P0 behaviors in TC-001 through TC-024 and P1 operational review. They exclude remote, UI, embeddings, compiler-complete semantics, and unsupported-language AST behavior.
- Evidence: test-cases.md Scope and Boundaries.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: Smoke touches all four workflows; regression covers every state/failure path; negative/security targets fail-closed boundaries; UAT demonstrates retrieval value and diagnostics; release audit repeats the complete evidence chain twice.
- Evidence: WF-001 through WF-004 and Layer Mapping.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Full suite coverage includes every AC-001 through AC-008, FR-001 through FR-008, BR-001 through BR-010, USAC-001 through USAC-024, and SM-001 through SM-007.
- Evidence: test-cases.md Scenario Matrix.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Suite oracles use TOON goldens, source fixtures, SQLite before/after state, stable hashes, bound counters, numeric recall/savings, offline network denial, and exclusion sentinels.
- Evidence: test-cases.md Expected Results and qa-strategy.md Test Data Strategy.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser lock/target matrix precedes install and parser suites; fixture manifests precede AST cases; verified graph precedes retrieval; all focused suites precede release audit.
- Evidence: release-slicing.md and test-cases.md Layer Mapping.
- Open questions/blockers: Parser and implementation assets are pending. Owner: Engineering and Security. Impact: suites are specified but not executable. Resolution: complete RS-0 and implement approved cases.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 govern suite membership and exit gates. All twelve languages appear in smoke and full regression; no language can be sampled away for release.
- Evidence: decision-log.md.
- Open questions/blockers: None.

## Success Measures
- Confirmed facts: Smoke proves the critical path is alive; regression proves all 24 cases; UAT proves user value; release audit proves two-run determinism and all SM thresholds.
- Evidence: SM-001 through SM-007 and TC-021/022.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/business-context.md; specs-refiniment/019-whole-codebase-graph/delivery-spec.md; specs-refiniment/019-whole-codebase-graph/qa.md; specs-refiniment/019-whole-codebase-graph/qa-gap-review.md; specs-refiniment/019-whole-codebase-graph/qa-strategy.md; specs-refiniment/019-whole-codebase-graph/test-cases.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; and /Users/mikegorelikov/.agents/skills/ai-sdlc-test-case-and-suite-synthesis/references/test-case-structures.md.
- Evidence: Full-flow scan and direct review of all case definitions, layer mapping, release gates, environments, and budget-omitted next reads.
- Open questions/blockers: None.

## Suite Coverage Matrix
| Suite | Purpose | Test IDs | Trigger | Environment | Owner |
| --- | --- | --- | --- | --- | --- |
| S-SMOKE | Smallest signal that install, twelve-language AST, graph, retrieval, economics, and fallback work | TC-001, TC-003, TC-007, TC-009, TC-011, TC-013, TC-015, TC-017, TC-019, TC-020 | Every merge affecting module; release target | Clean optional install; compact fixture corpus; network denied | Engineering and QA |
| S-REGRESSION | Preserve all new and feature 018 behavior | TC-001 through TC-020, TC-023, TC-024 plus existing test_context_cache.py | Every merge; dependency/schema/parser change | Temp repositories; default and optional installs | Engineering and QA |
| S-NEGATIVE-SECURITY | Prove fail-closed parser, graph, source, network, and authority boundaries | TC-002, TC-006, TC-008, TC-010, TC-012, TC-014, TC-018, TC-019, TC-022, TC-024 | Security-sensitive change; release | Network denied; fault and unsafe-input fixtures | Security and QA |
| S-UAT | Demonstrate navigation, token value, diagnostics, and recovery | TC-015, TC-016, TC-017, TC-018, TC-020 | Release candidate | Golden corpus and real repository | QA and Harness Maintainers |
| S-RELEASE | Determine production-ready verdict | TC-001 through TC-024, full existing regression, security/code review, two clean corpus runs | Release candidate only | Every declared target plus repository corpus | QA, Security, Harness Maintainers |

## Smoke Suite
1. TC-001 verifies locked offline parser bundle.
2. TC-003 accounts for the safe corpus.
3. TC-007 executes all twelve language fixtures, explicitly including Kotlin and Swift.
4. TC-009 proves clean-build determinism.
5. TC-011 proves hubs and graph bounds.
6. TC-013 proves incremental stale-fact removal.
7. TC-015 proves golden symbol/path recall.
8. TC-017 proves accepted-pack anchors and >=25 percent savings.
9. TC-019 proves deterministic fail-closed fallback.
10. TC-020 proves operational coverage/stats contract.
- Entry: implementation and compact fixtures installed. Exit: all ten pass in one clean run; any failure blocks merge/release and routes cache use to direct_read.

## Regression Suite
- Core graph regression: TC-003 through TC-016 and TC-020.
- Parser/install regression: TC-001, TC-002, TC-005 through TC-008, TC-023.
- Retrieval/economics regression: TC-015 through TC-018.
- Failure/security regression: TC-012, TC-014, TC-019, TC-024.
- Compatibility regression: existing skills/ai-sdlc-context-cache/tests/test_context_cache.py under both default and optional installations.
- Exit: every case passes; no skipped selected language, changed golden, accepted threshold waiver, or flaky retry counts as pass.

## UAT Suite
| UAT | Actor | Steps | Observable acceptance |
| --- | --- | --- | --- |
| UAT-001 / TC-015 | AI coding agent | Query a symbol, dependency, test, and spec trace | Expected paths/symbols appear in stable order with source-backed explanations |
| UAT-002 / TC-016 | Developer | Query duplicate short names | Qualified symbols remain distinct and bounded |
| UAT-003 / TC-017 | AI coding agent | Request context pack and compare direct-read baseline | Critical anchors retained and receipt reports >=25 percent savings |
| UAT-004 / TC-018 | AI coding agent | Request a deficient or uneconomical pack | direct_read reason is explicit; no partial pack is accepted |
| UAT-005 / TC-020 | Harness Maintainer | Run stats and verify twice | TOON coverage, language status, bounds, freshness, and fingerprint are understandable and stable |
- UAT supplements automation; all linked automated TCs must already pass.

## Entry Criteria
- Approved delivery-spec.md, qa.md, qa-gap-review.md, qa-strategy.md, and test-cases.md.
- Locked parser runtime/grammar artifacts with hashes, licenses, ABI proof, and declared target matrix.
- Implemented graph runtime and TC automation paths; deterministic TOON fixture manifests present for all twelve languages.
- Clean default and optional environments; SQLite FTS5; network denial; isolated temporary repositories; stable real-corpus snapshot.
- Focused lower-layer tests pass before a dependent suite begins.

## Exit Criteria
- S-SMOKE, S-REGRESSION, S-NEGATIVE-SECURITY, and S-UAT pass with no waived P0 case.
- S-RELEASE executes TC-001 through TC-024 twice where specified, AC-001 through AC-008 and SM-001 through SM-007 are fully traceable, and deterministic evidence matches.
- Parser checks pass for all twelve languages and every declared target; default install stays unchanged.
- Security and code review have no unresolved blocking/high findings; validation commands and outputs are recorded.
- Any failed, skipped, flaky, partial, below-recall, below-savings, stale, unsafe, or nondeterministic result yields production_ready: no.

## Execution Dependencies
1. RS-0 / TC-001, TC-002, TC-023: lock and verify parsers; blocks all semantic suites; failure action: stop without reducing scope.
2. Language fixtures / TC-005 through TC-008: prove twelve-language AST; blocks graph_complete; failure action: name language and fix adapter/grammar/manifest.
3. Graph/storage / TC-003, TC-004, TC-009 through TC-014, TC-019, TC-020, TC-024: prove accounting, identity, bounds, freshness, safety; blocks retrieval.
4. Retrieval/economics / TC-015 through TC-018: prove value; blocks UAT and release.
5. Smoke, regression, negative/security, UAT: each blocks release on any P0 failure.
6. S-RELEASE / TC-021 and TC-022: run full corpus twice plus reviews; only this suite may produce production_ready: yes.
- Pending assets have Owner: Engineering and Security; Impact: no suite execution; Resolution: implement in dependency order and retain direct_read until all exits pass.
