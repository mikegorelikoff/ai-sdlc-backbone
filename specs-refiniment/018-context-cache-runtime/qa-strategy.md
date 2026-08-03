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
  at: "2026-08-03T12:24:13Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "qa-strategy.md"
  path: "specs-refiniment/018-context-cache-runtime/qa-strategy.md"
  workspace: "refinement"
  skill: "ai-sdlc-test-scope-and-strategy-design"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "QA Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "BR-001"
    - "BR-006"
    - "DEC-001"
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
    - "specs-refiniment/018-context-cache-runtime/delivery-spec.md"
    - "specs-refiniment/018-context-cache-runtime/discovery.md"
    - "specs-refiniment/018-context-cache-runtime/goal-capability-map.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
    - "specs-refiniment/018-context-cache-runtime/prfaq.md"
    - "specs-refiniment/018-context-cache-runtime/qa-gap-review.md"
    - "specs-refiniment/018-context-cache-runtime/qa.md"
    - "specs-refiniment/018-context-cache-runtime/release-slicing.md"
    - "specs-refiniment/018-context-cache-runtime/requirements-readiness.md"
    - "specs-refiniment/018-context-cache-runtime/user-stories.md"
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
The strategy proves that optional automatic context reuse is correct, private, bounded, and backwards-compatible before measuring convenience. It prioritizes AC-001 through AC-008, WF-001 through WF-004, and BR-001 through BR-006. QA gap review returned GO, so detailed case synthesis can proceed without inventing actors, permissions, expected outcomes, or failure behavior.

## Actors and Stakeholders
Agents and contributors exercise user-visible compilation. Maintainers own lifecycle fixtures and support operations. Repository maintainers exercise policy. QA owns functional, concurrency, regression, and deterministic economics coverage; Security owns privacy and confinement. No UI, remote service, external provider, approval workflow, or production operator adds a separate test layer.

## Scope and Boundaries
In scope are unit, component, integration, multi-process, fault, install-layout, security/privacy, documentation, and manual operational review. Out of scope are remote integration, embeddings, daemon lifecycle, cross-project retrieval, full GraphRAG, live credentials, UI accessibility, and numeric performance SLOs. Latency sampling is informational, while timeout bounds are deterministic.

## Workflows and Failure Paths
WF-001 cached success is exercised end to end; WF-002 direct fallback is the central regression path; WF-003 receives controlled concurrent, mutation, corruption, and interruption coverage; WF-004 covers aggregate inspection and reset. Every named failure must demonstrate rejection or stable direct recovery, never partial state, silent authority change, or raw evidence persistence.

## Requirements and Business Rules
FR-001 through FR-008 drive functional cases, BR-001 through BR-006 drive invariant and negative cases, and AC-001 through AC-008 define release outcomes. Mandatory checks cover activation, freshness, convergence, strict policy, manifest clamp, owner and anchors, economics, privacy, stable reasons, confinement, offline behavior, and deterministic receipts.

## Data, Integrations, and Non-Functional Requirements
Tests use isolated temporary repositories and databases, deterministic files, malformed TOON, exact overrides, unsafe paths, secret-like sentinels, mutation barriers, timeouts, low-savings documents, installed and absent module trees, and repeatable clocks only where logical. SQLite is local; no third-party integration exists. Fingerprints and logical state replace wall-clock assertions.

## Dependencies, Risks, and Constraints
Positive caching depends on Python and SQLite FTS5; unavailability must validate fallback. Multi-process support and writable temporary storage are required. Main risks are race flakiness, source-tree false activation, incomplete anchor assertions, accidental raw observation storage, token-math errors, and platform timing variance. Controlled synchronization, schema equality, explicit sentinels, and repeated deterministic fixtures mitigate them.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 govern coverage. Owner: QA Maintainers. Impact: correctness, privacy, and token economics use deterministic gates, while latency remains a separate observation. Next step: synthesize cases and suites. No blocking question remains; future patched-runtime WAL, embeddings, exporters, and full GraphRAG require new strategy rather than expanding this release.

## Success Measures
Every AC has at least one automated case and every P0 risk has positive, negative, or boundary evidence appropriate to its behavior. Smoke proves direct and cached paths. Regression protects source authority and feature-017 commands. Security proves confinement and privacy. UAT demonstrates automatic value and diagnosable fallback. All deterministic receipts repeat; skipped evidence is named and owned.

