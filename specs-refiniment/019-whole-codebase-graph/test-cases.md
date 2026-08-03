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
  at: "2026-08-03T19:59:24Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "test-cases.md"
  path: "specs-refiniment/019-whole-codebase-graph/test-cases.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-cases"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
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
    - "BR-005"
    - "BR-008"
    - "BR-010"
    - "DEC-001"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "SC-001"
    - "SC-002"
    - "SC-003"
    - "SC-004"
    - "SC-005"
    - "SC-006"
    - "SC-007"
    - "SC-008"
    - "SC-009"
    - "SC-010"
    - "SC-011"
    - "SC-012"
    - "SC-013"
    - "SC-014"
    - "SC-015"
    - "SC-016"
    - "SC-017"
    - "SC-018"
    - "SC-019"
    - "SC-020"
    - "SC-021"
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
    - "WF-001"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/backlog.md"
    - "specs-refiniment/019-whole-codebase-graph/business-context.md"
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-spec.md"
    - "specs-refiniment/019-whole-codebase-graph/discovery.md"
    - "specs-refiniment/019-whole-codebase-graph/goal-capability-map.md"
    - "specs-refiniment/019-whole-codebase-graph/index.md"
    - "specs-refiniment/019-whole-codebase-graph/prfaq.md"
    - "specs-refiniment/019-whole-codebase-graph/qa-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/qa-strategy.md"
    - "specs-refiniment/019-whole-codebase-graph/qa.md"
    - "specs-refiniment/019-whole-codebase-graph/release-slicing.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
    - "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-cases"
    - "test-cases"
    - "approved"
---

# test-cases.md

## Feature Summary
- Confirmed facts: The case set proves whole-safe-corpus accounting and deterministic AST graph behavior for TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift.
- Evidence: USAC-001 through USAC-024 and qa-strategy.md.
- Open questions/blockers: No case-design blocker; implementation and parser artifacts are prerequisites for execution.

## Actors and Stakeholders
- Confirmed facts: Engineering implements automated cases; QA owns expected manifests, recall/economics, and release execution; Security owns supply-chain/offline/exclusion cases; Maintainers own operational acceptance.
- Evidence: qa.md Signoff Criteria.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: Cases cover only the optional local runtime, twelve-language AST facts, local graph/storage/query/pack contracts, safe fallback, and compatibility. They exclude remote services, embeddings, UI, unsupported-language AST, speculative semantic resolution, and performance SLAs.
- Evidence: qa-strategy.md Test Scope.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: TC-001 through TC-024 cover build/preflight, corpus classification, parsing, graph construction, query/pack, incremental refresh, rejection/recovery, security, and release audit.
- Evidence: WF-001 through WF-004; SC-001 through SC-021.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Every USAC has one primary case; every AC and FR has multiple direct cases. No case permits heuristic AST completeness, non-TOON machine output, stale evidence, unbounded traversal, runtime network, or authority escalation.
- Evidence: delivery-spec.md and user-stories.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Oracles use source-backed expected AST facts, TOON receipts, SQLite state, stable hashes, deterministic ordering, bound counters, network denial, and token estimates. Elapsed time is not compared byte-for-byte.
- Evidence: DEC-005 through DEC-007 and qa-strategy.md Test Data Strategy.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Cases execute after parser locks and target matrix exist. All repository mutations occur in temporary roots and all derived cache writes stay repository-bounded.
- Evidence: QA-001, QA-007, QA-012.
- Open questions/blockers: Parser lock is pending. Owner: Engineering and Security. Impact: TC-001, TC-002, and TC-023 cannot execute. Resolution: finish RS-0 before implementation acceptance.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 determine all expected outcomes; no unresolved business behavior remains.
- Evidence: decision-log.md and qa-gap-review.md GO verdict.
- Open questions/blockers: Exact class/test names may be mechanically adjusted during implementation without changing TC IDs, inputs, or expected outcomes.

## Success Measures
- Confirmed facts: TC-003/004 prove accounting; TC-005 through TC-008 prove AST coverage; TC-009/010/013/014/020 prove determinism and freshness; TC-011/012 prove bounds; TC-015 through TC-018 prove recall/economics; TC-019/023/024 prove offline safety; TC-021/022 prove release gating.
- Evidence: SM-001 through SM-007.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/business-context.md; specs-refiniment/019-whole-codebase-graph/delivery-spec.md; specs-refiniment/019-whole-codebase-graph/qa.md; specs-refiniment/019-whole-codebase-graph/qa-gap-review.md; specs-refiniment/019-whole-codebase-graph/qa-strategy.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; skills/ai-sdlc-context-cache/tests/test_context_cache.py; and /Users/mikegorelikov/.agents/skills/ai-sdlc-test-cases/references/test-case-template.md.
- Evidence: Full-flow scan plus direct inspection of requirements, QA matrices, strategy layers, fixture expectations, runtime test conventions, and budget-omitted next reads.
- Open questions/blockers: None.

