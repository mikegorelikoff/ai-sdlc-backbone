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
  at: "2026-07-27T19:32:16Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "qa.md"
  path: "specs/014-one-line-agent-installer/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/014-one-line-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/014-one-line-agent-installer/decision-log.md"
  status: "validated"
  owner: "Repository Maintainers"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "TC-001"
    - "TC-006"
  related_artifacts:
    - "specs/014-one-line-agent-installer/decision-log.md"
    - "specs/014-one-line-agent-installer/design.md"
    - "specs/014-one-line-agent-installer/index.md"
    - "specs/014-one-line-agent-installer/plan.md"
    - "specs/014-one-line-agent-installer/requirements.md"
    - "specs/014-one-line-agent-installer/tasks.md"
    - "specs/014-one-line-agent-installer/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "validated"
    - "installer"
---

# QA

## Change Summary
Replace the user-facing multi-flag bootstrap with a one-line host-parameterized shell wrapper.

## Acceptance Scenarios
Exercise Codex, one non-Codex identifier, overrides, help, invalid arity, missing npx, delegated failure, and documentation examples.

## Regression Targets
Pinned CLI version, all-skill selection, explicit host scoping, project scope, telemetry opt-out, and existing advanced install guidance.

## Risk Notes
The largest risks are silently targeting multiple hosts, swallowing installer failures, or presenting a mutable curl URL as reproducible.

## Validation Commands
`sh -n install.sh`; `python3 -m unittest tests/test_install_sh.py`; `python3 docs/scripts/validate_docs.py`; `python3 -m pytest -q docs/tests`; SDD gates; `git diff --check`.

## Manual Checks
Read the README quick start and install guide top-to-bottom; confirm a new user sees one command, one agent placeholder, and a direct advanced-path link.

## Signoff
Ready when TC-001 through TC-006 pass and the published-script live smoke is the only recorded residual risk.
