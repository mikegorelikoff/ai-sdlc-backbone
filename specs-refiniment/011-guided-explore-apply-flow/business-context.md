---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "011-guided-explore-apply-flow"
  artifact: "business-context.md"
  path: "specs-refiniment/011-guided-explore-apply-flow/business-context.md"
  workspace: "refinement"
  skill: "ai-sdlc-ba"
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
    - "DEC-002"
    - "DEC-003"
    - "DEC-007"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
  related_artifacts:
    - "specs-refiniment/011-guided-explore-apply-flow/backlog-gap-review.md"
    - "specs-refiniment/011-guided-explore-apply-flow/backlog.md"
    - "specs-refiniment/011-guided-explore-apply-flow/decision-log.md"
    - "specs-refiniment/011-guided-explore-apply-flow/delivery-gap-review.md"
    - "specs-refiniment/011-guided-explore-apply-flow/discovery.md"
    - "specs-refiniment/011-guided-explore-apply-flow/goal-capability-map.md"
    - "specs-refiniment/011-guided-explore-apply-flow/prfaq.md"
    - "specs-refiniment/011-guided-explore-apply-flow/release-slicing.md"
    - "specs-refiniment/011-guided-explore-apply-flow/requirements-readiness.md"
    - "specs-refiniment/011-guided-explore-apply-flow/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-ba"
    - "business-context"
    - "approved"
---

# business-context.md

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
Authoritative evidence reviewed: `specs-refiniment/011-guided-explore-apply-flow/decision-log.md`, `specs-refiniment/011-guided-explore-apply-flow/discovery.md`, `specs-refiniment/011-guided-explore-apply-flow/prfaq.md`, `specs-refiniment/011-guided-explore-apply-flow/delivery-gap-review.md`, `specs-refiniment/011-guided-explore-apply-flow/requirements-readiness.md`, `specs-refiniment/011-guided-explore-apply-flow/goal-capability-map.md`, `specs-refiniment/011-guided-explore-apply-flow/backlog-gap-review.md`, `specs-refiniment/011-guided-explore-apply-flow/backlog.md`, `specs-refiniment/011-guided-explore-apply-flow/user-stories.md`, `specs-refiniment/011-guided-explore-apply-flow/release-slicing.md`, `specs-refiniment/011-guided-explore-apply-flow/business-context.md`. Baselines include `specs/009-operational-feedback-hardening/requirements.md`, `specs/007-context-and-prompt-engineering/requirements.md`, `docs/reference/workflow-map.md`, `docs/reference/directory-layout.md`, and `concepts/context-and-quality.md`; stakeholder feedback and DEC-001–DEC-007 confirm scope.

## Current Behavior
Current navigation can select a recent completed feature before recognizing new-refinement intent, leaving contributors to infer skill order. Compressed context can cost more after rereads, and rationale-first review can hide bugs and readability defects.

## Desired Behavior
Explore resolves intent, feature, workspace, stage, rigor, roles, evidence, costs, writes, and blockers into a readable card. Apply recomputes hashes and state, rejects drift, executes one checkpoint, records evidence, and returns control.

## Actor and Permission Matrix
| Actor | Role | Permissions | Restrictions | Source |
| --- | --- | --- | --- | --- |
| Contributor | Contributor | Explore and accept | Intent-first Explore contract | FR-001 and AC-001 |
| Repository Maintainer | Repository Maintainer | Maintain routes and fixtures | Fingerprint and two-root safety | DEC-002 |
| Reviewer and QA | Reviewer and QA | Validate without prior rationale | Context economics and spec-first review | fixture-003 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Explore new feedback | Intent-first Explore contract | Contributor | Run Explore | Intent-first Explore contract | Intent-first Explore contract | FR-001 and AC-001 |
| Apply accepted route | Fingerprint and two-root safety | Repository Maintainer | Run Apply | Fingerprint and two-root safety | Fingerprint and two-root safety | DEC-002 |
| Review independently | Context economics and spec-first review | Reviewer and QA | Run spec-first review | Context economics and spec-first review | Context economics and spec-first review | fixture-003 |

## Business Rule Catalog
| Rule ID | Rule | Applies To | Failure Behavior | Source | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| Intent-first Explore contract | Intent-first Explore contract | Intent-first Explore contract | Intent-first Explore contract | FR-001 and AC-001 | DEC-001 |
| Fingerprint and two-root safety | Fingerprint and two-root safety | Fingerprint and two-root safety | Fingerprint and two-root safety | DEC-002 | DEC-002 |
| Context economics and spec-first review | Context economics and spec-first review | Context economics and spec-first review | Context economics and spec-first review | fixture-003 | DEC-003 |

## Acceptance Criteria
| AC ID | Given | When | Then | Rule Ref | Source |
| --- | --- | --- | --- | --- | --- |
| Intent-first Explore contract | New feedback request | Run Explore | Select this refinement with no writes | Intent-first Explore contract | FR-001 and AC-001 |
| Fingerprint and two-root safety | Accepted current decision card | Run Apply | Execute one checkpoint or block drift | Fingerprint and two-root safety | DEC-002 |
| Context economics and spec-first review | Seeded change and requirements | Run spec-first review | Detect seeded defect and readability issue | Context economics and spec-first review | fixture-003 |

## Business Context Gaps
No unresolved in-scope blocker or contradiction remains. Global installation and live telemetry are explicit exclusions; internal mechanisms are intentionally deferred to SDD. Every accepted behavior has an owner, acceptance ID, failure path, and fixture evidence.