## Scenario Matrix
| Scenario ID | Requirement Ref | Type | Preconditions | Expected Outcome |
| --- | --- | --- | --- | --- |
| TC-001 | USAC-001; AC-006 | Integration/security | Clean declared target; locked optional artifacts; network denied | All twelve grammars verify pins/hashes/licenses/imports and runtime makes zero downloads |
| TC-002 | USAC-002; AC-003 | Negative integration | One grammar missing or ABI-incompatible | Preflight names language/reason; graph_complete false; direct_read |
| TC-003 | USAC-003; AC-001/004 | Integration | Mixed safe corpus | Every safe file has one stable status and two discovery receipts match |
| TC-004 | USAC-004; AC-008 | Integration | Unsupported safe text | File/chunks remain searchable with unsupported_ast and no semantic claims |
| TC-005 | USAC-005; AC-002 | Parameterized integration | Minimal and rich fixtures for all twelve languages | Expected definitions, occurrences, imports, containment, and provable references match TOON goldens |
| TC-006 | USAC-006; AC-003 | Negative parser | Malformed/error source beyond policy | graph_complete false and heuristic facts do not substitute |
| TC-007 | USAC-007; AC-002/003 | Boundary integration | Twelve-language matrix including Kotlin and Swift | Every language passes the same node/edge completeness contract |
| TC-008 | USAC-008; AC-002 | Negative integration | Remove one grammar from matrix | Suite fails naming that language; no reduced-scope success |
| TC-009 | USAC-009; AC-004 | Determinism integration | Identical normalized snapshots | Graph records, ordering, fingerprint, and receipts are byte-identical |
| TC-010 | USAC-010; AC-004 | Migration integration | Valid feature 018 cache/schema | Warm atomically publishes only current schema or retains prior valid cache |
| TC-011 | USAC-011; AC-005 | Adversarial unit/integration | Dense traces and references | Hubs prevent trace cliques; all fan-out and total bounds hold |
| TC-012 | USAC-012; AC-005/008 | Negative policy | Deliberate bound breach | Candidate rejected; TOON names policy; direct_read |
| TC-013 | USAC-013; AC-004 | State transition integration | Edit, rename, and delete sources | Only affected facts change and zero removed facts remain |
| TC-014 | USAC-014; AC-008 | Concurrency integration | Source mutates during warm | Candidate discarded and previous valid graph remains |
| TC-015 | USAC-015; AC-007 | E2E retrieval | Golden path/symbol queries | 100 percent expected evidence in stable rank order |
| TC-016 | USAC-016; AC-004/005 | Boundary retrieval | Same-name symbols in different scopes/files | Qualified identities remain distinct and traversal explanations are bounded |
| TC-017 | USAC-017; AC-007 | E2E economics | Pack meets anchors and savings | Pack accepted with all anchors and savings >=25 percent |
| TC-018 | USAC-018; AC-008 | Negative economics | Missing anchor or savings <25 percent | Pack rejected with deterministic direct_read reason |
| TC-019 | USAC-019; AC-006/008 | Fault injection/security | Missing/stale/corrupt/unsafe/timeout states | Deterministic TOON reason and unchanged direct-read authority |
| TC-020 | USAC-020; AC-004 | Contract | Healthy graph | Repeated stats expose equal coverage/language/node/edge/bound/fingerprint fields |
| TC-021 | USAC-021; AC-001..008 | Release E2E | Golden and repository corpora | Two full runs pass SM-001 through SM-007 with stable evidence |
| TC-022 | USAC-022; DEC-007 | Negative release | Inject any failed gate | Production-ready verdict withheld |
| TC-023 | USAC-023; AC-006 | Install/security | Each declared offline target | Optional install and twelve-parser preflight succeed with network denied |
| TC-024 | USAC-024; AC-001/008 | Permission/security | Secret, ignored, oversized, binary, symlink, path escape | Input excluded with reason and no content persisted or emitted |

