---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-04T11:51:12Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "020-context-graph-viewer"
  artifact: "design.md"
  path: "specs/020-context-graph-viewer/design.md"
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
    - "specs/020-context-graph-viewer/index.md"
    - "specs/020-context-graph-viewer/plan.md"
    - "specs/020-context-graph-viewer/qa.md"
    - "specs/020-context-graph-viewer/requirements.md"
    - "specs/020-context-graph-viewer/tasks.md"
    - "specs/020-context-graph-viewer/test-cases.md"
    - "specs/020-context-graph-viewer/validation.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
    - "context-graph-viewer"
---

# Design

## Overview
Package the validated prototype as a renderer helper owned by ai-sdlc-context-cache and invoke it from a new visualize CLI branch. Keep cache authority, data extraction, presentation generation, and browser interaction separated.

## Architecture
context_cache.py validates root, cache compatibility, graph completeness, freshness metadata, and output containment, then calls graph_viewer.render. graph_viewer.py reads SQLite in read-only URI mode, constructs deterministic compact arrays and optional source snapshots, renders a self-contained HTML template, atomically replaces the target, and returns receipt fields. Browser JavaScript performs canvas rendering and local DOM interaction only.

## Components
CLI parser and dispatch; viewer request validation; read-only graph extractor; deterministic cluster layout; cohesive Linear-inspired responsive application header with compact product identity, primary search, graph counts, and plain local status; canvas renderer; persistent top toolbar with accessible rectangular layer, connection, fit, and zoom controls; centered accessible modal inspector with one selected-node header, underline Details/Relations/Source navigation, a row-based Properties list, direct incoming/outgoing/source context, compact relation rows with in-place navigation, source code range view, focus management, and backdrop dismissal; safe tokenizer; receipt builder; focused unit and CLI tests.

## Interfaces and Contracts
Command: context_cache.py visualize --root ROOT [--cache CACHE] [--output OUTPUT] [--include-source]. Default output resolves to ROOT/.ai-sdlc/cache/context-graph.html. Success receipt schema is ai-sdlc-context-graph-view/v1. Errors reuse the existing stable ai-sdlc-context-cache-error/v1 envelope.

## Data Model
Compact node rows contain id, kind, path, label, x, y, start line, and end line. Edge rows contain source index, target index, kind, label, and evidence path. Optional source rows map repository path to text and current-hash-match boolean. All ordering is canonical and every dynamic string uses deterministic browser-native literal encoding with less-than escaped.

## Error Handling
Reject absent or incompatible cache, missing graph tables, incomplete graph, output escape, symlink boundary, non-file overwrite target, and read or atomic-write failures. Never rebuild implicitly. Preserve an existing target until a complete temporary artifact is fsynced and atomically replaced.

## Security Considerations
Open SQLite read-only. Confine output to the cache directory. Reject symlinks. Do not include source by default. When enabled, include only currently indexed repository-contained regular non-symlink files. Escape embedded script boundaries and build code tokens with text nodes, never source-derived innerHTML. Use a restrictive local Content-Security-Policy with no network sources.

## Observability
Return node, edge, path, source-file, stale-source, byte counts, include_source, fresh, graph fingerprint, repository fingerprint, output path, and content SHA-256 in canonical TOON. Do not record queries, code, labels, identity, or wall-clock time.

## Risks and Tradeoffs
A self-contained complete graph can be tens of megabytes; accepted because output is explicit and local. Canvas 2D avoids dependencies but provides less advanced layout than WebGL. Syntax highlighting is intentionally lightweight and language-family based; exact source text and range identity matter more than parser-perfect coloring.

## Validation Strategy
Use synthetic SQLite fixtures for deterministic output, complete counts, no-source default, source opt-in, escaping, stale hashes, relation coverage, modal presence and dismissal contracts, containment, symlinks, and CLI receipts. Compile embedded JavaScript with Node when available and assert no external network locators. Run context-cache tests and documentation validators.

## Migration Notes
Additive command only. Existing cache schema, query, pack, build, verify, and graph-stats behavior remains unchanged. Installed context-cache modules receive the helper through normal skill packaging without new dependencies.

