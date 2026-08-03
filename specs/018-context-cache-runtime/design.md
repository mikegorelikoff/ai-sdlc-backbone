---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "stable"
generated:
  by: "process:ai-sdlc"
  at: "2026-08-03T12:33:46Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "018-context-cache-runtime"
  artifact: "design.md"
  path: "specs/018-context-cache-runtime/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "full"
  state_file: "specs/018-context-cache-runtime/_ai_sdlc/state.toon"
  decision_log: "specs/018-context-cache-runtime/decision-log.md"
  status: "approved"
  owner: "Harness Maintainers"
  created_at: "2026-08-03"
  updated_at: "2026-08-03"
  trace_ids:
    - "AC-001"
    - "AC-008"
    - "TC-001"
    - "TC-012"
  related_artifacts:
    - "specs/018-context-cache-runtime/branch-plan.md"
    - "specs/018-context-cache-runtime/decision-log.md"
    - "specs/018-context-cache-runtime/index.md"
    - "specs/018-context-cache-runtime/qa.md"
    - "specs/018-context-cache-runtime/requirements.md"
    - "specs/018-context-cache-runtime/tasks.md"
    - "specs/018-context-cache-runtime/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
---

# Design

## Overview
Add a read-through adapter to shared StepCard context compilation. It detects only project-installed cache modules, resolves bounded policy, invokes warm and pack through a local process, validates the returned v4 contract and economics, records an aggregate outcome, and returns direct context on every exception or rejection.

## Architecture
Shared runtime remains the control plane and repository paths remain authoritative. The optional context-cache process is a derived projection adapter. A rollback-journal accepted SQLite file is atomically replaced; a separate control SQLite database serializes warmers and stores aggregate observations. Strict TOON policy configures bounded behavior.

## Components
ai_sdlc_steps.py owns install detection, policy resolution, budget clamp, adapter invocation, v4 acceptance, and fallback. context_cache.py owns control schema, warm transaction, source snapshot verification, atomic projection replacement, pack economics, observation aggregation, and CLI operations. runtime-policy.toon provides safe defaults and exact override structure.

## Interfaces and Contracts
Runtime policy schema ai-sdlc-context-cache-runtime-policy/v1 accepts only known typed fields and exact skill/step overrides, then clamps to the manifest. Adapter commands emit TOON. Accepted context must decode as ai-sdlc-context-pack/v4, be packed, contain explicit direct paths, preserve owning step and mandatory anchors, verify current hashes, respect ordering/authority, and meet configured savings.

## Data Model
Accepted projection uses context-cache.sqlite3 in DELETE journal mode. Control schema stores versioned lifecycle state and allowlisted aggregate rows keyed by operation, outcome, and reason with call count, raw tokens, packed tokens, and savings totals. It stores no query text, prompt, content, credentials, identity, or deterministic timestamps.

## Error Handling
Catch missing module, invalid policy, subprocess failure, timeout, decode failure, missing FTS5, lock contention, corruption, source drift, schema/owner/anchor/hash/authority failure, budget excess, and uneconomic pack. Warm retries source drift once. Corrupt derived state rebuilds safely. Every terminal adapter failure returns explicit direct paths and a stable reason.

## Security Considerations
Resolve cache root only inside project .agents/skills or .claude/skills, never source checkout. Confine derived writes below project .ai-sdlc/cache, reject unsafe sources and symlinks, load no SQLite extensions, perform no network calls, preserve evidence-only authority for cached content, and allowlist every observation field and enum.

## Observability
Record only bounded aggregate operation, outcome, reason, call count, raw tokens, packed tokens, and calculated savings in control state. Provide observe and reset-observations operations. Deterministic receipts exclude wall-clock values; latency may be collected transiently as observational validation evidence but never influences fingerprints or golden results.

## Risks and Tradeoffs
Short-lived processes trade some latency for isolation and optional installation. Rollback journal trades potential WAL throughput for safety on affected SQLite runtimes. Single-writer bounded transactions may fall back under contention but never expose partial state. Strict validation can reduce hit rate, deliberately favoring correctness and authority over cache adoption.

## Validation Strategy
Map AC-001 through AC-008 to TC-001 through TC-012. Run cache lifecycle, concurrency, privacy, recovery, determinism, confinement, and TOON output tests; shared-runtime policy, installed/absent StepCard, timeout, fallback, and parity tests; then full runtime, docs, install smoke, security, code review, and patch gates.

## Migration Notes
No source or user data migration. Existing feature-017 accepted projections remain disposable and can rebuild. The control database initializes lazily under the confined cache root. Default installations do not detect the module and retain direct reads. Project policy is optional and invalid overrides recover to safe defaults or direct context.
