# Scheduler contract

The scheduler is the single writer of its canonical state projection. Each
mutation holds an exclusive state lock, checks the caller's expected revision,
appends a fingerprint-linked event, increments the revision, recomputes ready
tasks in lexical order, and atomically replaces the projection.

A lease binds task, worker, attempt, scheduler revision, issue time, expiry, and
nonce. Only the matching worker and nonce may commit. Once expired, the old
lease cannot commit even when it later returns. Recovery returns the task to
pending without clearing its attempt count. The fingerprinted scheduler state
sets a positive maximum parallelism and refuses claims while that many leases
are active. A matching worker may heartbeat only a live lease and only by
moving its expiry forward; heartbeat and recovery are explicit journal events.

Context freshness is checked before issuing a lease. External-effect execution
must additionally use the StepCard idempotency key and effect receipt contract;
the scheduler lease does not replace effect idempotency.

The injected integer clock is evidence, not hidden environment state. Replay
reconstructs every mutable task field from immutable task definitions and the
event chain; it does not trust the stored projection. The same journal must
produce byte-identical canonical TOON.
