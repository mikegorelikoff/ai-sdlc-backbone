---
type: "ai-sdlc.validation-report"
title: "Validation Report"
description: "Deterministic validation commands, results, and residual risk."
tags:
  - "ai-sdlc"
  - "validation"
  - "harness-v4"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "validation.md"
  path: "specs/015-executable-skill-harness-v4/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "validated"
  owner: "Engineering, QA, and Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
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
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "DEC-007"
    - "DEC-008"
    - "DEC-009"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
    - "NFR-008"
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
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "T011"
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/_ai_sdlc/validation-plan.toon"
    - "specs/015-executable-skill-harness-v4/_ai_sdlc/validation-receipt.toon"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/design.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/qa.md"
    - "specs/015-executable-skill-harness-v4/requirements.md"
    - "specs/015-executable-skill-harness-v4/tasks.md"
    - "specs/015-executable-skill-harness-v4/test-cases.md"
  validation:
    - "ai-sdlc-test-suite-receipt/v1: 95 test files; 0 failures"
    - "ai-sdlc-eval-receipt/v1: 44 skills; 220 deterministic scenarios; 0 failures"
    - "ai-sdlc-live-eval-protocol/v1: 6 offline scenarios; 0 failures"
    - "ai-sdlc-validation-receipt/v1: current command evidence"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
    - "harness-v4"
---

# Validation

## Result

The executable skill harness v4 implementation passes its deterministic
implementation gates. The repository now validates 44 semantic skill graphs
with 221 nodes, runs every one of 95 skill-owned test files explicitly, and
exercises 220 deterministic evaluation scenarios without failures.

Context-engineering behavior is enforced as executable protocol: each planned
step carries a validated context pack, critical-anchor recall and token
economics are recomputed before execution, and insufficient packs fail closed
to direct reading. Apply execution binds the plan, step, context fingerprint,
attempt, and idempotency scope to an append-only journal.

## Coverage

- Semantic DAG schema, dependency order, entrypoints, generated-router drift,
  stable StepCards, graph fingerprints, failure policy, and hard-cut
  diagnostics across all skills.
- Exact-range context packing, source authority, skipped-source reasons,
  critical-anchor recall, token savings, direct-read fallback, path
  containment, secret exclusion, and tamper rejection.
- Flow and workflow intent routing, Explore zero-write, stale Apply rejection,
  runtime journal order, retries, replay, evidence, result projection, and
  side-effect idempotency.
- Full StepCard agreement across selector, flow, workflow, runtime, host
  adapter, and handoff boundaries.
- Source-checkout and native project-scoped installed layouts.
- Compatibility API 4.0.0, 12 protected contracts, 44 skills, five modules,
  generated catalogs, strict documentation build, and rendered-link integrity.
- Repository-wide TOON-only absence, decoding, canonical byte stability, and
  post-build checks.

## Evidence

- Reviewed plan:
  `specs/015-executable-skill-harness-v4/_ai_sdlc/validation-plan.toon`.
- Current command receipt:
  `specs/015-executable-skill-harness-v4/_ai_sdlc/validation-receipt.toon`.
- Complete test-suite receipt: 95/95 files passed; fingerprint
  `4d7881a8cdb44d4f8cbbb7e995d8384f8d07968a4bdf0d892bbfb30ef0e47d9f`.
- Native installation: 10 installer cases, 6 record cases, deterministic lock
  equality across two consumers, and the complete 44-skill installed workflow
  passed.
- Deterministic evaluation: 44 skills, 220 scenarios, two runs with identical
  31,999-byte output; receipt fingerprint
  `1d47e6bbd5259b874ee9600040bf1aa716684fd0cdb2740b9bcaba910943f0d2`.
- Offline live-protocol validation: 6/6 representative scenarios passed;
  receipt fingerprint
  `39589f99fbc80b108649b07f02dbc43a2fe6dadc5744508af88aed1dd1541ac2`.
- Documentation: 200 public pages, 46 unit tests, and a strict rendered site
  with 201 HTML pages and 5,423 validated local targets.
- Hash-locked documentation dependencies installed and verified with Python
  3.11.
- Exact release-history compatibility passed after the v4 release subject with
  all 18 protected pre-v4 and release commits declared in order.

## Residual Risk

The deterministic implementation is complete. DEC-008 authorizes publication
with provider certification pending and prohibits treating offline evidence as
provider execution. An authorized TC-012 receipt must still meet the published
routing, step-compliance, evidence, recovery, authorization, and context
thresholds while recording host, provider, model, scenario version, execution
identity, effect receipts, and recovery evidence before any provider-
certification claim is made.
