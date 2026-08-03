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
  at: "2026-08-03T12:19:13Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "delivery-spec.md"
  path: "specs-refiniment/018-context-cache-runtime/delivery-spec.md"
  workspace: "refinement"
  skill: "ai-sdlc-delivery-spec-synthesis"
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
    - "AC-007"
    - "AC-008"
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "DEC-001"
    - "DEC-002"
    - "DEC-004"
    - "DEC-005"
    - "DEC-007"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/backlog-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/backlog.md"
    - "specs-refiniment/018-context-cache-runtime/business-context.md"
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/release-slicing.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
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
Feature 018 delivers a governed read-through context cache at the existing StepCard compilation boundary. The optional module warms fresh project evidence, enforces exact policy and manifest ceilings, accepts only valid economical context-pack/v4 output, records aggregate outcomes, and falls back to authoritative direct reads. The delivery contract spans STORY-001 through STORY-008 and AC-001 through AC-008 with no unresolved scope blocker.

## Actors and Stakeholders
Contributors and AI agents consume StepCards; Harness maintainers implement and support runtime integration; repository maintainers own strict project policy; QA owns deterministic, concurrency, recovery, compatibility, and economics evidence; Security owns confinement and privacy approval. Product and Architecture own deferred scope decisions. No remote operator, embedding provider, or external analytics system participates.

## Scope and Boundaries
The release includes optional-install detection, bounded warm coordination, freshness recheck, strict TOON policy defaults and exact overrides, manifest clamping, pack validation, aggregate observations, inspect and reset operations, reason-coded recovery, docs, and local tests. It excludes autonomous daemons, network calls, remote storage, embeddings, cross-repository retrieval, full GraphRAG extraction, new authority classes, and mandatory installation.

## Workflows and Failure Paths
WF-001 resolves step and policy, warms a candidate, verifies fresh source state, packs within budget, validates owner and anchors, checks economics, records an aggregate, and returns evidence. WF-002 covers absence or any unhealthy result with explicit direct reads. WF-003 serializes concurrent warmers and atomically publishes one accepted fingerprint. WF-004 supports inspect and reset without exposing raw evidence.

## Requirements and Business Rules
FR-001 through FR-008 and BR-001 through BR-006 are mandatory P0 contracts. Activation remains conditional, warming is bounded and crash-safe, policy is strict, requests stay within manifest budgets, observations are aggregate only, operations are explicit, failure reasons are stable, and sources are rechecked before publication. Cache projections never outrank repository instructions or owning steps.

## Data, Integrations, and Non-Functional Requirements
Project-local accepted and control SQLite databases use rollback journals, bounded transactions, and atomic replacement. Portable policies, receipts, and machine-facing outputs use TOON. Integration is a bounded local process invoked by shared StepCard compilation. NFRs require deterministic ordering and fingerprints, offline operation, idempotence, crash recovery, freshness, confinement, privacy, timeout bounds, and absent-module parity.

## Dependencies, Risks, and Constraints
Feature 017 commit ef67851, Python, SQLite FTS5 when enabled, shared TOON codecs, context-pack/v4, valid manifests, and writable derived cache storage are dependencies. Risks are contention, source drift, corruption, runtime variation, recursion, token regression, leakage, and compatibility drift. Controls are bounded locking, atomic replace, post-build recheck, strict decode, timeout, allowlists, validation, and direct fallback.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 are accepted. Owner: Harness Maintainers. Assumptions are local derived-storage availability, viable direct reads, recoverable FTS5 absence, and short control transactions. Impact: engineering does not need to invent product behavior. Next step: implement and validate the specified P0 contracts. Future WAL, embeddings, GraphRAG, exporter, and latency-SLO choices are separate non-blocking roadmap decisions.

## Success Measures
The release passes when mandatory-anchor recall is complete; stale, partial, or divergent accepted state is zero; concurrent warmers converge; absent and unhealthy modules preserve direct behavior; policy respects owning budgets; observations contain no raw evidence; receipts remain byte-stable; default installation is unchanged; and all mapped acceptance, security, documentation, and compatibility gates pass.

## Source Coverage
Consumed sources: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/release-slicing.md; specs-refiniment/018-context-cache-runtime/business-context.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md.

