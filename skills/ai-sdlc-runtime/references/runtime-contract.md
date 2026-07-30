# Resumable Runtime Contract

## Plans and readiness

A plan is immutable after start. Task IDs are unique, dependencies exist, and
the graph is acyclic. A task is ready only when it is pending, has attempts
remaining, and every dependency succeeded. Ready tasks sort by plan order then
ID. Only one task may be running; repeated selection returns that task without
another attempt or event.

## Journal and recovery

Every transition appends one canonical event file named
`journal/<sequence>.toon` with a contiguous sequence, previous-event
fingerprint, and its own fingerprint. The immutable `plan.toon` and journal are
authoritative; `state.toon` is an atomic replay-derived projection. Replay
validates the hash chain, plan identity, task-planned coverage, and the exact
`planned → started → terminal → evidence → result` boundary. Missing, corrupt,
or stale projections are recoverable from a valid journal; invalid history
fails closed. Mutations acquire the per-run lock before replay and never
replace an existing journal sequence.

## Budgets, retries, and stops

Every recorded task result consumes one step. Failed outcomes consume one
failure; all outcomes add bounded reported tokens. Retryable failures return to
pending only through a journaled retry event. Maximum attempts, steps, failures,
and tokens produce exact stop reasons. Blocked tasks pause with their recorded
reason. A deliberate stop is terminal and preserves its reason.

## Completion and commits

Success requires a 64-character result fingerprint. Side-effecting success
requires an effect receipt. Tasks marked `after-step` also require a
7-to-64-character hexadecimal commit identity. The run completes only when
every task succeeded. A completion fingerprint binds the result record,
evidence set, and effect receipt at the terminal boundary. Repeating an
identical completion is idempotent; a conflicting replay fails closed. A
process interrupted after terminal or evidence persistence resumes only the
missing protocol events and never repeats the recorded effect.
