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
  at: "2026-08-04T11:21:03Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "test-cases.md"
  path: "specs/020-context-graph-viewer/test-cases.md"
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
    - "specs/020-context-graph-viewer/tasks.md"
    - "specs/020-context-graph-viewer/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "context-graph-viewer"
---

# Test Cases

## Scope
Validate CLI discovery, deterministic rendering, full graph preservation, interaction data, source opt-in and highlighting, security boundaries, errors, packaging, and documentation.

## Scenario Matrix
| ID | Acceptance | Scenario | Expected result |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Run visualize against a compatible graph fixture through the supported CLI | Success receipt and self-contained HTML are created below cache |
| TC-002 | AC-002 | Render identical inputs twice | HTML bytes and content fingerprint are identical |
| TC-003 | AC-003 | Compare database and embedded graph counts and inspect the top shell | Every graph node and edge is included, full-corpus rendering succeeds, accessible filters remain outside the modal, and the shell uses compact neutral rectangular controls without decorative badge or pill classes |
| TC-004 | AC-004 | Select and inspect a node, compare every pane, navigate a relation, then dismiss the inspector | A centered role=dialog modal opens with one node header; Details contains row-based Properties plus direct incoming, outgoing, and source context without global graph statistics; Relations uses compact navigable rows for every edge; Source contains code and freshness; Close, Escape, and backdrop close it while selection remains |
| TC-005 | AC-005 | Render without --include-source | Source bodies are absent and metadata remains usable |
| TC-006 | AC-005 | Render with --include-source | Exact ranges, freshness, escaping, and safe syntax token classes are present |
| TC-007 | AC-006, AC-007 | Use stale source, malicious script-like text, or a symlinked path | Drift is labeled, unsafe paths fail closed, and content cannot terminate the data script or become markup |
| TC-008 | AC-006 | Use escaping, unrelated, or malformed output | Stable error receipt; no outside write or overwrite |
| TC-009 | AC-006 | Use absent, incompatible, or incomplete graph | Stable direct-read error; no implicit build |
| TC-010 | AC-001, AC-008 | Run installed-layout, help, focused test, docs, catalog, and diff checks | Helper is packaged, command is discoverable and documented, generated reference is current, and required checks pass |

## Layer Mapping
Unit: layout, escaping, tokenizer metadata, output containment, and deterministic bytes. Integration: SQLite fixture through render helper. CLI: parser, receipt, and failure envelopes. Documentation: catalog generation and source validation. Manual: full repository visual usability, keyboard search, zoom, selection, relation navigation, and code readability.

## Automation Plan
Add test_context_cache_viewer.py using temporary Git repositories and deterministic SQLite graph fixtures. Reuse context-cache builders where parser availability is not required. Validate HTML markers and embedded array sizes, compile JavaScript with Node when present, and execute focused unittest discovery.

## Open Gaps
Automated browser performance timing and pixel-level visual regression remain optional because the artifact has no bundled browser dependency. Manual full-corpus verification covers perceived usability; future WebGL work should add dedicated browser benchmarks.

