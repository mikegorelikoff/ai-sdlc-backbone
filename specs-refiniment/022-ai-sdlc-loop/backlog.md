---
type: "ai-sdlc.backlog"
title: "Delivery Backlog"
description: "Epics, stories, acceptance summaries, dependencies, and delivery tasks."
tags:
  - "ai-sdlc"
  - "planning"
  - "backlog"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-17T10:50:26Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "022-ai-sdlc-loop"
  artifact: "backlog.md"
  path: "specs-refiniment/022-ai-sdlc-loop/backlog.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-decomposition-and-task-planning"
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
    - "AC-004"
    - "AC-006"
    - "BR-001"
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
    - "DEC-004"
    - "DEC-005"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "REQ-001"
    - "REQ-002"
    - "REQ-006"
    - "REQ-007"
    - "REQ-009"
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
    - "ai-sdlc-backlog-decomposition-and-task-planning"
    - "backlog"
    - "approved"
---

# backlog.md

## Feature Summary
The delivery backlog decomposes three P0 epics into nine actor-centered MVP stories and linked technical, QA, documentation, release, and integration tasks.

## Actors and Stakeholders
Contributors own requests and evidence review; reviewers own the two approvals; Loop maintainers implement, validate, document, and release; Harness maintainers validate promotion and parent integration.

## Scope and Boundaries
Every item implements CAP-001 through CAP-006 and stays inside one user-facing skill, three stages, compatible artifacts, all verified project hosts, two approval gates, public release, and products/ai-sdlc-loop submodule integration.

## Workflows and Failure Paths
Backlog stories cover the complete happy path and explicit negative paths for absent or stale approvals, unsafe or overlapping changes, failed checks, invalid artifacts, unsupported profiles, installer interruption, promotion loss, and submodule drift.

## Requirements and Business Rules
Stories trace to REQ-001 through REQ-009, AC-001 through AC-006, BR-001 through BR-007, DEC-001 through DEC-005, CAP-001 through CAP-006, and EPIC-001 through EPIC-003. No story can weaken approval or one-skill boundaries.

## Data, Integrations, and Non-Functional Requirements
Backlog outputs include one skill package, install scripts, compatible Markdown and TOON schemas, approval receipts, validation evidence, tests, CI, README and security guidance, public Git history, and a pinned parent submodule.

## Dependencies, Risks, and Constraints
STORY-001 precedes installer claims. STORY-003 precedes approval fingerprinting. STORY-004 and STORY-005 precede verification. STORY-006 precedes commit approval. Compatibility and release tasks depend on all core safety tests. Scope creep and approval replay remain P0 regression risks.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-005 are accepted. OQ-001 is implemented by STORY-001. Exact v0.x selection belongs to release task TASK-009 after all acceptance checks. No story contains an unresolved product decision.

## Success Measures
All nine MVP stories meet their acceptance summaries, every advertised profile installs exactly one visible skill, both approval boundaries fail closed on drift, relevant checks produce evidence, compatible promotion passes, and the validated repository commit is pinned by the Harness submodule.

## Source Coverage
Consumed specs-refiniment/022-ai-sdlc-loop/goal-capability-map.md, specs-refiniment/022-ai-sdlc-loop/backlog-gap-review.md, specs-refiniment/022-ai-sdlc-loop/requirements-readiness.md, specs-refiniment/022-ai-sdlc-loop/prfaq.md, specs-refiniment/022-ai-sdlc-loop/decision-log.md, specs-refiniment/022-ai-sdlc-loop/discovery.md, specs-refiniment/022-ai-sdlc-loop/delivery-gap-review.md, specs-refiniment/022-ai-sdlc-loop/_ai_sdlc/state.toon, and specs-refiniment/022-ai-sdlc-loop/index.md.

## Epic Backlog
| Epic ID | Outcome | Actors | Priority | Dependencies |
| --- | --- | --- | --- | --- |
| EPIC-001 | Teams install one independently released Loop skill through every supported project host | Contributor; Loop maintainer; Harness maintainer | P0 | Profile inventory; repository; installer fixtures |
| EPIC-002 | A reviewed request becomes verified code and only an explicitly approved commit | Contributor; reviewer; Loop maintainer | P0 | Compatible spec; Git fingerprints; command runner |
| EPIC-003 | Automated evidence proves safety, compatibility, publication, and parent integration | Loop maintainer; Harness maintainer | P0 | EPIC-001; EPIC-002; CI; promotion fixture |

