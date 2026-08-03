---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:25:59Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "test-cases.md"
  path: "specs-refiniment/018-context-cache-runtime/test-cases.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-cases"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "QA Maintainers"
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
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "DEC-001"
    - "DEC-007"
    - "NFR-001"
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
    - "WF-001"
    - "WF-002"
    - "WF-003"
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
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-cases"
    - "test-cases"
    - "approved"
---

# test-cases.md

## Feature Summary
These executable cases prove AC-001 through AC-008 for the optional runtime cache. They cover direct parity, installed activation, fresh convergent warming, strict policy, manifest budgets, pack acceptance, aggregate observation, fault recovery, deterministic receipts, confinement, and offline behavior. Each scenario stays within the approved local runtime scope and has a concrete automated path.

## Actors and Stakeholders
Agent and contributor scenarios validate context outcomes; maintainer scenarios validate lifecycle and observations; repository-maintainer scenarios validate policy; QA owns automation and traceability; Security owns privacy and confinement assertions. Product and Architecture have no unresolved expected-result decision. No external provider, UI operator, or remote administrator appears in the case matrix.

## Scope and Boundaries
In scope are unit, component, integration, multi-process, regression, privacy, and security cases for feature 018 and sensitive feature-017 behavior. Out of scope are daemon, network, embeddings, cross-project retrieval, full GraphRAG, UI, live data, and deterministic latency thresholds. No case tests deferred behavior or assumes production credentials.

## Workflows and Failure Paths
Cases exercise WF-001 accepted cache, WF-002 direct recovery, WF-003 controlled publication, and WF-004 inspect/reset. Negative variants include absence, invalid policy, over-budget request, source drift, corrupt state, concurrent contention, timeout, missing FTS5, missing anchors, low savings, unsafe path, and raw-content sentinel. Each end state is directly observable.

## Requirements and Business Rules
TC-001 through TC-012 map FR-001 through FR-008, BR-001 through BR-006, and AC-001 through AC-008. Repository authority, conditional activation, manifest ceiling, mandatory anchors, aggregate-only observations, and non-blocking fallback are asserted as invariants. No expected result relies on implementation inspection alone.

## Data, Integrations, and Non-Functional Requirements
Each case creates an isolated temporary project with deterministic sources, policy, cache state, and installed layout. Multiprocess cases use synchronization barriers. Privacy cases seed unique sentinel text and inspect control columns. Freshness cases mutate a source before acceptance. No network integration exists. Stable fingerprints, exact fields, exit codes, and returned paths provide verifiable outcomes.

## Dependencies, Risks, and Constraints
Python, subprocess and multiprocessing, temporary filesystem writes, shared codecs, manifests, and SQLite are required. FTS5 absence has its own passing fallback expectation. Race flakiness is controlled with barriers and bounded joins; platform latency is not asserted. All destructive fixture actions remain inside disposable temporary roots.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 define every expected result. Owner: QA Maintainers. Impact: no blocking decision remains and no manual-only test is required. Next step: group these cases into smoke, regression, negative, security, and UAT suites. Latency observations remain outside fingerprints, while adapter timeout behavior is tested deterministically.

## Success Measures
The matrix is complete when every AC appears, each case has preconditions, trigger, exact outcome, layer, priority, and automation path, every P0 invariant has negative coverage, and execution can occur without external services or unstated data. Release evidence requires all P0 cases and mapped suites to pass.

## Source Coverage
Consumed sources: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/release-slicing.md; specs-refiniment/018-context-cache-runtime/business-context.md; specs-refiniment/018-context-cache-runtime/delivery-spec.md; specs-refiniment/018-context-cache-runtime/qa.md; specs-refiniment/018-context-cache-runtime/qa-gap-review.md; specs-refiniment/018-context-cache-runtime/qa-strategy.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md.

