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
  at: "2026-08-17T10:52:57Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "user-stories.md"
  path: "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
  workspace: "refinement"
  skill: "ai-sdlc-user-story-decomposition"
  flow_mode: "full"
  state_file: "specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
  status: "approved"
  owner: "maintainer"
  created_at: "2026-08-17"
  updated_at: "2026-08-17"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "CAP-001"
    - "CAP-006"
    - "DEC-001"
    - "DEC-002"
    - "DEC-005"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "REQ-001"
    - "REQ-002"
    - "REQ-004"
    - "REQ-005"
    - "REQ-006"
    - "REQ-007"
    - "REQ-008"
    - "REQ-009"
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
AI SDLC Loop is a separately released, minimal member of the AI SDLC product family. It exposes one user-facing ai-sdlc skill and guides a bounded change through Specify, Implement, and Verify while preserving compatible evidence for later promotion into AI SDLC Harness. The product reduces the maintained support surface without claiming reduced model-call volume.

## Actors and Stakeholders
Contributors provide bounded requests and review results. Reviewers grant or reject the two explicit approvals. Loop maintainers own the package, compatibility inventory, tests, documentation, and releases. Harness maintainers validate artifact promotion and the pinned parent-repository submodule. Security and QA reviewers validate safety boundaries and release evidence.

## Scope and Boundaries
Scope includes one visible skill, a one-command installer, all source-verified Harness project profiles, compatible specification and verification artifacts, approval-bound mutation and commit behavior, deterministic relevant checks, a public Apache-2.0 repository, CI, and parent submodule integration. Full Harness orchestration, multiple public skills, telemetry, and unapproved code or Git mutation are excluded.

## Workflows and Failure Paths
The primary workflow installs and verifies ai-sdlc, creates a compact specification with a fingerprint, requests approval, applies only the approved scoped mutation, runs relevant checks, records evidence, requests a second approval, and commits only after approval. Missing, rejected, stale, or mismatched approvals fail closed. Unsupported profiles, unsafe paths, interrupted installation, artifact drift, failed checks, and incompatible promotion produce actionable errors without destructive cleanup.

## Requirements and Business Rules
Stories cover REQ-001 through REQ-009, AC-001 through AC-006, BR-001 through BR-007, DEC-001 through DEC-005, CAP-001 through CAP-006, and EPIC-001 through EPIC-003. BR-001 fixes the public surface at one skill. BR-002 and BR-003 require a current specification approval before mutation. BR-004 requires deterministic verification evidence. BR-005 requires a current verified-change approval before commit. BR-006 preserves promotion compatibility, and BR-007 requires fail-closed behavior.

## Data, Integrations, and Non-Functional Requirements
The implementation produces a skill package, installation manifest, compact Markdown and TOON state, content fingerprints, approval receipts, validation evidence, test fixtures, CI configuration, and public documentation. Integrations are limited to verified agent project profiles, the local filesystem, approved test commands, Git, GitHub release hosting, and Harness promotion. Outputs must be deterministic, inspectable, path-safe, secret-safe, and Apache-2.0 licensed.

## Dependencies, Risks, and Constraints
STORY-001 must establish the authoritative profile inventory before installer claims. Specification and approval primitives precede mutation; mutation precedes verification; verification precedes commit approval. Promotion fixtures precede parent submodule publication. Principal risks are host drift, ambiguous approval scope, unsafe path handling, mutation of unrelated dirty work, nondeterministic evidence, remote-install compromise, and compatibility loss. Tests and fail-closed contracts mitigate each risk.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted and govern the product name, repository, single-skill interface, three-stage workflow, two approval gates, compatibility target, public licensing, and submodule location. The support objective is reduced maintained surface, not fewer requests or model calls. Open questions: none. Owner: maintainer. Impact: none on current scope. Resolution and next step: derive exact profile names and schema details from repository source during design and lock them with fixtures before release.

