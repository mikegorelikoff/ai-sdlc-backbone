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
  at: "2026-08-03T12:00:54Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "backlog.md"
  path: "specs-refiniment/018-context-cache-runtime/backlog.md"
  workspace: "refinement"
  skill: "ai-sdlc-backlog-decomposition-and-task-planning"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
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
    - "BR-006"
    - "DEC-001"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "GOAL-001"
    - "GOAL-004"
    - "TASK-001"
    - "TASK-002"
    - "TASK-003"
    - "TASK-004"
    - "TASK-005"
    - "TASK-006"
    - "TASK-007"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/backlog-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
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
Feature 018 delivers automatic optional-cache use through four outcome epics and eight independently testable stories. The backlog preserves source authority, direct-read availability, TOON-only portable artifacts, and explicit deferred scope.

## Actors and Stakeholders
Contributors and agents consume StepCards; maintainers operate the adapter and cache lifecycle; repository maintainers own policy; QA and Security approve deterministic and privacy evidence. Each story has one primary actor and observable outcome.

## Scope and Boundaries
MVP includes STORY-001 through STORY-008 below. No daemon, remote provider, embedding, GraphRAG pipeline, network telemetry, cross-project cache, mandatory install, or pack schema change is included.

## Workflows and Failure Paths
Stories cover detection/direct parity, coordinated warm, snapshot acceptance, policy resolution, validated pack selection, observation/operations, fault fallback, and end-to-end evidence. Every cache fault terminates in stable direct reads.

## Requirements and Business Rules
BR-001 through BR-006 and AC-001 through AC-008 are distributed across stories without weakening repository authority, owning-step precedence, mandatory anchors, manifest budgets, confinement, privacy, or fallback.

## Data, Integrations, and Non-Functional Requirements
Implementation uses accepted index plus separate control SQLite DB in rollback-journal mode, strict TOON policy and receipts, bounded subprocess integration, and context-pack/v4 validation. Determinism, offline operation, atomic acceptance, source freshness, crash recovery, privacy, and default compatibility are cross-cutting.

## Dependencies, Risks, and Constraints
EPIC-002 safe lifecycle and EPIC-003 governance precede enabling EPIC-001 automatic reuse; EPIC-004 operational trust completes release evidence. Feature 017 ef67851 is the baseline. Direct reads contain every dependency failure.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 govern the backlog. Owner: Harness Maintainers. Impact: all MVP stories are ready; later WAL, embeddings, GraphRAG, and exporters require separate decisions. Next step: implement in dependency order.

## Success Measures
All eight acceptance criteria pass; concurrent processes converge; no stale or partial pack is accepted; budget and authority remain bounded; observations expose no raw evidence; default installs remain byte-compatible; eligible cached packs meet configured savings.

## Source Coverage
Consumed: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/validation.md.

## Epic Backlog
| Epic ID | Outcome | Actors | Priority | Dependencies |
| --- | --- | --- | --- | --- |
| EPIC-001 | ordinary StepCards transparently reuse valid cache evidence | contributor, agent | P0 | EPIC-002, EPIC-003 |
| EPIC-002 | warming publishes only fresh convergent accepted state | maintainer, agent | P0 | feature 017, control DB |
| EPIC-003 | policy, tokens, anchors, and authority are deterministic | repository maintainer, security | P0 | TOON codec, manifests, v4 |
| EPIC-004 | faults are diagnosable, private, and recoverable | maintainer, QA, security | P1 | EPIC-001 through EPIC-003 |

## Story Backlog
| Story ID | Epic Ref | Actor | Story | Priority | MVP |
| --- | --- | --- | --- | --- | --- |
| STORY-001 | EPIC-001 | contributor | use normal StepCard compilation with installed-module detection and absent-module parity | P0 | Yes |
| STORY-002 | EPIC-002 | maintainer | serialize concurrent warmers with bounded crash-safe coordination | P0 | Yes |
| STORY-003 | EPIC-002 | agent | accept a rebuilt index only after post-build source verification | P0 | Yes |
| STORY-004 | EPIC-003 | repository maintainer | configure strict default, skill, and step TOON policy clamped to manifest | P0 | Yes |
| STORY-005 | EPIC-003 | agent | accept only fresh economical context-pack/v4 with owner and anchors | P0 | Yes |
| STORY-006 | EPIC-004 | maintainer | inspect and reset allowlisted aggregate observations | P1 | Yes |
| STORY-007 | EPIC-004 | agent | receive stable direct reads and reason for every cache fault | P0 | Yes |
| STORY-008 | EPIC-004 | QA reviewer | validate concurrency, faults, privacy, determinism, economics, docs, and installation parity | P0 | Yes |

## Acceptance Summary
| Story ID | Acceptance Refs | Given | When | Then |
| --- | --- | --- | --- | --- |
| STORY-001 | AC-001 | module absent or installed | StepCard compiles | absent path is byte-equivalent; installed path is bounded |
| STORY-002 | AC-002 | concurrent processes | warming races | one logical fingerprint is accepted; no partial read |
| STORY-003 | AC-002, AC-006 | source changes during build | acceptance checks run | candidate is rejected and retried once or direct reads return |
| STORY-004 | AC-003, AC-008 | default and exact overrides | policy resolves | unknown input fails safely and budget/path remain bounded |
| STORY-005 | AC-004, AC-007 | fresh candidate evidence | pack validates | owner, anchors, order, freshness, economics, and determinism pass |
| STORY-006 | AC-005 | operations occur | observations are inspected/reset | only allowlisted aggregates exist in TOON output |
| STORY-007 | AC-006 | any adapter/cache failure | StepCard compiles | stable reason-coded direct reads return within timeout |
| STORY-008 | AC-001 through AC-008 | release candidate | full gates run | all P0 evidence passes and portable machine artifacts are TOON only |

## Priorities and Dependencies
Delivery order: STORY-002 and STORY-003 establish safe lifecycle; STORY-004 and STORY-005 establish governance; STORY-001 enables automatic runtime use; STORY-007 closes every fault path; STORY-006 adds operations; STORY-008 proves release readiness. P0 gates P1 and no observation work may delay safe fallback.

## Cross-Functional Tasks
| Task ID | Owner | Output | Dependencies | Refs |
| --- | --- | --- | --- | --- |
| TASK-001 | Dev | control DB, warm command, source verification, adapter | feature 017 | STORY-001 through STORY-003 |
| TASK-002 | Dev | strict policy resolver, budget clamp, pack validator | manifests, TOON | STORY-004, STORY-005 |
| TASK-003 | Dev | aggregate observation schema and inspect/reset commands | control DB | STORY-006 |
| TASK-004 | QA | unit, subprocess concurrency, mutation, corruption, timeout, parity, golden suites | TASK-001 through TASK-003 | STORY-008 |
| TASK-005 | Security | path, symlink, extension, authority, and observation privacy review | implementation | AC-005, AC-008 |
| TASK-006 | Docs | policy, automatic flow, fallback reasons, operations, limitations | stable CLI | GOAL-001, GOAL-004 |
| TASK-007 | Maintainer | skill validation, shared/full validation, install smoke, code review | all tasks | release gate |

## Definition of Ready
Every story has one actor, outcome, priority, MVP status, acceptance references, dependency, business value through an epic/capability/goal, and named evidence owner. No story contains deferred retrieval scope or unresolved product choice. All eight stories are ready for detailed scenario decomposition and estimation.
