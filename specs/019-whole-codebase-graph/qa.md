---
type: "ai-sdlc.qa-plan"
title: "QA Plan"
description: "Acceptance, regression, risk, and manual validation plan."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T20:13:42Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "qa.md"
  path: "specs/019-whole-codebase-graph/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "TC-001"
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/branch-plan.md"
    - "specs/019-whole-codebase-graph/decision-log.md"
    - "specs/019-whole-codebase-graph/design.md"
    - "specs/019-whole-codebase-graph/plan.md"
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/tasks.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
---

# QA

## Change Summary
QA validates the feature-018 cache upgrade into an optional twelve-language AST code graph over the whole safe corpus, with Kotlin and Swift mandatory, typed bounded retrieval, TOON-only evidence, offline parser operation, deterministic incremental lifecycle, safe direct-read fallback, and measurable token savings.

## Acceptance Scenarios
QA-001 locked offline parser preflight; QA-002 whole-safe-corpus accounting; QA-003 twelve-language AST fixture matrix; QA-004 missing grammar and parse-error rejection; QA-005 stable graph IDs and atomic migration; QA-006 bounded hubs and traversal; QA-007 incremental freshness and drift rejection; QA-008 golden recall and qualified disambiguation; QA-009 anchor-preserving 25 percent savings; QA-010 stable TOON fallback; QA-011 deterministic stats; QA-012 real-corpus production audit.

## Regression Targets
Protect feature-018 build/query/pack/verify/purge/observe behavior, context-pack/v4 validation, StepCard budget and authority constraints, source-checkout non-activation, optional-module installation, direct_read parity, FTS fallback, cache confinement, unsafe-source exclusion, docs/catalog validation, and all existing shared-runtime tests.

## Risk Notes
P0: parser supply-chain or ABI drift, missing Kotlin/Swift coverage, false AST completeness, stale/partial publication, graph explosion, unsafe ingestion, authority widening, or non-TOON portable output. P1: recall or savings regression and operational ambiguity. No P0 failure or missing target evidence may be waived for production.

## Validation Commands
Run install_graph_smoke.py offline; the three focused graph unittest files; existing context-cache and shared-runtime suites; release_graph_audit.py twice with TOON output; docs validation/tests; module install smoke; generated-catalog checks; security testing; code review; SDD validation; and git diff --check. Record exact commands, runtimes, outcomes, and fingerprints in validation.md.

## Manual Checks
Harness Maintainers and Security inspect parser-lock provenance/licenses, one Kotlin and one Swift fact set, an accepted graph pack, a missing-grammar fallback, dense-graph stats, incremental deletion, cache confinement, network-denied execution, and operator documentation. Manual checks supplement but never replace automated P0 gates.

## Signoff
Status: ready for implementation, not release-approved. QA signs only after TC-001 through TC-024 pass, the real-corpus audit passes twice, accepted savings is at least 0.25, graph_complete covers every observed selected-language file, all portable outputs are TOON, security/code review have no unresolved high finding, and regression/install/docs gates are green.
