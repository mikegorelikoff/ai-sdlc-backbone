---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "qa-readiness.md"
  path: "specs-refiniment/011-guided-explore-apply-flow/qa-readiness.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa-traceability-and-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Product and Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
    - "AC-001"
    - "AC-003"
    - "AC-004"
    - "AC-007"
    - "AC-008"
    - "AC-010"
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "DEC-001"
    - "DEC-007"
    - "TC-001"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-010"
    - "TC-011"
    - "TC-014"
    - "TC-015"
    - "TC-018"
    - "TC-019"
    - "TC-020"
  related_artifacts:
    - "specs-refiniment/011-guided-explore-apply-flow/backlog-gap-review.md"
    - "specs-refiniment/011-guided-explore-apply-flow/backlog.md"
    - "specs-refiniment/011-guided-explore-apply-flow/business-context.md"
    - "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
    - "specs-refiniment/011-guided-explore-apply-flow/delivery-gap-review.md"
    - "specs-refiniment/011-guided-explore-apply-flow/delivery-spec.md"
    - "specs-refiniment/011-guided-explore-apply-flow/discovery.md"
    - "specs-refiniment/011-guided-explore-apply-flow/goal-capability-map.md"
    - "specs-refiniment/011-guided-explore-apply-flow/prfaq.md"
    - "specs-refiniment/011-guided-explore-apply-flow/qa-gap-review.md"
    - "specs-refiniment/011-guided-explore-apply-flow/qa-strategy.md"
    - "specs-refiniment/011-guided-explore-apply-flow/qa.md"
    - "specs-refiniment/011-guided-explore-apply-flow/release-slicing.md"
    - "specs-refiniment/011-guided-explore-apply-flow/requirements-readiness.md"
    - "specs-refiniment/011-guided-explore-apply-flow/test-cases.md"
    - "specs-refiniment/011-guided-explore-apply-flow/test-suite.md"
    - "specs-refiniment/011-guided-explore-apply-flow/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa-traceability-and-readiness-review"
    - "qa-readiness"
    - "approved"
---

# qa-readiness.md

## Feature Summary
`ai-sdlc-flow` provides read-only intent-first Explore and fingerprinted single-checkpoint Apply while keeping direct skills compatible. FR-001–FR-010 and AC-001–AC-010 define the complete fixture-testable contract.

## Actors and Stakeholders
Contributors verify and accept routes; maintainers own flow, policy, paths, fixtures, docs, and compatibility; Engineering and QA independently validate requirements, readability, and defects. Cross-functional participation requires explicit evidence.

## Scope and Boundaries
QA covers intent, card schema, no-write behavior, fingerprint drift, one-step mutation, roots, roles, rigor, context economics, blind review, and compatibility. Global installation, publication, live telemetry, and product code are excluded by DEC-007 and the refinement boundary.

## Workflows and Failure Paths
Explore classifies and explains a route without mutation. Apply revalidates and either performs one checkpoint or safely refuses ambiguity, drift, unsafe filesystem topology, anchor loss, or policy violation. Each outcome has a deterministic fixture and clear user-facing explanation.

## Requirements and Business Rules
FR-001–FR-010 map to AC-001–AC-010 and TC-001–TC-020. BR-001 requires fail-closed routing; BR-002 requires zero Explore writes; BR-003 guards fingerprints; BR-004 protects roots; BR-005 governs roles and context; BR-006 requires independent review.

## Data, Integrations, and Non-Functional Requirements
Tests consume synthetic lifecycle state, indexes, project-context metadata, policy, source hashes, and fixture repositories. They verify deterministic output, no Explore mutation, explainability, 100% critical-anchor recall, at least 15% net pack savings including rereads, compatibility, and readability.

## Dependencies, Risks, and Constraints
Local state/index/path helpers, context benchmark, policy, and review harness are controlled dependencies. Wrong routing, context loss, anchoring, unreadable output, and compatibility drift are covered by owned fixture suites. Network, secrets, and customer data are unnecessary.

## Decisions, Assumptions, and Open Questions
DEC-001–DEC-007 are accepted and fully represented. Owner: Product. Impact: product and QA contracts are stable. Resolution: later SDD work binds implementation mechanisms to these tests, and any contract change requires a new explicit decision plus traceability update.

