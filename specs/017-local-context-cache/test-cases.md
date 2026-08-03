---
type: "ai-sdlc.test-cases"
title: "Test Cases"
description: "Test scenarios, expected outcomes, and coverage mapping."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T09:43:20Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "017-local-context-cache"
  artifact: "test-cases.md"
  path: "specs/017-local-context-cache/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/017-local-context-cache/_ai_sdlc/state.toon"
  decision_log: "specs/017-local-context-cache/decision-log.md"
  status: "approved"
  owner: "QA and Harness Maintainers"
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
  related_artifacts:
    - "specs/017-local-context-cache/decision-log.md"
    - "specs/017-local-context-cache/design.md"
    - "specs/017-local-context-cache/index.md"
    - "specs/017-local-context-cache/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
    - "context-cache"
---

# Test Cases

## Scope
Validate deterministic ingestion and retrieval, bounded graph-enhanced expansion, context-pack/v4 compatibility, freshness and security fail-closed behavior, TOON-only interfaces, purge confinement, optional module installation, and repository-wide regression safety.

## Scenario Matrix
| ID | Requirement | Scenario | Verifiable outcome |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Rebuild unchanged fixture twice | Logical fingerprints and TOON receipts are byte-identical. |
| TC-002 | AC-002 | Modify and delete indexed files | Only changed documents are replaced and deleted chunks or edges disappear. |
| TC-003 | AC-003 | Repeat lexical query with tied candidates | Scores and stable path-line ordering match exactly. |
| TC-004 | AC-004 | Query relation-rich fixture with bounded graph expansion | Only allowed typed edges within depth and node limits appear in stable order. |
| TC-005 | AC-005 | Pack query results under small and normal budgets | Packed output validates as context-pack/v4 or explicitly falls back to direct reads. |
| TC-006 | AC-006 | Add a new eligible file or remove, alter, or corrupt cache state | Verify and pack report an explained fallback and never sufficient stale or incomplete evidence. |
| TC-007 | AC-007 | Add symlink, binary, oversized, secret-named, credential-like, and generated files | Every unsafe source is excluded before storage. |
| TC-008 | AC-008 | Put instruction-shaped commands inside indexed content and query text | They remain evidence-only and no command or external action executes. |
| TC-009 | AC-009 | Exercise every CLI and scan emitted artifacts | Stdout decodes as TOON and no alternate machine format mode or artifact exists. |
| TC-010 | AC-010 | Install default and context-cache module profiles twice | Default set is unchanged; opt-in set adds cache skill and shared dependency deterministically. |
| TC-011 | AC-011 | Purge default, absent, unsafe, and custom cache paths | Only validated cache files inside the repository are removed; sources remain intact. |
| TC-012 | AC-012 | Run focused and repository gates | All tests, schemas, docs, security, compatibility, and install checks pass. |
| TC-013 | AC-013 | Run TOON golden cases twice across lexical, graph-enhanced, and pack modes | Required path and anchor recall is 100 percent, declared strategy matches, packed savings is at least 15 percent, and receipts are byte-identical. |

## Layer Mapping
- Unit: safe paths, chunking, relation extraction, scoring, traversal, fingerprints, config bounds, and receipt validation.
- Service: SQLite transactions, FTS queries, incremental update, freshness verification, pack assembly, and purge.
- Integration: installed project execution, default versus opt-in inventory, shared context-pack validator, and interrupted or corrupt cache recovery.
- Release: generated docs, TOON-only scan, complete per-skill suite, native install smoke, and strict docs build.

## Automation Plan
Use temporary Git repositories with fixed text fixtures and no network. Compare canonical TOON bytes, inspect SQLite semantic rows, mutate sources between operations, inject invalid databases and paths, validate packs through `validate_step_context_pack`, execute TOON golden cases twice, and execute installer selections against isolated consumer repositories.

## Open Gaps
Optional semantic embeddings remain unimplemented and unclaimed. The initial release measures lexical and graph retrieval only; future adapters require a new accepted contract and benchmark evidence.
