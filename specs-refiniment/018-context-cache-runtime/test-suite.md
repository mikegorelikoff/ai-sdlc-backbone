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
  at: "2026-08-03T12:27:16Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "test-suite.md"
  path: "specs-refiniment/018-context-cache-runtime/test-suite.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-case-and-suite-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "QA Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "BR-001"
    - "BR-006"
    - "DEC-001"
    - "DEC-007"
    - "TC-001"
    - "TC-002"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-009"
    - "TC-010"
    - "TC-012"
    - "WF-001"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/backlog-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/backlog.md"
    - "specs-refiniment/018-context-cache-runtime/business-context.md"
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-spec.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/qa-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/qa-strategy.md"
    - "specs-refiniment/018-context-cache-runtime/qa.md"
    - "specs-refiniment/018-context-cache-runtime/release-slicing.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
    - "specs-refiniment/018-context-cache-runtime/test-cases.md"
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
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
The suites organize TC-001 through TC-012 into a smallest launch-critical smoke set, a risk-based regression set, and stakeholder-readable UAT. Together they cover AC-001 through AC-008 without adding deferred retrieval scope. Deterministic correctness, privacy, authority, freshness, compatibility, and token economics gate release; latency remains an observation.

## Actors and Stakeholders
QA owns suite execution and evidence; Harness maintainers provide fixtures and resolve failures; repository maintainers review policy and UAT; Security approves privacy and confinement; contributors and agents are represented by UAT outcomes. No external provider or production operator is required.

## Scope and Boundaries
Suites cover local cache and StepCard behavior, feature-017 regression, multi-process lifecycle, fault recovery, policy, privacy, confinement, docs, and install layouts. They exclude daemons, network services, embeddings, full GraphRAG, UI, production data, and latency SLOs. Every included case maps to approved scope.

## Workflows and Failure Paths
Smoke proves cached success, absent direct behavior, one representative fault fallback, convergence, and privacy. Regression expands all policy, mutation, corruption, confinement, determinism, lifecycle, and operations cases. UAT demonstrates ordinary automatic reuse, safe direct recovery, and maintainer diagnosis. No failure lacks a suite.

## Requirements and Business Rules
The suite matrix covers FR-001 through FR-008, BR-001 through BR-006, AC-001 through AC-008, and WF-001 through WF-004 through TC-001 through TC-012. Authority, optional activation, manifest ceiling, anchors, aggregate privacy, and non-blocking fallback remain P0 exit gates.

## Data, Integrations, and Non-Functional Requirements
All suites use deterministic temporary repositories, local SQLite, isolated policy and cache state, controlled processes, and sentinel data. No external integration exists. Receipts, fingerprints, returned paths, source hashes, schema fields, counters, exit codes, and filesystem locations provide assertions. Timing never enters golden output.

## Dependencies, Risks, and Constraints
Execution needs Python, filesystem write access to temporary roots, subprocess and multiprocessing, shared codecs and manifests, and SQLite. FTS5 absence routes its negative case. Flaky races are controlled with barriers and bounded joins. Any partial state, privacy breach, or default drift stops the suite immediately.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 set suite boundaries. Owner: QA Maintainers. Impact: no unresolved suite decision or manual-only blocker exists. Next step: build traceability and readiness. Patched SQLite WAL, embeddings, exporters, GraphRAG, and latency thresholds remain excluded and require separate future suites.

## Success Measures
Smoke passes on every candidate handoff. Regression passes before release and after runtime, cache, manifest, codec, or docs changes. UAT passes before stakeholder acceptance. All P0 cases must pass, all ACs remain covered, no release-blocking gap is waived, and security plus documentation evidence is current.

## Source Coverage
Consumed sources: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/release-slicing.md; specs-refiniment/018-context-cache-runtime/business-context.md; specs-refiniment/018-context-cache-runtime/delivery-spec.md; specs-refiniment/018-context-cache-runtime/qa.md; specs-refiniment/018-context-cache-runtime/qa-gap-review.md; specs-refiniment/018-context-cache-runtime/qa-strategy.md; specs-refiniment/018-context-cache-runtime/test-cases.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md.

## Suite Coverage Matrix
| Suite | Purpose | Test IDs | Trigger | Environment | Owner |
| --- | --- | --- | --- | --- | --- |
| Smoke | prove launch-critical cached, direct, convergence, fallback, and privacy paths | TC-001, TC-002, TC-005, TC-006, TC-007, TC-010 | every implementation handoff and release candidate | local Python with temporary project; FTS5 positive or recoverable absence | QA |
| Regression | protect all new behavior and sensitive existing contracts | TC-001 through TC-012 | cache, runtime, policy, manifest, codec, docs, or install change | full local supported matrix | QA, Maintainers |
| UAT | prove automatic value and safe diagnosis in ordinary workflow | TC-001, TC-006, TC-007, TC-010, TC-012 | stakeholder acceptance and release candidate | project-installed and absent layouts | Repository Maintainer, QA |
| Security | prove authority, privacy, confinement, and offline boundaries | TC-005, TC-006, TC-009 | security review and release candidate | isolated offline temporary root | Security |

## Smoke Suite
Run TC-001 absent parity, TC-010 ordinary installed cache, TC-002 concurrent convergence, TC-005 accepted-pack gates, TC-007 representative fault fallback, and TC-006 observation privacy/reset. Entry requires approved cases and a clean disposable fixture. Any failed case blocks handoff; fix and rerun the focused case then the entire smoke suite.

## Regression Suite
Run TC-001 through TC-012, existing feature-017 cache tests, full shared-runtime tests, docs validators, catalog checks, install smoke, and patch checks. Trigger on every relevant runtime, cache, policy, manifest, codec, installer, or documentation change. A failure blocks release until root cause is fixed and affected plus downstream suites rerun.

## UAT Suite
A repository maintainer installs the optional module, runs an ordinary skill, observes a valid packed receipt with mandatory context, then exercises a forced fallback and inspects aggregate outcomes without raw evidence. A second absent-layout run demonstrates unchanged direct behavior. Each step uses a checklist of visible TOON fields and filesystem confinement; automation provides underlying proof.

## Entry Criteria
Approved delivery spec, QA plan, QA gap GO verdict, strategy, and test cases are required. Implementation must compile, temporary fixture creation must work, no unresolved P0 decision may exist, and active-cache environments must either expose FTS5 or enter the specified recoverable absence path. Security sentinel and offline guard must be enabled for release execution.

## Exit Criteria
All smoke, regression P0, UAT, and security cases pass with current receipts; every AC is covered; no stale or partial state appears; direct parity, manifest limits, anchors, privacy, confinement, and deterministic receipts hold; docs and install checks pass; skipped non-P0 evidence has owner and rationale. Any high security finding or P0 failure blocks.

## Execution Dependencies
Order is unit policy and validation, cache component lifecycle, StepCard integration, multi-process convergence, smoke, full regression, security, docs/install, then UAT. Each layer begins only after predecessors pass. Failures stop execution, preserve logs without raw evidence, assign an owner, fix the cause, rerun focused coverage, and then rerun every dependent suite.
