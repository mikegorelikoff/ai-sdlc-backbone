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
  at: "2026-09-15T13:28:22Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "025-adaptive-execution"
  artifact: "requirements.md"
  path: "specs/025-adaptive-execution/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/025-adaptive-execution/_ai_sdlc/state.toon"
  decision_log: "specs/025-adaptive-execution/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-09-15"
  updated_at: "2026-09-15"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "DEC-001"
  related_artifacts:
    - "specs/025-adaptive-execution/decision-log.md"
    - "specs/025-adaptive-execution/design.md"
    - "specs/025-adaptive-execution/index.md"
    - "specs/025-adaptive-execution/plan.md"
    - "specs/025-adaptive-execution/qa.md"
    - "specs/025-adaptive-execution/tasks.md"
    - "specs/025-adaptive-execution/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "draft"
---

# Requirements

## Goal
Reduce unnecessary orchestration across Harness backbone and Loop with risk-proportional execution.

## Problem Statement
Loop has a fixed five-stage router and sequential verification. Harness has adaptive rigor and step context but lacks a shared execution-depth decision and run-level evidence budget. No in-process model provider is called by Loop.

## Scope
Shared deterministic adaptive execution policy, reusable context, bounded evidence state, routing integration, verification concurrency, all skill shared contracts, tests and reproducible benchmarks.

## Actors
Contributor; coordinating agent; owning skill; deterministic validator.

## Inputs
User request, relevant repository paths, evidence-based risk signals, existing authorization and quality gates.

## Outputs
FAST/STANDARD/DEEP classification, canonical task record with context/decisions/verification/metrics, source-bound evidence, benchmark.

## Functional Requirements
AC-001: Classify risk from scope and evidence, never prompt length alone.
AC-002: Escalate monotonically without discarding context or prior work.
AC-003: Reuse context with incremental refresh and explicit uncertainty.
AC-004: Select checks by risk, retain authorization and quality gates.
AC-005: Bound retries, reject unchanged retries and stop on success.
AC-006: Record real timing and call metrics; unknown host metrics remain unknown.
AC-007: Preserve existing commands and full SDLC capability.

## Non-Functional Requirements
Optimize deterministic orchestration overhead; do not claim synthetic timings represent end-to-end agent latency. Fail closed on invalid inputs or stale evidence.

## Constraints
Canonical TOON; additive interfaces; Loop is a separate Git submodule. Existing submodule revision differs from parent before this task; preserve it. No external provider or messaging is needed.

## Acceptance Criteria
Given the observed task and scope, classification and execution must satisfy these observable checks:

AC-001: Tiny bugs and documentation select FAST; localized features select STANDARD; architecture and security select DEEP.
AC-002: New risk escalates without deleting completed context, implementation or retry history.
AC-003: All consumers reuse relevant context; changed sources refresh incrementally.
AC-004: Deterministic checks and relevant capabilities are selected; existing approvals and quality gates remain mandatory.
AC-005: Failed verification allows two repairs; unchanged repeats are rejected; successful unchanged verification terminates.
AC-006: Capture measured stages and counters, distinguish unknown host metrics, and benchmark helpers before/after.
AC-007: Legacy commands and full SDLC workflow remain available without weakening existing gates.

## Out of Scope
Replacing model providers, automatically committing changes, deleting quality gates, changing public paths.

## Assumptions
Use current checkout as integration baseline. No ticket was supplied; this user request is the approved no-ticket source. Shared skill contract applies to the whole family; domain-specific required gates remain authoritative.

## Open Questions
None blocking implementation. End-to-end provider latency requires a live host run and cannot be inferred from fixture timing.

## Decision Status
DEC-001 accepted. All blocking decisions are resolved. Accepted assumptions: preserve existing stage-owned receipts, use current checkout as baseline, and treat live provider performance as unmeasured rather than an implementation blocker.

