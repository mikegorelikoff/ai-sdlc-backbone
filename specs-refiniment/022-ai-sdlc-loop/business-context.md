---
type: "ai-sdlc.business-context"
title: "Business Context"
description: "Actors, workflows, rules, exceptions, and acceptance context."
tags:
  - "ai-sdlc"
  - "analysis"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:56:05Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "business-context.md"
  path: "specs-refiniment/022-ai-sdlc-loop/business-context.md"
  workspace: "refinement"
  skill: "ai-sdlc-ba"
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
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "REQ-001"
    - "REQ-002"
    - "REQ-003"
    - "REQ-005"
    - "REQ-007"
    - "REQ-009"
    - "TASK-001"
    - "TASK-005"
    - "TASK-007"
    - "TASK-009"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
    - "WF-005"
  related_artifacts:
    - "specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/backlog.md"
    - "specs-refiniment/022-ai-sdlc-loop/decision-log.md"
    - "specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md"
    - "specs-refiniment/022-ai-sdlc-loop/discovery.md"
    - "specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md"
    - "specs-refiniment/022-ai-sdlc-loop/index.md"
    - "specs-refiniment/022-ai-sdlc-loop/prfaq.md"
    - "specs-refiniment/022-ai-sdlc-loop/release-slicing.md"
    - "specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md"
    - "specs-refiniment/022-ai-sdlc-loop/user-stories.md"
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
AI SDLC Loop is a separately maintained minimal workflow for teams that need a safe bounded change without adopting the full AI SDLC Harness surface. Its business outcome is lower maintainer support complexity while retaining explicit human authority, reproducible verification, and a lossless escalation path into the AI SDLC product family.

## Actors and Stakeholders
The contributor initiates install and delivery work and reviews evidence. The reviewer is the authority for code mutation and commit creation. The Loop maintainer owns contracts, implementation, fixtures, documentation, CI, and releases. The Harness maintainer owns promotion compatibility and the parent submodule. QA and security reviewers validate observable safety and misuse behavior.

## Scope and Boundaries
In scope are one ai-sdlc skill, Specify, Implement, Verify, one-command installation for all source-verified project profiles, compact compatible artifacts, approval receipts, relevant tests, explicit commit approval, public Apache-2.0 distribution, and Harness submodule integration. Out of scope are the Harness skill catalog, complete refinement runtime, telemetry, deployment, silent commits, unapproved mutation, and claims of reduced model calls.

## Workflows and Failure Paths
The contributor installs Loop, submits a bounded request, inspects a fingerprinted specification, and requests review. A matching approval permits only scoped implementation. Verify selects and runs relevant deterministic checks and fingerprints the verified change. A second matching approval permits a commit. Any missing or stale approval, unsafe path, unrelated overlap, failed check, unsupported profile, incompatible artifact, or publication drift stops the workflow without unauthorized mutation.

## Requirements and Business Rules
REQ-001 through REQ-009 define product outcomes. BR-001 through BR-007 define invariants: one visible skill, specification before mutation, current approval before mutation, deterministic evidence, current approval before commit, compatible promotion, and fail-closed exceptions. AC-001 through AC-006 and SAC-001 through SAC-012 make each invariant observable without requiring knowledge of implementation internals.

## Data, Integrations, and Non-Functional Requirements
Business records are the specification, its fingerprint, approval receipts, scoped change fingerprint, command evidence, promotion result, and release/submodule identity. Records must be human-readable, deterministic, locally inspectable, and secret-safe. Supported integrations are verified project skill roots, local repositories, approved commands, Git, GitHub, and Harness promotion fixtures. No telemetry or remote service is required at runtime.

## Dependencies, Risks, and Constraints
The installer depends on source-verified Harness profiles. Implement depends on an immutable specification fingerprint and matching approval. Verify depends on scoped mutation; commit approval depends on passing immutable evidence. Publication depends on promotion and security evidence. Main risks are approval replay, path escape, unrelated-work damage, host drift, nondeterministic checks, secret exposure, and promotion loss. Fail-closed rules and fixtures are mandatory controls.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted and authoritative. Assumption owner: maintainer. Impact: exact host labels and compatible schema fields affect installer and promotion fixtures, not product scope. Resolution and next step: derive both from current Harness source during implementation design and freeze them in tests before publication. Open questions: none that alter actors, permissions, launch boundary, retention, or acceptance behavior.

## Success Measures
Success means every advertised host installs exactly one ai-sdlc skill; both approval gates reject absent, rejected, stale, or mismatched evidence; unrelated repository work remains intact; relevant checks yield deterministic evidence; compatible promotion preserves every supported field; public CI and documentation match verified commands; and Harness pins the released repository commit. Maintainer-facing success is a smaller public command and documentation surface.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/index.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/backlog.md, specs-refiniment/022-ai-sdlc-loop/user-stories.md, specs-refiniment/022-ai-sdlc-loop/release-slicing.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, and specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon. These sources cover customer value, roles, rules, priorities, scenarios, risk, readiness, and accepted authority.

## Current Behavior
AI SDLC Harness offers a broad multi-skill lifecycle and installers for several project profiles. It is the only maintained public contract in scope, so users seeking a small bounded flow still create support demand across a much larger surface. No separate AI SDLC Loop repository, one-skill install contract, Loop artifact, Loop release, or Harness submodule currently exists.

## Desired Behavior
A team installs one visible ai-sdlc skill into any verified project profile with one command. The skill owns a compact three-stage state machine. Specify creates the review boundary; Implement remains unavailable until a matching approval and changes only approved scope; Verify persists relevant test evidence and requires a second matching approval before commit. Artifacts can be promoted to Harness, and the independently released repository is pinned as a parent submodule.

