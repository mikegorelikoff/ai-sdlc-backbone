---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T13:17:52Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "qa.md"
  path: "specs/021-universal-agent-installer/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "review"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids: []
  related_artifacts:
    - "specs/021-universal-agent-installer/decision-log.md"
    - "specs/021-universal-agent-installer/design.md"
    - "specs/021-universal-agent-installer/index.md"
    - "specs/021-universal-agent-installer/requirements.md"
    - "specs/021-universal-agent-installer/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
    - "universal-installer"
---

# QA

## Change Summary
Add portable Windows/macOS/Linux installation and a safe configurable project skills root while preserving named profiles.

## Acceptance Scenarios
- QA-001: A contributor runs Python bootstrap and receives valid installed skills and TOON records.
- QA-002: Codex/Claude users retain the same targets.
- QA-003: A compatible host uses `.agent/skills` and automatic validation.
- QA-004: Escape or metadata-overlap targets fail before writes.

## Regression Targets
- Tag/SHA binding and dirty-source rejection.
- Collision review and rollback.
- Modules and TOON-only records.
- README/Home/Start here contracts.

## Risk Notes
- High: path escape.
- Medium: Windows locking/path behavior.
- Medium: overstated conformance.
- Low: shared parsing regression for named profiles.

## Validation Commands
Run focused installer tests/smoke, repository docs contract, SDD gates, `git diff --check`, and remote OS matrix before release.

## Manual Checks
Inspect both help screens, generated named/custom records, and supported-environment wording.

## Signoff
Planned; ready only after focused tests, complete docs gates, and remote OS matrix pass.
