---
type: "ai-sdlc.design"
title: "Design"
description: "Technical design, interfaces, architecture, and migration decisions."
tags:
  - "ai-sdlc"
  - "sdd"
  - "design"
status: "draft"
generated:
  by: "process:ai-sdlc"
  at: "2026-07-30T08:41:38Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "015-executable-skill-harness-v4"
  artifact: "design.md"
  path: "specs/015-executable-skill-harness-v4/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/015-executable-skill-harness-v4/_ai_sdlc/state.toon"
  decision_log: "specs/015-executable-skill-harness-v4/decision-log.md"
  status: "review"
  owner: "Repository Maintainers"
  created_at: "2026-07-30"
  updated_at: "2026-07-30"
  trace_ids: []
  related_artifacts:
    - "specs/015-executable-skill-harness-v4/branch-plan.md"
    - "specs/015-executable-skill-harness-v4/decision-log.md"
    - "specs/015-executable-skill-harness-v4/index.md"
    - "specs/015-executable-skill-harness-v4/plan.md"
    - "specs/015-executable-skill-harness-v4/qa.md"
    - "specs/015-executable-skill-harness-v4/requirements.md"
    - "specs/015-executable-skill-harness-v4/research.md"
    - "specs/015-executable-skill-harness-v4/tasks.md"
    - "specs/015-executable-skill-harness-v4/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
    - "harness-v4"
---

# Design

## Overview
v4 makes each skill a portable executable protocol. A v2 manifest declares the semantic DAG; the selector resolves ready steps; the context compiler produces bounded evidence; the workflow compiler emits run v2 tasks; runtime journals deterministic transitions; host adapters execute only declared portable operations.

## Architecture
The architecture has seven deterministic layers: canonical TOON decoding and schema validation; ready-step selection; per-step context compilation; workflow and run compilation; host operation execution; evidence and replay; eval and repository conformance reporting. `SKILL.md` remains the small Agent Skills router. `steps/manifest.toon` and referenced step docs are the source of truth. Generated routers and catalogs are projections checked for drift. All structured boundaries use the same canonical codec, so fingerprints are computed from one byte representation.

## Components
- `ai_sdlc_toon.py`: sole canonical decoder and encoder for structured machine data, including stable key order, table handling, scalar rules, and malformed-input rejection.
- `ai_sdlc_steps.py`: v2 loader, DAG validator, entrypoint resolver, ready-set selector, graph fingerprint, StepCard builder, and run-plan compiler.
- `ai_sdlc_step_context.py`: deterministic anchor, topology, trace, lexical range, budget, recall, savings, authority, and direct-read compiler.
- `runtime.py`: run v2 creation, immutable per-task TOON journal, retry, idempotency, evidence, replay, and result projection.
- `workflow.py`: workflow v2 skill-node validation and manifest-to-run compilation.
- `flow.py` and shared flow: zero-write Explore card plus fingerprinted Apply.
- Host adapter: full StepCard capability negotiation and semantic-preserving execution mapping.
- Skill graph generator: semantic scaffold, router generation, inventory validation, and drift check; it contains no legacy conversion mode.
- Eval harness: all-skill deterministic fixtures, byte-repeatability receipts, repository TOON-only checks, and provider-neutral live protocol.

## Interfaces and Contracts
- `ai-sdlc-skill-steps/v2`: skill, version, entrypoints, budgets, and typed semantic nodes.
- `ai-sdlc-step-card/v1`: run-independent ready-step contract with context, gates, outputs, recovery, side-effect, idempotency, and fingerprint.
- `ai-sdlc-context-pack/v4`: exact source ranges, mandatory anchors, recall, savings, sufficiency, authority, skipped-source reasons, and fingerprint.
- `ai-sdlc-workflow/v2`: skill-node DAG with entrypoints and compile metadata.
- `ai-sdlc-run-plan/v2`, `ai-sdlc-run-event/v2`, `ai-sdlc-run-state/v2`, `ai-sdlc-run-result/v2`: durable execution contracts.
- `ai-sdlc-flow/v3`: Explore decision and Apply receipt.
- `ai-sdlc-host-adapter/v2` and `ai-sdlc-handoff/v2`: StepCard capability, evidence, and status exchange.
- `ai-sdlc-eval-receipt/v1`: deterministic or live suite receipt.
- Canonical TOON bytes are the only machine interchange representation for every contract, fixture, journal, state, and receipt.