## Requirement Detail
| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref |
| --- | --- | --- | --- | --- | --- |
| FR-001 | shared runtime | activate integration only for project-installed optional module | STORY-001 | P0 | AC-001 |
| FR-002 | cache lifecycle | coordinate bounded warming and atomic fresh publication | STORY-002, STORY-003 | P0 | AC-002 |
| FR-003 | policy resolver | decode defaults and exact overrides strictly | STORY-004 | P0 | AC-003 |
| FR-004 | pack adapter | clamp limits and validate owner, anchors, freshness, ordering, authority, and economics | STORY-005 | P0 | AC-004 |
| FR-005 | control database | persist only allowlisted aggregate outcomes and token totals | STORY-006 | P0 | AC-005 |
| FR-006 | maintainer CLI | inspect and reset observation state deterministically | STORY-006 | P1 | AC-005 |
| FR-007 | shared runtime | return stable reason-coded direct reads for every unhealthy result | STORY-007 | P0 | AC-006 |
| FR-008 | cache lifecycle | recheck candidate sources before accepted replacement | STORY-003 | P0 | AC-002, AC-008 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Requirement Ref |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | normal StepCard compilation with module present | agent | resolve; warm; pack; validate; observe | accepted economical pack | any failed gate routes WF-002 | FR-001, FR-003, FR-004, FR-005 |
| WF-002 | module absent or cache unhealthy | agent | retain explicit direct paths and stable reason | authoritative direct context | no cache fault may block viable context | FR-001, FR-007 |
| WF-003 | missing, stale, corrupt, or contended projection | runtime | lock; double-check; build; source-recheck; replace | one fresh fingerprint | retry once then WF-002 | FR-002, FR-008 |
| WF-004 | support diagnosis or cleanup | maintainer | inspect aggregate state or reset it | bounded operational state | raw queries and content remain unavailable | FR-005, FR-006 |

## Business Rule Detail
| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-001 | sources and owning steps remain authoritative | every pack | business-context.md | reject and use direct reads | DEC-002 |
| BR-002 | activation requires optional project install | runtime detection | STORY-001 | retain default behavior | DEC-002 |
| BR-003 | policy never exceeds owning manifest budget | resolver and pack | STORY-004 | clamp or recover to defaults | DEC-004 |
| BR-004 | owning step and mandatory anchors are required | acceptance gate | STORY-005 | reject candidate | DEC-004 |
| BR-005 | observations are bounded aggregates only | control database | STORY-006 | reject unknown fields | DEC-005 |
| BR-006 | cache failure cannot block viable direct context | every exception | STORY-007 | stable direct fallback | DEC-002 |

## User Story Traceability
STORY-001 maps activation to FR-001 and AC-001. STORY-002 and STORY-003 map concurrency and freshness to FR-002, FR-008, and AC-002. STORY-004 maps policy to FR-003 and AC-003. STORY-005 maps acceptance to FR-004 and AC-004. STORY-006 maps operations to FR-005, FR-006, and AC-005. STORY-007 maps recovery to FR-007 and AC-006. STORY-008 owns AC-007, AC-008, and release evidence.

## Acceptance Traceability
AC-001 verifies optional absence parity; AC-002 verifies concurrent convergence and freshness; AC-003 verifies strict exact policy and budget clamp; AC-004 verifies v4 owner, anchors, source state, ordering, authority, and savings; AC-005 verifies aggregate privacy and reset; AC-006 verifies every fault fallback; AC-007 separates deterministic receipts from observational latency; AC-008 verifies confinement, no network, and deferred-scope absence. No AC is orphaned.

## QA and Operational Notes
QA must run focused unit and integration tests for installed and absent layouts, concurrent warmers, mutation during build, corruption, invalid policy, manifest clamp, missing anchors, low savings, timeout, FTS5 absence, observation privacy, and reset. Maintainers diagnose with aggregate observe and verify output, then rely on direct reads, reset observation state, or rebuild derived projections. Latency evidence is informational only.

## Handoff Risks
Implementation evidence, security review, and complete validation receipts remain lifecycle gates, not specification gaps. Highest risks are hidden activation drift, stale acceptance, unsafe contention handling, token regression, and observation leakage. Each has a named owner, deterministic test, and direct-read fallback. Release must stop if default-install parity, confinement, mandatory-anchor recall, fresh publication, or privacy evidence fails.
