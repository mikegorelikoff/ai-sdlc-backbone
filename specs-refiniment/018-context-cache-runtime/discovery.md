---
type: "ai-sdlc.discovery"
title: "Working Backwards Discovery"
description: "Customer problem, audience, value, scope, and discovery evidence."
tags:
  - "ai-sdlc"
  - "discovery"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T11:37:47Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "discovery.md"
  path: "specs-refiniment/018-context-cache-runtime/discovery.md"
  workspace: "refinement"
  skill: "ai-sdlc-working-backwards-discovery"
  flow_mode: "full"
  state_file: "specs-refiniment/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs-refiniment/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "DEC-001"
    - "DEC-007"
  related_artifacts:
    - "specs-refiniment/018-context-cache-runtime/decision-log.md"
    - "specs-refiniment/018-context-cache-runtime/index.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "refinement"
    - "ai-sdlc-working-backwards-discovery"
    - "discovery"
    - "approved"
---

# discovery.md

## Feature Summary
Feature 018 turns the optional deterministic context cache from an explicit CLI utility into an operational runtime capability. When the context-cache module is installed, step selection warms or refreshes the local projection, resolves a strict step policy, asks the cache for an anchor-complete context-pack/v4, and falls back to existing direct reads on any unsafe or uneconomic outcome. The feature preserves repository authority, offline operation, the default non-module installation, and TOON-only portable interchange.

Evidence: user acceptance of the proposed feature 018 scope; feature 017 implementation and validation; DEC-001 through DEC-007.

## Actors and Stakeholders
Primary users are repository contributors and AI agents running Harness skills. Harness maintainers own the runtime adapter and compatibility contract; repository maintainers own project policy; security reviewers own data-minimization and path boundaries; QA owns concurrency, recovery, and token-economics evidence. No external service, operator account, or remote cache administrator is introduced.

The buyer and beneficiary are the same local engineering organization: it opts into the module and benefits from fewer repeated reads without giving the cache authority.

## Scope and Boundaries
In scope: installed-module detection, automatic bounded warming, single-writer coordination, source-drift rejection, strict TOON policy defaults and exact step overrides, manifest-budget clamping, cached pack use, deterministic direct-read fallback, aggregate local counters, inspect and reset operations, documentation, security checks, and regression coverage.

Out of scope: autonomous background daemons, remote services, embeddings, cross-repository or cross-tenant indexes, raw prompt or content telemetry, full GraphRAG entity/community pipelines, a context-pack schema change, and mandatory installation.

## Workflows and Failure Paths
Happy path: a step selector resolves the owning StepCard, detects the installed module, loads validated policy, acquires the control transaction, verifies or incrementally warms the index, requests a bounded pack, validates v4, records aggregate counters, and returns the pack. An already-fresh cache produces a no-op warm result.

Failure paths: absent module keeps direct reads; lock timeout, missing FTS5, corrupt cache, source drift, invalid policy, stale post-build state, low savings, missing anchors, or adapter timeout yields a reason-coded direct-read fallback. No failure may fabricate evidence, widen authority, or block a step whose direct context remains sufficient.

## Requirements and Business Rules
FR-001 installed-module auto activation; FR-002 bounded crash-safe warming; FR-003 strict step policy; FR-004 manifest token-budget enforcement; FR-005 aggregate observability; FR-006 explicit inspect/reset; FR-007 stable fallback reasons; FR-008 source snapshot verification.

Business rules: repository sources and owning skill steps stay authoritative; cache evidence is evidence_only except pre-existing scoped repository instructions; automatic writes are confined to ignored derived cache paths; the cache is an optimization and never a prerequisite when direct reads are available.

## Data, Integrations, and Non-Functional Requirements
The accepted index remains `.ai-sdlc/cache/context-cache.sqlite3`; a separate project-local control SQLite database coordinates warmers and stores aggregate counters. Portable policy and receipts are TOON. Runtime integration occurs in shared step-context compilation and invokes the optional cache through a bounded process boundary.

NFRs: deterministic ordering and fingerprints; one accepted writer; atomic replacement; bounded lock and process timeouts; no network; no extensions; no symlink traversal; no raw query, content, secret, identity, or timestamp in deterministic receipts; default install compatibility.

## Dependencies, Risks, and Constraints
Dependencies are feature 017 at `ef67851`, Python standard library, SQLite with FTS5, context-pack/v4 validation, optional-module installation, and current step manifests. Key risks are writer contention, source changes during warming, corrupt projections, SQLite runtime variation, adapter recursion, token regression, high-cardinality telemetry, and hidden behavior changes.

Constraints: TOON-only portable machine artifacts; no network or daemon; cache paths stay under the project root; rollback-journal safety is preferred because host SQLite 3.51.0 predates the upstream WAL-reset fix.

## Decisions, Assumptions, and Open Questions
DEC-001 through DEC-007 are accepted. Assumptions: local repositories are writable below `.ai-sdlc/cache/`; direct-read compilation remains available; FTS5 absence is recoverable; one process can hold a short control transaction while a temporary index is built. No blocking product question remains.

Open future questions, not MVP blockers: whether a patched SQLite runtime should later opt into WAL; which local embedding adapter might be supported; whether organizations need an external metrics exporter.

