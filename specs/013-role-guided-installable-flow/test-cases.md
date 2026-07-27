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
  at: "2026-07-27T12:13:45Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "013-role-guided-installable-flow"
  artifact: "test-cases.md"
  path: "specs/013-role-guided-installable-flow/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/013-role-guided-installable-flow/_ai_sdlc/state.toon"
  decision_log: "specs/013-role-guided-installable-flow/decision-log.md"
  status: "review"
  owner: "Engineering"
  created_at: "2026-07-27"
  updated_at: "2026-07-27"
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
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "REQ-001"
    - "REQ-011"
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
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
  related_artifacts:
    - "specs/013-role-guided-installable-flow/branch-plan.md"
    - "specs/013-role-guided-installable-flow/code-review.md"
    - "specs/013-role-guided-installable-flow/decision-log.md"
    - "specs/013-role-guided-installable-flow/design.md"
    - "specs/013-role-guided-installable-flow/plan.md"
    - "specs/013-role-guided-installable-flow/qa.md"
    - "specs/013-role-guided-installable-flow/requirements.md"
    - "specs/013-role-guided-installable-flow/tasks.md"
    - "specs/013-role-guided-installable-flow/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "accepted"
---

# Test Cases

## Scope
Cover REQ-001 through REQ-015 and AC-001 through AC-022 at unit, contract, integration, installation, documentation, progressive-disclosure, OKF conformance, migration, and repository-validation layers.

## Scenario Matrix
| ID | Scenario | Expected | Refs |
| --- | --- | --- | --- |
| TC-001 | Scan tracked tree and imports | `_shared` absent; canonical runtime only | AC-001 |
| TC-002 | Full project install | runtime and selected skills execute | AC-002 |
| TC-003 | Selective install | transitive runtime installed once | AC-002 |
| TC-004 | Disposable-global install | no source fallback or real-home mutation | AC-002 |
| TC-005 | Validate five role contracts | exactly five complete, neutral contracts | AC-003 |
| TC-006 | Route clear intent | one role/action selected directly | AC-004 |
| TC-007 | Route ambiguous intent | deterministic menu returned | AC-004 |
| TC-008 | Apply valid overrides and aliases | explicit role/action wins deterministically | AC-004, AC-009 |
| TC-009 | Cross-role prerequisite | handoff reason and required stage emitted | AC-005 |
| TC-010 | Parse v1 payload | rejected with v2 migration guidance | AC-006 |
| TC-011 | Select JIT context | current flow and owning-skill steps only; selected/skipped reasons present | AC-007, AC-016 |
| TC-012 | Attempt traversal/symlink/oversize | fail closed with actionable error | AC-008, AC-015 |
| TC-013 | Validate bounded flow config | valid accepted; unknown/out-of-range rejected | AC-009 |
| TC-014 | Run context benchmark twice | 100% recall, >=15% savings, stable fingerprints | AC-010 |
| TC-015 | Regenerate docs | no drift; roles, flow steps, skill steps, and selectors documented | AC-011, AC-016 |
| TC-016 | Execute full validation matrix | all deterministic checks and review pass | AC-012 |
| TC-017 | Validate every skill step manifest | 44/44 valid, contained, linked, deterministic manifests | AC-013 |
| TC-018 | Measure routers before and after migration | every router <120 lines; aggregate words reduced >=60%; normative contract preserved | AC-014 |
| TC-019 | Select prepare/execute/validate across representative roles | correct record, reason, token count, and stable fingerprint; invalid inputs fail closed | AC-015 |
| TC-020 | Install full/selective/global copies and Explore a route | copied manifests resolve without source checkout; DecisionCard includes owning-skill step | AC-016 |
| TC-021 | Render and refresh representative lifecycle concepts | OKF fields and nested metadata coexist; actor/timestamp/status/verification rules hold | AC-017, AC-019 |
| TC-022 | Validate Feature 013 bundles and indexes | every concept conforms; reserved indexes declare/group/link content deterministically | AC-017, AC-020 |
| TC-023 | Exercise every durable writer family | shared profile required; generated Markdown validates in feature/change/runtime bundles | AC-018, AC-021 |
| TC-024 | Generate project context and module catalog | only new `_ai_sdlc` paths exist; no legacy root/human-index output or fallback | AC-020 |
| TC-025 | Create change set and external snapshot | reserved subindexes are valid; snapshot source evidence/body remains traceable | AC-018, AC-021 |
| TC-026 | Write to legacy feature with a conflict fixture | complete atomic migration succeeds or leaves the original tree byte-identical on failure | AC-022 |

## Layer Mapping
Unit: TC-005 through TC-014, TC-019, TC-021, and TC-026. Contract/schema: TC-005, TC-010, TC-013, TC-017, TC-018, and TC-022. Integration: TC-001, TC-006 through TC-011, TC-015, TC-020, TC-023, TC-024, and TC-025. Installation: TC-002 through TC-004, TC-020, TC-023, and TC-024. Repository regression: TC-016 through TC-026.

## Automation Plan
Use Python unittest scripts already present in skills, the canonical step-selector and OKF validators, temporary repositories and homes, deterministic subprocess calls, docs drift checks, full runtime discovery, focused flow/config/manifest/install modules, writer-family contract fixtures, atomic migration snapshots, router-size metrics, and contract-preservation scans over each router plus its declared steps.

## Open Gaps
None before implementation. If the context benchmark cannot demonstrate the target on representative fixtures, implementation remains incomplete rather than weakening AC-010.
