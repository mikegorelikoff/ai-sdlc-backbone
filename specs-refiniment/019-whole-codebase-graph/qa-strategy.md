---
type: "ai-sdlc.qa-strategy"
title: "QA Scope and Strategy"
description: "Risk-based QA scope, layers, data, environments, and suite intent."
tags:
  - "ai-sdlc"
  - "qa"
  - "testing"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:57:03Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "qa-strategy.md"
  path: "specs-refiniment/019-whole-codebase-graph/qa-strategy.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-scope-and-strategy-design"
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
    - "DEC-001"
    - "DEC-005"
    - "DEC-007"
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
    - "specs-refiniment/019-whole-codebase-graph/qa-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/qa.md"
    - "specs-refiniment/019-whole-codebase-graph/release-slicing.md"
    - "specs-refiniment/019-whole-codebase-graph/requirements-readiness.md"
    - "specs-refiniment/019-whole-codebase-graph/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-test-scope-and-strategy-design"
    - "qa-strategy"
    - "approved"
---

# qa-strategy.md

## Feature Summary
- Confirmed facts: The strategy validates a production-gated, offline, optional, deterministic code graph over the whole safe corpus with mandatory Tree-sitter AST coverage for twelve languages including Kotlin and Swift.
- Evidence: delivery-spec.md FR-001 through FR-008; qa-gap-review.md GO verdict.
- Open questions/blockers: No strategy blocker; executable evidence is produced during implementation.

## Actors and Stakeholders
- Confirmed facts: QA owns functional, corpus, recall, economics, and release suites; Engineering owns unit/integration implementation; Security owns dependency, network, secret, and path tests; Harness Maintainers own operational UAT and final acceptance.
- Evidence: qa.md Actors and Stakeholders and Signoff Criteria.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: Test scope covers parser preflight, corpus accounting, AST facts, stable graph identity, bounded typed relations/hubs, schema migration, incremental atomic refresh, query/ranking/packing, TOON diagnostics, offline operation, exclusions, direct-read fallback, and feature 018 compatibility.
- Evidence: AC-001 through AC-008 and qa.md Regression Targets.
- Open questions/blockers: UI, remote services, generative entity extraction, semantic embeddings, and unsupported-language AST semantics are out of scope.

## Workflows and Failure Paths
- Confirmed facts: Coverage follows WF-001 build, WF-002 retrieval, WF-003 incremental mutation, and WF-004 rejection/recovery. Each is exercised through primary, negative, boundary, concurrency, and recovery cases where applicable.
- Evidence: delivery-spec.md Workflow Detail and QA-001 through QA-012.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Every AC, FR, BR, USAC, and success measure maps to at least one planned layer. Critical rules include all-or-explicitly-incomplete AST coverage, bounded growth, byte stability, offline runtime, TOON-only contracts, no authority escalation, and full-gate production claims.
- Evidence: delivery-spec.md Acceptance Traceability; qa-gap-review.md QA Evidence Reviewed.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Tests treat Tree-sitter runtime/grammars and SQLite as local integrations. Non-functional gates are determinism, boundedness, atomicity, offline behavior, confidentiality, and token economics; elapsed latency is observational.
- Evidence: discovery.md non-functional requirements; DEC-005 through DEC-007.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Parser artifacts and supported target environments are prerequisites for install tests; implementation modules are prerequisites for executable graph tests; real-corpus runs require clean derived state and controlled source snapshots.
- Evidence: qa-gap-review.md Testability Gap Matrix.
- Open questions/blockers: Inputs are pending. Owner: Engineering and Security. Impact: execution order begins with RS-0. Resolution: lock artifacts and targets before broader automation.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are binding. No testing waiver, reduced language list, heuristic fallback, or below-threshold accepted pack is permitted.
- Evidence: decision-log.md.
- Open questions/blockers: Exact pins and command paths are pending. Owner: Engineering. Impact: strategy is stable but executable wiring is deferred. Resolution: bind both in implementation SDD.

## Success Measures
- Confirmed facts: Release gates are 100 percent safe-file accounting; successful AST coverage for every selected-language file or graph_complete false; zero stale facts; all graph bounds; 100 percent golden recall; at least 25 percent savings for accepted packs; byte-identical fingerprints and receipts.
- Evidence: SM-001 through SM-007; QA-012.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/business-context.md; specs-refiniment/019-whole-codebase-graph/delivery-spec.md; specs-refiniment/019-whole-codebase-graph/qa.md; specs-refiniment/019-whole-codebase-graph/qa-gap-review.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon; and /Users/mikegorelikov/.agents/skills/ai-sdlc-test-scope-and-strategy-design/references/test-strategy-structures.md.
- Evidence: Full-flow scan and direct inspection of QA scenarios, gap matrix, requirements, workflow, environment, risk, and release sections, including budget-omitted next reads.
- Open questions/blockers: None.

## Test Scope
- Must-test P0: optional parser installation/offline preflight; one minimal and one relationship-rich fixture per language; missing/error grammar behavior; every safe-file status; stable graph schema/IDs/order/fingerprint; bounded relations and trace hubs; atomic full/incremental publication; lexical plus bounded graph retrieval; golden recall and pack economics; deterministic TOON diagnostics; unsafe-input exclusions; default-install and feature 018 regressions.
- P1: operational explainability of stats, verify, and troubleshooting; observational timing and storage profiles on the repository corpus.
- Out of scope: UI/accessibility, remote deployment, remote GraphRAG, embeddings/vector database, compiler-complete type resolution, speculative call edges, AST support beyond the twelve selected languages.

