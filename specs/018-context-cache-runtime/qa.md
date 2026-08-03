---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:34:24Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "qa.md"
  path: "specs/018-context-cache-runtime/qa.md"
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
    - "TASK-007"
  related_artifacts:
    - "specs/018-context-cache-runtime/branch-plan.md"
    - "specs/018-context-cache-runtime/decision-log.md"
    - "specs/018-context-cache-runtime/design.md"
    - "specs/018-context-cache-runtime/index.md"
    - "specs/018-context-cache-runtime/requirements.md"
    - "specs/018-context-cache-runtime/tasks.md"
    - "specs/018-context-cache-runtime/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
---

# QA

## Change Summary
Automatic cache use now occurs inside ordinary StepCard compilation only when the optional skill is project-installed. QA verifies safe cached acceptance, complete direct fallback, concurrency, freshness, strict policy, privacy, confinement, deterministic economics, docs, and compatibility.

## Acceptance Scenarios
QA-001 absent parity; QA-002 concurrent fresh publication; QA-003 strict exact policy within manifest; QA-004 owner/anchor/fresh/economical v4 acceptance; QA-005 aggregate observation/reset privacy; QA-006 full fault fallback; QA-007 deterministic receipt with separate latency; QA-008 confined offline behavior.

## Regression Targets
Protect repository-instruction loading, owning-step precedence, direct StepCard selection, context-pack/v4 ordering and fingerprints, feature-017 build/query/pack/verify/purge, unsafe-source exclusion, TOON command output, source-checkout non-activation, docs/catalog contracts, and project install smoke.

## Risk Notes
P0 risks are stale or partial publication, authority or budget widening, privacy/confinement breach, default drift, and fault-blocked context. P1 risks are token regression and support ambiguity. Timing variation is observational. Any P0 or high security failure blocks release.

## Validation Commands
Run the cache unittest file, shared-runtime test_steps.py, full shared-runtime discovery, docs validator and tests, skill quick validation, install smoke, security tests, code review, generated catalog check, and git diff --check. Record exact current outcomes in validation.md.

## Manual Checks
Owner: Harness Maintainers and Security. Inspect one accepted and one fallback StepCard receipt, resolved policy precedence, observation/reset output, control schema fields, cache path confinement, and public guide troubleshooting. Impact: these checks verify operational clarity and privacy but cannot waive automated P0 failures. Next step: record the completed checklist in validation and security receipts.

## Signoff
Owner: QA Maintainers. Status: ready for implementation validation, not release-approved. Impact: release waits for all P0 automated suites, current security and code review, docs/install gates, deterministic receipt evidence, and zero unresolved high finding. Next step: execute the ordered validation and review gates, then update TASK-007 and the implementation plan.