## Data Model
A semantic step has a stable ID, document path, type, dependencies, condition, selectors, operation, capabilities, side-effect class, context contract, gates, outputs, attempts, commit boundary, and failure policy. A StepCard resolves those fields plus graph and context fingerprints. A run task copies the StepCard identity and stores status, attempts, idempotency key, evidence refs, and result. Journal events are append-only ordered records; derived state and result are replay projections.

## Error Handling
- Malformed TOON, wrong schema, unknown dependency, cycle, duplicate ID, path escape, and missing document errors fail before selection.
- Older schemas are decoded only as canonical TOON and rejected by exact expected-versus-received schema checks; there is no alternate parser, coercion path, or runtime conversion mode.
- No ready node, insufficient context, unsupported capability, stale fingerprint, and unsatisfied gate produce typed blocked outcomes before side effects.
- Started but non-terminal tasks are recoverable; replay reuses completed results and retries only within declared limits.
- Idempotency collisions with different payloads fail closed.
- Task protocol order is strict: planned, started, terminal, evidence, result. Out-of-order or identity-mismatched events are rejected.

## Security Considerations
Resolve all paths beneath the owning skill or repository root and reject symlink escape. Treat manifest operations as declarative allowlisted adapter actions, never arbitrary shell. Keep Explore free of writes. Require Apply authorization and matching fingerprint before run creation. Redact secrets from context and journal payloads. Separate read-only, workspace-write, external-write, and destructive side-effect classes and require compatible host capabilities.

## Observability
Every ready StepCard includes selection reasons and skipped reasons. Every Apply step emits planned, started, blocked or completed or failed, evidence, and result events with run, task, step, attempt, and fingerprint fields. Replay reports reused versus retried work. Context reports selected and skipped sources, token estimates, critical recall, savings, and direct-read reason. Eval receipts name fixtures, contract versions, results, environment, and unresolved release gates.

## Risks and Tradeoffs
- Mechanical decomposition can create shallow steps; mitigate with semantic step linting, a five-node floor, and representative review.
- A hard cut requires regeneration of older artifacts; mitigate with exact schema diagnostics, documented external regeneration, and no runtime ambiguity.
- Lexical retrieval can miss semantic paraphrases; mitigate with mandatory anchors, topology and trace selectors, direct reading, and live evals.
- Filesystem journals do not provide distributed transactions; keep scope local and side effects idempotent.
- Generated routers can hide source mistakes; validate manifest-to-doc-to-router round trips and review generated diffs.
- One structured representation increases conversion cost for external tools but removes dual-parser drift, stabilizes fingerprints, and shrinks context ambiguity.

## Validation Strategy
Run canonical TOON decode and byte-canonicalization checks; prove the repository and strict documentation build contain no alternate machine-format artifacts or identifiers; validate all 44 semantic graphs; run golden selector and StepCard fixtures; verify context determinism, mandatory-anchor recall, savings, authority, skipped-source reasons, and direct-read fallback; run flow zero-write snapshots; validate runtime protocol order, replay, retry, journal, and idempotency; exercise workflow and adapter integration; check generated-router drift and installed layout; run every skill test; run deterministic eval twice and compare receipt bytes; run docs and compatibility gates; then execute the representative live protocol before release.

## Migration Notes
This is a hard cut to v4. Repository-owned manifests and fixtures are regenerated once into canonical TOON and committed as the new source of truth. Runtime entrypoints contain no legacy parser, alternate serializer, compatibility mode, or in-place conversion command. Older user-owned artifacts must be regenerated outside runtime from authoritative source material, then validated against the current schema. The repository gate prevents an alternate machine-format artifact or identifier from re-entering source or documentation output.
