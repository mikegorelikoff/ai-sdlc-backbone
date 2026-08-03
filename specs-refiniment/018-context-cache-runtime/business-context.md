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
  at: "2026-08-03T12:17:44Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "business-context.md"
  path: "specs-refiniment/018-context-cache-runtime/business-context.md"
  workspace: "refinement"
  skill: "ai-sdlc-ba"
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
    - "DEC-006"
    - "DEC-007"
    - "EPIC-001"
    - "EPIC-004"
    - "GOAL-001"
    - "GOAL-004"
    - "TASK-001"
    - "WF-001"
    - "WF-002"
    - "WF-003"
    - "WF-004"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/backlog-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/backlog.md"
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
    - "ai-sdlc-ba"
    - "business-context"
    - "approved"
---

# business-context.md

## Feature Summary
Feature 018 makes the optional local context cache an automatic, bounded input to ordinary StepCard compilation. It preserves repository and owning-step authority, validates every packed result, and returns deterministic direct reads whenever cache use is unavailable, unsafe, stale, incomplete, or uneconomic. Evidence: GOAL-001 through GOAL-004, EPIC-001 through EPIC-004, and DEC-002 through DEC-007. No business-context blocker remains.

## Actors and Stakeholders
Repository contributors and AI agents consume compiled StepCards. Harness maintainers own runtime compatibility, cache lifecycle, and support. Repository maintainers own project policy. QA owns deterministic, concurrency, recovery, and token-economics evidence; Security owns confinement and observation privacy. No external service operator, tenant administrator, or remote retrieval provider participates in this release.

## Scope and Boundaries
In scope are installed-module detection, bounded warm-on-demand, single-writer coordination, post-build freshness checks, strict TOON policy with exact overrides, manifest-budget clamping, context-pack/v4 validation, aggregate observations, inspection and reset, reason-coded direct-read fallback, documentation, security checks, and regression evidence. DEC-006 excludes daemons, embeddings, remote services, network telemetry, cross-project indexes, and full GraphRAG.

## Workflows and Failure Paths
The runtime resolves an owning step, detects the optional module, resolves policy, coordinates warming, requests a bounded pack, verifies source hashes, mandatory anchors, ordering, authority, and economics, records an allowlisted aggregate outcome, then returns the pack. Absent module, contention, mutation, corruption, invalid policy, timeout, missing FTS5, missing anchors, or low savings ends in explicit direct reads without widening authority.

## Requirements and Business Rules
FR-001 through FR-008 require conditional activation, bounded crash-safe warming, strict policy, manifest-budget enforcement, aggregate observation, inspect and reset operations, stable fallback reasons, and source snapshot verification. BR-001 through BR-006 keep sources authoritative, confine writes below the project cache, preserve owning-step and mandatory anchors, minimize observations, and make cache failure non-blocking when direct context is viable.

## Data, Integrations, and Non-Functional Requirements
The accepted projection and separate control database are project-local SQLite files using rollback journals and atomic replacement. Portable policy and receipts use TOON. Integration occurs only at shared StepCard context compilation through a bounded local process. Required qualities are deterministic ordering and fingerprints, offline operation, idempotence, crash recovery, freshness, path confinement, privacy, bounded timeouts, and default-install compatibility.

## Dependencies, Risks, and Constraints
Delivery depends on feature 017, Python standard library, SQLite FTS5 when activated, shared TOON codecs, context-pack/v4, valid step manifests, and a writable project cache directory. Risks include contention, source drift, corruption, runtime variation, recursion, token regression, and observation leakage. Accepted controls are bounded transactions, atomic replacement, strict decoding, source recheck, process timeout, schema allowlists, and direct-read recovery.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 are accepted and cover branch lineage, optional activation, concurrency, policy, privacy, scope, and measurement. Owner: Harness Maintainers. Assumptions: project-local derived storage is writable, direct reads remain viable, and FTS5 absence is recoverable. Impact: no MVP choice is unresolved. Next step: complete delivery and QA evidence; future WAL, embedding, GraphRAG, or exporter work requires a separate decision.

## Success Measures
Acceptance requires complete mandatory-anchor recall, zero stale or partially built accepted packs, one logical fingerprint across concurrent warmers, direct-read parity when the module is absent or unhealthy, policy requests within the owning manifest budget, no raw evidence in observations, byte-stable deterministic receipts, and unchanged default installs. Aggregate outcomes and token totals demonstrate adoption and savings; latency remains observational.

## Source Coverage
Consumed sources: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/release-slicing.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md. These current artifacts cover intent, authority, workflows, rules, risks, acceptance, sequencing, ownership, and feature inventory.

## Current Behavior
The optional cache can build, verify, query, and pack local evidence through a separate command workflow, while normal StepCard compilation continues to scan authoritative repository paths directly. Users or agents must invoke refresh and packing manually, so safe reuse is easy to miss and aggregate operational evidence is unavailable in the ordinary skill path.

