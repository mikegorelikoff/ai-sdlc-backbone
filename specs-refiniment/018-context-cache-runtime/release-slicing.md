---
type: "ai-sdlc.release-slicing"
title: "Release Slicing and Readiness"
description: "MVP and release slices, sequencing, and backlog readiness."
tags:
  - "ai-sdlc"
  - "planning"
  - "release"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:14:36Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "release-slicing.md"
  path: "specs-refiniment/018-context-cache-runtime/release-slicing.md"
  workspace: "refinement"
  skill: "ai-sdlc-release-slicing-and-backlog-readiness-review"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "DEC-001"
    - "DEC-006"
    - "DEC-007"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/backlog-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/backlog.md"
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/delivery-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-release-slicing-and-backlog-readiness-review"
    - "release-slicing"
    - "approved"
---

# release-slicing.md

## Feature Summary
Feature 018 is sliced as one production MVP delivered through three evidence-gated increments: safe cache foundation, automatic governed StepCard integration, and operational/release assurance. All portable machine artifacts remain TOON.

## Actors and Stakeholders
Contributors and agents receive value in slice 2; maintainers implement and operate slices 1 through 3; repository maintainers own policy; QA and Security gate each boundary. No external operator or service is introduced.

## Scope and Boundaries
MVP contains STORY-001 through STORY-008. Autonomous daemons, remote retrieval, embeddings, full GraphRAG, cross-project state, network telemetry, mandatory installation, and pack schema changes remain excluded by DEC-006.

## Workflows and Failure Paths
Slice 1 proves convergent fresh state; slice 2 enables policy-bounded pack selection and direct fallback; slice 3 adds aggregate diagnosis and full fault/security evidence. No slice exposes a partial unsafe user path.

## Requirements and Business Rules
AC-001 through AC-008 are launch gates. Source authority, owning-step precedence, mandatory anchors, manifest-budget clamp, project-local writes, aggregate-only observations, optional installation, and direct fallback apply to every slice.

## Data, Integrations, and Non-Functional Requirements
Rollback-journal index and control SQLite state, strict TOON, bounded subprocess, v4 validation, deterministic fingerprints, offline operation, atomic publication, source freshness, privacy, and default-install parity are required before release.

## Dependencies, Risks, and Constraints
Feature 017 ef67851 is the baseline. Safe lifecycle and freshness precede policy/pack activation; fallback is implemented with the adapter; observations follow the stable control schema; QA, Security, docs, and full validation gate launch.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 are accepted. Owner: Harness Maintainers. Impact: no unresolved MVP decision affects slicing. Next step: execute the logical slices without fake sprint dates; later retrieval work requires a new feature.

## Success Measures
The MVP exits only with absent-module parity, concurrent convergence, zero stale/partial accepted packs, exact policy and budget enforcement, complete anchors, configured savings, privacy-safe observations, deterministic receipts, and passing installation/docs/security gates.

## Source Coverage
Consumed: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md.

## MVP Slice
The MVP is the complete bounded local runtime integration: STORY-002 and STORY-003 establish safe lifecycle; STORY-004 and STORY-005 establish governance; STORY-001 and STORY-007 expose automatic use with recovery; STORY-006 provides local operations; STORY-008 supplies release evidence. Observation ergonomics is P1 but included because supportability is required for production.

## Release Slice Matrix
### Release Slices

| Slice | Value | Stories | Dependencies | Exit Criteria | Risks |
| --- | --- | --- | --- | --- | --- |
| RS-1 Safe foundation | publish only fresh convergent local state | STORY-002, STORY-003 | feature 017, SQLite | concurrent, corruption, crash, and drift tests pass | lock contention, runtime variation |
| RS-2 Governed automatic reuse | normal StepCards receive valid economical packs or direct reads | STORY-001, STORY-004, STORY-005, STORY-007 | RS-1, TOON, manifests, v4 | activation, policy, budget, anchors, economics, timeout, parity pass | hidden drift, recursion, token regression |
| RS-3 Operational trust | support and approve production behavior | STORY-006, STORY-008 | RS-1, RS-2 | observation privacy, docs, install, security, full validation pass | cardinality, incomplete evidence |

## Sequencing and Dependencies
1. Control schema and atomic warm lifecycle. 2. Source snapshot rejection and corruption recovery. 3. Strict policy and manifest clamp. 4. Pack validation and automatic adapter. 5. Stable fallback catalog. 6. Aggregate observe/reset. 7. concurrency, security, docs, default/module install, and full regression evidence. Lifecycle and governance can partially run in parallel after contracts stabilize.

## Milestones and Readiness
M1 foundation-ready: STORY-002/003 tests green. M2 runtime-ready: STORY-001/004/005/007 tests green and installed-module smoke uses packed context. M3 release-ready: STORY-006/008, security review, code review, documentation, skill validation, and canonical receipt pass. Backlog readiness score is 9/10; implementation evidence is the only remaining point.

## Release Risks
| Risk | Signal | Mitigation | Owner |
| --- | --- | --- | --- |
| contention or crash | lock timeout/divergent fingerprint | bounded transaction, atomic replace, direct fallback | Dev, QA |
| source drift | post-build mismatch | reject and retry once | Dev |
| policy/authority drift | invalid field or widened budget | strict decode, clamp, v4 validation | Security |
| privacy leakage | forbidden persisted column/value | allowlist and schema test | Security |
| performance regression | timeout/fallback spike | bounded process and observational measurements | QA |
| compatibility drift | default install differs | absent-module parity and install smoke | Maintainer |

## Release Verdict
READY FOR LOGICAL DELIVERY SLICES; NOT YET READY FOR RELEASE. Top reasons: scope and dependencies are explicit, every story has acceptance/scenario coverage, and failure is safely recoverable. Release remains gated on completed SDD, security/code review, and canonical validation evidence.
