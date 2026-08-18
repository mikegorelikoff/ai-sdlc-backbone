---
type: "ai-sdlc.goal-capability-map"
title: "Goal, Capability, and Epic Map"
description: "Business goals mapped to roles, capabilities, and outcome-oriented epics."
tags:
  - "ai-sdlc"
  - "planning"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:49:07Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "goal-capability-map.md"
  path: "specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md"
  workspace: "refinement"
  skill: "ai-sdlc-goal-capability-and-epic-mapping"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-003"
    - "AC-005"
    - "AC-006"
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-005"
    - "BR-007"
    - "CAP-001"
    - "CAP-002"
    - "CAP-003"
    - "CAP-004"
    - "CAP-005"
    - "CAP-006"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
    - "REQ-001"
    - "REQ-006"
    - "REQ-007"
    - "REQ-009"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
    - "specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/discovery.md"
    - "specs-refiniment/022-ai-sdlc-loop/index.md"
    - "specs-refiniment/022-ai-sdlc-loop/prfaq.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
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
AI SDLC Loop structures a small team delivery loop around one ai-sdlc skill, three stages, two approval boundaries, compatible artifacts, all current project hosts, and an independent public release.

## Actors and Stakeholders
Contributors initiate and inspect; reviewers authorize mutation and commit; Loop maintainers own installation, workflow, validation, release, and support; Harness maintainers own compatibility and the pinned submodule.

## Scope and Boundaries
The goal map covers only the MVP capabilities required by REQ-001 through REQ-009 and AC-001 through AC-006. Advanced Harness lifecycle stages, modules, hosted services, telemetry, deployment, and quantitative ROI claims remain out of scope.

## Workflows and Failure Paths
Capabilities follow install to Specify to approval to Implement to Verify to approval to commit. Failure capabilities must reject stale or absent approvals, unsafe or overlapping mutations, failed checks, unsupported profiles, incompatible artifacts, and release drift.

## Requirements and Business Rules
GOAL, CAP, and EPIC entries trace to DEC-001 through DEC-005, BR-001 through BR-007, REQ-001 through REQ-009, and AC-001 through AC-006. No capability exists without an approved goal or delivery necessity.

## Data, Integrations, and Non-Functional Requirements
Capabilities operate on repository-local Markdown and TOON, Git state, Python 3.10 or newer, host skill roots, and local test commands. Determinism, path containment, approval auditability, portability, recovery, and no telemetry constrain every epic.

## Dependencies, Risks, and Constraints
Installer profile source, GitHub repository creation, approval fingerprint logic, test fixtures, promotion validation, CI, and parent submodule are dependencies. Scope creep and approval replay are primary risks; every epic has a one-skill or fail-closed success condition.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted. OQ-001 is owned by the maintainer and resolved by source-verifying current profiles before implementation design is approved. The release tag remains a post-validation release choice.

## Success Measures
Goal coverage is complete when one installed skill supports every verified profile, both approval boundaries pass negative and positive tests, compatible artifacts promote without supported-field loss, relevant checks execute, and the public repository is pinned as a submodule.

## Source Coverage
The map consumes specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon, and specs-refiniment/022-ai-sdlc-loop/index.md. Together they provide approved goals, roles, requirements, acceptance, risks, dependencies, and lifecycle evidence.

## Business Goals
| Goal ID | Goal | Metric | Target | Owner | Source |
| --- | --- | --- | --- | --- | --- |
| GOAL-001 | Reduce the maintained surface for the common team workflow | Installed public skill and optional-module count | Exactly one visible skill and zero optional modules | Loop maintainer | DEC-002; REQ-001 |
| GOAL-002 | Deliver bounded code changes with explicit human authority | Approval-boundary and verification acceptance tests | All AC-003 through AC-005 positive and negative paths pass | Loop maintainer and reviewer | DEC-004; BR-002 through BR-005 |
| GOAL-003 | Preserve adoption and escalation across supported environments | Verified install profiles and promotion fidelity | Every current project profile passes and AC-006 preserves all supported fields | Loop and Harness maintainers | DEC-003; DEC-005; REQ-006; REQ-007 |

## Role Matrix
| Actor | Role | Need | Permission Boundary | Source |
| --- | --- | --- | --- | --- |
| Contributor | Workflow initiator | Turn a bounded request into reviewed and verified code | Cannot authorize its own mutation or commit unless acting as the explicit human approver | Discovery; BR-002; BR-003 |
| Reviewer | Human authority | Inspect specification and verified change set | Separate approvals are required for mutation and commit | DEC-004; AC-003; AC-005 |
| Loop maintainer | Product operator | Release and support a narrow deterministic product | Cannot expand scope outside accepted decisions without a new decision | DEC-001 through DEC-005 |
| Harness maintainer | Compatibility owner | Promote artifacts and pin a tested submodule | Accepts only schema-valid compatible output and validated commits | DEC-005; REQ-007; REQ-009 |

## Capability Map
| Capability ID | Capability | Goal Ref | Actors | Dependencies |
| --- | --- | --- | --- | --- |
| CAP-001 | Cross-host one-command installation and verification | GOAL-001; GOAL-003 | Contributor; Loop maintainer | Verified profile inventory; installer fixtures |
| CAP-002 | Compact compatible specification | GOAL-002; GOAL-003 | Contributor; reviewer | Artifact schema; request context |
| CAP-003 | Fingerprinted implementation approval and scoped mutation | GOAL-002 | Reviewer; contributor | Git fingerprint; path containment |
| CAP-004 | Deterministic relevant verification and evidence | GOAL-002 | Contributor; reviewer | Repository test discovery; command runner |
| CAP-005 | Fingerprinted commit approval and commit execution | GOAL-002 | Reviewer; contributor | Verified change fingerprint; Git identity |
| CAP-006 | Harness promotion and pinned submodule integration | GOAL-001; GOAL-003 | Loop and Harness maintainers | Compatible schema; public repository; release validation |

## Epic Map
| Epic ID | Epic | Capability Ref | Outcome | Priority | Risks |
| --- | --- | --- | --- | --- | --- |
| EPIC-001 | Installable AI SDLC Loop product shell | CAP-001; CAP-006 | Teams install one supported skill and maintainers release and pin an independent product | P0 | Host drift; scope creep; release drift |
| EPIC-002 | Approval-controlled delivery loop | CAP-002; CAP-003; CAP-004; CAP-005 | A reviewed request becomes verified code and only an explicitly approved commit | P0 | Approval replay; unsafe mutation; incomplete checks |
| EPIC-003 | Compatibility and release assurance | CAP-001 through CAP-006 | Fixtures prove installation, safety, promotion, documentation, and parent integration before release | P0 | False compatibility claims; non-reproducible commands |

## Outcome Traceability
GOAL-001 is covered by CAP-001 and CAP-006 through EPIC-001 and EPIC-003. GOAL-002 is covered by CAP-002 through CAP-005 through EPIC-002 and EPIC-003. GOAL-003 is covered by CAP-001, CAP-002, and CAP-006 through EPIC-001 and EPIC-003. Every capability maps to at least one accepted requirement and actor; no miscellaneous epic or uncovered goal remains.
