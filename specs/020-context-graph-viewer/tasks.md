---
type: "ai-sdlc.tasks"
title: "Implementation Tasks"
description: "Traceable implementation task breakdown and status."
tags:
  - "ai-sdlc"
  - "sdd"
  - "tasks"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T11:57:17Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "tasks.md"
  path: "specs/020-context-graph-viewer/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/020-context-graph-viewer/_ai_sdlc/state.toon"
  decision_log: "specs/020-context-graph-viewer/decision-log.md"
  status: "review"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "DEC-008"
    - "NFR-003"
    - "NFR-004"
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
  related_artifacts:
    - "specs/020-context-graph-viewer/branch-plan.md"
    - "specs/020-context-graph-viewer/decision-log.md"
    - "specs/020-context-graph-viewer/design.md"
    - "specs/020-context-graph-viewer/index.md"
    - "specs/020-context-graph-viewer/plan.md"
    - "specs/020-context-graph-viewer/qa.md"
    - "specs/020-context-graph-viewer/requirements.md"
    - "specs/020-context-graph-viewer/test-cases.md"
    - "specs/020-context-graph-viewer/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
    - "context-graph-viewer"
---

# Tasks

## Implementation
- [x] T001. Add deterministic graph_viewer.py with safe read-only extraction, layout, source opt-in, atomic output, and receipt data.
Output: packaged standard-library renderer helper.
Refs: FR-002, FR-003, FR-005, FR-007, FR-008, AC-002, AC-003, AC-005, AC-007, TC-001, TC-002, TC-003, TC-005, TC-006, TC-007
Depends on: none
- [x] T002. Add visualize CLI parsing, containment, compatibility gates, and TOON success or error receipts.
Output: supported reusable context_cache.py command.
Refs: FR-001, FR-002, FR-006, FR-008, AC-001, AC-006, TC-001, TC-008, TC-009
Depends on: T001
- [x] T003. Deliver a cohesive Linear-inspired responsive application header, persistent top toolbar with restrained rectangular filters and view controls, and a concise responsive modal with one selected-node header, underline Details/Relations/Source navigation, row-based Properties, direct context metrics, compact relation navigation, keyboard controls, focus behavior, and safe offline syntax highlighting.
Output: compact neutral header, accessible top graph controls, and structured centered modal interaction runtime inside the self-contained HTML application.
Refs: FR-003, FR-004, FR-005, NFR-003, NFR-004, AC-003, AC-004, AC-005, TC-003, TC-004, TC-006, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006
Depends on: T001

## Testing
- [x] T004. Add deterministic unit and CLI tests for rendering, counts, source opt-in, escaping, failures, and packaging.
Output: test_context_cache_viewer.py and focused validation evidence.
Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010
Depends on: T001, T002, T003

## Documentation
- [x] T005. Document visualize in the skill and guide, refresh generated references, decision log, changelog, and spec indexes.
Output: verified reusable command documentation and current catalogs.
Refs: AC-001, AC-008, TC-010
Depends on: T002, T004
- [x] T006. Prepare the additive v4.3.0 release candidate with Harness API 4.1.0, context-cache module 4.3.0, immutable install references, compatibility metadata, generated catalogs, and release validation.
Output: validated v4.3.0 release metadata ready for an annotated tag and publication.
Refs: AC-001, AC-008, TC-010, DEC-007
Depends on: T005
- [x] T007. Correct the protected-CI machine-boundary and router-budget failures, publish immutable v4.3.1 metadata, and validate the complete shared-runtime suite before tagging.
Output: compatible v4.3.1 corrective candidate with browser-native embedded data and a compliant context-cache router.
Refs: AC-002, AC-007, AC-008, TC-002, TC-007, TC-010, DEC-008
Depends on: T006

