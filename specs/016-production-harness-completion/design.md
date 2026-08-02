---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-02T21:13:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "design.md"
  path: "specs/016-production-harness-completion/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids: []
  related_artifacts:
    - "specs/016-production-harness-completion/decision-log.md"
    - "specs/016-production-harness-completion/index.md"
    - "specs/016-production-harness-completion/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
    - "production-harness"
---

# Design

## Overview
- Extend the v4 local harness with a deterministic scheduler service, a sealed effect-driver boundary, provider execution receipts, and declarative install profiles. Existing StepCards remain the semantic unit of work.

## Architecture
- Compiler: validates run plan and per-step context fingerprints.
- Scheduler: owns task readiness, leases, attempts, recovery, and deterministic state projection.
- Worker protocol: claims a lease, dispatches a StepCard, and commits a terminal outcome using compare-and-commit semantics.
- Effect driver: maps one negotiated operation to a bounded native implementation and returns an attestable receipt.
- Evaluation runner: distinguishes offline protocol lint from genuine provider execution.
- Installer: resolves an explicit host profile to a project-scoped destination and verifies exact-source digests.

## Components
- ai-sdlc-scheduler: schemas, scheduler CLI, journal store, leases, worker protocol, and tests.
- ai-sdlc-host-adapter: executable driver registry, request and receipt validators, and safe reference drivers.
- ai-sdlc-shared-runtime evaluator: provider execution input and receipt validation.
- installer: host profile registry, destination policy, clean-install matrix, and deterministic record generator.

## Interfaces and Contracts
- Scheduler commands: create, claim, heartbeat, complete, fail, recover, status, and replay; machine output is TOON.
- Claim requires worker identity, lease duration, expected scheduler revision, and current context fingerprint.
- Effect execution requires negotiated adapter identity, operation, capabilities, side-effect class, idempotency key, bounded arguments, and approval evidence when required.
- Provider receipts require explicit execution mode, provider, host, model, execution identity, scenario version, evidence list, scores, verdict, and timestamp.
- Install profiles declare host ID, scope, skills root, discovery marker, and verification commands.

## Data Model
- scheduler-state: run ID, revision, plan fingerprint, task projections, ready order, leases, terminal outcomes, and journal fingerprint.
- lease: task ID, worker ID, nonce, issued time, expiry, attempt, and context fingerprint.
- effect-receipt: request fingerprint, driver ID and version, idempotency key, status, evidence fingerprint, and redacted diagnostic.
- provider-receipt: immutable execution metadata, scenario results, thresholds, and certification verdict.
- install-profile: host identity, supported scope, destination template, verification marker, and profile version.

## Error Handling
- Revision, nonce, fingerprint, capability, approval, or idempotency mismatch fails closed before mutation.
- Expired leases are recovered through an appended event; stale workers cannot commit.
- Unknown drivers and operations are rejected; driver failure records a bounded redacted diagnostic.
- Offline evaluation can validate shape but cannot produce certified status.

## Security Considerations
- No generic shell driver is provided. Reference drivers expose allowlisted repository operations with argument schemas.
- Secrets enter only through host runtime injection and are never serialized.
- Paths are project-root confined, symlinks and traversal are rejected, and receipts redact sensitive values.
- Provider evidence records identity and fingerprints, not credential material.

## Observability
- Append-only scheduler and effect events include run, task, attempt, revision, worker, operation, status, and fingerprints.
- Status and replay produce canonical deterministic projections.
- Human diagnostics explain rejected claims, stale context, expired leases, and certification state without leaking secrets.

## Risks and Tradeoffs
- Filesystem transactions provide a portable reference but not multi-region availability; backend interfaces keep remote implementations possible.
- Clock-based lease expiry can vary, so deterministic projections normalize ordering and tests inject a clock.
- Host diversity can create false portability claims; only profiles with fresh-install evidence are advertised.
- Provider results are variable; immutable scenario versions and threshold rules keep certification auditable.

## Validation Strategy
- Model-based scheduler unit tests plus multi-process contention and crash recovery integration tests.
- Adapter contract, traversal, capability, approval, idempotency, redaction, and replay tests.
- Offline and provider receipt evaluator tests with negative certification cases.
- Two-clean-install byte comparison per host profile.
- Full harness, docs, security, compatibility, and TOON-only gates.

## Migration Notes
- Introduce new versioned schemas without compatibility readers.
- Existing local runtime remains a worker-facing execution engine and is integrated behind the scheduler.
- Existing Codex project profile becomes the first explicit profile; new profiles are advertised only after clean-install validation.
