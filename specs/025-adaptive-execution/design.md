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
  at: "2026-09-15T13:25:36Z"
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "025-adaptive-execution"
  artifact: "design.md"
  path: "specs/025-adaptive-execution/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/025-adaptive-execution/_ai_sdlc/state.toon"
  decision_log: "specs/025-adaptive-execution/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-09-15"
  updated_at: "2026-09-15"
  trace_ids:
    - "TC-001"
    - "TC-014"
  related_artifacts:
    - "specs/025-adaptive-execution/decision-log.md"
    - "specs/025-adaptive-execution/index.md"
    - "specs/025-adaptive-execution/plan.md"
    - "specs/025-adaptive-execution/qa.md"
    - "specs/025-adaptive-execution/requirements.md"
    - "specs/025-adaptive-execution/tasks.md"
    - "specs/025-adaptive-execution/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
---

# Design

## Overview
Incrementally extend existing runtimes; classify depth separately from quick/full interaction flags.

## Architecture
### Observed execution before this change

| Entry / stage | Owner and inputs | Outputs | Blocking dependency / next stage | Observed cost |
| --- | --- | --- | --- | --- |
| Harness Explore | flow.py → build_card; intent, role/action, source evidence, lifecycle state | Fingerprinted decision card, selected StepCard, compiled run plan | Read-only; Apply revalidates the card | Repeated manifest/context compilation: about 3,900 read_bytes calls, 25 MB per measured decision |
| Harness context | select_references → select_steps → compile_step_context, then compile_run_plan → select_steps and cards again | Source-bound excerpts, mandatory anchors, token estimates | Context sufficiency before owning action | Same files read repeatedly; existing optional graph cache already provides cross-session retrieval |
| Harness Apply/runtime | Accepted current card, immutable graph task plan | Runtime journal, task state, stage artifacts | Dependency closure, existing max_attempts and owning validators | Already supports dependency waves and bounded runtime attempts; no evidence that every task runs all lifecycle skills |
| Loop Specify | loop.py specify / ai-sdlc-loop-specify; request, allowed paths, traces | spec.toon, state.toon | Current implementation approval → Implement | Compact deterministic receipt, not duplicated planning/readiness/full SDD records |
| Loop Implement | implement-check / implementation owner; current specification and approval | Source diff | Current diff → Engineering Quality Gate | Source changes are performed by host agent, not an in-process model client |
| Loop Quality Gate | context, finalize, verify_report_current; request, diff, source examples, check candidates, semantic draft | quality-context.toon, quality-gate.toon | Current ready report → Verify | Context rebuilt during freshness validation; retained because new/changed source must invalidate evidence |
| Loop Verify | explicit argv commands plus current spec/approval/snapshot/quality report | evidence.toon and stage state | All command exits pass, no source drift → completion / separately authorized Commit | Commands executed sequentially; no per-feature verification budget in old CLI |
| Optional specialists | Explicit doctor/review/security/QA owner | Owning reports | Only selected capability / next requested action | No evidence that all hunters or doctor were automatically invoked on every task |
| Commit / promotion | Current spec and passing evidence; separate commit approval | Commit or Harness promotion TOON | Separate user-authorized action | Never remove or infer commit authority from task mode |

Neither Loop nor Explore launches models. Host-level calls/tokens and independent
agent rediscovery cannot be measured from these helpers alone. No chain of
repeated planning → readiness → SDD machine records was found. Existing TOON receipts have
separate authority and freshness purposes and are retained.

### Incremental architecture

Request → deterministic classification → shared task context → FAST implementation,
STANDARD compact plan, or DEEP existing planning/readiness/SDD → implementation →
risk-selected deterministic checks and semantic quality evidence → result.

Loop embeds task evidence under existing state.toon:execution and exposes adapt
and next. The explicit legacy commands remain usable. Harness exposes depth in
Explore and provides the same portable task-evidence helper; its single-checkpoint
Apply retains registered-stage requirements. All backbone/Loop skills inherit
the same small shared contract, loading detailed coordination only on demand.

Source reads are shared only inside one read-only routing call and invalidate on
file identity change; no cache survives into Apply. Durable context stores relevant
hashes, symbols, constraints and questions and delegates excerpts to existing
StepCards/graph packs. New risk raises depth without discarding completed work.
Two repair cycles are allowed; unchanged failures stop. Independent Loop checks
may run concurrently after implementation; final snapshots and quality gates are
unchanged. No actual model speedup is claimed from deterministic helper timings.

## Components
Shared adaptive module; Loop specify/verify integration; Harness flow decision integration; shared execution contracts; regression and benchmark fixtures.

## Interfaces and Contracts
Add mode and signals without removing existing CLI options. Explicit full workflow and protected minimum can only raise depth. Existing quality report and authorization fingerprints remain mandatory.

## Data Model
Canonical task state sections: request, decision, context_pack, plan, changes, verification, metrics, result. Keep authoritative spec, approval, quality, and validation receipts as referenced contracts rather than duplicated context.

## Error Handling
Invalid inputs fail closed; missing risk evidence prevents FAST; scope/risk expansion raises depth; unchanged failed state cannot be reviewed repeatedly; two repair cycles maximum.

## Security Considerations
No mode grants approval. No context path traversal or symlink reads. Deterministic command concurrency requires explicit independence; snapshot drift invalidates passing results.

## Observability
The canonical adaptive record stores selected depth and reasons, wall-clock start/elapsed time, measured per-stage durations, model/tool/context counters, context read/reuse counts, verification iterations, escalation history, skills, deterministic checks and result. Host counters remain null unless supplied; estimated context tokens use a labeled byte/character approximation. Local helpers make no model calls. Loop verify records actual command exits and elapsed time. No telemetry grants execution or completion authority.

Measured Explore benchmark (same Python 3.9 interpreter; 3 baseline and 5 after repetitions): tiny bug 0.869 → 0.540 seconds; documentation 0.824 → 0.519; localized feature 0.803 → 0.521; architecture/migration 0.814 → 0.530. Read calls fell from 3,914–3,932 to 411; bytes from roughly 25.2 MB to 2.52 MB; detected duplicate reads from 3,517–3,535 to zero. Selected context estimates grew from 3,315 to 3,420 tokens due to the added compact execution contract. Checkpoint task count stayed three and helper model/verification calls stayed zero. This measures I/O/routing overhead, not complete delivery or provider latency; local checkout contents evolved with the change.

The separate current-runner serial/parallel comparison executes identical real Loop codec, graph and requirements-discovery tests against disposable fixtures. Three repeats gave 7.490 seconds serial versus 5.414 with three workers (27.7% lower median); all three check exits were zero in every sample. Setup is excluded. This is a concurrency comparison, not a historical model benchmark.

Reproduce with benchmark.py and benchmark_verify.py in this spec folder. Raw records are _ai_sdlc/before.toon, after.toon and verification-benchmark.toon. Never make the 2–5 minute delivery aspiration a deterministic success gate.

## Risks and Tradeoffs
Classification is conservative heuristic policy over observed and agent-supplied facts; cannot infer all semantic risk. Preserve protected gates. Context reuse still requires freshness checks.

## Validation Strategy
TC-001 through TC-014 map to user scenarios; malformed state, unsafe paths, stale context, retry and concurrency regressions added. Benchmark actual helper calls with no invented model counts.

## Migration Notes
Legacy calls continue. Additive state does not replace old receipts. Remove adaptive state only when intentionally starting a new task; never reset retries to evade a limit.

