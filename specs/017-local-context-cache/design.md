---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T09:42:39Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "design.md"
  path: "specs/017-local-context-cache/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids: []
  related_artifacts:
    - "specs/017-local-context-cache/decision-log.md"
    - "specs/017-local-context-cache/index.md"
    - "specs/017-local-context-cache/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
    - "context-cache"
---

# Design

## Overview
Add a separately selectable `context-cache` module whose skill owns a deterministic local index. The index is an optimization boundary: every hit retains source hashes and exact ranges, pack assembly rechecks freshness, and any uncertainty returns `direct_read` rather than stale evidence.

## Architecture
- Discovery layer: Git-aware safe file enumeration with conservative exclusions.
- Ingestion layer: stable line-window chunking plus heading, trace-ID, import, and path relations.
- Store layer: project-local SQLite database using normalized tables and FTS5; schema and configuration fingerprints guard compatibility.
- Retrieval layer: deterministic FTS ranking, explicit-path boosts, bounded graph traversal, deduplication, and stable tie-breaking.
- Pack layer: resolves the owning step from its validated manifest, inserts the complete step document first, verifies all declared critical anchors, adds fresh cache hits, enforces the 15 percent savings threshold, and validates the result with shared context-pack/v4 code.
- Evaluation layer: reads strict TOON golden cases and compares lexical-only, graph-enhanced, packed, and direct-read outcomes with stable fingerprints; wall-clock latency remains a separate observational tier.
- CLI and skill layer: build, update, query, pack, inspect, verify, purge, and lifecycle StepCards; stdout is canonical TOON only.

## Components
- `skills/ai-sdlc-context-cache/scripts/context_cache.py`: standard-library runtime and CLI.
- `references/context-cache.schema.toon` and `references/context-query.schema.toon`: portable contracts.
- `steps/manifest.toon` plus five procedural step documents: prepare, index/context, retrieve/execute, validate, handoff.
- `modules/context-cache/module.toon`: optional module requiring core.
- Installer module resolver: maps core plus requested modules to a deterministic skill inventory.
- Tests: ingestion, determinism, incremental updates, graph bounds, stale fallback, secret exclusion, pack compatibility, purge safety, and optional installation.

## Interfaces and Contracts
- `build --root PATH [--cache PATH]`: transactionally rebuild or incrementally update and emit an index receipt.
- `query --root PATH --query TEXT [--limit N] [--graph-depth N] [--graph-limit N]`: emit ranked fresh evidence and graph paths.
- `pack --root PATH --query TEXT --skill ID --step-id ID --budget-tokens N`: emit an owning-step and anchor-complete context-pack/v4 or direct-read fallback.
- `benchmark --root PATH --cases FILE.toon`: emit a deterministic golden evaluation receipt with path recall, anchor recall, strategy, savings, and mode fingerprints.
- `inspect` and `verify`: emit statistics, configuration, logical fingerprint, and freshness verdict.
- `purge`: remove only the validated project-local database and sidecars, returning an idempotent TOON receipt.
- Default cache path: `.ai-sdlc/cache/context-cache.sqlite3`; generated cache paths are excluded from ingestion and Git guidance.

## Data Model
- metadata(key, value): schema, configuration fingerprint, repository identity, logical index fingerprint.
- documents(path, sha256, byte_size, line_count, authority): current source identity.
- chunks(id, path, ordinal, start_line, end_line, sha256, token_estimate, heading, content): exact retrievable units.
- chunk_fts(content, heading, path, trace_ids): FTS5 projection keyed by chunk row.
- edges(source_chunk, target_chunk, kind, label): typed relations such as same-document, heading-reference, trace-id, import, and path-reference.
- Logical fingerprints hash canonical semantic rows, never SQLite page bytes or timestamps.

## Error Handling
Unsafe root or cache paths, symlinks, incompatible schemas, corrupt databases, unavailable FTS5, invalid bounds, and stale documents return typed TOON error or fallback receipts. Query never silently rebuilds. Pack may return `direct_read` with candidate paths and reasons, but never labels stale cache output sufficient.

## Security Considerations
Content is untrusted evidence. The runtime executes no retrieved commands, loads no plugins, follows no symlinks, makes no network calls, and reads bounded regular text only. Secret-like filenames and credential-like content are rejected before storage. SQLite parameters bind all values; FTS syntax is constructed only from normalized tokens. Purge resolves and confines every target before unlinking.

## Observability
Build receipts report discovered, indexed, unchanged, removed, and excluded counts plus semantic fingerprints. Query receipts explain normalized terms, lexical seeds, graph paths, scores, source hashes, freshness, raw and packed token estimates, and cache savings. Stable discovery, chunk IDs, sorted relations, integer scoring, bounded traversal, canonical TOON, and semantic fingerprints make repeated output reproducible.

## Risks and Tradeoffs
- FTS5 may be absent in a custom Python build; fail to direct reads and explain remediation.
- Heuristic relations are less precise than language-specific ASTs but stay portable and deterministic.
- A stale cache can mislead; source hash verification is mandatory before emitting sufficient results.
- Graph expansion can inflate context; explicit depth, node, result, and token budgets cap it.
- SQLite bytes are not reproducible across engines; only logical semantic fingerprints and TOON receipts are portability contracts.
- Mandatory instructions and explicit paths outrank retrieved evidence; cache hits never gain authority from relevance score.

## Validation Strategy
Run focused unit tests, repeated TOON golden benchmarks, per-skill test aggregation, context-pack/v4 validation, module discovery, two-clean-install comparisons for default and opt-in selection, TOON contract decoding, security abuse cases, docs catalog generation, strict documentation build, and full repository conformance.

## Migration Notes
Default installers keep the current complete baseline inventory except the optional cache skill. Users opt in with `./install.sh codex-project --module context-cache` or the Claude equivalent. Removing the module does not affect repository artifacts; deleting its disposable database restores direct-read behavior.