## Success Measures
QA readiness requires complete FR/AC/test traceability, all P0 fixtures passing, 100% anchor recall, accepted pack savings of at least 15%, seeded P0/P1 detection, readable output, direct-skill compatibility, and the full refinement gate.

## Source Coverage
Authoritative evidence reviewed: `specs-refiniment/011-guided-explore-apply-flow/decision-log.md`, `specs-refiniment/011-guided-explore-apply-flow/discovery.md`, `specs-refiniment/011-guided-explore-apply-flow/prfaq.md`, `specs-refiniment/011-guided-explore-apply-flow/delivery-gap-review.md`, `specs-refiniment/011-guided-explore-apply-flow/requirements-readiness.md`, `specs-refiniment/011-guided-explore-apply-flow/goal-capability-map.md`, `specs-refiniment/011-guided-explore-apply-flow/backlog-gap-review.md`, `specs-refiniment/011-guided-explore-apply-flow/backlog.md`, `specs-refiniment/011-guided-explore-apply-flow/user-stories.md`, `specs-refiniment/011-guided-explore-apply-flow/release-slicing.md`, `specs-refiniment/011-guided-explore-apply-flow/business-context.md`, `specs-refiniment/011-guided-explore-apply-flow/delivery-spec.md`, `specs-refiniment/011-guided-explore-apply-flow/qa.md`, `specs-refiniment/011-guided-explore-apply-flow/qa-gap-review.md`, `specs-refiniment/011-guided-explore-apply-flow/qa-strategy.md`, `specs-refiniment/011-guided-explore-apply-flow/test-cases.md`, `specs-refiniment/011-guided-explore-apply-flow/test-suite.md`. Baseline routing, context, workflow, directory, and quality sources are also covered.

## Requirement-to-Test Traceability
| Requirement | Acceptance Ref | Test IDs | Suite | Status | Gap |
| --- | --- | --- | --- | --- | --- |
| FR-001–FR-004 | AC-001–AC-003 | TC-001–TC-006 | Smoke and Regression | covered | Closed by routing, no-write, and drift fixtures |
| FR-005–FR-008 | AC-004–AC-007 | TC-007–TC-014 | Regression | covered | Closed by root, role, rigor, and context fixtures |
| FR-009–FR-010 | AC-008–AC-010 | TC-015–TC-020 | Regression and UAT | covered | Closed by review and compatibility fixtures |

## Risk Coverage
Wrong feature selection is controlled by TC-001; mutation drift and root attacks by TC-005–TC-010; context loss by TC-011–TC-014; review anchoring and readability by TC-015–TC-018; compatibility drift by TC-019–TC-020. Owners and failure impact are recorded in the suite.

## Coverage Gaps
All in-scope requirements have planned tests, suites, owners, expected results, and negative cases. Owner: QA. Impact: complete planned coverage supports implementation. Resolution: the later SDD binds these stable cases to code-level commands; explicit exclusions need no feature coverage.

## Execution Readiness Evidence
| Evidence Area | Required Signal | Present | Gap | Impact |
| --- | --- | --- | --- | --- |
| Routing and Explore | Correct intent plus zero writes | yes | Closed by TC-001–TC-004 | Safe entry is testable |
| Apply and workspace | Fingerprint drift and root attacks | yes | Closed by TC-005–TC-010 | Mutation safety is testable |
| Context, review, compatibility | Economics, seeded defects, direct skills | yes | Closed by TC-011–TC-020 | Quality and migration are testable |

## Blocked Coverage
Every in-scope case has local synthetic data, an execution surface, and an accountable owner. Owner: QA and Repository Maintainers. Impact: execution can proceed locally after SDD bindings exist. Resolution: bind TC-001–TC-020 to implementation tests during SDD; external services and sensitive data are unnecessary.

## QA Readiness Verdict
**READY FOR SDD AND QA IMPLEMENTATION.** Traceability is complete, risks have owned tests, execution inputs are local, and acceptance thresholds are numeric. QA will withhold final release signoff until the implemented fixtures and manual readability review pass.
