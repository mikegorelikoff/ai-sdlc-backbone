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
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "qa.md"
  path: "specs/013-role-guided-installable-flow/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Engineering and QA"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
  trace_ids:
    - "AC-001"
    - "AC-012"
  related_artifacts:
    - "specs/013-role-guided-installable-flow/branch-plan.md"
    - "specs/013-role-guided-installable-flow/code-review.md"
    - "specs/013-role-guided-installable-flow/decision-log.md"
    - "specs/013-role-guided-installable-flow/design.md"
    - "specs/013-role-guided-installable-flow/plan.md"
    - "specs/013-role-guided-installable-flow/requirements.md"
    - "specs/013-role-guided-installable-flow/tasks.md"
    - "specs/013-role-guided-installable-flow/test-cases.md"
    - "specs/013-role-guided-installable-flow/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
---

# QA

## Change Summary
Validate the removal of duplicated runtime plumbing, role-guided selector-backed flow v2, and native OKF v0.2 durable Markdown generation across source, installed copies, configuration, documentation, feature/change/runtime bundles, and migrations.

## Acceptance Scenarios
Validate one BA, PM, architect, engineer, and QA skill through prepare, execute, and validate/handoff selection. Confirm each selected file is readable as a standalone imperative procedure and that the router explains exactly when it loads. Confirm flow's six steps contain real entry, evidence, action, blocker, and exit guidance rather than one-line summaries.

## Regression Targets
Existing flow routing, state prerequisites, artifact ownership, safety boundaries, quick/full behavior, script commands, output contracts, generated guides, install layouts, compact TOON routing, legacy feature readability, and all 44 skill triggers. Instruction relocation and OKF centralization must not remove lifecycle tokens, unknown metadata extensions, or change the skill inventory.

## Risk Notes
Primary risks are semantic loss during mechanical splitting and trust corruption during metadata refresh. Mitigate with before/after section accounting, profile coverage, unknown-extension preservation, meaningful-change/verification tests, atomic migrations, manifest link validation, representative human review, and the full runtime suite. Secondary risk is false context savings when agents broad-load all steps; routers, selectors, compact TOON, and progressive bundle indexes must keep reads bounded.

## Validation Commands
Run focused runtime and flow unit tests; install smoke in full, selective, and disposable-global modes; generated-doc drift checks; `python3 scripts/validate_all.py`; SDD analyze/validate; documentation validator; `git diff --check`; and final code review.

## Manual Checks
Read the generated router and all steps for `ai-sdlc-sdd`, `ai-sdlc-code-review`, `ai-sdlc-working-backwards-discovery`, `ai-sdlc-security-testing`, and `ai-sdlc-flow`. Inspect Feature 013, change-set, and runtime OKF indexes; verify selectors match role ownership, procedures remain ordered, provenance is honest, paths match the hard cut, code examples remain intact, and no external framework or source is named.

## Signoff
Engineering and QA signoff require AC-001 through AC-022, no unresolved high-severity review findings, no generated drift, conformant Feature 013 bundles, and an auditable validation summary. Status remains pending until implementation evidence is recorded.
