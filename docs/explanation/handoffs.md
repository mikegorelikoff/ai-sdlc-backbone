---
title: Workflow handoffs
description: How every durable workflow communicates result, blockers, required next work, and optional opportunities.
---

A workflow is not complete when it produces a file; it is complete when the next participant can understand the outcome and continue safely.

## The common contract

The handoff contains `result`, `blockers`, `next_required`, and `next_optional`. Every action explains its reason, exact command, and expected artifact. Required work is separated from useful but non-blocking improvement.

## Why exact commands matter

Skill names and flags are public workflow contracts. An exact command reduces routing ambiguity, preserves quick/full intent, and lets deterministic helpers validate the same transition.

## Relationship to navigation

Flow Explore infers the next action from intent and bounded repository evidence. A workflow handoff knows what just happened. When both use the same state, policy, capability registry, and artifact contracts, their recommendations should agree.

## Resumable runtime

A handoff explains what should happen next; a runtime records whether bounded
work actually started and how it ended. Versioned run plans define task
dependencies, input identity, retry limits, budgets, and commit boundaries.

The runtime appends one hash-chained TOON event under
`journal/<sequence>.toon` before atomically replacing the replay-derived
`state.toon`. If a process stops between those writes, replay repairs the state
projection from the immutable plan and journal. Repeating task selection
returns the already-running task, and repeating identical completion evidence
does not create another event.

Ready tasks require all dependencies to have succeeded. Steps, failures, and
recorded tokens have separate budgets and stop reasons. Blocked work pauses with
its cause; retry exhaustion is distinct from budget exhaustion. A task declared
as a commit boundary cannot succeed until its result fingerprint and commit SHA
are recorded together.

Runtime state is intentionally host-neutral. It does not execute commands or
create commits; later workflow and adapter layers perform those actions and
return exact evidence to the journaled state machine.

Declarative workflow planning validates skill nodes and their canonical
entrypoints, evaluates bounded conditions, preserves explicit approval owners,
and compiles each eligible skill graph into one runtime-compatible plan.
Dependency waves are deterministic views bounded by requested concurrency;
the embedded task graph remains sequentially safe.

Every cross-component handoff carries the same StepCard identity, operation,
capabilities, side-effect class, gates, outputs, context decision, evidence
requirements, idempotency scope, and fingerprints. A host adapter may map those
semantics to a native operation or a registered equivalent fallback, but it
cannot weaken an approval, context, or evidence boundary.

Handoffs keep delivery continuous across roles, assistants, sessions, and context compaction without turning the conversation transcript into a dependency.
