---
type: "ai-sdlc.business-context"
title: "Business Context"
description: "Actors, workflows, rules, exceptions, and acceptance context."
tags:
  - "ai-sdlc"
  - "analysis"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:48:07Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "business-context.md"
  path: "specs-refiniment/019-whole-codebase-graph/business-context.md"
  workspace: "refinement"
  skill: "ai-sdlc-ba"
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
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "BR-007"
    - "BR-008"
    - "BR-009"
    - "BR-010"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "SC-001"
    - "SC-021"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md"
    - "specs-refiniment/019-whole-codebase-graph/backlog.md"
    - "specs-refiniment/019-whole-codebase-graph/decision-log.md"
    - "specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md"
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
    - "ai-sdlc-ba"
    - "business-context"
    - "approved"
---

# business-context.md

## Feature Summary
- Confirmed facts: Feature 019 upgrades the optional local context cache into a deterministic whole-codebase graph with Tree-sitter AST intelligence for twelve languages, bounded traversal, token-efficient packs, and safe direct-read fallback.
- Evidence: discovery.md, backlog.md, user-stories.md, release-slicing.md.
- Open questions/blockers: None.

## Actors and Stakeholders
- Confirmed facts: AI agents and developers consume evidence; maintainers operate the cache; Engineering implements parsers and graph; QA gates coverage and economics; Security gates source and dependency boundaries.
- Evidence: goal-capability-map.md.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: The selected languages are TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift. Other safe text remains lexical evidence with unsupported_ast. Runtime downloads, remote services, LLM extraction, and heuristic AST-complete claims are excluded.
- Evidence: DEC-002 through DEC-004.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: Four workflows govern atomic warm, symbol-aware query/pack, incremental refresh, and rejection/direct-read recovery.
- Evidence: WF-001 through WF-004 and SC-001 through SC-021.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: FR-001 through FR-008, BR-001 through BR-007, AC-001 through AC-008, and USAC-001 through USAC-024 form the requirements contract.
- Evidence: discovery.md and user-stories.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: Inputs are safe repository files and StepCard/query constraints. Derived storage is local SQLite. Portable policies, coverage, stats, query, pack, benchmark, and failure receipts are TOON. Identical inputs yield byte-stable identities, ordering, rank, and fingerprints.
- Evidence: DEC-005 and DEC-006.
- Open questions/blockers: None.

## Dependencies, Risks, and Constraints
- Confirmed facts: Feature 018 is the base; a pinned twelve-grammar Tree-sitter bundle is required. Parser ABI drift, incomplete AST, graph explosion, stale publication, false relations, unsafe ingestion, and token regression have release gates.
- Evidence: release-slicing.md Release Risks.
- Open questions/blockers: No business blocker; evidence is required before release.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted. There is no business assumption about reducing language scope or allowing hidden fallback.
- Evidence: decision-log.md.
- Open questions/blockers: Exact pins are an engineering decision constrained by objective install/security evidence.

## Success Measures
- Confirmed facts: Complete safe-file and AST accounting, zero stale accepted nodes, bounded graph size, full golden recall, >=25 percent accepted-pack savings, and deterministic fingerprints are mandatory.
- Evidence: SM-001 through SM-007.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon. Budget-omitted next_reads were inspected directly in their owning sections.
- Evidence: Full-flow BA scan fingerprint 49c7c305ffbc90de585cc14d58a58bc06d5aebf51d2ba58d126524d8abcb129b.
- Open questions/blockers: None.

## Current Behavior
- Confirmed facts: The cache discovers most safe text and provides deterministic chunks, FTS5 search, same-document adjacency, imports, trace IDs, and literal path references. It has no explicit file/symbol/occurrence graph and trace-ID clique edges dominate.
- Evidence: Baseline: 1264 documents, 3040 chunks, 284243 edges, 282 imports, and 275048 trace-ID edges.
- Open questions/blockers: None.

## Desired Behavior
- Confirmed facts: Warm accounts for every safe file, parses every selected-language file with pinned Tree-sitter, extracts stable facts, enforces bounds, rechecks sources, and atomically publishes. Query combines lexical seeds with typed graph traversal and packs only when recall and savings gates pass. Any invalid state produces deterministic TOON diagnostics and direct_read.
- Evidence: WF-001 through WF-004.
- Open questions/blockers: None.

