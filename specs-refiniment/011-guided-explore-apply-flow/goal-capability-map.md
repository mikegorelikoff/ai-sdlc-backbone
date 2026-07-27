---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "goal-capability-map.md"
  path: "specs-refiniment/011-guided-explore-apply-flow/goal-capability-map.md"
  workspace: "refinement"
  skill: "ai-sdlc-goal-capability-and-epic-mapping"
  flow_mode: "full"
  state_file: "specs-refiniment/011-guided-explore-apply-flow/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
  status: "approved"
  owner: "Product and Repository Maintainers"
  created_at: "2026-07-26"
  updated_at: "2026-07-26"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "BR-001"
    - "BR-002"
    - "CAP-001"
    - "CAP-002"
    - "CAP-003"
    - "DEC-001"
    - "DEC-002"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
  related_artifacts:
    - "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
    - "specs-refiniment/011-guided-explore-apply-flow/delivery-gap-review.md"
    - "specs-refiniment/011-guided-explore-apply-flow/discovery.md"
    - "specs-refiniment/011-guided-explore-apply-flow/prfaq.md"
    - "specs-refiniment/011-guided-explore-apply-flow/requirements-readiness.md"
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
`ai-sdlc-flow` supplies one guided Explore→Apply entrypoint. Explore is read-only and intent-first; Apply revalidates evidence and executes exactly one bounded lifecycle checkpoint. Direct skills remain an advanced, compatible escape hatch.

## Actors and Stakeholders
Repository contributors are the primary users; maintainers own routing, policy, fixtures, and compatibility. Engineering reviewers and QA consume independent evidence. Product, BA, security, operations, and other roles join only when request evidence requires their decisions.

## Scope and Boundaries
In scope are the meta-skill contract, decision card, fingerprinted Apply, safe two-root routing, adaptive roles and rigor, context economics, spec-first review, documentation, catalogs, and local fixtures. Global installation, product-code implementation, publication, remote services, and live customer research are excluded.

## Workflows and Failure Paths
Explore classifies intent, validates context freshness, selects feature/workspace/stage, and shows evidence, cost, roles, writes, blockers, and next checkpoint. Apply rechecks the route fingerprint and performs one action. Ambiguity, drift, unsafe paths, missing anchors, or unsafe overrides block without mutation.

## Requirements and Business Rules
FR-001 intent before feature; FR-002 complete read-only decision card; FR-003 fingerprinted Apply; FR-004 one bounded action; FR-005 preserved tool-owned roots; FR-006 adaptive roles; FR-007 adaptive rigor; FR-008 transparent context economics; FR-009 independent spec-first review; FR-010 direct-skill compatibility. BR-001 fail closed and BR-002 never create unrequested paths.

## Data, Integrations, and Non-Functional Requirements
Inputs are lifecycle state, indexes, project-context metadata, policy, source hashes, and local fixtures. NFR-001 deterministic output, NFR-002 zero Explore writes, NFR-003 explainable routing, NFR-004 100% critical-anchor recall, NFR-005 at least 15% net pack savings including rereads, NFR-006 compatibility, and NFR-007 human readability apply.

## Dependencies, Risks, and Constraints
Dependencies are navigator intent classification, shared path/state/index helpers, project-context freshness, context benchmarking, policy, and review/test skills. Risks include hidden assumptions, role creep, lossy compression, reviewer anchoring, and compatibility drift. The historical `specs-refiniment` name remains a physical constraint.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 establish the meta-skill, Explore/Apply boundary, two roots, adaptive roles, pack threshold, spec-first review, and global-install exclusion. Stakeholder decisions resolve blocking product questions; later SDD work may choose internal implementation details without changing these contracts.

## Success Measures
AC-001 correct new-refinement routing; AC-002 read-only complete Explore; AC-003 drift-safe single-step Apply; AC-004 safe root fixtures; AC-005 evidence-backed roles; AC-006 explained rigor and safe overrides; AC-007 anchor/economics threshold; AC-008 blind seeded-defect detection; AC-009 compatibility; AC-010 all local gates pass.

## Source Coverage
Authoritative evidence reviewed: `specs-refiniment/011-guided-explore-apply-flow/decision-log.md`, `specs-refiniment/011-guided-explore-apply-flow/discovery.md`, `specs-refiniment/011-guided-explore-apply-flow/prfaq.md`, `specs-refiniment/011-guided-explore-apply-flow/delivery-gap-review.md`, `specs-refiniment/011-guided-explore-apply-flow/requirements-readiness.md`, `specs-refiniment/011-guided-explore-apply-flow/goal-capability-map.md`. Baselines include `specs/009-operational-feedback-hardening/requirements.md`, `specs/007-context-and-prompt-engineering/requirements.md`, `docs/reference/workflow-map.md`, `docs/reference/directory-layout.md`, and `concepts/context-and-quality.md`; stakeholder feedback and DEC-001–DEC-007 confirm scope.

## Business Goals
| Goal ID | Goal | Metric | Target | Owner | Source |
| --- | --- | --- | --- | --- | --- |
| GOAL-001 | GOAL-001 | Correct route and zero writes | 100% | Product | FR-001 and AC-001 |
| GOAL-002 | GOAL-002 | One action with drift rejection | one checkpoint | Repository Maintainers | DEC-002 |
| GOAL-003 | GOAL-003 | 100% anchors and seeded defect detection | 100% anchors; ≥15% savings | Engineering and QA | fixture-003 |

## Role Matrix
| Actor | Role | Need | Permission Boundary | Source |
| --- | --- | --- | --- | --- |
| Contributor | Contributor | Classify intent and explain Explore | Explore and accept | FR-001 and AC-001 |
| Repository Maintainer | Repository Maintainer | Revalidate and bound Apply | Maintain routes and fixtures | DEC-002 |
| Reviewer and QA | Reviewer and QA | Prove context and independent review | Validate without prior rationale | fixture-003 |

## Capability Map
| Capability ID | Capability | Goal Ref | Actors | Dependencies |
| --- | --- | --- | --- | --- |
| CAP-001 | CAP-001 | GOAL-001 | Contributor | Intent-first Explore contract |
| CAP-002 | CAP-002 | GOAL-002 | Repository Maintainer | Fingerprint and two-root safety |
| CAP-003 | CAP-003 | GOAL-003 | Reviewer and QA | Context economics and spec-first review |

## Epic Map
| Epic ID | Epic | Capability Ref | Outcome | Priority | Risks |
| --- | --- | --- | --- | --- | --- |
| EPIC-001 | EPIC-001 | CAP-001 | Correct intent-first routing | P0 | Wrong feature selection |
| EPIC-002 | EPIC-002 | CAP-002 | Safe bounded mutation | P0 | Stale or unsafe mutation |
| EPIC-003 | EPIC-003 | CAP-003 | Readable defect-sensitive evidence | P0 | Context loss and review anchoring |

## Outcome Traceability
This goal-capability-map section connects FR-001–FR-010, AC-001–AC-010, and DEC-001–DEC-007 to a bounded Explore→Apply outcome. It is owned, locally testable, readable, and ready for downstream SDD without scope expansion.
