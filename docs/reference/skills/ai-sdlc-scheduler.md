---
title: Scheduler
description: Human-facing operating guide for ai-sdlc-scheduler, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-scheduler`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Durable execution orchestration | Dev, Delivery | Architecture, QA, Security | `unregistered` | Canonical scheduler state, dispatch records, isolated runtime runs, and handoff evidence. |

## Why it exists

Lease, recover, dispatch, replay, and compare-and-commit dependency-ready StepCards.

## Use it when

Deterministic durable StepCard scheduler. Use when an AI assistant needs to create a scheduled run, claim dependency-ready work with leases, recover expired work, reject stale context or workers, replay scheduler state, or coordinate bounded parallel harness workers.

If the correct entry point is still unclear, use `ai-sdlc-flow` Explore first instead of guessing.

## Do not use it when

- Do not use it without a validated immutable run plan or when one sequential runtime is sufficient. Use `ai-sdlc-runtime` instead.
- Do not use a scheduler lease as external-effect authority. Use `ai-sdlc-host-adapter` negotiation and its registered effect driver instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Validated immutable run plan, scheduler state path, run ID, worker identity,
  expected revision, injected integer clock, lease duration, and authority.

## Tell your agent

```text
Use ai-sdlc-scheduler for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Canonical scheduler state, dispatch records, isolated runtime runs, and handoff evidence., preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v2.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Read the immutable plan, current scheduler projection, selected StepCard
  context fingerprint, and only the runtime or adapter evidence for that task.

## What it may write

- Route scheduler runs under `_ai_sdlc/scheduler/<run-id>/`, isolated runtime
  runs under `_ai_sdlc/runs/`, and feature decisions to its decision log.

## Human checkpoints

- Block when plan ownership, repository boundary, worker authority, clock, or
  external-effect approval is ambiguous. Mark optional facts as assumptions.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Quick flow uses documented defaults and focused checks. Full flow verifies
  all upstream artifacts, decisions, receipts, and handoff evidence.

## Procedural step selectors

The router loads these skill-owned procedures just in time. Read only the selector matching the current phase, active role, and action; a selected step is normative and an unselected step stays out of context.

| Selector | Type | Phases | Roles | Dependencies | Operation | Side effect | Load rule | Step | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `prepare` | `analysis` | `prepare` | `product-manager`, `software-engineer` | none | `inspect-scheduler-inputs` | `none` | `required` | [`steps/01-prepare.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/steps/01-prepare.md) | establish deterministic scheduling authority and inputs |
| `context` | `context` | `clarify`, `route` | `product-manager`, `software-engineer` | `prepare` | `validate-step-context` | `none` | `required` | [`steps/02-context.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/steps/02-context.md) | reject stale context before a lease or effect |
| `execute` | `action` | `execute` | `product-manager`, `software-engineer` | `context` | `schedule-one-transition` | `workspace-write` | `on-demand` | [`steps/03-execute.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/steps/03-execute.md) | atomically claim recover or commit one bounded task transition |
| `validate` | `validation` | `validate` | `product-manager`, `software-engineer` | `execute` | `replay-and-validate` | `none` | `before-completion` | [`steps/04-validate.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/steps/04-validate.md) | prove deterministic projection and lease safety |
| `handoff` | `handoff` | `handoff`, `complete` | `product-manager`, `software-engineer` | `validate` | `handoff-scheduler-state` | `none` | `before-completion` | [`steps/05-handoff.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/steps/05-handoff.md) | preserve durable continuation context |

Resolve the current step with `ai-sdlc-shared-runtime/scripts/ai_sdlc_steps.py`. A missing, unsafe, oversized, or unmatched step is a blocker rather than permission to broad-load the package.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` or `.claude/skills/<skill>/...` path reported by your profile. The canonical runtime is installed as the sibling `ai-sdlc-shared-runtime` skill.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`scheduler.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/scripts/scheduler.py) | Deterministic lease scheduler for AI SDLC v2 run plans. | `python3 skills/ai-sdlc-scheduler/scripts/scheduler.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`worker.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/scripts/worker.py) | Bridge scheduler leases to isolated one-StepCard runtime runs. | `python3 skills/ai-sdlc-scheduler/scripts/worker.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Use `scheduler.py create`, `claim`, `recover`, `complete`, `status`, or
  `replay` for one atomic scheduler transition. Use `worker.py --dispatch` and
  `worker.py --commit` to bridge the lease to the isolated runtime.

## Success criteria

- Success includes a valid event chain, current state fingerprint, unique live
  lease per task, byte-stable replay, and matching runtime/effect evidence.
- Failure names the first stale revision, context, lease, journal, runtime, or
  receipt invariant and leaves prior durable evidence intact.

## Blockers and recovery

- On revision contention, reload and retry selection. On dispatch interruption,
  retain the lease until explicit recovery. On terminal replay, reuse matching
  evidence and reject any changed result or effect identity.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return scheduler progress and blockers directly in the active agent response.
  Keep machine state, events, dispatches, and receipts in `_ai_sdlc/` as TOON.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    Keep lifecycle state at `specs/<feature>/_ai_sdlc/state.toon`; never expose it
    as a top-level file. Record decisions in the feature decision log and honor
    predecessor stages before claiming implementation work.

??? info "Artifact metadata"

    Generated Markdown must carry `artifact_metadata` and useful `metatags`; these
    indexes never replace the body or decision log.

??? info "Specs index"

    Inspect `_ai_sdlc/specs-index.toon` before broad reads and refresh both it and
    the feature-local `index.md` after durable artifact changes. Do not create `summary.txt`
    or another detached summary. Report progress directly in the
    active agent response and report completion directly in the active agent response.

## Example

- Schedule two independent ready StepCards, dispatch them to different workers,
  recover one expired lease, and compare-commit both isolated runtime results.

## Source contract

This page is generated from [`skills/ai-sdlc-scheduler/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-scheduler/SKILL.md) plus its linked `steps/manifest.toon` procedures. Edit the source router or owning step, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