## Detailed Test Cases
| Test ID | Scenario Ref | Steps | Expected Result | Priority | Automation |
| --- | --- | --- | --- | --- | --- |
| TC-001 | SC-001 | Install locked extra; verify lock; deny network; import parsers; warm fixtures | Command exits 0; receipt lists twelve verified parsers and zero runtime downloads | P0 | `python3 skills/ai-sdlc-context-cache/tests/test_context_cache_graph.py ContextCacheGraphTests.test_tc_001_locked_offline_bundle -v` |
| TC-002 | SC-002 | Remove/invalidate one grammar; run preflight and warm | Exit/non-acceptance asserts named parser_abi reason, graph_complete false, direct_read | P0 | same test file, `ContextCacheGraphTests.test_tc_002_rejects_missing_or_incompatible_grammar` |
| TC-003 | SC-003 | Discover mixed corpus twice | Canonical TOON statuses and corpus fingerprint match; accounted total equals eligible total | P0 | same test file, `ContextCacheGraphTests.test_tc_003_accounts_for_every_safe_file` |
| TC-004 | SC-003 | Warm unsupported safe file; query its term | Result contains file/chunk with unsupported_ast and no symbol occurrence | P0 | same test file, `ContextCacheGraphTests.test_tc_004_keeps_unsupported_text_searchable` |
| TC-005 | SC-004 | Parse parameterized minimal/rich fixtures; compare expected manifests | All twelve manifest comparisons pass exactly | P0 | `python3 skills/ai-sdlc-context-cache/tests/test_context_cache_languages.py -v` |
| TC-006 | SC-005 | Parse malformed sources beyond policy | Receipt identifies language/path; graph_complete false; zero heuristic semantic rows | P0 | language test file, `ContextCacheLanguageTests.test_tc_006_parse_errors_fail_completeness` |
| TC-007 | SC-006 | Execute twelve-language expected-node/edge matrix | Twelve named subtests pass including kotlin and swift | P0 | language test file, `ContextCacheLanguageTests.test_tc_007_all_languages_share_completeness_gate` |
| TC-008 | SC-007 | Omit each grammar in turn | Each subtest rejects named language; accepted count never becomes eleven | P0 | language test file, `ContextCacheLanguageTests.test_tc_008_each_missing_grammar_blocks_graph_complete` |
| TC-009 | SC-008 | Clean build twice; dump canonical records/receipts | Byte comparisons and graph fingerprint equality pass | P0 | graph test file, `ContextCacheGraphTests.test_tc_009_clean_builds_are_byte_stable` |
| TC-010 | SC-008 | Seed feature 018 DB; warm; interrupt candidate path | No mixed schema accepted; either new graph valid or prior cache intact | P0 | graph test file, `ContextCacheGraphTests.test_tc_010_schema_upgrade_is_atomic` |
| TC-011 | SC-009 | Build dense trace/reference corpus; inspect relation counts | No pairwise trace clique; every configured bound assertion passes | P0 | graph test file, `ContextCacheGraphTests.test_tc_011_hubs_and_relation_bounds_hold` |
| TC-012 | SC-010 | Configure test bound below fixture fan-out; verify/query | graph accepted false; reason includes breached relation/policy; strategy direct_read | P0 | graph test file, `ContextCacheGraphTests.test_tc_012_bound_breach_rejects_graph` |
| TC-013 | SC-011 | Snapshot graph; edit/rename/delete; incremental warm; diff | Unaffected fingerprints equal; affected facts replaced; deleted IDs absent | P0 | graph test file, `ContextCacheGraphTests.test_tc_013_incremental_refresh_removes_stale_facts` |
| TC-014 | SC-012 | Hook source mutation between build and publish | Candidate absent; prior graph fingerprint unchanged; source_drift reason emitted | P0 | graph test file, `ContextCacheGraphTests.test_tc_014_source_drift_retains_previous_graph` |
| TC-015 | SC-013 | Run every golden query twice | Expected path/symbol set recall equals 1.0 and canonical rank results match | P0 | `python3 skills/ai-sdlc-context-cache/tests/test_context_cache_retrieval.py ContextCacheRetrievalTests.test_tc_015_golden_recall_and_rank -v` |
| TC-016 | SC-014 | Query duplicate short names; traverse references | Results contain distinct qualified IDs and traversal never exceeds bounds | P0 | retrieval test file, `ContextCacheRetrievalTests.test_tc_016_qualified_symbols_disambiguate` |
| TC-017 | SC-015 | Compile accepted golden packs at boundary budgets | Critical anchors subset result and computed savings >=0.25 | P0 | retrieval test file, `ContextCacheRetrievalTests.test_tc_017_accepts_only_economical_complete_pack` |
| TC-018 | SC-016 | Remove anchor then lower baseline savings | Both variants return strategy direct_read with stable named reason | P0 | retrieval test file, `ContextCacheRetrievalTests.test_tc_018_rejects_incomplete_or_uneconomical_pack` |
| TC-019 | SC-017 | Parameterize rejected cache states and fallback calls | Canonical TOON equal across repeats; authority/budget constraints unchanged | P0 | graph test file, `ContextCacheGraphTests.test_tc_019_faults_fail_closed_with_toon` |
| TC-020 | SC-017 | Run stats twice on healthy graph | Required fields exist and canonical deterministic fields compare equal | P0 | graph test file, `ContextCacheGraphTests.test_tc_020_stats_are_complete_and_stable` |
| TC-021 | SC-018 | Execute full suite twice on clean goldens and repository | Both evidence bundles pass AC-001..008/SM-001..007 and deterministic comparison | P0 | `python3 skills/ai-sdlc-context-cache/tests/release_graph_audit.py --root . --runs 2 --format toon` |
| TC-022 | SC-019 | Inject each release-gate failure into audit | Every variant exits nonzero and emits production_ready: no | P0 | release audit `--fault <gate> --format toon` |
| TC-023 | SC-021 | Run clean install/preflight with network denied per target | All declared targets exit 0 with twelve parsers verified | P0 | `python3 skills/ai-sdlc-context-cache/tests/install_graph_smoke.py --lock skills/ai-sdlc-context-cache/references/parser-lock.toon --offline --format toon` |
| TC-024 | SC-020 | Discover each unsafe/excluded fixture; scan DB/receipt | Exclusion reason present; sentinel content absent from DB and output | P0 | graph test file, `ContextCacheGraphTests.test_tc_024_excludes_unsafe_inputs_without_leakage` |

