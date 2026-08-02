---
title: Operate the scheduler
description: Lease dependency-ready StepCards, recover expired work, and commit only terminal runtime evidence.
---

# Operate the scheduler

## Goal

Execute an immutable `ai-sdlc-run-plan/v2` through deterministic leases while
preserving context freshness, retry limits, exact-once terminal results, and a
replayable TOON event chain.

## Procedure

Create state with an injected clock, never wall-clock discovery:

```bash
python3 .agents/skills/ai-sdlc-scheduler/scripts/scheduler.py create \
  --plan run-plan.toon --state scheduler-state.toon \
  --run-id delivery-016 --now 1785700000 --max-parallelism 2
```

Read the current revision, then dispatch one ready StepCard into an isolated
runtime sub-run:

```bash
python3 .agents/skills/ai-sdlc-scheduler/scripts/worker.py . --dispatch \
  --plan run-plan.toon --state scheduler-state.toon \
  --dispatch-record dispatch.toon --expected-revision 0 \
  --worker worker-a --lease-seconds 300 --now 1785700001
```

The dispatch record binds the lease nonce, scheduler revision, StepCard,
context fingerprint, and one-task runtime run. Execute and terminally record
that runtime task before calling `worker.py --commit` with the returned
revision, worker, nonce, state, dispatch record, and a later injected clock.
The scheduler rejects a claim whenever the configured number of active leases
has been reached.

For long-running work, use `scheduler.py heartbeat` with the task, matching
worker and nonce, current revision, positive lease duration, and injected
clock. A heartbeat must extend a still-live lease and becomes a journal event;
it cannot revive expired or foreign work.

After a crash or timeout, run `scheduler.py recover` with the exact current
revision and a clock at or after lease expiry. The expired lease returns to
pending without erasing its attempt. A late worker with the stale nonce cannot
commit.

## Verify

Run `scheduler.py replay --state scheduler-state.toon` and compare its
fingerprint and projection with `status`. Replay reconstructs mutable state from
the immutable task definitions and hash-linked events. Identical inputs must
produce byte-identical TOON. Preserve the state and event files when any hash,
revision, context, worker, or nonce check fails.

## Context boundary

The scheduler never rebuilds or widens context. It accepts only a validated
StepCard context fingerprint and rejects a stale claimant. The worker carries
that exact context into the isolated runtime sub-run; a new attempt must obtain
a freshly compiled context pack before a new lease.
