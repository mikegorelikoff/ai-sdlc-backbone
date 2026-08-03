---
type: "ai-sdlc.delivery-spec"
title: "Delivery Specification"
description: "Structured implementation and cross-functional delivery contract."
tags:
  - "ai-sdlc"
  - "requirements"
  - "delivery"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T19:49:56Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "019-whole-codebase-graph"
  artifact: "delivery-spec.md"
  path: "specs-refiniment/019-whole-codebase-graph/delivery-spec.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-spec-synthesis"
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
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "EPIC-005"
    - "SC-001"
    - "SC-003"
    - "SC-008"
    - "SC-009"
    - "SC-013"
    - "US-001"
    - "US-002"
    - "US-003"
    - "US-004"
    - "US-005"
    - "US-006"
    - "US-007"
    - "US-008"
    - "US-009"
    - "US-010"
    - "US-011"
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
    - "ai-sdlc-delivery-spec-synthesis"
    - "delivery-spec"
    - "approved"
---

# delivery-spec.md

## Feature Summary
- Confirmed facts: Deliver a production-ready optional local graph index over the safe repository corpus, with deterministic Tree-sitter AST facts for twelve languages, bounded typed traversal, token-efficient packing, TOON-only portable contracts, and safe direct-read fallback.
- Evidence: business-context.md, user-stories.md, release-slicing.md.
- Open questions/blockers: None for delivery handoff.

## Actors and Stakeholders
- Confirmed facts: Agent and Developer consume evidence; Maintainer operates it; Engineering implements it; QA and Security independently gate it.
- Evidence: business-context.md Actor and Permission Matrix.
- Open questions/blockers: None.

## Scope and Boundaries
- Confirmed facts: All twelve languages, whole safe-file accounting, graph storage, incremental refresh, query/pack, diagnostics, fixtures, installer, docs, security, and benchmarks are in MVP. Remote/LLM/embedding extraction and runtime grammar download are out.
- Evidence: DEC-002 through DEC-006.
- Open questions/blockers: None.

## Workflows and Failure Paths
- Confirmed facts: WF-001 atomic warm, WF-002 retrieval/pack, WF-003 incremental refresh, and WF-004 reject/fallback cover the end-to-end lifecycle.
- Evidence: business-context.md Workflow Detail.
- Open questions/blockers: None.

## Requirements and Business Rules
- Confirmed facts: Eight functional requirements and ten business rules below are binding and traceable to stories and acceptance.
- Evidence: business-context.md and user-stories.md.
- Open questions/blockers: None.

## Data, Integrations, and Non-Functional Requirements
- Confirmed facts: SQLite stores derived file, chunk, symbol, occurrence, and typed relation state plus FTS. Tree-sitter provides ASTs from preinstalled pinned grammars. StepCard/query constraints govern retrieval. Portable structured artifacts are TOON; runtime stays offline; output is deterministic and bounded.
- Evidence: DEC-003 through DEC-006.
- Open questions/blockers: Exact schema and parser APIs belong to implementation SDD while preserving these contracts.

## Dependencies, Risks, and Constraints
- Confirmed facts: Feature 018, supported Python/SQLite, Tree-sitter runtime, twelve grammars, TOON codec, StepCard contracts, and optional installer are dependencies. Release risks and early warnings are explicit in release-slicing.md.
- Evidence: RS-0 through RS-4.
- Open questions/blockers: Parser bundle proof blocks release, not design.

## Decisions, Assumptions, and Open Questions
- Confirmed facts: DEC-001 through DEC-007 are accepted. No unresolved product or delivery decision remains.
- Evidence: decision-log.md.
- Open questions/blockers: Engineering must record exact parser/schema choices in the implementation decision log.

## Success Measures
- Confirmed facts: SM-001 through SM-007 and AC-001 through AC-008 are the production success gates.
- Evidence: discovery.md and user-stories.md.
- Open questions/blockers: None.

## Source Coverage
- Confirmed facts: Consumed specs-refiniment/019-whole-codebase-graph/business-context.md; specs-refiniment/019-whole-codebase-graph/user-stories.md; specs-refiniment/019-whole-codebase-graph/release-slicing.md; specs-refiniment/019-whole-codebase-graph/backlog.md; specs-refiniment/019-whole-codebase-graph/decision-log.md; specs-refiniment/019-whole-codebase-graph/discovery.md; specs-refiniment/019-whole-codebase-graph/prfaq.md; specs-refiniment/019-whole-codebase-graph/delivery-gap-review.md; specs-refiniment/019-whole-codebase-graph/requirements-readiness.md; specs-refiniment/019-whole-codebase-graph/goal-capability-map.md; specs-refiniment/019-whole-codebase-graph/backlog-gap-review.md; specs-refiniment/019-whole-codebase-graph/index.md; specs-refiniment/019-whole-codebase-graph/_ai_sdlc/state.toon. Budget-omitted next_reads were inspected in their named sections.
- Evidence: Full-flow delivery scan fingerprint 1829afd3dbf0c64fb889d01f0fb2376384f9cfee14e580284b97c01dcde5c0c8.
- Open questions/blockers: None.