## Permission and Negative Cases
- TC-002/006/008 deny partial parser authority; TC-012 denies over-bound graph authority; TC-014 denies publication after source drift; TC-018 denies lossy/uneconomical packs; TC-019 denies stale/corrupt/unsafe/timed-out cache authority; TC-022 denies production claims after any gate failure; TC-024 denies reading or leaking excluded inputs.
- Fallback is not a permission escalation: all direct reads retain the original StepCard path, instruction, safety, and budget constraints.
- Evidence: BR-005, BR-008 through BR-010; QA-004, QA-010, QA-012.
- Open questions/blockers: None.

## Expected Results
- Pass/fail oracles are exact TOON fields, exit codes, database before/after sets, stable hashes, set recall, fan-out/total counters, and numeric savings.
- AST oracles name symbol kind, qualified identity, definition/reference role, byte/point range, containing file/symbol, and relation type. Speculative references are asserted absent.
- Deterministic comparisons exclude explicitly observational elapsed-time fields and compare canonical portable results byte-for-byte.
- Every failure oracle asserts both the rejection reason and absence of prohibited side effects: no accepted partial graph, no stale rows, no leaked content, no runtime network, and no authority expansion.

## Layer Mapping
1. Unit/policy: run on every graph change; blocks parser/storage integration; failure action: fix deterministic extraction, identity, bounds, ranking, or TOON encoding and rerun.
2. Parser fixture integration: run after parser lock and adapters exist; blocks graph_complete claims; failure action: name failing language, fix grammar/query/manifest, rerun all twelve.
3. Storage/incremental integration: run after schema code; blocks retrieval; failure action: retain prior valid cache, fix migration/freshness/atomicity.
4. Retrieval/economics E2E: run after graph verification; blocks UAT/release; failure action: route direct_read, fix traversal/ranking/packing without weakening anchors.
5. Security/install regression: run on parser, discovery, fallback, or packaging changes; blocks release; failure action: fail closed and require Security review.
6. Full release audit: run twice only after all focused layers pass; blocks production-ready verdict; failure action: emit production_ready: no and attach failed TC/AC.

## Automation Plan
- Implement TC-001 through TC-024 using the exact target files and invocations in Detailed Test Cases; test method names preserve TC IDs.
- Store language sources and expected manifests under skills/ai-sdlc-context-cache/tests/fixtures/languages/<language>/; portable expected manifests use .toon.
- Store adversarial, mutation, retrieval, and pack cases under skills/ai-sdlc-context-cache/tests/fixtures/graph/ with TOON expectations.
- Add install_graph_smoke.py and release_graph_audit.py as deterministic offline/release harnesses whose machine output is TOON only.
- No case is manual-only. Human UAT supplements TC-015/017/020 but cannot satisfy their automated gates.
- Decisions required: none; parser pins and target matrix are implementation outputs governed by DEC-006, not ambiguous expected behavior.
