---
type: "ai-sdlc.release-slicing"
title: "Release Slicing and Readiness"
description: "MVP and release slices, sequencing, and backlog readiness."
tags:
  - "ai-sdlc"
  - "planning"
  - "release"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:54:23Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "release-slicing.md"
  path: "specs-refiniment/022-ai-sdlc-loop/release-slicing.md"
  workspace: "refinement"
  skill: "ai-sdlc-release-slicing-and-backlog-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-006"
    - "BR-001"
    - "BR-007"
    - "DEC-001"
    - "DEC-005"
    - "REQ-001"
    - "REQ-009"
    - "RISK-001"
    - "RISK-002"
    - "RISK-003"
    - "RISK-004"
    - "RISK-005"
    - "TASK-001"
    - "TASK-002"
    - "TASK-003"
    - "TASK-004"
    - "TASK-005"
    - "TASK-006"
    - "TASK-007"
    - "TASK-008"
    - "TASK-009"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/backlog.md"
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
    - "specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/discovery.md"
    - "specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md"
    - "specs-refiniment/022-ai-sdlc-loop/index.md"
    - "specs-refiniment/022-ai-sdlc-loop/prfaq.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-release-slicing-and-backlog-readiness-review"
    - "release-slicing"
    - "approved"
---

# release-slicing.md

## Feature Summary
AI SDLC Loop is a minimal, independently released AI SDLC product with one ai-sdlc skill. It converts a bounded request into an approved specification, scoped implementation, deterministic verification evidence, and an explicitly approved commit. The release objective is a smaller support surface with a compatible escalation path into AI SDLC Harness.

## Actors and Stakeholders
Contributors install and run the workflow; reviewers own specification and commit approvals; Loop maintainers own implementation, documentation, CI, release, and profile inventory; Harness maintainers own promotion validation and parent submodule integration; QA and security reviewers own regression, misuse, path-safety, secret-safety, and approval-boundary evidence.

## Scope and Boundaries
The launch scope is exactly STORY-001 through STORY-009 because installation, the safe three-stage loop, promotion compatibility, and independent publication are jointly required for the stated product outcome. Cosmetic enhancements, telemetry, deployment automation, multiple public skills, the full 18-stage runtime, and broader Harness catalog behavior are post-MVP or out of scope.

## Workflows and Failure Paths
Delivery proceeds through compatibility inventory and installer, then specification and approval primitives, scoped mutation, verification, commit approval, promotion validation, and public integration. Negative work is first-class: interrupted installation, profile drift, stale or absent approvals, path overlap, unrelated dirty work, failed or unavailable checks, incompatible artifacts, release failure, and submodule drift must stop safely with retained evidence.

## Requirements and Business Rules
The slices preserve REQ-001 through REQ-009, BR-001 through BR-007, AC-001 through AC-006, and SAC-001 through SAC-012. No slice may weaken the one-skill boundary, allow mutation before a matching specification approval, allow commit before passing evidence and matching approval, advertise unverified profiles, or claim promotion compatibility without field-fidelity fixtures.

## Data, Integrations, and Non-Functional Requirements
Release outputs include the ai-sdlc skill, installer and verifier, profile manifest, compact compatible artifacts, deterministic fingerprints, approval receipts, validation evidence, tests, security guidance, Apache-2.0 license, CI, public GitHub release, and pinned Harness submodule. Integrations are local filesystems, supported agent project roots, approved commands, Git, GitHub, and Harness fixtures. Safety and reproducibility are launch requirements.

## Dependencies, Risks, and Constraints
The critical chain is STORY-001 to STORY-002; STORY-003 to STORY-004 to STORY-005 to STORY-006 to STORY-007; then STORY-008 and STORY-009. Documentation, QA, and security tasks run alongside implementation but must converge before launch. No calendar or capacity evidence exists, so this plan uses dependency-based sequence rather than invented dates. Profile verification and schema design are implementation checks owned by maintainers.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted. Launch composition includes all nine stories because excluding any one breaks an accepted outcome or safety boundary. Owner: maintainer. Impact: one complete v0.x launch rather than a partially supported public release. Resolution and next step: execute three internal evidence slices, then select the first version only after all launch gates pass. Open questions: none that change scope.

