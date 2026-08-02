# Execute — AI SDLC Scheduler

## Entry

Context is current and mutation authority is explicit.

## Procedure

Claim using the expected revision, stable worker identity, bounded duration,
and injected clock. Dispatch through the runtime. Commit only with the matching
nonce; reload on contention. Recover expired work through a journaled mutation.

Use `scripts/worker.py` to create one isolated runtime run per leased StepCard.
Run negotiated side effects only through the host adapter effect driver and
pass its receipt into runtime completion. If dispatch fails after a lease is
durable, preserve the lease and let explicit expiry recovery make the task
ready; never delete state or manufacture a terminal result.

## Script Usage

- Use `scheduler.py create`, `claim`, `recover`, `complete`, `status`, or
  `replay` for one atomic scheduler transition. Use `worker.py --dispatch` and
  `worker.py --commit` to bridge the lease to the isolated runtime.

## Inputs

- Read the immutable plan, current scheduler projection, selected StepCard
  context fingerprint, and only the runtime or adapter evidence for that task.

## Exit

One bounded transition is durably recorded with its new revision.
