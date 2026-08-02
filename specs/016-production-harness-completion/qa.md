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
  at: "2026-08-02T21:23:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "016-production-harness-completion"
  artifact: "qa.md"
  path: "specs/016-production-harness-completion/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/016-production-harness-completion/_ai_sdlc/state.toon"
  decision_log: "specs/016-production-harness-completion/decision-log.md"
  status: "approved"
  owner: "QA and Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
  related_artifacts:
    - "specs/016-production-harness-completion/decision-log.md"
    - "specs/016-production-harness-completion/design.md"
    - "specs/016-production-harness-completion/index.md"
    - "specs/016-production-harness-completion/plan.md"
    - "specs/016-production-harness-completion/requirements.md"
    - "specs/016-production-harness-completion/tasks.md"
    - "specs/016-production-harness-completion/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
    - "production-harness"
---

# QA

## Change Summary
- Close the four disclosed v4 production gaps without weakening StepCard semantics, deterministic context selection, journal replay, or the TOON-only contract.

## Acceptance Scenarios
- QA-001: two or more workers contend for ready tasks; verify unique leases and stable wave order (TC-001).
- QA-002: interrupt at every effect commit boundary; verify recovery without duplicate effects (TC-002/TC-003).
- QA-003: replay and stale-context cases prove deterministic output and pre-effect rejection (TC-004/TC-005).
- QA-004: execute pinned scenarios in an authorized provider host and validate the receipt; offline mode remains pending (TC-006/TC-007).
- QA-005: perform duplicate clean installs for every advertised profile and compare bytes and discovery (TC-008).
- QA-006: run repository conformance and complete delivery gates (TC-009/TC-010).

## Regression Targets
- All 45 skills and generated routers.
- Explore zero-write and stale Apply rejection.
- Runtime phase ordering, retry budgets, completion fingerprints, and idempotency.
- Workflow, scheduler, and adapter StepCard field preservation.
- Existing Codex project-scoped one-line install behavior.
- Documentation structure, links, compatibility, package, and security tests.

## Risk Notes
- Critical: duplicate external effects under retry or lease loss.
- Critical: generic drivers could bypass authority or leak secrets.
- High: a provider-neutral fixture could be mislabeled as live certification.
- High: host path guessing could write outside the consumer project.
- Medium: lease timing and provider variability can reduce reproducibility; injected clocks and immutable scenario versions bound this risk.

## Validation Commands
- python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/016-production-harness-completion --quick-flow
- Focused scheduler, runtime, adapter, evaluator, and installer suites.
- python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_test_suite.py --format toon
- Run deterministic skill evaluation twice and compare canonical bytes.
- Run documentation, compatibility, clean-install, security, and TOON-only gates.

## Manual Checks
- Inspect one recovered run and confirm journal, lease, effect receipt, and result identity.
- Inspect a rejected unsafe driver request and confirm no side effect or secret-bearing diagnostic.
- Verify a genuine provider receipt inside the authorized host session.
- Launch each supported host against a fresh consumer repository and confirm skill discovery.

## Signoff
- Signoff requires current evidence for TC-001 through TC-010. Provider certification is not signed off while TC-006 lacks genuine authorized execution evidence; unverified install profiles must not be advertised.
