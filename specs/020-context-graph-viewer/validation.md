---
type: "ai-sdlc.validation"
title: "Validation Evidence"
description: "Focused validation outcomes for the reusable context graph viewer."
tags:
  - "ai-sdlc"
  - "validation"
status: "stable"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "validation.md"
  path: "specs/020-context-graph-viewer/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "quick"
  state_file: "specs/020-context-graph-viewer/_ai_sdlc/state.toon"
  decision_log: "specs/020-context-graph-viewer/decision-log.md"
  status: "validated"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids:
    - "AC-003"
    - "AC-004"
    - "AC-008"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "T006"
    - "TC-003"
    - "TC-004"
  related_artifacts:
    - "specs/020-context-graph-viewer/_ai_sdlc/validation-receipt.toon"
    - "specs/020-context-graph-viewer/requirements.md"
    - "specs/020-context-graph-viewer/test-cases.md"
    - "specs/020-context-graph-viewer/qa.md"
    - "specs/020-context-graph-viewer/tasks.md"
  validation:
    - "canonical argv-only validation receipt: current"
    - "focused viewer tests: passed on Python 3.9 and Python 3.11"
    - "documentation validation and 47 documentation tests: passed"
    - "SDD clarify, checklist, structure, analyze, and plan-link gates: passed"
    - "full 121857-node Linear-inspired HTML render, concise-modal shell check, and embedded JavaScript parse: passed"
    - "v4.3.0 compatibility, native installation, all-skill, documentation, online and offline strict build gates: passed"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
---

# Validation Evidence

## Scope

Validate the compact Linear-inspired responsive header, badge-free persistent
top graph controls, concise structured node modal, complete relation
navigation, source view, deterministic generation, documentation, and SDD
traceability.

## Results

- PASS: focused viewer tests on Python 3.9 and Python 3.11.
- PASS: the fresh full cache rendered 121,857 nodes and 33,694 edges; embedded
  JavaScript parsed successfully, the concise modal contract is present, and
  legacy badge classes are absent from the generated UI shell.
- PASS: graph filters, connection visibility, fit, and zoom are outside the
  modal; the modal has one selected-node header and task-specific Details,
  Relations, and Source panes without duplicated global graph statistics.
- PASS: Details separates row-based properties from direct incoming/outgoing
  context; Relations exposes every direct edge as a keyboard-reachable target.
- PASS: documentation catalog check, documentation validator, and 47 tests.
- PASS: SDD clarify, checklist, structural, analyze, plan-link, and diff checks.
- PASS: the `v4.3.0` candidate preserves Harness API `4.1.0`, advances the
  optional context-cache module to `4.3.0`, and passes the exact compatibility
  gate against `v2.1.0` with the pending release commit explicitly allowed.
- PASS: all 29 shared script-contract tests, every per-skill test file, the
  native project installation smoke, and 35 Python 3.11 context-cache tests.
- PASS: strict documentation builds passed with the hash-locked dependencies
  online and then offline; rendered validation resolved all 5,555 local targets
  across 207 HTML pages.

## Residual Risk

Pixel-level browser automation was unavailable in this environment. The final
self-contained HTML was opened locally for visual review; DOM contracts and
embedded JavaScript were validated deterministically.
