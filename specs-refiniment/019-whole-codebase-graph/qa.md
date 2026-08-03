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
  at: "2026-08-03T19:54:02Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "qa.md"
  path: "specs-refiniment/019-whole-codebase-graph/qa.md"
  workspace: "refinement"
  skill: "ai-sdlc-qa"
  flow_mode: "full"
  state_file: "specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/019-whole-codebase-graph/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "BR-001"
    - "BR-010"
    - "DEC-001"
    - "DEC-002"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "SC-001"
    - "SC-021"
    - "US-001"
    - "US-012"
    - "WF-001"
    - "WF-002"
    - "WF-003"
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
    - "specs-refiniment/019-whole-codebase-graph/release-slicing.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
    - "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-qa"
    - "qa"
    - "approved"
---

# qa.md

## Feature Summary
- Confirmed facts: Feature 019 upgrades the optional local context cache into a bounded heterogeneous code graph. It must account for the whole safe repository corpus and produce AST-derived facts for TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift.
- Evidence: discovery.md baseline records 1264 indexed documents, 3040 chunks, and 284243 edges, of which 275048 are trace-ID edges and only 282 are imports; delivery-spec.md defines FR-001 through FR-008.
- Open questions/blockers: Production evidence is pending. Owner: Engineering, QA, and Security. Impact: production signoff is withheld, while implementation may proceed. Resolution: complete RS-0 through RS-4 and attach executable evidence.

## Actors and Stakeholders
- Confirmed facts: AI coding agents and developers consume graph evidence; Harness Maintainers operate warm, verify, query, stats, pack, and purge; Engineering implements parsers and graph behavior; QA owns coverage, determinism, recall, economics, and freshness gates; Security owns parser supply chain and unsafe-input boundaries.
- Evidence: business-context.md Actor and Permission Matrix and user-stories.md US-001 through US-012.
- Open questions/blockers: Supported installation targets are pending. Owner: Engineering and Security. Impact: parser release compatibility cannot be signed off. Resolution: publish and execute the RS-0 target matrix without reducing the twelve-language scope.

## Scope and Boundaries
- Confirmed facts: In scope are safe-file accounting, pinned offline Tree-sitter parsing for twelve languages including Kotlin and Swift, stable file/chunk/symbol/occurrence/hub records, bounded typed relations, incremental atomic refresh, symbol-aware retrieval, deterministic TOON receipts, and direct-read fallback. Unsupported safe text remains searchable as unsupported_ast.
- Evidence: AC-001 through AC-008, FR-001 through FR-008, DEC-002 through DEC-007.
- Open questions/blockers: Binary, ignored, generated, vendor, oversized, symlinked, path-escaping, and secret-like inputs remain excluded; no heuristic may satisfy AST coverage.

## Workflows and Failure Paths
- Confirmed facts: WF-001 validates parsers, discovers and parses the corpus, checks bounds and source freshness, then publishes atomically. WF-002 performs lexical seeding, bounded typed traversal, stable ranking, and pack gates. WF-003 invalidates only affected facts after mutations. WF-004 rejects missing, stale, partial, unsafe, corrupt, timed-out, low-recall, or uneconomical evidence and routes direct_read.
- Evidence: delivery-spec.md Workflow Detail and user-stories.md SC-001 through SC-021.
- Open questions/blockers: None; each failure path has an observable rejection state.

## Requirements and Business Rules
- Confirmed facts: The QA model covers AC-001 through AC-008, FR-001 through FR-008, BR-001 through BR-010, USAC-001 through USAC-024, and SM-001 through SM-007. Graph-complete requires successful AST coverage for every selected-language file; portable machine contracts are TOON only.
- Evidence: discovery.md Acceptance Criteria, business-context.md Business Rule Catalog, delivery-spec.md Acceptance Traceability, and user-stories.md Acceptance Criteria Matrix.
- Open questions/blockers: No rule can be waived by a partial pass or a successful file-only index.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite remains repository-local derived storage; parser artifacts are pinned and preinstalled; warm and query are offline; IDs, ordering, ranking, fingerprints, and receipts are deterministic; direct reads remain authoritative.
- Evidence: discovery.md Data, Integrations, and Non-Functional Requirements; DEC-005; DEC-006; feature 018 runtime behavior.
- Open questions/blockers: Exact runtime and grammar artifacts are pending. Owner: Engineering and Security. Impact: offline and ABI release gates remain unproven. Resolution: record versions, hashes, licenses, supported wheels, and ABI receipt in RS-0.

