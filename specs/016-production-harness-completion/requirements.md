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
  at: "2026-08-02T21:22:30Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "requirements.md"
  path: "specs/016-production-harness-completion/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
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
    - "AC-009"
    - "AC-010"
    - "DEC-001"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "TC-012"
  related_artifacts:
    - "specs/016-production-harness-completion/decision-log.md"
    - "specs/016-production-harness-completion/design.md"
    - "specs/016-production-harness-completion/index.md"
    - "specs/016-production-harness-completion/plan.md"
    - "specs/016-production-harness-completion/qa.md"
    - "specs/016-production-harness-completion/tasks.md"
    - "specs/016-production-harness-completion/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
    - "production-harness"
---

# Requirements

## Goal
- Make the AI SDLC Harness production-grade across durable orchestration, executable external effects, provider-executed evaluation, and portable native installation while preserving deterministic per-step context engineering and TOON-only machine contracts.

## Problem Statement
- Version 4 provides deterministic local journaling and adapter negotiation, but production completion is not proven because distributed scheduling is excluded, external effects remain host-owned, TC-012 has no authorized provider receipt, and native installation is certified for only one project-scoped host target.

## Scope
- Durable scheduler leases, recovery, concurrency control, and deterministic projections.
- Executable effect-driver protocol with allowlisted operations, idempotency, receipts, and fail-closed capability binding.
- Provider execution runner and attestable TC-012 receipt validation.
- Native install profiles and clean-install smoke for supported project-scoped host families.
- Documentation, migration, security, and release evidence.

## Actors
- Harness operator: compiles and resumes runs.
- Host adapter maintainer: supplies capability and effect mappings.
- Release maintainer: executes and signs provider evaluation evidence.
- Consumer repository maintainer: installs and verifies the harness.

## Inputs
- v4 StepCards, run plans, journals, adapter manifests, live scenario catalog, source revision, install target, and bounded per-step context packs.

## Outputs
- Canonical TOON scheduler state, leases, effect requests and receipts, provider evaluation receipts, install records and locks, plus human-readable operational documentation.

## Functional Requirements
- FR-001: Schedule dependency-ready StepCards with stable ordering and bounded parallelism.
- FR-002: Persist leases and recover abandoned work without duplicating terminal outcomes.
- FR-003: Execute only negotiated effect operations and bind every result to an idempotency key and receipt.
- FR-004: Validate provider-executed TC-012 receipts against scenario, host, model, evidence, and threshold contracts.
- FR-005: Install and verify exact-source skill trees for every declared host profile.
- FR-006: Compile sufficient context independently for each scheduled step and reject stale fingerprints.

## Non-Functional Requirements
- NFR-001: All repository machine artifacts and CLI machine output use canonical TOON only.
- NFR-002: Identical inputs produce byte-identical plans and deterministic projections.
- NFR-003: Crashes, retries, and concurrent claims never duplicate a committed effect.
- NFR-004: No credential value is persisted in plans, journals, receipts, or logs.
- NFR-005: The core remains provider-neutral and standard-library portable.

## Constraints
- Existing v4 contracts remain immutable; the scheduler introduces a versioned post-v4 capability and expands the public inventory from 44 to 45 skills.
- External provider execution requires user-authorized credentials and cannot be simulated as certification.
- Host profiles must remain project-scoped and exact-source reproducible.

## Acceptance Criteria
- AC-001: Given a dependency DAG, when multiple workers claim work, the scheduler must issue at most one active lease per task and produce a stable ready order.
- AC-002: Given an expired lease or interrupted process, when recovery runs, it must resume or retry within limits without duplicating a terminal result or effect receipt.
- AC-003: Given a negotiated StepCard, when an effect executes, the driver must reject undeclared capabilities and persist one validated receipt for the stable idempotency key.
- AC-004: Given the same scheduler inputs and journal, repeated projection must produce byte-identical canonical TOON.
- AC-005: Given stale step context, execution must stop before a lease or external effect is committed.
- AC-006: Given an authorized provider run, TC-012 must report provider, host, model, execution identity, scenario version, per-dimension scores, evidence references, and threshold verdict.
- AC-007: Given an offline-only run, the evaluator must mark provider certification pending and must not emit a passing provider verdict.
- AC-008: Given each declared install profile, two clean installs of the same revision must produce byte-identical install records and identical skill-tree digests.
- AC-009: Given any repository validation scan, no alternate machine representation artifact or identifier may be present and all owned TOON artifacts must decode.
- AC-010: Given a complete implementation, focused, integration, security, documentation, and fresh-install gates must pass with current evidence.

## Out of Scope
- Operating a hosted multi-tenant control-plane service.
- Storing production provider credentials in the repository.
- Claiming certification for providers or host profiles that were not actually executed.
- Compatibility readers for superseded machine schemas.

## Assumptions
- Accepted assumption: a filesystem-backed reference scheduler can prove transactional semantics for one shared checkout; remote queue backends use the same driver contract later.
- Accepted assumption: host families are certified through explicit declarative profiles rather than implicit path guessing.

## Open Questions
- No blocking product questions remain. Provider credentials and execution windows are release-owned runtime inputs, not repository design decisions.

## Decision Status
- All blocking decisions resolved through DEC-001: implement a transactional local reference scheduler and versioned driver interfaces, require genuine provider evidence for certification, and certify only explicitly declared install profiles.
