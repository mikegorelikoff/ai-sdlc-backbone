---
type: "ai-sdlc.prfaq"
title: "PRFAQ Package"
description: "Working-backwards press release, FAQ, and business requirements."
tags:
  - "ai-sdlc"
  - "discovery"
  - "requirements"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T11:40:05Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "prfaq.md"
  path: "specs-refiniment/018-context-cache-runtime/prfaq.md"
  workspace: "refinement"
  skill: "ai-sdlc-prfaq-package-synthesis"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "BR-001"
    - "BR-002"
    - "BR-003"
    - "BR-004"
    - "BR-005"
    - "BR-006"
    - "DEC-001"
    - "DEC-002"
    - "DEC-003"
    - "DEC-004"
    - "DEC-005"
    - "DEC-006"
    - "DEC-007"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-prfaq-package-synthesis"
    - "prfaq"
    - "approved"
---

# prfaq.md

## Feature Summary
Feature 018 makes the installed optional context-cache module part of normal StepCard context compilation. It automatically warms fresh local evidence, applies strict per-step TOON policy and manifest budgets, validates context-pack/v4, records privacy-safe aggregate economics, and returns to direct reads on any failure. DEC-002 defines opt-in activation and DEC-006 bounds the MVP.

## Actors and Stakeholders
Repository contributors and AI agents are users; Harness maintainers own runtime compatibility; repository maintainers own project policy; QA owns deterministic and concurrency evidence; Security owns confinement and telemetry minimization; Delivery owns rollout of the opt-in module. There is no external operator or service dependency.

## Scope and Boundaries
MVP includes runtime detection, warm-on-miss/stale, serialized warmers, source-drift rejection, strict policy resolution, token clamps, valid cached packs, aggregate observations, inspect/reset, tests, and docs. It excludes mandatory installation, daemons, network calls, embeddings, raw telemetry, multi-host operation, full GraphRAG, and a v4 schema change.

## Workflows and Failure Paths
Normal skill execution resolves a StepCard, checks module availability, loads policy, obtains or refreshes the cache under a bounded control transaction, packs evidence, validates it, and returns it. Missing module, contention, corrupt state, source drift, invalid policy, FTS5 absence, timeout, low savings, or incomplete anchors returns a stable reason-coded direct-read result.

## Requirements and Business Rules
BR-001 cache use is conditional on explicit module installation. BR-002 repository and owning skill files remain authoritative. BR-003 all derived writes stay under `.ai-sdlc/cache/`. BR-004 no runtime policy may exceed the manifest budget. BR-005 observations store counters and token totals only. BR-006 cache failure cannot remove an otherwise sufficient direct-read path.

## Data, Integrations, and Non-Functional Requirements
Data consists of the existing disposable FTS5 index, a rollback-journal control database, strict TOON policy, aggregate counters, and TOON receipts. Shared step-context compilation is the integration boundary. Required properties are offline operation, atomic acceptance, bounded locking and subprocesses, deterministic ordering, crash recovery, no symlink escape, no extensions, and unchanged default installation.

## Dependencies, Risks, and Constraints
Depends on feature 017 commit `ef67851`, optional module resolution, Python, FTS5, shared TOON codec, context-pack/v4, and validated skill manifests. Principal risks are contention, source drift, corrupt state, affected SQLite WAL runtimes, recursion, hidden token growth, and telemetry leakage. DEC-003, DEC-004, DEC-005, and direct-read fallback mitigate them.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 are accepted. Local cache storage and FTS5 are assumed available only after opt-in; absence is recoverable.

Open questions: none blocking. Owner: Architecture. Impact: no effect on MVP acceptance. Next step: evaluate patched-runtime WAL opt-in, local embeddings, and external metrics export only through separate accepted contracts after deterministic runtime evidence exists.

## Success Measures
Required outcomes: concurrent warmers converge to one fingerprint; zero stale accepted packs; 100 percent critical-anchor recall; every request stays within its StepCard budget; absent or unhealthy cache matches direct-read behavior; no raw evidence enters observations; default installation is identical; deterministic receipts repeat byte-for-byte.

## Source Coverage
Sources: `specs-refiniment/018-context-cache-runtime/discovery.md`, `specs-refiniment/018-context-cache-runtime/decision-log.md`, and `specs-refiniment/018-context-cache-runtime/index.md`; feature 017 SDD, validation, implementation, tests, and cache guide; SQLite transaction, busy-timeout, journal, integrity, and WAL-reset documentation; Python sqlite3 docs; OpenTelemetry database conventions. Coverage includes value, scope, runtime design, risk, operations, and measurement.

## Press Release
Harness users get automatic safe context reuse.

Teams that install the optional context-cache module can now run ordinary Harness skills and receive fresh, bounded repository evidence without a separate cache workflow. The runtime warms only derived local state, preserves the owning step and every critical anchor, respects the declared token budget, and returns to authoritative direct reads whenever evidence is stale, incomplete, contended, or uneconomic.

The first release is offline and project-scoped. It adds no daemon, remote service, embedding provider, raw telemetry, or new authority.

## Customer FAQ
| Question | Answer |
| --- | --- |
| Must every user install it? | No. Only the optional module activates integration; default installs keep direct reads. |
| Can it hide stale content? | No. Source hashes and post-build freshness gate every accepted pack. |
| Can cache text change instructions? | No. Retrieved repository ranges remain evidence-only under existing authority rules. |
| What happens on failure? | The StepCard receives explicit direct-read paths and stable reasons. |
| Does it upload data? | No network call or remote telemetry exists in MVP. |

## Internal FAQ
| Question | Answer |
| --- | --- |
| How are writers coordinated? | A separate rollback-journal control database uses bounded `BEGIN IMMEDIATE`; the accepted index is atomically replaced. |
| Why not WAL? | Host SQLite 3.51.0 predates the upstream 3.51.3 WAL-reset fix; safe rollback journal is the default. |
| How is policy applied? | Strict defaults plus exact skill and step overrides, always clamped to the owning manifest. |
| What is measured? | Counts, outcome reasons, raw tokens, packed tokens, and savings; never query or content payloads. |
| Who supports incidents? | Maintainers inspect observation and verify receipts, then use direct reads, reset, or rebuild. |

## Business Requirements
| ID | Requirement | Priority | Acceptance |
| --- | --- | --- | --- |
| BR-001 | Auto-activate only for installed module | P0 | absent-module parity |
| BR-002 | Serialize and recover warming | P0 | concurrent convergence |
| BR-003 | Enforce strict step policy and budget | P0 | invalid and over-budget rejection |
| BR-004 | Preserve v4 authority and anchors | P0 | 100 percent recall |
| BR-005 | Emit privacy-safe aggregate observations | P1 | schema allowlist |
| BR-006 | Keep failure non-blocking through direct reads | P0 | fault matrix passes |

## Launch Risks
| Risk | Go/no-go evidence | Mitigation |
| --- | --- | --- |
| Contention or crash | multi-process and interrupted warm tests | control transaction and atomic replace |
| Source drift | mutation-during-build test | reject and bounded retry |
| Token regression | golden economics suite | 15 percent gate and manifest clamp |
| Privacy leakage | persisted-schema security test | aggregate allowlist only |
| Compatibility drift | default and module install smoke | feature detection and fallback |

Launch is blocked until all P0 evidence, security review, documentation checks, and canonical validation pass.
