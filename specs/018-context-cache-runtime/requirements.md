---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:37:08Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "requirements.md"
  path: "specs/018-context-cache-runtime/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/018-context-cache-runtime/decision-log.md"
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
    - "DEC-001"
    - "DEC-007"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "TASK-007"
  related_artifacts:
    - "specs/018-context-cache-runtime/branch-plan.md"
    - "specs/018-context-cache-runtime/decision-log.md"
    - "specs/018-context-cache-runtime/design.md"
    - "specs/018-context-cache-runtime/index.md"
    - "specs/018-context-cache-runtime/plan.md"
    - "specs/018-context-cache-runtime/qa.md"
    - "specs/018-context-cache-runtime/tasks.md"
    - "specs/018-context-cache-runtime/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
---

# Requirements

## Goal
Integrate the optional project-installed context cache into ordinary StepCard compilation so fresh bounded evidence reduces repeated context reads without changing repository authority, mandatory anchors, manifest budgets, privacy, or default-install behavior.

## Problem Statement
Feature 017 provides a deterministic local cache only through explicit commands. Normal StepCard compilation still scans authoritative paths directly, so safe token savings require manual orchestration and produce no aggregate operational evidence. Feature 018 adds governed read-through use with deterministic fallback.

## Scope
Implement project-install detection, strict TOON runtime policy, bounded warm-on-demand with single-writer coordination, post-build source recheck, context-pack/v4 acceptance, manifest clamping, aggregate observations, inspect/reset operations, stable reason-coded direct fallback, tests, docs, and validation evidence.

## Actors
AI agents and contributors consume StepCards. Harness maintainers own runtime integration and cache lifecycle. Repository maintainers own project policy. QA owns deterministic, concurrency, recovery, compatibility, and token-economics evidence. Security owns path, authority, offline, and observation privacy review.

## Inputs
Owning skill and step identity, StepCard manifest budget, critical anchors, direct-read paths, project-installed cache skill, strict runtime-policy.toon defaults and exact overrides, project sources, accepted index and control database state, and feature-local delivery decisions.

## Outputs
Either a validated economical context-pack/v4 with owning step and mandatory anchors retained, or authoritative direct-read context with a stable fallback reason. Derived outputs include confined cache state and allowlisted aggregate operation/token counters.

## Functional Requirements
FR-001 activate only for project installations. FR-002 coordinate bounded crash-safe warmers. FR-003 resolve strict defaults and exact skill/step overrides. FR-004 clamp and validate v4 packs. FR-005 persist allowlisted aggregate observations. FR-006 inspect and reset observations. FR-007 return stable direct fallback. FR-008 recheck sources before accepted replacement.

## Non-Functional Requirements
NFR-001 deterministic ordering, fingerprints, receipts, and logical concurrency outcomes. NFR-002 offline operation and no extension loading. NFR-003 path confinement and aggregate-only privacy. NFR-004 bounded lock/process execution, crash recovery, idempotence, atomic publication, default-install parity, and latency excluded from golden fingerprints.

## Constraints
Portable machine artifacts use TOON. Repository sources and owning steps remain authoritative. Cache writes remain below project .ai-sdlc/cache. Accepted index stays rollback-journal SQLite with atomic replace; separate control state uses bounded BEGIN IMMEDIATE. No daemon, network, embeddings, cross-project store, or full GraphRAG.

## Acceptance Criteria
- AC-001 Pass when an absent optional module and a source checkout return the same authoritative direct paths and create no cache state.
- AC-002 Pass when concurrent warmers terminate with one fresh logical fingerprint, no partial accepted state, and mutation during build never publishes stale content.
- AC-003 Pass when strict TOON defaults and exact overrides resolve deterministically, unknown fields fail safely, and effective limits never exceed the owning manifest.
- AC-004 Pass when only a packed context-pack/v4 with owner, every mandatory anchor, current hashes, deterministic order, allowed authority, manifest budget, and configured savings is accepted.
- AC-005 Pass when observations expose only allowlisted aggregate operation, outcome, reason, call, and token totals, raw sentinel content is absent, and reset clears rows.
- AC-006 Pass when every documented adapter fault completes the StepCard with explicit authoritative direct paths and its stable fallback reason.
- AC-007 Pass when repeated identical fixtures produce byte-identical receipts and fingerprints while wall-clock latency remains outside deterministic output.
- AC-008 Pass when all derived reads and writes stay inside allowed project roots, unsafe symlinks are excluded, no network call occurs, and deferred retrievers are absent.

## Out of Scope
Autonomous background processes, remote storage or retrieval, embedding providers, entity/community GraphRAG pipelines, cross-tenant or cross-project indexes, network telemetry, raw prompt/query/content/identity observations, context-pack schema changes, mandatory installation, and numeric latency release SLOs.

## Assumptions
Project-local derived storage is writable when the optional module is installed; direct-read compilation remains viable; FTS5 absence is recoverable; supported hosts can hold a short control transaction and run bounded subprocesses. These assumptions are safe because every failure returns direct reads.

## Open Questions
No blocking implementation question. Future patched-runtime WAL opt-in, local embedding adapters, metrics exporters, full GraphRAG, and latency targets require separate product and architecture decisions and do not alter feature 018.

## Decision Status
Resolved blockers: none remain after the approved 18-stage refinement. Accepted assumptions: project-local derived storage is writable when installed, direct reads remain viable, FTS5 absence is recoverable, and supported hosts can run bounded local processes. Decision coverage: DEC-001 through DEC-007 are accepted for baseline, activation, concurrency, strict TOON policy, aggregate privacy, focused local scope, and deterministic measurement. Owner: Harness Maintainers. Impact: implementation can proceed without product invention. Resolution and next step: complete TASK-007 validation and review receipts.