## Actor and Permission Matrix
| Actor | Role | Permissions | Restrictions | Source |
| --- | --- | --- | --- | --- |
| AI coding agent | Retrieval consumer | Query graph and request context pack | Cache is advisory; cannot override instructions, safety, budget, or direct-read authority | AC-008 |
| Developer | Navigation consumer | Run local query, stats, verify, and inspect | Read-only evidence consumer unless explicitly operating warm/purge | PRFAQ |
| Harness Maintainer | Operator | Install optional module; warm, verify, inspect, purge derived cache | May mutate only repository-bounded derived cache; no implicit network | DEC-006 |
| Software Engineer | Implementer | Change schema, parser adapters, graph and query code in task scope | Must preserve all twelve languages and TOON contracts | DEC-002; DEC-003 |
| QA Engineer | Gate owner | Execute fixtures, corpus suites, and economics checks | Cannot waive coverage, bounds, freshness, or recall | DEC-007 |
| Security Engineer | Boundary owner | Review dependencies, exclusions, offline behavior, and unsafe paths | Blocks unverified parser bundle or unsafe ingestion | DEC-004; DEC-006 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | Build or warm request | Maintainer | Discover; classify; parse; extract; bound; recheck; atomically publish | Fresh graph or retained previous graph | Missing grammar, parse failure, drift, unsafe source, bound breach | discovery.md |
| WF-002 | Query or pack request | Agent or Developer | Lexical seed; typed bounded traversal; stable ranking; budget/recall gate | Evidence or accepted pack | Stale/corrupt graph, insufficient recall/savings, timeout | discovery.md |
| WF-003 | Source change | Maintainer | Diff fingerprints; reparse affected files; invalidate facts; rebuild affected relations; publish | No stale accepted facts | Concurrent mutation discards candidate | discovery.md |
| WF-004 | Any acceptance failure | Runtime | Emit deterministic TOON reason; reject graph evidence; route direct_read | Safe authoritative read path | No silent partial acceptance | discovery.md |

## Business Rule Catalog
| Rule ID | Rule | Applies To | Failure Behavior | Source | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-001 | Every safe eligible file is a file node or explicit exclusion | Discovery/warm | Graph incomplete | prfaq.md | DEC-004 |
| BR-002 | Every selected-language file requires successful Tree-sitter AST | Warm/coverage | graph_complete false | prfaq.md | DEC-003 |
| BR-003 | IDs, ordering, ranking, and fingerprints are deterministic | All operations | Verification failure | prfaq.md | DEC-005 |
| BR-004 | Relation fan-out and total graph growth are bounded | Edge construction/query | Reject candidate and direct_read | prfaq.md | DEC-005 |
| BR-005 | Stale, partial, unsafe, or corrupt graph evidence is never accepted | Warm/query | Retain valid graph or direct_read | prfaq.md | DEC-004 |
| BR-006 | Runtime performs no network call or grammar download | Install/warm/query | Fail parser preflight | prfaq.md | DEC-006 |
| BR-007 | Portable machine contracts use TOON only | Policies/receipts/results | Contract validation fails | prfaq.md | DEC-006 |
| BR-008 | No heuristic may claim AST completeness | Extraction/coverage | Explicit unsupported or parse failure status | discovery.md | DEC-003 |
| BR-009 | Failure cannot grant broader authority | Fallback | Direct reads under original StepCard constraints | user-stories.md | DEC-004 |
| BR-010 | Production claims require all release gates | Release | Withhold production-ready verdict | release-slicing.md | DEC-007 |

## Acceptance Criteria
| AC ID | Given | When | Then | Rule Ref | Source |
| --- | --- | --- | --- | --- | --- |
| AC-001 | Safe repository | Warm runs | Every file is accounted for deterministically | BR-001 | discovery.md |
| AC-002 | Twelve language fixtures | Parser suite runs | All expected AST facts pass, including Kotlin and Swift | BR-002 | user-stories.md |
| AC-003 | Missing grammar or invalid AST | Coverage evaluates | graph_complete is false; no heuristic substitution | BR-002; BR-008 | discovery.md |
| AC-004 | Identical sources or changed/deleted sources | Full or incremental warm runs | Stable fingerprints match and stale facts are zero | BR-003; BR-005 | discovery.md |
| AC-005 | Dense trace/reference corpus | Graph builds | Hubs and relation bounds hold | BR-004 | discovery.md |
| AC-006 | Runtime and supported install targets | Parser preflight/warm/query runs | No network occurs; parser bundle is verified | BR-006 | user-stories.md |
| AC-007 | Golden query and pack corpus | Retrieval runs | Expected path/symbol recall is 100 percent and accepted savings >=25 percent | BR-003 | discovery.md |
| AC-008 | Unsupported, stale, corrupt, unsafe, or uneconomical state | Consumer requests evidence | Deterministic TOON reason and direct_read preserve authority | BR-005; BR-007; BR-009 | discovery.md |

## Business Context Gaps
- Confirmed facts: No actor, business outcome, permission, data ownership, workflow, exception, scope, metric, or release-rule gap remains.
- Evidence: Requirements readiness 9/10, backlog/story readiness, release slicing, and the matrices above.
- Open questions/blockers: Implementation must produce parser pin/ABI, fixture, benchmark, security, and validation evidence. Those are delivery gates, not missing business context.