## Risk and Coverage Priorities
| Risk | Likelihood | Impact | Coverage Layer | Priority | Owner |
| --- | --- | --- | --- | --- | --- |
| Grammar/ABI or hidden download failure | Medium | Blocks all semantic indexing or violates offline boundary | install smoke, dependency integrity, parser preflight | P0 | Engineering and Security |
| Per-language semantic mismatch | High | False graph completeness and poor navigation | parameterized parser unit/golden fixture integration | P0 | Engineering and QA |
| Nondeterministic IDs/order/ranking | Medium | Unreproducible cache and token packs | clean double-build and repeated query oracle | P0 | Engineering and QA |
| Graph clique/fan-out explosion | High | Excessive storage/query cost | adversarial graph unit and corpus bounds audit | P0 | Engineering |
| Stale or partial publication | Medium | Agents consume incorrect source facts | mutation, migration, race, corruption integration tests | P0 | Engineering and QA |
| Recall or economics regression | Medium | Missed evidence or no token value | golden E2E query/pack suite | P0 | QA |
| Unsafe input or authority escalation | Low | Secret leakage or unsafe action | security boundary and fallback integration suite | P0 | Security |
| Operational diagnostics ambiguity | Medium | Slow recovery | CLI contract tests and maintainer UAT | P1 | Maintainers and QA |

## Layer and Suite Strategy
| Suite | Intent | Contents | Trigger |
| --- | --- | --- | --- |
| Unit | Prove deterministic pure extraction/policy behavior | language classification, stable IDs, AST query mapping, relation bounds, ranking, TOON encoding | Every change |
| Parser fixture integration | Prove real grammars and cross-file facts | 24 core fixtures plus malformed/missing grammar cases across twelve languages | Parser/adapter changes and CI |
| Storage/incremental integration | Prove schema, atomicity, freshness, migration | full warm, edit/rename/delete, drift, corruption, previous-valid retention | Graph/storage changes and CI |
| Smoke | Smallest launch-critical signal | optional preflight, one 12-language matrix, warm, stats/verify, one query, one accepted and one rejected pack | Every merge/release target |
| Regression | Preserve feature 018 and safety | default install, legacy commands, exclusions, fallback, FTS/document retrieval, concurrency | Every merge |
| Negative/security | Prove fail-closed behavior | secrets, paths, symlinks, network denial, parser failures, bounds, stale/corrupt/timeout | Every security-sensitive change and release |
| UAT | Stakeholder-readable value proof | find definitions/dependencies/tests/specs and compare accepted pack to direct reads | Release candidate |
| Full release | Production verdict | all suites plus two clean real-corpus runs and code/security review | Release candidate only |

## Test Data Strategy
- Maintain deterministic fixture directories per language with minimal syntax and relationship-rich multi-file projects. Expected outcomes are TOON manifests listing definitions, occurrences, imports, containment, provable references, and excluded speculative edges.
- Kotlin fixtures include package/class/object/function/property/import/call relations; Swift fixtures include module-like file scope, type/protocol/extension/function/property/import/call relations. They use the same graph_complete gate as all other languages.
- Add shared adversarial corpora for dense traces/references, ambiguous names, path/spec/test links, unsupported text, malformed sources, source mutations, exclusions, and golden retrieval/packs.
- Golden manifests and machine receipts are TOON only; source bytes and expected stable identifiers are version controlled.

## Environment Dependencies
- Required environments: clean default installation without parser extras; clean optional installation for every declared Python/platform target; network-disabled warm/query; SQLite with FTS5; temporary repository roots; pre-019 and current schema; real repository snapshot.
- Isolation: derived cache under repository policy, no home/global state, fixed fixture bytes, controlled environment inputs, no wall-clock value in fingerprints, and clean cache for determinism runs.
- Pending dependency: declared targets and locked parser artifacts. Owner: Engineering and Security. Impact: install matrix execution cannot start. Resolution: RS-0 evidence precedes all release suites.

## Automation Strategy
- Automate all pass/fail release gates. Use parameterized tests for twelve languages, table-driven relation policies, golden TOON comparisons, isolated temp repositories, monkeypatched/denied network, deterministic source mutation hooks, and two-run byte comparisons.
- Keep manual checks only for graph explainability, diagnostics usability, dependency/license review, and stakeholder comparison of accepted packs; manual review cannot substitute for automated coverage, freshness, bounds, recall, or economics gates.
- CI layering: fast unit/regression on ordinary changes; parser/storage integrations when affected; full offline target matrix and real-corpus audit for release. Every failure emits the related AC/USAC/QA identifier.

## Strategy Risks
- Parser wheels may not exist for every target: stop at RS-0, change packaging without reducing language scope, and rerun security review.
- Tree-sitter CST differences may make cross-language normalization uneven: keep language-specific expected manifests while enforcing shared identity and relation contracts.
- Real-corpus goldens may become brittle: assert semantic anchors, bounds, and fingerprints against controlled snapshots; update only with reviewed source/contract changes.
- Token estimates may drift: use the same deterministic estimator for candidate and direct-read baselines and reject, rather than accept, ambiguous savings.
- Full matrix cost may grow: preserve the P0 smoke subset for feedback, but never omit full release execution.
- No residual risk is accepted silently; owner is QA, impact is withheld production signoff, and resolution is passing the corresponding release gate.