## Desired Behavior
After the optional module is installed, ordinary StepCard compilation automatically attempts a bounded warm and validated pack using exact step policy and the manifest ceiling. A fresh, complete, economical pack becomes context evidence; every other outcome returns the same authoritative direct-read paths with a stable reason. The integration remains invisible when the module is absent and never requires a daemon or network.

## Actor and Permission Matrix
| Actor | Role | Permissions | Restrictions | Source |
| --- | --- | --- | --- | --- |
| Contributor or agent | StepCard consumer | run ordinary skills and receive packed or direct context | cannot grant cache authority or access excluded paths | discovery.md; AC-001 |
| Harness maintainer | runtime owner | maintain adapter, lifecycle, reason codes, and support commands | must preserve compatibility and bounded behavior | backlog.md; TASK-001 |
| Repository maintainer | policy owner | set strict project and exact step overrides | cannot exceed manifest budgets or weaken anchors | DEC-004; AC-003 |
| QA reviewer | evidence owner | execute deterministic, concurrency, fault, and economics suites | latency cannot enter golden fingerprints | DEC-007; AC-007 |
| Security reviewer | boundary owner | verify confinement and observation schema | no raw content, query, credential, or identity may persist | DEC-005; AC-005 |

## Workflow Detail
| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| WF-001 | ordinary step compilation with module installed | agent | resolve policy; warm; pack; validate; observe | accepted economical pack | any failed gate returns WF-002 | AC-003; AC-004 |
| WF-002 | module absent or cache outcome unsafe | agent | preserve direct paths; attach stable reason | authoritative direct context | none may block a viable step | AC-001; AC-006 |
| WF-003 | concurrent or stale warming | maintainer runtime | acquire bounded control transaction; build candidate; recheck sources; publish atomically | one fresh logical fingerprint | contention or drift retries once then uses WF-002 | AC-002 |
| WF-004 | support inspection or reset | maintainer | inspect aggregates or reset observation rows | diagnosable or clean control state | raw evidence is never exposed | AC-005 |

## Business Rule Catalog
| Rule ID | Rule | Applies To | Failure Behavior | Source | Decision Ref |
| --- | --- | --- | --- | --- | --- |
| BR-001 | Repository sources and owning steps remain authoritative. | every compilation | use direct reads and reject conflicting cache evidence | discovery.md | DEC-002 |
| BR-002 | Cache use activates only with the optional project installation. | module detection | preserve default direct-read behavior | prfaq.md | DEC-002 |
| BR-003 | Requested limits never exceed the owning manifest budget. | policy resolution | clamp safely or reject invalid policy | discovery.md | DEC-004 |
| BR-004 | Owning step and all mandatory anchors must survive packing. | pack acceptance | reject pack and return direct reads | AC-004 | DEC-004 |
| BR-005 | Observations contain only allowlisted aggregate counts and token economics. | control database | reject unknown fields and retain no raw evidence | AC-005 | DEC-005 |
| BR-006 | Cache failure cannot block a step with viable direct context. | every fault path | return stable reason-coded direct reads | AC-006 | DEC-002 |

## Acceptance Criteria
| AC ID | Given | When | Then | Rule Ref | Source |
| --- | --- | --- | --- | --- | --- |
| AC-001 | optional module is absent | a StepCard compiles | output matches authoritative direct-read behavior | BR-002, BR-006 | user-stories.md |
| AC-002 | multiple warmers or source mutation | warming runs concurrently | only one fresh logical fingerprint is accepted and no partial index is visible | BR-001 | backlog.md |
| AC-003 | valid or invalid exact overrides exist | policy resolves | strict values are applied within the manifest ceiling or safe defaults recover | BR-003 | decision-log.md |
| AC-004 | a candidate pack exists | acceptance gates run | owner, anchors, freshness, ordering, authority, and savings all pass before use | BR-001, BR-004 | requirements-readiness.md |
| AC-005 | cache operations occur | observations are inspected | only allowlisted aggregate outcomes and token totals are present and reset works | BR-005 | backlog.md |
| AC-006 | contention, timeout, corruption, drift, or validation failure occurs | compilation completes | stable reason-coded direct reads are returned | BR-006 | user-stories.md |
| AC-007 | deterministic and performance evidence is collected | receipts are compared | fingerprints stay byte-stable while latency is reported separately | BR-001 | DEC-007 |
| AC-008 | paths, authority, and scope are challenged | security gates run | derived writes remain confined and deferred remote retrieval remains absent | BR-001, BR-005 | DEC-006 |

## Business Context Gaps
No unresolved business-context gap affects delivery. Actors, permissions, desired workflow, failure outcomes, authority, storage, privacy, acceptance, dependencies, and MVP exclusions are explicit and trace to approved decisions. Remaining work is lifecycle evidence rather than clarification: Dev completes implementation SDD alignment, QA executes deterministic and fault suites, Security verifies boundaries, and maintainers produce release-readiness receipts.