## Dependencies, Risks, and Constraints
- Confirmed facts: P0 risks are grammar availability or ABI drift, incomplete per-language semantics, parse-error recovery, graph explosion, stale publication, false relations, recall loss, token regression, unsafe ingestion, hidden network access, and default-install regression.
- Evidence: release-slicing.md Release Risks and requirements-readiness.md Required Follow-Up.
- Open questions/blockers: Parser supply-chain and platform evidence is pending. Owner: Engineering and Security. Impact: production release is blocked, but implementation is not. Resolution: pass QA-001 and QA-012 on every declared target.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted. Twelve languages are mandatory, Tree-sitter AST is required, unsupported text is explicit, relations are bounded, runtime is optional and offline, and production acceptance requires full coverage plus at least 25 percent savings for accepted packs.
- Evidence: decision-log.md and all upstream traceability matrices.
- Open questions/blockers: Parser pins remain an implementation decision. Owner: Engineering and Security. Impact: no scope change is allowed and release remains conditional. Resolution: select compatible pinned artifacts in RS-0 and verify them through QA-001.

## Success Measures
- Confirmed facts: Pass requires 100 percent safe-file accounting; all selected-language files successfully covered or graph_complete false; zero stale accepted facts; declared graph bounds; 100 percent golden path/symbol recall; at least 25 percent savings for every accepted pack; and byte-identical graph/receipt fingerprints for identical inputs.
- Evidence: SM-001 through SM-007 and AC-001 through AC-008.
- Open questions/blockers: Latency is observational and excluded from deterministic fingerprints, but bounded runtime and timeout fallback remain tested.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/business-context.md; specs-refiniment/019-whole-codebase-graph/delivery-spec.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; and /Users/mikegorelikov/.agents/skills/ai-sdlc-qa/references/qa-plan-template.md.
- Evidence: Full-flow context scan plus direct inspection of acceptance, story, workflow, rule, risk, and readiness sections, including budget-omitted next-read ranges.
- Open questions/blockers: None.

