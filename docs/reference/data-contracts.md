---
title: Data contracts
description: Core versioned records used for artifacts, handoffs, modules, compatibility, context, and findings.
---

| Schema | Purpose |
| --- | --- |
| `ai-sdlc-artifact-metadata/v1` | Route, own, index, and trace Markdown artifacts. |
| `ai-sdlc-handoff/v2` | Communicate result, blockers, and next actions. |
| `ai-sdlc-module/v1` | Register compatible core or optional capabilities. |
| `ai-sdlc-compatibility-result/v1` | Report release contract validation. |
| `ai-sdlc-change-set/v1` | Identify an isolated draft change, its canonical targets, authority boundary, artifacts, and deterministic fingerprint. |
| `ai-sdlc-spec-delta/v1` | Project validated requirement operations, stable IDs, source hashes, scenarios, and non-mutation authority. |
| `ai-sdlc-change-preview/v1` | Record virtual target diffs, conflicts, stale evidence, reopen actions, gates, and drift-sensitive preview identity. |
| `ai-sdlc-change-approval/v1` | Bind an accountable accepted decision and complete gate set to one current preview fingerprint. |
| `ai-sdlc-change-recovery/v1` | Preserve target hashes, backups, applied paths, transaction state, and rollback evidence. |
| `ai-sdlc-delivery-node/v1` | Identify one feature-scoped lifecycle object with exact repository or Git anchors. |
| `ai-sdlc-delivery-edge/v1` | Record one evidence-backed semantic or declaration relationship. |
| `ai-sdlc-delivery-graph/v1` | Aggregate deterministic nodes, edges, coverage gaps, orphans, source identity, and graph identity. |
| `ai-sdlc-evidence-source/v1` | Capture producer, subjects, artifact and dependency hashes, expiry, and upstream evidence identity. |
| `ai-sdlc-evidence-ledger/v1` | Recalculate evidence state, propagate staleness, and report fresh-only lifecycle coverage. |
| `ai-sdlc-policy-layer/v1` | Declare versioned action rules, predicates, effects, gates, protection, and waiver eligibility. |
| `ai-sdlc-policy-waiver/v1` | Bind one accountable, constrained, expiring exception to an exact rule and decision. |
| `ai-sdlc-policy-decision/v1` | Explain the resolved allow, require, or deny result with provenance, gates, reasons, and waiver outcomes. |
| `ai-sdlc-repository-topology/v2` | Map ownership, source-to-test links, manifests, stack, commands, revision, and topology identity. |
| `ai-sdlc-context-selectors/v2` | Declare conditional task, path, and tag selectors with include globs, priority, caps, and exclusions. |
| `ai-sdlc-context/v3` | Preserve a bounded per-skill evidence snapshot, targeted next reads, gaps, trace IDs, and presentation-only interaction preferences. |
| `ai-sdlc-context-pack/v3` | Return goal-relevant explained ranges, instruction authority, sufficiency, budget allocation, exclusions, freshness, and task identity. |
| `ai-sdlc-skill-steps/v2` | Declare one skill's semantic DAG, entrypoints, context budget, operations, gates, outputs, side effects, retries, and recovery policy. |
| `ai-sdlc-step-card/v1` | Carry one dependency-ready semantic step with resolved context, capabilities, idempotency scope, and graph/step fingerprints. |
| `ai-sdlc-context-pack/v4` | Compile exact per-step source ranges, instruction authority, selected/skipped evidence, mandatory-anchor recall, savings, sufficiency, and direct-read fallback. |
| `ai-sdlc-context-cache-receipt/v1` | Report local index build, inspection, verification, or purge status with logical cache and repository fingerprints. |
| `ai-sdlc-context-query/v1` | Return fresh ranked lexical and bounded graph evidence, exact source identity, explained fallback, and query fingerprint. |
| `ai-sdlc-context-cache-benchmark-cases/v1` | Declare deterministic golden queries, expected paths and anchors, owning steps, budgets, and expected packed or direct-read strategies. |
| `ai-sdlc-context-cache-benchmark/v1` | Compare lexical, graph-enhanced, and context-pack outcomes with recall, savings, stable mode fingerprints, and a deterministic release verdict. |
| `ai-sdlc-run-plan/v2` | Define immutable StepCard-derived dependency tasks, fingerprints, idempotency keys, retry limits, budgets, and commit boundaries. |
| `ai-sdlc-run-event/v2` | Append one canonical TOON transition with contiguous sequence, previous-event identity, task attempt, and evidence payload. |
| `ai-sdlc-run-state/v2` | Project replayable task phase, status, attempts, readiness, budgets, stop reason, and run identity. |
| `ai-sdlc-workflow/v2` | Declare installed skill nodes, canonical phase entrypoints, dependencies, bounded conditions, routing evidence, and explicit approval owners. |
| `ai-sdlc-workflow-plan/v2` | Record node decisions, dependency waves, approvals, derived capabilities and side effects, plus the embedded runtime plan. |
| `ai-sdlc-host-adapter/v2` | Declare host identity, harness API range, capabilities, equivalent operation mappings, concurrency, and isolation. |
| `ai-sdlc-capability-request/v2` | Request execution of one complete StepCard without weakening its operation, side-effect, approval, context, output, evidence, or idempotency semantics. |
| `ai-sdlc-capability-negotiation/v2` | Explain native mappings, registered equivalent fallbacks, missing requirements, effective limits, compatibility, and preserved StepCard identity. |
| `ai-sdlc-effect-request/v1` | Bind one allowlisted effect driver to the negotiated operation, StepCard, context, capabilities, approval, arguments, and stable idempotency key. |
| `ai-sdlc-effect-receipt/v1` | Prove one durable effect outcome and permit exact replay without repeating the effect. |
| `ai-sdlc-scheduler-state/v1` | Project ready work, leases, attempts, terminal results, revisions, and the scheduler event chain deterministically. |
| `ai-sdlc-scheduler-dispatch/v1` | Bind one scheduler lease to one isolated StepCard runtime sub-run and context fingerprint. |
| `ai-sdlc-eval-receipt/v1` | Record deterministic all-skill scenarios or provider-neutral live-protocol checks with a canonical receipt fingerprint. |
| `ai-sdlc-provider-execution/v1` | Attest provider, host, model, execution identity, scenario version, per-scenario evidence, effect receipts, and recovery proof. |
| `ai-sdlc-live-eval-receipt/v1` | Validate a provider observation against the pinned protocol and thresholds; unattested execution remains pending. |
| `ai-sdlc-test-suite-receipt/v1` | Prove that every discovered skill-owned Python test file executed, report explicit status per file, and prevent silent zero-test discovery. |
| `ai-sdlc-doctor-report/v1` | Report deterministic installation checks, evidence, remediation, and health. |
| `ai-sdlc-upgrade-inventory/v1` | Describe versioned package files with safe paths, hashes, schemas, and harness API range. |
| `ai-sdlc-upgrade-plan/v1` | Preview file changes, schema migrations, backups, rollback actions, compatibility, and blockers. |
| `ai-sdlc-package/v1` | Declare package origin, compatibility, capabilities, files, digest, and provenance evidence. |
| `ai-sdlc-package-trust-decision/v1` | Evaluate origin, compatibility, capabilities, file integrity, and required provenance independently. |
| `ai-sdlc-local-metrics/v1` | Aggregate content-free local run, task, retry, budget, coverage, and freshness measures. |
| Project context contracts | Preserve evidence-backed repository memory and drift identity. |
| Quality finding contracts | Record evidence, severity, owner, resolution, and trace targets. |

## Artifact metadata fields

Required metadata includes feature, artifact, path, workspace, skill, flow mode, state file, decision log, status, owner, timestamps, trace IDs, related artifacts, validation, and metatags.

Versioned contracts evolve additively within a major harness API. Breaking
field or authority changes require an explicit decision, source regeneration
guidance, and compatibility review. Runtime never silently coerces an older
schema.

## Representation strategy

TOON is the only structured machine-data representation. One shared canonical
codec reads and writes contracts, fixtures, manifests, context, plans, journal
events, state, and receipts. Human review uses Markdown, but Markdown never
replaces a required machine field.

Every runtime event is one hash-chained
`_ai_sdlc/runs/<run-id>/journal/<sequence>.toon` file. Repository and strict
documentation-build gates reject alternate machine artifacts or identifiers
and validate all TOON inputs. See
[TOON-only agent artifacts](../explanation/toon-first.md).
