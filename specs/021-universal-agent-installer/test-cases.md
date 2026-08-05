---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T13:17:51Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "021-universal-agent-installer"
  artifact: "test-cases.md"
  path: "specs/021-universal-agent-installer/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/021-universal-agent-installer/_ai_sdlc/state.toon"
  decision_log: "specs/021-universal-agent-installer/decision-log.md"
  status: "review"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-05"
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
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
  related_artifacts:
    - "specs/021-universal-agent-installer/decision-log.md"
    - "specs/021-universal-agent-installer/design.md"
    - "specs/021-universal-agent-installer/index.md"
    - "specs/021-universal-agent-installer/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "universal-installer"
---

# Test Cases

## Scope
Installer CLI, source resolution, locking, target safety, record validation, modules, docs, and CI.

## Scenario Matrix
- TC-001 / AC-001: named profiles install and validate.
- TC-002 / AC-002, AC-003: custom `.agent/skills` install and record validation.
- TC-003 / AC-004: unsafe targets fail with no records.
- TC-004 / AC-005: Unix and simulated Windows locks.
- TC-005 / AC-006: context-cache module via Python/custom profile.
- TC-006 / AC-007: installer, docs, SDD, and OS workflow gates.
- TC-007 / AC-008: portable commands and compatibility caveat in canonical docs.
- TC-008 / AC-009: Python and shell update recover custom/named profiles and
  selections; managed local drift fails without overwrite.

## Layer Mapping
- Unit: normalization, resolution, locks, validator.
- Integration: Python and shell install-to-update bootstrap fixtures.
- System: installed-runtime smoke.
- Documentation: validators, tests, strict build, rendered checks.

## Automation Plan
Extend shared-runtime tests/smoke, add Python bootstrap integration tests, and add a GitHub Actions native OS matrix. Keep immutable release-remote smoke.

## Open Gaps
Real model execution on unnamed agent hosts remains outside package-install conformance.
