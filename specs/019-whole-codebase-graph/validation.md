---
type: "ai-sdlc.validation-report"
title: "Validation Report"
description: "Deterministic production evidence for the whole-codebase AST graph."
tags:
  - "ai-sdlc"
  - "validation"
  - "whole-codebase-graph"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "validation.md"
  path: "specs/019-whole-codebase-graph/validation.md"
  workspace: "implementation"
  skill: "ai-sdlc-validation"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
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
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/_ai_sdlc/validation-plan.toon"
    - "specs/019-whole-codebase-graph/_ai_sdlc/validation-receipt.toon"
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
    - "specs/019-whole-codebase-graph/qa.md"
  validation:
    - "31 focused context-cache and graph tests passed"
    - "178 shared-runtime tests passed"
    - "47 documentation tests passed"
    - "two-run full-corpus graph audit passed"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-validation"
    - "validation"
    - "validated"
---

# Validation

## Result

Full-flow validation passes for AC-001 through AC-008 and TC-001 through
TC-024. The graph is built only from pinned Tree-sitter AST parsers, remains
offline and bounded, and fails closed to authoritative direct reads whenever
completeness, freshness, safety, recall, or economics cannot be proven.

## Commands and Outcomes

| Command | Outcome | Coverage |
| --- | --- | --- |
| Focused context-cache suites under the pinned Python 3.11 graph runtime | passed: 31 tests | exact lock completeness, twelve languages, native-crash isolation, graph lifecycle, retrieval, bounds, fallback, unsafe inputs |
| Two-run `release_graph_audit.py` on the repository | passed | equal cache fingerprints, complete graph, bounded relations, 100 percent critical recall, token economics |
| Parser fault injection audit | expected failure observed | parser failure forces `production_ready: false` and a non-zero result |
| Offline install smoke and lock verification | passed: 13 hashes and 12 grammars | runtime network denial, exact wheel provenance, Kotlin and Swift parity |
| Python 3.9 context-cache compatibility suite | passed: 11 tests | lexical and direct-read behavior on a host outside graph mode |
| Shared-runtime discovery suite | passed: 178 tests | harness lifecycle, TOON, installer, state, context, module, and per-skill regression |
| Documentation validation and tests | passed: 206 pages and 47 tests | generated catalog, public contracts, navigation, links, and executable help |
| Full refinement and SDD gates | passed | 18-stage upstream package, implementation traceability, plan links, and status |
| `git diff --check` | passed | patch whitespace and conflict-marker hygiene |

## Production Evidence

The latest completed real-corpus run before this report indexed 1,305 safe
files, parsed 212 selected-language files, emitted 119,662 graph nodes and
32,822 bounded typed edges, retained 100 percent of critical anchors, and
reported 87.19 percent estimated token savings. Its two independent builds had
the same cache fingerprint. The canonical validation receipt reruns the same
gate against the finalized validation inputs.

## Context Engineering Evidence

Retrieval combines lexical and symbol seeds with deterministic typed traversal,
stable tie-breaks, authority labels, exact source hashes, mandatory anchors, and
a bounded token budget. Packed output is accepted only at the configured
economics threshold; otherwise the consumer receives explicit direct-read
paths. Repository text remains untrusted evidence and cannot gain instruction
authority through graph proximity.

## Residual Risk

The checked wheel hashes and ABI smoke are for the declared CPython 3.11 macOS
arm64 target available in this environment. Other declared targets require the
same offline lock verification in protected CI. Independent security testing
and code review completed with no unresolved finding; protected remote CI is
the remaining environment-specific confirmation after push.
