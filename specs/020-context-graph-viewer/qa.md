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
  at: "2026-08-04T11:21:03Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "qa.md"
  path: "specs/020-context-graph-viewer/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/020-context-graph-viewer/_ai_sdlc/state.toon"
  decision_log: "specs/020-context-graph-viewer/decision-log.md"
  status: "review"
  owner: "Harness Maintainers"
  created_at: "2026-08-04"
  updated_at: "2026-08-04"
  trace_ids: []
  related_artifacts:
    - "specs/020-context-graph-viewer/branch-plan.md"
    - "specs/020-context-graph-viewer/decision-log.md"
    - "specs/020-context-graph-viewer/design.md"
    - "specs/020-context-graph-viewer/index.md"
    - "specs/020-context-graph-viewer/plan.md"
    - "specs/020-context-graph-viewer/requirements.md"
    - "specs/020-context-graph-viewer/tasks.md"
    - "specs/020-context-graph-viewer/test-cases.md"
    - "specs/020-context-graph-viewer/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
    - "context-graph-viewer"
---

# QA

## Change Summary
Add a reusable offline graph viewer command and packaged professional HTML explorer without changing cache authority or existing retrieval behavior.

## Acceptance Scenarios
Verify command discovery, default and explicit output, full node and edge presence, deterministic rerender, search, a compact Linear-inspired top shell without decorative badge or pill treatments, persistent layer and connection controls, click selection, centered modal opening, one selected-node header, underline Details, Relations, and Source navigation, row-based Properties, direct incoming, outgoing, and source context, absence of unrelated global graph statistics, compact accessible relation rows, relation navigation within the same modal, Close, Escape and backdrop dismissal, source opt-in, freshness labeling, safe syntax highlighting, responsive modal layout, and meaningful empty/error states.

## Regression Targets
Existing build, warm, query, pack, benchmark, inspect, verify, observe, purge, graph-preflight, and graph-stats commands; module packaging; generated skill reference; cache path safety; TOON receipts.

## Risk Notes
Primary risks are source disclosure, HTML injection, output escape, huge artifacts, sluggish interaction, stale range confusion, and generated-reference drift. Controls are explicit source opt-in, containment, escaping and text nodes, deterministic canvas layout, freshness labels, and focused tests.

## Validation Commands
python3 -m unittest skills.ai-sdlc-context-cache.tests.test_context_cache_viewer -v
python3 -m unittest discover -s skills/ai-sdlc-context-cache/tests -v
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
git diff --check

## Manual Checks
Generate the full repository viewer with --include-source; open locally; verify the compact desktop and narrow layouts; confirm layer filters, Connections, Fit, and zoom controls stay in the top bar; search context_cache; select file, symbol, call, occurrence, chunk, and trace hub nodes; confirm each selection opens the centered modal with one type, title, and path header; confirm Details shows only Properties plus direct incoming, outgoing, and source context; confirm Relations uses readable compact rows and navigates between neighbors without closing; verify Source highlighting and stale warning; close with the button, Escape, and backdrop; confirm graph selection remains.

## Signoff
Quick-flow implementation may complete when all automated focused checks pass and the full-corpus artifact is manually inspected. Broader release signoff and browser performance baselines remain maintainer-owned.