## Success Measures
Release readiness requires every advertised profile to install exactly one visible ai-sdlc skill, schema-valid artifacts to promote without supported-field loss, all mutation and commit bypass cases to fail closed, deterministic relevant checks to retain evidence, and public CI to pass. Support success is measured by a materially smaller maintained command, workflow, and documentation surface than AI SDLC Harness.

## Source Coverage
Canonical inputs are specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, and specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon. All story, acceptance, scenario, dependency, priority, and readiness claims trace to these sources.

## Story Detail Matrix
| Story ID | Epic ID | Actor | Story | Value | Priority | MVP |
| --- | --- | --- | --- | --- | --- | --- |
| STORY-001 | EPIC-001 | Loop maintainer | As a Loop maintainer, I want a source-verified supported-profile inventory so compatibility claims remain accurate. | Prevents unsupported installation promises. | P0 | Yes |
| STORY-002 | EPIC-001 | Contributor | As a contributor, I want one command to install and verify exactly one ai-sdlc skill in any supported project profile. | Makes first use small and consistent. | P0 | Yes |
| STORY-003 | EPIC-002 | Contributor | As a contributor, I want a bounded request converted into a compact compatible specification and fingerprint. | Creates an auditable mutation boundary. | P0 | Yes |
| STORY-004 | EPIC-002 | Reviewer | As a reviewer, I want to approve or reject code mutation against the current specification fingerprint. | Prevents unapproved implementation. | P0 | Yes |
| STORY-005 | EPIC-002 | Contributor | As a contributor, I want only approved scoped changes applied while unrelated work is preserved. | Protects user-owned repository state. | P0 | Yes |
| STORY-006 | EPIC-002 | Contributor | As a contributor, I want relevant deterministic checks selected, executed, and recorded. | Produces reproducible verification evidence. | P0 | Yes |
| STORY-007 | EPIC-002 | Reviewer | As a reviewer, I want to approve or reject commit creation against the verified-change fingerprint. | Prevents unapproved Git history mutation. | P0 | Yes |
| STORY-008 | EPIC-003 | Harness maintainer | As a Harness maintainer, I want Loop artifacts promoted without supported-field loss. | Preserves an upgrade path into the full product. | P0 | Yes |
| STORY-009 | EPIC-003 | Loop maintainer | As a Loop maintainer, I want a public versioned repository pinned as a Harness submodule. | Enables independent release and governed integration. | P0 | Yes |

## Acceptance Criteria Matrix
| AC ID | Story ID | Given | When | Then | Rule Covered |
| --- | --- | --- | --- | --- | --- |
| SAC-001 | STORY-001 | Current Harness installer source and tests | The compatibility inventory is generated and checked | Every advertised profile is source-backed and fixture-covered | REQ-006, AC-001 |
| SAC-002 | STORY-002 | A clean fixture for any supported profile | The documented install command and verification run | Exactly one visible ai-sdlc skill is installed and verification succeeds | REQ-001, AC-001, BR-001 |
| SAC-003 | STORY-002 | Invalid, interrupted, drifted, or unsupported installation state | Installation or verification runs | It fails safely with actionable recovery and preserves unrelated files | BR-007 |
| SAC-004 | STORY-003 | A bounded valid change request | Specify completes | A schema-valid compatible artifact and deterministic fingerprint are persisted before mutation | REQ-002, AC-002, BR-002 |
| SAC-005 | STORY-004 | Missing, rejected, stale, or mismatched specification approval | Implement is requested | Code mutation is blocked with no repository changes | AC-003, BR-003 |
| SAC-006 | STORY-004 | An approval matching the current specification fingerprint | Implement is requested | The workflow may enter scoped mutation and records the approval receipt | AC-003, BR-003 |
| SAC-007 | STORY-005 | An approved specification and a repository with unrelated dirty work | Scoped implementation completes | Only approved paths change and unrelated user work remains byte-for-byte intact | REQ-004, BR-007 |
| SAC-008 | STORY-006 | An approved implemented change | Verify runs | Relevant deterministic checks run, evidence persists, and any failure blocks commit readiness | REQ-005, AC-004, BR-004 |
| SAC-009 | STORY-007 | Missing, rejected, stale, or mismatched verified-change approval | Commit is requested | Commit creation is blocked and the index and history remain unchanged | AC-005, BR-005 |
| SAC-010 | STORY-007 | A passing evidence set and matching verified-change approval | Commit is requested | Exactly the approved change is committed with traceable evidence | REQ-005, AC-005, BR-005 |
| SAC-011 | STORY-008 | A valid Loop artifact or an incompatible fixture | Promotion validation runs | Valid content is preserved without supported-field loss and incompatible content is rejected explicitly | REQ-007, AC-006, BR-006 |
| SAC-012 | STORY-009 | Passing release evidence and an approved version | Publication and parent integration run | The public Apache-2.0 repository, CI, release, and pinned products/ai-sdlc-loop submodule are verifiable | REQ-008, REQ-009, DEC-002 |

