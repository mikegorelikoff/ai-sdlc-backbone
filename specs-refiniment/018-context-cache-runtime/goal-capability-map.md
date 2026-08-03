---
type: "ai-sdlc.goal-capability-map"
title: "Goal, Capability, and Epic Map"
description: "Business goals mapped to roles, capabilities, and outcome-oriented epics."
tags:
  - "ai-sdlc"
  - "planning"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T11:44:52Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "goal-capability-map.md"
  path: "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
  workspace: "refinement"
  skill: "ai-sdlc-goal-capability-and-epic-mapping"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
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
    - "AC-008"
    - "BR-001"
    - "BR-006"
    - "CAP-001"
    - "CAP-002"
    - "CAP-003"
    - "CAP-004"
    - "DEC-001"
    - "DEC-002"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-002"
    - "EPIC-003"
    - "EPIC-004"
    - "GOAL-001"
    - "GOAL-002"
    - "GOAL-003"
    - "GOAL-004"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-goal-capability-and-epic-mapping"
    - "goal-capability-map"
    - "approved"
---

# goal-capability-map.md

## Feature Summary
Feature 018 turns the installed local cache from a manual utility into an automatic, bounded StepCard capability while preserving direct-read authority. Evidence: discovery, requirements readiness 9/10, and DEC-002 through DEC-007. No planning blocker remains.

## Actors and Stakeholders
Contributors and agents need transparent safe reuse; maintainers need supportable contracts; repository owners need policy control; QA and Security need deterministic and privacy evidence. Evidence: discovery Actors and Stakeholders. No actor gap remains.

## Scope and Boundaries
The plan covers runtime activation, safe warming, policy/budget enforcement, validated packs, aggregate observation, recovery, docs, and evidence. Daemons, remote retrieval, embeddings, full GraphRAG, and network telemetry are excluded by DEC-006.

## Workflows and Failure Paths
Normal selection resolves policy, coordinates warming, validates a fresh pack, records an aggregate outcome, and returns it. Every absence, timeout, contention, drift, corruption, invalidity, or poor-economics path returns reason-coded direct reads. Evidence: AC-001 through AC-008.

## Requirements and Business Rules
BR-001 through BR-006 and FR-001 through FR-008 map to four delivery capabilities: transparent reuse, safe lifecycle, bounded governance, and operational assurance. Repository evidence and owning steps remain authoritative; the cache is never a permission or availability prerequisite.

## Data, Integrations, and Non-Functional Requirements
The system uses project-local rollback-journal SQLite, a separate control database, TOON policy and receipts, a bounded process boundary, and context-pack/v4. Determinism, confinement, offline operation, atomicity, crash recovery, privacy, and default parity are non-negotiable.

## Dependencies, Risks, and Constraints
Feature 017 at ef67851, Python, SQLite/FTS5, shared runtime, codec, v4, and manifests are required. Concurrency, source drift, corruption, policy drift, token regression, privacy, recursion, and timeout risks have explicit mitigation and direct-read recovery.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 are accepted. Owner: Product and Architecture. Impact: future WAL, embeddings, GraphRAG, and exporters are separate roadmap choices. Next step: deliver only the bounded local runtime integration; no open MVP question remains.

## Success Measures
Goals are satisfied only with complete anchor recall, zero stale accepted packs, concurrent convergence, direct-read parity, manifest-budget compliance, observation allowlisting, deterministic receipts, and unchanged default installation. Token totals and cache/fallback counts measure operational value.

## Source Coverage
Consumed: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md; specs/017-local-context-cache/requirements.md; specs/017-local-context-cache/design.md; specs/017-local-context-cache/validation.md; skills/ai-sdlc-context-cache/scripts/context_cache.py; skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_step_context.py; skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py. Coverage includes customer, scope, requirements, acceptance, architecture, baseline, risk, and delivery readiness.