## Acceptance Scenarios
| ID | Actor | Setup | Action | Expected Result | Evidence | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| QA-001 | Security Engineer | Clean supported target and locked parser artifacts | Install optional module and disable network | Runtime plus all twelve grammars match pins/hashes/licenses, import successfully, and warm performs no download | Automated install/offline smoke | High: supply-chain or ABI failure blocks all AST coverage |
| QA-002 | QA Engineer | One canonical fixture for each of twelve languages, including Kotlin and Swift | Run AST extraction and coverage gate | Expected definitions, occurrences, imports, containment, and only provable references are emitted for every language | Parameterized fixture suite | High: false completeness corrupts retrieval |
| QA-003 | Harness Maintainer | Safe mixed corpus with supported and unsupported text plus excluded inputs | Run discovery and warm twice | Every safe file has one stable status; unsupported text is searchable as unsupported_ast; excluded content is not stored or leaked | Corpus accounting assertions and receipts | High: whole-corpus or confidentiality claim |
| QA-004 | QA Engineer | Missing grammar, ABI mismatch, malformed source beyond policy, and parser error fixtures | Run preflight and warm | graph_complete is false, named deterministic TOON reasons are emitted, and no heuristic substitutes for AST | Negative parser suite | High: unsafe partial acceptance |
| QA-005 | Software Engineer | Identical normalized repository snapshots | Build graph twice from clean derived storage | File, chunk, symbol, occurrence, hub, relation ordering, graph fingerprint, and receipts are byte-identical | Determinism comparison | High: cache reproducibility |
| QA-006 | Software Engineer | Dense repeated trace IDs and high-reference fixture | Build and verify graph | Trace hubs replace cliques; each relation fan-out and total-growth policy holds; breaches reject the candidate | Bound assertions and graph stats | High: graph explosion |
| QA-007 | Harness Maintainer | Warm graph followed by changed, renamed, and deleted sources | Run incremental warm, then mutate source during a separate warm | Only affected facts change, removed facts are absent, concurrent candidate is discarded, and previous valid graph remains | Incremental and race tests | High: stale evidence |
| QA-008 | AI coding agent | Golden symbol/path queries with ambiguous same-name symbols | Query lexical plus typed graph traversal twice | All expected paths and qualified symbols are returned in stable order with bounded explanations | Golden recall suite | High: missed or misleading context |
| QA-009 | AI coding agent | Golden candidate packs with critical anchors and known direct-read token baseline | Compile packs at boundary budgets | Accepted packs retain all critical anchors and save at least 25 percent; failures return direct_read with reason | Economics and budget suite | High: claimed savings may lose evidence |
| QA-010 | Harness Maintainer | Stale, corrupt, partial, unsafe, timed-out, fan-out-breached, and uneconomical states | Run query, pack, stats, and verify | Every rejected state emits deterministic TOON and preserves original StepCard/direct-read authority | Fault-injection suite | High: fallback authority or safety regression |
| QA-011 | Developer | Feature 018 corpus and commands with optional AST dependencies absent | Run default install and legacy cache flows | Default installation stays unchanged; safe direct-read/process fallbacks and existing TOON contracts remain compatible | Regression suite | High: optional feature breaks baseline |
| QA-012 | QA Engineer | Golden fixtures and real repository corpus | Run the complete release suite twice from clean state | AC-001 through AC-008 and SM-001 through SM-007 pass with stable evidence; any failure withholds production-ready verdict | End-to-end release audit | High: final release claim |

## Regression Targets
| Target | Why at risk | Required evidence |
| --- | --- | --- |
| Feature 018 warm/query/pack/stats/verify/purge | Schema and traversal are extended | Existing focused runtime tests plus command smoke |
| Direct-read and process fallback | New graph acceptance could mask rejection | Failure-injection assertions preserve authority and reason |
| Safe discovery exclusions | AST parsing expands file handling | Secret, ignore, binary, size, symlink, and path-escape fixtures |
| TOON-only portable contracts | New policies and receipts add structures | Contract scan rejects non-TOON machine artifacts and unstable ordering |
| Atomic publication and concurrency | Incremental graph adds more derived tables | race, source-drift, and previous-valid-graph tests |
| Default installation | Parser bundle is optional and larger | clean default install smoke without parser dependencies |
| Existing document/FTS retrieval | Symbol graph changes ranking seeds | legacy lexical/path query regression corpus |

## Risk-Based Coverage
| Priority | Risk area | Coverage strategy | Release rule |
| --- | --- | --- | --- |
| P0 | Parser supply chain and offline ABI | locked dependency verification, clean install matrix, imports, network denial | Any missing language blocks release |
| P0 | Twelve-language AST correctness | per-language golden fixtures and negative parse cases | Any selected language failure makes graph_complete false |
| P0 | Freshness and determinism | clean double builds, incremental mutation, concurrent drift | Any fingerprint drift or stale fact blocks release |
| P0 | Graph boundedness | dense adversarial fixtures, hub assertions, total/fan-out gates | Any bound breach rejects graph |
| P0 | Retrieval recall and economics | golden path/symbol queries and token baselines | 100 percent critical recall and >=25 percent savings per accepted pack |
| P0 | Safety and fallback | exclusions, corruption, timeout, unsafe sources, authority checks | Only deterministic TOON rejection and direct_read allowed |
| P1 | Operational diagnostics | repeated stats/verify/query receipts and troubleshooting checks | Required fields and reasons remain stable |

