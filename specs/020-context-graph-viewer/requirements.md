---
type: "ai-sdlc.requirements"
title: "Requirements"
description: "Implementation requirements, constraints, and acceptance criteria."
tags:
  - "ai-sdlc"
  - "sdd"
  - "requirements"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T11:21:02Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "requirements.md"
  path: "specs/020-context-graph-viewer/requirements.md"
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
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
  related_artifacts:
    - "specs/020-context-graph-viewer/branch-plan.md"
    - "specs/020-context-graph-viewer/decision-log.md"
    - "specs/020-context-graph-viewer/design.md"
    - "specs/020-context-graph-viewer/index.md"
    - "specs/020-context-graph-viewer/plan.md"
    - "specs/020-context-graph-viewer/qa.md"
    - "specs/020-context-graph-viewer/tasks.md"
    - "specs/020-context-graph-viewer/test-cases.md"
    - "specs/020-context-graph-viewer/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "context-graph-viewer"
---

# Requirements

## Goal
Provide a reusable professional offline HTML graph explorer inside ai-sdlc-context-cache so maintainers and developers can inspect the complete repository graph, direct relations, and source context through one supported command.

## Problem Statement
The context cache exposes deterministic graph facts and statistics but no human visual inspection surface. The current exploratory HTML prototype lives outside the skill, is not reproducible from the CLI, has no supported safety contract, and cannot be tested or reused across installed projects.

## Scope
Add a visualize subcommand and packaged standard-library renderer; generate a self-contained local HTML artifact from an existing compatible cache; render the complete graph with deterministic layout and performant canvas interaction; provide search, filters, selection, relation inspection, code ranges, source freshness, offline syntax highlighting, responsive professional UI, keyboard access, deterministic receipts, tests, and operator documentation.

## Actors
Repository developers explore definitions, calls, references, imports, tests, traces, and chunks. Harness maintainers own the viewer contract and release validation. Security reviewers verify output confinement, escaping, source opt-in, and absence of network dependencies.

## Inputs
Repository root, existing context-cache SQLite path, optional output path below the disposable cache boundary, graph nodes and edges, current repository source files when explicitly requested, and visualization bounds.

## Outputs
A self-contained HTML file below .ai-sdlc/cache plus a canonical TOON receipt identifying output path, source inclusion, node and edge counts, graph and repository fingerprints, freshness, byte size, and deterministic content hash.

## Functional Requirements
FR-001 expose visualize through context_cache.py in source and installed skill layouts. FR-002 read an existing compatible graph without warming, rebuilding, or mutating SQLite. FR-003 render every graph node and edge with deterministic positions, zoom, pan, fit, search, a persistent top filter bar for node layers and connections, and a type legend outside the inspector. FR-004 open a centered modal inspector when a node is selected; use one selected-node header, underline navigation, a Properties list, direct incoming/outgoing/source context, a compact relation list, and a source pane; navigate to related nodes inside the same modal; dismiss via Close, Escape, or backdrop click while preserving graph selection. FR-005 show exact source ranges with safe offline syntax highlighting when --include-source is supplied; otherwise expose metadata without source copies. FR-006 distinguish fresh and drifted source hashes and never present stale ranges as authoritative. FR-007 produce one self-contained HTML artifact with no CDN, telemetry, remote assets, model calls, or runtime network access. FR-008 emit a deterministic TOON receipt and stable HTML for identical inputs.

## Non-Functional Requirements
NFR-001 use Python standard library and browser-native APIs only. NFR-002 keep generated state disposable, Git-ignored, path-confined, symlink-safe, and escaped against HTML or script injection. NFR-003 remain usable for at least the current full corpus of 120000 nodes and 33000 edges through canvas rendering, static layout, bounded labels, and event-time filtering. NFR-004 provide a professional responsive Linear-inspired visual hierarchy with compact neutral surfaces, restrained rectangular controls, no decorative badge or pill treatments, keyboard search, accessible controls, readable empty and error states, and high-contrast code ranges. NFR-005 preserve repository authority and mark the viewer as a snapshot. NFR-006 keep portable machine output TOON-only; HTML is local disposable presentation state, not a portable contract.

## Constraints
The command requires an existing compatible cache with graph tables. Default output is .ai-sdlc/cache/context-graph.html. Explicit output must remain inside the resolved cache directory. Source content is excluded unless --include-source is explicit. Visualization does not install parsers, rebuild the graph, start a server, or open a browser.

## Acceptance Criteria
AC-001 visualize appears in --help and succeeds through source and installed skill paths. AC-002 identical compatible cache inputs produce byte-identical HTML and receipt fingerprints. AC-003 the artifact includes every stored graph node and edge, remains interactive on the full repository fixture, and exposes layer and connection filters in a persistent top bar outside the modal. AC-004 clicking a node opens a centered accessible modal with one selected-node header and task-specific Details, Relations, and Source panes; Details presents a compact Properties list and direct incoming, outgoing, and source context without unrelated global graph statistics; Relations lists every direct edge without truncation and supports in-place navigation; Close, Escape, and backdrop click dismiss the modal while graph selection remains. AC-005 --include-source shows escaped current code, exact selected line ranges, source hash freshness, and offline syntax highlighting; the default artifact contains no source bodies. AC-006 missing, incompatible, graph-incomplete, path-escaping, symlinked, or malformed inputs fail with stable error receipts and do not overwrite unrelated files. AC-007 generated HTML contains no external URL dependency, telemetry, executable repository content, or unescaped source injection. AC-008 documentation, generated skill reference, focused tests, skill tests, and diff checks pass.

## Out of Scope
Editing source, graph mutation, force-directed runtime layout, remote hosting, multi-repository federation, embeddings, graph database migration, source downloads, browser auto-launch, IDE integration, and treating the HTML artifact as durable evidence or authority.

## Assumptions
Modern local browsers provide Canvas 2D and standard DOM APIs. Static deterministic cluster layout is preferable to expensive force simulation for complete large graphs. Users who request --include-source accept a disposable local source copy inside the Git-ignored cache boundary.

## Open Questions
No blocking question remains. Future options include WebGL rendering, shareable redacted exports, editor deep links, and richer language-aware tokenization; each requires a separate contract because it changes dependencies, disclosure, or platform scope.

## Decision Status
All blocking decisions are resolved. Accepted assumptions: command name visualize; existing-cache read only; self-contained offline HTML; default no source bodies; explicit --include-source; output confined below .ai-sdlc/cache; deterministic static layout; centered modal inspector instead of a persistent drawer; Close, Escape, and backdrop dismissal; safe DOM-based syntax highlighting; no automatic browser launch. Owner: Harness Maintainers.