## Business Goals
| Goal ID | Goal | Metric | Target | Owner | Source |
| --- | --- | --- | --- | --- | --- |
| GOAL-001 | Make optional cache value automatic in normal skill execution | installed-module StepCards using a valid cache pack or explicit fallback | 100% bounded outcomes | Product | BR-001, AC-001 |
| GOAL-002 | Reduce repeated context tokens without correctness loss | mandatory-anchor recall and eligible pack savings | 100% recall; at least configured 15% savings | Product, QA | AC-004 |
| GOAL-003 | Make local cache operation production-safe | stale/partial accepts and concurrent divergence | zero | Architecture, QA | AC-002, AC-006 |
| GOAL-004 | Keep governance and privacy auditable | budget violations and forbidden observation fields | zero | Security | AC-003, AC-005, AC-008 |

## Role Matrix
| Actor | Role | Need | Permission Boundary | Source |
| --- | --- | --- | --- | --- |
| Contributor or AI agent | Consumer | automatic fresh bounded context | existing repository read and project-local derived write only | AC-001, AC-008 |
| Harness maintainer | Operator | inspect, reset, diagnose, and evolve contracts | no remote service or wider evidence authority | DEC-005, DEC-006 |
| Repository maintainer | Policy owner | exact per-skill and step control | strict documented TOON fields clamped to manifest | DEC-004 |
| QA reviewer | Evidence owner | deterministic concurrency, fault, and economics proof | observational latency separated from goldens | DEC-007 |
| Security reviewer | Boundary owner | confinement and data minimization | aggregate allowlist; no raw payloads | DEC-005 |

## Capability Map
| Capability ID | Capability | Goal Ref | Actors | Dependencies |
| --- | --- | --- | --- | --- |
| CAP-001 | Transparent cache-aware StepCard compilation | GOAL-001, GOAL-002 | contributor, agent | optional module detection, shared runtime |
| CAP-002 | Concurrency-safe fresh cache lifecycle | GOAL-003 | maintainer, agent | control DB, atomic build, source verification |
| CAP-003 | Step-level policy and token governance | GOAL-002, GOAL-004 | repository maintainer, security | TOON codec, manifests, v4 validator |
| CAP-004 | Privacy-safe operations and recovery | GOAL-003, GOAL-004 | maintainer, QA, security | aggregate schema, reason catalog, direct compiler |

## Epic Map
### Epics

| Epic ID | Epic | Capability Ref | Outcome | Priority | Risks |
| --- | --- | --- | --- | --- | --- |
| EPIC-001 | Automatic context reuse | CAP-001 | normal StepCard path uses a valid economical pack when available and preserves absent-module parity | P0 | hidden behavior drift |
| EPIC-002 | Safe cache lifecycle | CAP-002 | concurrent and interrupted warmers never publish stale or partial state | P0 | contention, source drift, SQLite variation |
| EPIC-003 | Deterministic context governance | CAP-003 | exact TOON policy and manifest clamp preserve authority, anchors, and budgets | P0 | policy drift, token regression |
| EPIC-004 | Operational trust | CAP-004 | operators can diagnose aggregate outcomes and every fault recovers to direct reads | P1 | privacy leakage, cardinality, timeout |

## Outcome Traceability
| Goal ID | Capability IDs | Epic IDs | Coverage | Notes |
| --- | --- | --- | --- | --- |
| GOAL-001 | CAP-001 | EPIC-001 | Covered | activation and fallback parity |
| GOAL-002 | CAP-001, CAP-003 | EPIC-001, EPIC-003 | Covered | anchor recall and token economics |
| GOAL-003 | CAP-002, CAP-004 | EPIC-002, EPIC-004 | Covered | lifecycle, recovery, diagnosis |
| GOAL-004 | CAP-003, CAP-004 | EPIC-003, EPIC-004 | Covered | policy, budget, confinement, privacy |

Every goal has capability and epic coverage; every capability maps to a measurable goal; no miscellaneous epic exists.