## Actor and Permission Matrix
| Actor | Role | Permissions | Restrictions | Source |
| --- | --- | --- | --- | --- |
| Contributor | Requester and operator | Install, specify, inspect evidence, request approvals, run approved workflow | Cannot self-assert approval or bypass safety gates | DEC-002, DEC-004, STORY-002 through STORY-007 |
| Reviewer | Human authority | Approve or reject current specification and verified-change fingerprints | Approval is valid only for the exact current fingerprint; no implicit approval | DEC-004, BR-003, BR-005 |
| Loop maintainer | Product owner | Maintain contracts, code, tests, docs, CI, security evidence, and releases | Cannot advertise unverified profiles or release failing evidence | DEC-001, DEC-003, TASK-001 through TASK-009 |
| Harness maintainer | Compatibility owner | Validate promotion and pin the approved release as submodule | Cannot accept lossy or incompatible promotion | DEC-005, STORY-008, STORY-009 |
| QA and security reviewer | Assurance owner | Design and evaluate positive, negative, drift, abuse, and recovery tests | Cannot waive approval, path, secret, or failed-check launch gates | TASK-005, TASK-007 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | Project needs Loop | Contributor | Select verified profile; run one install command; run separate verification | Exactly one ai-sdlc skill installed | Unsupported profile, collision, interruption, or drift fails safely | STORY-001, STORY-002, SAC-001 through SAC-003 |
| WF-002 | Bounded change request | Contributor and reviewer | Create compatible spec; fingerprint; review; approve or reject | Approved immutable implementation boundary or stopped request | Missing, rejected, stale, or mismatched approval blocks mutation | STORY-003, STORY-004, SAC-004 through SAC-006 |
| WF-003 | Current spec approved | Contributor | Apply scoped changes; preserve unrelated work; run relevant checks; persist evidence | Verified-change fingerprint or failed verification | Unsafe overlap, path escape, unavailable or failed check blocks readiness | STORY-005, STORY-006, SAC-007, SAC-008 |
| WF-004 | Passing verified change | Reviewer and contributor | Review evidence; approve current fingerprint; create exact commit | Traceable approved commit | Missing or stale approval leaves index and history unchanged | STORY-007, SAC-009, SAC-010 |
| WF-005 | Release candidate passes | Maintainers | Validate promotion; publish public release; pin parent submodule | Reproducible compatible public integration | Lossy promotion, CI failure, or submodule mismatch blocks launch | STORY-008, STORY-009, SAC-011, SAC-012 |

## Business Rule Catalog
| Rule ID | Rule | Applies To | Failure Behavior | Source | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-001 | The public installation must expose exactly one ai-sdlc skill | Install and verification | Fail verification and report unexpected surface | REQ-001, AC-001 | DEC-002 |
| BR-002 | Specify must persist a compatible artifact and deterministic fingerprint before mutation | Specify | Implement remains unavailable | REQ-002, AC-002 | DEC-002 |
| BR-003 | Only a matching current specification approval permits mutation | Implement | Stop with no code changes | REQ-003, AC-003 | DEC-004 |
| BR-004 | Verify must run relevant deterministic checks and persist evidence | Verify | Failed or unavailable checks block commit readiness | REQ-005, AC-004 | DEC-004 |
| BR-005 | Only a matching current verified-change approval permits commit | Commit | Preserve index and history unchanged | REQ-005, AC-005 | DEC-004 |
| BR-006 | Promotion must preserve every supported Loop field | Promotion | Reject incompatibility without partial output | REQ-007, AC-006 | DEC-005 |
| BR-007 | Install, workflow, and release exceptions fail closed and preserve unrelated state | All workflows | Stop safely with actionable recovery | SAC-003, SAC-007 through SAC-012 | DEC-003, DEC-004 |

## Acceptance Criteria
| AC ID | Given | When | Then | Rule Ref | Source |
| --- | --- | --- | --- | --- | --- |
| AC-001 | Any advertised clean project profile | Install and verify run | Exactly one visible ai-sdlc skill is present | BR-001, BR-007 | SAC-001 through SAC-003 |
| AC-002 | A bounded valid request | Specify completes | Schema-valid compatible artifact and deterministic fingerprint persist | BR-002 | SAC-004 |
| AC-003 | Any approval state | Implement is requested | Mutation occurs only for an approval matching the current spec fingerprint | BR-003, BR-007 | SAC-005, SAC-006 |
| AC-004 | An approved scoped implementation | Verify runs | Relevant checks and deterministic evidence persist; failure blocks readiness | BR-004, BR-007 | SAC-007, SAC-008 |
| AC-005 | Any verified-change approval state | Commit is requested | Commit occurs only for passing evidence and matching current approval | BR-005, BR-007 | SAC-009, SAC-010 |
| AC-006 | Valid and incompatible Loop fixtures | Promotion runs | Valid fields are preserved and incompatible input is rejected without partial output | BR-006, BR-007 | SAC-011, SAC-012 |

## Business Context Gaps
No business-analysis blocker remains. Exact supported profile identifiers and the compatible field set are controlled implementation evidence gaps. Owner: Loop and Harness maintainers. Impact: installation claims and promotion fidelity. Resolution and next step: inspect current parser, installer tests, artifact schemas, and promotion contracts during delivery design; add fixtures; block documentation and release if source and tests disagree. Capacity and dates remain intentionally unspecified, so sequencing is logical rather than calendar-based.
