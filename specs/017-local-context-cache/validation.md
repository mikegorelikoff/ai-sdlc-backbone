---
type: "ai-sdlc.validation-report"
title: "Validation Report"
description: "Current deterministic validation evidence for the optional local context cache."
tags:
  - "ai-sdlc"
  - "validation"
  - "context-cache"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "validation.md"
  path: "specs/017-local-context-cache/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "validated"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
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
    - "TC-011"
    - "TC-012"
    - "TC-013"
  related_artifacts:
    - "specs/017-local-context-cache/_ai_sdlc/validation-plan.toon"
    - "specs/017-local-context-cache/_ai_sdlc/validation-receipt.toon"
    - "specs/017-local-context-cache/security-review.md"
    - "specs-refiniment/017-local-context-cache/_ai_sdlc/full-flow-receipt.toon"
  validation:
    - "ai-sdlc-validation-receipt/v1: 17 current commands; 0 failures"
    - "ai-sdlc-context-pack/v4: 100 percent critical recall; 77.77 percent savings"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
    - "context-cache"
---

# Validation

## Result

The optional local context cache passes the full-flow implementation gates. The
canonical argv-only TOON validation receipt binds 17 commands to the current
workspace fingerprint with no failed command.

## Coverage

- Safe deterministic discovery, chunking, incremental invalidation, SQLite
  FTS5 indexing, stable lexical scoring, typed graph expansion, and TOON output.
- Context-pack/v4 authority separation, owning-step inclusion, complete critical
  anchors, freshness checks, context economics, and direct-read fallback.
- Deterministic lexical, graph-enhanced, and pack benchmark fingerprints with
  correctness metrics separated from observational latency.
- Explicit optional installation, unchanged default inventory, compatibility
  baselines, all semantic skill graphs, and native Codex and Claude profiles.
- Complete refinement cascade, full SDD gates, documentation catalogs, source
  checks, rendered links, and repository diff hygiene.

## Context Engineering Evidence

The validation execute step was compiled through the new cache itself. The pack
included the complete owning step document, retained 3 of 3 critical anchors,
used evidence_only for retrieved repository text, and reduced the estimated
context from 24,561 to 5,459 tokens, a 77.77 percent saving.

## Security

The full-flow security review found no open critical, high, or medium finding.
Accepted residual risks are heuristic secret detection, downstream model
susceptibility to adversarial evidence, cache readability matching repository
filesystem permissions, and SQLite build compatibility.

## Residual Risk

This MVP is local graph-enhanced RAG, not an LLM-based GraphRAG community and
entity extraction pipeline. Optional embeddings and community summaries remain
future extensions. Wall-clock latency stays outside deterministic golden
receipts as a separate observational tier.
