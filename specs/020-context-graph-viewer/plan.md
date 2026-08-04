---
type: "ai-sdlc.implementation-plan"
title: "Implementation Plan"
description: "Ordered implementation and validation plan."
tags:
  - "ai-sdlc"
  - "sdd"
  - "planning"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T11:57:21Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "plan.md"
  path: "specs/020-context-graph-viewer/plan.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/020-context-graph-viewer/_ai_sdlc/state.toon"
  decision_log: "specs/020-context-graph-viewer/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "plan"
    - "draft"
---

# plan.md

## Upstream Refinement Sources
- Refinement index: `specs-refiniment/_ai_sdlc/specs-index.toon`
- Refinement state: `specs-refiniment/<feature-name>/_ai_sdlc/state.toon`
- Delivery spec: `specs-refiniment/<feature-name>/delivery-spec.md`
- QA readiness: `specs-refiniment/<feature-name>/qa-readiness.md`
- Decision trace: `decision-log.md`

## SDD Artifact Links
- Requirements: `requirements.md`
- Design: `design.md`
- Test cases: `test-cases.md`
- QA: `qa.md`
- Tasks: `tasks.md`
- Machine plan: `_ai_sdlc/plan.toon`
- Decision log: `decision-log.md`

## Cross-Artifact Trace Map
- AC-001: requirements.md -> test-cases.md (TC-001, TC-010) -> tasks.md (T002, T004, T005, T006) -> qa.md -> decision-log.md
- AC-002: requirements.md -> test-cases.md (TC-002) -> tasks.md (T001, T004, T007) -> qa.md -> decision-log.md
- AC-003: requirements.md -> test-cases.md (TC-003) -> tasks.md (T001, T003, T004) -> qa.md -> decision-log.md
- AC-004: requirements.md -> test-cases.md (TC-004) -> tasks.md (T003, T004) -> qa.md -> decision-log.md
- AC-005: requirements.md -> test-cases.md (TC-005, TC-006) -> tasks.md (T001, T003, T004) -> qa.md -> decision-log.md
- AC-006: requirements.md -> test-cases.md (TC-007, TC-008, TC-009) -> tasks.md (T002, T004) -> qa.md -> decision-log.md
- AC-007: requirements.md -> test-cases.md (TC-007) -> tasks.md (T001, T004, T007) -> qa.md -> decision-log.md
- AC-008: requirements.md -> test-cases.md (TC-010) -> tasks.md (T005, T006, T007) -> qa.md -> decision-log.md

## Task Execution Plan
- [x] T001: Add deterministic graph_viewer.py with safe read-only extraction, layout, source opt-in, atomic output, and receipt data.; refs: FR-002, FR-003, FR-005, FR-007, FR-008, AC-002, AC-003, AC-005, AC-007, TC-001, TC-002, TC-003, TC-005, TC-006, TC-007; output: packaged standard-library renderer helper.
- [x] T002: Add visualize CLI parsing, containment, compatibility gates, and TOON success or error receipts.; refs: FR-001, FR-002, FR-006, FR-008, AC-001, AC-006, TC-001, TC-008, TC-009; output: supported reusable context_cache.py command.
- [x] T003: Deliver a cohesive Linear-inspired responsive application header, persistent top toolbar with restrained rectangular filters and view controls, and a concise responsive modal with one selected-node header, underline Details/Relations/Source navigation, row-based Properties, direct context metrics, compact relation navigation, keyboard controls, focus behavior, and safe offline syntax highlighting.; refs: FR-003, FR-004, FR-005, NFR-003, NFR-004, AC-003, AC-004, AC-005, TC-003, TC-004, TC-006, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006; output: compact neutral header, accessible top graph controls, and structured centered modal interaction runtime inside the self-contained HTML application.
- [x] T004: Add deterministic unit and CLI tests for rendering, counts, source opt-in, escaping, failures, and packaging.; refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010; output: test_context_cache_viewer.py and focused validation evidence.
- [x] T005: Document visualize in the skill and guide, refresh generated references, decision log, changelog, and spec indexes.; refs: AC-001, AC-008, TC-010; output: verified reusable command documentation and current catalogs.
- [x] T006: Prepare the additive v4.3.0 release candidate with Harness API 4.1.0, context-cache module 4.3.0, immutable install references, compatibility metadata, generated catalogs, and release validation.; refs: AC-001, AC-008, TC-010, DEC-007; output: validated v4.3.0 release metadata ready for an annotated tag and publication.
- [x] T007: Correct the protected-CI machine-boundary and router-budget failures, publish immutable v4.3.1 metadata, and validate the complete shared-runtime suite before tagging.; refs: AC-002, AC-007, AC-008, TC-002, TC-007, TC-010, DEC-008; output: compatible v4.3.1 corrective candidate with browser-native embedded data and a compliant context-cache router.

## Task Dependencies
- T001: depends on none
- T002: depends on T001
- T003: depends on T001
- T004: depends on T001, T002, T003
- T005: depends on T002, T004
- T006: depends on T005
- T007: depends on T006

## Validation Sequence
- 1. `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py <spec-dir> --full-flow`
- 2. `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py <spec-dir> --full-flow`
- 3. `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py <spec-dir> --full-flow`
- 4. `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py <spec-dir> --full-flow`
- Generated: 2026-08-04

## Open Links And Blockers
- No unresolved AC/TC/task links; decision and external blockers remain in `decision-log.md` and owner reports.
