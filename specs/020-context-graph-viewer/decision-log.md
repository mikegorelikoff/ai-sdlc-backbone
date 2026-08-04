---
type: "ai-sdlc.decision-log"
title: "Decision Log"
description: "Auditable decisions, evidence, alternatives, and traceability."
tags:
  - "ai-sdlc"
  - "decision"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T10:17:58Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "decision-log.md"
  path: "specs/020-context-graph-viewer/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/020-context-graph-viewer/_ai_sdlc/state.toon"
  decision_log: "specs/020-context-graph-viewer/decision-log.md"
  status: "draft"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
    - "context-graph-viewer"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-08-04 | accepted | Harness Maintainers | Package the graph explorer as the offline visualize command with source embedding opt-in | The working prototype proves full-graph inspection while repository contracts require reusable deterministic local tooling | Keep a temporary script; ship a separate web app; package a standard-library skill renderer | skills/ai-sdlc-context-cache/scripts/graph_viewer.py; skills/ai-sdlc-context-cache/scripts/context_cache.py; docs/how-to/use-local-context-cache.md | AC-001; AC-005; AC-006; AC-007; TC-001; TC-005; TC-008 |
| DEC-002 | 2026-08-04 | accepted | User | Replace the persistent right-side inspector drawer with a centered modal dialog | The user explicitly requested modal interaction so the graph remains visually primary and the inspector appears only when a node is selected | Keep persistent drawer; use modal dialog; use bottom sheet | skills/ai-sdlc-context-cache/scripts/graph_viewer.py; specs/020-context-graph-viewer/design.md; specs/020-context-graph-viewer/test-cases.md | AC-004; NFR-004; TC-004; T003 |
| DEC-003 | 2026-08-04 | accepted | User | Keep graph layer and connection filters in a persistent top filter bar outside the node modal and simplify the modal around selected-node context | The user requested filters above the graph and explicitly removed them from the modal while asking for a clearer modal hierarchy | Filters inside modal; left toolbar; top filter bar | skills/ai-sdlc-context-cache/scripts/graph_viewer.py; specs/020-context-graph-viewer/design.md; specs/020-context-graph-viewer/test-cases.md | AC-003; AC-004; NFR-004; TC-003; TC-004; T003 |
| DEC-004 | 2026-08-04 | accepted | User | Replace separated floating header cards with one cohesive responsive application header that prioritizes product identity, search, and local graph status | The user explicitly requested a better header after moving controls to the second top row | Keep split cards; unified application header; minimal search-only header | skills/ai-sdlc-context-cache/scripts/graph_viewer.py | NFR-004; TC-003; T003 |
| DEC-005 | 2026-08-04 | accepted | User | Restyle the viewer with a Linear-inspired neutral interface and remove decorative badge and pill treatments | The user requested less badge-like chrome and a closer fit to Linear while preserving all graph controls and semantic status | keep current pill-heavy chrome; remove only the header status pill; apply a restrained rectangular control language throughout the viewer | skills/ai-sdlc-context-cache/scripts/graph_viewer.py; skills/ai-sdlc-context-cache/tests/test_context_cache_viewer.py; requirements.md; design.md; test-cases.md; qa.md; tasks.md | NFR-004; AC-003; AC-004; TC-003; TC-004; T003 |
| DEC-006 | 2026-08-04 | accepted | User | Restructure the node modal as a concise node workspace with a single hierarchy and task-specific panes | The user found the current modal visually heavy and unstructured; global graph statistics compete with selected-node information | retain two equal overview cards; use a right drawer; use a compact modal with node header, underline navigation, node facts, local relation context, and source pane | skills/ai-sdlc-context-cache/scripts/graph_viewer.py; skills/ai-sdlc-context-cache/tests/test_context_cache_viewer.py; requirements.md; design.md; test-cases.md; qa.md; tasks.md | NFR-004; AC-004; TC-004; T003 |
| DEC-007 | 2026-08-04 | accepted | Harness Maintainers | Publish the additive graph viewer as AI SDLC Harness v4.3.0 while keeping Harness API 4.1.0 | The release adds an opt-in offline visualization command without changing existing commands, cache schemas, lifecycle contracts, or installation profiles | Patch v4.2.3; minor v4.3.0; Harness API major change | CHANGELOG.md; README.md; install.sh; compatibility/baseline-v1.toon; modules/context-cache/module.toon; docs/reference/versions.md | AC-001; AC-008; TC-010; T006 |
| DEC-008 | 2026-08-04 | accepted | Harness Maintainers | Preserve immutable v4.3.0 and publish corrective v4.3.1 after protected CI exposed two repository-contract violations | Both Python 3.10 and 3.13 jobs rejected a forbidden alternate machine-encoding token in the viewer and design plus a context-cache router one line above the strict budget; local focused tests did not include the complete shared-runtime discovery suite | Rewrite v4.3.0; leave the failed release current; publish v4.3.1 with the corrected browser-native encoder and compact router | skills/ai-sdlc-context-cache/scripts/graph_viewer.py; skills/ai-sdlc-context-cache/SKILL.md; specs/020-context-graph-viewer/design.md; CHANGELOG.md; docs/reference/versions.md; compatibility/baseline-v1.toon | AC-002; AC-007; AC-008; TC-002; TC-007; TC-010; T007 |