## Test Data and Environment
- Confirmed facts: Test data must include one minimal and one relationship-rich fixture per language; Kotlin and Swift are mandatory peers. Add malformed/error fixtures, cross-file imports/references, duplicate symbol names, dense trace/reference graphs, changed/renamed/deleted files, unsupported safe text, ignored/vendor/generated/binary/oversized/secret-like inputs, symlinks/path escapes, and golden query/pack expectations.
- Environment: clean default install; optional parser install on each supported Python/platform target; network-disabled runtime; temporary repository roots; fresh and pre-feature-019 schema states; real repository corpus.
- Determinism controls: fixed locale/timezone-independent ordering, clean derived cache, stable fixture bytes, repeated runs, and exclusion of elapsed time from fingerprints.
- Open questions/blockers: Target matrix and pinned artifacts are pending. Owner: Engineering and Security. Impact: environment coverage cannot be finalized. Resolution: bind the matrix and artifacts in RS-0 before QA execution.

## Validation Commands
| Command intent | Planned command/evidence | Status |
| --- | --- | --- |
| Focused unit and fixture coverage | Repository test runner targeting context-cache graph, parser, query, and TOON contract tests | Planned: tests not implemented yet |
| Twelve-parser preflight | Optional installer smoke plus parser preflight command under denied network | Planned: pins and command to be created in RS-0 |
| Deterministic full build | Warm/build twice from clean derived storage and byte-compare TOON receipts/fingerprints | Planned |
| Incremental freshness | Mutation suite for edit, rename, delete, and mid-build source drift | Planned |
| Bounds and hubs | Dense graph fixture followed by stats/verify bound assertions | Planned |
| Recall and economics | Golden query/pack benchmark with expected anchors and direct-read token baseline | Planned |
| Existing regression | Current feature 018 focused tests and installation smoke | Planned |
| Full release audit | Project validation, code review, security testing, and two clean end-to-end corpus runs | Planned |
- Open questions/blockers: Executable command paths are pending. Owner: Engineering and QA. Impact: no validation result may be claimed yet. Resolution: bind commands in implementation SDD and record outputs in implementation validation evidence.

## Manual Checks
| Check | Environment | Expected result | Owner | Status |
| --- | --- | --- | --- | --- |
| Inspect one rich graph path for each language | Local fixture corpus | Qualified symbol, occurrence, source range, and typed relation are explainable and source-backed | QA | Planned |
| Inspect Kotlin and Swift parity | Kotlin/Swift fixtures | Same completeness and fallback rules as the other ten languages | QA | Planned |
| Review graph stats and coverage receipt | Real repository | Counts, exclusions, language statuses, bounds, freshness, and fingerprint are understandable TOON | Maintainer and QA | Planned |
| Review fallback diagnostics | Fault-injection corpus | Reason is actionable and direct-read remains authoritative | Maintainer and Security | Planned |
| Review dependency licenses/hashes | Locked optional bundle | All runtime and grammar artifacts are approved and reproducible | Security | Planned |
| Compare accepted pack to direct reads | Golden queries | Critical anchors remain while accepted pack saves >=25 percent | QA and Harness Maintainers | Planned |

## Signoff Criteria
- QA plan status: Approved for implementation; not yet approved for production release.
- Production Ready requires QA-001 through QA-012 to pass, AC-001 through AC-008 and SM-001 through SM-007 to be traceable to executed evidence, all twelve parsers including Kotlin and Swift to pass offline installation and AST fixtures, and repeated clean runs to be deterministic.
- Any parser, corpus accounting, completeness, freshness, bound, recall, economics, safety, TOON-contract, security, code-review, or validation failure withholds the production-ready claim and routes graph consumers to direct_read.
- Required signoff owners: Engineering for implementation evidence, QA for functional and economics gates, Security for dependencies/exclusions/offline behavior, and Harness Maintainers for final acceptance.
- Residual risk: None may be silently accepted; unresolved target-platform or parser evidence remains an explicit release blocker.