## Success Measures
The launch passes when each verified profile installs exactly one skill, Specify emits a schema-valid compatible artifact, mutation and commit gates reject missing or stale approvals, scoped changes preserve unrelated work, relevant checks persist deterministic evidence, promotion preserves supported fields, public CI passes, and the parent submodule pins the released commit. Backlog readiness requires complete ownership, traceability, and executable acceptance coverage.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, and specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon.

## MVP Slice
The public MVP contains STORY-001 through STORY-009 and TASK-001 through TASK-009. Internally it is delivered as three evidence slices: foundation, safe loop, and compatibility/release. These slices reduce integration risk and permit early fixture validation, but none is advertised as a complete public product until approval, safety, compatibility, CI, documentation, and submodule gates all pass. There is no manual workaround for either approval boundary.

## Release Slice Matrix
| Slice | Value | Stories | Dependencies | Exit Criteria | Risks |
| --- | --- | --- | --- | --- | --- |
| Slice A — Installable foundation | Establishes the independently installable one-skill surface and verified host contract | STORY-001, STORY-002 | Harness installer source and profile fixtures; TASK-001, TASK-002 | All advertised profiles install and verify exactly one ai-sdlc skill; drift and interruption fixtures pass | Host contract drift; unsafe overwrite |
| Slice B — Safe delivery loop | Proves Specify, Implement, and Verify with two fingerprint-bound approvals | STORY-003, STORY-004, STORY-005, STORY-006, STORY-007 | Slice A; TASK-003, TASK-004, TASK-005, TASK-007 | SAC-004 through SAC-010 pass, unrelated work is preserved, and failed checks block commit readiness | Approval replay; path escape; nondeterministic evidence |
| Slice C — Compatible public launch | Proves escalation, governance, and independent distribution | STORY-008, STORY-009 | Slices A and B; TASK-006, TASK-008, TASK-009 | Promotion fidelity passes; public CI and license are visible; Harness pins the validated released commit | Schema loss; publication or submodule drift |

## Sequencing and Dependencies
Sequence 1: STORY-001 and TASK-001 establish source-backed contracts. Sequence 2: STORY-002 and TASK-002 produce install and recovery evidence. Sequence 3: STORY-003 and STORY-004 establish spec and approval primitives; security design can run in parallel. Sequence 4: STORY-005 and STORY-006 implement scoped mutation and checks while QA builds negative fixtures. Sequence 5: STORY-007 closes Git authority. Sequence 6: STORY-008 validates promotion. Sequence 7: STORY-009 publishes and pins. Documentation spans all sequences and must match verified commands.

## Milestones and Readiness
Milestone M1 exits when Slice A passes cross-profile install, verification, drift, interruption, and recovery tests. M2 exits when Slice B passes positive and negative approval, path-safety, dirty-work preservation, validation, and commit tests. M3 exits when Slice C passes promotion, documentation, license, public CI, release-resolution, and submodule-pin checks. Every story has actor, value, priority, acceptance, scenario, owner role, dependency, and task coverage; estimates await team capacity but items are technically ready for implementation planning.

## Release Risks
RISK-001 profile drift has medium likelihood and high impact; owner Loop maintainer; signal is fixture/source mismatch; mitigation is generated inventory CI. RISK-002 approval replay or stale fingerprints has medium likelihood and critical impact; owner security and developer; mitigation is fail-closed receipts and negative tests. RISK-003 unsafe paths or unrelated-work mutation has medium likelihood and critical impact; mitigation is containment and dirty-tree fixtures. RISK-004 promotion loss has low likelihood and high impact; mitigation is round-trip fixtures. RISK-005 remote install or release compromise has low likelihood and critical impact; mitigation is pinned sources, checksums where applicable, least privilege, and public CI evidence.

## Release Verdict
Ready for delivery planning, score 9/10. First, scope and priorities are explicit: all nine P0 stories are required for the accepted launch. Second, dependency sequencing and cross-functional ownership are defined without fake dates. Third, every launch requirement and failure boundary has acceptance and scenario coverage. Remaining implementation checks are source-verifying exact profile names, finalizing the compatible schema, and selecting a v0.x version after validation; their owners and gates are explicit and they do not block design start.