## Scenario Coverage Matrix
| Scenario ID | Story ID | Type | Trigger | Expected Outcome | AC Ref |
| --- | --- | --- | --- | --- | --- |
| SCN-001 | STORY-001 | Primary | Maintainer refreshes profiles after Harness changes | Inventory and fixtures agree or CI reports exact drift | SAC-001 |
| SCN-002 | STORY-002 | Primary | Contributor installs into each supported clean profile | One ai-sdlc skill is visible and verified | SAC-002 |
| SCN-003 | STORY-002 | Failure | Install is interrupted or existing files conflict | Operation stops safely and provides recovery guidance | SAC-003 |
| SCN-004 | STORY-003 | Primary | Contributor submits a bounded request | Compatible spec and fingerprint are created | SAC-004 |
| SCN-005 | STORY-004 | Permission | Contributor attempts mutation without current approval | Mutation is denied with no code changes | SAC-005 |
| SCN-006 | STORY-004 | Primary | Reviewer approves the current spec fingerprint | Implement becomes eligible and receipt is stored | SAC-006 |
| SCN-007 | STORY-005 | Boundary | Approved paths overlap unrelated dirty work | Unsafe overlap is rejected or unrelated work is preserved | SAC-007 |
| SCN-008 | STORY-006 | Primary | Relevant checks pass | Deterministic evidence and verified fingerprint are persisted | SAC-008 |
| SCN-009 | STORY-006 | Failure | Any selected check fails or cannot execute | Commit readiness is denied with actionable evidence | SAC-008 |
| SCN-010 | STORY-007 | Permission | Commit is requested with stale approval | Commit and index remain unchanged | SAC-009 |
| SCN-011 | STORY-007 | Primary | Reviewer approves current verified fingerprint | One traceable commit is created for approved content | SAC-010 |
| SCN-012 | STORY-008 | Compatibility | Harness consumes a valid Loop fixture | All supported fields survive promotion | SAC-011 |
| SCN-013 | STORY-008 | Negative | Harness consumes an incompatible fixture | Promotion fails explicitly without partial output | SAC-011 |
| SCN-014 | STORY-009 | Release | Maintainer publishes a passing version | Public release and pinned submodule resolve reproducibly | SAC-012 |

## Story Dependencies and Risks
Execution order is STORY-001, STORY-002, STORY-003, STORY-004, STORY-005, STORY-006, STORY-007, STORY-008, then STORY-009, with documentation, QA, and security tasks spanning the sequence. STORY-004 depends on the stable fingerprint from STORY-003; STORY-007 depends on immutable evidence from STORY-006. Highest risks are approval replay or drift, path escape, unrelated-work damage, nondeterministic test selection, installer drift, secret leakage, and lossy promotion; negative fixtures and security review are mandatory mitigations.

## Story Readiness
All nine P0 MVP stories have a named actor, business value, epic, testable acceptance criteria, positive and negative scenarios, explicit dependencies, and traceability to accepted requirements and decisions. Product decisions are complete. The backlog is ready for release slicing; source verification of profile names and implementation-level schema choices belongs to design validation and does not change product scope.
