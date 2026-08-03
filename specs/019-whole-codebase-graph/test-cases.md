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
  at: "2026-08-03T20:13:31Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "test-cases.md"
  path: "specs/019-whole-codebase-graph/test-cases.md"
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
    - "specs/019-whole-codebase-graph/branch-plan.md"
    - "specs/019-whole-codebase-graph/decision-log.md"
    - "specs/019-whole-codebase-graph/design.md"
    - "specs/019-whole-codebase-graph/plan.md"
    - "specs/019-whole-codebase-graph/qa.md"
    - "specs/019-whole-codebase-graph/requirements.md"
    - "specs/019-whole-codebase-graph/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
---

# Test Cases

## Scope
TC-001 through TC-024 cover parser supply chain, all twelve AST languages, whole-corpus accounting, typed identities/relations, deterministic and incremental graph lifecycle, bounds, retrieval, economics, fallback, stats, offline behavior, unsafe inputs, and production gating. Kotlin and Swift are included in every parameterized completeness matrix.

## Scenario Matrix
| ID | Requirement | Scenario | Verifiable outcome |
| --- | --- | --- | --- |
| TC-001 | AC-002, AC-008 | preflight locked bundle on declared targets | package/runtime/hash/ABI and all twelve grammar keys pass offline |
| TC-002 | AC-003 | remove or mismatch parser bundle | graph_complete no; direct_read; no candidate accepted |
| TC-003 | AC-001 | discover mixed safe corpus | every safe file is indexed or has one stable exclusion reason |
| TC-004 | AC-001 | compare discovery, DB, and receipt sets | counts and exact paths reconcile with no duplicates |
| TC-005 | AC-002 | parse one golden fixture per language | expected definitions, occurrences, imports, and provable calls pass for all twelve |
| TC-006 | AC-003 | inject syntax/parser errors | named language fails completeness and no heuristic semantic rows appear |
| TC-007 | AC-002 | run shared language matrix including kotlin and swift | all twelve meet the same AST contract |
| TC-008 | AC-003 | omit each grammar independently | each omission rejects completeness; eleven is never accepted as twelve |
| TC-009 | AC-004 | build clean fixture twice | canonical records, receipts, and fingerprints are byte-identical |
| TC-010 | AC-006 | seed v1 then interrupt v2 candidate | no mixed schema; v2 valid or prior cache intact |
| TC-011 | AC-005 | build dense trace/reference corpus | trace hubs replace cliques and every bound holds |
| TC-012 | AC-005 | set bound below fixture fan-out | graph rejected with named bound and direct_read |
| TC-013 | AC-006 | edit, rename, and delete then incremental warm | affected facts replaced, stale facts absent, unaffected fingerprints stable |
| TC-014 | AC-006 | mutate source before publish | candidate discarded and prior fingerprint retained |
| TC-015 | AC-007 | run golden queries twice | expected path/symbol recall is 1.0 and rank is canonical |
| TC-016 | AC-007 | query duplicate short names | qualified identities disambiguate and traversal remains bounded |
| TC-017 | AC-007 | pack at boundary budgets | anchors retained and savings is at least 0.25 |
| TC-018 | AC-007, AC-008 | remove anchor or lower savings | direct_read with stable missing_anchor or uneconomical reason |
| TC-019 | AC-008 | parameterize stale/corrupt/unsafe/timeout states | canonical TOON fallback and unchanged authority/budget |
| TC-020 | AC-004 | emit graph stats twice | required deterministic fields exist and compare equal |
| TC-021 | AC-008 | audit real corpus twice | all AC/SM gates pass with deterministic evidence |
| TC-022 | AC-008 | inject each release failure | nonzero result and production_ready no |
| TC-023 | AC-008 | install locked wheels then deny network | all targets and twelve grammars operate without network |
| TC-024 | AC-001, AC-008 | discover unsafe and sentinel fixtures | reason present; sentinel absent from DB and receipts |

## Layer Mapping
Unit and policy cover classification, IDs, AST rule interpretation, bounds, ranking, and TOON. Parser integration covers TC-001/002/005/006/007/008/023. Storage and lifecycle cover TC-003/004/009/010/011/012/013/014/020/024. Retrieval/economics cover TC-015 through TC-018. Security and release cover TC-019 and TC-021 through TC-024. Any failed lower layer blocks dependent suites.

## Automation Plan
Create test_context_cache_languages.py, test_context_cache_graph.py, test_context_cache_retrieval.py, fixtures/languages/<language>/ expected TOON manifests, fixtures/graph adversarial and golden packs, install_graph_smoke.py, and release_graph_audit.py. Preserve TC IDs in test names, use temporary repository roots, deny network, run deterministic cases twice, and keep all portable expected/receipt data in TOON.

## Open Gaps
No expected-behavior or manual-only P0 gap remains. Execution is blocked until the locked parser environment, code, fixtures, and target jobs exist. Owner: Engineering, QA, and Security. Impact: production_ready must remain no. Resolution: implement T001 through T009 and execute every gate without waiver.