## Source Coverage
Consumed sources: specs-refiniment/018-context-cache-runtime/discovery.md; specs-refiniment/018-context-cache-runtime/prfaq.md; specs-refiniment/018-context-cache-runtime/delivery-gap-review.md; specs-refiniment/018-context-cache-runtime/requirements-readiness.md; specs-refiniment/018-context-cache-runtime/goal-capability-map.md; specs-refiniment/018-context-cache-runtime/backlog-gap-review.md; specs-refiniment/018-context-cache-runtime/backlog.md; specs-refiniment/018-context-cache-runtime/user-stories.md; specs-refiniment/018-context-cache-runtime/release-slicing.md; specs-refiniment/018-context-cache-runtime/business-context.md; specs-refiniment/018-context-cache-runtime/delivery-spec.md; specs-refiniment/018-context-cache-runtime/qa.md; specs-refiniment/018-context-cache-runtime/qa-gap-review.md; specs-refiniment/018-context-cache-runtime/decision-log.md; specs-refiniment/018-context-cache-runtime/index.md.

## Test Scope
Must-test areas are absent-module parity, installed activation, concurrent fresh publication, source recheck, strict policy and clamp, v4 owner and anchors, savings rejection, aggregate-only observations, every reason-coded fallback, path confinement, offline operation, and deterministic receipts. Nice-to-test areas are broader timing distributions and extra repository shapes. Unchanged but sensitive areas are direct selection, feature-017 commands, docs, catalogs, and project install smoke.

## Risk and Coverage Priorities
| Risk | Likelihood | Impact | Coverage Layer | Priority | Owner |
| --- | --- | --- | --- | --- | --- |
| stale or partial accepted evidence | Medium | Critical | component plus controlled multi-process integration | P0 | QA, Dev |
| authority, anchor, or budget widening | Medium | Critical | unit plus StepCard integration | P0 | QA, Security |
| privacy or path breach | Low | Critical | schema, sentinel, symlink, and offline security tests | P0 | Security |
| default-install drift | Medium | High | absent and source-checkout integration smoke | P0 | QA |
| fault blocks viable context | Medium | High | parameterized fault matrix | P0 | QA |
| token regression | Medium | Medium | deterministic economics boundary tests | P1 | QA |
| support ambiguity | Low | Medium | observe/reset and manual guide review | P1 | Maintainer |
| latency variation | High | Low | observational repeated measurement | Informational | QA |

## Layer and Suite Strategy
Unit coverage owns strict decode, clamp, validation, allowlists, reasons, and token math. Component coverage owns cache build/warm/verify/observe/reset and corruption recovery. Integration coverage owns ordinary StepCard installed/absent flows and bounded process behavior. Multi-process coverage owns convergence and atomicity. Smoke runs absent direct, installed cached, one fault fallback, and privacy. Regression protects feature-017 and shared runtime. UAT demonstrates automatic reuse and maintainer diagnosis.

## Test Data Strategy
Create minimal named fixtures per rule, then combine only for end-to-end scenarios. Include exact known anchors, changing source hashes, duplicate concurrency input, invalid policy types and fields, over-budget limits, low-savings text, corrupt database bytes, unsafe symlinks, sentinel prompt-like content, missing FTS5 behavior, and installed/absent layouts. Fixtures stay local, deterministic, disposable, and free of production content or credentials.

## Environment Dependencies
Required baseline is supported Python, temporary filesystem write access, subprocess and multiprocessing, and SQLite. Active-cache cases run when FTS5 is present; absence runs the recoverable fallback case. No network, daemon, container, account, or provider is required. Platform-specific timing is never a golden assertion. Test commands must terminate within bounded time and clean only their own temporary paths.

## Automation Strategy
Automate every AC and P0 risk in unittest-based local suites with deterministic assertions. Use barriers rather than sleeps for races, exact TOON decode and schema comparisons for portable output, fixture hashes for freshness, and byte comparison for golden receipts. Keep manual review limited to policy readability, reason clarity, operational guide flow, and security schema inspection. Broader full suites run at final validation, not per small iteration.

## Strategy Risks
Residual risks are scheduler differences in multi-process tests, SQLite builds without FTS5, incomplete simulation of abrupt process death, and observational latency variance. The suite contains bounded synchronization and recoverable FTS5 expectations; crash tests verify atomic accepted state rather than relying on timing. Release blocks on any deterministic failure. Latency or unavailable optional performance evidence is reported without weakening correctness signoff.
