---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-09-08T10:32:51Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "024-skill-execution-reinforcement"
  artifact: "requirements.md"
  path: "specs/024-skill-execution-reinforcement/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/024-skill-execution-reinforcement/_ai_sdlc/state.toon"
  decision_log: "specs/024-skill-execution-reinforcement/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-09-08"
  updated_at: "2026-09-08"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "NFR-001"
    - "NFR-002"
  related_artifacts:
    - "specs/024-skill-execution-reinforcement/decision-log.md"
    - "specs/024-skill-execution-reinforcement/design.md"
    - "specs/024-skill-execution-reinforcement/index.md"
    - "specs/024-skill-execution-reinforcement/plan.md"
    - "specs/024-skill-execution-reinforcement/qa.md"
    - "specs/024-skill-execution-reinforcement/reinforcement-report.md"
    - "specs/024-skill-execution-reinforcement/tasks.md"
    - "specs/024-skill-execution-reinforcement/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
---

# Requirements

## Goal
Reinforce every skill in both AI SDLC Harness and AI SDLC Loop as a predictable executable system.

## Problem Statement
Existing selectors accept inconsistent completion claims, handoff prose conflicts with authorized orchestration, and Loop can retain stale success evidence.

## Scope
All 48 Harness and 21 Loop skills, shared runtime, step graphs, evidence gates, tests/evals and generated documentation.

## Actors
Skill users, implementing agents, maintainers and downstream artifact consumers.

## Inputs
User request, existing source contracts, tests and dirty-workspace baseline captured before edits.

## Outputs
Explicit skill execution contracts, deterministic failure gates, regression evidence and per-skill architecture report.

## Functional Requirements
FR-001: Preserve specialized responsibilities and public paths.
FR-002: Reject dependency-inconsistent completion and stale evidence.
FR-003: Resolve inputs and bound recovery consistently across skills.

## Non-Functional Requirements
NFR-001: Preserve TOON, sibling runtime imports and router budgets.
NFR-002: Reuse existing lifecycle/artifact mechanisms and reduce duplicate instructions.

## Constraints
Preserve all pre-existing dirty changes in both products. Do not switch dirty branches, commit or publish.

## Acceptance Criteria
AC-001: Given any of the 69 skills, its preflight must resolve required/discoverable/inherited/optional inputs and expose failure and handoff rules.
AC-002: When a completed step lacks a completed predecessor or a terminal graph bypasses action validation, selectors must reject it.
AC-003: When commands change source or commit evidence is stale/tampered, Loop must return non-zero and must not report readiness or record commit approval.
AC-004: Given unchanged inputs, both products must emit byte-identical selections and pass their positive/negative graph evals and existing regressions.
AC-005: Catalog check, docs tests, strict builds, rendered validation and per-skill evidence must describe the current inventory without drift.

## Out of Scope
New product features, unrelated existing edits, publication and remote provider execution.

## Assumptions
The product inventory contains Harness and the Loop submodule, verified against .gitmodules and products/.

## Open Questions
None blocking implementation.

## Decision Status
All blocking decisions are resolved from repository evidence and the explicit all-product request. Accepted assumption: the two available product roots define this local scope. Preserve existing dirty branches; no commit or publication is included. No-ticket exception: direct repository maintenance request.