## Story Backlog
| Story ID | Epic Ref | Actor | Story | Priority | MVP |
| --- | --- | --- | --- | --- | --- |
| STORY-001 | EPIC-001 | Loop maintainer | Verify and codify the current supported project host profile inventory | P0 | Yes |
| STORY-002 | EPIC-001 | Contributor | Install and verify exactly one ai-sdlc skill with one command in any supported profile | P0 | Yes |
| STORY-003 | EPIC-002 | Contributor | Turn a bounded request into a compact Harness-compatible specification and fingerprint | P0 | Yes |
| STORY-004 | EPIC-002 | Reviewer | Approve or reject code mutation against the current specification fingerprint | P0 | Yes |
| STORY-005 | EPIC-002 | Contributor | Apply only the approved scoped code changes while preserving unrelated work | P0 | Yes |
| STORY-006 | EPIC-002 | Contributor | Select and execute relevant deterministic checks and record evidence | P0 | Yes |
| STORY-007 | EPIC-002 | Reviewer | Approve or reject a commit against the verified change fingerprint | P0 | Yes |
| STORY-008 | EPIC-003 | Harness maintainer | Promote a Loop artifact into Harness without losing supported fields | P0 | Yes |
| STORY-009 | EPIC-003 | Loop maintainer | Publish the validated public repository and enable a pinned Harness submodule | P0 | Yes |

## Acceptance Summary
STORY-001: source and tests agree on the advertised profiles. STORY-002: clean fixtures install and verify one skill; invalid, interrupted, and drifted installs fail safely. STORY-003: required intent, scope, acceptance, tests, tasks, and fingerprint fields validate. STORY-004: missing, rejected, or stale approval blocks mutation; matching approval permits it. STORY-005: only approved paths change and unrelated dirty work is preserved. STORY-006: focused checks run, failures block readiness, and evidence is deterministic. STORY-007: missing or stale verified-change approval blocks commit; matching approval creates the expected commit only. STORY-008: promotion preserves all supported fields and rejects incompatible input. STORY-009: repository is public and reproducible, CI passes, release guidance is accurate, and the parent submodule pins the validated commit.

## Priorities and Dependencies
All stories are P0 because each is necessary for the promised install, safety, compatibility, or release outcome. Sequence: STORY-001; STORY-002 and STORY-003; STORY-004; STORY-005; STORY-006; STORY-007; STORY-008; STORY-009. Documentation and QA tasks evolve with their parent story and cannot be deferred beyond release.

## Cross-Functional Tasks
| Task ID | Owner | Output | Dependencies | Refs |
| --- | --- | --- | --- | --- |
| TASK-001 | Dev | One-skill package, workflow state, and compatible spec schema | STORY-003 | CAP-002; REQ-001; REQ-002; REQ-007 |
| TASK-002 | Dev | Cross-host installer, verifier, and recovery behavior | STORY-001 | CAP-001; AC-001; REQ-006 |
| TASK-003 | Dev | Specification and verified-change fingerprint approval engine | TASK-001 | CAP-003; CAP-005; DEC-004 |
| TASK-004 | Dev | Scoped mutation and relevant validation runner | TASK-003 | CAP-003; CAP-004; AC-003; AC-004 |
| TASK-005 | QA | Positive, negative, drift, interruption, path-safety, and compatibility fixtures | TASK-001 through TASK-004 | AC-001 through AC-006 |
| TASK-006 | Docs | README, install, verify, workflow, escalation, recovery, security, support, and compatibility guidance | Validated commands | REQ-006 through REQ-009 |
| TASK-007 | Security | Threat review for remote install, path handling, approvals, commands, secrets, and Git mutation | TASK-002 through TASK-004 | BR-003; BR-005; BR-007 |
| TASK-008 | Harness maintainer | Promotion fixture and products/ai-sdlc-loop integration | STORY-008; validated Loop commit | DEC-001; DEC-005; REQ-009 |
| TASK-009 | Loop maintainer | Public repository, CI, initial v0.x release selection, and release evidence | All P0 validation | EPIC-003; STORY-009 |

## Definition of Ready
A story is ready only when actor, outcome, priority, MVP status, parent epic, requirement and acceptance references, dependencies, failure behavior, and owner are explicit. All nine stories meet this bar. OQ-001 is represented by STORY-001 and is not hidden. No story is too large to estimate at delivery-plan granularity.