## Requirement Detail
| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref |
| --- | --- | --- | --- | --- | --- |
| FR-001 | Discovery/warm | Account for every safe eligible file as a file node or explicit exclusion | US-002 | P0 | AC-001; USAC-003; USAC-004 |
| FR-002 | Parser subsystem | Parse TypeScript, Python, JavaScript, Java, C#, PHP, Shell, C++, Go, Rust, Kotlin, and Swift through pinned Tree-sitter grammars | US-001; US-003; US-004 | P0 | AC-002; AC-003 |
| FR-003 | Graph builder | Create stable file, chunk, symbol, occurrence, and hub identities | US-005 | P0 | AC-004 |
| FR-004 | Graph builder | Create typed contains, defines, references, imports, provable calls, path-reference, test-target, spec-trace, and adjacent relations | US-003; US-005 | P0 | AC-002; AC-004 |
| FR-005 | Graph policy | Bound per-relation fan-out and total growth; replace trace cliques with hubs | US-006 | P0 | AC-005 |
| FR-006 | Operations | Expose deterministic TOON coverage, parser, graph, freshness, bounds, and fingerprint diagnostics | US-010 | P0 | AC-004; AC-006; AC-008 |
| FR-007 | Query/pack | Combine lexical seeds with bounded typed traversal and deterministic budgeted packing | US-008; US-009 | P0 | AC-007 |
| FR-008 | Runtime | Preserve direct-read authority and reject missing, stale, partial, unsafe, corrupt, uneconomical, or timed-out graph evidence | US-007; US-010; US-012 | P0 | AC-006; AC-008 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Requirement Ref |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | warm/build | Maintainer | discover; classify; parser preflight; AST extract; graph build; bounds check; source recheck; atomic publish | fresh graph | parser/AST/source/bounds/integrity failure retains valid graph or direct_read | FR-001 through FR-006 |
| WF-002 | query/pack | Agent or Developer | FTS seeds; typed bounded expansion; stable rank; critical recall and economics gate | evidence or accepted pack | stale/corrupt/timeout/recall/savings failure returns direct_read | FR-006 through FR-008 |
| WF-003 | source mutation | Maintainer | compare fingerprints; reparse affected files; invalidate facts; rebuild affected relations; atomic publish | fresh incremental graph | concurrent drift discards candidate | FR-003 through FR-006 |
| WF-004 | acceptance failure | Runtime | classify reason; emit TOON receipt; reject cache; retain authority; route direct_read | safe recovery | never accepts partial completeness | FR-006; FR-008 |

## Business Rule Detail
| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-001 | Every safe file is accounted | discovery | business-context.md | graph incomplete | DEC-004 |
| BR-002 | Selected-language AST is mandatory | warm | business-context.md | graph_complete false | DEC-003 |
| BR-003 | Semantic outputs are deterministic | all operations | business-context.md | verification fail | DEC-005 |
| BR-004 | Relations and total graph are bounded | graph/query | business-context.md | reject/direct_read | DEC-005 |
| BR-005 | Stale, partial, unsafe, or corrupt evidence is not accepted | publish/query | business-context.md | retain valid graph/direct_read | DEC-004 |
| BR-006 | Runtime is offline | install/warm/query | business-context.md | parser preflight fail | DEC-006 |
| BR-007 | Portable machine contracts are TOON only | policy/results/receipts | business-context.md | contract fail | DEC-006 |
| BR-008 | Heuristics never claim AST completeness | extraction | business-context.md | explicit unsupported/error | DEC-003 |
| BR-009 | Fallback grants no extra authority | runtime | business-context.md | original StepCard/direct-read constraints remain | DEC-004 |
| BR-010 | Production claims require every release gate | release | business-context.md | withhold verdict | DEC-007 |

## User Story Traceability
- EPIC-001 / FR-001–FR-002: US-001 through US-004.
- EPIC-002 / FR-003–FR-005: US-005 through US-007.
- EPIC-003 / FR-007: US-008 and US-009.
- EPIC-004 / FR-006 and FR-008: US-010.
- EPIC-005 / all requirements: US-011 and US-012.
- No story or requirement is orphaned; all are P0/MVP.

## Acceptance Traceability
- AC-001 maps to FR-001, US-002, USAC-003/004, SC-003.
- AC-002/003 map to FR-002/004, US-001/003/004, USAC-001/002/005–008, SC-001/002/004–007.
- AC-004 maps to FR-003/004/006, US-005/007/010, USAC-009/010/013/014/020, SC-008/011/012/017.
- AC-005 maps to FR-005, US-006, USAC-011/012, SC-009/010.
- AC-006 maps to FR-002/006/008, US-001/010/012, USAC-001/002/019/023, SC-001/002/017/021.
- AC-007 maps to FR-007, US-008/009/011, USAC-015–018/021, SC-013–016/018.
- AC-008 maps to FR-001/006/008, US-002/007/009/010/012, negative and permission scenarios.

## QA and Operational Notes
- QA must parameterize AST coverage across all twelve languages and run deterministic builds twice.
- Real-corpus verification must measure safe-file accounting, language coverage, node/edge distribution, fan-out, freshness, recall, and token economics.
- Operators require build, incremental warm, query, pack, stats, verify, and purge flows with TOON receipts.
- Optional install must keep the default installation unchanged and validate hashes, licenses, ABI, offline behavior, and supported targets.
- Direct reads remain the documented recovery for every rejected cache state.

## Handoff Risks
- Confirmed facts: The delivery package is ready for QA and implementation SDD. Remaining risks are executable: parser packaging/ABI, per-language extraction correctness, stable schema migration, bounded graph construction, incremental invalidation, recall/economics, and source/dependency security.
- Evidence: Release Risks and USAC-001 through USAC-024.
- Open questions/blockers: No specification blocker. Production-ready status requires implementation, QA, security, code review, and validation evidence.
