---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-27T19:31:05Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "014-one-line-agent-installer"
  artifact: "test-cases.md"
  path: "specs/014-one-line-agent-installer/test-cases.md"
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
    - "specs/014-one-line-agent-installer/decision-log.md"
    - "specs/014-one-line-agent-installer/design.md"
    - "specs/014-one-line-agent-installer/index.md"
    - "specs/014-one-line-agent-installer/plan.md"
    - "specs/014-one-line-agent-installer/qa.md"
    - "specs/014-one-line-agent-installer/requirements.md"
    - "specs/014-one-line-agent-installer/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "validated"
    - "installer"
---

# Test Cases

## Scope
Validate AC-001 through AC-006 across shell argument handling, command construction, failure behavior, and public documentation.

## Scenario Matrix
| ID | Requirement | Scenario | Expected |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Run directly and through `sh -s -- codex` with fake npx | Exact pinned all-skills project invocation; telemetry disabled |
| TC-002 | AC-002 | Run with `claude-code` and a spaced identifier | Exact alternate identifier remains one argument |
| TC-003 | AC-003 | Run with no args, help, and extra args | Usage/help emitted; fake npx untouched |
| TC-004 | AC-004 | Set source and CLI version overrides | Both overrides appear in exact argument vector |
| TC-005 | AC-005 | Parse with `sh -n`; hide npx from PATH; force delegated failure | Syntax passes; missing prerequisite returns 127; delegated status propagates |
| TC-006 | AC-006 | Scan README and install guide | One-line wrapper is the primary first-install command |

## Layer Mapping
TC-001 through TC-005 are offline shell integration tests. TC-006 is documentation validation plus review.

## Automation Plan
Use Python unittest with a temporary fake `npx` executable that records environment and arguments; do not access npm or GitHub.

## Open Gaps
A live remote curl/install smoke is deferred until the script is published on GitHub.
