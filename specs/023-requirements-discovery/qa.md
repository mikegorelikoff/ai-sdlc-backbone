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
  at: "2026-09-07T18:49:57Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "023-requirements-discovery"
  artifact: "qa.md"
  path: "specs/023-requirements-discovery/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/023-requirements-discovery/_ai_sdlc/state.toon"
  decision_log: "specs/023-requirements-discovery/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-09-07"
  updated_at: "2026-09-07"
  trace_ids:
    - "TC-001"
    - "TC-004"
    - "TC-005"
    - "TC-010"
  related_artifacts:
    - "specs/023-requirements-discovery/decision-log.md"
    - "specs/023-requirements-discovery/design.md"
    - "specs/023-requirements-discovery/index.md"
    - "specs/023-requirements-discovery/plan.md"
    - "specs/023-requirements-discovery/requirements.md"
    - "specs/023-requirements-discovery/tasks.md"
    - "specs/023-requirements-discovery/test-cases.md"
    - "specs/023-requirements-discovery/validation.md"
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
Add a source-backed requirements assistant with deterministic offline preparation, strict typed analysis validation and canonical report finalization to each product. Existing execution stages remain unchanged.

## Acceptance Scenarios
TC-001 through TC-004 cover selection, raw-request analysis, evidence limits and public discovery. TC-005 through TC-010 exercise repeatability, malformed data rejection, freshness, safe writes, installed helpers and Unicode projections.

## Regression Targets
Harness core inventory and v2 manifests; Loop installer profiles and Doctor inventory; source and installed helpers with sibling runtimes; generated catalogs, public paths and navigation.

## Risk Notes
Deterministic checks validate structure, traceability and local freshness; they do not authenticate stakeholder identity or prove model reasoning quality. Stdin is a fixed snapshot, not live conversation freshness. Source files are untrusted data. Publication remains paused by the user.

## Validation Commands
- python3 skills/ai-sdlc-requirements-discovery/tests/test_scripts.py -v
- python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_steps.py -v
- python3 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_modules.py -v
- python3.11 -m unittest discover -s skills/ai-sdlc-shared-runtime/tests -p test_native_install.py -v
- python3 -m unittest discover -s tests -v (Loop working directory)
- python3 docs/scripts/build_catalog.py --check (each product)
- python3 docs/scripts/validate_docs.py (each product)
- python3 -m unittest discover -s docs/tests -v (Harness)
- mkdocs build --strict (each product)
- python3 docs/scripts/validate_rendered.py site (each product)
- git diff --check (each product)

## Manual Checks
Review the bulk-approval fixture and product-local instructions: distinguish request from problem, measured evidence from an unmeasured pilot, material gaps from facts, and recommendation from accepted direction. Inspect full UTF-8 TOON and escaped Markdown; verify question-to-option links, source snapshot limitations and unresolved decision status.

## Signoff
Record actual check outcomes and update the SDD plan before marking implementation complete. A structurally complete packet conveys neither stakeholder acceptance nor execution authority. No commit or release is authorized after the user stop.
