---
type: "ai-sdlc.code-review"
title: "Code Review"
description: "Independent findings-first review of the whole-codebase AST graph implementation."
tags:
  - "ai-sdlc"
  - "code-review"
  - "whole-codebase-graph"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "code-review.md"
  path: "specs/019-whole-codebase-graph/code-review.md"
  workspace: "implementation"
  skill: "ai-sdlc-code-review"
  flow_mode: "full"
  state_file: "specs/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs/019-whole-codebase-graph/decision-log.md"
  status: "approved"
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
    - "TC-021"
    - "TC-023"
    - "TC-024"
  related_artifacts:
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/design.md"
    - "specs/019-whole-codebase-graph/test-cases.md"
    - "specs/019-whole-codebase-graph/validation.md"
    - "specs/019-whole-codebase-graph/security-review.md"
  validation:
    - "independent diff and contract review completed"
    - "all review findings fixed before approval"
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-code-review"
    - "code-review"
    - "approved"
---

# Code Review

## Findings

No unresolved finding remains in the reviewed diff.

| Severity | Evidence | Independent finding | Resolution |
| --- | --- | --- | --- |
| Medium | `install_graph_runtime.py`; parser lock | Verify mode accepted the hashes of whatever wheel rows were present but did not prove that the runtime, all twelve grammars, and all thirteen wheels were present exactly once. | Added one shared strict lock validator used by installer and smoke. It rejects partial, duplicate, drifted, malformed, runtime-download-enabled, or non-TOON locks. A regression removes one wheel and proves fail-closed behavior. |
| Medium | `install_graph_runtime.py`; wheelhouse-to-pip transition | A writable wheelhouse entry could be replaced after its bytes were hashed and before pip reopened the path. | Installer now hashes bytes once, writes those verified bytes into a private temporary directory, makes them read-only, and installs only staged paths with `--no-index --no-deps`. A disposable real install loaded all twelve grammars. |
| Medium | `code_graph.extract_isolated` | Parser children inherited the complete parent environment, unnecessarily exposing credentials and user import hooks to native grammar processes. | Parser children now receive a minimal allowlisted environment, no user site, no proxy route, and the runtime network-denial marker. A regression proves a parent secret marker is absent. |
| Medium | `ai_sdlc_context._render`; generated context TOON | A single-record table omitted its cardinality and empty fields were emitted as blank CSV cells, so strict TOON decoding rejected a generated context artifact. | Single-record interaction output is now `[1]` and empty fields are explicitly quoted. Repository-wide TOON validation and shared-runtime tests pass. |
| Low | Generated docs inventory | Adding two CLI scripts left the generated catalog and its inventory assertion at the old count. | Regenerated all catalog projections and updated the deterministic expected script count from 118 to 120. |

## Requirements and Design Alignment

- All twelve selected languages, including Kotlin and Swift, share the same
  pinned-parser and completeness contract.
- Safe corpus accounting, AST facts, graph v2 tables, typed bounded relations,
  trace hubs, incremental replacement, query ranking, pack economics, and
  direct-read fallback align with FR-001 through FR-008.
- Stable sorting and fingerprints cover every portable result. Repository files
  remain authoritative and cached content remains `evidence_only`.
- The graph remains local derived SQLite state; all portable machine contracts
  and receipts are TOON.

## Test and Failure-Path Review

The focused suite covers parser preflight, exact lock completeness, native
crash isolation, environment stripping, every language fixture, real parse
failure, missing grammars, stable rebuilds, v1 replacement, trace hubs, bounds,
incremental invalidation, unsafe inputs, golden ranking, qualified-symbol
disambiguation, pack acceptance, and strict fallback. The real-corpus audit
tests two-build determinism and injected parser-gate failure.

## Validation Gaps and Residual Risk

- Local wheel and ABI evidence is limited to CPython 3.11 on macOS arm64;
  declared additional targets require equivalent protected-CI lock smoke.
- The Python socket denial is defense in depth, not an OS sandbox. Integrity is
  primarily established by exact package versions and wheel hashes; host
  sandbox policy remains authoritative for stronger process isolation.
- No unresolved correctness, contract, security, test, or maintainability
  blocker remains for the reviewed target.