## Success Measures
Acceptance requires 100 percent mandatory-anchor recall; zero stale or partially built accepted packs; all concurrent warmers converge on one logical fingerprint; direct-read parity when the module is absent or unhealthy; policy requests never exceed the owning step budget; no raw evidence in observations; default installation remains unchanged.

Operational measures are warm no-op rate, rebuild count, contention fallback count, cached-pack count, direct-read fallback count, raw and packed token totals, and calculated savings. Golden receipts remain byte-identical; latency is observational only.

## Source Coverage
Consumed: `specs/017-local-context-cache/requirements.md`, `design.md`, and `validation.md`; refinement delivery and QA readiness for feature 017; the public cache guide; the cache contract; shared step-context and step-selection runtime; current cache implementation and tests; SQLite WAL, transaction, busy timeout, integrity-check, and journal-mode documentation; Python sqlite3 documentation; OpenTelemetry database semantic conventions; the user-approved feature 018 scope; `specs-refiniment/018-context-cache-runtime/decision-log.md`; and `specs-refiniment/018-context-cache-runtime/index.md`.

These sources cover product intent, current behavior, gaps, concurrency mechanics, recovery, observability vocabulary, security boundaries, compatibility, active decisions, and current artifact inventory.

## Customer and Problem Evidence
Target customer: teams using AI SDLC Harness repeatedly across medium or large repositories after explicitly installing the context-cache module. The current cache already retrieves useful bounded evidence, but users or agents must build, verify, query, and pack it manually; the normal StepCard path still performs direct repository scans. This leaves token savings optional in theory but operationally easy to miss.

The concrete pain is repeated broad reading, redundant index work, inconsistent manual refresh behavior, and no aggregate proof that the cache saves context safely.

## Current Process and Alternatives
Today, StepCard compilation directly scans selected repository paths while the cache CLI is a separate workflow. A user can manually build and pack, or ignore the module and use direct reads. Alternatives considered were a background daemon, unconditional WAL, remote vector storage, and changing every skill manifest.

The chosen alternative is read-through integration at the existing step-context boundary with short-lived processes, strict policy, a control database, and direct-read recovery. It requires no service lifecycle and preserves the v4 pack contract.

## Value Proposition and Business Goals
For Harness contributors who repeatedly load repository context, the runtime integration automatically reuses fresh local evidence so they spend fewer tokens and less manual effort, unlike the current disconnected CLI workflow. The immediate value is a safe cache hit inside normal step selection; the long-term value is measurable context economics without provider lock-in.

Primary business goal: increase effective adoption of the optional cache while holding correctness and authority constant. Secondary goals: reduce support ambiguity and produce evidence for later retrieval investments.

## Users, Roles, and Scenarios
Contributor scenario: install the optional module and run a normal skill; no cache command is needed. Agent scenario: compile a StepCard and receive either a validated packed context or explicit direct reads. Maintainer scenario: inspect aggregate counters and resolved policy. QA scenario: run concurrent warmers, corruption, drift, and absent-module tests. Security scenario: verify no prompt or content telemetry.

Permissions are filesystem-local only. The integration cannot authorize commands, change approvals, access the network, or read excluded files.

## MVP and Priorities
Must: automatic installed-module detection; warm-on-miss/stale; bounded single-writer coordination; post-build freshness; strict TOON policy; budget clamp; v4 validation; aggregate counters; fallback; tests and docs. Should: exact skill/step overrides and observation reset. Could: patched-runtime WAL opt-in and exporter adapters. Won't: daemon, embeddings, remote telemetry, global GraphRAG, multi-host cache.

P0 is correctness, confinement, and fallback. P1 is policy ergonomics and operational reporting. Performance optimization cannot weaken P0.

## Functional and Non-Functional Needs
Functionally the runtime resolves policy, warms exactly once under contention, packs with the owning step first, records only aggregate outcomes, and exposes warm/observe/reset commands. It reports stable reason codes for hit, rebuild, contention, invalid policy, unavailable module, stale source, corrupt cache, uneconomic pack, and validation failure.

Non-functionally it is deterministic, offline, bounded, idempotent, crash-recoverable, source-fresh, backwards-compatible, and testable across project install layouts. Any inability to satisfy these properties returns to direct reads.

## Operations, Launch, and Support
Launch as an enhancement to the opt-in module, initially enabled automatically only where that module is present. Documentation explains the derived writes, policy precedence, counters, fallback reasons, purge/reset, and why WAL is not the default. Support starts with `observe`, `verify`, and direct-read recovery.

Go/no-go requires concurrency tests, crash/corruption recovery, installed and absent-module workflows, token-budget and authority tests, security review, docs validation, and a current full validation receipt.

## Discovery Risks and Dependencies
| Risk | Signal | Mitigation | Owner | Fallback |
| --- | --- | --- | --- | --- |
| Concurrent warmers | lock contention rises | bounded control transaction and double-check | Dev | direct reads |
| Source drift | post-build hash mismatch | reject replacement and retry once | Dev | direct reads |
| Unsafe SQLite mode | affected runtime detected | keep DELETE journal default | Security | atomic rebuild |
| Policy drift | strict decode fails | ignore unsafe override with reason | Maintainer | safe defaults/direct reads |
| Token regression | savings below 15 percent | v4 economics gate | QA | direct reads |
| Telemetry leakage | unexpected stored field | schema allowlist and tests | Security | disable counters |

Feature 017, FTS5, and shared runtime are required dependencies; no external dependency blocks delivery.
