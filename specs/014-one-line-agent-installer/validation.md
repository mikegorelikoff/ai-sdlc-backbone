---
type: "ai-sdlc.validation-report"
title: "Validation Report"
description: "Deterministic validation commands, results, and residual risk."
tags:
  - "ai-sdlc"
  - "validation"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "validation.md"
  path: "specs/014-one-line-agent-installer/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "quick"
  state_file: "specs/014-one-line-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/014-one-line-agent-installer/decision-log.md"
  status: "validated"
  owner: "Engineering and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
  related_artifacts:
    - "specs/014-one-line-agent-installer/_ai_sdlc/validation-plan.toon"
    - "specs/014-one-line-agent-installer/_ai_sdlc/validation-receipt.toon"
  validation:
    - "ai-sdlc-validation-receipt/v1: current; 9 commands; 0 failures"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
---

# Validation

## Result

Quick-flow validation covers the one-line installer contract, POSIX shell
syntax, the complete installed package shape, public documentation, SDD
traceability, and repository diff hygiene. The canonical receipt records nine
commands and zero failures.

## Coverage

- Exact Skills CLI arguments, telemetry opt-out, project scope, alternate and
  quoted agent identifiers, source/version overrides, and delegated statuses.
- Direct execution and the documented `curl | sh -s -- AGENT` stdin shape.
- Missing input, help, extra input, and missing `npx` fail without installation.
- All 44 skills remain usable from an emulated project-scoped installation.
- README and install-guide navigation remain valid across the public docs.
- Requirements, tests, tasks, decision, and plan links remain structurally
  current.

## Evidence

- Plan: `specs/014-one-line-agent-installer/_ai_sdlc/validation-plan.toon`
- Receipt:
  `specs/014-one-line-agent-installer/_ai_sdlc/validation-receipt.toon`
- Receipt commands: 9
- Additional current checks outside the receipt: `sh -n install.sh`;
  `python3 -m pytest -q docs/tests` (44 passed).

## Residual Risk

A real networked `curl` plus npm/GitHub installation was not run because the
script is not available at its public URL until these changes are published.
The offline fake-`npx` contract and existing disposable installed-package smoke
cover local behavior; publication still needs the existing remote CI smoke.