## Scenario Matrix
| Scenario ID | Requirement Ref | Type | Preconditions | Expected Outcome |
| --- | --- | --- | --- | --- |
| TC-001 | AC-001, FR-001, BR-002 | regression | optional module absent or source checkout only | StepCard returns baseline direct paths; no cache process or derived write |
| TC-002 | AC-002, FR-002 | concurrency | stale cache and multiple synchronized processes | one fresh logical fingerprint accepted; no partial state |
| TC-003 | AC-002, FR-008 | negative | source mutates while candidate builds | candidate rejected, retry bounded, then fresh accept or direct fallback |
| TC-004 | AC-003, FR-003, BR-003 | boundary | defaults, exact override, invalid field, over-budget value | exact valid values apply within manifest; invalid input safely recovers |
| TC-005 | AC-004, FR-004, BR-004 | positive-negative | valid pack plus missing-owner, missing-anchor, stale, low-savings variants | only complete fresh economical v4 is accepted |
| TC-006 | AC-005, FR-005, FR-006, BR-005 | privacy | cache outcomes and sentinel raw text | only allowlisted aggregates persist; reset empties observations |
| TC-007 | AC-006, FR-007, BR-006 | fault matrix | timeout, corruption, contention, FTS5 absence, validation failure | stable reason-coded direct reads return |
| TC-008 | AC-007, NFR-001 | determinism | identical fixture run repeatedly | receipts and fingerprints are byte-identical; timing excluded |
| TC-009 | AC-008, BR-001 | security | excluded path, symlink, offline guard | writes and reads remain confined; no network occurs |
| TC-010 | AC-001, AC-004 | integration | project-installed module and ordinary StepCard | bounded cache is used only when all acceptance gates pass |
| TC-011 | AC-002, AC-006 | recovery | corrupt accepted/control state | rebuild is safe or direct fallback returns; source remains untouched |
| TC-012 | AC-005, AC-007 | operations | warm no-op, rebuild, hit, fallback, reset | aggregate totals are deterministic and diagnosable |

## Detailed Test Cases
| Test ID | Scenario Ref | Steps | Expected Result | Priority | Automation |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | TC-001 | create absent and source-checkout layouts; compile same step | equality of direct paths and zero cache writes | P0 | `python3 skills/ai-sdlc-shared-runtime/tests/test_steps.py -v` |
| TEST-002 | TC-002 | start synchronized warmers against one stale root; join bounded | all processes complete and report one fingerprint; verify passes | P0 | `python3 skills/ai-sdlc-context-cache/tests/test_context_cache.py -v` |
| TEST-003 | TC-003 | pause candidate; mutate source; resume | stale candidate never replaces accepted state | P0 | cache lifecycle focused unittest |
| TEST-004 | TC-004 | resolve valid exact and malformed policies against a small manifest | decoded effective limits equal safe expected values | P0 | shared runtime policy focused unittest |
| TEST-005 | TC-005 | submit each pack variant to StepCard acceptance | valid candidate packed; every invalid variant uses direct paths | P0 | shared runtime StepCard integration unittest |
| TEST-006 | TC-006 | run operations with sentinel; inspect schema; reset; inspect again | sentinel absent; only allowed columns; counters empty after reset | P0 | cache observation focused unittest |
| TEST-007 | TC-007 | inject each documented failure into compilation | command exits successfully with expected reason and direct paths | P0 | parameterized shared runtime fault unittest |
| TEST-008 | TC-008 | run identical pack and receipt twice | byte equality holds and no time field participates | P0 | deterministic cache and runtime unittests |
| TEST-009 | TC-009 | create excluded symlink and deny network; warm and pack | excluded content absent; paths confined; network call count zero | P0 | cache confinement plus security tests |
| TEST-010 | TC-010 | install module into project tree; compile ordinary step | validated pack selected and mandatory direct anchors retained | P0 | installed-cache integration unittest |
| TEST-011 | TC-011 | corrupt state then warm and compile | recovery or stable direct result; no source mutation | P0 | corrupt-state cache unittest |
| TEST-012 | TC-012 | produce known outcomes; inspect totals; reset | exact allowlisted counts and token arithmetic match expected | P1 | observation lifecycle unittest |

## Permission and Negative Cases
Permission is filesystem-local: policy may narrow or tune within the manifest but cannot widen authority, and cache evidence cannot become repository instruction. Negative cases explicitly test excluded paths, symlink traversal, unknown policy fields, excessive limits, missing owner or anchors, raw-content sentinel, source drift, corrupt state, and network denial. Every violation rejects the cache result or returns direct reads.

## Expected Results
Verifiable results are command exit zero plus exact returned direct paths, packed flag, stable reason, logical fingerprint, source hashes, mandatory-anchor set, effective budget, observation column set, token totals, and filesystem confinement. Multi-process success means all bounded processes terminate and one fingerprint verifies. No case passes merely from absence of an exception or code inspection.

## Layer Mapping
Execution order: 1) unit policy, validation, allowlist, token-math, and reason tests run on every change and block component work; 2) cache component lifecycle, recovery, privacy, and confinement tests block runtime integration; 3) StepCard installed/absent and fault integration tests block regression; 4) multi-process convergence blocks release; 5) docs, install smoke, security review, and stakeholder-readable UAT block final signoff. Failure stops the current layer, fixes the cause, and reruns focused then downstream coverage.

## Automation Plan
TEST-001 through TEST-012 are automated in the existing cache and shared-runtime unittest suites; implementation test names must include TC or AC trace in docstrings or nearby specification mapping. Focused cache and StepCard commands run first, then full shared runtime, docs validators, install smoke, security testing, and patch checks. There are no manual-only cases and no unresolved decisions; human review supplements but never substitutes automated P0 evidence.
