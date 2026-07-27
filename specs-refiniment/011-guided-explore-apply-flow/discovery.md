---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "discovery.md"
  path: "specs-refiniment/011-guided-explore-apply-flow/discovery.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
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
    - "DEC-001"
    - "DEC-007"
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
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "discovery"
    - "approved"
---

# discovery.md

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
Evidence includes stakeholder feedback and confirmed decisions dated 2026-07-26; `specs-refiniment/011-guided-explore-apply-flow/decision-log.md`; `specs/009-operational-feedback-hardening/requirements.md`; `specs/009-operational-feedback-hardening/design.md`; `specs/007-context-and-prompt-engineering/requirements.md`; `docs/reference/workflow-map.md`; `docs/reference/directory-layout.md`; and `concepts/context-and-quality.md`. The repository sources cover current routing, workspace, context, and review behavior; DEC-001 through DEC-007 cover the new value proposition and scope.

## Customer and Problem Evidence
Evidence reviewed includes the stakeholder feedback, confirmed DEC-001–DEC-007, prior routing/context specs, repository workflow and directory references, and every approved upstream artifact in this package. Evidence is local, versionable, and sufficient for fixture-based delivery planning.

## Current Process and Alternatives
The current navigator selects recent lifecycle state before it reliably resolves a new-refinement intent, and contributors must infer the order of many direct skills. Context compression can be difficult to read and its net savings are not consistently positive once rereads are counted.

## Value Proposition and Business Goals
GOAL-001 makes routing correct and safe; GOAL-002 makes context quality and economics visible; GOAL-003 makes delivery output readable and defect-sensitive. Success is measured by AC-001 through AC-010 rather than adoption telemetry in this fixture-only scope.

## Users, Roles, and Scenarios
| Role | Permission or responsibility | Expansion signal |
|---|---|---|
| Contributor | Explore, accept, and Apply one checkpoint | always |
| Maintainer | own policy, routes, fixtures, compatibility | repository change |
| Reviewer/QA | independently verify spec and defects | delivery/review stage |
| Cross-functional role | answer domain-specific questions | explicit request evidence only |

## MVP and Priorities
MVP/P0 sequence: intent and decision-card schema; fingerprinted single-step Apply; workspace safety; adaptive roles and rigor; context benchmark gate; spec-first review; compatibility, docs, and catalogs. Every increment is fixture-verifiable and the whole slice precedes making the flow the recommended entrypoint.

## Functional and Non-Functional Needs
For discovery, this section applies FR-001–FR-010, AC-001–AC-010, and DEC-001–DEC-007 to the guided Explore→Apply flow. The outcome is explicit, locally verifiable, owned by repository maintainers, and bounded to fixture-backed refinement and later SDD handoff.

## Operations, Launch, and Support
Roll out through repository docs, catalogs, and deterministic fixtures before recommending the flow by default. Maintainers support routing and compatibility; direct skills remain available during migration. No production service or customer-data operation is introduced.

## Discovery Risks and Dependencies
Highest risks are wrong feature selection, hidden context loss, unreadable output, and review anchoring. Controls are fail-closed classification, critical-anchor fixtures, explicit economics, blind review ordering, compatibility regression, and ownership by repository maintainers.
